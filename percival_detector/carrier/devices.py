"""
Created on 8 May 2015

@author: Ulrik Pedersen
"""

from percival_detector.carrier.const import DeviceFamily, DeviceCmd, DeviceFunction

import logging
logger = logging.getLogger(__name__)


class DeviceFeatures(object):
    """Mapping PCB devices to their supported functionality
    
    This represent the documented table "Supported DEVICE_CMD vs device family"
    """
    def __init__(self, device_family_id, function, description="", commands=None):
        """
            :param device_family_id: The component family ID
            :type  device_family_id: :obj:`percival_detector.carrier.const.DeviceFamily`
            :param function:         The enumerated functionality of the device
            :type  function:         :obj:`percival_detector.carrier.const.DeviceFunction`
            :param description:      Human readable description of the device
            :type  description:      unicode
            :param commands:         Supported commands for this device
            :type  commands:         `list` of :obj:`percival_detector.carrier.const.DeviceCmd`
        """
        if commands is None:
            commands = []
        self._device_family_id = device_family_id
        self._function = function
        self._description = description
        self._commands = commands
        
    @property
    def device_family_id(self):
        return self._device_family_id

    @property
    def function(self):
        return self._function

    @property
    def description(self):
        return self._description
    
    def supports_cmd(self, cmd):
        """Check if a given command is supported for this device
        
            :param cmd: The command to check for
            :type cmd:  :obj:`percival_detector.carrier.const.DeviceCmd`
            :returns:   True if the command is supported, False if not.
            :rtype:     boolean
        """
        return cmd in self._commands
        

DeviceFamilyFeatures = {
    DeviceFamily.AD5242:   DeviceFeatures(DeviceFamily.AD5242, DeviceFunction.control,
                                          "Digital potentiometer",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.reset,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value,
                                           DeviceCmd.set_value_on,
                                           DeviceCmd.set_value_off]),
    DeviceFamily.AD5263:   DeviceFeatures(DeviceFamily.AD5263, DeviceFunction.control,
                                          "Digital potentiometer",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.reset,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value]),
    DeviceFamily.AD5629:   DeviceFeatures(DeviceFamily.AD5629, DeviceFunction.control,
                                          "DAC for control",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.reset,
                                           DeviceCmd.initialize,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value,
                                           DeviceCmd.enable_standby_mode,
                                           DeviceCmd.disable_standby_mode]),
    DeviceFamily.AD5669:   DeviceFeatures(DeviceFamily.AD5669, DeviceFunction.control,
                                          "DAC for control",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.reset,
                                           DeviceCmd.initialize,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value,
                                           DeviceCmd.enable_standby_mode,
                                           DeviceCmd.disable_standby_mode]),
    DeviceFamily.LTC2309:  DeviceFeatures(DeviceFamily.LTC2309, DeviceFunction.monitoring,
                                          "ADC for monitoring",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value]),
    DeviceFamily.LTC2497:  DeviceFeatures(DeviceFamily.LTC2497, DeviceFunction.monitoring,
                                          "ADC for monitoring",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.set_value,
                                           DeviceCmd.get_value,
                                           DeviceCmd.set_and_get_value]),
    DeviceFamily.MAX31730: DeviceFeatures(DeviceFamily.MAX31730, DeviceFunction.monitoring,
                                          "Temperature for monitoring",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.reset,
                                           DeviceCmd.initialize,
                                           DeviceCmd.set_and_get_value]),
    DeviceFamily.AT24CM01: DeviceFeatures(DeviceFamily.AT24CM01, DeviceFunction.eeprom,
                                          "EEPROM for on-board storage",
                                          [DeviceCmd.no_operation,
                                           DeviceCmd.set_word_value,
                                           DeviceCmd.get_word_value,
                                           DeviceCmd.set_page_value,
                                           DeviceCmd.get_page_value]),
    }


class AD5242(object):
    """
    Representation of the AD5242 digital potentiometer device.
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._device = DeviceFamily.AD5242

    def initialize(self):
        self._channel.cmd_initialize()

    def set_value(self, value, timeout=0.1):
        """
        Set the value of the device.

        :param value: the value to set
        :param timeout: timeout for the set to complete
        """
        self._channel.set_value(value, timeout)

    def get_value(self):
        return self._channel.get_value()

    @property
    def name(self):
        return self._name

    @property
    def device(self):
        return self._device.name


class AD5263(object):
    """
    Representation of the AD5263 digital potentiometer device.
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._device = DeviceFamily.AD5263

    def initialize(self):
        self._channel.cmd_initialize()

    def set_value(self, value, timeout=0.1):
        """
        Set the value of the device.

        :param value: the value to set
        :param timeout: timeout for the set to complete
        """
        self._channel.set_value(value, timeout)

    def get_value(self):
        return self._channel.get_value()

    @property
    def name(self):
        return self._name

    @property
    def device(self):
        return self._device.name


class AD5669(object):
    """
    Representation of the AD5669 DAC device
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._device = DeviceFamily.AD5669

    def initialize(self):
        self._channel.cmd_initialize()

    def set_value(self, value, timeout=0.1):
        """
        Set the value of the device.

        :param value: the value to set
        :param timeout: timeout for the set to complete
        """
        self._channel.set_value(value, timeout)

    def get_value(self):
        return self._channel.get_value()

    @property
    def name(self):
        return self._name

    @property
    def device(self):
        return self._device.name


class MAX31730(object):
    """
    Representation of the MAX31730 temperature device
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._device = DeviceFamily.MAX31730
        self._raw_value = 0
        self._temperature = 0.0
        self._low_threshold = 0
        self._extreme_low_threshold = 0
        self._high_threshold = 0
        self._extreme_high_threshold = 0
        self._safety_exception = 0
        self._i2c_comms_error = 0
        self._sample_number = 0
        self._offset = float(self._channel._channel_ini.Offset)
        self._divider = float(self._channel._channel_ini.Divider)
        self._multiplier = float(self._channel._channel_ini.Multiplier)
        self._unit = self._channel._channel_ini.Unit

    def update(self, data=None):
        """
        Update the device status.  If data is provided (from reading a shortcut) then
        the device will update its fields accordingly.  If no data is provided then
        the device will request its current value from the hardware and update its own
        value accordingly.

        :param data: the data object for the device (or None)
        """
        if data is not None:
            self._update_status(data)
        else:
            data = self._channel.get_value()
        self._update_value(data)

    def _update_value(self, data):
        """Internal update of status items

            :param data: Data object containing all related values
            :type data:  :obj:`percival_detector.carrier.registers.ReadValueMap`
        """
        self._i2c_comms_error = data.i2c_communication_error
        self._raw_value = data.read_value
        self._temperature = (float(data.read_value) - self._offset) / self._divider * self._multiplier
        self._sample_number = data.sample_number

    def _update_status(self, data):
        """Internal update of status items
             :param data: Data object containing all related values
             :type data:  :obj:`percival_detector.carrier.registers.ReadValueMap`
        """
        self._low_threshold = data.below_low_threshold
        self._extreme_low_threshold = data.below_extreme_low_threshold
        self._high_threshold = data.above_high_threshold
        self._extreme_high_threshold = data.above_extreme_high_threshold
        self._safety_exception = data.safety_exception_detected

    @property
    def temperature(self):
        return self._temperature

    @property
    def unit(self):
        return self._unit

    @property
    def name(self):
        return self._name

    @property
    def device(self):
        return self._device.name

    @property
    def status(self):
        return {
            "device":                 "MAX31730",
            "temperature":            self._temperature,
            "raw_value":              self._raw_value,
            "sample_number":          self._sample_number,
            "low_threshold":          self._low_threshold,
            "extreme_low_threshold":  self._extreme_low_threshold,
            "high_threshold":         self._high_threshold,
            "extreme_high_threshold": self._extreme_high_threshold,
            "safety_exception":       self._safety_exception,
            "i2c_comms_error":        self._i2c_comms_error,
            "unit":                   self._unit
        }


class LTC2309:
    """
    Representation of the LTC2309 ADC device
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._device = DeviceFamily.LTC2309
        self._raw_value = 0
        self._value = 0.0
        self._low_threshold = 0
        self._extreme_low_threshold = 0
        self._high_threshold = 0
        self._extreme_high_threshold = 0
        self._safety_exception = 0
        self._i2c_comms_error = 0
        self._sample_number = 0
        self._offset = float(self._channel._channel_ini.Offset)
        self._divider = float(self._channel._channel_ini.Divider)
        self._multiplier = float(self._channel._channel_ini.Multiplier)
        self._unit = self._channel._channel_ini.Unit

    def update(self, data=None):
        """
        Update the device status.  If data is provided (from reading a shortcut) then
        the device will update its fields accordingly.  If no data is provided then
        the device will request its current value from the hardware and update its own
        value accordingly.

        :param data: the data object for the device (or None)
        """
        if data is not None:
            self._update_status(data)
        else:
            data = self._channel.get_value()
        self._update_value(data)

    def _update_value(self, data):
        """Internal update of status items

            :param data: Data object containing all related values
            :type data:  :obj:`percival_detector.carrier.registers.ReadValueMap`
        """
        self._i2c_comms_error = data.i2c_communication_error
        self._raw_value = data.read_value
        self._value = (float(data.read_value) - self._offset) / self._divider * self._multiplier
        self._sample_number = data.sample_number

    def _update_status(self, data):
        """Internal update of status items
             :param data: Data object containing all related values
             :type data:  :obj:`percival_detector.carrier.registers.ReadValueMap`
        """
        self._low_threshold = data.below_low_threshold
        self._extreme_low_threshold = data.below_extreme_low_threshold
        self._high_threshold = data.above_high_threshold
        self._extreme_high_threshold = data.above_extreme_high_threshold
        self._safety_exception = data.safety_exception_detected

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def name(self):
        return self._name

    @property
    def device(self):
        return self._device.name

    @property
    def status(self):
        return {
            "device":                 "LTC2309",
            "value":                  self._value,
            "raw_value":              self._raw_value,
            "sample_number":          self._sample_number,
            "low_threshold":          self._low_threshold,
            "extreme_low_threshold":  self._extreme_low_threshold,
            "high_threshold":         self._high_threshold,
            "extreme_high_threshold": self._extreme_high_threshold,
            "safety_exception":       self._safety_exception,
            "i2c_comms_error":        self._i2c_comms_error,
            "unit":                   self._unit
        }


DeviceFactory = {
    DeviceFamily.AD5242:     ("Digital potentiometer", AD5242),
    DeviceFamily.AD5263:     ("Digital potentiometer", AD5263),
    DeviceFamily.AD5669:     ("DAC",                   AD5669),
    DeviceFamily.MAX31730:   ("Temperature sensor",    MAX31730),
    DeviceFamily.LTC2309:    ("ADC",                   LTC2309)
}

