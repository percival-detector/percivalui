

import unittest, logging
from mock import MagicMock, call
from builtins import bytes

import percival_detector.carrier.const as const
from percival_detector.carrier.sensor import Sensor

class TestSensorClass(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.buffer_cmd = MagicMock()
        self.sensor = Sensor(self.buffer_cmd)

        # Execute the send_setup_to_dac command
        self.buffer_cmd.send_dacs_setup_cmd = MagicMock()
        self.sensor.apply_dac_values({"iBiasPLL_H1" : 1, "Master_DAC_Current_H0" : 2});
        self.buffer_cmd.send_dacs_setup_cmd.assert_called_with([0x01<<2,0,0,0,0,0x02<<2,0])

    def test_values_to_data_word(self):
        # Verify the combining of configuration values for ADCs which are operational
        test_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(self.sensor.configuration_values_to_word(3, test_values), 0)
        test_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(self.sensor.configuration_values_to_word(3, test_values), 613566756)
        test_values = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2]
        self.assertEqual(self.sensor.configuration_values_to_word(3, test_values), 701216808)

        # Verify too many values will generate an exception
        with self.assertRaises(RuntimeError):
            test_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            self.sensor.configuration_values_to_word(3, test_values)

        # Try 6 bit values
        test_values = [0, 0, 0, 0, 0]
        self.assertEqual(self.sensor.configuration_values_to_word(6, test_values), 0)
        test_values = [1, 1, 1, 1, 1]
        self.assertEqual(self.sensor.configuration_values_to_word(6, test_values), 68174084)

        # Verify too many values will generate an exception
        with self.assertRaises(RuntimeError):
            test_values = [1, 1, 1, 1, 1, 1]
            self.sensor.configuration_values_to_word(6, test_values)

    def test_apply_configuration(self):
        self.buffer_cmd.send_configuration_setup_cmd = MagicMock()
        test_config = {
            'H1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                   0, 0, 0, 0, 5],
            'H0': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                   0, 0, 5],
            'G': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                  0, 0, 0, 0, 5]
        }
        self.sensor.apply_configuration(test_config)
        # Verify that the buffer command was called with the correct words
        self.buffer_cmd.send_configuration_setup_cmd.assert_called_with([0x04,
                                                                         0x08,
                                                                         0x0C,
                                                                         0x10,
                                                                         0xA0000,
                                                                         0x20000,
                                                                         0x40000,
                                                                         0x60000,
                                                                         0x80500,
                                                                         0x100,
                                                                         0x200,
                                                                         0x300,
                                                                         0x400,
                                                                         0x2800000])

    def test_apply_debug(self):
        self.buffer_cmd.send_debug_setup_cmd = MagicMock()
        test_debug = {
            'debug_dmxSEL': 1,
            'debug_SC': 1,
            'debug_adcCPN': 1
        }
        # 010011 is replicated 5 times into
        # 01001101 00110100 11010011 01001100 = 0x4d34d34c
        self.sensor.apply_debug(test_debug)
        
        correctresult = [0x4d34d34c for i in range(9)];
        self.buffer_cmd.send_debug_setup_cmd.assert_called_once_with(correctresult);

    def test_combine_9bit_lists_into_8bit_list(self):
        test_list_1 = [1,1,1,1]
        test_list_2 = [1,1,1,1]
        self.assertEqual(self.sensor.combine_9bit_lists_into_8bit_list(test_list_1, test_list_2),
                         [0, 128, 64, 32, 16, 8, 4, 2, 1])

        test_list_1 = [1, 2, 3, 4]
        test_list_2 = [5, 6, 7, 8]
        self.assertEqual(self.sensor.combine_9bit_lists_into_8bit_list(test_list_1, test_list_2),
                         [0, 129, 64, 64, 96, 24, 28, 8, 8])

    def test_combine_8bit_lists_into_32bit_list(self):
        test_list_1 = [1, 2, 3, 4]
        test_list_2 = [5, 6, 7, 8]
        test_list_3 = [9, 10, 11, 12]
        test_list_4 = [13, 14, 15, 16]
        self.assertEqual(self.sensor.combine_8bit_lists_into_32bit_list(test_list_1,
                                                                        test_list_2,
                                                                        test_list_3,
                                                                        test_list_4),
                         [17107213, 33950222, 50793231, 67636240])

    def test_apply_calibration(self):
        self.buffer_cmd.send_calibration_setup_cmd = MagicMock()
        test_calibration = {'H1':{'Cal0': {'Right': [1, 2, 3, 4],
                                           'Left': [5, 6, 7, 8]},
                                  'Cal1': {'Right': [9, 10, 11, 12],
                                           'Left': [13, 14, 15, 16]},
                                  'Cal2': {'Right': [17, 18, 19, 20],
                                           'Left': [21, 22, 23, 24]},
                                  'Cal3': {'Right': [25, 26, 27, 28],
                                           'Left': [29, 30, 31, 32]},
                                  },
                            'H0': {'Cal0': {'Right': [33, 34, 35, 36],
                                            'Left': [37, 38, 39, 40]},
                                   'Cal1': {'Right': [41, 42, 43, 44],
                                            'Left': [45, 46, 47, 48]},
                                   'Cal2': {'Right': [49, 50, 51, 52],
                                            'Left': [53, 54, 55, 56]},
                                   'Cal3': {'Right': [57, 58, 59, 60],
                                            'Left': [61, 62, 63, 64]},
                                   },
                            'G':  {'Cal0': {'Right': [65, 66, 67, 68],
                                            'Left': [69, 70, 71, 72]},
                                   'Cal1': {'Right': [73, 74, 75, 76],
                                            'Left': [77, 78, 79, 80]},
                                   'Cal2': {'Right': [81, 82, 83, 84],
                                            'Left': [85, 86, 87, 88]},
                                   'Cal3': {'Right': [89, 90, 91, 92],
                                            'Left': [93, 94, 95, 96]},
                                   }
                            }
        self.sensor.apply_calibration(test_calibration)

        self.buffer_cmd.send_calibration_setup_cmd.assert_called_with([0x0004080C,
                                                                       0x81838587,
                                                                       0x40414243,
                                                                       0x40404141,
                                                                       0x60E060E0,
                                                                       0x185898D8,
                                                                       0x1C3C5C7C,
                                                                       0x08182838,
                                                                       0x08101820,
                                                                       0x1014181C,
                                                                       0x898B8D8F,
                                                                       0x44454647,
                                                                       0x42424343,
                                                                       0x61E161E1,
                                                                       0x185898D8,
                                                                       0x9CBCDCFC,
                                                                       0x48586878,
                                                                       0x28303840,
                                                                       0x2024282C,
                                                                       0x91939597,
                                                                       0x48494A4B,
                                                                       0x44444545,
                                                                       0x62E262E2,
                                                                       0x195999D9,
                                                                       0x1C3C5C7C,
                                                                       0x8898A8B8,
                                                                       0x48505860])

