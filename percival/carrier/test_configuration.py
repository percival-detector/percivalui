import unittest
import os
from percival.carrier.configuration import find_file, ChannelParameters, BoardParameters, ControlParameters,\
    SensorConfigurationParameters, SensorCalibrationParameters, SensorDebugParameters
from percival.carrier.const import BoardTypes


class TestConfiguration(unittest.TestCase):
    def test_find_file(self):
        # Create a nonsense search path
        os.environ["PERCIVAL_CONFIG_DIR"] = str(":/dir1:/dir2")
        # Verify an appropriate error is raised
        with self.assertRaises(IOError):
            find_file("config/nofile.ini")

        # Create a valid search path
        fl = open("/tmp/testfile.ini", "w");
        fl.close();
        os.environ["PERCIVAL_CONFIG_DIR"] = str("/tmp")
        fn = find_file("testfile.ini")
        # Verify the file is found
        self.assertEqual(fn, "/tmp/testfile.ini")


class TestChannelParameters(unittest.TestCase):
    def setUp(self):
        f = open("/tmp/ChannelParameters.ini", "w+")
        f.write("\
[Control_channel<0001>]\n\
UART_address = 10\n\
Board_type = 0\n\
Channel_name = \"\"\n\
I2C_address = 0\n\
I2C_Sub_address = 0\n\
I2C_bus_selection = 0\n\
Component_family_ID = 0\n\
Device_ID = 0\n\
Channel_ID = 0\n\
Minimum_value = 0\n\
Maximum_value = 0\n\
Default_OFF_value = 0\n\
Default_ON_value = 0\n\
Value = 0\n\
Power_status = FALSE\n\
Channel_offset = 0\n\
Channel_multiplier = 1\n\
Channel_divider = 1\n\
Channel_unit = \"\"\n\
\n\
[Control_channel<0002>]\n\
UART_address = 19\n\
Board_type = 3\n\
Channel_name = \"VCH0\"\n\
I2C_address = 84\n\
I2C_Sub_address = 0\n\
I2C_bus_selection = 0\n\
Component_family_ID = 3\n\
Device_ID = 0\n\
Channel_ID = 0\n\
Minimum_value = 0\n\
Maximum_value = 65535\n\
Default_OFF_value = 0\n\
Default_ON_value = 65535\n\
Value = 0\n\
Power_status = FALSE\n\
Channel_offset = 0\n\
Channel_multiplier = 1\n\
Channel_divider = 1\n\
Channel_unit = \"\"\n\
\n\
[Monitoring_channel<0000>]\n\
UART_address = 75\n\
Board_type = 3\n\
Channel_name = \"VCH0\"\n\
I2C_address = 25\n\
I2C_Sub_address = 0\n\
I2C_bus_selection = 2\n\
Component_family_ID = 7\n\
Device_ID = 3\n\
Channel_ID = 0\n\
Extreme_low_threshold = 0\n\
Extreme_high_threshold = 4095\n\
Low_threshold = 0\n\
High_threshold = 4095\n\
Safety_action_0_select = no\n\
Safety_action_1_select = no\n\
Safety_action_2_select = no\n\
Safety_action_3_select = no\n\
Safety_action_4_select = no\n\
Safety_action_5_select = no\n\
Safety_action_6_select = no\n\
Safety_action_7_select = no\n\
Read_frequency = 1\n\
Safety_exception_threshold = 1\n\
Minimum_value = 0\n\
Maximum_value = 0\n\
Offset = 0\n\
Multiplier = 1\n\
Divider = 1000\n\
Unit = \"V\"\n\
\n\
[Monitoring_channel<0001>]\n\
UART_address = 79\n\
Board_type = 3\n\
Channel_name = \"VCH1\"\n\
I2C_address = 25\n\
I2C_Sub_address = 1\n\
I2C_bus_selection = 2\n\
Component_family_ID = 7\n\
Device_ID = 3\n\
Channel_ID = 1\n\
Extreme_low_threshold = 0\n\
Extreme_high_threshold = 4095\n\
Low_threshold = 0\n\
High_threshold = 4095\n\
Safety_action_0_select = no\n\
Safety_action_1_select = no\n\
Safety_action_2_select = no\n\
Safety_action_3_select = no\n\
Safety_action_4_select = no\n\
Safety_action_5_select = no\n\
Safety_action_6_select = no\n\
Safety_action_7_select = no\n\
Read_frequency = 1\n\
Safety_exception_threshold = 1\n\
Minimum_value = 0\n\
Maximum_value = 0\n\
Offset = 0\n\
Multiplier = 1\n\
Divider = 1000\n\
Unit = \"V\"\n\
\n\
")

    f = open("/tmp/ChannelNONE.ini", "w+")
    f.write("")

    def test_get_channels(self):
        cp = ChannelParameters("/tmp/ChannelParameters.ini")
        cp.load_ini()
        self.assertEqual(type(cp.control_channels), list)
        self.assertEqual(type(cp.monitoring_channels), list)
        self.assertEqual(cp.control_channels_by_name("VCH0").UART_address, 19)
        self.assertEqual(cp.control_channel_name_by_index(1), "Control_channel<0001>")
        self.assertEqual(cp.monitoring_channel_name_by_id_and_board_type(1, BoardTypes.carrier), "VCH1")
        self.assertEqual(cp.monitoring_channel_by_address(79).Channel_name, "VCH1")
        self.assertEqual(str(cp), "<ChannelParameters: inifile: /tmp/ChannelParameters.ini Control channels: 2 Monitoring channels: 2>")
        cp = ChannelParameters("/tmp/ChannelNONE.ini")
        cp.load_ini()
        self.assertEqual(str(cp), "<ChannelParameters: inifile: /tmp/ChannelNONE.ini Control channels: [] Monitoring channels: []>")

    def test_channel_parameters(self):
        cp = ChannelParameters("/tmp/ChannelParameters.ini")
        cp.load_ini()
        self.assertEqual(type(cp.control_channels), list)
        self.assertEqual(type(cp.monitoring_channels), list)
        self.assertEqual(len(cp.control_channels), 2)
        self.assertEqual(len(cp.monitoring_channels), 2)



class TestBoardParameters(unittest.TestCase):
    def setUp(self):
        f = open("/tmp/BoardCARRIER.ini", "w+")
        f.write("\
[Board_header]\n\
Board_name = \"PercivalAdapter V2.0 (S/N: 000002)\"\n\
Board_type = 3\n\
Board_revision_number = 0\n\
\n\
[Entry_counts]\n\
Components_count = 6\n\
Devices_count = 7\n\
Control_channels_count = 14\n\
Monitoring_channels_count = 19\n\
Total_channels_count = 33\n\
\n\
")
        f = open("/tmp/BoardNONE.ini", "w+")
        f.write("")

    def test_board_parameters(self):
        bp = BoardParameters("/tmp/BoardCARRIER.ini")
        bp.load_ini()
        self.assertEqual(bp.board_name, '\"PercivalAdapter V2.0 (S/N: 000002)\"')
        self.assertEqual(bp.board_type, BoardTypes.carrier)
        self.assertEqual(bp.board_revision, 0)
        self.assertEqual(bp.control_channels_count, 14)
        self.assertEqual(bp.monitoring_channels_count, 19)

    def test_board_exceptions(self):
        bp = BoardParameters("/tmp/BoardNONE.ini")
        bp.load_ini()
        with self.assertRaises(RuntimeError):
            self.assertEqual(bp.board_name, '\"PercivalAdapter V2.0 (S/N: 000002)\"')
        with self.assertRaises(RuntimeError):
            self.assertEqual(bp.board_type, BoardTypes.carrier)
        with self.assertRaises(RuntimeError):
            self.assertEqual(bp.board_revision, 0)
        with self.assertRaises(RuntimeError):
            self.assertEqual(bp.control_channels_count, 14)
        with self.assertRaises(RuntimeError):
            self.assertEqual(bp.monitoring_channels_count, 19)


class TestControlParameters(unittest.TestCase):
    def setUp(self):
        f = open("/tmp/Percival.ini", "w+")
        f.write("\
[Control]\n\
carrier_ip = \"127.0.0.1\"\n\
\n\
[Configuration]\n\
system_settings_file = \"config/SystemSettings.ini\"\n\
download_system_settings = True\n\
chip_readout_settings_file = \"config/ChipReadoutSettings.ini\"\n\
download_chip_readout_settings = True\n\
clock_settings_file = \"config/ClockSettings.ini\"\n\
download_clock_settings = True\n\
sensor_configuration_file = \"config/SensorConfiguration.ini\"\n\
download_sensor_configuration = True\n\
sensor_calibration_file = \"config/SensorCalibration.ini\"\n\
download_sensor_calibration = True\n\
sensor_debug_file = \"config/SensorDebug.ini\"\n\
download_sensor_debug = True\n\
board_bottom_settings_file = \"config/Board BOTTOM.ini\"\n\
board_carrier_settings_file = \"config/Board CARRIER.ini\"\n\
board_left_settings_file = \"config/Board LEFT.ini\"\n\
board_plugin_settings_file = \"config/Board PLUGIN.ini\"\n\
channel_settings_file = \"config/Channel parameters.ini\"\n\
")
        f = open("/tmp/PercivalNONE.ini", "w+")
        f.write("")

    def test_control_parameters(self):
        pp = ControlParameters("/tmp/Percival.ini")
        pp.load_ini()
        self.assertEqual(pp.carrier_ip, '127.0.0.1')
        self.assertEqual(pp.system_settings_file, 'config/SystemSettings.ini')
        self.assertEqual(pp.chip_readout_settings_file, 'config/ChipReadoutSettings.ini')
        self.assertEqual(pp.clock_settings_file, 'config/ClockSettings.ini')
        self.assertEqual(pp.sensor_configuration_file, 'config/SensorConfiguration.ini')
        self.assertEqual(pp.sensor_calibration_file, 'config/SensorCalibration.ini')
        self.assertEqual(pp.sensor_debug_file, 'config/SensorDebug.ini')
        self.assertEqual(pp.board_bottom_settings_file, 'config/Board BOTTOM.ini')
        self.assertEqual(pp.board_carrier_settings_file, 'config/Board CARRIER.ini')
        self.assertEqual(pp.board_left_settings_file, 'config/Board LEFT.ini')
        self.assertEqual(pp.board_plugin_settings_file, 'config/Board PLUGIN.ini')
        self.assertEqual(pp.channel_settings_file, 'config/Channel parameters.ini')

    def test_control_exceptions(self):
        pp = ControlParameters("/tmp/PercivalNONE.ini")
        pp.load_ini()
        with self.assertRaises(RuntimeError):
            self.assertEqual(pp.carrier_ip, '127.0.0.1')


class TestSensorConfigurationParameters(unittest.TestCase):
    def setUp(self):
        self._ini_description = "[General]\n" \
                                "Cols<H1>=5\n" \
                                "Cols<H0>=4\n" \
                                "Cols<G>=3\n" \
                                "\n" \
                                "[H1]\n" \
                                "Col<0>=5\n" \
                                "Col<1>=4\n" \
                                "Col<2>=3\n" \
                                "Col<3>=2\n" \
                                "Col<4>=1\n" \
                                "\n" \
                                "[H0]\n" \
                                "Col<0>=1\n" \
                                "Col<1>=2\n" \
                                "Col<2>=3\n" \
                                "Col<3>=4\n" \
                                "\n" \
                                "[G]\n" \
                                "Col<0>=3\n" \
                                "Col<1>=2\n" \
                                "Col<2>=1\n" \
                                "\n"

    def test_configuration_parameters(self):
        cp = SensorConfigurationParameters(self._ini_description)
        cp.load_ini()
        self.assertEqual(cp.value_map, {'H1': [5, 4, 3, 2, 1],
                         'H0': [1, 2, 3, 4],
                         'G': [3, 2, 1]})


class TestSensorCalibrationParameters(unittest.TestCase):
    def setUp(self):
        self._ini_description = "[General]\n" \
                                "Cols<H1>=3\n" \
                                "Cols<H0>=2\n" \
                                "Cols<G>=1\n" \
                                "target_signals=4\n" \
                                "\n" \
                                "[H1]\n" \
                                "RightCal<0>Col<0>=1\n" \
                                "LeftCal<0>Col<0>=2\n" \
                                "RightCal<1>Col<0>=3\n" \
                                "LeftCal<1>Col<0>=4\n" \
                                "RightCal<2>Col<0>=5\n" \
                                "LeftCal<2>Col<0>=6\n" \
                                "RightCal<3>Col<0>=7\n" \
                                "LeftCal<3>Col<0>=8\n" \
                                "RightCal<0>Col<1>=9\n" \
                                "LeftCal<0>Col<1>=10\n" \
                                "RightCal<1>Col<1>=11\n" \
                                "LeftCal<1>Col<1>=12\n" \
                                "RightCal<2>Col<1>=13\n" \
                                "LeftCal<2>Col<1>=14\n" \
                                "RightCal<3>Col<1>=15\n" \
                                "LeftCal<3>Col<1>=16\n" \
                                "RightCal<0>Col<2>=17\n" \
                                "LeftCal<0>Col<2>=18\n" \
                                "RightCal<1>Col<2>=19\n" \
                                "LeftCal<1>Col<2>=20\n" \
                                "RightCal<2>Col<2>=21\n" \
                                "LeftCal<2>Col<2>=22\n" \
                                "RightCal<3>Col<2>=23\n" \
                                "LeftCal<3>Col<2>=24\n" \
                                "\n" \
                                "[H0]\n" \
                                "RightCal<0>Col<0>=25\n" \
                                "LeftCal<0>Col<0>=26\n" \
                                "RightCal<1>Col<0>=27\n" \
                                "LeftCal<1>Col<0>=28\n" \
                                "RightCal<2>Col<0>=29\n" \
                                "LeftCal<2>Col<0>=30\n" \
                                "RightCal<3>Col<0>=31\n" \
                                "LeftCal<3>Col<0>=32\n" \
                                "RightCal<0>Col<1>=33\n" \
                                "LeftCal<0>Col<1>=34\n" \
                                "RightCal<1>Col<1>=35\n" \
                                "LeftCal<1>Col<1>=36\n" \
                                "RightCal<2>Col<1>=37\n" \
                                "LeftCal<2>Col<1>=38\n" \
                                "RightCal<3>Col<1>=39\n" \
                                "LeftCal<3>Col<1>=40\n" \
                                "\n" \
                                "[G]\n" \
                                "RightCal<0>Col<0>=41\n" \
                                "LeftCal<0>Col<0>=42\n" \
                                "RightCal<1>Col<0>=43\n" \
                                "LeftCal<1>Col<0>=44\n" \
                                "RightCal<2>Col<0>=45\n" \
                                "LeftCal<2>Col<0>=46\n" \
                                "RightCal<3>Col<0>=47\n" \
                                "LeftCal<3>Col<0>=48\n" \
                                "\n"

    def test_configuration_parameters(self):
        cp = SensorCalibrationParameters(self._ini_description)
        cp.load_ini()
        self.assertEqual(cp.value_map, {'H1': {'Cal0': {'Right' :[1, 9, 17],
                                                        'Left': [2, 10, 18]},
                                               'Cal1': {'Right': [3, 11, 19],
                                                        'Left': [4, 12, 20]},
                                               'Cal2': {'Right': [5, 13, 21],
                                                        'Left': [6, 14, 22]},
                                               'Cal3': {'Right': [7, 15, 23],
                                                        'Left': [8, 16, 24]},
                                               },
                                        'H0': {'Cal0': {'Right': [25, 33],
                                                        'Left': [26, 34]},
                                               'Cal1': {'Right': [27, 35],
                                                        'Left': [28, 36]},
                                               'Cal2': {'Right': [29, 37],
                                                        'Left': [30, 38]},
                                               'Cal3': {'Right': [31, 39],
                                                        'Left': [32, 40]},
                                               },
                                        'G': {'Cal0': {'Right': [41],
                                                       'Left': [42]},
                                              'Cal1': {'Right': [43],
                                                       'Left': [44]},
                                              'Cal2': {'Right': [45],
                                                       'Left': [46]},
                                              'Cal3': {'Right': [47],
                                                       'Left': [48]},
                                              }
                                        })


class TestSensorDebugParameters(unittest.TestCase):
    def setUp(self):
        self._ini_description = "[Debug]\n"\
                                "debug_CLKin = 1\n"\
                                "debug_adcCPN = 0\n"\
                                "\n";

    def test_debug_parameters(self):
        cp = SensorDebugParameters(self._ini_description)
        cp.load_ini()
        self.assertEqual(cp.value_map, {'debug_CLKin': '1', 'debug_adcCPN': '0'})


if __name__ == '__main__':
    unittest.main()
