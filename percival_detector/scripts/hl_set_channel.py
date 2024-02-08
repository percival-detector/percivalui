'''
Created on 17 May 2016

@author: gnx91527
'''


import sys
import argparse
import getpass
from datetime import datetime

import percival_detector.log
from percival_detector.scripts.util import PercivalClient

slogger = percival_detector.log.logger("percival_scripts")

def options():
    desc = """Set a channel value on the Percival Carrier Board
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    channel_help = "Channel to set"
    parser.add_argument("-c", "--channel", action="store", help=channel_help)
    value_help = "Value to set"
    parser.add_argument("-v", "--value", action="store", default=0, help=value_help)
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    read_help = "print current channel-values to stdout"
    parser.add_argument("-r", "--read", action="store_true", default=False, help=read_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    slogger.info(args)
    pc = PercivalClient(args.address)

    if(args.read):
      result = pc.get_status("channel_values");
      print(result);

    else:
      data = {
                 'channel': args.channel,
                 'value': args.value
             }


      result = pc.send_command('cmd_set_channel',
                               'hl_set_channel.py',
                               arguments=data,
                               wait=(args.wait.lower() == "true"))
      slogger.info("Response: %s", result)


if __name__ == '__main__':
    main()
