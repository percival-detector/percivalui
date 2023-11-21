'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse
import signal

import percival_detector.log
from percival_detector.scripts.util import PercivalClient

slogger = percival_detector.log.logger("percival_scripts")

def options():
    desc = """Scan from the current position to a demand setpoint.  Dwell at each point.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    final_help = "Final set-point to scan to"
    parser.add_argument("-f", "--final_setpoint", action="store", help=final_help)
    number_help = "Number of steps in the scan (default 10)"
    parser.add_argument("-n", "--number_of_steps", action="store", default=10, help=number_help)
    delay_help = "Delay time between steps in ms (default 1000)"
    parser.add_argument("-d", "--delay_between_steps", action="store", default=1000, help=delay_help)
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()

    return args


def sigint_handler(signum, frame):
    args = options()
    pc = PercivalClient(args.address)
    result = pc.send_command('cmd_abort_scan', 'hl_safety_setpoint_scan.py')
    slogger.info("Response: %s", result)

signal.signal(signal.SIGINT, sigint_handler)


def main():
    args = options()
    slogger.info(args)

    data = {
               'setpoints': args.final_setpoint,
               'dwell': args.delay_between_steps,
               'steps': args.number_of_steps
           }

    pc = PercivalClient(args.address)
    result = pc.send_command('cmd_scan_setpoints',
                             'hl_safety_setpoint_scan.py',
                             arguments=data,
                             wait=(args.wait.lower() == "true"))
    slogger.info("Response: %s", result)


if __name__ == '__main__':
    main()
