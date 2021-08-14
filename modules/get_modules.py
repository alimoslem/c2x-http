#!/usr/bin/env python3

'''
this script contains modules to get data from files and return desired values
'''

import json
from random import randint
from hashlib import md5


def get_config_value(main_key):

    '''
    this function is for reading main/core/config.json file and return value for desired key
    '''

    file = open('main/core/config.json')
    config_file = json.load(file)
    try :
        value = config_file[main_key]
    except :
        print('Error finding : ' + main_key + ' in config.json')
    else:
        return value

def generate_zombie_token():
    '''
    create a random token for zombies
    '''
    random_number1 = str(randint(1, 1000000))
    random_number2 = str(randint(1, 1000000))
    random_number3 = str(randint(1, 1000000))

    combined = f'{random_number1}{random_number2}{random_number3}'
    my_hash = md5()
    my_hash.update(combined.encode())
    token = str(my_hash.hexdigest())
    return token