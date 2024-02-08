

import unittest, logging
from mock import MagicMock, call
from builtins import bytes

import percival_detector.carrier.const as const
from percival_detector.carrier.values import BoardValues
from percival_detector.carrier.txrx import TxMessage


class TestBoardValuesClass(unittest.TestCase):
    def setUp(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(logging.DEBUG)
        self.txrx = MagicMock()
        self.txrx.send_recv_message = MagicMock()

    def TestFunctions(self):
        # Test reading values from carrier board
        self.value = BoardValues(self.txrx, const.BoardTypes.carrier)
        self.value.read_values()
        print(self.txrx.send_recv_message.mock_calls);
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x03\x83\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=4, expect_eom=False))

        self.txrx.send_recv_message.reset_mock()
        # Test reading values from periphery left board
        self.value = BoardValues(self.txrx, const.BoardTypes.left)
        self.value.read_values()
        self.txrx.send_recv_message.assert_called_with(
            TxMessage(bytes("\x03\x81\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=1, expect_eom=False))

        self.txrx.send_recv_message.reset_mock()
        # Test reading values from periphery bottom board
        self.value = BoardValues(self.txrx, const.BoardTypes.bottom)
        self.value.read_values()
        self.txrx.send_recv_message.assert_called_with(
            TxMessage(bytes("\x03\x82\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=84, expect_eom=False))

        self.txrx.send_recv_message.reset_mock()
        # Test reading values from plugin board
        self.value = BoardValues(self.txrx, const.BoardTypes.plugin)
        self.value.read_values()
        self.txrx.send_recv_message.assert_called_with(
            TxMessage(bytes("\x03\x84\x00\x00\x00\x00", encoding="latin-1"), num_response_msg=1, expect_eom=False))

        # status board has not been implemented.
