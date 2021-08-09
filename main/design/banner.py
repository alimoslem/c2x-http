#!/usr/bin/env python3

'''
Banner printing script
'''

from colorama import Fore
from random import randint
from modules.get_modules import get_config_value

# Version
app_version = get_config_value('app_version')
version_text = '{version : ' + app_version + '}'
# Link to github
github_link = 'https://github.com/nxenon/c2x-http'

color_list = [Fore.RED,Fore.CYAN,Fore.YELLOW,Fore.GREEN,Fore.LIGHTRED_EX,Fore.LIGHTYELLOW_EX,Fore.MAGENTA]
random_color = color_list[randint(0,len(color_list)-1)]

line_1 = '  .oooooo.     ' + random_color + '.oooo.' + Fore.RESET + '   oonoooo  ooooo'
line_2 = ' d8P\'  `Y8b  ' + random_color + '.dP""Y88b' + Fore.RESET + '   `8x88    d8\'' + '    ' + Fore.LIGHTBLUE_EX + ' HTTP(S) Version' + Fore.RESET
line_3 = '888                ' + random_color + ']8P\'' + Fore.RESET + '    Ye88..8P'
line_4 = '888              ' + random_color + '.d8P\'' + Fore.RESET + '      `8n88\''
line_5 = '888            ' + random_color + '.dP\'' + Fore.RESET + '        .8PYo88.' + '       ' + Fore.LIGHTBLUE_EX + version_text + Fore.RESET
line_6 = '`88b    ooo  ' + random_color + '.oP' + Fore.RESET + '     ' + random_color + '.o' + Fore.RESET + '   d8\'  `n88b' + '      ' + Fore.LIGHTCYAN_EX + github_link + Fore.RESET
line_7 = ' `-nxenon-\'  ' + random_color + '8888888888' + Fore.RESET + ' o888o  o88888o'

banner_logo = line_1 + '\n' + line_2 + '\n' + line_3 + '\n' + line_4 + '\n' + line_5 + '\n' + line_6 + '\n' + line_7 + '\n'

def print_banner():
    print(banner_logo)