#!/usr/bin/env python3

'''
this script is for logging terminal messages in file
'''

from os.path import exists

class Logger:

    def __init__(self ,file_name=None):
        self.logs_prefix = 'logs/'
        self.file_path = ''
        if file_name == 'terminal':
            self.file_path = self.logs_prefix + 'terminal.txt'

        elif file_name == 'server':
            self.file_path = self.logs_prefix + 'server.txt'

        elif file_name == 'create_script':
            self.file_path = self.logs_prefix + 'create_script.txt'

        elif file_name is None:
            self.file_path = self.logs_prefix + 'terminal.txt'

        if not exists(self.file_path):
            with open(self.file_path, 'w'):
                pass

    def create_separator(self):
        with open(self.file_path, 'a') as file:
            file.write('\n+---------------------------------+\n')

    def log(self, text, print_text=False):
        with open(self.file_path, 'a') as terminal_file:
            terminal_file.write(text + '\n')
        if print_text:
            print(text)