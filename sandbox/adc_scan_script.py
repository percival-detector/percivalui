'''
Created on 17 May 2016

@author: gnx91527
'''


import sys
import argparse
import time
import logging

from percival_detector.log import log
from percival_detector.carrier import const
from percival_detector.scripts.util import PercivalClient

system_commands = "\n\t".join([name for name, tmp in list(const.SystemCmd.__members__.items())])


def options():
    desc = """Perform a sequence of acquisitions for each scan point
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    #action_help = "System command to send. Valid commands are: %s" % system_commands
    #parser.add_argument("-c", "--command", action="store", default="no_operation", help=action_help)
    #wait_help = "Wait for the command to complete (default true)"
    #parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    #no_of_frames_help = "How many frames to acquire at each point (default 5)"
    #parser.add_argument("-f", "--frames", action="store", default=5, help=no_of_frames_help)
    wait_time_help = "How long (seconds) to pause between each scan point (default 5.0)"
    parser.add_argument("-w", "--wait", action="store", default=5.0, help=wait_time_help)
    parser.add_argument("-r", "--range", default="0,100,20", help="Scan range in integers formatted like this: start,stop,step")
    parser.add_argument("channel", action='store', help="Control Channel to scan")
    args = parser.parse_args()
    args.range = [int(x) for x in args.range.split(',')]
    return args


def main():
    args = options()
    log.info(args)

    pc = PercivalClient(args.address)

    # Create the list of scan points from the users range arg
    scan_range = list(range(*args.range))
    # Ensure that the last point of the range is always included in the list
    # even if the last step is not a full step size.
    if args.range[1] > scan_range[-1]:
        scan_range.append(args.range[1])

    for new_value in scan_range:
        data = {
               'channel': args.channel,
               'value': new_value
        }
        print("Writing Control Channel \'{}\' value = {}".format(args.channel, new_value))
        result = pc.send_command('cmd_set_channel',
                                 'hl_set_channel.py',
                                 arguments=data,
                                 wait=(args.wait.lower() == "true"))
        print("Channel set response: {}".format(result))
        time.sleep(float(args.wait))

        system_command = const.SystemCmd['start_acquisition']
        result = pc.send_system_command(system_command, 'hl_system_command.py', wait=(args.wait.lower() == "true"))
        print("Acquisition set response: {}".format(result))
        time.sleep(float(args.wait))
        #raw_input("Press Enter to continue...")

    print("The scan has completed :)")


if __name__ == '__main__':
    main()
