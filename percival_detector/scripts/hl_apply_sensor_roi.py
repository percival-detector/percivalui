'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse

import percival_detector.log
from percival_detector.scripts.util import PercivalClient

slogger = percival_detector.log.logger("percival_scripts")

def options():
    desc = """Send the apply sensor ROI command to the Percival Carrier Board
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
    slogger.info(args)

    pc = PercivalClient(args.address)
    result = pc.send_command('cmd_apply_roi', 'hl_apply_sensor_roi.py', wait=(args.wait.lower() == "true"))
    slogger.info("Response: %s", result)


if __name__ == '__main__':
    main()
