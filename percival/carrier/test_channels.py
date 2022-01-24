'''
Created on 8 May 2015

@author: up45
'''


import unittest, sys, logging
from mock import MagicMock, call
from builtins import bytes

import percival.carrier.const as const
from percival.carrier.channels import ControlChannel, MonitoringChannel
from percival.carrier.txrx import TxMessage
from percival.carrier.errors import PercivalControlDeviceError


class TestChannels(unittest.TestCase):

    def setUp(self):
        # Perform any setup here
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.txrx = MagicMock()
        self.channel_ini = MagicMock()
        # these are tuples of address->32 bit value; set max to 0x20
        self.settings = [(0, 0x00), (0, 0x00200000), (0, 0x00), (0, 0x00)]
        self.echo_word_address = 0x036F

    def TestControlChannel(self):
        self.txrx.send_recv_message = MagicMock(return_value=[(self.echo_word_address, 0x00000019)])
        self.channel_ini.Component_family_ID = const.DeviceFamily.AD5669
        self.channel_ini._channel_number = 1
        self.channel_ini.UART_address = 10
        self.channel_ini.Board_type = const.BoardTypes.bottom
        ctrlChannel = ControlChannel(self.txrx, self.channel_ini, self.settings)
        # Send a command to initialise the channel
        ctrlChannel.cmd_initialize()

        # Verify the txrx mock had send_recv_message called
        # this is device-initialize, control dev-1
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x02\xCA\x20\x00\x00\x01", encoding="latin-1"), expect_eom=True))

        # Send a no-op command
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.cmd_no_operation()
        # Verify the txrx mock had send_recv_message called
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x02\xCA\x00\x00\x00\x01", encoding="latin-1"), expect_eom=True))

        # Send a set and get value
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.cmd_set_and_get_value()
        # Verify the txrx mock had send_rcv_message called
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x02\xCA\x50\x00\x00\x01", encoding="latin-1"), expect_eom=True))

        # Send a read echo word command
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.read_echo_word()
        # Verify the txrx mock had send_recv_message called
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x03\x87\x00\x00\x00\x00", encoding="latin-1"), expect_eom=False))

        # Set the value to 10
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.cmd_control_set_value(10)
        # Verify the txrx mock had send_rcv_message called last
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x00\x0D\x00\x00\x00\x0A", encoding="latin-1"), expect_eom=True))

        # Set the value to 20
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.cmd_control_set_value(20)
        # Verify the txrx mock had send_recv_message called last
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x00\x0D\x00\x00\x00\x14", encoding="latin-1"), expect_eom=True))

        # Set the value to 25 from the control point
        self.txrx.send_recv_message.reset_mock()
        ctrlChannel.set_value(25)
        # Verify the txrx mock had send_rcv_message called
        calls = self.txrx.send_recv_message.mock_calls
        self.assertEqual(calls[0], call(
            # Command: no-op on device index 1
            TxMessage(bytes("\x02\xCA\x00\x00\x00\x01", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[1], call(
            # Set Control value on UART addr 0x000D to 25 (=0x19)
            TxMessage(bytes("\x00\x0D\x00\x00\x00\x19", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[2], call(
            # Command: no-op on device index 1
            TxMessage(bytes("\x02\xCA\x00\x00\x00\x01", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[3], call(
            # Command: set_and_get_value on device index 1
            TxMessage(bytes("\x02\xCA\x50\x00\x00\x01", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[4], call(
            # Readback READ ECHO WORD
            TxMessage(bytes("\x03\x87\x00\x00\x00\x00", encoding="latin-1"), expect_eom=False)))

        # Set the value to 26 from the control point
        self.txrx.send_recv_message.reset_mock()
        # Verify this times out and raises a runtime error
        with self.assertRaises(PercivalControlDeviceError):
            ctrlChannel.set_value(26, 0.01)

        # Set the value to 25 from the control point
        self.txrx.send_recv_message.reset_mock()
        # Set the mock to return an i2c error
        self.txrx.send_recv_message.return_value = [(self.echo_word_address, 0x00010019)]
        # Verify this raises an IO error
        with self.assertRaises(IOError):
            ctrlChannel.set_value(25)

    def TestAD5242ControlChannel(self):
        self.channel_ini.reset_mock()
        self.txrx.send_recv_message = MagicMock(return_value=[(self.echo_word_address, 0x00000019)])
        self.channel_ini.Component_family_ID = const.DeviceFamily.AD5242
        self.channel_ini._channel_number = 0x34
        # note 0x06 is the base address, and there are 4 words in the section
        self.channel_ini.UART_address = 0xD6
        self.channel_ini.Board_type = const.BoardTypes.bottom
        ctrlChannel = ControlChannel(self.txrx, self.channel_ini, self.settings)
        ctrlChannel.cmd_control_set_value(0x0A)
        # Verify the txrx mock had send_rcv_message called
        self.txrx.send_recv_message.assert_called_once_with(
            TxMessage(bytes("\x00\xD9\x00\x01\x00\x0A", encoding="latin-1"), expect_eom=True))

    def TestMonitoringChannel(self):
        self.txrx.send_recv_message = MagicMock(return_value=[(self.echo_word_address, 0x01000023)])
        self.channel_ini.Component_family_ID = const.DeviceFamily.MAX31730
        self.channel_ini._channel_number = 0x12;
        self.channel_ini.UART_address = 139
        self.channel_ini.Board_type = const.BoardTypes.carrier
        mntrChannel = MonitoringChannel(self.txrx, self.channel_ini, self.settings)

        # Call get value on the monitor
        self.txrx.send_recv_message.reset_mock()
        with self.assertRaises(RuntimeError):
            mntrChannel.get_value()
        # Verify the txrx mock had send_recv_message called
        calls = self.txrx.send_recv_message.mock_calls
        self.assertEqual(calls[0], call(
            # it doesnt just read, it waits for the id to up and takes the new value.
            TxMessage(bytes("\x03\x87\x00\x00\x00\x00", encoding="latin-1"), expect_eom=False)))
            # noop, mon device, num 0x12 
        self.assertEqual(calls[1], call(
            TxMessage(bytes("\x02\xCA\x00\x80\x00\x12", encoding="latin-1"), expect_eom=True)))
            # setandget
        self.assertEqual(calls[2], call(
            TxMessage(bytes("\x02\xCA\x50\x80\x00\x12", encoding="latin-1"), expect_eom=True)))
        self.assertEqual(calls[3], call(
            TxMessage(bytes("\x03\x87\x00\x00\x00\x00", encoding="latin-1"), expect_eom=False)))

        # Setup the mock with different sample numbers
        self.txrx.send_recv_message = MagicMock() #return_value=[(0x03EE, 0x01000023), (0x03EE, 0x02000023)])
        self.txrx.send_recv_message.side_effect = [[(self.echo_word_address, 0x01000012)], # from first echo
                                                   [(self.echo_word_address, 0xABBABAC1)], # from nop
                                                   [(self.echo_word_address, 0xABBABAC1)], # from getsend
                                                   [(self.echo_word_address, 0x02000013)]] # from second echo
        mntrChannel = MonitoringChannel(self.txrx, self.channel_ini, self.settings)
        self.txrx.send_recv_message.reset_mock()
        value = mntrChannel.get_value()
        self.assertEqual(value.read_value, 0x13);

        # Setup the mock to return i2c error
        self.txrx.send_recv_message = MagicMock() #return_value=[(0x03EE, 0x01000023), (0x03EE, 0x02000023)])
        self.txrx.send_recv_message.side_effect = [[(self.echo_word_address, 0x01010012)],
                                                   [(self.echo_word_address, 0xABBABAC1)],
                                                   [(self.echo_word_address, 0xABBABAC1)],
                                                   [(self.echo_word_address, 0x02010013)]]
        # Verify this raises an IO error
        with self.assertRaises(IOError):
            value = mntrChannel.get_value()

