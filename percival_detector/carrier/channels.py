"""
Created on 16 May 2016

:author: gnx91527

A class representation for a Percival channel.  The channel ini settings
are stored within this class.  There are two subclasses available, the
ControlChannel and the MonitoringChannel.  It is possible to set the value
of a ControlChannel and to get the value of a MonitoringChannel.
"""


import time
import logging

from percival_detector.carrier import const
from percival_detector.carrier.registers import UARTRegister, BoardRegisters, generate_register_maps
from percival_detector.carrier.devices import DeviceCmd, DeviceFamilyFeatures, DeviceFamily
from percival_detector.carrier.errors import PercivalControlDeviceError

class Channel(object):
    """
    Represent a specific device channel on any of the control boards.
    """

    def __init__(self, txrx, channel_ini):
        """ Channel constructor. Call this from derived classes

        Keeps a reference to the txrx communication object and initialises itself based on the parameters in channel_ini.

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param channel_ini: Channel configuration parameters from INI file
        :type  channel_ini: percival_detector.carrier.configuration.ControlChannelIniParameters
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._txrx = txrx
        self._channel_ini = channel_ini

        self.device_family = DeviceFamily(channel_ini.Component_family_ID)
        self._device_family_features = DeviceFamilyFeatures[self.device_family]

#        if self._device_family_features.function != DeviceFunction.control:
#            raise TypeError("Not a control device")
        self.channel_index = channel_ini._channel_number
        self._log.debug("Channel index number: %d", self.channel_index)
        self.uart_device_address = channel_ini.UART_address
        self._log.debug("Channel device address: %d", self.uart_device_address)

        self._reg_uart = UARTRegister(const.COMMAND)
        self._reg_uart.initialize_map([0,0,0])
        self._reg_uart.fields.device_type = self._device_family_features.function.value
        # this renaming of channel_index to device_index is dubious.
        self._reg_uart.fields.device_index = self.channel_index

        self._reg_echo = UARTRegister(const.READ_ECHO_WORD)

        self._addr_settings_header, self._addr_settings_control, self._addr_settings_monitoring = \
            BoardRegisters[const.BoardTypes(channel_ini.Board_type)]

    def read_echo_word(self):
        """
        Read the echo word by sending the appropriate message.
        """
        self._log.debug("READ ECHO WORD")
        echo_cmd_msg = self._reg_echo.get_read_cmd_msg()
        response = self._txrx.send_recv_message(echo_cmd_msg)
        return response

    def get_command_msg(self, cmd):
        """
        Method to construct a command message object (TxMessage).

        The returned object contains the correct address and word for executing the
        specified command and can be sent through the txrx object to the Percival
        hardware.

        :param cmd: command to encode
        :type  cmd: DeviceCmd
        :returns: percival_detector.carrier.txrx.TxMessage
        """
        if not self._device_family_features.supports_cmd(cmd):
            raise TypeError("Device family does not support command %s"%cmd)
        self._reg_uart.fields.device_cmd = cmd.value
        self._log.debug(self._reg_uart.fields)
        cmd_msg = self._reg_uart.get_write_cmd_msg(eom=True)[0]
        return cmd_msg

    def command(self, cmd):
        """
        Method to construct and send a command.

        This method gets the TxMessage object representation of the command and
        sends it through the txrx object to the Percival hardware, returning any
        response.

        :param cmd: command to encode, probably an int / Enum from const.py
        :type  cmd: DeviceCmd
        :returns: list of (address, dataword) tuples
        """
        self._log.debug("Device CommandMap: %s", cmd)
        cmd_msg = self.get_command_msg(cmd)
        self._log.debug("Device CommandMsg: %s", cmd_msg)
        response = self._txrx.send_recv_message(cmd_msg)
        return response

    def cmd_no_operation(self):
        """
        Method to send a no_operation device command.

        :returns: list of (address, dataword) tuples
        """
        result = self.command(DeviceCmd.no_operation)
        return result

    def cmd_set_and_get_value(self):
        """
        Method to send a set_and_get_value device command.

        :returns: list of (address, dataword) tuples
        """
        result = self.command(DeviceCmd.set_and_get_value)
        return result

    def cmd_initialize(self):
        """
        Method to send an initialize command.

        :returns: list of (address, dataword) tuples
        """
        result = None

        # Send an initialize command to the device if it is supported
        if self._device_family_features.supports_cmd(DeviceCmd.initialize):
            result = self.command(DeviceCmd.initialize)

        return result


class ControlChannel(Channel):
    """
    Represent a specific control device channel on any of the control boards.
    """

    def __init__(self, txrx, channel_ini, settings):
        """ ControlChannel constructor. Create a control channel

        Keeps a reference to the txrx communication object and initialises itself based on the parameters in channel_ini.
        Provides the set_value method in addition to the general channel methods

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param channel_ini: Channel configuration parameters from INI file
        :type channel_ini: ControlChannelIniParameters
        :param settings: List of values used to initialise UARTRegister
        :type settings: List
        """
        super(ControlChannel, self).__init__(txrx, channel_ini)

        # Setup this control channels UART register
        # _addr_settings_control is a UARTBlock obtained from BoardRegisters
        # uart_device_address is read from the channel ini object for this channel
        self._reg_control_settings = UARTRegister(self._addr_settings_control, self.uart_device_address)
        # Initialise the UARTRegister map
        self._reg_control_settings.initialize_map(settings)
        self._log.debug("Control Settings Map: %s", self._reg_control_settings.fields)

    def cmd_control_set_value(self, value):
        """
        Method to send the set value command for a control channel.

        :param value: new value to set
        """
        self._log.debug("Device Control Settings write:")
        self._reg_control_settings.fields.value = value
        # Check if the control device is a potentiometer
        if self.device_family == DeviceFamily.AD5242 or self.device_family == DeviceFamily.AD5263:
            # This type of device requires power status set to on (1)
            self._reg_control_settings.fields.power_status = 1
        self._log.debug(self._reg_control_settings.fields)
        cmd_msg = self._reg_control_settings.get_write_cmd_msg(eom=True)
        self._log.debug(cmd_msg)
        # TODO: this is a bit hacky to go this far for the register index...
        value_register_index = self._reg_control_settings.fields._mem_map['value'].word_index
        response = self._txrx.send_recv_message(cmd_msg[value_register_index])
        return response

    def set_value(self, value, timeout=0.1):
        """
        Method to set the value of a control channel.  Sends the following commands:

        * cmd_no_operation
        * cmd_control_set_value
        * cmd_no_operation
        * cmd_set_and_get_value

        :param value: new value to set
        :param timeout: timeout for acknowledgement
        """
        self._log.debug("set_value=%s (\"%s\")", value, self._channel_ini.Channel_name)
        self._log.debug(self._reg_control_settings.fields)
        # Check the value is within range
        if value < self._reg_control_settings.fields.channel_range_min:
            self._log.debug("Cannot set value below minimum of %d", self._reg_control_settings.fields.channel_range_min)
            raise PercivalControlDeviceError("Cannot set channel %s to %d, below minimum of %d",
                                             self._channel_ini.Channel_name,
                                             value,
                                             self._reg_control_settings.fields.channel_range_min)
        if value > self._reg_control_settings.fields.channel_range_max:
            self._log.debug("Cannot set value above maximum of %d", self._reg_control_settings.fields.channel_range_max)
            raise PercivalControlDeviceError("Cannot set channel %s to %d, above maximum of %d",
                                             self._channel_ini.Channel_name,
                                             value,
                                             self._reg_control_settings.fields.channel_range_max)
        # we need to remove these no_op commands.
        self.cmd_no_operation()
        self.cmd_control_set_value(value)
        self.cmd_no_operation()
        self.cmd_set_and_get_value()
        start_time = time.time()
        retries = 0
        while True:
            echo = self.read_echo_word()
            result = generate_register_maps(echo)
            if result[0].i2c_communication_error:
                raise IOError("I2C communication error when writing to \'%s\'" % self._channel_ini.Channel_name)
            if result[0].read_value == value:
                self._log.debug("Read value same a set value %s (\"%s\")", value, self._channel_ini.Channel_name)
                break
            if time.time() > (start_time + timeout):
                raise PercivalControlDeviceError("Readback ECHO word (%d) does not match \'%s\'"
                                                 " demand (%d) after %d retries",
                                                 result[0].read_value,
                                                 self._channel_ini.Channel_name,
                                                 value,
                                                 retries)

            time.sleep(0.1)
            self._log.debug("####### Retrying (%d) reading ECHO word. Got: %s", retries, result)
        return result[0]

    def get_value(self):
        return self._reg_control_settings.fields.value


class MonitoringChannel(Channel):
    """
    Represent a specific monitoring channel on any of the control boards.
    """

    def __init__(self, txrx, channel_ini, settings):
        """ MonitoringChannel constructor. Create a monitoring channel

        Keeps a reference to the txrx communication object and initialises itself based on the parameters in channel_ini.
        Provides the get_value method in addition to the general channel methods

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param channel_ini: Channel configuration parameters from INI file
        :type channel_ini: ControlChannelIniParameters
        :param settings: List of values used to initialise UARTRegister
        :type settings: List
        """
        super(MonitoringChannel, self).__init__(txrx, channel_ini)

        self._reg_monitor_settings = UARTRegister(self._addr_settings_monitoring)
        self._reg_monitor_settings.initialize_map(settings)
        self._log.debug("Monitor Settings Map: %s", self._reg_monitor_settings.fields)

    def get_value(self, timeout=0.1):
        """
        Method to get the value of a monitoring channel.  Sends the following commands:

        * cmd_no_operation
        * cmd_set_and_get_value

        This method will inspect the sample_number of the returned value and only complete
        once the sample_number has incremented (or it times out).  This ensures that the
        value returned is the latest value requested and not an old value.

        :param timeout: timeout for reading the value
        """
        self._log.debug("get_value (\"%s\")", self._channel_ini.Channel_name)
        # We need to store the sample number from the last write
        echo = self.read_echo_word()
        result = generate_register_maps(echo)
        sample_number = result[0].sample_number
        self._log.debug("Initial sample_number %s", sample_number)
        self.cmd_no_operation()
        self.cmd_set_and_get_value()
        start_time = time.time()
        while True:
            echo = self.read_echo_word()
            # Although this is a readout of the echo word, for monitors it provides
            # status as though it was a read value
            result = generate_register_maps(echo)
            self._log.debug("New sample_number %s", result[0].sample_number)
            if result[0].i2c_communication_error:
                raise IOError("I2C communication error when writing to %s", self._channel_ini.Channel_name)
            if result[0].sample_number != sample_number:
                self._log.debug("Sample number has changed %s", result[0].sample_number)
                break
            if time.time() > (start_time + timeout):
                raise RuntimeError("Timeout when reading back value from ECHO word")

            time.sleep(0.1)
            self._log.debug("####### Retrying reading ECHO word. Got: %s", result)

        self._log.debug("got value=%s (\"%s\")", result[0], self._channel_ini.Channel_name)
        return result[0]

