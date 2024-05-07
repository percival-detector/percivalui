"""
Definitions of the Carrier Board UART control registers

Update this whenever there are any firmware/documentation changes to register map definitions in the UART blocks.
"""



from future.utils import with_metaclass, raise_with_traceback
from builtins import range  # pylint: disable=W0622
import abc

from percival_detector.control.interface import IABCMeta
from . import encoding, const
from percival_detector.carrier import txrx
import logging

logger = logging.getLogger(__name__)


class RegisterMap(object):
    """Mixin to be used by classes that implement the `IRegisterMap` interface"""
    def __getattr__(self, name):
        if name in list(self._mem_map.keys()):
            return self._mem_map[name].value
        else:
            raise_with_traceback(AttributeError("No attribute: %s"%name))

    def __setattr__(self, name, value):
        #logger.debug(str(self._mem_map))
        if name not in list(self._mem_map.keys()):
            return object.__setattr__(self, name, value)
        else:
            self._mem_map[name].value = value

    def __getitem__(self, item):
        return self._mem_map[item]

    # words is a list of 32-bit words that are the words you want in the register, verbatim.
    # the words are split into the various fields by this functions.
    def parse_map(self, words):
        if len(words) != self.num_words:
            raise_with_traceback(IndexError("Map must contain %d words. Got only %d" % (self.num_words, len(words))))
        map_fields = [f for (k, f) in sorted(list(self._mem_map.items()),
                      key=lambda key_field: key_field[1].word_index, reverse=True)]
        for map_field in map_fields:
            map_field.set_field_value_from(words)

    def parse_map_from_tuples(self, tuples):
        words = [value for (addr, value) in tuples]
        self.parse_map(words)

    def generate_map(self):
        words = list(range(self.num_words))
        logger.debug("map: %s", str(self._mem_map))
        for (key, field) in list(self._mem_map.items()):  # pylint: disable=W0612
            logger.debug("field: %s", str(field))
            field.get_field_value_into(words)
            logger.debug("generate_map: words: %s", str(words))
        return words

    def as_dict(self):
        ret = {};
        for key in self._mem_map.keys():
          ret[key] = self._mem_map[key].value;
        return ret;

    @property
    def map_fields(self):
        return list(self._mem_map.keys())

    @property
    def mem_map(self):
        return self._mem_map

    def __str__(self):
        map_str = ""
        map_fields = [f for (k, f) in sorted(list(self._mem_map.items()),
                      key=lambda key_field: key_field[1].word_index, reverse=True)]
        for map_field in map_fields:
            map_str += str(map_field) + ", "
        s = "<%s: Fields = %s>"%(self.__class__.__name__, map_str)
        return s

    def __repr__(self):
        return self.__str__()


class MapField(object):
    """
    Store the information required to parse a value out of a specific field in a register map

     * Word index
     * Number of bits
     * Value bit offset within the word
    """
    def __init__(self, name, word_index, num_bits, bit_offset):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._word_index = word_index
        self._num_bits = num_bits
        self._name = name
        self._bit_offset = bit_offset
        self._value = None

    @property
    def num_bits(self):
        return self._num_bits

    @property
    def bit_offset(self):
        return self._bit_offset

    @property
    def name(self):
        return self._name

    @property
    def word_index(self):
        return self._word_index

    @property
    def mask(self):
        return (2**self._num_bits -1) << self._bit_offset

    @property
    def value(self):
        self._log.debug("getting value = %s", str(self._value))
        return self._value

    @value.setter
    def value(self, value):
        self._log.debug("setting value = %s (was = %s)", str(value), str(self._value))
        self._value = value

    def set_field_value_from(self, words):
        self._value = (words[self._word_index] & self.mask) >> self._bit_offset
        return self._value

    def get_field_value_into(self, words):
        # Clear the relevant bits in the input word
        # Then set self._value in the relevant part of the input word
        # nb words is a list passed by reference
        if self._value is None:
            raise_with_traceback(ValueError("No value initialised for field: \'%s\'"%self._name))
        words[self._word_index] = (words[self._word_index] & (self.mask ^ 2**32-1)) | (self._value << self._bit_offset)

    def __repr__(self):
        s = "<MapField: \"%s\" word:%i offset:%i bits:%i val:%s>"%(self._name,
                                                                 self._word_index,
                                                                 self._bit_offset,
                                                                 self._num_bits,
                                                                 str(self._value))
        return s

    def __str__(self):
        s = "<%s=%s>"%(self._name, str(self._value))
        return s

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class HeaderInfoMap(RegisterMap):
    """Represent the Header Info register bank"""
    num_words = 1

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"eeprom_address":               MapField("eeprom_address",              0, 8, 16),
                         "monitoring_channels_count":    MapField("monitoring_channels_count",   0, 8,  8),
                         "control_channels_count":       MapField("control_channels_count",      0, 8,  0),
                         }


class ControlChannelMap(RegisterMap):
    """Represent the map of Control Channels register bank"""
    num_words = 4

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"channel_id":                   MapField("channel_id",                  0,  5, 27),
                         "board_type":                   MapField("board_type",                  0,  3, 24),
                         "component_family_id":          MapField("component_family_id",         0,  4, 20),
                         "device_i2c_bus_select":        MapField("device_i2c_bus_select",       0,  2, 18),
                         "channel_device_id":            MapField("channel_device_id",           0,  5, 13),
                         "channel_sub_address":          MapField("channel_sub_address",         0,  5,  8),
                         "device_address":               MapField("device_address",              0,  8,  0),

                         "channel_range_max":            MapField("channel_range_max",           1, 16, 16),
                         "channel_range_min":            MapField("channel_range_min",           1, 16,  0),

                         "channel_default_on":           MapField("channel_default_on",          2, 16, 16),
                         "channel_default_off":          MapField("channel_default_off",         2, 16,  0),

                         # These are not yet in use
                         #"channel_monitoring":           MapField("channel_monitoring",          3,  8, 16),
                         #"safety_exception_threshold":   MapField("safety_exception_threshold",  3,  8,  8),
                         #"read_frequency":               MapField("read_frequency",              3,  8,  0),

                         "power_status":                 MapField("power_status",                3,  1, 16),
                         "value":                        MapField("value",                       3, 16,  0),
                         }


class MonitoringChannelMap(RegisterMap):
    """Represent the map of Monitoring Channel register bank"""
    num_words = 4

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
                                                                                     #    word, num-bits, lowest-bit
        self._mem_map = {"channel_id":                   MapField("channel_id",                  0,  5, 27),
                         "board_type":                   MapField("board_type",                  0,  3, 24),
                         "component_family_id":          MapField("component_family_id",         0,  4, 20),
                         "device_i2c_bus_select":        MapField("device_i2c_bus_select",       0,  2, 18),
                         "channel_device_id":            MapField("channel_device_id",           0,  5, 13),
                         "channel_sub_address":          MapField("channel_sub_address",         0,  5,  8),
                         "device_address":               MapField("device_address",              0,  8,  0),

                         "channel_ext_low_threshold":    MapField("channel_ext_low_threshold",   1, 16, 16),
                         "channel_ext_high_threshold":   MapField("channel_ext_high_threshold",  1, 16,  0),

                         "channel_low_threshold":        MapField("channel_low_threshold",       2, 16, 16),
                         "channel_high_threshold":       MapField("channel_high_threshold",      2, 16,  0),

                         "safety_action_7_select":       MapField("safety_action_7_select",      3,  1, 23),
                         "safety_action_6_select":       MapField("safety_action_6_select",      3,  1, 22),
                         "safety_action_5_select":       MapField("safety_action_5_select",      3,  1, 21),
                         "safety_action_4_select":       MapField("safety_action_4_select",      3,  1, 20),
                         "safety_action_3_select":       MapField("safety_action_3_select",      3,  1, 19),
                         "safety_action_2_select":       MapField("safety_action_2_select",      3,  1, 18),
                         "safety_action_1_select":       MapField("safety_action_1_select",      3,  1, 17),
                         "safety_action_0_select":       MapField("safety_action_0_select",      3,  1, 16),
                         "safety_exception_threshold":   MapField("safety_exception_threshold",  3,  8,  8),
                         "read_frequency":               MapField("read_frequency",              3,  8,  0),
                         }


class CommandMap(RegisterMap):
    """Represent the CommandMap register bank:

        * Word 0: Device command interface word
        * Word 1: Sensor command interface word
        * Word 2: System command interface word
    """
    num_words = 3

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"device_cmd":                   MapField("device_cmd",                   0,  3, 28),
                         "device_type":                  MapField("device_type",                  0,  2, 23),
                         #"eeprom_target":                MapField("eeprom_target",                0,  3, 25),
                         "device_index":                 MapField("device_index",                 0, 16,  0),

                         "buffer_cmd_destination":       MapField("buffer_cmd_destination",       1,  4, 28),
                         "buffer_cmd":                   MapField("buffer_cmd",                   1,  4, 24),
                         "buffer_cmd_words":             MapField("buffer_cmd_words",             1,  8, 16),
                         "buffer_cmd_address":           MapField("buffer_cmd_address",           1, 16,  0),

                         "system_cmd":                   MapField("system_cmd",                   2, 16, 16),
                         "system_cmd_data":              MapField("system_cmd_data",              2, 16,  0),
                         }


class EchoWordMap(RegisterMap):
    """Represent the ECHO WORD register bank of just one single word
    """
    num_words = 1

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"read_value":                   MapField("read_value",                   0,  16,  0),
                         "i2c_communication_error":      MapField("i2c_communication_error",      0,   1, 16),
                         "sample_number":                MapField("sample_number",                0,   8, 24),
                         }


class ReadValueMap(RegisterMap):
    """Represent the READ VALUE register bank of just one single word
    """
    num_words = 1

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"read_value":                   MapField("read_value",                   0,  16,  0),
                         "i2c_communication_error":      MapField("i2c_communication_error",      0,   1, 16),
                         "safety_exception_detected":    MapField("safety_exception_detected",    0,   1, 17),
                         "below_extreme_low_threshold":  MapField("below_extreme_low_threshold",  0,   1, 18),
                         "below_low_threshold":          MapField("below_low_threshold",          0,   1, 19),
                         "above_high_threshold":         MapField("above_high_threshold",         0,   1, 20),
                         "above_extreme_high_threshold": MapField("above_extreme_high_threshold", 0,   1, 21),
                         "sample_number":                MapField("sample_number",                0,   8, 24),
                         }

class SystemStatusMap(RegisterMap):
    """Represents the system settings block that is submitted through the buffer interface
    """
    num_words = 8

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"Image_counter":
                             MapField("Image_counter",                               0,   32,  0),
                         "Acquisition_counter":
                             MapField("Acquisition_counter",                         1,   32,  0),
                         "Train_number_MSB":
                             MapField("Train_number_LSB",                            2,   32,  0),
                         "Train_number_LSB":
                             MapField("Train_number_MSB",                            3,   32,  0),
                         "LVDS_IOs_enabled":
                             MapField("LVDS_IOs_enabled",                            4,   1,   0),
                         "Master_reset":
                             MapField("Master_reset",                                4,   1,   1),
                         "PLL_reset":
                             MapField("PLL_reset",                                   4,   1,   2),
                         "dmux_CDN":
                             MapField("dmux_CDN",                                    4,   1,   3),
                         "sr7DIn_0":
                             MapField("sr7DIn_0",                                    4,   1,   4),
                         "sr7DIn_1":
                             MapField("sr7DIn_1",                                    4,   1,   5),
                         "horiz_data_in_0":
                             MapField("horiz_data_in_0",                             4,   1,   6),
                         "horiz_data_in_1":
                             MapField("horiz_data_in_1",                             4,   1,   7),
                         "enable_testpoints":
                             MapField("enable_testpoints",                           4,   1,   8),
                         "startup_mode_enabled":
                             MapField("startup_mode_enabled",                        4,   1,   9),
                         "global_monitoring_enabled":
                             MapField("global_monitoring_enabled",                   4,   1,  10),
                         "device_level_safety_controls_enabled":
                             MapField("device_level_safety_controls_enabled",        4,   1,  11),
                         "system_level_safety_controls_enabled":
                             MapField("system_level_safety_controls_enabled",        4,   1,  12),
                         "experimental_level_safety_controls_enabled":
                             MapField("experimental_level_safety_controls_enabled",  4,   1,  13),
                         "safety_actions_enabled":
                             MapField("safety_actions_enabled",                      4,   1,  14),
                         "system_armed":
                             MapField("system_armed",                                4,   1,  15),
                         "acquiring":
                             MapField("acquiring",                                   4,   1,  16),
                         "wait_for_trigger":
                             MapField("wait_for_trigger",                            4,   1,  17),
                         "sensor_active_for_acquisition":
                             MapField("sensor_active_for_acquisition",               4,   1,  18),
                         "MEZZ_A_PHY_OK":
                             MapField("MEZZ_A_PHY_OK",                               4,   1,  19),
                         "MEZZ_A_MGT_OK":
                             MapField("MEZZ_A_MGT_OK",                               4,   1,  20),
                         "MEZZ_A_RESET":
                             MapField("MEZZ_A_RESET",                                4,   1,  21),
                         "MEZZ_B_PHY_OK":
                             MapField("MEZZ_B_PHY_OK",                               4,   1,  22),
                         "MEZZ_B_MGT_OK":
                             MapField("MEZZ_B_MGT_OK",                               4,   1,  23),
                         "MEZZ_B_RESET":
                             MapField("MEZZ_B_RESET",                                4,   1,  24),
                         "MARKER_OUT_0":
                             MapField("MARKER_OUT_0",                                4,   1,  25),
                         "MARKER_OUT_1":
                             MapField("MARKER_OUT_1",                                4,   1,  26),
                         "MARKER_OUT_2":
                             MapField("MARKER_OUT_2",                                4,   1,  27),
                         "MARKER_OUT_3":
                             MapField("MARKER_OUT_3",                                4,   1,  28),
                         "include_train_number_in_status_record":
                             MapField("include_train_number_in_status_record",       4,   1,  29),
                         "PLUGIN_RESET":
                             MapField("PLUGIN_RESET",                                4,   1,  30),
                         "DataSynchError":
                             MapField("DataSynchError",                              4,   1,  31),
                         "HIGH_FREQ_ADJ_CLOCK_0_clock_enable":
                             MapField("HIGH_FREQ_ADJ_CLOCK_0_clock_enable",          			5,   1,   0),
                         "HIGH_FREQ_ADJ_CLOCK_1_clock_enable":
                             MapField("HIGH_FREQ_ADJ_CLOCK_1_clock_enable",          			5,   1,   1),
                         "HIGH_FREQ_ADJ_CLOCK_2_clock_enable":
                             MapField("HIGH_FREQ_ADJ_CLOCK_2_clock_enable",          			5,   1,   2),
                         "HIGH_FREQ_ADJ_CLOCK_3_clock_enable":
                             MapField("HIGH_FREQ_ADJ_CLOCK_3_clock_enable",          			5,   1,   3),
                         "LOW_FREQ_ADJ_CLOCK_0_clock_enable":
                             MapField("LOW_FREQ_ADJ_CLOCK_0_clock_enable",           			5,   1,   4),
                         "LOW_FREQ_ADJ_CLOCK_1_clock_enable":
                             MapField("LOW_FREQ_ADJ_CLOCK_1_clock_enable",          			5,   1,   5),
                         "safety_driven_assert_marker_out_3_completed":
                             MapField("safety_driven_assert_marker_out_3_completed", 			5,   1,   6),
                         "safety_driven_assert_marker_out_2_completed":
                             MapField("safety_driven_assert_marker_out_2_completed", 			5,   1,   7),
                         "safety_driven_assert_marker_out_1_completed":
                             MapField("safety_driven_assert_marker_out_1_completed", 			5,   1,   8),
                         "safety_driven_assert_marker_out_0_completed":
                             MapField("safety_driven_assert_marker_out_0_completed", 			5,   1,   9),
                         "safety_driven_fast_enable_control_standby_completed":
                             MapField("safety_driven_fast_enable_control_standby_completed",    5,   1,  10),
                         "safety_driven_fast_sensor_powerdown_completed":
                             MapField("safety_driven_fast_sensor_powerdown_completed",          5,   1,  11),
                         "safety_driven_exit_acquisition_armed_status_completed":
                             MapField("safety_driven_exit_acquisition_armed_status_completed",  5,   1,  12),
                         "safety_driven_stop_acquisition_completed":
                             MapField("safety_driven_stop_acquisition_completed",         		5,   1,  13),
							 
                         }


class SystemSettingsMap(RegisterMap):
    """Represents the system settings block that is submitted through the buffer interface
    """
    num_words = 18

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"REGION_OF_INTEREST_ROI_mode":
                             MapField("REGION_OF_INTEREST_ROI_mode",                           0,   1,  31),
                         "REGION_OF_INTEREST_Illumination":
                             MapField("REGION_OF_INTEREST_Illumination",                       0,   1,  30),
                         "REGION_OF_INTEREST_Sensor_type":
                             MapField("REGION_OF_INTEREST_Sensor_type",                        0,   3,  27),
                         "REGION_OF_INTEREST_Vertical_ROI_start_row_group":
                             MapField("REGION_OF_INTEREST_Vertical_ROI_start_row_group",       0,   7,  13),
                         "REGION_OF_INTEREST_Vertical_ROI_start_block":
                             MapField("REGION_OF_INTEREST_Vertical_ROI_start_block",           0,   3,  10),
                         "REGION_OF_INTEREST_Vertical_ROI_stop_row_group":
                             MapField("REGION_OF_INTEREST_Vertical_ROI_stop_row_group",        0,   7,  3),
                         "REGION_OF_INTEREST_Vertical_ROI_stop_block":
                             MapField("REGION_OF_INTEREST_Vertical_ROI_stop_block",            0,   3,  0),
                         "REGION_OF_INTEREST_Horizontal_ROI_start_column":
                             MapField("REGION_OF_INTEREST_Horizontal_ROI_start_column",        1,   5,  13),
                         "REGION_OF_INTEREST_Horizontal_ROI_start_block":
                             MapField("REGION_OF_INTEREST_Horizontal_ROI_start_block",         1,   3,  10),
                         "REGION_OF_INTEREST_Horizontal_ROI_stop_column":
                             MapField("REGION_OF_INTEREST_Horizontal_ROI_stop_column",         1,   5,  3),
                         "REGION_OF_INTEREST_Horizontal_ROI_stop_block":
                             MapField("REGION_OF_INTEREST_Horizontal_ROI_stop_block",          1,   3,  0),
                         "ACQUISITION_Continuous_acquisition":
                             MapField("ACQUISITION_Continuous_acquisition",                    2,   1,  20),
                         "ACQUISITION_Acquisition_mode":
                             MapField("ACQUISITION_AcquisitionMode",                           2,   2,  18),
                         "ACQUISITION_Number_of_frames":
                             MapField("ACQUISITION_Number_of_frames",                          2,   18, 0),
                         "INTEGRATION_Integration_mode":
                             MapField("INTEGRATION_Integration_mode",                          3,   1,  16),
                         "INTEGRATION_Integration_window_width":
                             MapField("INTEGRATION_Integration_window_width",                  3,   16, 0),
                         "TRIGGERING_Trigger_acquisition_delay":
                             MapField("TRIGGERING_Trigger_acquisition_delay",                  4,   16, 16),
                         "TRIGGERING_Number_of_frames_per_trigger":
                             MapField("TRIGGERING_Number_of_frames_per_trigger",               4,   6, 10),
                         "TRIGGERING_Gate_polarity":
                             MapField("TRIGGERING_Gate_polarity",                              4,   1,  9),
                         "TRIGGERING_External_gate_signal":
                             MapField("TRIGGERING_External_gate_signal",                       4,   1,  8),
                         "TRIGGERING_Gating":
                             MapField("TRIGGERING_Gating",                                     4,   1,  7),
                         "TRIGGERING_Trigger_mode":
                             MapField("TRIGGERING_Trigger_mode",                               4,   1,  6),
                         "TRIGGERING_Trigger_edge_selection":
                             MapField("TRIGGERING_Trigger_edge_selection",                     4,   2,  4),
                         "TRIGGERING_External_trigger_signal":
                             MapField("TRIGGERING_External_trigger_signal",                    4,   3,  1),
                         "TRIGGERING_Trigger_source":
                             MapField("TRIGGERING_Trigger_source",                             4,   1,  0),
                         "TRIGGERING_Repetition_rate":
                             MapField("TRIGGERING_Repetition_rate",                            5,   32, 0),
                         "TRIGGERING_Burst_period":
                             MapField("TRIGGERING_Burst_period",				               6,   32, 0),
                         "ADVANCED_Custom_global_disable_duration":
                             MapField("ADVANCED_Custom_global_disable_duration",               7,   16, 9),
                         "ADVANCED_Custom_global_disable_before_each_new_frame":
                             MapField("ADVANCED_Custom_global_disable_before_each_new_frame",  7,   1,  8),
                         "SAMPLING_SR_phase_Resampling_mode":
                             MapField("SAMPLING_SR_phase_Resampling_mode",                     7,   1,  5),
                         "SAMPLING_S3_phase_Resampling_mode":
                             MapField("SAMPLING_S3_phase_Resampling_mode",                     7,   1,  4),
                         "SAMPLING_S2_phase_Resampling_mode":
                             MapField("SAMPLING_S2_phase_Resampling_mode",                     7,   1,  3),
                         "SAMPLING_S1_phase_Resampling_mode":
                             MapField("SAMPLING_S1_phase_Resampling_mode",                     7,   1,  2),
                         "SAMPLING_S0_phase_Resampling_mode":
                             MapField("SAMPLING_S0_phase_Resampling_mode",                     7,   1,  1),
                         "SAMPLING_Sampling_mode":
                             MapField("SAMPLING_Sampling_mode",                                7,   1,  0),
                         "SAMPLING_SR_phase_n_factor":
                             MapField("SAMPLING_SR_phase_n_factor",                            8,   6,  24),
                         "SAMPLING_S3_phase_n_factor":
                             MapField("SAMPLING_S3_phase_n_factor",                            8,   6,  18),
                         "SAMPLING_S2_phase_n_factor":
                             MapField("SAMPLING_S2_phase_n_factor",                            8,   6,  12),
                         "SAMPLING_S1_phase_n_factor":
                             MapField("SAMPLING_S1_phase_n_factor",                            8,   6,  6),
                         "SAMPLING_S0_phase_n_factor":
                             MapField("SAMPLING_S0_phase_n_factor",                            8,   6,  0),
                         "SAMPLING_SR_phase_number_of_repeats":
                             MapField("SAMPLING_SR_phase_number_of_repeats",                   9,   6, 24),
                         "SAMPLING_S3_phase_number_of_repeats":
                             MapField("SAMPLING_S3_phase_number_of_repeats",                   9,   6, 18),
                         "SAMPLING_S2_phase_number_of_repeats":
                             MapField("SAMPLING_S2_phase_number_of_repeats",                   9,   6, 12),
                         "SAMPLING_S1_phase_number_of_repeats":
                             MapField("SAMPLING_S1_phase_number_of_repeats",                   9,   6, 6),
                         "SAMPLING_S0_phase_number_of_repeats":
                             MapField("SAMPLING_S0_phase_number_of_repeats",                   9,   6, 0),
                         "ADVANCED_dmuxSEL_EXT_options":
                             MapField("ADVANCED_dmuxSEL_EXT_options",                          10,  2,  18),
                         "ADVANCED_SC_EXT_options":
                             MapField("ADVANCED_SC_EXT_options",                               10,  2,  16),
                         "ADVANCED_sr7SC_EXT_options":
                             MapField("ADVANCED_sr7SC_EXT_options",                            10,  2,  14),
                         "ADVANCED_CPNI_EXT_options":
                             MapField("ADVANCED_CPNI_EXT_options",                             10,  2,  12),
                         "ADVANCED_adcCPN_EXT_options":
                             MapField("ADVANCED_adcCPN_EXT_options",                           10,  2,  10),
                         "ADVANCED_PLLClk_EXT_options":
                             MapField("ADVANCED_PLLClk_EXT_options",                           10,  2,  8),
                         "ADVANCED_Enable_dmuxSEL_EXT":
                             MapField("ADVANCED_Enable_dmuxSEL_EXT",                           10,  1,  7),
                         "ADVANCED_Enable_SC_EXT":
                             MapField("ADVANCED_Enable_SC_EXT",                                10,  1,  6),
                         "ADVANCED_Enable_sr7SC_EXT":
                             MapField("ADVANCED_Enable_sr7sc_EXT",                             10,  1,  5),
                         "ADVANCED_Enable_CPNI_EXT":
                             MapField("ADVANCED_Enable_CPNI_EXT",                              10,  1,  4),
                         "ADVANCED_Enable_adcCPN_EXT":
                             MapField("ADVANCED_Enable_adcCPN_EXT",                            10,  1,  3),
                         "ADVANCED_Enable_PLLClk_EXT":
                             MapField("ADVANCED_Enable_PLLClk_EXT",                            10,  1,  2),
                         "ADVANCED_Calibration_options":
                             MapField("ADVANCED_Calibration_options",                          10,  2,  0),
                         "MONITORING_Monitoring_time_value_s":
                             MapField("MONITORING_Monitoring_time_value_s",                    11,  32, 0),
                         "MONITORING_I2C_idle_time_us":
                             MapField("MONITORING_I2C_idle_time_us",                           12,  16,  0),
                         "SAFETY_Priority_7_Action_select":
                             MapField("SAFETY_Priority_7_Action_select",                       13,  4,  28),
                         "SAFETY_Priority_6_Action_select":
                             MapField("SAFETY_Priority_6_Action_select",                       13,  4,  24),
                         "SAFETY_Priority_5_Action_select":
                             MapField("SAFETY_Priority_5_Action_select",                       13,  4,  20),
                         "SAFETY_Priority_4_Action_select":
                             MapField("SAFETY_Priority_4_Action_select",                       13,  4,  16),
                         "SAFETY_Priority_3_Action_select":
                             MapField("SAFETY_Priority_3_Action_select",                       13,  4,  12),
                         "SAFETY_Priority_2_Action_select":
                             MapField("SAFETY_Priority_2_Action_select",                       13,  4,  8),
                         "SAFETY_Priority_1_Action_select":
                             MapField("SAFETY_Priority_1_Action_select",                       13,  4,  4),
                         "SAFETY_Priority_0_Action_select":
                             MapField("SAFETY_Priority_0_Action_select",                       13,  4,  0),
                         "SAFETY_Priority_7_Action_global_enable":
                             MapField("SAFETY_Priority_7_Action_global_enable",                14,  1,  7),
                         "SAFETY_Priority_6_Action_global_enable":
                             MapField("SAFETY_Priority_6_Action_global_enable",                14,  1,  6),
                         "SAFETY_Priority_5_Action_global_enable":
                             MapField("SAFETY_Priority_5_Action_global_enable",                14,  1,  5),
                         "SAFETY_Priority_4_Action_global_enable":
                             MapField("SAFETY_Priority_4_Action_global_enable",                14,  1,  4),
                         "SAFETY_Priority_3_Action_global_enable":
                             MapField("SAFETY_Priority_3_Action_global_enable",                14,  1,  3),
                         "SAFETY_Priority_2_Action_global_enable":
                             MapField("SAFETY_Priority_2_Action_global_enable",                14,  1,  2),
                         "SAFETY_Priority_1_Action_global_enable":
                             MapField("SAFETY_Priority_1_Action_global_enable",                14,  1,  1),
                         "SAFETY_Priority_0_Action_global_enable":
                             MapField("SAFETY_Priority_0_Action_global_enable",                14,  1,  0),
                         "MARKER_BOARD_marker_in_3_ENABLE":
                             MapField("MARKER_BOARD_marker_in_3_ENABLE",                       15,  1,  31),
                         "MARKER_BOARD_marker_in_2_ENABLE":
                             MapField("MARKER_BOARD_marker_in_2_ENABLE",                       15,  1,  30),
                         "MARKER_BOARD_marker_in_1_ENABLE":
                             MapField("MARKER_BOARD_marker_in_1_ENABLE",                       15,  1,  29),
                         "MARKER_BOARD_marker_in_0_ENABLE":
                             MapField("MARKER_BOARD_marker_in_0_ENABLE",                       15,  1,  28),
                         "PLUGIN_BOARD_Post_trigger_train_number_capture_delay":
                             MapField("PLUGIN_BOARD_Post_trigger_train_number_capture_delay",  15,  25, 1),
                         "PLUGIN_BOARD_Include_train_number_in_status_record":
                             MapField("PLUGIN_BOARD_Include_train_number_in_status_record",    15,  1,  0),
                         "UNUSED_1":
                             MapField("UNUSED_1",                                              16,  32, 0),
                         "UNUSED_2":
                             MapField("UNUSED_2",                                              17,  32, 0)
                         }


class ChipReadoutSettingsMap(RegisterMap):
    """Represents the system settings block that is submitted through the buffer interface
    """
    num_words = 32

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"RST_VOLTAGE_Standby":              MapField("RST_VOLTAGE_Standby",               0,  2,  0),
                         "RST_VOLTAGE_Integration":          MapField("RST_VOLTAGE_Integration",           0,  2,  2),
                         "RST_VOLTAGE_S0":                   MapField("RST_VOLTAGE_S0",                    0,  2,  4),
                         "RST_VOLTAGE_S1":                   MapField("RST_VOLTAGE_S1",                    0,  2,  6),
                         "RST_VOLTAGE_S2":                   MapField("RST_VOLTAGE_S2",                    0,  2,  8),
                         "RST_VOLTAGE_S3":                   MapField("RST_VOLTAGE_S3",                    0,  2, 10),
                         "RST_VOLTAGE_Reset":                MapField("RST_VOLTAGE_Reset",                 0,  2, 12),
                         "RST_VOLTAGE_SR":                   MapField("RST_VOLTAGE_SR",                    0,  2, 14),
                         "SEL_VOLTAGE_Standby":              MapField("SEL_VOLTAGE_Standby",               1,  2,  0),
                         "SEL_VOLTAGE_Integration":          MapField("SEL_VOLTAGE_Integration",           1,  2,  2),
                         "SEL_VOLTAGE_S0":                   MapField("SEL_VOLTAGE_S0",                    1,  2,  4),
                         "SEL_VOLTAGE_S1":                   MapField("SEL_VOLTAGE_S1",                    1,  2,  6),
                         "SEL_VOLTAGE_S2":                   MapField("SEL_VOLTAGE_S2",                    1,  2,  8),
                         "SEL_VOLTAGE_S3":                   MapField("SEL_VOLTAGE_S3",                    1,  2, 10),
                         "SEL_VOLTAGE_Reset":                MapField("SEL_VOLTAGE_Reset",                 1,  2, 12),
                         "SEL_VOLTAGE_SR":                   MapField("SEL_VOLTAGE_SR",                    1,  2, 14),
                         "SW0_VOLTAGE_Standby":              MapField("SW0_VOLTAGE_Standby",               2,  2,  0),
                         "SW0_VOLTAGE_Integration":          MapField("SW0_VOLTAGE_Integration",           2,  2,  2),
                         "SW0_VOLTAGE_S0":                   MapField("SW0_VOLTAGE_S0",                    2,  2,  4),
                         "SW0_VOLTAGE_S1":                   MapField("SW0_VOLTAGE_S1",                    2,  2,  6),
                         "SW0_VOLTAGE_S2":                   MapField("SW0_VOLTAGE_S2",                    2,  2,  8),
                         "SW0_VOLTAGE_S3":                   MapField("SW0_VOLTAGE_S3",                    2,  2, 10),
                         "SW0_VOLTAGE_Reset":                MapField("SW0_VOLTAGE_Reset",                 2,  2, 12),
                         "SW0_VOLTAGE_SR":                   MapField("SW0_VOLTAGE_SR",                    2,  2, 14),
                         "SW1_VOLTAGE_Standby":              MapField("SW1_VOLTAGE_Standby",               3,  2,  0),
                         "SW1_VOLTAGE_Integration":          MapField("SW1_VOLTAGE_Integration",           3,  2,  2),
                         "SW1_VOLTAGE_S0":                   MapField("SW1_VOLTAGE_S0",                    3,  2,  4),
                         "SW1_VOLTAGE_S1":                   MapField("SW1_VOLTAGE_S1",                    3,  2,  6),
                         "SW1_VOLTAGE_S2":                   MapField("SW1_VOLTAGE_S2",                    3,  2,  8),
                         "SW1_VOLTAGE_S3":                   MapField("SW1_VOLTAGE_S3",                    3,  2, 10),
                         "SW1_VOLTAGE_Reset":                MapField("SW1_VOLTAGE_Reset",                 3,  2, 12),
                         "SW1_VOLTAGE_SR":                   MapField("SW1_VOLTAGE_SR",                    3,  2, 14),
                         "SW2_VOLTAGE_Standby":              MapField("SW2_VOLTAGE_Standby",               4,  2,  0),
                         "SW2_VOLTAGE_Integration":          MapField("SW2_VOLTAGE_Integration",           4,  2,  2),
                         "SW2_VOLTAGE_S0":                   MapField("SW2_VOLTAGE_S0",                    4,  2,  4),
                         "SW2_VOLTAGE_S1":                   MapField("SW2_VOLTAGE_S1",                    4,  2,  6),
                         "SW2_VOLTAGE_S2":                   MapField("SW2_VOLTAGE_S2",                    4,  2,  8),
                         "SW2_VOLTAGE_S3":                   MapField("SW2_VOLTAGE_S3",                    4,  2, 10),
                         "SW2_VOLTAGE_Reset":                MapField("SW2_VOLTAGE_Reset",                 4,  2, 12),
                         "SW2_VOLTAGE_SR":                   MapField("SW2_VOLTAGE_SR",                    4,  2, 14),
                         "AB_VOLTAGE_Standby":               MapField("AB_VOLTAGE_Standby",                5,  2,  0),
                         "AB_VOLTAGE_Integration":           MapField("AB_VOLTAGE_Integration",            5,  2,  2),
                         "AB_VOLTAGE_S0":                    MapField("AB_VOLTAGE_S0",                     5,  2,  4),
                         "AB_VOLTAGE_S1":                    MapField("AB_VOLTAGE_S1",                     5,  2,  6),
                         "AB_VOLTAGE_S2":                    MapField("AB_VOLTAGE_S2",                     5,  2,  8),
                         "AB_VOLTAGE_S3":                    MapField("AB_VOLTAGE_S3",                     5,  2, 10),
                         "AB_VOLTAGE_Reset":                 MapField("AB_VOLTAGE_Reset",                  5,  2, 12),
                         "AB_VOLTAGE_SR":                    MapField("AB_VOLTAGE_SR",                     5,  2, 14),
                         "PGA_GAIN_Standby":                 MapField("PGA_VOLTAGE_Standby",               6,  2,  0),
                         "PGA_GAIN_Integration":             MapField("PGA_VOLTAGE_Integration",           6,  2,  2),
                         "PGA_GAIN_S0":                      MapField("PGA_GAIN_S0",                       6,  2,  4),
                         "PGA_GAIN_S1":                      MapField("PGA_GAIN_S1",                       6,  2,  6),
                         "PGA_GAIN_S2":                      MapField("PGA_GAIN_S2",                       6,  2,  8),
                         "PGA_GAIN_S3":                      MapField("PGA_GAIN_S3",                       6,  2, 10),
                         "PGA_GAIN_Reset":                   MapField("PGA_GAIN_Reset",                    6,  2, 12),
                         "PGA_GAIN_SR":                      MapField("PGA_GAIN_SR",                       6,  2, 14),
                         "DURATION_Sampling_prep_phase":     MapField("DURATION_Sampling_prep_phase",      7, 16,  0),
                         "DURATION_Sampling_phase":          MapField("DURATION_Sampling_phase",           7, 16, 16),
                         "DURATION_ADC_prep_phase":          MapField("DURATION_ADC_prep_phase",           8, 16,  0),
                         "DURATION_Reset_phase":             MapField("DURATION_Reset_phase",              8, 16, 16),
                         "SAMPLING_PREP_step1":              MapField("SAMPLING_PREP_step1",               9,  8,  0),
                         "SAMPLING_PREP_step2":              MapField("SAMPLING_PREP_step2",               9,  8,  8),
                         "SAMPLING_PREP_step3":              MapField("SAMPLING_PREP_step3",               9,  8, 16),
                         "SAMPLING_PHASE_S":                 MapField("SAMPLING_PHASE_S",                 10, 16,  0),
                         "SAMPLING_PHASE_PGA_GAIN":          MapField("SAMPLING_PHASE_PGA_GAIN",          10, 16, 16),
                         "SAMPLING_PHASE_SRAMreset_rise":    MapField("SAMPLING_PHASE_SRAMreset_rise",    11, 16,  0),
                         "SAMPLING_PHASE_PrstCol_fall":      MapField("SAMPLING_PHASE_PrstCol_fall",      11, 16, 16),
                         "SAMPLING_PHASE_SampleRS_fall":     MapField("SAMPLING_PHASE_SampleRS_fall",     12, 16,  0),
                         "SAMPLING_PHASE_Mem_fall":          MapField("SAMPLING_PHASE_Mem_fall",          12, 16, 16),
                         "SAMPLING_PHASE_Write_rise":        MapField("SAMPLING_PHASE_Write_rise",        13, 16,  0),
                         "SAMPLING_PHASE_Write_fall":        MapField("SAMPLING_PHASE_Write_fall",        13, 16, 16),
                         "SAMPLING_PHASE_Mem_rise":          MapField("SAMPLING_PHASE_Mem_rise",          14, 16,  0),
                         "ADC_PREP_PHASE_Drst_fall":         MapField("ADC_PREP_PHASE_Drst_fall",         15, 16,  0),
                         "ADC_PREP_PHASE_Drst_rise":         MapField("ADC_PREP_PHASE_Drst_rise",         15, 16, 16),
                         "ADC_PREP_PHASE_ResetADC_fall":     MapField("ADC_PREP_PHASE_ResetADC_fall",     16, 16,  0),
                         "ADC_PREP_PHASE_ResetADC_rise":     MapField("ADC_PREP_PHASE_ResetADC_rise",     16, 16, 16),
                         "ADC_PREP_PHASE_PreSRst_rise":      MapField("ADC_PREP_PHASE_PreSRst_rise",      17, 16,  0),
                         "ADC_PREP_PHASE_PreSRst_fall":      MapField("ADC_PREP_PHASE_PreSRst_fall",      17, 16, 16),
                         "ADC_PREP_PHASE_SampleADC_rise":    MapField("ADC_PREP_PHASE_SampleADC_rise",    18, 16,  0),
                         "ADC_PREP_PHASE_SampleADC_fall":    MapField("ADC_PREP_PHASE_SampleADC_fall",    18, 16, 16),
                         "RESET_PHASE_RST_reset_start":      MapField("RESET_PHASE_RST_reset_start",      19, 16,  0),
                         "RESET_PHASE_RST_reset_stop":       MapField("RESET_PHASE_RST_reset_stop",       19, 16, 16),
                         "RESET_PHASE_SW_reset_start":       MapField("RESET_PHASE_SW_reset_start",       20, 16,  0),
                         "RESET_PHASE_SW_reset_stop":        MapField("RESET_PHASE_SW_reset_stop",        20, 16, 16),
                         "RESET_PHASE_AB_reset_start":       MapField("RESET_PHASE_AB_reset_start",       21, 16,  0),
                         "RESET_PHASE_AB_reset_stop":        MapField("RESET_PHASE_AB_reset_stop",        21, 16, 16),
                         "DURATION_ADC_ramps_phase":         MapField("DURATION_ADC_ramps_phase",         22, 16,  0),
						 "ADC_RAMPS_PHASE_Fskip_duration_time":   MapField("ADC_RAMPS_PHASE_Fskip_duration_time",   22, 16, 16),
                         "ADC_RAMPS_PHASE_CConvEn_rise":     MapField("ADC_RAMPS_PHASE_CConvEn_rise",     23, 16,  0),
                         "ADC_RAMPS_PHASE_CConvEn_fall":     MapField("ADC_RAMPS_PHASE_CConvEn_fall",     23, 16, 16),
                         "ADC_RAMPS_PHASE_FConvEn_rise":     MapField("ADC_RAMPS_PHASE_FConvEn_rise",     24, 16,  0),
                         "ADC_RAMPS_PHASE_FConvEn_fall":     MapField("ADC_RAMPS_PHASE_FConvEn_fall",     24, 16, 16),
                         "STREAMOUT_PHASE_sr7CDNin_rise":    MapField("STREAMOUT_PHASE_sr7CDNin_rise",    25, 16,  0),
                         "STREAMOUT_PHASE_LoadDO_rise":      MapField("STREAMOUT_PHASE_LoadDO_rise",      25, 16, 16),
                         "STREAMOUT_PHASE_LoadDO_fall":      MapField("STREAMOUT_PHASE_LoadDO_fall",      26, 16,  0),
                         "MISC_Force_DebugSel":              MapField("MISC_Force_DebugSel",              27,  1,  0),
                         "MISC_PrstCol_options":             MapField("MISC_PrstCol_options",             27,  2,  1),
                         "UNUSED_1":                         MapField("UNUSED_1",                         28, 32,  0),
                         "UNUSED_2":                         MapField("UNUSED_2",                         29, 32,  0),
                         "UNUSED_3":                         MapField("UNUSED_3",                         30, 32,  0),
                         "UNUSED_4":                         MapField("UNUSED_4",                         31, 32,  0)
                         }


class ClockSettingsMap(RegisterMap):
    """Represent high and low frequency clock registers
    """
    num_words = 8

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"UNUSED_1":                         MapField("UNUSED_1",                          6, 32,  0),
                         "UNUSED_2":                         MapField("UNUSED_2",                          7, 32,  0)
                         }
        for number in [0, 1, 2, 3]:
            prefix = "HIGH_FREQ_ADJ_CLOCK<{}>".format(number)
            word_idx = number
            self._mem_map[prefix + "_enable_clock"] = MapField(prefix + "_enable_clock",       word_idx,  1, 24)
            self._mem_map[prefix + "_clkout_divider"] = MapField(prefix + "_clkout_divider",   word_idx,  8, 16)
            self._mem_map[prefix + "_base_multiplier"] = MapField(prefix + "_base_multiplier", word_idx,  8,  8)
            self._mem_map[prefix + "_base_divider"] = MapField(prefix + "_base_divider",       word_idx,  8,  0)
        for number in [0, 1]:
            prefix = "LOW_FREQ_ADJ_CLOCK<{}>".format(number)
            word_idx = number + 4
            self._mem_map[prefix + "_enable_clock"] = MapField(prefix + "_enable_clock",       word_idx,  1, 24)
            self._mem_map[prefix + "_cycles_value"] = MapField(prefix + "_cycles_value",       word_idx, 16,  0)


class SensorDACMap(RegisterMap):
    """Represent buffer command sensor DAC values
    """
    num_words = 7

    def __init__(self):
        object.__setattr__(self, '_mem_map', {})  # This prevents infinite recursion when setting attributes
        self._mem_map = {"vRefPGA_H1":              MapField("vRefPGA_H1",              0,  6, 26),
                         "vCasc_H1":                MapField("vCasc_H1",                0,  6, 20),
                         "vRefADC_H1":              MapField("vRefADC_H1",              0,  6, 14),
                         "vRefDB_H1":               MapField("vRefDB_H1",               0,  6,  8),
                         "iBiasPLL_H1":             MapField("iBiasPLL_H1",             0,  6,  2),
                         "unused_1":                MapField("unused_1",                0,  2,  0),
                         "iBiasTail_H1":            MapField("iBiasTail_H1",            1,  6, 26),
                         "iBiasCalibF_H1":          MapField("iBiasCalibF_H1",          1,  6, 20),
                         "iBiasCalibC_H1":          MapField("iBiasCalibC_H1",          1,  6, 14),
                         "iBiasSF_H1":              MapField("iBiasSF_H1",              1,  6,  8),
                         "iBiasCOMP_H1":            MapField("iBiasCOMP_H1",            1,  6,  2),
                         "unused_2":                MapField("unused_2",                1,  2,  0),
                         "ADCBias2_H1":             MapField("ADCBias2_H1",             2,  6, 26),
                         "ADCBias1_H1":             MapField("ADCBias1_H1",             2,  6, 20),
                         "iFBiasN_H1":              MapField("iFBiasN_H1",              2,  6, 14),
                         "iCBiasP_H1":              MapField("iCBiasP_H1",              2,  6,  8),
                         "Master_DAC_Current_H1":   MapField("Master_DAC_Current_H1",   2,  6,  2),
                         "unused_3":                MapField("unused_3",                2,  2,  0),
                         "vRefPGA_H0":              MapField("vRefPGA_H0",              3,  6, 26),
                         "vCasc_H0":                MapField("vCasc_H0",                3,  6, 20),
                         "vRefADC_H0":              MapField("vRefADC_H0",              3,  6, 14),
                         "vRefDB_H0":               MapField("vRefDB_H0",               3,  6,  8),
                         "iBiasPLL_H0":             MapField("iBiasPLL_H0",             3,  6,  2),
                         "unused_4":                MapField("unused_4",                3,  2,  0),
                         "iBiasTail_H0":            MapField("iBiasTail_H0",            4,  6, 26),
                         "iBiasCalibF_H0":          MapField("iBiasCalibF_H0",          4,  6, 20),
                         "iBiasCalibC_H0":          MapField("iBiasCalibC_H0",          4,  6, 14),
                         "iBiasSF_H0":              MapField("iBiasSF_H0",              4,  6,  8),
                         "iBiasCOMP_H0":            MapField("iBiasCOMP_H0",            4,  6,  2),
                         "unused_5":                MapField("unused_5",                4,  2,  0),
                         "ADCBias2_H0":             MapField("ADCBias2_H0",             5,  6, 26),
                         "ADCBias1_H0":             MapField("ADCBias1_H0",             5,  6, 20),
                         "iFBiasN_H0":              MapField("iFBiasN_H0",              5,  6, 14),
                         "iCBiasP_H0":              MapField("iCBiasP_H0",              5,  6,  8),
                         "Master_DAC_Current_H0":   MapField("Master_DAC_Current_H0",   5,  6,  2),
                         "unused_6":                MapField("unused_6",                5,  2,  0),
                         "iBiasColTop_A":           MapField("iBiasColTop_A",           6,  6, 26),
                         "unused_7":                MapField("unused_7",                6, 26,  0)
                         }


class IRegisterMap(with_metaclass(abc.ABCMeta, IABCMeta)):
    """
    Interface to a Device Setting bitmap.
    """
    __iproperties__ = ['num_words']
    __imethods__ = ['parse_map', 'parse_map_from_tuples', 'generate_map']
    _iface_requirements = __imethods__ + __iproperties__

    @abc.abstractproperty
    def num_words(self):
        """Number of 32bit words in the bitmap"""
        raise NotImplementedError

    @abc.abstractproperty
    def _mem_map(self):
        """Internal (private) logical representation of the bitmap

            Must be a dictionary of :class:`MapField` objects
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_map(self, words):
        """Parse a list of words as a bitmap and write to the relevant internal MapFields

            :param words: 32 bit integer words
            :type  words: list"""
        raise NotImplementedError

    @abc.abstractmethod
    def parse_map_from_tuples(self, tuples):
        """Parse a list of words as a bitmap and write to the relevant internal MapFields

            :param tuples: List of tuples with (address, value) where address is 16bit and value is 32 bit integer words
            :type  tuples: list"""
        raise NotImplementedError

    @abc.abstractmethod
    def generate_map(self):
        """Generate a bitmap from the device MapFields.

            :returns: a list of 32bit words"""
        raise NotImplementedError


IRegisterMap.register(HeaderInfoMap)
IRegisterMap.register(ControlChannelMap)
IRegisterMap.register(MonitoringChannelMap)

RegisterMapClasses = {
    const.RegisterMapType.header:       HeaderInfoMap,
    const.RegisterMapType.control:      ControlChannelMap,
    const.RegisterMapType.monitoring:   MonitoringChannelMap,
    const.RegisterMapType.command:      CommandMap,
    const.RegisterMapType.system:       SystemSettingsMap,
    const.RegisterMapType.chip_readout: ChipReadoutSettingsMap,
    const.RegisterMapType.clock:        ClockSettingsMap
}

BoardRegisters = {
    #                          header,                        control,                        monitoring
    const.BoardTypes.left:    (const.HEADER_SETTINGS_LEFT,    const.CONTROL_CHANNELS_LEFT,    const.MONITORING_CHANNELS_LEFT),
    const.BoardTypes.bottom:  (const.HEADER_SETTINGS_BOTTOM,  const.CONTROL_CHANNELS_BOTTOM,  const.MONITORING_CHANNELS_BOTTOM),
    const.BoardTypes.carrier: (const.HEADER_SETTINGS_CARRIER, const.CONTROL_CHANNELS_CARRIER, const.MONITORING_CHANNELS_CARRIER),
    const.BoardTypes.plugin:  (const.HEADER_SETTINGS_PLUGIN,  const.CONTROL_CHANNELS_PLUGIN,  const.MONITORING_CHANNELS_PLUGIN),
}

BoardValueRegisters = {
    const.BoardTypes.left: const.READ_VALUES_PERIPHERY_LEFT,
    const.BoardTypes.bottom: const.READ_VALUES_PERIPHERY_BOTTOM,
    const.BoardTypes.carrier: const.READ_VALUES_CARRIER,
    const.BoardTypes.plugin: const.READ_VALUES_PLUGIN
}

# Each entry is a tuple of:     (description, readback_block=(read_addr, entries, words-per-entry), RegisterMap subclass)
CarrierUARTRegisters = {
    const.HEADER_SETTINGS_LEFT:         ("Header settings left",        const.READBACK_HEADER_SETTINGS_LEFT,         HeaderInfoMap),
    const.CONTROL_CHANNELS_LEFT:        ("Control settings left",       const.READBACK_CONTROL_CHANNELS_LEFT,        ControlChannelMap),
    const.MONITORING_CHANNELS_LEFT:     ("Monitoring settings left",    const.READBACK_MONITORING_CHANNELS_LEFT,     MonitoringChannelMap),
    const.READ_VALUES_PERIPHERY_LEFT:   ("Read monitor values left",    const.READBACK_READ_VALUES_PERIPHERY_LEFT,   ReadValueMap),
    const.HEADER_SETTINGS_BOTTOM:       ("Header settings bottom",      const.READBACK_HEADER_SETTINGS_BOTTOM,       HeaderInfoMap),
    const.CONTROL_CHANNELS_BOTTOM:      ("Control settings bottom",     const.READBACK_CONTROL_CHANNELS_BOTTOM,      ControlChannelMap),
    const.MONITORING_CHANNELS_BOTTOM:   ("Monitoring settings bottom",  const.READBACK_MONITORING_CHANNELS_BOTTOM,   MonitoringChannelMap),
    const.READ_VALUES_PERIPHERY_BOTTOM: ("Read monitor values bottom",  const.READBACK_READ_VALUES_PERIPHERY_BOTTOM, ReadValueMap),
    const.HEADER_SETTINGS_CARRIER:      ("Header settings carrier",     const.READBACK_HEADER_SETTINGS_CARRIER,      HeaderInfoMap),
    const.CONTROL_CHANNELS_CARRIER:     ("Control settings carrier",    const.READBACK_CONTROL_CHANNELS_CARRIER,     ControlChannelMap),
    const.MONITORING_CHANNELS_CARRIER:  ("Monitoring settings carrier", const.READBACK_MONITORING_CHANNELS_CARRIER,  MonitoringChannelMap),
    const.READ_VALUES_CARRIER:          ("Read monitor values carrier", const.READBACK_READ_VALUES_CARRIER,          ReadValueMap),
    const.HEADER_SETTINGS_PLUGIN:       ("Header settings plugin",      const.READBACK_HEADER_SETTINGS_PLUGIN,       HeaderInfoMap),
    const.CONTROL_CHANNELS_PLUGIN:      ("Control settings plugin",     const.READBACK_CONTROL_CHANNELS_PLUGIN,      ControlChannelMap),
    const.MONITORING_CHANNELS_PLUGIN:   ("Monitoring settings plugin",  const.READBACK_MONITORING_CHANNELS_PLUGIN,   MonitoringChannelMap),
    const.READ_VALUES_PLUGIN:           ("Read monitor values plugin",  const.READBACK_READ_VALUES_PLUGIN,           ReadValueMap),
    const.SYSTEM_SETTINGS:              ("System settings",             const.READBACK_SYSTEM_SETTINGS,              SystemSettingsMap),
    const.CHIP_READOUT_SETTINGS:        ("Chip readout settings",       const.READBACK_CHIP_READOUT_SETTINGS,        ChipReadoutSettingsMap),
    const.CLOCK_SETTINGS:               ("Clock settings",              const.READBACK_CLOCK_SETTINGS,               ClockSettingsMap),
    const.COMMAND:                      ("CommandMap",                  None,                                        CommandMap),
    const.READ_ECHO_WORD:               ("Read Echo Word",              const.READBACK_READ_ECHO_WORD,               EchoWordMap),
    const.READ_VALUES_STATUS:           ("Read system status",          const.READBACK_READ_VALUES_STATUS,           SystemStatusMap),
}
"""Look-up table of UART addresses and the corresponding details

        The key is the UART write address :obj:`percival_detector.carrier.const.UARTBlock` and each item is a tuple of:

        * description
        * UART read_addr :obj:`percival_detector.carrier.const.UARTBlock`
        * Corresponding implementation of the :class:`percival_detector.carrier.devices.IRegisterMap` interface
"""


class UARTRegister(object):
    """ Represent a specific UART register on the Percival Carrier Board
    """
    UART_ADDR_WIDTH = 16
    UART_WORD_WIDTH = 32

    def __init__(self, uart_block, uart_device=None):
        """Constructor

            :param uart_block: UART start address for a block of registers.
                This is used as a look-up key to the functionality of that register in the CarrierUARTRegisters dictionary
            :type  uart_block: :obj:`percival_detector.carrier.const.UARTBlock`
            :param uart_device: UART start address for a specific device within the register block. If defined
                this will be used to generate write commands in get_write_cmd_msg().
            :type uart_device: int
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        (self._name, self._readback_addr, DeviceClass) = CarrierUARTRegisters[uart_block]
        self._uart_block = uart_block
        self._uart_address = uart_block.start_address
        self._log.debug("UARTRegister _uart_address: %02X", self._uart_address)

        self.fields = None  # A devices.RegisterMap object
        if DeviceClass:
            self.fields = DeviceClass()

        if uart_device:
            self._uart_address = uart_device
            self._log.debug("UARTRegister updated _uart_address: %02X", self._uart_address)
            if uart_device.bit_length() > self.UART_ADDR_WIDTH:
                raise_with_traceback(ValueError("UART device address value 0x%X is greater than 16 bits" %
                                                uart_device))

        if uart_block.start_address.bit_length() > self.UART_ADDR_WIDTH:
            raise_with_traceback(ValueError("UART block address value 0x%X is greater than 16 bits" %
                                            uart_block.start_address))
        if self._readback_addr:
            if self._readback_addr.start_address.bit_length() > self.UART_ADDR_WIDTH:
                raise_with_traceback(ValueError("readback_addr value 0x%X is greater than 16 bits" %
                                                self._readback_addr.start_address))

    @property
    def words_per_item(self):
        return self._uart_block.words_per_entry

    @property
    def num_items(self):
        return self._uart_block.entries

    def initialize_map(self, register_map):
        if len(register_map) >= 1:
            if type(register_map[0]) == int:
                self.fields.parse_map(register_map)
            elif type(register_map[0]) == tuple:
                self.fields.parse_map_from_tuples(register_map)
            else:
                raise_with_traceback(TypeError("register_map must be list/tuple of type int or tuple"))
        else:
            raise_with_traceback("Cannot initialize register map with an empty container")
       
    def get_read_cmd_msg(self):
        """Generate a message to do a readback (shortcut) command of the current register map
        
            :returns: A read UART command message
            :rtype:  list of :class:`percival_detector.carrier.txrx.TxMessage` objects
        """
        if not self._readback_addr:
            raise_with_traceback( TypeError("A readback shortcut is not available for \'%s\'"%self._name) )
        read_cmd_msg = encoding.encode_message(self._readback_addr.start_address, 0x00000000)
        self._log.debug(read_cmd_msg)
        return txrx.TxMessage(read_cmd_msg, self.words_per_item * self.num_items)
    
    def get_write_cmd_msg(self, eom=False):
        """Flatten the 2D matrix of datawords into one continuous list
        
            :returns: A write UART command message
            :rtype:  list of :class:`percival_detector.carrier.txrx.TxMessage` objects"""
        data_words = self.fields.generate_map()
        write_cmd_msg = encoding.encode_multi_message(self._uart_address, data_words)
        write_cmd_msg = [txrx.TxMessage(msg, num_response_msg=1, expect_eom=eom) for msg in write_cmd_msg]

        return write_cmd_msg


def get_register_block(addr):
    """Scan through the top-level register blocks to find the block addr belongs in.

    :param addr: UART address
    :type addr: int
    :return: Return the address block if found or None if addr is out of range
    :rtype: :obj:`percival_detector.carrier.const.UARTBlock`
    """
    register_blocks = list(CarrierUARTRegisters.keys())
    for register_block in register_blocks:
        if register_block.start_address <= \
           addr < \
           (register_block.start_address + (register_block.entries * register_block.words_per_entry)):
            return register_block


def generate_register_maps(registers):
    """Provides the connection between raw register maps: list of (addr, data) tuples and
    :class:`percival_detector.carrier.registers.RegisterMap` implementations.

    :param registers: List of (addr, data) register tuples, consecutive by address, 
            describing whole registerblocks where they exist - As returned by READ_CONTROL_SOMETHING.
    :type registers: list
    :returns: A list of :class:`RegisterMap` objects
    :rtype: list
    """
    index = 0
    register_maps = []
    while index < len(registers):
        addr, data = registers[index]  # pylint: disable=W0612
        uart_block = get_register_block(addr)
        if not uart_block:
            logger.warning("Did not find UART block for address: 0x%X", addr)
            index += 1
            continue
        if ((addr - uart_block.start_address) % uart_block.words_per_entry) != 0:
            logger.warning("UART address %s doesn't align with element boundary within the block %s.", addr, uart_block)
            index += 1
            continue
        (name, readback_addr_block, RegisterMapClass) = CarrierUARTRegisters[uart_block]  # pylint: disable=W0612
        block_map = RegisterMapClass()
        block_words = registers[index:(index + block_map.num_words)]
        try:
            block_map.parse_map_from_tuples(block_words)
        except IndexError as e:
            logger.warning("Register map length issue: %s", str(e))
            index += 1
            continue

        register_maps.append(block_map)
        index += block_map.num_words
    return register_maps

