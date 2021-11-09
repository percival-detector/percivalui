"""
Configuration of the Percival Detector system can be loaded from various files.

This module contain classes and functions to manage the loading of configurations.
"""
from __future__ import unicode_literals, absolute_import
from future.utils import raise_with_traceback

import logging

import os
import errno
import re
from io import StringIO
from collections import OrderedDict
from configparser import SafeConfigParser
from percival.carrier.const import BoardTypes


logger = logging.getLogger(__name__)

env_config_dir = "PERCIVAL_CONFIG_DIR"
'''
The environment variable PERCIVAL_CONFIG_DIR can optionally contain a path where
to look for configuration files at runtime. The current working directory and direct/full
paths will always override this directory, which will only be searched if the file
cannot be found
'''

env_carrier_ip = "PERCIVAL_CARRIER_IP"

positive_configuration = ["true", "yes", "on", "enable", "enabled"]
negative_configuration = ["false", "no", "off", "disable", "disabled"]


def find_file(filename):
    """Search for a file and return the full path if it can be found.

    Raises IOError if a file of the given name cannot be found.

    :param filename: The filename to search for. Can be relative or full path.
    :returns: An absolute path to the file of the same name.
    """
    # Check if the filename exist as a relative or absolute path
    if os.path.isfile(filename):
        return os.path.abspath(filename)

    # Check  if the file exist in one of the search paths, indicated by
    # the user in an environemnt variable
    search_paths = os.getenv(env_config_dir, "")
    if search_paths:
        for path in search_paths.split(":"):
            fl = os.path.abspath(str(os.path.join(path, filename)))
            if os.path.isfile(fl):
                return fl

    # All other searches failed. We cant find this file. Raise exception.
    raise_with_traceback(IOError(errno.ENOENT, "%s: %s" % (os.strerror(errno.ENOENT), filename)))


class IniSectionParameters(object):
    """Mixin to be used by classes that load configuration sections from INI files.

    Child classes must implement a self._parameters dictionary of tuples: {<name>: (<value>, <datatype>)}
    """
    def __getattr__(self, name):
        if name in self._parameters.keys():
            return self._parameters[name][0]
        else:
            raise_with_traceback(AttributeError("No parameter: %s"%name))

    def __setattr__(self, name, value):
        if name not in self._parameters.keys():
            return object.__setattr__(self, name, value)
        else:
            if self._parameters[name][1] == type(value):
                self._parameters[name] = (value, type(value))
            else:
                raise_with_traceback(TypeError("Invalid type %s for parameter \"%s\""%(type(value), name)))

    def parameters(self):
        """return a list of parameter names"""
        return self._parameters.keys()

    def get_type(self, parameter):
        return self._parameters[parameter][1]

    def __str__(self):
        param_str = ""
        for (name, value) in self._parameters.items():
            param_str += "%s=%s, "%(name, value[0])
        s = "<%s: Parameters = %s>"%(self.__class__.__name__, param_str)
        return s

    @property
    def channel_index(self):
        return self._channel_number

    def __repr__(self):
        return self.__str__()


class ControlChannelIniParameters(IniSectionParameters):
    section_regexp = re.compile(r'^Control_channel<\d{4}>$')

    def __init__(self, channel_number):
        object.__setattr__(self, '_parameters', {})  # This prevents infinite recursion when setting attributes
        self._channel_number = channel_number
        self.ini_section = None
        self._parameters = {"UART_address": (0, int),
                            "Board_type": (0, int),
                            "Channel_name": (0, str),
                            "I2C_address": (0, int),
                            "I2C_Sub_address": (0, int),
                            "I2C_bus_selection": (0, int),
                            "Component_family_ID": (0, int),
                            "Device_ID": (0, int),
                            "Channel_ID": (0, int),
                            "Minimum_value": (0, int),
                            "Maximum_value": (0, int),
                            "Default_OFF_value": (0, int),
                            "Default_ON_value": (0, int),
                            "Value": (0, int),
                            "Power_status": (0, bool),
                            "Channel_offset": (0, int),
                            "Channel_multiplier": (0, int),
                            "Channel_divider": (0, int),
                            "Channel_unit": (0, str),
                            }


class MonitoringChannelIniParameters(IniSectionParameters):
    section_regexp = re.compile(r'^Monitoring_channel<\d{4}>$')

    def __init__(self, channel_number):
        object.__setattr__(self, '_parameters', {})  # This prevents infinite recursion when setting attributes
        self._channel_number = channel_number
        self.ini_section = None
        self._parameters = {"UART_address": (0, int),
                            "Board_type": (0, int),
                            "Channel_name": (0, str),
                            "I2C_address": (0, int),
                            "I2C_Sub_address": (0, int),
                            "I2C_bus_selection": (0, int),
                            "Component_family_ID": (0, int),
                            "Device_ID": (0, int),
                            "Channel_ID": (0, int),
                            "Extreme_low_threshold": (0, int),
                            "Extreme_high_threshold": (0, int),
                            "Low_threshold": (0, int),
                            "High_threshold": (0, int),
                            "Safety_action_0_select": (0, bool),
                            "Safety_action_1_select": (0, bool),
                            "Safety_action_2_select": (0, bool),
                            "Safety_action_3_select": (0, bool),
                            "Safety_action_4_select": (0, bool),
                            "Safety_action_5_select": (0, bool),
                            "Safety_action_6_select": (0, bool),
                            "Safety_action_7_select": (0, bool),
                            "Read_frequency": (0, int),
                            "Safety_exception_threshold": (0, int),
                            "Minimum_value": (0, int),
                            "Maximum_value": (0, int),
                            "Offset": (0, int),
                            "Multiplier": (0, int),
                            "Divider": (0, int),
                            "Unit": (0, str),
                            }


#class BufferDACIniParameters(IniSectionParameters):
#    section_regexp = re.compile(r'^Buffer_DAC<\d{4}>$')
#
#    def __init__(self, channel_number):
#        object.__setattr__(self, '_parameters', {})  # This prevents infinite recursion when setting attributes
#        self._channel_number = channel_number
#        self.ini_section = None
#        self._parameters = {"Channel_name": (0, str),
#                            "Buffer_index": (0, int),
#                            "Bit_offset": (0, int),
#                            "Bit_size": (0, int),
#                            }


class ChannelParameters(object):
    """
    Loads device channel settings and parameters from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = find_file(ini_file)
        self.conf = None

        self._control_channels = None
        self._monitoring_channels = None

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the `self.control_channels` and `self.monitoring_channels` properties.
        """
        self._control_channels = None
        self._monitoring_channels = None
        self.conf = SafeConfigParser(dict_type=OrderedDict)
        self.conf.read(self._ini_filename)
        self.log.debug("Read Board Parameters INI file %s:", self._ini_filename)
        self.log.debug("    sections: %s", self.conf.sections())

    @staticmethod
    def _get_channel_number(section_name):
        match = re.match(r'^.*_channel<(\d{4})>$', section_name)
        if match:
            result = int(match.group(1))
            return result
        else:
            raise_with_traceback(RuntimeError("Unable to detect channel name from \"%s\""%section_name))

    def _get_channel_matching(self, regexp):
        sections_matching = []
        for section in self.conf.sections():
            if regexp.match(section):
                sections_matching.append(section)
        return sections_matching

    def _get_channel_name_by_address(self, uart_address, channels):
        for ch in channels:
            if ch.UART_address == uart_address:
                return ch.Channel_name

    def _get_channel_name_by_index(self, index, channels):
        for ch in channels:
            if ch.channel_index == index:
                name = ch.Channel_name
                if name is None or len(name) == 0:
                    name = ch.ini_section
                return name

    def _get_channel_name_by_id_and_board_type(self, channel_id, board_type, channels):
        for ch in channels:
            if ch.Channel_ID == channel_id and BoardTypes(ch.Board_type) == board_type:
                name = ch.Channel_name
                if name is None or len(name) == 0:
                    name = ch.ini_section
                return name

    def _get_channel_by_address(self, uart_address, channels):
        for ch in channels:
            if ch.UART_address == uart_address:
                return ch

    def monitoring_channel_name_by_index(self, index):
        return self._get_channel_name_by_index(index, self.monitoring_channels)

    def monitoring_channel_name_by_id_and_board_type(self, channel_id, board_type):
        return self._get_channel_name_by_id_and_board_type(channel_id, board_type, self.monitoring_channels)

    def control_channel_name_by_index(self, index):
        return self._get_channel_name_by_index(index, self.control_channels)

    def monitoring_channel_name(self, uart_address):
        return self._get_channel_name_by_address(uart_address, self.monitoring_channels)

    def control_channel_name(self, uart_address):
        return self._get_channel_name_by_address(uart_address, self.control_channels)

    def control_channel_by_address(self, uart_address):
        return self._get_channel_by_address(uart_address, self.control_channels)

    def monitoring_channel_by_address(self, uart_address):
        return self._get_channel_by_address(uart_address, self.monitoring_channels)

    def control_channels_by_name(self, name):
        return self._get_channels_by_name(self.control_channels, name)

    def monitoring_channels_by_name(self, name):
        return self._get_channels_by_name(self.monitoring_channels, name)

    @property
    def control_channels(self):
        """
        List of `ControlChannelIniParameters`
        """
        if self._control_channels:
            return self._control_channels
        self._control_channels = self._get_channels(ControlChannelIniParameters)
        return self._control_channels

    @property
    def monitoring_channels(self):
        """
        List of `MonitoringChannelIniParameters`
        """
        if self._monitoring_channels:
            return self._monitoring_channels
        self._monitoring_channels = self._get_channels(MonitoringChannelIniParameters)
        return self._monitoring_channels

    def _get_channels(self, channel_class):
        """
        Loop through all channel sections matching a certain type `channel_class` and parse the parameters of each
        section into new `channel_class` instance objects.

        :param channel_class: an :class:`IniSectionParameters` derivative class
        :return: a list of instances of the channel_class :obj:`IniSectionParameters` derivative.
        :rtype list:
        """
        channels = []
        sections = self._get_channel_matching(channel_class.section_regexp)
        for section in sections:
            channel_number = self._get_channel_number(section)
            channel = channel_class(channel_number)
            channel.ini_section = section
            for param in channel.parameters():
                parameter_type = channel.get_type(param)
                if parameter_type == int:
                    value = self.conf.getint(section, param)
                elif parameter_type == str:
                    value = self.conf.get(section, param)
                    value = str(value.strip("\""))  # Get rid of any double quotes from the ini file
                elif parameter_type == bool:
                    str_value = self.conf.get(section, param)
                    if str_value.lower() in positive_configuration:
                        value = True
                    elif str_value.lower() in negative_configuration:
                        value = False
                    else:
                        raise_with_traceback(TypeError("Unsupported boolean: %s = \"%s\""%(param, str_value)))
                else:
                    raise_with_traceback(TypeError("Unsupported parameter type %s"%str(parameter_type)))
                channel.__setattr__(param, value)
            self.log.debug("Appending channel: %s", channel)
            channels.append(channel)
        return channels

    @staticmethod
    def _get_channels_by_name(channel_list, name):
        result = []
        for ch in channel_list:
            if re.match(name, ch.Channel_name):
                result.append(ch)
        if len(result) == 1:
            result = result[0]
        return result

    def __str__(self):
        channels = "Control channels: "
        if self._control_channels:
            channels += str(len(self._control_channels))
        else:
            channels += "[]"
        channels += " Monitoring channels: "
        if self._monitoring_channels:
            channels += str(len(self._monitoring_channels))
        else:
            channels += "[]"
        s = "<%s: inifile: %s %s>"%(self.__class__.__name__, self._ini_filename, channels)
        return s

    def __repr__(self):
        return self.__str__()


class BoardParameters(object):
    """
    Loads device channel settings and parameters from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = find_file(ini_file)
        self.conf = None

    def load_ini(self):
        """
        Loads and parses the data from INI file.
        """
        self.conf = SafeConfigParser(dict_type=OrderedDict)
        self.conf.read(self._ini_filename)

        self.log.debug("Read Board Parameters INI file %s:", self._ini_filename)
        self.log.debug("    sections: %s", self.conf.sections())

    @property
    def board_name(self):
        if "Board_header" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Board_header section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Board_header", "Board_name")

    @property
    def board_type(self):
        if "Board_header" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Board_header section not found in ini file %s" % str(self._ini_filename)))
        return BoardTypes(self.conf.getint("Board_header", "Board_type"))


    @property
    def board_revision(self):
        if "Board_header" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Board_header section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.getint("Board_header", "Board_revision_number")

    @property
    def control_channels_count(self):
        if "Entry_counts" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Entry_counts section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.getint("Entry_counts", "Control_channels_count")

    @property
    def monitoring_channels_count(self):
        if "Entry_counts" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Entry_counts section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.getint("Entry_counts", "Monitoring_channels_count")


class ControlParameters(object):
    """
    Loads control parameter from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = find_file(ini_file)
        self.conf = None
        self._ini_file_options = ["system_settings_file",
                                  "chip_readout_settings_file",
                                  "clock_settings_file",
                                  "sensor_dac_file",
                                  "sensor_configuration_file",
                                  "sensor_calibration_file",
                                  "sensor_debug_file",
                                  "board_bottom_settings_file",
                                  "board_carrier_settings_file",
                                  "board_left_settings_file",
                                  "board_plugin_settings_file",
                                  "channel_settings_file"]
        self._ini_download_options = ["system_settings_download",
                                      "chip_readout_settings_download",
                                      "clock_settings_download",
                                      "sensor_dac_download",
                                      "sensor_configuration_download",
                                      "sensor_calibration_download",
                                      "sensor_debug_download"]

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        """
        self.conf = SafeConfigParser(dict_type=OrderedDict)
        self.conf.read(self._ini_filename)
        self.log.debug("Read Percival control ini file %s:", self._ini_filename)
        self.log.debug("    sections: %s", self.conf.sections())

    @property
    def carrier_ip(self):
        if "Control" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Control section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Control", "carrier_ip").strip("\"")

    @property
    def database_ip(self):
        if "Database" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Database section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Database", "address").strip("\"")

    @property
    def database_port(self):
        if "Database" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Database section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Database", "port").strip("\"")

    @property
    def database_name(self):
        if "Database" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Database section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Database", "name").strip("\"")

    def __getattr__(self, item):
        if item in self._ini_file_options:
            return self.get_ini_file(item)
        elif item in self._ini_download_options:
            return self.get_ini_file_download(item)

    def get_ini_file(self, item):
        if "Configuration" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Configuration section not found in ini file %s" % str(self._ini_filename)))
        value = self.conf.get("Configuration", item).strip("\"")
        self.log.debug("Checking for %s in percival control config file.  Value: %s", item, value)
        return value

    def get_ini_file_download(self, item):
        value = False
        if "Configuration" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Configuration section not found in ini file %s" % str(self._ini_filename)))
        raw_value = self.conf.get("Configuration", item).strip("\"")
        self.log.debug("Checking for %s in percival control config file.  Raw value: %s", item, raw_value)
        if 'false' in str(raw_value).lower():
            value = False
        elif 'true' in str(raw_value).lower():
            value = True
        else:
            self.log.error("Could not parse %s in percival control config file.  Raw value: %s", item, raw_value)

        self.log.debug("    Processed value: %s", value)
        return value

    @property
    def control_group_ini_file(self):
        if "Configuration" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Configuration section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Configuration", "control_groups").strip("\"")

    @property
    def monitor_group_ini_file(self):
        if "Configuration" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Configuration section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Configuration", "monitor_groups").strip("\"")

    @property
    def setpoint_ini_file(self):
        if "Configuration" not in self.conf.sections():
            raise_with_traceback(RuntimeError("Configuration section not found in ini file %s" % str(self._ini_filename)))
        return self.conf.get("Configuration", "setpoints").strip("\"")


#class BufferParameters(object):
#    """
#    Loads buffer transfer description from an INI file.
#    """
#    def __init__(self, ini_file):
#        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
#        self._ini_filename = find_file(ini_file)
#        self.conf = None
#        self._dac_channels = None
#
#    def load_ini(self):
#        """
#        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
#        through the property methods
#        """
#        self.conf = SafeConfigParser(dict_type=OrderedDict)
#        self.conf.read(self._ini_filename)
#        self.log.debug("Read Buffer Transfer Parameters INI file %s:", self._ini_filename)
#        self.log.debug("    sections: %s", self.conf.sections())
#
#    @staticmethod
#    def _get_channel_number(section_name):
#        match = re.match(r'^.*Buffer_DAC<(\d{4})>$', section_name)
#        if match:
#            result = int(match.group(1))
#            return result
#        else:
#            raise_with_traceback(RuntimeError("Unable to detect channel name from \"%s\""%section_name))
#
#    def _get_channel_matching(self, regexp):
#        sections_matching = []
#        for section in self.conf.sections():
#            if regexp.match(section):
#                sections_matching.append(section)
#        return sections_matching
#
#    @property
#    def dac_channels(self):
#        """
#        List of `BufferDACIniParameters`
#        """
#        if self._dac_channels:
#            return self._dac_channels
#        self._dac_channels = self._get_channels(BufferDACIniParameters)
#        return self._dac_channels
#
#
#    def _get_channels(self, channel_class):
#        """
#        Loop through all channel sections matching a certain type `channel_class` and parse the parameters of each
#        section into new `channel_class` instance objects.
#
#        :param channel_class: an :class:`IniSectionParameters` derivative class
#        :return: a list of instances of the channel_class :obj:`IniSectionParameters` derivative.
#        :rtype list:
#        """
#        channels = []
#        sections = self._get_channel_matching(channel_class.section_regexp)
#        for section in sections:
#            channel_number = self._get_channel_number(section)
#            channel = channel_class(channel_number)
#            channel.ini_section = section
#            for param in channel.parameters():
#                parameter_type = channel.get_type(param)
#                if parameter_type == int:
#                    value = self.conf.getint(section, param)
#                elif parameter_type == str:
#                    value = self.conf.get(section, param)
#                    value = str(value.strip("\""))  # Get rid of any double quotes from the ini file
#                elif parameter_type == bool:
#                    str_value = self.conf.get(section, param)
#                    if str_value.lower() in positive_configuration:
#                        value = True
#                    elif str_value.lower() in negative_configuration:
#                        value = False
#                    else:
#                        raise_with_traceback(TypeError("Unsupported boolean: %s = \"%s\"" % (param, str_value)))
#                else:
#                    raise_with_traceback(TypeError("Unsupported parameter type %s" % str(parameter_type)))
#                channel.__setattr__(param, value)
#            self.log.debug("Appending channel: %s", channel)
#            channels.append(channel)
#        return channels


class ChannelGroupParameters(object):
    """
    Loads groups of controls description from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        """
        self.conf = SafeConfigParser(dict_type=OrderedDict)
        self.conf.optionxform = str
        if self._ini_filename:
            self.conf.read(self._ini_filename)
            self.log.debug("Read Channel Groups INI file %s:", self._ini_filename)
        else:
            self.conf.readfp(self._ini_buffer)
            self.log.info("Read Channel Groups INI object %s", self._ini_buffer)
        self.log.debug("    sections: %s", self.conf.sections())

    @property
    def sections(self):
        return self.conf.sections()

    def get_name(self, section):
        name = ""
        for item in self.conf.items(section):
            if "Group_name" in item[0]:
                name = item[1].replace('"', '')
                break
        return name

    def get_description(self, section):
        desc = ""
        for item in self.conf.items(section):
            if "Group_description" in item[0]:
                desc = item[1].replace('"', '')
                break
        return desc

    def get_channels(self, section):
        channels = []
        for item in self.conf.items(section):
            if "Channel_name" in item[0]:
                channels.append(item[1].replace('"', ''))
        return channels


class SetpointGroupParameters(object):
    """
    Loads groups of controls description from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        """
        self.conf = SafeConfigParser(dict_type=OrderedDict)
        self.conf.optionxform = str
        if self._ini_filename:
            self.conf.read(self._ini_filename)
            self.log.info("Read Setpoint Groups INI file: %s", self._ini_filename)
        else:
            self.conf.readfp(self._ini_buffer)
            self.log.info("Read Setpoint Groups INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self.conf.sections())

    @property
    def sections(self):
        return self.conf.sections()

    def get_name(self, section):
        name = ""
        for item in self.conf.items(section):
            if "Setpoint_name" in item[0]:
                name = item[1].replace('"', '')
                break
        return name

    def get_description(self, section):
        desc = ""
        for item in self.conf.items(section):
            if "Setpoint_description" in item[0]:
                desc = item[1].replace('"', '')
                break
        return desc

    # this needs renaming eg get_devices2values
    def get_setpoints(self, section):
        sps = {}
        for item in self.conf.items(section):
            if "Setpoint_description" not in item and "Setpoint_name" not in item:
                sps[item[0]] = item[1]
        return sps


class SystemSettingsParameters(object):
    """
    Loads groups of controls description from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read System Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read System Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the section names
        # For each section read out the param names
        # Create a large map of both
        map = {}
        for section in self._conf.sections():
            for item in self._conf.items(section):
                map[section+"_"+item[0]] = item[1]
        return map


class ChipReadoutSettingsParameters(object):
    """
    Loads chip readout settings from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Chip Readout Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Chip Readout Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the section names
        # For each section read out the param names
        # Create a large map of both
        map = {}
        for section in self._conf.sections():
            for item in self._conf.items(section):
                map[section+"_"+item[0]] = item[1]
        return map


class ClockSettingsParameters(object):
    """
    Loads clock settings from an INI file.
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Clock Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Clock Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the section names
        # For each section read out the param names
        # Create a large map of both
        map = {}
        for section in self._conf.sections():
            for item in self._conf.items(section):
                map[section+"_"+item[0]] = item[1]
        return map


class SensorDACParameters(object):
    """
    Loads sensor configuration parameters from an INI file
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Sensor DAC INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Sensor DAC INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the DAC section that sets the sensor DAC values
        values = {}
        for item in self._conf.items('Sensor_DAC'):
            values[item[0]] = int(item[1])
        return values


class SensorConfigurationParameters(object):
    """
    Loads sensor configuration parameters from an INI file
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Sensor Configuration Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Sensor Configuration Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the section General that describes the rest of the file
        values = {}
        desc = {}
        for item in self._conf.items('General'):
            match = re.match(r'^.*Cols<(\w*)>$', item[0])
            if match:
                desc[match.group(1)] = int(item[1])
        # Now loop over each defined group adding the values
        self.log.info("Ini description: %s", desc)
        for item in desc:
            val_list = []
            for index in range(desc[item]):
                item_name = "Col<{}>".format(index)
                val_list.append(self._conf.getint(item, item_name))
            values[item] = val_list
        return values


class SensorCalibrationParameters(object):
    """
    Loads sensor calibration parameters from an INI file
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Sensor Configuration Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Sensor Configuration Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        # Read out the section General that describes the rest of the file
        values = {}
        desc = {}
        target_signals = 4
        for item in self._conf.items('General'):
            match = re.match(r'^.*Cols<(\w*)>$', item[0])
            if match:
                desc[match.group(1)] = int(item[1])
            elif 'target_signals' in item[0].lower():
                target_signals = int(item[1])
        # Now loop over each defined group adding the values
        self.log.info("Ini description: %s", desc)
        for item in desc:
            values[item] = {}
            for cal_no in range(target_signals):
                target_string = 'Cal{}'.format(cal_no)
                values[item][target_string] = {}
                right_val_list = []
                left_val_list = []
                for index in range(desc[item]):
                    item_name = "RightCal<{}>Col<{}>".format(cal_no, index)
                    right_val_list.append(self._conf.getint(item, item_name))
                    item_name = "LeftCal<{}>Col<{}>".format(cal_no, index)
                    left_val_list.append(self._conf.getint(item, item_name))
                values[item][target_string]['Right'] = right_val_list
                values[item][target_string]['Left'] = left_val_list
        self.log.info("Calibration Map: %s", values)
        return values


class SensorDebugParameters(object):
    """
    Loads sensor debug parameters from an INI file
    """
    def __init__(self, ini_file):
        self.log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._ini_filename = None
        self._ini_buffer = None
        self._conf = None
        try:
            self._ini_filename = find_file(ini_file)
        except:
            # If we catch any kind of exception here then treat the parameter as the configuration
            self._ini_buffer = StringIO(unicode(ini_file))

    def load_ini(self):
        """
        Loads and parses the data from INI file. The data is stored internally in the object and can be retrieved
        through the property methods
        For the system settings all parameter names <section>_<name>
        """
        self._conf = SafeConfigParser(dict_type=OrderedDict)
        self._conf.optionxform = str
        if self._ini_filename:
            self._conf.read(self._ini_filename)
            self.log.info("Read Sensor Debug Settings INI file: %s", self._ini_filename)
        else:
            self._conf.readfp(self._ini_buffer)
            self.log.info("Read Sensor Debug Settings INI object %s", self._ini_buffer)
        self.log.info("    sections: %s", self._conf.sections())

    @property
    def value_map(self):
        values = {}
        desc = {}
        # item will be a tuple (key , value) from the Debug section of the config file
        for item in self._conf.items('Debug'):
            values[item[0]] = item[1]

        return values


