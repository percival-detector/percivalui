"""
Created on 10 June 2016

:author: Alan Greer
"""


import logging

from percival_detector.carrier.registers import UARTRegister, BoardRegisters


class BoardSettings:
    """
    Class to represent the settings of a Percival board.  This class can be used to
    initialise a board from an ini file, or to read back settings from the board.
    """
    def __init__(self, txrx, board):
        """
        Constructor.

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param board: Which board to initialise/read
        :type  board: BoardTypes
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self.txrx = txrx
        self.board = board
        self._header_block, self._control_block, self._monitoring_block = BoardRegisters[board]

        self._reg_header_settings = UARTRegister(self._header_block)

        self._reg_control_settings = UARTRegister(self._control_block)
        self._control_settings = None

        self._reg_monitoring_settings = UARTRegister(self._monitoring_block)
        self._monitoring_settings = None

    def initialise_board(self, ini):
        """
        Initialise the hardware from the settings provided by the ini object.

        :param ini: The initialisation object to use for sending messages to the hardware
        """
        # Create the settings message
        self._reg_header_settings.fields.eeprom_address = 0x50
        self._reg_header_settings.fields.monitoring_channels_count = ini.monitoring_channels_count(self.board)
        self._reg_header_settings.fields.control_channels_count = ini.control_channels_count(self.board)
        cmd_msg = self._reg_header_settings.get_write_cmd_msg(True)

        # Initialise the control channels
        #self._log.info(self._reg_control_settings.num_items)
        self._control_settings = {}
        self._log.info("Num Items: %d", self._reg_control_settings.num_items)
        for address in range(0, self._reg_control_settings.num_items):
            channel_address = self._reg_control_settings._uart_address + (address * self._reg_control_settings.words_per_item)
            channel = ini.control_channel_by_address(channel_address)
            #self._log.info(channel_address)
            #self._log.info("self._reg_control_settings._uart_address: %d", self._reg_control_settings._uart_address)
            #self._log.info("address: %d", address)
            #self._log.info("self._reg_control_settings.words_per_item: %d", self._reg_control_settings.words_per_item)
            #self._log.info("Uart address %02X", self._reg_control_settings._uart_address + (address * self._reg_control_settings.words_per_item))
            #self._log.info(channel)

            self._control_settings[address] = UARTRegister(self._control_block, channel_address)

            self._control_settings[address].fields.channel_id = channel.Channel_ID
            self._control_settings[address].fields.device_address = 0
            self._control_settings[address].fields.board_type = channel.Board_type
            self._control_settings[address].fields.component_family_id = channel.Component_family_ID
            self._control_settings[address].fields.device_i2c_bus_select = channel.I2C_bus_selection
            self._control_settings[address].fields.channel_device_id = channel.Device_ID
            self._control_settings[address].fields.channel_sub_address = channel.I2C_Sub_address
            self._control_settings[address].fields.device_address = channel.I2C_address
            self._control_settings[address].fields.channel_range_max = channel.Maximum_value
            self._control_settings[address].fields.channel_range_min = channel.Minimum_value
            self._control_settings[address].fields.channel_default_on = channel.Default_ON_value
            self._control_settings[address].fields.channel_default_off = channel.Default_OFF_value
            self._control_settings[address].fields.power_status = channel.Power_status
            self._control_settings[address].fields.value = channel.Value
            try:
                cmd_msg += self._control_settings[address].get_write_cmd_msg(True)
            except:
                self._log.info(channel_address)
                self._log.info("self._reg_control_settings._uart_address: %d", self._reg_control_settings._uart_address)
                self._log.info("address: %d", address)
                self._log.info("self._reg_control_settings.words_per_item: %d", self._reg_control_settings.words_per_item)
                self._log.info("Uart address %02X", self._reg_control_settings._uart_address + (address * self._reg_control_settings.words_per_item))
                self._log.info(channel)
                raise

        # Initialise the control channels
        # self._log.info(self._reg_control_settings.num_items)
        self._monitoring_settings = {}
        for address in range(0, self._reg_monitoring_settings.num_items):
            channel_address = self._reg_monitoring_settings._uart_address + (address * self._reg_monitoring_settings.words_per_item)
            channel = ini.monitoring_channel_by_address(channel_address)
            #self._log.info(channel_address)
            #self._log.info("Uart address %02X", self._reg_monitoring_settings._uart_address + (address * self._reg_monitoring_settings.words_per_item))
            #self._log.info(channel.Channel_ID)

            self._monitoring_settings[address] = UARTRegister(self._monitoring_block, channel_address)

            #self._log.info("Channel ID: %d", channel.Channel_ID)
            self._monitoring_settings[address].fields.channel_id = channel.Channel_ID
            self._monitoring_settings[address].fields.device_address = 0
            self._monitoring_settings[address].fields.board_type = channel.Board_type
            self._monitoring_settings[address].fields.component_family_id = channel.Component_family_ID
            self._monitoring_settings[address].fields.device_i2c_bus_select = channel.I2C_bus_selection
            self._monitoring_settings[address].fields.channel_device_id = channel.Device_ID
            self._monitoring_settings[address].fields.channel_sub_address = channel.I2C_Sub_address
            self._monitoring_settings[address].fields.device_address = channel.I2C_address
            self._monitoring_settings[address].fields.channel_ext_low_threshold = channel.Extreme_low_threshold
            self._monitoring_settings[address].fields.channel_ext_high_threshold = channel.Extreme_high_threshold
            self._monitoring_settings[address].fields.channel_low_threshold = channel.Low_threshold
            self._monitoring_settings[address].fields.channel_high_threshold = channel.High_threshold
            self._monitoring_settings[address].fields.safety_action_0_select = channel.Safety_action_0_select
            self._monitoring_settings[address].fields.safety_action_1_select = channel.Safety_action_1_select
            self._monitoring_settings[address].fields.safety_action_2_select = channel.Safety_action_2_select
            self._monitoring_settings[address].fields.safety_action_3_select = channel.Safety_action_3_select
            self._monitoring_settings[address].fields.safety_action_4_select = channel.Safety_action_4_select
            self._monitoring_settings[address].fields.safety_action_5_select = channel.Safety_action_5_select
            self._monitoring_settings[address].fields.safety_action_6_select = channel.Safety_action_6_select
            self._monitoring_settings[address].fields.safety_action_7_select = channel.Safety_action_7_select			
            self._monitoring_settings[address].fields.safety_exception_threshold = channel.Safety_exception_threshold
            self._monitoring_settings[address].fields.read_frequency = channel.Read_frequency
            try:
                cmd_msg += self._monitoring_settings[address].get_write_cmd_msg(True)
            except:
                self._log.info(channel_address)
                self._log.info("Uart address %02X", self._reg_monitoring_settings._uart_address + (address * self._reg_monitoring_settings.words_per_item))
                self._log.info(channel)
                raise

        return cmd_msg

    def _readback_settings(self, uart_register):
        """
        Generate the command message for reading the settings, send it and
        return the response.

        :param uart_register: UART register to construct read command message
        :type  uart_register: UARTRegister
        :returns: list of (address, dataword) tuples
        """
        cmd_msg = uart_register.get_read_cmd_msg()
        response = self.txrx.send_recv_message(cmd_msg)
        return response

    def readback_control_settings(self):
        """
        Generate the command message for reading the control settings, send it and
        store the response
        """
        self._log.debug("Readback Board Control Settings")
        self._control_settings = self._readback_settings(self._reg_control_settings)

    def device_control_settings(self, device_addr):
        """
        Return the device control settings for the specified device address.

        :param device_addr: Address of device
        :returns: settings of the device
        """
        offset = device_addr - self._control_block.start_address
        if not self._control_block.is_address_valid(device_addr):
            raise IndexError("Device address 0x%X not in range of block 0x%X" %
                             (device_addr, self._control_block.start_address))
        result = self._control_settings[offset:offset+self._reg_control_settings.words_per_item]
        return result

    def device_monitoring_settings(self, device_addr):
        """
        Return the device monitoring settings for the specified device address.

        :param device_addr: Address of device
        :returns: settings of the device
        """
        offset = device_addr - self._monitoring_block.start_address
        if not self._monitoring_block.is_address_valid(device_addr):
            raise IndexError("Device address 0x%X not in range of block 0x%X" %
                             (device_addr, self._monitoring_block.start_address))
        result = self._monitoring_settings[offset:offset+self._reg_monitoring_settings.words_per_item]
        return result

    def readback_monitoring_settings(self):
        """
        Generate the command message for reading the monitoring settings, send it and
        store the response
        """
        self._log.debug("Readback Board Monitoring Settings")
        self._monitoring_settings = self._readback_settings(self._reg_monitoring_settings)

