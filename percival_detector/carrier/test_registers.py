'''
Created on 5 Dec 2014

@author: Ulrik Pedersen
'''

from builtins import bytes, range
import unittest, logging
from percival_detector.carrier import registers, txrx, const

logging.basicConfig()
logging.getLogger(__name__).setLevel(logging.DEBUG)


class TestRegisterMapInterfaces(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHeaderInfoInterface(self):
        """carrier.devices.HeaderInfoMap class implements the IRegisterMap interface"""
        self.assertTrue(issubclass(registers.HeaderInfoMap, registers.IRegisterMap),
                        "HeaderInfoMap class does not fully implement the IRegisterMap interface")

    def testControlChannelInterface(self):
        """carrier.devices.ControlChannelMap class implements the IRegisterMap interface"""
        self.assertTrue(issubclass(registers.ControlChannelMap, registers.IRegisterMap),
                        "ControlChannelMap class does not fully implement the IRegisterMap interface")

    def testMonitoringChannelsInterface(self):
        """carrier.devices.MonitoringChannelMap class implements the IRegisterMap interface"""
        self.assertTrue(issubclass(registers.MonitoringChannelMap, registers.IRegisterMap),
                        "MonitoringChannelMap class does not fully implement the IRegisterMap interface")


class TestHeaderInfoMap(unittest.TestCase):
    def setUp(self):
        self.dut = registers.HeaderInfoMap()

    def testMemMapAttributes(self):
        self.assertTrue(hasattr(self.dut, "eeprom_address"))
        self.assertTrue(hasattr(self.dut, "monitoring_channels_count"))
        self.assertTrue(hasattr(self.dut, "control_channels_count"))
        self.assertEqual(self.dut["eeprom_address"], registers.MapField("eeprom_address", 0, 8, 16))
        self.assertEqual(self.dut["monitoring_channels_count"], registers.MapField("monitoring_channels_count", 0, 8, 8))
        self.assertEqual(self.dut["control_channels_count"], registers.MapField("control_channels_count", 0, 8, 0))
        with self.assertRaises(AttributeError):
            self.dut.no_parameter_with_this_name
        self.assertTrue(hasattr(self.dut, "num_words"))
        self.assertEqual(list(self.dut.map_fields).sort(), ["control_channels_count",
                                                             "monitoring_channels_count",
                                                             "eeprom_address"].sort())

    def testParseValidMap(self):
        self.dut.parse_map([0xA1234567])
        self.assertEqual(0x23, self.dut.eeprom_address)
        self.assertEqual(0x45, self.dut.monitoring_channels_count)
        self.assertEqual(0x67, self.dut.control_channels_count)

    def testValidGenerateMap(self):
        self.dut.parse_map([0xA1234567])
        words = self.dut.generate_map()
        self.assertEqual([0x00234567], words)

    def testParseInvalidMap(self):
        """Empty map should raise index error and no values parsed"""
        with self.assertRaises(IndexError):
            self.dut.parse_map([])
        self.assertEqual(None, self.dut.eeprom_address)
        self.assertEqual(None, self.dut.monitoring_channels_count)
        self.assertEqual(None, self.dut.control_channels_count)


class TestControlChannelMap(unittest.TestCase):
    def setUp(self):
        self.dut = registers.ControlChannelMap()

    def testParseValidMap(self):
        # The full 5 word register is not yet in use in the firmware
        #self.dut.parse_map([0xA1234567, 0x89ABCDEF, 0x11223344, 0x55667788, 0x99AABBCC])
        self.dut.parse_map( [0xA1234567, 0x89ABCDEF, 0x11223344,             0x99AABBCC])
        self.assertEqual(0x01, self.dut.board_type)
        self.assertEqual(0x02, self.dut.component_family_id)
        self.assertEqual(0x00, self.dut.device_i2c_bus_select)
        self.assertEqual(0x1A, self.dut.channel_device_id)
        self.assertEqual(0x05, self.dut.channel_sub_address)
        self.assertEqual(0x67, self.dut.device_address)

        self.assertEqual(0x89AB, self.dut.channel_range_max)
        self.assertEqual(0xCDEF, self.dut.channel_range_min)

        self.assertEqual(0x1122, self.dut.channel_default_on)
        self.assertEqual(0x3344, self.dut.channel_default_off)

        # No yet in use in firmware
        #self.assertEqual(0x66, self.dut.channel_monitoring)
        #self.assertEqual(0x77, self.dut.safety_exception_threshold)
        #self.assertEqual(0x88, self.dut.read_frequency)

        self.assertEqual(0x00, self.dut.power_status)
        self.assertEqual(0xBBCC, self.dut.value)

    def testValidGenerateMap(self):
        # The full 5 word register is not yet in use in the firmware
        #self.dut.parse_map([0xA1234567, 0x89ABCDEF, 0x11223344, 0x55667788, 0x99AABBCC])
        self.dut.parse_map( [0xA1234567, 0x89ABCDEF, 0x11223344,             0x99AABBCC])
        words = self.dut.generate_map()
        #self.assertEqual([0x01234567, 0x89ABCDEF, 0x11223344, 0x00667788, 0x0000BBCC], words)
        self.assertEqual( [0xA1234567, 0x89ABCDEF, 0x11223344,             0x0000BBCC], words)

    def testParseInvalidMap(self):
        """Empty map should raise index error and no values parsed"""
        with self.assertRaises(IndexError):
            self.dut.parse_map([0xA1234567, 0x89ABCDEF])
        self.assertEqual(None, self.dut.board_type)
        self.assertEqual(None, self.dut.component_family_id)
        self.assertEqual(None, self.dut.device_i2c_bus_select)
        self.assertEqual(None, self.dut.channel_device_id)
        self.assertEqual(None, self.dut.channel_sub_address)
        self.assertEqual(None, self.dut.device_address)


class TestCommandMap(unittest.TestCase):
    def setUp(self):
        self.dut = registers.CommandMap()

    def testInitialMapFieldValue(self):
        self.assertIs(self.dut.device_index, None, "device_index should be initialised to None")
        self.assertTrue("device_index" in list(self.dut._mem_map.keys()), "No device index in: %s"%str(list(self.dut._mem_map.keys())))
        self.dut.device_index = 10
        self.assertIs(self.dut.device_index, 10, "device_index should now be set to 10, not %s"%str(self.dut.device_index))


class TestEchoWordMap(unittest.TestCase):
    def setUp(self):
        self.dut = registers.EchoWordMap()

    def testInitialMapFieldValue(self):
        self.assertIs(self.dut.read_value, None, "read_value should be initialised to None")
        self.assertTrue("read_value" in list(self.dut._mem_map.keys()), "No read_value in: %s"%str(list(self.dut._mem_map.keys())))
        self.dut.read_value = 10
        self.assertIs(self.dut.read_value, 10, "read_value should now be set to 10, not %s"%str(self.dut.read_value))


class TestReadValueMap(unittest.TestCase):
    def setUp(self):
        self.dut = registers.ReadValueMap()

    def testInitialMapFieldValue(self):
        self.assertIs(self.dut.sample_number, None, "sample_number should be initialised to None")
        self.assertTrue("sample_number" in list(self.dut._mem_map.keys()), "No sample_number in: %s"%str(list(self.dut._mem_map.keys())))
        self.dut.sample_number = 10
        self.assertIs(self.dut.sample_number, 10, "sample_number should now be set to 10, not %s"%str(self.dut.sample_number))


class TestMapField(unittest.TestCase):
    def setUp(self):
        self.dut = registers.MapField("TEST", 2, 3, 4)

    def TestName(self):
        self.assertEqual(self.dut.name, "TEST")

    def TestProps(self):
        self.assertEqual(self.dut.num_bits, 3)
        self.assertEqual(self.dut.bit_offset, 4)
        self.assertEqual(self.dut.word_index, 2)
        self.assertEqual(self.dut.value, None)

    def TestValue(self):
        self.assertEqual(self.dut.value, None)
        with self.assertRaises(ValueError):
            self.dut.insert_field_value([0x00, 0x00])
        self.dut.value = 45
        self.assertEqual(self.dut.value, 45)
        self.assertEqual(self.dut._value, 45)


class TestUARTRegister(unittest.TestCase):

    def setUp(self):
        self.command_reg = registers.UARTRegister(const.COMMAND)  # CommandMap Register
        cl = ".".join([__name__, str(self.__class__)])
        self._log = logging.getLogger(cl)

    def test_invalid_command_readback_msg(self):
        """Check that a Readback message from get_read_cmdmsg() throws an exception
        CommandMap has no readback shortcut"""
        with self.assertRaises(TypeError) as cm: self.command_reg.get_read_cmd_msg()

    def test_write_msg(self):
        self.command_reg.fields.parse_map([0, 1, 2])
        self.assertEqual(self.command_reg.fields.device_index, 0)
        self.assertEqual(self.command_reg.fields.device_cmd, 0)
        msg = self.command_reg.get_write_cmd_msg()
        self.assertTrue(type(msg), list)
        self.assertIsInstance(msg[0], txrx.TxMessage)
        self.assertEqual(len(msg), 3)
        expected_msg = [bytes.fromhex("02ca 00 00 00 00"),
                        bytes.fromhex("02cb 00 00 00 01"),
                        bytes.fromhex("02cc 00 00 00 02"),];
        for i in range(3):
            self.assertEqual(msg[i].message, expected_msg[i], msg[i].message)


class TestRegister(unittest.TestCase):
    def setUp(self):
        addr = const.CONTROL_SETTINGS_CARRIER.start_address
        self.addr_word = [
            (addr + 0, 0x000A),
            (addr + 1, 0x00A0),
            (addr + 2, 0x0A00),
            (addr + 3, 0xA000),
            (addr + 4, 0x000B),
            (addr + 5, 0x00B0),
            (addr + 6, 0x0B00),
            (addr + 7, 0xB000),
        ]

    def test_generate_maps(self):
        regs = registers.generate_register_maps(self.addr_word)
        self.assertIsInstance(regs, list)
        self.assertEqual(len(regs), 2)
        self.assertIsInstance(regs[0], registers.ControlChannelMap)

    def test_too_many_words(self):
        regs = registers.generate_register_maps(self.addr_word[:-1])
        self.assertIsInstance(regs, list)
        self.assertEqual(len(regs), 1)

    def test_too_few_words(self):
        regs = registers.generate_register_maps(self.addr_word[:3])
        self.assertIsInstance(regs, list)
        self.assertEqual(len(regs), 0)

    def test_misaligned_words(self):
        regs = registers.generate_register_maps(self.addr_word[1:])
        self.assertIsInstance(regs, list)
        self.assertEqual(len(regs), 1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

