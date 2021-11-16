'''
Created on 17 July 2017

@author: gnx91527
'''



import unittest, sys, logging
from mock import MagicMock, call
from builtins import bytes

import percival.carrier.const as const
from percival.carrier.buffer import BufferCommand, SensorBufferCommand
from percival.carrier.txrx import TxMessage


class TestBuffer(unittest.TestCase):

    def setUp(self):
        # Perform any setup here
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.ERROR)
        self.txrx = MagicMock()
        self.buffer = SensorBufferCommand(self.txrx)

    def TestSimpleBufferCommand(self):

        self.buffer = BufferCommand(self.txrx, const.BufferTarget.mezzanine_board_A)
        cmd = self.buffer._get_command_msg(const.BufferCmd.no_operation)
        self.assertEqual(cmd, TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"), expect_eom=False))

        cmd = self.buffer._get_command_msg(const.BufferCmd.read)
        self.assertEqual(cmd, TxMessage(bytes("\x02\xCB\x11\x00\x00\x00", encoding="latin-1"),
                                        num_response_msg=2,
                                        expect_eom=False))

        cmd = self.buffer._get_command_msg(const.BufferCmd.write, 0x05, 0x3A)
        self.assertEqual(cmd, TxMessage(bytes("\x02\xCB\x10\x05\x00\x3A", encoding="latin-1"),
                                        num_response_msg=2,
                                        expect_eom=False))

        self.txrx.send_recv_message = MagicMock(return_value=[(0x00000001, 0x00000002)])
        response = self.buffer.cmd_no_operation()
        self.assertEqual(response, [(0x00000001, 0x00000002)])

        self.txrx.send_recv_message = MagicMock(return_value=[(0x00000003, 0x00000004)])
        response = self.buffer.send_command(const.BufferCmd.write, 0x1, 0x2)
        self.assertEqual(response, [(0x00000003, 0x00000004)])

    def TestSensorBufferCommandDac(self):
        #
        # Sensor DAC command
        #
        self.txrx.send_recv_message = MagicMock(return_value=[(0xFFFF, 0xABBABAC1), (0xFFF3, 0xABBA3333)])
        self.buffer.send_dacs_setup_cmd([0x00000001, 0x00000002, 0x00000003, 0x00000004])
        calls = self.txrx.send_recv_message.mock_calls
        # Assert that the data words were written into the buffer
        self.assertEqual(calls[0], call(TxMessage(bytes("\x02\x8A\x00\x00\x00\x01", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[1], call(TxMessage(bytes("\x02\x8B\x00\x00\x00\x02", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[2], call(TxMessage(bytes("\x02\x8C\x00\x00\x00\x03", encoding="latin-1"),
                                                  num_response_msg = 1,
                                                  expect_eom = False)))
        self.assertEqual(calls[3], call(TxMessage(bytes("\x02\x8D\x00\x00\x00\x04", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[4], call(TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[5], call(TxMessage(bytes("\x02\xCB\x50\x00\x00\x01", encoding="latin-1"),
                                                  num_response_msg=2,
                                                  expect_eom=False)))
        self.assertEqual(len(calls),6);

    def TestSensorBufferCommandConfig(self):
        #
        # Sensor Config command
        #
        # Generate the words required to submit a sensor config command
        words = list(range(0,144))
        std_reply = (0xFFFF, 0xABBABAC1)
        sensor_reply = (0xFFF3, 0xABBA3333)
        # Create the returned expected responses for the config command
        return_values = []
        for index in range(64):
            return_values.append(std_reply)
        # Iteration 1 null command standard response
        return_values.append(std_reply)
        # Iteration 1 sensor response
        return_values.append([std_reply, sensor_reply])
        for index in range(64):
            return_values.append(std_reply)
        # Iteration 2 null command standard response
        return_values.append(std_reply)
        # Iteration 1 sensor response
        return_values.append([std_reply, sensor_reply])
        for index in range(16):
            return_values.append(std_reply)
        # Iteration 3 null command standard response
        return_values.append(std_reply)
        # Iteration 1 sensor response
        return_values.append([std_reply, sensor_reply])
        self.log.debug("Return values : %s", return_values)
        self.txrx.send_recv_message = MagicMock()
        self.txrx.send_recv_message.side_effect = return_values
        self.buffer.send_configuration_setup_cmd(words)
        # Verify that the correct calls were made to the txrx object for filling in the buffers
        calls = self.txrx.send_recv_message.mock_calls
        
        extra = 0;
        # Assert that the data words were written into the write-buffer
        for i in range(0,144):
            msg = bytearray(6); # 6 zeros
            offset = 0x028a + (i%64); # the buffer is 64 words in size, so we do it in 3 batches: 64,64,16
            msg[0] = (offset & 0xff00) >> 8;
            msg[1] = offset & 0x00ff;
            msg[5] = i;
            
            extra = (i//64)*2; # there are 2 command messages after every batch

            self.assertEqual(calls[i+extra], call(TxMessage(msg,
                                                  num_response_msg=1,
                                                  expect_eom=False)))

        # Verify the buffer commands were sent after every batch, at messages 64,65 and so on.
        self.assertEqual(calls[64], call(TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[65], call(TxMessage(bytes("\x02\xCB\x51\x00\x00\x01", encoding="latin-1"),
                                                  num_response_msg=2,
                                                  expect_eom=False)))
        self.assertEqual(calls[130], call(TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[131], call(TxMessage(bytes("\x02\xCB\x51\x00\x00\x02", encoding="latin-1"),
                                                  num_response_msg=2,
                                                  expect_eom=False)))
        self.assertEqual(calls[148], call(TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[149], call(TxMessage(bytes("\x02\xCB\x51\x00\x00\x03", encoding="latin-1"),
                                                  num_response_msg=2,
                                                  expect_eom=False)))

        self.assertEqual(len(calls), 144 + 6);

    def TestSensorBufferCommandCalib(self):
        #
        # Sensor calibration command: see the doco; 90x tranfers of 36 words each.
        #
        # Generate the words required to submit a sensor config command
        words = list(range(0,3240))
        std_reply = (0xFFFF, 0xABBABAC1)
        sensor_reply = (0xFFF3, 0xABBA3333)
        # Create the returned expected responses for the config command
        return_values = []
        for index in range(0,90):
            for index2 in range(36):
                return_values.append(std_reply)
            # block-end null command standard response
            return_values.append(std_reply)
            # block-end sensor response
            return_values.append([std_reply, sensor_reply])
        self.log.debug("Return values : %s", return_values)
        self.txrx.send_recv_message = MagicMock()
        self.txrx.send_recv_message.side_effect = return_values
        self.buffer.send_calibration_setup_cmd(words)
        # Verify that the correct calls were made to the txrx object for filling in the buffers
        calls = self.txrx.send_recv_message.mock_calls

        self.assertEqual(len(calls), 90 * 38);
                                            
        # Assert that the data words were written into the write-buffer
        for i in range(0,36*90):
            msg = bytearray(6); # 6 zeros
            msg[0] = 0x02;
            msg[1] = 0x8a + (i%36);
            msg[4] = (i & 0xff00) >> 8;
            msg[5] = i & 0x00ff;
            
            extra = (i//36)*2; # there are 2 command messages after every batch

            self.assertEqual(calls[i+extra], call(TxMessage(msg,
                                                  num_response_msg=1,
                                                  expect_eom=False)))

        # verify buffer commands once the buffer is full
        index = 36;
        for j in range(0,90):
            msg = bytearray.fromhex("02 cb 00 00 00 00");

            self.assertEqual(calls[index], call(TxMessage(msg,
                                                   num_response_msg=1,
                                                   expect_eom=False)))

            msg = bytearray.fromhex("02 cb 52 00 00 01");
            msg[5] = j+1;
            self.assertEqual(calls[index+1], call(TxMessage(msg,
                                                   num_response_msg=2,
                                                   expect_eom=False)))
            index += 38;

        # Verify incorrect number of values will generate an exception
        with self.assertRaises(RuntimeError):
            test_values = [1, 1]
            self.buffer.send_calibration_setup_cmd(test_values)

    def TestSensorBufferCommandDebug(self):
        #
        # Sensor Debug command
        #
        self.txrx.send_recv_message = MagicMock()
        std_reply = (0xFFFF, 0xABBABAC1)
        sensor_reply = (0xFFF3, 0xABBA3333)
        # Create the returned expected responses for the config command
        return_values = []
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append(std_reply)
        return_values.append([std_reply, sensor_reply])
        self.txrx.send_recv_message.side_effect = return_values

        self.buffer = SensorBufferCommand(self.txrx)
        self.buffer.send_debug_setup_cmd([0x00000000,
                                          0x00000101,
                                          0x00000202,
                                          0x00000303,
                                          0x00000404,
                                          0x00000505,
                                          0x00000606,
                                          0x00000707,
                                          0x00000808]);
        calls = self.txrx.send_recv_message.mock_calls

        self.assertEqual(len(calls), 11);
        # Assert that the data words were written into the buffer
        for i in range(0,9):
            msg = bytearray.fromhex("02 8a 00 00 00 00");
            msg[1] += i;
            msg[4] = i;
            msg[5] = i;
            self.assertEqual(calls[i], call(TxMessage(msg,
                                                  num_response_msg=1,
                                                  expect_eom=False)));

        # Verify that the correct calls were made to the txrx object for sending the buffer commands
        # Assert that the commands were sent in the correct order
        self.assertEqual(calls[9], call(TxMessage(bytes("\x02\xCB\x00\x00\x00\x00", encoding="latin-1"),
                                                  num_response_msg=1,
                                                  expect_eom=False)))
        self.assertEqual(calls[10], call(TxMessage(bytes("\x02\xCB\x54\x00\x00\x01", encoding="latin-1"),
                                                   num_response_msg=2,
                                                   expect_eom=False)))

        # Verify incorrect number of values will generate an exception
        with self.assertRaises(RuntimeError):
            test_values = [1, 1]
            self.buffer.send_debug_setup_cmd(test_values)
