'''
Created on 15 July 2016

:author: Alan Greer

A class representation for a Percival buffer command.

An instance is initialised with a percival.carrier.txrx.TxRx object and
also the target destination for commands (const.BufferTarget).  Commands
can then be constructed and sent depending on the target.  Commands can
be sent using the send_command method.

TODO: This assumes the buffer has already been filled with values.  This
class could instead of taking the number of words, take the actual words and
fill the buffer itself.
'''


import logging

from percival.carrier import const
from percival.carrier.encoding import encode_message, encode_multi_message, decode_message
from percival.carrier.registers import UARTRegister
from percival.carrier.txrx import TxMessage


class BufferCommand(object):
    """
    Represent a Percival buffer command.
    """
    def __init__(self, txrx, target):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param target: target board for the buffer command
        :type  target: BufferTarget
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._txrx = txrx
        self._target = target
        self._reg_command = UARTRegister(const.COMMAND)
        self._reg_command.initialize_map([0,0,0])

    def _get_command_msg(self, cmd, words=None, address=None):
        """
        Private method to construct a buffer command message object (TxMessage).

        The returned object contains the correct address and word for executing the
        specified command and can be sent through the txrx object to the Percival
        hardware.

        Depending on the target the command value can take on different meanings, and
        also the number of return messages can vary.  These values are looked up from
        the percival.carrier.const.BufferCommands dictionary.

        :param cmd: command to encode
        :type  cmd: BufferCmd
        :param words: the number of words in the buffer to execute the command on
        :param address: the starting address of the target to execute the command on
        :returns: percival.carrier.txrx.TxMessage
        """
        self._log.debug("Cmd: %s  const.BufferCmd.no_operation: %s", cmd, const.BufferCmd.no_operation)
        if cmd is const.BufferCmd.no_operation:
            self._log.debug("No_op comparison True")
            self._reg_command.fields.buffer_cmd = 0
            self._reg_command.fields.buffer_cmd_destination = 0
            self._reg_command.fields.buffer_cmd_words = 0
            self._reg_command.fields.buffer_cmd_address = 0
        else:
            self._reg_command.fields.buffer_cmd_destination = self._target.value
            self._reg_command.fields.buffer_cmd = const.BufferCommands[self._target][cmd]["command"]
            if words:
                self._reg_command.fields.buffer_cmd_words = words
            else:
                self._reg_command.fields.buffer_cmd_words = 0
            if address:
                self._reg_command.fields.buffer_cmd_address = address
            else:
                self._reg_command.fields.buffer_cmd_address = 0

        cmd_msg = self._reg_command.get_write_cmd_msg(eom=False)[1]
        if cmd is const.BufferCmd.no_operation:
            cmd_msg.num_response_msg = 1
        else:
            cmd_msg.num_response_msg = const.BufferCommands[self._target][cmd]["response"]
        return cmd_msg

    def _command(self, cmd, words=None, address=None):
        """
        Private method to construct and send a buffer command.

        This method gets the TxMessage object representation of the buffer command
        and sends it through the txrx object to the Percival hardware, returning any
        response.

        :param cmd: command to encode
        :type  cmd: BufferCmd
        :param words: the number of words in the buffer to execute the command on
        :param address: the starting address of the target to execute the command on
        :returns: list of (address, dataword) tuples
        """
        self._log.debug("Cmd: %s  Words: %s  Address: %s", cmd, words, address)
        cmd_msg = self._get_command_msg(cmd, words, address)
        self._log.debug("Command Message: %s", cmd_msg)
        response = self._txrx.send_recv_message(cmd_msg)
        self._log.debug("Response Message: %s", response)
        return response

    def write_words_to_buffer(self, words):
        # Encode the words into the correct message format and send the values
        msg = encode_multi_message(const.WRITE_BUFFER.start_address, words)
        self._log.debug("Writing buffer words to address: %X ...", const.WRITE_BUFFER.start_address)
        try:
            for item in msg:
                self._txrx.send_recv_message(TxMessage(item))
        except RuntimeError:
            self._log.exception("No response (addr: %X)", const.WRITE_BUFFER.start_address)
            raise

    def read_words_from_write_buffer(self):
        msg = encode_message(const.READBACK_WRITE_BUFFER.start_address, 0x00000000)
        resp = self._txrx.send_recv(msg, 6*64)
        data = decode_message(resp)
        return data

    def read_words_from_read_buffer(self):
        msg = encode_message(const.READBACK_READ_BUFFER.start_address, 0x00000000)
        resp = self._txrx.send_recv(msg, 6*64)
        data = decode_message(resp)
        return data

    def cmd_no_operation(self):
        """
        Method to send a no_operation buffer command.

        :returns: list of (address, dataword) tuples
        """
        result = self._command(const.BufferCmd.no_operation)
        return result

    def send_command(self, cmd, words, address):
        """
        Method to send a buffer command.

        This method first sends a no_operation command, followed by the specified
        buffer command.

        :param cmd: command to encode
        :type  cmd: BufferCmd
        :param words: the number of words in the buffer to execute the command on
        :param address: the starting address of the target to execute the command on
        """
        self._log.debug("Sending a no operation command")
        self.cmd_no_operation()
        self._log.debug("Now sending the command: %s", cmd)
        result = self._command(cmd, words=words, address=address)
        return result


class SensorBufferCommand(BufferCommand):
    def __init__(self, txrx):
        super(SensorBufferCommand, self).__init__(txrx, const.BufferTarget.percival_sensor)
        #self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))

    def cmd_no_operation(self):
        """
        Method to send a no_operation buffer command.

        :returns: list of (address, dataword) tuples
        """
        result = self._command(const.BufferCmd.no_operation)
        return result

    def write_words_to_buffer(self, words):
        # Encode the words into the correct message format and send the values
        msg = encode_multi_message(const.WRITE_BUFFER.start_address, words)
        self._log.debug("Writing buffer words to address: %X ...", const.WRITE_BUFFER.start_address)
        try:
            for item in msg:
                self._txrx.send_recv_message(TxMessage(item))
        except RuntimeError:
            self._log.exception("No response (addr: %X)", const.WRITE_BUFFER.start_address)
            raise

    def verify_response(self, response):
        # We should receive the generic acknowledge plus the sensor specific acknowledge
        verified = False
        if len(response) == 2:
            if response[0] == (0xFFFF, 0xABBABAC1) and response[1] == (0xFFF3, 0xABBA3333):
                self._log.debug("Verified sensor buffer response from hardware")
                verified = True
        if not verified:
            self._log.debug("Unable to verify sensor buffer response: %s", response)
        return verified

    def send_dacs_setup_cmd(self, words):
        # First encode the words into the correct message format and send the values
        # to fill up the buffer
        self._log.debug("Writing DAC values to buffer")
        self.write_words_to_buffer(words)

        # Now send the command to write the buffer as sensor DAC values
        # cmd = send_DACs_setup_to_target
        # words = 0
        # address = 1
        self._log.debug("Now sending the sensor buffer command to setup DACS")
        result = self.send_command(const.SensorBufferCmd.send_DACs_setup, 0, 1)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Sensor DAC command failed")

    def send_configuration_setup_cmd(self, words):
        self._log.debug("Executing sensor configuration command with words: %s", words)
        if len(words) != 144:
            self._log.error("Supplied word list for sensor config is not length 144")
            raise RuntimeError("Supplied word list for sensor config is not length 144")

        # Write the first 64 words into the buffer
        self._log.debug("Writing the first 64 config words to the buffer")
        self.write_words_to_buffer(words[0:64])

        # Now send the config command with base address set for iteration 1
        self._log.debug("Sending the config command iteration 1")
        result = self.send_command(const.SensorBufferCmd.send_CONFIGURATION_setup, 0, 1)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Config command iteration 1 failed")

        # Write the second set of 64 words into the buffer
        self._log.debug("Writing the second set of 64 config words to the buffer")
        self.write_words_to_buffer(words[64:128])

        # Now send the config command with base address set for iteration 2
        self._log.debug("Sending the config command iteration 2")
        result = self.send_command(const.SensorBufferCmd.send_CONFIGURATION_setup, 0, 2)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Config command iteration 2 failed")

        # Write the third set of words (16 words) into the buffer
        self._log.debug("Writing the third set of config words (16 words) to the buffer")
        self.write_words_to_buffer(words[128:144])

        # Now send the config command with base address set for iteration 2
        self._log.debug("Sending the config command iteration 3")
        result = self.send_command(const.SensorBufferCmd.send_CONFIGURATION_setup, 0, 3)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Config command iteration 3 failed")

    def send_calibration_setup_cmd(self, words):
        self._log.debug("Executing sensor calibration command with words: %s", words)
        if len(words) != 3240:
            self._log.error("Supplied word list for sensor calibration is not length 3240")
            self._log.error("Provided word length is: %d", len(words))
            raise RuntimeError("Supplied word list for sensor config is not length 3240")

        # Now perform 90 iterations, each time writing 36 words to the buffer and then sending the
        # configuration command words
        for index in range(0, 90):
            # Write the first 64 words into the buffer
            first_word = index * 36
            last_word = first_word + 36
            self._log.debug("Writing calibration words [%d:%d] to the buffer", first_word, last_word)
            self.write_words_to_buffer(words[first_word:last_word])

            # Now send the command
            iteration = index + 1
            self._log.debug("Sending the sensor calibration command iteration %d", iteration)
            result = self.send_command(const.SensorBufferCmd.send_CALIBRATION_setup, 0, iteration)
            # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
            if not self.verify_response(result):
                raise RuntimeError("Sensor calibration command iteration %d failed", iteration)

    def send_debug_setup_cmd(self, words):
        self._log.debug("Executing sensor debug command with words: %s", words)
        if len(words) != 9:
            self._log.error("Supplied word list for sensor debug is not length 9")
            raise RuntimeError("Supplied word list for sensor debug is not length 9")

        # Write the words into the buffer
        self._log.debug("Writing the debug words to the buffer")
        self.write_words_to_buffer(words)

        # Now send the debug command with base address set as 1
        self._log.debug("Sending the sensor debug command")
        result = self.send_command(const.SensorBufferCmd.send_DEBUG_setup, 0, 1)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Sensor debug command failed")

    def send_roi_setup_cmd(self):
        self._log.debug("Executing sensor ROI command")

        # Now send the ROI command with base address set as 1
        result = self.send_command(const.SensorBufferCmd.send_ROI_setup, 0, 1)
        # We expect to see FFFF, ABBABAC1 followed by FFF3 ABBA3333
        if not self.verify_response(result):
            raise RuntimeError("Sensor ROI command failed")

