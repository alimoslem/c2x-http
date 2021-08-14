#!/usr/bin/env python3

'''
this script is for starting server for listening and other configs
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from modules.logger import Logger
from threading import Thread
from colorama import Fore

serverLogger = Logger(file_name='server')
serverModule = None


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


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes('<h1>test</h1>', 'UTF-8'))

    def log_message(self, format, *args):
        pass