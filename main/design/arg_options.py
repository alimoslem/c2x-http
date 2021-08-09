#!/usr/bin/env python3

'''
this is the script for parsing arguments
'''

import argparse


def start_web(use_ssl):
    from web_interface.main_web import main_web_start
    main_web_start(use_ssl=use_ssl)

def parse_args():
    parser = argparse.ArgumentParser(usage='python3 %(prog)s [--web]')

    parser.add_argument('--web', help='Start Web Interface', action='store_true')
    parser.add_argument('--use-https', help='Enable HTTPS for Web Interface', action='store_true')

    args ,unknown = parser.parse_known_args()

    if (args.web):
        use_ssl = None
        if args.use_https:
            use_ssl = True

        start_web(use_ssl=use_ssl)

    else:
        parser.print_help()