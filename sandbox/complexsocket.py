"""
Created on 13 May 2015

@author: up45
"""

import os

from percival_detector.log import log
from percival_detector.carrier.txrx import TxRxContext
from percival_detector.carrier.encoding import (encode_message, decode_message)

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")

def main():
    """

    :rtype: int
    """
    log.debug("complexsocket...")
    
    with TxRxContext(board_ip_address) as trx:
        
        #msg = encode_message(0x0140, 0x00000000) # Header Settings Carrier shortcut
        #msg = encode_message(0x0141, 0x00000000) # Control Settings Carrier shortcut
        #msg = encode_message(0x0142, 0x00000000)  # Monitoring Settings Carrier shortcut
        msg = encode_message(0x014D, 0x00000000)  # shortcut: Readback READ VALUES CARRIER


        log.debug("as string: %s",str([msg]))
        #trx.tx_msg(msg)
        #trx.tx_msg(msg)
        #resp = trx.rx_msg()
        resp = trx.send_recv(msg)
        log.debug("Device CommandMap: %d bytes: %s", len(resp), [resp])
        resp = decode_message(resp)
        log.info("Got %d words", len(resp))
        log.info(resp)
        
        #msg = encode_message(0x0151, 0x00000000) # ECHO WORD (times out)
        #resp = trx.send_recv(msg)
        #log.debug("ECHO WORD: %d bytes: %s", len(resp), [resp])
        #resp = decode_message(resp)
        #log.info("Got %d words", len(resp))
        #log.info(resp)
    
if __name__ == '__main__':
    main()
