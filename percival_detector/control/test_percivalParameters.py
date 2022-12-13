from unittest import TestCase

from percival_detector.carrier.const import BoardTypes
from percival_detector.carrier.registers import UARTRegister, BoardRegisters
from percival_detector.control.detector import PercivalParameters


class TestPercivalParameters(TestCase):
    def setUp(self):
        self.pp = PercivalParameters()
        self.pp.load_ini()

    def test_list_properties(self):
        self.assertEqual(type(self.pp.monitoring_channels), list)
        self.assertEqual(type(self.pp.control_channels), list)

    def test_plugin_board_control_monitoring_uart_addresses(self):
        """Check that all Plugin Board Control and Monitoring Channels UART addresses are correct in Channel parameters ini file"""
        board = BoardTypes.plugin
        header_block, control_block, monitor_block = BoardRegisters[board]

        control_settings_register = UARTRegister(control_block)
        for addr in range(0, control_settings_register.num_items):
            channel_address = control_settings_register._uart_address + (addr * control_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.control_channel_by_address(channel_address), msg=
                                 "UART address %d for Control Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

        monitor_settings_register = UARTRegister(monitor_block)
        for addr in range(0, monitor_settings_register.num_items):
            channel_address = monitor_settings_register._uart_address + (addr * monitor_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.monitoring_channel_by_address(channel_address), msg=
                                 "UART address %d for Monitoring Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

    def test_carrier_board_control_monitoring_uart_addresses(self):
        """Check that all Carrier Board Control and Monitoring Channels UART addresses are correct in Channel parameters ini file"""
        board = BoardTypes.carrier
        header_block, control_block, monitor_block = BoardRegisters[board]

        control_settings_register = UARTRegister(control_block)
        for addr in range(0, control_settings_register.num_items):
            channel_address = control_settings_register._uart_address + (addr * control_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.control_channel_by_address(channel_address), msg=
                                 "UART address %d for Control Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

        monitor_settings_register = UARTRegister(monitor_block)
        for addr in range(0, monitor_settings_register.num_items):
            channel_address = monitor_settings_register._uart_address + (addr * monitor_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.monitoring_channel_by_address(channel_address), msg=
                                 "UART address %d for Monitoring Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

    def test_left_board_control_monitoring_uart_addresses(self):
        """Check that all Left Board Control and Monitoring Channels UART addresses are correct in Channel parameters ini file"""
        board = BoardTypes.left
        header_block, control_block, monitor_block = BoardRegisters[board]

        control_settings_register = UARTRegister(control_block)
        for addr in range(0, control_settings_register.num_items):
            channel_address = control_settings_register._uart_address + (addr * control_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.control_channel_by_address(channel_address), msg=
                                 "UART address %d for Control Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

        monitor_settings_register = UARTRegister(monitor_block)
        for addr in range(0, monitor_settings_register.num_items):
            channel_address = monitor_settings_register._uart_address + (addr * monitor_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.monitoring_channel_by_address(channel_address), msg=
                                 "UART address %d for Monitoring Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

    def test_bottom_board_control_monitoring_uart_addresses(self):
        """Check that all Bottom Board Control and Monitoring Channels UART addresses are correct in Channel parameters ini file"""
        board = BoardTypes.bottom
        header_block, control_block, monitor_block = BoardRegisters[board]

        control_settings_register = UARTRegister(control_block)
        for addr in range(0, control_settings_register.num_items):
            channel_address = control_settings_register._uart_address + (addr * control_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.control_channel_by_address(channel_address), msg=
                                 "UART address %d for Control Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))

        monitor_settings_register = UARTRegister(monitor_block)
        for addr in range(0, monitor_settings_register.num_items):
            channel_address = monitor_settings_register._uart_address + (addr * monitor_settings_register.words_per_item)
            self.assertIsNotNone(self.pp.monitoring_channel_by_address(channel_address), msg=
                                 "UART address %d for Monitoring Channel #%d on %s not found in \'%s\'. Check ini file or address map in const.py!" %
                                 (channel_address, addr, board, self.pp._channel_params._ini_filename))


