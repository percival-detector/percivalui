"""
Created on 20 May 2016

@author: Alan Greer
"""

import argparse

from percival.log import log
from percival.detector.standalone import PercivalStandalone


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", action="store_true", help="Download the ini configuration to the board")
    parser.add_argument("-i", "--init", action="store_true", help="Initialise DAC channels on the board")
    parser.add_argument("-c", "--control", action="store", default="tcp://127.0.0.1:8888", help="ZeroMQ control endpoint")
    parser.add_argument("-s", "--status",  action="store", default="tcp://127.0.0.1:8889", help="ZeroMQ status endpoint")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    # Create the stand alone device
    percival = PercivalStandalone(args.load, args.init)

    # Initialise the control endpoint
    percival.setup_control_channel(args.control)

    # Initialise the status endpoint
    percival.setup_status_channel(args.status)

    # Startup the IpcReactor
    percival.start_reactor()


if __name__ == '__main__':
    main()
