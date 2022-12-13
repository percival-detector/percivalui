'''
Created on 31 Jan 2018

@author: gnx91527
'''


import sys
import argparse

from percival_detector.log import log
from percival_detector.carrier import const
from percival_detector.carrier.registers import UARTRegister
from percival_detector.scripts.util import PercivalClient

system_settings = [name for name in UARTRegister(const.SYSTEM_SETTINGS).fields.map_fields]
system_settings.sort()
system_settings = "\n\t".join(system_settings)


def options():
    desc = """Send a System Command to the Percival Carrier Board
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    action_help = "System setting to set. Valid settings are: %s" % system_settings
    parser.add_argument("-s", "--setting", action="store", default="ACQUISTION_Acquisition_mode", help=action_help)
    value_help = "The value to set (default 0)"
    parser.add_argument("-v", "--value", action="store", default=0, help=value_help)
    wait_help = "Wait for the command to complete (default true)"
    parser.add_argument("-w", "--wait", action="store", default="true", help=wait_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    data = {
        'setting': args.setting,
        'value': args.value
    }

    pc = PercivalClient(args.address)
    result = pc.send_command('cmd_system_setting',
                             'hl_set_system_setting.py',
                             arguments=data,
                             wait=(args.wait.lower() == "true"))
    log.info("Response: %s", result)


if __name__ == '__main__':
    main()
