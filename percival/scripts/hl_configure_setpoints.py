'''
Created on 17 May 2016

@author: gnx91527
'''


import argparse
import xlrd

from percival.log import log
from percival.scripts.util import PercivalClient
from percival.detector.spreadsheet_parser import SetpointGroupGenerator


def options():
    parser = argparse.ArgumentParser(description="Load named-setpoints into odin from xls spreadsheet. Existing setpoints will be kept, or silently overwritten.")
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    parser.add_argument("-i", "--input", nargs="+", required=True, action='store', help="Input spreadsheets to parse")
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    parser.add_argument("--textdump", help="list setpoint to stdout (setpoint_id or 'all')")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    ini_str = "";
    sgg = SetpointGroupGenerator()
    for xls in args.input:
      workbook = xlrd.open_workbook(xls)
      ini_str += sgg.generate_ini(workbook)

    if args.textdump:
        setpoint_we_want = args.textdump;
        if setpoint_we_want == "all":
          print (ini_str);
        else:
          # this is a bit hacky. but I'm not changing the spreadsheetparser
          lines = ini_str.splitlines(False);
          key = "Setpoint_name = \"{}\"".format(setpoint_we_want);
          on = False;
          for l in lines:
            if l == key:
              on = True;
            if on:
              print (l)
              if l == "":
                on = False;

    else:
        pc = PercivalClient(args.address)
        result = pc.send_configuration('setpoints',
                                       ini_str,
                                       'hl_configure_setpoints.py',
                                       wait=(args.wait.lower() == "true"))
        log.info("Response: %s", result)


if __name__ == '__main__':
    main()
