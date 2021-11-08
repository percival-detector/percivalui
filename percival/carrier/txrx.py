"""
Communications module for the Percival Carrier Board XPort interface.
"""

from builtins import bytes  # pylint: disable=W0622
from future.utils import raise_with_traceback


import logging
import binascii
import socket

from contextlib import contextmanager
from multiprocessing import Lock

from percival.carrier.encoding import DATA_ENCODING, NUM_BYTES_PER_MSG, END_OF_MESSAGE
from percival.carrier.encoding import decode_message
from percival.carrier.errors import PercivalCommsError, PercivalProtocolError


def hexify(registers):
    """
    Utility function to generate a string representation of a register map with hexadecimal formatted values.

    :param registers: A list of ints or tuples that represents an register map
    :type registers:  list
    :return: string
    """
    registers_str = "|"
    if type(registers[0]) == int:
        for word in registers:
            registers_str += " %s |"%(hex(word))
    elif type(registers[0]) == tuple:
        for addr,word in registers:
            registers_str += " %s: %s |"%(hex(addr), hex(word))
    else:
        registers_str = str(registers)
    return registers_str


class TxMessage(object):
    """Encapsulate a single Percival carrier board message and the number of messages to expect in response"""
    def __init__(self, message, num_response_msg=1, expect_eom=False):
        """ TxMessage constructor
        
            :param message: A Percival Carrier Board message contains address (2 bytes) and data (4 bytes)
            :type message: bytearray
            :param num_response_msg: Number of messages to expect in response
            :param num_response_msg: int
            :param expect_eom: set true if end-of-message is expected to be the response
            :type expect_eom: boolean
        """
        self.num_response_msg = num_response_msg
        self._message = message
        self._expect_eom = False
        if expect_eom:
            self._expect_eom = END_OF_MESSAGE
        
    @property
    def message(self):
        return self._message
    
    @property
    def expected_bytes(self):
        return self.num_response_msg * NUM_BYTES_PER_MSG
    
    @property
    def expected_response(self):
        if self._expect_eom:
            return END_OF_MESSAGE

    def validate_eom(self, response):
        if self._expect_eom:
            return response == self._expect_eom

        # If no EOM is expected then just return OK
        else:
            return True

    def __repr__(self):
        s = "<TxMessage msg=0x%s %d msgs %s>"%(binascii.hexlify(self._message).upper(),
                                                               self.num_response_msg, bool(self._expect_eom))
        return s
        
    def __str__(self, *args, **kwargs):
        s = "<TxMessage msg=0x%s exp. resp.: %d msgs, EOM: %s>"%(binascii.hexlify(self._message).upper(),
                                                               self.num_response_msg, bool(self._expect_eom))
        return s

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class TxRx(object):
    """
    Transmit and receive data and commands to/from the Carrier Board through the XPort Ethernet
    """

    def __init__(self, fpga_addr, port = 10001, timeout = 2.0):
        """TxRx Constructor

            :param fpga_addr: IP address or network name of the Carrier Board XPort device
            :type  fpga_addr: `str`
            :param port:      IP port number
            :type  port:      `int`
            :param timeout:   Socket communication timeout (seconds)
            :type  timeout:   `float`
        """
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        
        self._fpga_addr = (fpga_addr, port)
        self._connected = False
        self._mutex = Lock()
        self.sock = None
        self.connect(timeout)

    def connect(self, timeout=2.0):
        if not self._connected:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(timeout)
                self.log.info("connecting to FPGA at %s", str(self._fpga_addr))
                self.sock.connect(self._fpga_addr)
                self._connected = True
            except Exception as ex:
                # Any kind of exception will result in non-connection and so set status accordingly
                self.log.error("Unable to connect to FPGA: %s", ex)
                self._connected = False

    def get_status(self):
        status = {
            "address": self._fpga_addr[0],
            "port": self._fpga_addr[1],
            "connected": self._connected
        }
        return status

    @property
    def fpga_addr(self):
        return self._fpga_addr
    
    @property
    def timeout(self):
        return self.sock.gettimeout()

    @property
    def connected(self):
        return self._connected

    @timeout.setter
    def timeout(self, value):
        self.sock.settimeout(value)
    
    def tx_msg(self, msg):
        """Transmit a single message of :const:`percival.carrier.encoding.NUM_BYTES_PER_MSG` bytes to the Carrier Board
        
        :param msg: Message to transmit
        :type  msg: bytearray
        :raises `PercivalCommsError`: if the socket connection appears to be broken
        """
        if self._connected:
            try:
              #  txt = binascii.hexlify(msg);
                self.log.debug("sending %s", binascii.hexlify(msg));
                self.sock.sendall(msg)
            except socket.error as e:
                self._connected = False
                self.clean()
                raise_with_traceback(PercivalCommsError("Unable to send message (%s)" % e))
        else:
            self._connected = False
            raise raise_with_traceback(PercivalCommsError("Socket not connected"))

    def rx_msg(self, expected_bytes = None):
        """Receive messages of `expected_bytes` length
        
        :param expected_bytes: Number of bytes to be received. If `expected_bytes`
                               is None, read one single message of size NUM_BYTES_PER_MSG
        :raises `PercivalCommsError`: if the socket connection appears to be broken
        :returns: The received message
        :rtype:   bytearray
        """
        msg = bytes()
        if self._connected:
            block_read_bytes = expected_bytes
            expected_resp_len = expected_bytes

            if expected_bytes is None:
                expected_resp_len = NUM_BYTES_PER_MSG
                block_read_bytes = 4096

            while len(msg) < expected_resp_len:
                if expected_bytes:
                    block_read_bytes = expected_bytes-len(msg)
                try:
                    chunk = self.sock.recv(block_read_bytes)
                except socket.error as e:
                    self._connected = False
                    self.clean()
                    raise raise_with_traceback(PercivalCommsError("socket connection broken (%s)" % e))
                if isinstance(chunk, str):
                    chunk = bytes(chunk, encoding=DATA_ENCODING)
                if len(chunk) == 0:
                    self._connected = False
                    self.clean()
                    raise raise_with_traceback(
                        PercivalCommsError("socket connection broken (expected a multiple of 6 bytes)"))
                msg = msg + chunk;
                self.log.debug("receiving %s", binascii.hexlify(chunk));
        else:
            self._connected = False
            raise raise_with_traceback(PercivalCommsError("Socket not connected"))
        self.log.debug(" ie response: %s", hexify(msg))
        return msg

    def send_recv(self, msg, expected_bytes = None):
        """Send `msg` and wait for receipt of `expected_bytes` in response or timeout
        
        :param msg: UART message to send
        :type  msg: bytearray
        :param expected_bytes: Number of bytes expected to be received. If `expected_bytes`
                               is None, read one message
        :raises `PercivalCommsError`: if the socket connection appears to be broken
        :returns:   Response from UART
        :rtype:     bytearray
        """
        resp = None
        with self._mutex:
            if self._connected:
                try:
                    self.tx_msg(msg)
                except PercivalCommsError as e:
                    self._connected = False
                    self.clean()
                    self.log.exception("Failed to send message %s. ERROR: %s" % (msg, e))
                    raise
                try:
                    resp = self.rx_msg(expected_bytes)
                except PercivalCommsError as e:
                    self._connected = False
                    self.clean()
                    self.log.exception("Failed to receive response to message %s. ERROR: %s" % (msg, e))
                    raise
            else:
                self._connected = False
                raise raise_with_traceback(PercivalCommsError("Socket not connected"))
        return resp
    
    def send_recv_message(self, message):
        """Send a message and wait for response
        
        :param message: a single message to send
        :type message: :obj:`TxMessage`
        :raises `PercivalCommsError`: if the socket connection appears to be broken
        :raises `TypeError`: if the message is not a :obj:`TxMessage` instance
        :raises `PercivalProtocolError`: if the response to the command does not validate (checking for EOM)
        :retuns: Response from UART as a list of tuples: [(address, data)...]
        :rtype:  list
        """
        if not isinstance(message, TxMessage):
            raise TypeError("message must be of type TxMessage, not %s"%str(type(message)))

        result = None
        if self._connected:
            with self._mutex:
                try:
                    self.tx_msg(message.message)
                except PercivalCommsError as e:
                    self._connected = False
                    self.clean()
                    self.log.exception("Failed to send message %s. ERROR: %s" % (message, e))
                    raise
                try:
                    resp = self.rx_msg(message.expected_bytes)
                except PercivalCommsError as e:
                    self._connected = False
                    self.clean()
                    self.log.exception("Failed to receive response to message %s. ERROR: %s" % (message, e))
                    raise
            result = decode_message(resp)

            # Check for expected response
            if not message.validate_eom(resp):
                raise PercivalProtocolError("Expected EOM on TxMessage: %s - got %s"%(str(message), str(result)))
        else:
            self._connected = False
            raise raise_with_traceback(PercivalCommsError("Socket not connected"))
        return result

    def clean(self):
        """Shutdown and close the socket safely
            
        Sockets are normally closed down cleanly on exit from the interpreter, however this method
        may be used in case the socket need to be closed down temporarily.
        """
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except socket.error:
            self.log.warning("unable to shutdown socket")
        try:
            self.sock.close()
        except socket.error:
            self.log.warning("unable to close socket")


@contextmanager
def TxRxContext(*args, **kwargs):
    """Provide a context which keeps a :class:`TxRx` module alive with an open socket only for the duration of the context
    
    Minimal example:

    >>> msg = encode_message(0x0144, 0x00000000) # Header Info Readback
    >>>
    >>> # Start the context - create the TxRx object and open the socket
    >>> with TxRxContext("192.168.1.3") as trx:
    >>>     response = trx.send_recv(msg)
    >>> # End of context - socket is closed down cleanly
    >>>
    >>> response = decode_message(response)
    >>> print response
    """
    trx = TxRx(*args, **kwargs)
    yield trx
    trx.clean()

