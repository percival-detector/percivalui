'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse

import percival_detector.log
from percival_detector.scripts.util import PercivalClient

slogger = percival_detector.log.logger("percival_scripts")

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    parser.add_argument("-i", "--input", required=True, action='store', help="Input settings ini file to apply")
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    slogger.info(args)

    with open(args.input, 'r') as ini_file:
        ini_str = ini_file.read()

    pc = PercivalClient(args.address)
    result = pc.send_configuration('system_settings',
                                   ini_str,
                                   'hl_configure_system_settings.py',
                                   wait=(args.wait.lower() == "true"))
    slogger.info("Response: %s", result)


if __name__ == '__main__':
    main()
