

import unittest, logging
from mock import MagicMock, call
from builtins import bytes

import percival.carrier.const as const
from percival.carrier.system import SystemCommand
from percival.carrier.txrx import TxMessage


class TestSystemCommandClass(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.txrx = MagicMock()
        self.txrx.send_recv_message = MagicMock()
        self.system = SystemCommand(self.txrx)

    def TestFunctions(self):
        # Send a valid system command
        self.system.send_command(const.SystemCmd.disable_global_monitoring)
        # Verify the correct TxMessages are sent to the socket
        calls = self.txrx.send_recv_message.mock_calls
        self.assertEqual(calls[0], call(
            TxMessage(bytes("\x02\xCC\x00\x00\x00\x00", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[1], call(
            TxMessage(bytes("\x02\xCC\x00\x02\x00\x00", encoding="latin-1"), expect_eom=True)))

        # Send a command that is not a system command type
        # Check that a TypeError is raised
        with self.assertRaises(TypeError):
            self.system.send_command(5)

