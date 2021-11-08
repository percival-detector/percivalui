'''
Created on 13 May 2015

@author: Ulrik Pedersen
'''


from builtins import range  # pylint: disable=W0622
import os

from percival.log import log
from percival.carrier.txrx import TxRxContext
from percival.carrier.encoding import (encode_message, decode_message)
from percival.carrier.const import *

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")

scanrange = list(range(READBACK_HEADER_SETTINGS_LEFT.start_address, READBACK_MONITORING_SETTINGS_PLUGIN.start_address+1, 1))

def main():
    log.info("Scanning shortcuts...")

    try:
        with TxRxContext(board_ip_address) as trx:
            trx.timeout = 1.0

            expected_bytes = None
            #for addr, expected_bytes in scanrange:
            for addr in scanrange:
                msg = encode_message(addr, 0x00000000)

                log.debug("Querying address: %X ...", addr)
                try:
                    resp = trx.send_recv(msg, expected_bytes)
                except RuntimeError:
                    log.exception("no response (addr: %X)", addr)
                    continue
                data = decode_message(resp)
                log.info("Got from addr: 0x%04X bytes: %d  words: %d", addr, len(resp), len(data))
                for (a, w) in data:
                    log.info("           (0x%04X) 0x%08X", a, w)
    except:
        log.info("Exception in TxRx: Check PERCIVAL_CARRIER_IP is correct")
                
if __name__ == '__main__':
    main()
