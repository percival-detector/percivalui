'''
Created on 17 May 2016

@author: gnx91527
'''


import sys
import argparse

import percival_detector.log
from percival_detector.carrier import const
from percival_detector.scripts.util import PercivalClient

slogger = percival_detector.log.logger("percival_scripts")

system_commands = "\n\t".join([name for name, tmp in list(const.SystemCmd.__members__.items())])


def options():
    desc = """Send a System Command to the Percival Carrier Board
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    action_help = "System command to send. Valid commands are: %s" % system_commands
    parser.add_argument("-c", "--command", action="store", default="no_operation", help=action_help)
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    slogger.info(args)

    try:
        system_command = const.SystemCmd[args.command]
    except KeyError:
        slogger.error("Invalid command \'%s\' supplied to --command", args.command)
        print("Invalid command: \'%s\'" % args.command)
        print("Valid commands are: \n\t%s" % system_commands)
        sys.exit(-1)

    pc = PercivalClient(args.address)
    result = pc.send_system_command(system_command, 'hl_system_command.py', wait=(args.wait.lower() == "true"))
    slogger.info("Response: %s", result)


if __name__ == '__main__':
    main()
