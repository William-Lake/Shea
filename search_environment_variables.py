from argparse import ArgumentParser, RawTextHelpFormatter
import ctypes
import os
import re

import colorama
from colorama import Fore, Back, Style



SEARCH_KEYS = ['keys','k']

SEARCH_VALUES = ['values','v']

SEARCH_BOTH = ['both','b']

SEARCH_CHOICES = SEARCH_KEYS + SEARCH_VALUES + SEARCH_BOTH

def gather_string_indexes(search_target,search_string):

    string_indexes = []

    for match in re.finditer(search_string.lower(),search_target.lower()):

        string_indexes.append(match.start())

    return string_indexes

def provide_output(name, value, var_part_to_search, search_string):

    out_str = f'{name} : {value}'

    out_str_parts = []

    if var_part_to_search not in SEARCH_BOTH:

        if var_part_to_search in SEARCH_VALUES:

            out_str_parts.append(f'{name} : ')

            out_str = value

        else:

            out_str = name    

    string_indexes = gather_string_indexes(out_str,search_string)

    if string_indexes:

        # This smells about this...

        '''
        for each idx
            add x, search string, x to results
            determine end substring index
                the next idx if there is one, else the string length
            add the search target substring from (idx + 2 + str length) -> next idx
        '''    

        for idx, str_idx in enumerate(string_indexes):

            out_str_parts.extend([
                Fore.MAGENTA,
                out_str[str_idx:str_idx+len(search_string)],
                Fore.RESET
            ])

            sub_str_strt_idx = str_idx + len(search_string)

            sub_str_end_idx = len(out_str) if idx == len(string_indexes) - 1 else string_indexes[idx + 1]

            out_str_parts.append(out_str[sub_str_strt_idx:sub_str_end_idx])

        if var_part_to_search in SEARCH_KEYS:

            print(''.join(out_str_parts) + f' : {value}')

        else:

            print(''.join(out_str_parts))
def main(args):

    for name, value in os.environ.items():

        if name.lower() == 'path': continue

        provide_output(name, value, args.var_part_to_search, args.search_string)

def gather_args():

    arg_parser = ArgumentParser(formatter_class=RawTextHelpFormatter,description='Searches environment variables keys and/or values for some text.',prog='SHEA.exe',epilog=f'''
======================

{Fore.YELLOW}Usage Examples{Fore.RESET}

Search environment variable keys and values for "XDG"

    {Fore.MAGENTA}SHEA.exe XDG{Fore.RESET}

Search environment variable keys for "XDG"

    {Fore.MAGENTA}SHEA.exe keys XDG{Fore.RESET}

Search environment variable values for "XDG"

    {Fore.MAGENTA}SHEA.exe values XDG{Fore.RESET}
''')

    arg_parser.add_argument('var_part_to_search',help='The part of the environment variables to search.',choices=SEARCH_CHOICES,type=str.lower,default='b',nargs='?')

    arg_parser.add_argument("search_string",help='The text to search for.')

    return arg_parser.parse_args()

def is_admin():  # https://raccoon.ninja/en/dev/using-python-to-check-if-the-application-is-running-as-an-administrator/

    try:

        is_admin = os.getuid() == 0

    except AttributeError:

        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin

def print_banner():

    print(fr'''{Fore.MAGENTA}
  ___ _  _ ___   _   
 / __| || | __| /_\  
 \__ \ __ | _| / _ \ 
 |___/_||_|___/_/ \_\
                     
{Fore.YELLOW + Style.BRIGHT}SearcH Environment vAriables{Style.RESET_ALL}
''')

    if not is_admin():

        print(f'{Fore.BLACK + Back.WHITE}You\'re not running this script from an administrative command prompt; results may be incomplete.{Style.RESET_ALL}\n')

if __name__ == "__main__":

    colorama.init()

    print_banner()

    args = gather_args()

    main(args)

