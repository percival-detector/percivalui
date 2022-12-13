'''
Created on 19 June 2019

@author: gnx91527
'''


import sys
import argparse
import logging

from percival_detector.log import log
from percival_detector.carrier import const
from percival_detector.scripts.util import DAQClient


SCRIPT_NAME = "test_fp.py"


def options():
    desc = """Test script to demonstrate starting an acquisition
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    args = parser.parse_args()
    return args


def parse_response(response):
    log.info("Response: %s", response)
    if 'error' in response:
        log.info("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    args = options()
    log.setLevel(logging.DEBUG)
    dc = DAQClient(args.address)

    log.info("Test FP")

    parse_response(dc.set_frames(10))
    parse_response(dc.set_file_path('/tmp/'))
    parse_response(dc.set_file_name('test_01'))
    parse_response(dc.start_writing())
    parse_response(dc.get_status())


if __name__ == '__main__':
    main()
