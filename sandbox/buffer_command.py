"""
Created on 15 July 2016

@author: Alan Greer
"""


import os

import argparse

from percival_detector.log import log
from percival_detector.carrier.txrx import TxRxContext
from percival_detector.carrier.registers import UARTRegister
from percival_detector.carrier import const
#from percival_detector.carrier.encoding import encode_message
#from percival_detector.carrier.buffer import BufferCommand

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", action="store", default="write", choices=["write", "read", "soft_reset"],
                        help="Which command to submit")
    parser.add_argument("-b", "--board", action="store", default="A", choices=["A", "B", "both", "plugin", "sensor"],
                        help="Board type")
    parser.add_argument("-a", "--address", action="store", type=int, default=1,
                        help="Starting address for operation (0 not valid, 1..n)")
    parser.add_argument("-n", "--number", action="store", type=int, default=16,
                        help="Number of words to read/write")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)
    log.info("Applying buffer command...")

    cmd_type = 0
    board = 0

    # Check the command type
    if args.command.upper() == "WRITE":
        cmd_type = 0
    if args.command.upper() == "READ":
        cmd_type = 1
    if args.command.upper() == "SOFT_RESET":
        cmd_type = 2

    # Check argument board type
    if args.board.upper() == "A":
        board = 1
    if args.board.upper() == "B":
        board = 2
    if args.board.upper() == "BOTH":
        board = 3
    if args.board.upper() == "PLUGIN":
        board = 4
    if args.board.upper() == "SENSOR":
        board = 5

    #cmd = cmd_type << 7 + board << 6 + int(args.number) << 4 + int(args.address)

    with TxRxContext(board_ip_address) as trx:
        trx.timeout = 10.0

        #buffer_cmd = BufferCommand(trx, const.BufferTarget.mezzanine_board_A)
        #buffer_cmd.send_command(const.BufferCmd.write, 10, 1)

        addr = 0x00F9

        #expected_bytes = None
        #msg = encode_message(addr, cmd)

        reg_command = UARTRegister(const.COMMAND)
        reg_command.initialize_map([0,0,0])

        # First send a no-op
        cmd_msg = reg_command.get_write_cmd_msg(eom=False)[1]
        log.debug("Sending to address: %X ...", addr)
        log.debug("Sending message: %s", cmd_msg)
        try:
            resp = trx.send_recv_message(cmd_msg)
        except RuntimeError:
            log.exception("no response (addr: %X)", addr)
        else:
            log.debug("Response: %s", resp)

        reg_command.fields.buffer_cmd_destination = board
        reg_command.fields.buffer_cmd = cmd_type
        reg_command.fields.buffer_cmd_words = int(args.number)
        reg_command.fields.buffer_cmd_address = int(args.address)
        cmd_msg = reg_command.get_write_cmd_msg(eom=False)[1]
        cmd_msg.num_response_msg = 2
        if board == 3:
            cmd_msg.num_response_msg = 3

        log.debug("Sending to address: %X ...", addr)
        log.debug("Sending message: %s", cmd_msg)
        try:
            resp = trx.send_recv_message(cmd_msg)
#            resp = trx.send_recv(msg, expected_bytes)
        except RuntimeError:
            log.exception("no response (addr: %X)", addr)

        log.debug("Response: %s", resp)
        #for data in resp:
#            addr, value = data
        log.info("Got from addr: 0x%04X words: %d", addr, len(resp))
        for (a, w) in resp:
            log.info("           (0x%04X) 0x%08X", a, w)


if __name__ == '__main__':
    main()
