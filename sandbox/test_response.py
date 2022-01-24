'''
Created on 2 August 2017

@author: Alan Greer
'''

import argparse
import os

from percival.log import logger
from percival.carrier.txrx import TxRxContext
from percival.carrier.encoding import (encode_message, decode_message)

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", action="store", default=board_ip_address, help="IP address of Percival hardware")
    parser.add_argument("-a", "--address", action="store", default=0x02E0, help="Address of word to write")
    parser.add_argument("-v", "--value", action="store", default=0x00000000, help="Value of word to write")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log = logger("percival_sandbox")

    log.info("Sending single word to hardware...")

    try:
        with TxRxContext(args.ip) as trx:
            trx.timeout = 1.0

            expected_bytes = None
            # for addr, expected_bytes in scanrange:
            msg = encode_message(args.address, args.value)
            log.debug("Querying address: %X ...", args.address)
            try:
                resp = trx.send_recv(msg, expected_bytes)
            except RuntimeError:
                log.exception("no response (addr: %X)", args.address)
            data = decode_message(resp)
            log.info("Got from addr: 0x%04X bytes: %d  words: %d", args.address, len(resp), len(data))
            for (a, w) in data:
                log.info("           (0x%04X) 0x%08X", a, w)
    except:
        log.info("Exception in TxRx: Check PERCIVAL_CARRIER_IP is correct")


if __name__ == '__main__':
    main()
