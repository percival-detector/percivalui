

import unittest
import socket
from mock import MagicMock, call
from builtins import bytes

import percival.carrier.const as const
from percival.carrier.devices import DeviceFamilyFeatures, MAX31730, LTC2309
from percival.carrier.txrx import hexify, TxRx, TxMessage, TxRxContext
from percival.carrier.encoding import END_OF_MESSAGE, DATA_ENCODING
from percival.carrier.errors import PercivalProtocolError, PercivalCommsError


class TestTxRxClasses(unittest.TestCase):
    def setUp(self):
        self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        #self.txrx = TxRx("127.0.0.1")

    def TestHexify(self):
        # Verify the hexify function stringifies values as expected
        self.assertEqual(hexify([(0x00, 0x01), (0x02, 0x03)]), "| 0x0: 0x1 | 0x2: 0x3 |")
        self.assertEqual(hexify([0x03, 0x02, 0x01, 0x00]), "| 0x3 | 0x2 | 0x1 | 0x0 |")
        self.assertEqual(hexify([0.0, 0.1, 0.2, 0.3]), "[0.0, 0.1, 0.2, 0.3]")

    def TestTxMessage(self):
        # Verification of TxMessage class
        msg = TxMessage(bytes("\x01\x4D\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=19, expect_eom=True)
        # Verify message, expected_bytes, expected_response and validate_eom are all as expected
        self.assertEqual(msg.message, bytes("\x01\x4D\x00\x00\x00\x00", encoding="latin-1"))
        self.assertEqual(msg.expected_bytes, 19*6)
        self.assertEqual(msg.expected_response, bytes('\xFF\xFF\xAB\xBA\xBA\xC1', encoding="latin-1"))
        self.assertEqual(msg.validate_eom(bytes('\x00\x00\x00\x00\x00\x00', encoding="latin-1")), False)
        msg = TxMessage(bytes("\x01\x4D\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=19, expect_eom=False)
        self.assertEqual(msg.validate_eom(None), True)
        msg2 = TxMessage(bytes("\x00\x00\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=19, expect_eom=False)
        self.assertNotEqual(msg, msg2)

    def TestTxRx(self):
        # Open a dummy socket for our txrx object to connect to
        self.s.bind(("127.0.0.1", 0))
        self.s.listen(3)
        port = self.s.getsockname()[1]
        txrx = TxRx("127.0.0.1", port)
        self.cnxn, self.addr = self.s.accept()
        self.assertEqual(txrx.fpga_addr, ("127.0.0.1", port))
        self.assertAlmostEqual(txrx.timeout, 2.0)
        txrx.timeout = 3.0
        self.assertAlmostEqual(txrx.timeout, 3.0)
        # Send some bytes out through txrx
        txrx.tx_msg(bytes('\x00\x01\x02\x03\x04\x05', encoding="latin-1"))
        # Receive the bytes from our test socket
        msg = self.cnxn.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, bytes('\x00\x01\x02\x03\x04\x05', encoding="latin-1"))
        # Send some bytes back through the socket
        self.cnxn.send(bytes('\x06\x07\x08\x09\x0A\x0B', encoding="latin-1"))
        # Receive the bytes through the txrx object
        reply = txrx.rx_msg(expected_bytes=6)
        # Verify the bytes have arrived
        self.assertEqual(reply, bytes('\x06\x07\x08\x09\x0A\x0B', encoding="latin-1"))
        # Send some more bytes back through the socket
        self.cnxn.send(bytes('\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B', encoding="latin-1"))
        # Receive the bytes through the txrx object
        reply = txrx.rx_msg()
        # Verify the bytes have arrived
        self.assertEqual(reply, bytes('\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B', encoding="latin-1"))
        # Close the connection
        self.cnxn.close()
        # Try to read bytes through the closed connection
        with self.assertRaises(PercivalCommsError):
            reply = txrx.rx_msg()

        txrx = TxRx("127.0.0.1", port)
        self.cnxn, self.addr = self.s.accept()
        # Send a message through the socket and expect receive the response
        self.cnxn.send(bytes('\xAA\xAB\xAC\xAD\xAE\xAF', encoding="latin-1"))
        reply = txrx.send_recv(bytes('\xBA\xBB\xBC\xBD\xBE\xBF', encoding="latin-1"))
        # Receive the bytes from our test socket
        msg = self.cnxn.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, bytes('\xBA\xBB\xBC\xBD\xBE\xBF', encoding="latin-1"))
        # Verify the reply bytes have arrived
        self.assertEqual(reply, bytes('\xAA\xAB\xAC\xAD\xAE\xAF', encoding="latin-1"))
        # Verify an incorrect message type raises an exception
        with self.assertRaises(TypeError):
            txrx.send_recv_message(0)

        txmsg = TxMessage(bytes("\x01\x01\x01\x01\x01\x01", encoding="latin-1"), num_response_msg=1, expect_eom=True)
        # Send a message through the socket and expect receive the response
        self.cnxn.send(bytes('\xFF\xFF\xAB\xBA\xBA\xC1', encoding="latin-1"))
        rxmsg = txrx.send_recv_message(txmsg)
        # Check the recevied message is EOM
        self.assertEqual(rxmsg, [(0xFFFF, 0xABBABAC1)])
        # Receive the bytes from our test socket
        msg = self.cnxn.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, bytes('\x01\x01\x01\x01\x01\x01', encoding="latin-1"))
        # Close down the txrx object
        txrx.clean()
        # Verify the context doesn't throw any errors
        with TxRxContext("127.0.0.1", port) as trx:
            # Accept a new connection
            self.cnxn, self.addr = self.s.accept()
            # Send a message through the socket and expect receive the response
            self.cnxn.send(bytes('\xFF\xFF\xAB\xBA\xBA\xC1', encoding="latin-1"))
            txmsg = TxMessage(bytes("\x01\x01\x01\x01\x01\x01", encoding="latin-1"), expect_eom=True)
            rxmsg = trx.send_recv_message(txmsg)
            # Check the recevied message is EOM
            self.assertEqual(rxmsg, [(0xFFFF, 0xABBABAC1)])

        # Close down the socket
        self.s.close()


class TestTxRx(unittest.TestCase):
    def setUp(self):
        self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        # Open a dummy socket for our txrx object to connect to
        self.s.bind(("127.0.0.1", 0))
        self.s.listen(3)
        port = self.s.getsockname()[1]
        self.txrx = TxRx("127.0.0.1", port)
        self.connection, self.addr = self.s.accept()

    def tearDown(self):
        self.txrx.clean()
        self.connection.close()
        self.s.close()

    def TestTransmitReceiveBytearray(self):
        byte_array_msg_tx = bytes('\x00\x01\x02\x03\x04\x05', encoding=DATA_ENCODING)
        self.txrx.tx_msg(byte_array_msg_tx)
        # Receive the bytes from our test socket
        msg = self.connection.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, byte_array_msg_tx)
        # Send some bytes back through the socket
        byte_array_msg_rx = bytes('\x06\x07\x08\x09\x0A\x0B', encoding=DATA_ENCODING)
        self.connection.send(byte_array_msg_rx)
        # Receive the bytes through the txrx object
        reply = self.txrx.rx_msg(expected_bytes=6)
        # Verify the bytes have arrived
        self.assertEqual(reply, byte_array_msg_rx)

    def TestClosedConnection(self):
        self.connection.close()
        byte_array_msg_tx = bytes('\x0C\x0D\x0E\x0F\x10\x11', encoding=DATA_ENCODING)

        self.txrx.tx_msg(byte_array_msg_tx)
        with self.assertRaises(PercivalCommsError):
            reply = self.txrx.rx_msg()

    def TestClosedSocketAndConnection(self):
        """Check that a RuntimeError is raised on txrx.rx_msg() when attempting to read a closed socket through a closed
        connection which has been closed from the server end"""
        self.connection.close()
        self.s.close()
        byte_array_msg_tx = bytes('\x0C\x0D\x0E\x0F\x10\x11', encoding=DATA_ENCODING)

        self.txrx.tx_msg(byte_array_msg_tx)
        with self.assertRaises(PercivalCommsError):
            reply = self.txrx.rx_msg()

    def TestClosedSocketTimeout(self):
        """Check that a RuntimeError is raised on txrx.rx_msg() when attempting to read a socket which has been closed
        from the server end"""
        self.txrx.timeout = 0.1  # Set a really short timeout so we don't hold up testing
        self.s.close()
        byte_array_msg_tx = bytes('\x0C\x0D\x0E\x0F\x10\x11', encoding=DATA_ENCODING)

        self.txrx.tx_msg(byte_array_msg_tx)
        with self.assertRaises(PercivalCommsError):
            reply = self.txrx.rx_msg()

    def TestCloseTxRxSocket(self):
        """Check that a socket.error is raised on TxRx.tx_msg() and TxRx.rx_msg() when attempting to send/receive data
        when the client side socket has been closed"""
        self.txrx.clean()
        byte_array_msg_tx = bytes('\x0C\x0D\x0E\x0F\x10\x11', encoding=DATA_ENCODING)

        with self.assertRaises(PercivalCommsError):
            self.txrx.tx_msg(byte_array_msg_tx)

        with self.assertRaises(PercivalCommsError):
            reply = self.txrx.rx_msg()

    def TestSendRecvMessage(self):
        """The vanilla use-case - send a message and expect an ABBABAC1 return EOM"""
        byte_array_message = bytes("\x01\x01\x01\x01\x01\x01", encoding=DATA_ENCODING)
        txmsg = TxMessage(byte_array_message, num_response_msg=1, expect_eom=True)
        # Send a response back from the server (in advance to avoid potential race condition or timeout
        byte_array_response = bytes('\xFF\xFF\xAB\xBA\xBA\xC1', encoding=DATA_ENCODING)
        self.connection.send(byte_array_response)
        rxmsg = self.txrx.send_recv_message(txmsg)
        # Check the received message is EOM
        self.assertEqual(rxmsg, [(0xFFFF, 0xABBABAC1)])
        # Receive the bytes from our test socket
        msg = self.connection.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, byte_array_message)

    def TestSendRecvMessageTimeoutRaisesCommsError(self):
        """Check that no response times out and raises a PercivalCommsError"""
        self.txrx.timeout = 0.2  # short timeout so we don't hold up testing too much

        byte_array_message = bytes("\x01\x01\x01\x01\x01\x01", encoding=DATA_ENCODING)
        txmsg = TxMessage(byte_array_message, num_response_msg=1, expect_eom=True)
        with self.assertRaises(PercivalCommsError):
            self.txrx.send_recv_message(txmsg)

        # Receive the bytes from our test socket
        msg = self.connection.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, byte_array_message)

    def TestSendRecvMessageSocketRaisesCommsError(self):
        """Check that a broken socket connection raises a PercivalCommsError"""
        # close the dummy socket
        self.s.close()
        self.txrx.timeout = 0.2  # short timeout so we don't hold up testing too much
        byte_array_message = bytes("\x09\x08\x07\x06\x05\x04", encoding=DATA_ENCODING)
        txmsg = TxMessage(byte_array_message, num_response_msg=1, expect_eom=True)
        with self.assertRaises(PercivalCommsError):
            self.txrx.send_recv_message(txmsg)

    def TestSendRecvMessageInvalidResponseRaisesCommsError(self):
        """Check that invalid response raises a PercivalProtocolError"""
        byte_array_message = bytes("\x01\x01\x01\x01\x01\x01", encoding=DATA_ENCODING)

        # Put an invalid response back from the server (in advance to avoid potential race condition or timeout)
        byte_array_response = bytes('\xBA\xBA\xB0\x00\xB1\x11', encoding=DATA_ENCODING)
        self.connection.send(byte_array_response)

        txmsg = TxMessage(byte_array_message, num_response_msg=1, expect_eom=True)
        with self.assertRaises(PercivalProtocolError):
            self.txrx.send_recv_message(txmsg)

        # Receive the bytes from our test socket
        msg = self.connection.recv(6)
        # Verify the bytes are the same as those sent
        self.assertEqual(msg, byte_array_message)
