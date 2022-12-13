"""
Created on 15 July 2016

@author: Alan Greer
"""


from builtins import range  # pylint: disable=W0622
import os

import argparse

from percival_detector.log import log
from percival_detector.carrier.txrx import TxRxContext
from percival_detector.carrier.encoding import (encode_message, encode_multi_message, decode_message)

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", default=16, help="Number of addresses to write to")
    parser.add_argument("-v", "--value", default=0, help="Starting value")
    parser.add_argument("-t", "--type", default="constant", help="Data options (constant|increase|decrease)")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)
    log.info("Writing data to buffer...")

    with TxRxContext(board_ip_address) as trx:
        trx.timeout = 10.0

        addr = 0x00D8

        values = []
        if args.type == "constant":
            # TODO: refactor slightly clunky loop
            for n in range(0, args.number):
                values.append(int(args.value))

        if args.type == "increase":
            # TODO: refactor slightly clunky loop
            nval = int(args.value)
            for n in range(0, args.number):
                values.append(nval)
                nval += 1

        if args.type == "decrease":
            # TODO: refactor slightly clunky loop
            nval = int(args.value)
            for n in range(0, args.number):
                values.append(nval)
                nval -= 1
                if nval < 0:
                    nval = 0

        expected_bytes = None
        msg = encode_multi_message(addr, values)

        log.debug("Sending to address: %X ...", addr)
        try:
            for m in msg:
                resp = trx.send_recv(m, expected_bytes)
        except RuntimeError:
            log.exception("no response (addr: %X)", addr)

        addr = 0x014A
        expected_bytes = None

        msg = encode_message(addr, 0x00000000)
        log.debug("Querying address: %X ...", addr)
        try:
            resp = trx.send_recv(msg, expected_bytes)
        except RuntimeError:
            log.exception("no response (addr: %X", addr)

        data = decode_message(resp)
        log.info("Got from addr: 0x%04X bytes: %d  words: %d", addr, len(resp), len(data))
        for (a, w) in data:
            log.info("           (0x%04X) 0x%08X", a, w)


if __name__ == '__main__':
    main()
