"""
Created on 15 July 2016

@author: Alan Greer
"""


import os

from percival_detector.log import log
from percival_detector.carrier.txrx import TxRxContext
from percival_detector.carrier.encoding import (encode_message, decode_message)

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")


def main():
    log.info("Scanning buffer shortcut...")

    with TxRxContext(board_ip_address) as trx:
        trx.timeout = 1.0
        addr = 0x014A
        expected_bytes = None

        msg = encode_message(addr, 0x00000000)
        log.debug("Querying address: %X ...", addr)
        try:
            resp = trx.send_recv(msg, expected_bytes)
        except RuntimeError:
            log.exception("Error sending msg: %s", msg)

        data = decode_message(resp)
        log.info("Got from addr: 0x%04X bytes: %d  words: %d", addr, len(resp), len(data))
        for (a, w) in data:
            log.info("           (0x%04X) 0x%08X", a, w)


if __name__ == '__main__':
    main()
