#!/usr/bin/env python3

from colorama import Fore

note_1 = Fore.RED + '*** ' + Fore.RESET + 'You have to run C2X-HTTP with root privileges for using C2 listening port from 1-1023' + Fore.RED + ' ***' + Fore.RESET

notes = note_1

def print_notes():
    print(notes)