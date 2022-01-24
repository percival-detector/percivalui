"""
Encode and decode Carrier Board Xport messages
"""

from builtins import bytes  # pylint: disable=W0622
try:
    import itertools.izip as zip  # pylint: disable=W0622
except ImportError:
    pass

import struct
import logging
logger = logging.getLogger(__name__)

SINGLE_MSG_FMT = b'!HI'

NUM_BYTES_PER_MSG = 6
"""Number of bytes per message. Each message consist of a 2 byte address field and a 4 byte data field"""

DATA_ENCODING='latin-1' # Just because latin-1 allow values from 0-255

END_OF_MESSAGE = bytes('\xFF\xFF\xAB\xBA\xBA\xC1', encoding=DATA_ENCODING)
"""End of message is used in some cases. The EOM word is 0xFFFFABBABAC1"""

msg_packer = struct.Struct(SINGLE_MSG_FMT)


def encode_message(addr, word):
    """Encode a single address and dataword into a bytes-obj of 6 bytes with address and dataword encoded
    
    :param addr: UART address (16bit integer)
    :param word: data word (32bit integer)
    :returns: object of type bytes (or future.types.newbytes.newbytes)
    """
    logger.debug("%s", ([addr, word]))
    encoded_msg = msg_packer.pack(addr, word)
    # Python 2 -> 3 compatibility workaround:
    # In python2 struct.pack() returns a string which we then
    # need to convert to a 'bytes' object.
    if isinstance(encoded_msg, str):
        encoded_msg = bytes(encoded_msg, encoding=DATA_ENCODING)
    logger.debug("encode_message returning: %s", [encoded_msg])
    return encoded_msg


def encode_multi_message(start_addr, words):
    """Encode multiple 32bit words as a multi-message and return list of encoded words,
    each of which consists of 6 bytes: 2 words of address and 4 words of data

    :param start_addr: The UART starting address (a 16bit integer word)
    :param words:      A list of 32bit integer words to be encoded
    :returns: list
    """ 
    logger.debug("%s", ([start_addr, words]))
    addresses = list(range(start_addr, start_addr + len(words)))
    encoded_msg = []
    assert len(addresses) == len(words)
    for addr, word in zip(*[addresses, words]):
        encoded_msg.append(encode_message(addr, word))
    logger.debug("encode_multi_message returning: %s", encoded_msg)
    return encoded_msg


def decode_message(msg):
    """Decode a byte array into a list of (address, dataword) tuples.
    
    The address field is a 16bit integer and the dataword is a 32bit integer.
    
    :param msg: The input message
    :type  msg: bytearray
    :returns:   list
    """
    logger.debug(msg)
    extra_bytes = len(msg)%NUM_BYTES_PER_MSG
    if extra_bytes > 0:
        logger.warning("Too many (%d) bytes in message", extra_bytes)
        msg = msg[:-extra_bytes] # WARNING: we are chopping away some bytes here...
    num_words =  len(msg)//NUM_BYTES_PER_MSG
    fmt = b"!"
    fmt += b"HI" * num_words
    
    msg_unpacker = struct.Struct(fmt)
    addr_word_list = msg_unpacker.unpack(msg)
    
    # reshape the linear list of (addr, word, addr, word, addr, word...) into a 
    # neat [(addr,word), (addr, word) ... ] list
    addr_word_sets = [ aw_set for aw_set in zip(*[iter(addr_word_list)]*2) ]
    logger.debug("Returning: %s", str(addr_word_sets))
    return addr_word_sets

