'''
Created on 15 July 2016

:author: Alan Greer

A class representation for the Percival Sensor.

This class will maintain the sensor DACs, and apply using the buffer transfer
when requested.

TODO: This assumes the buffer has already been filled with values.  This
class could instead of taking the number of words, take the actual words and
fill the buffer itself.
'''

from percival_detector.carrier.registers import SensorDACMap
from percival_detector.carrier.errors import PercivalControlDeviceError

import logging


class Sensor(object):
    """
    Represent the Percival Sensor.
    """
    def __init__(self, buffer_cmd):
        """
        Constructor

        :param buffer_cmd: Percival buffer command object
        :type  buffer: SensorBufferCommand
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._buffer_cmd = buffer_cmd
        self._dacs_register_map = SensorDACMap()
        self._dacs_register_map.parse_map([0, 0, 0, 0, 0, 0, 0])
        self._buffer_words = {}

    def configuration_values_to_word(self, size, values):
        self._log.debug("Combining sensor values into 32 bit word")
        # Check how many values can be combined
        self._log.debug("Size of each value: %d", size)
        qty_values = 32 // size
        self._log.debug("Number of values that can fit into 32 bits: %d", qty_values)
        extra_shift = 32 % size
        self._log.debug("Extra shift required: %d", extra_shift)
        mask = 2**size - 1
        self._log.debug("Mask for values: %d", mask)
        if len(values) > qty_values:
            self._log.error("Too many sensor values to be stored in a 32 bit word")
            raise RuntimeError("Too many sensor values to be stored in a 32 bit word")
        # Extend the values if necessary
        if len(values) < qty_values:
            values = (values + [0] * qty_values)[:qty_values]

        value = 0
        for index in range(qty_values):
            value = (value << size) + (values[index] & mask)
        value <<= extra_shift
        return value

    def apply_dac_values(self, config):
        self._log.debug("Sensor DAC configuration: %s", config)
        for item in config:
            try:
                value = int(float(config[item]))
                self._log.debug("Setting sensor DAC %s = %d", item, value)
                if value < 0:
                    raise PercivalControlDeviceError("Value of {} cannot be negative".format(item))
                if value > 63:
                    raise PercivalControlDeviceError("Maximum value of {} is 63".format(item))
                if hasattr(self._dacs_register_map, item):
                    setattr(self._dacs_register_map, item, value)
                else:
                    self._log.debug("No register found for %s", item)
                    raise PercivalControlDeviceError("No register found for {}".format(item))
            except:
                self._log.error("Failed to set item %s", item)
                raise

        # Obtain the buffer words from the register map
        words = self._dacs_register_map.generate_map()
        self._log.debug("Applying sensor DAC values: %s", words)
        self._buffer_cmd.send_dacs_setup_cmd(words)

    def apply_configuration(self, config):
        if config:
            self._log.debug("Applying sensor configuration: %s", config)
            # We need to verify the configuration
            if 'H1' in config and 'H0' in config and 'G' in config:
                for item in config['H1']:
                    value = int(float(item))
                    if value < 0:
                        raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                    if value > 7:
                        raise PercivalControlDeviceError("Maximum sensor configuration value is 7")
                for item in config['H0']:
                    value = int(float(item))
                    if value < 0:
                        raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                    if value > 7:
                        raise PercivalControlDeviceError("Maximum sensor configuration value is 7")
                for item in config['G']:
                    value = int(float(item))
                    if value < 0:
                        raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                    if value > 7:
                        raise PercivalControlDeviceError("Maximum sensor configuration value is 7")
                h1_values = config['H1']
                words = []
                while len(h1_values) > 9:
                    words.append(self.configuration_values_to_word(3, h1_values[0:10]))
                    h1_values = h1_values[10:]
                h0_values = h1_values + config['H0']
                while len(h0_values) > 9:
                    words.append(self.configuration_values_to_word(3, h0_values[0:10]))
                    h0_values = h0_values[10:]
                g_values = h0_values + config['G']
                while len(g_values) > 9:
                    words.append(self.configuration_values_to_word(3, g_values[0:10]))
                    g_values = g_values[10:]
                if len(g_values) > 0:
                    words.append(self.configuration_values_to_word(3, g_values))
                self._log.debug("Sensor configuration words: %s", words)
                self._buffer_cmd.send_configuration_setup_cmd(words)

    def parse_debug_flag(self, flag):
        value = 0
        if isinstance(flag, str) or isinstance(flag, str):
            if 'false' in flag.lower():
                flag = 0
            elif 'true' in flag.lower():
                flag = 1
        value = int(flag) & 1
        return value

    def apply_debug(self, debug):
        """
        The documentation says nothing about this; info was gathered on the phone.
        It seems that you create a 6-bitmask with
         (CLKin, adcCPN, CPNI, sr7SC, SC, dmxSEL) which come from the ini file,
        and this is put into all of the 9x5 H0, H1, G slots in the debug block. 
        """
        self._log.debug("Applying sensor debug: %s", debug)
        debug_value = 0
        if 'debug_dmxSEL' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_dmxSEL'])
        if 'debug_SC' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_SC'])<<1
        if 'debug_sr7SC' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_sr7SC'])<<2
        if 'debug_CPNI' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_CPNI'])<<3
        if 'debug_adcCPN' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_adcCPN'])<<4
        if 'debug_CLKin' in debug:
            debug_value |= self.parse_debug_flag(debug['debug_CLKin'])<<5
        self._log.debug("Debug value to set: 0x%x", debug_value)
        words = []
        for index in range(0, 9):
            words.append(self.configuration_values_to_word(6, [debug_value,
                                                               debug_value,
                                                               debug_value,
                                                               debug_value,
                                                               debug_value]))
        self._log.debug("Sensor debug words: %s", words)
        self._buffer_cmd.send_debug_setup_cmd(words)

    def apply_roi(self):
        self._log.debug("Applying sensor ROI")
        self._buffer_cmd.send_roi_setup_cmd()

    def apply_calibration(self, calibration):
        #self._log.debug("Applying sensor calibration: %s", calibration)
        # We need to first verify the debug description
        # Expected format
        #
        # { H1 : { Cal1 : { Left : [],
        #                   Right: [] },
        #          Cal2 : { Left : [],
        #                   Right: [] },
        #          Cal3 : { Left : [],
        #                   Right: [] },
        #          Cal4 : { Left : [],
        #                   Right: [] },
        #        },
        #   H0 : { Cal1 : { Left : [],
        #                   Right: [] },
        #          Cal2 : { Left : [],
        #                   Right: [] },
        #          Cal3 : { Left : [],
        #                   Right: [] },
        #          Cal4 : { Left : [],
        #                   Right: [] },
        #        },
        #   G  : { Cal1 : { Left : [],
        #                   Right: [] },
        #          Cal2 : { Left : [],
        #                   Right: [] },
        #          Cal3 : { Left : [],
        #                   Right: [] },
        #          Cal4 : { Left : [],
        #                   Right: [] },
        #        }
        # }
        #
        data_words = []
        calibration_keys = ['H1', 'H0', 'G']
        calibration_set_names = ['Cal0', 'Cal1', 'Cal2', 'Cal3']
        if all(name in calibration_keys for name in calibration):
            for key in calibration_keys:
                calibration_set = calibration[key]
                if all(name in calibration_set_names for name in calibration_set):
                    calibration_set_1 = calibration_set['Cal0']
                    for item in calibration_set_1['Right']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")
                    for item in calibration_set_1['Left']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")

                    calibration_set_2 = calibration_set['Cal1']
                    for item in calibration_set_2['Right']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")
                    for item in calibration_set_2['Left']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")

                    calibration_set_3 = calibration_set['Cal2']
                    for item in calibration_set_3['Right']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")
                    for item in calibration_set_3['Left']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")

                    calibration_set_4 = calibration_set['Cal3']
                    for item in calibration_set_4['Right']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")
                    for item in calibration_set_4['Left']:
                        value = int(float(item))
                        if value < 0:
                            raise PercivalControlDeviceError("Sensor configuration value cannot be negative")
                        if value > 511:
                            raise PercivalControlDeviceError("Maximum sensor configuration value is 511")

                    col1_values = self.combine_9bit_lists_into_8bit_list(calibration_set_1['Right'],
                                                                         calibration_set_1['Left'])
                    col2_values = self.combine_9bit_lists_into_8bit_list(calibration_set_2['Right'],
                                                                         calibration_set_2['Left'])
                    col3_values = self.combine_9bit_lists_into_8bit_list(calibration_set_3['Right'],
                                                                         calibration_set_3['Left'])
                    col4_values = self.combine_9bit_lists_into_8bit_list(calibration_set_4['Right'],
                                                                         calibration_set_4['Left'])
                    data_words = data_words + self.combine_8bit_lists_into_32bit_list(col1_values,
                                                                                      col2_values,
                                                                                      col3_values,
                                                                                      col4_values)
                else:
                    self._log.error("Unable to find calibration targets %s in set %s", calibration_set_names, key)
                    raise RuntimeError("Unable to find calibration targets %s in set %s", calibration_set_names, key)
            self._log.debug("Sensor calibration words: %s", data_words)
            self._buffer_cmd.send_calibration_setup_cmd(data_words)
        else:
            self._log.error("Unable to find calibration sets %s within calibration object", calibration_keys)
            raise RuntimeError("Unable to find calibration sets %s within calibration object", calibration_keys)

    def combine_9bit_lists_into_8bit_list(self, list1, list2):
        self._log.debug("Combining 2 x 9 bit lists: %s and %s", list1, list2)
        # This method takes two lists of 9 bit values and creates a single list of 8 bit values
        # First interleave the two lists
        interleaved = [val for pair in zip(list1, list2) for val in pair]
        # Now loop over the new list and convert into 8 bit
        values = []
        bit = 0
        value = 0
        for val in interleaved:
            bits_left = 9
            while bits_left > 0:
                value <<= 1
                value += (val & (1<<(bits_left-1))) >> (bits_left-1)
                bit += 1
                if bit == 8:
                    # Filled up 8 bit value so add it
                    values.append(value)
                    value = 0
                    bit = 0
                bits_left -= 1
        return values

    def combine_8bit_lists_into_32bit_list(self, list1, list2, list3, list4):
        self._log.debug("Combining 4 x 8 bit lists: %s, %s, %s and %s", list1, list2, list3, list4)
        # Verify all lists are the same length
        if len(list1) != len(list2) or len(list2) != len(list3) or len(list3) != len(list4):
            self._log.error("Inconsistent list sizes, cannot combine")
            raise RuntimeError("Inconsistent list sizes, cannot combine")

        values = []
        for index in range(len(list1)):
            value = ((list1[index]&0xFF)<<24) + ((list2[index]&0xFF)<<16) + ((list3[index]&0xFF)<<8) + (list4[index]&0xFF)
            values.append(value)

        self._log.error("Calculated 32 bit values: %s", values)

        return values
