'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse
import xlrd

from percival_detector.log import log
from percival_detector.scripts.util import PercivalClient
from percival_detector.control.spreadsheet_parser import MonitorGroupGenerator


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    parser.add_argument("-i", "--input", required=True, action='store', help="Input spreadsheet to parse")
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    workbook = xlrd.open_workbook(args.input)

    mgg = MonitorGroupGenerator(workbook)
    ini_str = mgg.generate_ini()

    pc = PercivalClient(args.address)
    result = pc.send_configuration('monitor_groups',
                                   ini_str,
                                   'hl_configure_monitor_groups.py',
                                   wait=(args.wait.lower() == "true"))
    log.info("Response: %s", result)


if __name__ == '__main__':
    main()
