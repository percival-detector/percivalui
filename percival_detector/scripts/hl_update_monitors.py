'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse

from percival_detector.log import log
from percival_detector.scripts.util import PercivalClient


def options():
    desc = """Force the driver to update the monitor status values
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    pc = PercivalClient(args.address)
    result = pc.send_command('cmd_update_monitors', 'hl_update_monitors.py', wait=(args.wait.lower() == "true"))
    log.info("Response: %s", result)


if __name__ == '__main__':
    main()
