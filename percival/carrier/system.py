"""
Created on 18 May 2016

:author: Alan Greer

A class representation for a Percival system command.

An instance is initialised with a percival.carrier.txrx.TxRx object and
commands can be sent using the send_command method.
"""


import logging
from percival.carrier import const
from percival.carrier.registers import UARTRegister, generate_register_maps
from percival.carrier.errors import PercivalSystemCommandError


class SystemCommand(object):
    """
    Represent a Percival system command.
    """
    def __init__(self, txrx):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self._txrx = txrx
        self._reg_command = UARTRegister(const.COMMAND)
        self._reg_command.initialize_map([0,0,0])

    def _get_command_msg(self, cmd):
        """
        Private method to construct a system command message object (TxMessage).

        The returned object contains the correct address and word for executing the
        specified command and can be sent through the txrx object to the Percival
        hardware.

        :param cmd: command to encode
        :type  cmd: SystemCmd
        :returns: percival.carrier.txrx.TxMessage
        """
        if type(cmd) != const.SystemCmd:
            raise TypeError("Command %s is not a SystemCommand"%cmd)
        self._reg_command.fields.system_cmd = cmd.value
        cmd_msg = self._reg_command.get_write_cmd_msg(eom=True)[2]
        return cmd_msg

    def _command(self, cmd):
        """
        Private method to construct and send a system command.

        This method gets the TxMessage object representation of the system command
        and sends it through the txrx object to the Percival hardware, returning any
        response.

        Returns nothing as the lower level checks for expected response.
        Can raise RuntimeError if the expected response is not received.

        :param cmd: command to encode
        :type  cmd: SystemCmd
        """
        cmd_msg = self._get_command_msg(cmd)
        self._txrx.send_recv_message(cmd_msg)

    def cmd_no_operation(self):
        """
        Method to send a no_operation system command.

        Returns nothing as the lower level checks for expected response.
        Can raise RuntimeError if the expected response is not received.
        """
        self._command(const.SystemCmd.no_operation)

    def send_command(self, cmd):
        """
        Method to send a system command.

        This method first sends a no_operation command, followed by the specified
        system command.

        :param cmd: command to encode
        :type  cmd: SystemCmd
        """
        self.cmd_no_operation()
        self._command(cmd)


class SystemStatus(object):
    # Constants used for limits
    def __init__(self, txrx):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._txrx = txrx
        self._value_block = const.READ_VALUES_STATUS
        self._reg_status_values = UARTRegister(self._value_block)
        self._cmd_msg = self._reg_status_values.get_read_cmd_msg()
        self._read_maps = None

    def read_values(self):
        """Read all carrier monitor channels with one READ VALUES shortcut command

        Parse the resuling [(address, data), (address, data)...] array of tuples into a list of
        :class:`percival.carrier.register.ReadValueMap` objects.

        :returns: list of :class:`percival.carrier.register.ReadValueMap` objects.
        :rtype: list
        """
        response = self._txrx.send_recv_message(self._cmd_msg)
        self._log.debug(response)
        self._read_maps = generate_register_maps(response)[0]
        self._log.debug(self._read_maps)
        return response

    def get_status(self):
        response = {
            "Image_counter": self._read_maps.Image_counter,
            "Acquisition_counter": self._read_maps.Acquisition_counter,
            "Train_number": (self._read_maps.Train_number_MSB << 32) + self._read_maps.Train_number_LSB,
            "LVDS_IOs_enabled": self._read_maps.LVDS_IOs_enabled,
            "Master_reset": self._read_maps.Master_reset,
            "PLL_reset": self._read_maps.PLL_reset,
            "dmux_CDN": self._read_maps.dmux_CDN,
            "sr7DIn_0": self._read_maps.sr7DIn_0,
            "sr7DIn_1": self._read_maps.sr7DIn_1,
            "horiz_data_in_0": self._read_maps.horiz_data_in_0,
            "horiz_data_in_1": self._read_maps.horiz_data_in_1,
            "enable_testpoints": self._read_maps.enable_testpoints,
            "startup_mode_enabled": self._read_maps.startup_mode_enabled,
            "global_monitoring_enabled": self._read_maps.global_monitoring_enabled,
            "device_level_safety_controls_enabled": self._read_maps.device_level_safety_controls_enabled,
            "system_level_safety_controls_enabled": self._read_maps.system_level_safety_controls_enabled,
            "experimental_level_safety_controls_enabled": self._read_maps.experimental_level_safety_controls_enabled,
            "safety_actions_enabled": self._read_maps.safety_actions_enabled,
            "system_armed": self._read_maps.system_armed,
            "acquiring": self._read_maps.acquiring,
            "wait_for_trigger": self._read_maps.wait_for_trigger,
            "sensor_active_for_acquisition": self._read_maps.sensor_active_for_acquisition,
            "MEZZ_A_PHY_OK": self._read_maps.MEZZ_A_PHY_OK,
            "MEZZ_A_MGT_OK": self._read_maps.MEZZ_A_MGT_OK,
            "MEZZ_A_RESET": self._read_maps.MEZZ_A_RESET,
            "MEZZ_B_PHY_OK": self._read_maps.MEZZ_B_PHY_OK,
            "MEZZ_B_MGT_OK": self._read_maps.MEZZ_B_MGT_OK,
            "MEZZ_B_RESET": self._read_maps.MEZZ_B_RESET,
            "MARKER_OUT_0": self._read_maps.MARKER_OUT_0,
            "MARKER_OUT_1": self._read_maps.MARKER_OUT_1,
            "MARKER_OUT_2": self._read_maps.MARKER_OUT_2,
            "MARKER_OUT_3": self._read_maps.MARKER_OUT_3,
            "include_train_number_in_status_record": self._read_maps.include_train_number_in_status_record,
            "PLUGIN_RESET": self._read_maps.PLUGIN_RESET,
            "DataSynchError": self._read_maps.DataSynchError,
            "HIGH_FREQ_ADJ_CLOCK_0_clock_enable": self._read_maps.HIGH_FREQ_ADJ_CLOCK_0_clock_enable,
            "HIGH_FREQ_ADJ_CLOCK_1_clock_enable": self._read_maps.HIGH_FREQ_ADJ_CLOCK_1_clock_enable,
            "HIGH_FREQ_ADJ_CLOCK_2_clock_enable": self._read_maps.HIGH_FREQ_ADJ_CLOCK_2_clock_enable,
            "HIGH_FREQ_ADJ_CLOCK_3_clock_enable": self._read_maps.HIGH_FREQ_ADJ_CLOCK_3_clock_enable,
            "LOW_FREQ_ADJ_CLOCK_0_clock_enable": self._read_maps.LOW_FREQ_ADJ_CLOCK_0_clock_enable,
            "LOW_FREQ_ADJ_CLOCK_1_clock_enable": self._read_maps.LOW_FREQ_ADJ_CLOCK_1_clock_enable,
            "safety_driven_assert_marker_out_3_completed": self._read_maps.safety_driven_assert_marker_out_3_completed,
            "safety_driven_assert_marker_out_2_completed": self._read_maps.safety_driven_assert_marker_out_2_completed,
            "safety_driven_assert_marker_out_1_completed": self._read_maps.safety_driven_assert_marker_out_1_completed,
            "safety_driven_assert_marker_out_0_completed": self._read_maps.safety_driven_assert_marker_out_0_completed,
            "safety_driven_fast_enable_control_standby_completed": self._read_maps.safety_driven_fast_enable_control_standby_completed,
            "safety_driven_fast_sensor_powerdown_completed": self._read_maps.safety_driven_fast_sensor_powerdown_completed,
            "safety_driven_exit_acquisition_armed_status_completed": self._read_maps.safety_driven_exit_acquisition_armed_status_completed,
            "safety_driven_stop_acquisition_completed": self._read_maps.safety_driven_stop_acquisition_completed
			}

        return response


class SystemSettings(object):
    # Constants used for limits
    Integration_window_width_max = 2**16 - 1
    TRIG_REP_RATE_MAX = 2**32 - 1
    TRIG_ACQ_DELAY_MAX = 2**16 - 1
    TRIG_FPT_MAX = 2**16 - 1
    SAMPLING_MAX = 2**4 - 1
    ADV_OPT_MAX = 2
    ADV_DISABLE_DURATION_MAX = 2**16 - 1
    I2C_IDLE_TIME_MAX = 2**16 - 1
    MONITORING_TIME_MAX = 2**32 - 1
    SAFETY_OPT_MAX = 2**4 - 1

    def __init__(self, settings_ini=None):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._reg_command = UARTRegister(const.SYSTEM_SETTINGS)
        self._reg_command.initialize_map([0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0])
        self._txrx = None
        self._settings_ini = None
        if settings_ini:
            self.load_ini(settings_ini)

    def load_ini(self, settings_ini):
        """
        Load settings from ini file into the registers ready for writing to hardware
        :param settings_ini:
        :return:
        """
        if settings_ini:
            self._settings_ini = settings_ini
            map = self._settings_ini.value_map
            self._log.info("Full description of ini %s", map)
            # First replace any true or false with 1 or 0
            for item in map:
                if isinstance(map[item], str) or isinstance(map[item], str):
                    if 'false' in map[item].lower():
                        map[item] = 0
                    elif 'true' in map[item].lower():
                        map[item] = 1
            # Now set the attributes within the UART Register
            for item in map:
                try:
                    if hasattr(self._reg_command.fields, item):
                        setattr(self._reg_command.fields, item, int(map[item]))
                    else:
                        self._log.debug("No register found for ini file setting %s", item)
                except:
                    self._log.error("Failed to set iten %s from ini file", item)
                    raise
        else:
            self._log.debug("Attempted to load a none type ini object")

    def set_txrx(self, txrx):
        self._txrx = txrx

    def _send_to_carrier(self):
        """
        Private method to construct and send a system command.

        This method gets the TxMessage object representation of the system command
        and sends it through the txrx object to the Percival hardware, returning any
        response.

        Returns nothing as the lower level checks for expected response.
        Can raise RuntimeError if the expected response is not received.

        :param cmd: command to encode
        :type  cmd: SystemCmd
        """
        cmd_msgs = self._reg_command.get_write_cmd_msg(eom=True)
        for cmd_msg in cmd_msgs:
            self._txrx.send_recv_message(cmd_msg)

    def download_settings(self):
        if self._settings_ini:
            self._send_to_carrier()

    @property
    def settings(self):
        return self._reg_command.fields.map_fields

    def set_number_of_frames(self, no_of_frames):
        self._reg_command.fields.ACQUISITION_Number_of_frames = no_of_frames
        self._send_to_carrier()

    def set_acquisition_mode(self, acquisition_mode):
        self._reg_command.fields.ACQUISITION_Acquisition_mode = acquisition_mode
        self._send_to_carrier()

    def set_continuous_acquisition(self, continuous_mode):
        self._reg_command.fields.ACQUISITION_Acquisition_mode = continuous_mode
        self._send_to_carrier()

    def set_sensor_type(self, sensor_type):
        self._reg_command.fields.REGION_OF_INTEREST_Sensor_type = sensor_type
        self._send_to_carrier()

    def set_illumination(self, illumination):
        self._reg_command.fields.REGION_OF_INTEREST_Illumination = illumination
        self._send_to_carrier()

    def set_value(self, setting, value):
        # First replace any true or false with 1 or 0
        if isinstance(value, str) or isinstance(value, str):
            if 'false' in value.lower():
                value = 0
            elif 'true' in value.lower():
                value = 1
        try:
            if hasattr(self._reg_command.fields, setting):
                setattr(self._reg_command.fields, setting, int(value))
                self._send_to_carrier()
            else:
                self._log.debug("No system register found for %s", setting)
                raise PercivalSystemCommandError("No system register found for {}".format(setting))
        except:
            self._log.error("Failed to set iten %s from ini file", setting)
            raise PercivalSystemCommandError("Failed to set {} to {}".format(setting, value))

    def set_values(self, section, params):
        # First replace any true or false with 1 or 0
        for item in params:
            if isinstance(params[item], str) or isinstance(params[item], str):
                if 'false' in params[item].lower():
                    params[item] = 0
                elif 'true' in params[item].lower():
                    params[item] = 1
        # Now set the attributes within the UART Register
        for item in params:
            full_name = section + item
            try:
                if hasattr(self._reg_command.fields, full_name):
                    setattr(self._reg_command.fields, full_name, int(params[item]))
                else:
                    self._log.debug("No system register found for %s", full_name)
                    raise PercivalSystemCommandError("No system register found for {}".format(full_name))
            except:
                self._log.error("Failed to set iten %s from ini file", full_name)
                raise PercivalSystemCommandError("Failed to set {} to {}".format(full_name, params[item]))
        self._send_to_carrier()

    def set_roi(self, params):
        self.set_values("REGION_OF_INTEREST_", params)

    def set_integration(self, params):
        self.set_values("INTEGRATION_", params)

    def set_triggering(self, params):
        self.set_values("TRIGGERING_", params)

    def set_sampling(self, params):
        self.set_values("SAMPLING_", params)

    def set_advanced(self, params):
        self.set_values("ADVANCED_", params)

    def set_monitoring(self, params):
        self.set_values("MONITORING_", params)

    def set_safety(self, params):
        self.set_values("SAFETY_", params)

    def set_marker_board(self, params):
        self.set_values("MARKER_BOARD_", params)

    def set_plugin_board(self, params):
        self.set_values("PLUGIN_BOARD_", params)

    @staticmethod
    def parse_boolean_param(name, params):
        value = 0
        try:
            if params[name]:
                value = 1
            else:
                value = 0
        except:
            # Raise a system command exception
            raise PercivalSystemCommandError("Cannot parse {} [supplied: {}]".format(name, params[name]))
        return value

    @staticmethod
    def parse_integer_param(name, params, min, max):
        try:
            parameter = params[name]
            if parameter < min:
                raise PercivalSystemCommandError("{} must be {} or greater [supplied: {}]".
                                                 format(name, min, parameter))
            if parameter > max:
                raise PercivalSystemCommandError("{} must be {} or less [supplied: {}]".
                                                 format(name, max, parameter))
            return parameter
        except:
            # Raise a system command exception
            raise PercivalSystemCommandError("Cannot parse {} [supplied: {}]".
                                             format(name, params[name]))


class ClockSettings(object):
    def __init__(self, settings_ini=None):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._reg_command = UARTRegister(const.CLOCK_SETTINGS)
        self._reg_command.initialize_map([0, 0, 0, 0, 0, 0, 0, 0])
        self._txrx = None
        self._settings_ini = None
        if settings_ini:
            self.load_ini(settings_ini)

    def load_ini(self, settings_ini):
        """
        Load settings from ini file into the registers ready for writing to hardware
        :param settings_ini:
        :return:
        """
        if settings_ini:
            self._settings_ini = settings_ini
            map = self._settings_ini.value_map
            self._log.info("Full description of ini %s", map)
            # First replace any true or false with 1 or 0
            for item in map:
                if isinstance(map[item], str) or isinstance(map[item], str):
                    if 'false' in map[item].lower():
                        map[item] = 0
                    elif 'true' in map[item].lower():
                        map[item] = 1
            # Now set the attributes within the UART Register
            for item in map:
                try:
                    if hasattr(self._reg_command.fields, item):
                        setattr(self._reg_command.fields, item, int(map[item]))
                    else:
                        self._log.debug("No register found for ini file setting %s", item)
                except:
                    self._log.error("Failed to set iten %s from ini file", item)
                    raise
        else:
            self._log.debug("Attempted to load a none type ini object")

    def set_txrx(self, txrx):
        self._txrx = txrx

    def _send_to_carrier(self):
        """
        Private method to construct and send a system command.

        This method gets the TxMessage object representation of the system command
        and sends it through the txrx object to the Percival hardware, returning any
        response.

        Returns nothing as the lower level checks for expected response.
        Can raise RuntimeError if the expected response is not received.

        :param cmd: command to encode
        :type  cmd: SystemCmd
        """
        cmd_msgs = self._reg_command.get_write_cmd_msg(eom=True)
        for cmd_msg in cmd_msgs:
            self._txrx.send_recv_message(cmd_msg)

    def download_settings(self):
        if self._settings_ini:
            self._send_to_carrier()

