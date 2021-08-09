#!/usr/bin/env python3

'''
this script is for starting program functions
'''

from main.design.banner import print_banner
from main.design.arg_options import parse_args
from main.design.notes import print_notes
from main.design.check_output_files import check_files

def start():
    check_files()
    print_banner()
    print_notes()
    parse_args()