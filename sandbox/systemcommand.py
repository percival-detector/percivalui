'''
Created on 17 May 2016

@author: gnx91527
'''


import sys
import argparse

from percival.log import log

from percival.carrier import const
from percival.carrier.txrx import TxRxContext
from percival.carrier.system import SystemCommand
from percival.detector.detector import PercivalParameters

system_commands = "\n\t".join([name for name, tmp in list(const.SystemCmd.__members__.items())])


def options():
    desc = """Send a System Command to the Percival Carrier Board
    """
    parser = argparse.ArgumentParser(description=desc)
    action_help = "System command to send. Valid commands are: %s" % system_commands
    parser.add_argument("-a", "--action", action="store", default="no_operation", help=action_help)
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    try:
        system_command = const.SystemCmd[args.action.lower()]
    except KeyError:
        log.error("Invalid command \'%s\' supplied to --action", args.action)
        print("Invalid command: \'%s\'" % args.action)
        print("Valid commands are: \n\t%s" % system_commands)
        sys.exit(-1)

    pcvl_params = PercivalParameters()
    pcvl_params.load_ini()
    log.info("Connecting to Carrier IP: %s", pcvl_params.carrier_ip)

    with TxRxContext(pcvl_params.carrier_ip) as trx:
        log.debug("Connected to %s", pcvl_params.carrier_ip)
        print("Sending System Command: %s", system_command.name)
        sys_cmd = SystemCommand(trx)
        sys_cmd.send_command(system_command)


if __name__ == '__main__':
    main()
