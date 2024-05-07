"""
Created on 20 May 2016

@author: Alan Greer
"""

import os
import logging
import threading
import time
from percival_detector.log import get_exclusive_file_logger
from datetime import datetime, timedelta
import getpass
import sys
import traceback
is_py2 = sys.version[0] == '2'
if is_py2:
    import queue as queue
else:
    import queue as queue

from percival_detector.carrier import const
from percival_detector.carrier.buffer import BufferCommand, SensorBufferCommand
from percival_detector.carrier.channels import ControlChannel, MonitoringChannel
from percival_detector.carrier.devices import DeviceFactory
from percival_detector.carrier.database import InfluxDB
from percival_detector.carrier.registers import generate_register_maps, BoardValueRegisters
from percival_detector.carrier.sensor import Sensor
from percival_detector.carrier.settings import BoardSettings
from percival_detector.carrier.system import SystemCommand, SystemSettings, ClockSettings, SystemStatus
from percival_detector.carrier.chip import ChipReadoutSettings
from percival_detector.carrier.txrx import TxRx
from percival_detector.carrier.values import BoardValues
from percival_detector.carrier.configuration import SystemSettingsParameters, \
    ChipReadoutSettingsParameters, \
    ClockSettingsParameters, \
    ChannelParameters,\
    SensorConfigurationParameters, \
    SensorCalibrationParameters, \
    SensorDebugParameters, \
    BoardParameters, \
    ControlParameters,\
    ChannelGroupParameters,\
    SetpointGroupParameters,\
    SensorDACParameters,\
    env_carrier_ip
from percival_detector.control.errors import PercivalDetectorError
from percival_detector.control.groups import Group
from percival_detector.control.command import PercivalCommandNames
from percival_detector.control.set_point import SetPointControl


class PercivalParameters(object):
    """
    High level representation of Parameters loaded from ini files.

    Currently the files are all hardcoded here which is not very elegant.

    A better approach would be to be able to specify the files within the main ini file, and for the files to be
    searched in standard locations or through environment variables.  This is partially implemented for the
    ChannelParameters class.

    ini files are parsed for overall control parameters, for each of the boards and finally for the channels.

    All ini settings are stored and can be accessed through this class.
    """
    def __init__(self, ini_file=None):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        # Check for master ini file
        if ini_file:
            self._control_params = ControlParameters(ini_file)
        else:
            # Try to load a default file
            try:
                self._control_params = ControlParameters("config/percival.ini")
            except:
                raise PercivalDetectorError("Could not process the Percival initialisation file")

        self._board_params = None
        self._channel_params = None
        self._system_settings_params = None
        self._chip_readout_settings_params = None
        self._clock_settings_params = None
        self._sensor_configuration_params = None
        self._sensor_calibration_params = None
        self._sensor_debug_params = None
        self._sensor_dac_params = None
        self._control_group_params = None
        self._monitor_group_params = None
        self._setpoint_group_params = SetpointGroupParameters();

    def load_ini(self):
        """
        Load the initialisation files for the control, four board types and for the channels
        """
        self._control_params.load_ini()

        try:
            self._board_params = {
                const.BoardTypes.left: BoardParameters(self._control_params.board_left_settings_file),
                const.BoardTypes.bottom: BoardParameters(self._control_params.board_bottom_settings_file),
                const.BoardTypes.carrier: BoardParameters(self._control_params.board_carrier_settings_file),
                const.BoardTypes.plugin: BoardParameters(self._control_params.board_plugin_settings_file)
            }
            self._board_params[const.BoardTypes.left].load_ini()
            self._board_params[const.BoardTypes.bottom].load_ini()
            self._board_params[const.BoardTypes.carrier].load_ini()
            self._board_params[const.BoardTypes.plugin].load_ini()
        except:
            self._log.error("Could not initialise board configuration from ini files")
            raise PercivalDetectorError("Could not initialise board configuration from ini files")

        try:
            self._channel_params = ChannelParameters(self._control_params.channel_settings_file)
            self._channel_params.load_ini()
        except:
            self._log.error("Could not initialise channel parameters from ini file")
            raise PercivalDetectorError("Could not initialise channel parameters from ini file")

        try:
            self.load_system_settings_ini(self._control_params.system_settings_file)
        except:
            self._log.debug("No default system settings ini file to load")

        try:
            self.load_chip_readout_settings_ini(self._control_params.chip_readout_settings_file)
        except:
            self._log.debug("No default chip readout settings ini file to load")

        try:
            self.load_clock_settings_ini(self._control_params.clock_settings_file)
        except:
            self._log.debug("No default clock settings ini file to load")

        try:
            self.load_sensor_configuration_params(self._control_params.sensor_configuration_file)
        except:
            self._log.debug("No default sensor configuration ini file to load")

        try:
            self.load_sensor_calibration_params(self._control_params.sensor_calibration_file)
        except:
            self._log.debug("No default sensor calibration ini file to load")

        try:
            self.load_sensor_debug_params(self._control_params.sensor_debug_file)
        except:
            self._log.debug("No default sensor debug ini file to load")

        try:
            self.load_sensor_dac_params(self._control_params.sensor_dac_file)
        except:
            self._log.debug("No default sensor DAC ini file to load")

        try:
            self.load_control_group_ini(self._control_params.control_group_ini_file)
        except:
            self._log.debug("No default control groups ini file to load")

        try:
            self.load_monitor_group_ini(self._control_params.monitor_group_ini_file)
        except:
            self._log.debug("No default monitor groups ini file to load")

        try:
            self.load_setpoint_group_ini(self._control_params.setpoint_ini_file)
        except:
            self._log.debug("No default setpoints ini file to load")

    def load_system_settings_ini(self, filename):
        # Create the ini object from either filename or raw file
        self._system_settings_params = SystemSettingsParameters(filename)
        self._system_settings_params.load_ini()

    def load_chip_readout_settings_ini(self, filename):
        # Create the ini object from either filename or raw file
        self._chip_readout_settings_params = ChipReadoutSettingsParameters(filename)
        self._chip_readout_settings_params.load_ini()

    def load_clock_settings_ini(self, filename):
        # Create the ini object from either filename or raw file
        self._clock_settings_params = ClockSettingsParameters(filename)
        self._clock_settings_params.load_ini()

    def load_sensor_configuration_params(self, filename):
        # Create the ini object from either filename or raw file
        self._sensor_configuration_params = SensorConfigurationParameters(filename)
        self._sensor_configuration_params.load_ini()

    def load_sensor_calibration_params(self, filename):
        # Create the ini object from either filename or raw file
        self._sensor_calibration_params = SensorCalibrationParameters(filename)
        self._sensor_calibration_params.load_ini()

    def load_sensor_debug_params(self, filename):
        # Create the ini object from either filename or raw file
        self._sensor_debug_params = SensorDebugParameters(filename)
        self._sensor_debug_params.load_ini()

    def load_sensor_dac_params(self, filename):
        # Create the ini object from either filename or raw file
        self._sensor_dac_params = SensorDACParameters(filename)
        self._sensor_dac_params.load_ini()

    def load_control_group_ini(self, filename):
        # Create the ini object from either filename or raw file
        self._control_group_params = ChannelGroupParameters(filename)
        self._control_group_params.load_ini()

    def load_monitor_group_ini(self, filename):
        # Create the ini object from either filename or raw file
        self._monitor_group_params = ChannelGroupParameters(filename)
        self._monitor_group_params.load_ini()

    def load_setpoint_group_ini(self, filename):
        # Extend the ini object from either filename or string
        self._setpoint_group_params.load_ini(filename)

    @property
    def carrier_ip(self):
        """
        Return the IP address of the carrier board.

        The IP address configuration will be loaded from the percival.ini config file or overwritten by the user with
        the environment variable PERCIVAL_CARRIER_IP. If no configurations can be found it will default to 192.168.0.2.

        :returns: IP address of the carrier board
        :rtype: str
        """
        try:
            default_carrier_ip = self._control_params.carrier_ip
        except RuntimeError:
            default_carrier_ip = "192.168.0.2"
            self._log.warning("No carrier IP address found in configuration file")
        return os.getenv(env_carrier_ip, default_carrier_ip)

    @property
    def database(self):
        """
        Return the IP address, port number and name of the database.

        The IP address configuration will be loaded from the percival.ini config file.

        :returns: Database configuration object
        :rtype: Dict
        """
        db = {}
        try:
            db["address"] = self._control_params.database_ip
        except RuntimeError:
            db["address"] = "127.0.0.1"

        try:
            db["port"] = int(self._control_params.database_port)
        except RuntimeError:
            db["port"] = 8086

        try:
            db["name"] = self._control_params.database_name
        except RuntimeError:
            db["name"] = "percival"

        return db

    @property
    def download_system_settings(self):
        download = False
        try:
            download = self._control_params.system_settings_download
        except:
            self._log.info("Could not parse system_settings_download value from config file")
        return download

    @property
    def download_chip_readout_settings(self):
        download = False
        try:
            download = self._control_params.chip_readout_settings_download
        except:
            self._log.info("Could not parse chip_readout_settings_download value from config file")
        return download

    @property
    def download_clock_settings(self):
        download = False
        try:
            download = self._control_params.clock_settings_download
        except:
            self._log.info("Could not parse clock_settings_download value from config file")
        return download

    @property
    def download_sensor_configuration(self):
        download = False
        try:
            download = self._control_params.sensor_configuration_download
        except:
            self._log.info("Could not parse sensor_configuration_download value from config file")
        return download

    @property
    def download_sensor_calibration(self):
        download = False
        try:
            download = self._control_params.sensor_calibration_download
        except:
            self._log.info("Could not parse sensor_calibration_download value from config file")
        return download

    @property
    def download_sensor_debug(self):
        download = False
        try:
            download = self._control_params.sensor_debug_download
        except:
            self._log.info("Could not parse sensor_debug_download value from config file")
        return download

    @property
    def download_sensor_dac(self):
        download = False
        try:
            download = self._control_params.sensor_dac_download
        except:
            self._log.info("Could not parse sensor_dac_download value from config file")
        return download

    def board_name(self, board):
        """
        Return the name of the specified board type

        :param board: Which board to return the name
        :type board: const.BoardTypes
        :returns: Name of the specified board
        :rtype: str
        """
        return self._board_params[board].board_name

    def board_type(self, board):
        """
        Return the type of the specified board

        :param board: Which board to return the type
        :type board: const.BoardTypes
        :returns: Type of the specified board
        :rtype: str
        """
        return self._board_params[board].board_type

    def control_channels_count(self, board):
        """
        Return the number of control channels of the specified board

        :param board: Which board to return the number of control channels
        :type board: const.BoardTypes
        :returns: Number of control channels
        :rtype: int
        """
        return self._board_params[board].control_channels_count

    def monitoring_channels_count(self, board):
        """
        Return the number of monitor channels of the specified board

        :param board: Which board to return the number of monitor channels
        :type board: const.BoardTypes
        :returns: Number of monitor channels
        :rtype: int
        """
        return self._board_params[board].monitoring_channels_count

    def control_channel_by_address(self, uart_address):
        """
        Search for the control channel by its UART address

        :param uart_address: Address of the control channel
        :type uart_address: int
        :returns: Control channel ini parameters
        :rtype: configuration.ControlChannelIniParameters
        """
        return self._channel_params.control_channel_by_address(uart_address)

    def monitoring_channel_by_address(self, uart_address):
        """
        Search for the monitor channel by its UART address

        :param uart_address: Address of the monitor channel
        :type uart_address: int
        :returns: Monitor channel ini parameters
        :rtype: configuration.MonitorChannelIniParameters
        """
        return self._channel_params.monitoring_channel_by_address(uart_address)

    def monitoring_channel_name_by_index_and_board_type(self, index, board):
        """
        Search for the monitor channel name by its ini file index and the board type

        :param index: Index of the channel
        :type index: int
        :param board: Which board to search
        :type board: const.BoardTypes
        :returns: Monitor channel name
        :rtype: str
        """
        return self._channel_params.monitoring_channel_name_by_id_and_board_type(index, board)

    def monitoring_channel_by_name(self, channel_name):
        """
        Search for the monitor channel by its name

        :param channel_name: Name of the monitor channel
        :type channel_name: str
        :returns: Monitor channel ini parameters
        :rtype: configuration.MonitorChannelIniParameters
        """
        self._log.debug(self._channel_params)
        return self._channel_params.monitoring_channels_by_name(channel_name)

    def control_channel_by_name(self, channel_name):
        """
        Search for the control channel by its name

        :param channel_name: Name of the control channel
        :type channel_name: str
        :returns: Control channel ini parameters
        :rtype: configuration.ControlChannelIniParameters
        """
        self._log.debug(self._channel_params)
        return self._channel_params.control_channels_by_name(channel_name)

    @property
    def monitoring_channels(self):
        """
        Return a list of `MonitoringChannelIniParameters`

        :returns: List of monitor channel ini parameters
        :rtype: list
        """
        return self._channel_params.monitoring_channels

    @property
    def control_channels(self):
        """
        Return a list of `ControlChannelIniParameters`

        :returns: List of control channel ini parameters
        :rtype: list
        """
        return self._channel_params.control_channels

    @property
    def system_settings_params(self):
        return self._system_settings_params

    @property
    def chip_readout_settings_params(self):
        return self._chip_readout_settings_params

    @property
    def clock_settings_params(self):
        return self._clock_settings_params

    @property
    def sensor_configuration_params(self):
        return self._sensor_configuration_params

    @property
    def sensor_calibration_params(self):
        return self._sensor_calibration_params

    @property
    def sensor_debug_params(self):
        return self._sensor_debug_params

    @property
    def sensor_dac_params(self):
        return self._sensor_dac_params

    @property
    def control_group_params(self):
        return self._control_group_params

    @property
    def monitor_group_params(self):
        return self._monitor_group_params

    @property
    def setpoint_params(self):
        return self._setpoint_group_params


class PercivalDetector(object):
    """
    High level representation of Detector hardware.
    This class manages the connection to the hardware, as well as the configuration and specific setup.

    Low level hardware complexity is handled internally and a simple interface is presented as a public API
    for control and status monitoring.

    This class has no threading internally but should be considered thread safe (needs checking)
    """
    def __init__(self, ini_file=None, download_config=True, initialise_hardware=True):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        logging.getLogger('requests').setLevel(self._log.level)
        logging.getLogger('urllib3').setLevel(self._log.level)
        self._trace_log = logging.getLogger("percival_trace")
        self._trace_log.info("Percival execution trace logging")
        self._log.info("Executing detector constructor")
        self._start_time = datetime.now()
        self._username = getpass.getuser()
        self._download_configuration = download_config
        self._initialise_hardware = initialise_hardware
        self._txrx = None
        self._db = None
        self._global_monitoring = True
        self._log.info("Executing detector constructor")
        self._percival_params = PercivalParameters(ini_file)
        self._board_settings = {}
        self._board_values ={}
        self._monitors = {}
        self._control_chs = {}
        self._sys_cmd = None
        self._system_status = None
        self._sensor_buffer_cmd = None
        self._sensor = None
        self._control_groups = None
        self._monitor_groups = None
        self._active_command = None
        self._write_buffer = []
        self._read_buffer = []
        self._log.info("Creating SystemSettings object")
        self._system_settings = SystemSettings()
        self._log.info("SystemSettings : %s", self._system_settings.settings)

        self._log.info("Creating ChipReadoutSettings object")
        self._chip_readout_settings = ChipReadoutSettings()
        self._log.info("Creating ClockSettings object")
        self._clock_settings = ClockSettings()
        self._log.info("Creating SetPointControl object")
        self._setpoint_control = SetPointControl(self)
        self._log.info("Starting setpoint control scan loop")
        self._setpoint_control.start_scan_loop()
        self._log.info("Calling load_ini for detector")
        self.load_ini()
        self._log.info("Setting up database connection to influxdb")
        self.setup_db()
        self._log.info("Setting up control interface")
        self.setup_control()
        self.connect()
        self._command_lock = threading.Lock()
        self._command_queue = queue.Queue(1)
        self._command_thread = threading.Thread(target=self.command_loop)
        self._command_thread.start()
        self._run_status_loop = True
        self._status_thread = threading.Thread(target=self.system_status_loop)
        self._status_thread.start()

    def system_status_loop(self):
        while self._run_status_loop:
            try:
                self._system_status.read_values()
                if self._db:
                    time_now = datetime.utcnow()
                    data = self._system_status.get_status()
                    point = {}
                    for key in ['Image_counter', 'system_armed', 'acquiring']:
                        point[key] = data[key]
                    self._db.log_point(time_now, 'Detector', point)
            except:
                pass
            time.sleep(2.0)

    def cleanup(self):
        self._run_status_loop = False
        self.queue_command(None)
        self._setpoint_control.stop_scan_loop()

    def load_ini(self):
        """
        Load the initialisation files for the detector
        """
        self._log.info("Loading detector ini files...")
        self._percival_params.load_ini()
        self._system_settings.load_ini(self._percival_params.system_settings_params)
        self._chip_readout_settings.load_ini(self._percival_params.chip_readout_settings_params)
        self._clock_settings.load_ini(self._percival_params.clock_settings_params)
        self._setpoint_control.set_params(self._percival_params.setpoint_params)

    def setup_control(self):
        """
        Setup the control interface for the detector.
        This currently:
        Creates the TxRx connection class and connects to the hardware
        Creates the BoardSettings classes to describe the hardware.  These can be used to either download hardware
        configurations from ini files or to read settings from the hardware.
        Creates a SystemCommand instance which can be used to send system commands to the hardware.
        """
        self._log.info("Carrier IP set as: %s", self._percival_params.carrier_ip)
        self._txrx = TxRx(self._percival_params.carrier_ip, port=10001)
        self._board_settings[const.BoardTypes.left] = BoardSettings(self._txrx, const.BoardTypes.left)
        self._board_settings[const.BoardTypes.bottom] = BoardSettings(self._txrx, const.BoardTypes.bottom)
        self._board_settings[const.BoardTypes.carrier] = BoardSettings(self._txrx, const.BoardTypes.carrier)
        self._board_settings[const.BoardTypes.plugin] = BoardSettings(self._txrx, const.BoardTypes.plugin)
        self._board_values[const.BoardTypes.left] = BoardValues(self._txrx, const.BoardTypes.left)
        self._board_values[const.BoardTypes.bottom] = BoardValues(self._txrx, const.BoardTypes.bottom)
        self._board_values[const.BoardTypes.carrier] = BoardValues(self._txrx, const.BoardTypes.carrier)
        self._board_values[const.BoardTypes.plugin] = BoardValues(self._txrx, const.BoardTypes.plugin)
        self._system_settings.set_txrx(self._txrx)
        self._chip_readout_settings.set_txrx(self._txrx)
        self._clock_settings.set_txrx(self._txrx)
        self._sys_cmd = SystemCommand(self._txrx)
        self._system_status = SystemStatus(self._txrx)
        self._sensor_buffer_cmd = SensorBufferCommand(self._txrx)
        self._sensor = Sensor(self._sensor_buffer_cmd)

    def connect(self):
        """
        Request a connection to the detector hardware
        :return:
        """
        self._txrx.connect()
        if self._txrx.connected:
            self._log.info("Checking for auto-download of configuration files")
            self.auto_download()
            if self._download_configuration:
                self._log.info("Loading channel configuration to hardware")
                self.load_configuration()
            self._log.info("Loading channel information from hardware shortcuts")
            self.load_channels()
            if self._initialise_hardware:
                self._log.info("Executing initialisation of channels")
                self.initialize_channels()

    def auto_download(self):
        # Check if we are asked to auto download the system settings to hardware
        if self._percival_params.download_system_settings:
            self._log.info("Auto-downloading system settings from default ini file")
            self.download_system_settings()

        # Check if we are asked to auto download the chip readout settings to hardware
        if self._percival_params.download_chip_readout_settings:
            self._log.info("Auto-downloading chip readout settings from default ini file")
            self.download_chip_readout_settings()

        # Check if we are asked to auto download the clock settings to hardware
        if self._percival_params.download_clock_settings:
            self._log.info("Auto-downloading clock settings from default ini file")
            self.download_clock_settings()

        # Check if we are asked to auto download the sensor configuration to hardware
        if self._percival_params.download_sensor_configuration:
            self._log.info("Auto-downloading sensor configuration from default ini file")
            self._sensor.apply_configuration(self._percival_params.sensor_configuration_params.value_map)

        # Check if we are asked to auto download the sensor configuration to hardware
        if self._percival_params.download_sensor_calibration:
            self._log.info("Auto-downloading sensor calibration from default ini file")
            self._sensor.apply_calibration(self._percival_params.sensor_calibration_params.value_map)

        # Check if we are asked to auto download the sensor configuration to hardware
        if self._percival_params.download_sensor_debug:
            self._log.info("Auto-downloading sensor debug from default ini file")
            self._sensor.apply_debug(self._percival_params.sensor_debug_params.value_map)

        # Check if we are asked to auto download the sensor configuration to hardware
        if self._percival_params.download_sensor_dac:
            self._log.info("Auto-downloading sensor DACs from default ini file")
            self._sensor.apply_dac_values(self._percival_params.sensor_dac_params.value_map)

    def setup_db(self):
        """
        Provide a DB interface for logging data from the detector.
        This will store the DB object for use when reading status.
        The DB object must support the following interface:
        ...
        ...
        ...

        :param db:
        :return:
        """
        self._db = InfluxDB(self._percival_params.database["address"],
                            self._percival_params.database["port"],
                            self._percival_params.database["name"]
                            )
        self._connect_db()

    def _connect_db(self):
        # Attempt connection to the database
        self._db.connect()

    def load_configuration(self):
        """
        Download the configuration from ini files to the hardware.
        """
        self._log.info("Downloading configuration to hardware")

        cmd_msgs = self._board_settings[const.BoardTypes.left].initialise_board(self._percival_params)
        cmd_msgs += self._board_settings[const.BoardTypes.bottom].initialise_board(self._percival_params)
        cmd_msgs += self._board_settings[const.BoardTypes.carrier].initialise_board(self._percival_params)
        cmd_msgs += self._board_settings[const.BoardTypes.plugin].initialise_board(self._percival_params)
        for cmd_msg in cmd_msgs:
            try:
                resp = self._txrx.send_recv_message(cmd_msg)
            except RuntimeError:
                self._log.exception("no response (message: %s)", cmd_msg)
            # TODO: check response resp

    def download_system_settings(self):
        self._log.info("Downloading system settings to hardware")
        self._system_settings.download_settings()

    def download_chip_readout_settings(self):
        self._log.info("Downloading chip readout settings to hardware")
        self._chip_readout_settings.download_settings()

    def download_clock_settings(self):
        self._log.info("Downloading clock settings to hardware")
        self._clock_settings.download_settings()

    def download_sensor_configuration(self):
        self._log.info("Downloading sensor configuration to hardware")
        self._sensor.apply_configuration(self._percival_params.sensor_configuration_params.value_map)

    def download_sensor_calibration(self):
        self._log.info("Downloading sensor calibration to hardware")
        self._sensor.apply_calibration(self._percival_params.sensor_calibration_params.value_map)

    def download_sensor_debug(self):
        self._log.info("Downloading sensor debug to hardware")
        self._sensor.apply_debug(self._percival_params.sensor_debug_params.value_map)

    def download_sensor_dacs(self):
        self._log.info("Downloading sensor DAC values to hardware")
        self._sensor.apply_dac_values(self._percival_params.sensor_dac_params.value_map)

    def apply_sensor_roi(self):
        self._log.info("Applying sensor ROI to hardware")
        self._sensor.apply_roi()

    def load_channels(self):
        """
        Readout the settings from the hardware and create all control and monitoring devices according to the current
        settings coupled with the ini file descriptions.
        Monitor type devices are stored in the _monitors dictionary.
        Control type devices are stored in the _control_chs dictionary.
        """
        # We can only load the channel information if we have a valid connection
        if self._txrx.connected:
            # Readback the monitoring settings
            self._board_settings[const.BoardTypes.left].readback_monitoring_settings()
            self._board_settings[const.BoardTypes.bottom].readback_monitoring_settings()
            self._board_settings[const.BoardTypes.carrier].readback_monitoring_settings()
            self._board_settings[const.BoardTypes.plugin].readback_monitoring_settings()
            # Get the list of monitor names
            monitors = self._percival_params.monitoring_channels
            for monitor in monitors:
                # Check for the board type
                bt = const.BoardTypes(monitor.Board_type)
                if bt != const.BoardTypes.prototype:
                    settings = self._board_settings[bt].device_monitoring_settings(monitor.UART_address)
                    mc = MonitoringChannel(self._txrx, monitor, settings)
                    if mc._channel_ini.Channel_name is None or len(mc._channel_ini.Channel_name) == 0:
                        self._log.debug("Dropping %s as it has no channel name defined",
                                        (const.DeviceFamily(mc._channel_ini.Component_family_ID)).name)
                    else:
                        self._log.debug("Adding %s [%s] to monitor set",
                                           (const.DeviceFamily(mc._channel_ini.Component_family_ID)).name,
                                           mc._channel_ini.Channel_name)
                        description, device = DeviceFactory[const.DeviceFamily(mc._channel_ini.Component_family_ID)]
                        self._monitors[mc._channel_ini.Channel_name] = device(mc._channel_ini.Channel_name, mc)

            # Readback the control settings
            self._board_settings[const.BoardTypes.left].readback_control_settings()
            self._board_settings[const.BoardTypes.bottom].readback_control_settings()
            self._board_settings[const.BoardTypes.carrier].readback_control_settings()
            self._board_settings[const.BoardTypes.plugin].readback_control_settings()
            # Get the list of control names
            controls = self._percival_params.control_channels
            for control in controls:
                # Check for the board type
                bt = const.BoardTypes(control.Board_type)
                if bt != const.BoardTypes.prototype:
                    settings = self._board_settings[bt].device_control_settings(control.UART_address)
                    cc = ControlChannel(self._txrx, control, settings)
                    if cc._channel_ini.Channel_name is None or len(cc._channel_ini.Channel_name) == 0:
                        self._log.debug("Dropping %s as it has no channel name defined",
                                        (const.DeviceFamily(cc._channel_ini.Component_family_ID)).name)
                    else:
                        self._log.debug("Adding %s [%s] to control set",
                                           (const.DeviceFamily(cc._channel_ini.Component_family_ID)).name,
                                           cc._channel_ini.Channel_name)
                        description, device = DeviceFactory[const.DeviceFamily(cc._channel_ini.Component_family_ID)]
                        self._control_chs[cc._channel_ini.Channel_name] = device(cc._channel_ini.Channel_name, cc)

#            # Load the sensor DACs from the ini file
#            sensor_dacs = self._percival_params.sensor_dac_channels
#            for dac in sensor_dacs:
#                self._sensor.add_dac(dac)

            # Load in control groups from the ini file
            self._control_groups = Group(self._percival_params.control_group_params)

            # Load in control groups from the ini file
            self._monitor_groups = Group(self._percival_params.monitor_group_params)

    def load_system_settings(self, system_settings_ini):
        self._log.debug("Loading system settings with config: %s", system_settings_ini)
        self._percival_params.load_system_settings_ini(system_settings_ini)
        self._system_settings.load_ini(self._percival_params.system_settings_params)

    def load_chip_readout_settings(self, chip_readout_settings_ini):
        self._log.debug("Loading chip readout settings with config: %s", chip_readout_settings_ini)
        self._percival_params.load_chip_readout_settings_ini(chip_readout_settings_ini)
        self._chip_readout_settings.load_ini(self._percival_params.chip_readout_settings_params)

    def load_clock_settings(self, clock_settings_ini):
        self._log.debug("Loading clock settings with config: %s", clock_settings_ini)
        self._percival_params.load_clock_settings_ini(clock_settings_ini)
        self._clock_settings.load_ini(self._percival_params.clock_settings_params)

    def load_sensor_configuration(self, sensor_config_ini):
        self._log.debug("Loading sensor configuration with config: %s", sensor_config_ini)
        self._percival_params.load_sensor_configuration_params(sensor_config_ini)

    def load_sensor_calibration(self, sensor_calib_ini):
        self._log.debug("Loading sensor calibration with config: %s", sensor_calib_ini)
        self._percival_params.load_sensor_calibration_params(sensor_calib_ini)

    def load_sensor_debug(self, sensor_debug_ini):
        self._log.debug("Loading sensor debug with config: %s", sensor_debug_ini)
        self._percival_params.load_sensor_debug_params(sensor_debug_ini)

    def load_sensor_dacs(self, sensor_dac_ini):
        self._log.debug("Loading sensor DACs with config: %s", sensor_dac_ini)
        self._percival_params.load_sensor_dac_params(sensor_dac_ini)

    def load_control_groups(self, control_groups_ini):
        self._log.debug("Loading control groups with config: %s", control_groups_ini)
        self._percival_params.load_control_group_ini(control_groups_ini)
        self._control_groups = Group(self._percival_params.control_group_params)

    def load_monitor_groups(self, monitor_groups_ini):
        self._log.debug("Loading monitor groups with config: %s", monitor_groups_ini)
        self._percival_params.load_monitor_group_ini(monitor_groups_ini)
        self._monitor_groups = Group(self._percival_params.monitor_group_params)

    def load_setpoints(self, setpoint_ini):
        self._log.debug("Loading set-points with config: %s", setpoint_ini)
        self._percival_params.load_setpoint_group_ini(setpoint_ini)
        self._setpoint_control.set_params(self._percival_params.setpoint_params)

    def queue_command(self, command):
        # Special command case is an abort of a scan
        if not self.check_for_abort_command(command):
            # acquire(F) says do not wait for command_lock.
            if self._command_lock.acquire(False):
                if command: command.activate();
                self._active_command = command
                self._command_queue.put(command, block=False)
                self._command_lock.release()
            else:
                # note this message is searched for in percival_detector.js
                raise PercivalDetectorError("Cannot submit command whilst another is active")

    def check_for_abort_command(self, command):
        if command is not None:
            if 'PUT' in command.command_type:
                if command.command_name in str(PercivalCommandNames.cmd_abort_scan):
                    # Log the trace information from the command object
                    self._trace_log.info("{} Command [{}] executed, parameters: {}".format(command.command_type,
                                                                                           command.command_name,
                                                                                           command.parameters))
                    self._trace_log.info(command.format_trace)
                    self._setpoint_control.abort_scan()
                    return True
        return False

    def command_loop(self):
        running = True
        while running:
            try:
                command = self._command_queue.get()
                if command:
                    with self._command_lock:
                        self.execute_command(command)
                else:
                    running = False
            except PercivalDetectorError as e:
                self._active_command.complete(success=False, message=str(e))
            except Exception as e:
                type_, value_, traceback_ = sys.exc_info()
                ex = traceback.format_exception(type_, value_, traceback_)
                self._active_command.complete(success=False, message="Unhandled exception: {} => {}".format(str(e), str(ex)))

    def execute_command(self, command):
        """
        Log the execution of the command (use command trace)
        Apply the command trace to the detector
        Check for the specific command type and call the correct method
        :param command:
        :return:
        """
        response = {}
        # Check if the command is a PUT command
        if 'PUT' in command.command_type:
            # Log the trace information from the command object
            self._trace_log.info("{} Command [{}] executed, parameters: {}".format(command.command_type,
                                                                                   command.command_name,
                                                                                   command.log_parameters))
            command.activate()
            self._trace_log.info(command.format_trace)
            self._active_command = command
            # Check if the command is a connection request to the DB
            if command.command_name in str(PercivalCommandNames.cmd_download_channel_cfg):
                # No parameters required for this command
                self._percival_params.load_ini()
                self.load_configuration()
                self.load_channels()
                self._active_command.complete(success=True)
            if command.command_name in str(PercivalCommandNames.cmd_connect_hardware):
                self.connect()
                self._active_command.complete(success=True)
            if command.command_name in str(PercivalCommandNames.cmd_connect_db):
                # No parameters required for this command
                self.setup_db()
                self._active_command.complete(success=True)
            if command.command_name in str(PercivalCommandNames.cmd_apply_roi):
                # No parameters required for this command
                self.apply_sensor_roi()
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_load_config):
                # Parameter [config_type] one of setpoint, ctrl_group, mon_group, channels
                # Parameter [config] path to config file or the configuration contents
                if command.has_param('config_type'):
                    if command.has_param('config'):
                        if len(command.get_param('config')) > 0:
                            config_type = command.get_param('config_type')
                            config_desc = command.get_param('config')
                            if 'setpoints' in config_type:
                                self.load_setpoints(config_desc)
                            elif 'control_groups' in config_type:
                                self.load_control_groups(config_desc)
                            elif 'monitor_groups' in config_type:
                                self.load_monitor_groups(config_desc)
                            elif 'system_settings' in config_type:
                                self.load_system_settings(config_desc)
                                self.download_system_settings()
                            elif 'chip_readout_settings' in config_type:
                                self.load_chip_readout_settings(config_desc)
                                self.download_chip_readout_settings()
                            elif 'clock_settings' in config_type:
                                self.load_clock_settings(config_desc)
                                self.download_clock_settings()
                            elif 'sensor_configuration' in config_type:
                                self.load_sensor_configuration(config_desc)
                                self.download_sensor_configuration()
                            elif 'sensor_calibration' in config_type:
                                self.load_sensor_calibration(config_desc)
                                self.download_sensor_calibration()
                            elif 'sensor_debug' in config_type:
                                self.load_sensor_debug(config_desc)
                                self.download_sensor_debug()
                            elif 'sensor_dacs' in config_type:
                                self.load_sensor_dacs(config_desc)
                                self.download_sensor_dacs()
                            self._active_command.complete(success=True)
                        else:
                            self._active_command.complete(success=False,
                                                          message='Empty configuration parameter supplied')
                    else:
                        raise PercivalDetectorError("No config provided (file or object)")
                else:
                    raise PercivalDetectorError("No config_type specified")
            elif command.command_name in str(PercivalCommandNames.cmd_set_channel):
                # Parameter [channel] is the name of the channel to apply to
                # Parameter [value] is the value to apply
                if command.has_param('channel'):
                    channel = command.get_param('channel')
                    if command.has_param('value'):
                        value = int(float(command.get_param('value')))
                        self.set_value(channel, value)
                        self._active_command.complete(success=True)
                    else:
                        raise PercivalDetectorError("No value supplied to set channel command")
                else:
                    raise PercivalDetectorError("No channel supplied for set channel command")
            elif command.command_name in str(PercivalCommandNames.cmd_system_setting):
                # Parameter [setting] is the name of the system setting to apply
                # Parameter [value] is the value to apply
                if command.has_param('setting'):
                    channel = command.get_param('setting')
                    if command.has_param('value'):
                        value = int(command.get_param('value'))
                        self.set_system_setting(channel, value)
                        self._active_command.complete(success=True)
                    else:
                        raise PercivalDetectorError("No value supplied to set system setting {}".format(channel))
                else:
                    raise PercivalDetectorError("No setting supplied for set system setting command")
            elif command.command_name in str(PercivalCommandNames.cmd_apply_setpoint):
                # Parameter [setpoint] is the name of the setpoint to apply
                if command.has_param('setpoint'):
                    self._setpoint_control.apply_set_point(command.get_param('setpoint'))
                    self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_scan_setpoints):
                # Parameter [setpoints] is a list of setpoints to scan or a single setpoint to scan to
                # Parameter [dwell] is the dwell time in ms at each point
                # Parameter [steps] is the number of steps between the points
                if command.has_param('setpoints'):
                    # Check there are at least two setpoints
                    setpoints = command.get_param('setpoints')
                    if isinstance(setpoints, list):
                        if len(setpoints) < 2:
                            raise PercivalDetectorError("Scanning requires two setpoints")
                        if command.has_param('dwell'):
                            dwell = int(command.get_param('dwell'))
                            if command.has_param('steps'):
                                steps = int(command.get_param('steps')) + 1
                                self._setpoint_control.scan_set_points(setpoints, steps, dwell)
                                self._setpoint_control.wait_for_scan_to_complete()
                                self._active_command.complete(success=True)
                            else:
                                raise PercivalDetectorError("Number of scan steps required to scan")
                        else:
                            raise PercivalDetectorError("Dwell time (ms) required to scan")
                    else:
                        # This is a safety scan starting from the current position
                        if command.has_param('dwell'):
                            dwell = int(command.get_param('dwell'))
                            if command.has_param('steps'):
                                steps = int(command.get_param('steps'))
                                self._setpoint_control.safety_scan_set_point(setpoints, steps, dwell)
                                self._setpoint_control.wait_for_scan_to_complete()
                                self._active_command.complete(success=True)
                            else:
                                raise PercivalDetectorError("Number of scan steps required to scan")
                        else:
                            raise PercivalDetectorError("Dwell time (ms) required to scan")
                else:
                    raise PercivalDetectorError("No setpoints defined to scan between")
            elif command.command_name in str(PercivalCommandNames.cmd_write_buffer):
                # Manual buffer write operation
                if command.has_param('data'):
                    data_words = command.get_param('data')
                    buffer_cmd = BufferCommand(self._txrx, const.BufferTarget.none)
                    if isinstance(data_words, str):
                        data_words = [data_words]
                    buffer_cmd.write_words_to_buffer([int(word) for word in data_words])
                    data = buffer_cmd.read_words_from_write_buffer()
                    self._write_buffer = []
                    for addr, value in data:
                        self._write_buffer.append(value)
                    self._active_command.complete(success=True)
                else:
                    raise PercivalDetectorError("No data supplied to the write buffer command")
            elif command.command_name in str(PercivalCommandNames.cmd_refresh_write_buffer):
                buffer_cmd = BufferCommand(self._txrx, const.BufferTarget.none)
                data = buffer_cmd.read_words_from_write_buffer()
                self._write_buffer = []
                for addr, value in data:
                    self._write_buffer.append(value)
                self._log.error("WRITE BUFFER: %s", self._write_buffer)
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_refresh_read_buffer):
                buffer_cmd = BufferCommand(self._txrx, const.BufferTarget.none)
                data = buffer_cmd.read_words_from_read_buffer()
                self._read_buffer = []
                for addr, value in data:
                    self._read_buffer.append(value)
                self._log.error("READ BUFFER: %s", self._read_buffer)
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_buffer_transfer):
                target = const.BufferTarget[command.get_param('target')]
                cmd = const.BufferCmd[command.get_param('command')]
                no_of_words = int(command.get_param('words'))
                address = int(command.get_param('address'))
                buffer_cmd = BufferCommand(self._txrx, target)
                buffer_cmd.send_command(cmd, no_of_words, address)
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_update_monitors):
                # Force a read of the monitors.  This will result in values being written to db
                self.update_monitors()
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_initialise_channels):
                # Initialise the channels on the Percival hardware
                self.initialize_channels()
                self._active_command.complete(success=True)
            elif command.command_name in str(PercivalCommandNames.cmd_apply_sensor_dacs):
                # Apply the current set of sensor DAC values
                self.apply_sensor_dac_values()
                self._active_command.complete(success=True)
            # Check if the command is a system_command
            elif command.command_name in str(PercivalCommandNames.cmd_system_command):
                # We expect a single parameter which is the command
                if command.has_param('name'):
                    # Execute the system command
                    self.system_command(command.get_param('name'))
                    self._active_command.complete(success=True)

        # Check if the command is a GET command
        elif 'GET' in command.command_type:
            # Request for reading information
            response = self.read(command.command_name)

        return response

    def download_configuration(self):
        self.load_configuration()
        self.load_channels()

    def initialize_channels(self):
        """
        Initialize all control devices that support the command.
        """
        for control in self._control_chs:
            self._control_chs[control].initialize()

    def set_global_monitoring(self, state=True):
        """
        Turn on or off global monitoring.  This sends two system commands; enable_global_monitoring and
        enable_device_level_safety_controls.
        It also sets the internal monitoring flag to either True or False.
        This seems to be some debug function that is dubious. I don't know why you would want to
          disable it here.

        :param state: Turn global monitoring on (True) or off (False)
        :type state: bool
        """
        if state:
            #self._sys_cmd.send_command(const.SystemCmd.enable_global_monitoring)
            #self._sys_cmd.send_command(const.SystemCmd.enable_device_level_safety_controls)
            self._global_monitoring = True
        else:
            self._global_monitoring = False
            #self._sys_cmd.send_command(const.SystemCmd.disable_global_monitoring)
            #self._sys_cmd.send_command(const.SystemCmd.disable_device_level_safety_controls)

    def system_command(self, cmd):
        """
        Send a system command.

        :param cmd: System command to send
        :type cmd: str
        """
        self._sys_cmd.send_command(const.SystemCmd[cmd])

    def initialize(self, device):
        """
        Initialize a control device.

        :param device: Name of device to set the value of
        :type device: str
        """
        if device in self._control_chs:
            self._control_chs[device].initialize()

    def set_system_setting(self, setting, value):
        """
        Set the value of a system setting.

        """
        self._log.info("Setting %s to %s", setting, str(value))
        self._system_settings.set_value(setting, value)

    def set_value(self, cchannel, value, timeout=0.1):
        """
        Set the value of a control-channel.

        :param cchannel: Name of channel to set the value of
        :type cchannel: str
        :param value: Value to set
        :type value: int
        :param timeout: Timeout for the set operation
        :type timeout: double
        """
        self._log.info("Setting ch %s to %d", cchannel, value)
        if cchannel in self._control_chs:
            self._control_chs[cchannel].set_value(value, timeout)

        #elif device in self._sensor.dacs:
        #    self._sensor.set_dac(device, value)

        elif cchannel in self._control_groups.group_names:
            # A group name has been specified for the set value
            # Get the list of channels and apply the value for each one
            for channel in self._control_groups.get_channels(cchannel):
                self._control_chs[channel].set_value(value, timeout)

        else:
            self._log.warn("Channel  %s not found", cchannel)
            raise PercivalDetectorError("Cannot set value, channel {} does not exist".format(cchannel))

    def get_value(self, cchannel):
        """
        Get the last set value of a control channel.

        :param cchannel: Name of channel of which to get the value
        :type cchannel: str
        """
        value = 0
        self._log.info("Getting last value of %s", cchannel)
        if cchannel in self._control_chs:
            value = self._control_chs[cchannel].get_value()
            self._log.info("Value of %s is %d", cchannel, value)

        else:
            self._log.warn("Channel %s not found", cchannel)
            raise PercivalDetectorError("Cannot get value, channel {} does not exist".format(cchannel))

        return value

    def apply_sensor_dac_values(self):
        self._sensor.apply_dac_values()

    def read(self, getcmd):
        """
        Read a parameter from the detector.
        The parameters currently include:
        - list of control devices
        - list of monitor devices
        - hardware description
        - status of all monitors
        - status of a specific monitor

        :param getcmd: Name of parameter to read status of
        :type getcmd: str
        :returns: Status report of the requested getcmd
        :rtype: dict
        """
        self._log.debug("Reading data: %s", getcmd)

        # First check to see if getcmd is a keyword
        if getcmd == "driver":
            reply = {"username": self._username,
                     "start_time": self._start_time.strftime("%B %d, %Y %H:%M:%S"),
                     "up_time": str(datetime.now() - self._start_time),
                     "influx_db": self._db.get_status(),
                     "hardware": self._txrx.get_status()
                     }

        elif getcmd == "action":
            if self._active_command:
                reply = {'response': self._active_command.state,
                         'error': self._active_command.message,
                         'command': self._active_command.command_name,
                         'param_names': self._active_command.param_names,
                         'parameters': self._active_command.parameters,
                         'time': self._active_command.command_time
                         }
            else:
                reply = {'response': '',
                         'error': '',
                         'command': '',
                         'param_names': '',
                         'parameters': '',
                         'time': ''
                         }

        elif getcmd == "write_buffer":
            reply = {'data': self._write_buffer}

        elif getcmd == "read_buffer":
            reply = {'data': self._read_buffer}

        elif getcmd == "groups":
            # Construct dictionaries of control and monitor groups
            reply = {"control_groups": {"group_names": []},
                     "monitor_groups": {"group_names": []}
                     }
            ctrl_group_names = self._control_groups.group_names
            for ctrl_group in ctrl_group_names:
                reply["control_groups"]["group_names"].append(ctrl_group)
                reply["control_groups"][ctrl_group] = {
                    "description": self._control_groups.get_description(ctrl_group),
                    "channels": self._control_groups.get_channels(ctrl_group)
                }
            monitor_group_names = self._monitor_groups.group_names
            for monitor_group in monitor_group_names:
                reply["monitor_groups"]["group_names"].append(monitor_group)
                reply["monitor_groups"][monitor_group] = {
                    "description": self._monitor_groups.get_description(monitor_group),
                    "channels": self._monitor_groups.get_channels(monitor_group)
                }

        elif getcmd == "commands":
            reply = {}
            reply["commands"] = []
            for name, tmp in list(const.SystemCmd.__members__.items()):
                reply["commands"].append(name)

        # this is a misnomer as it returns the keys of the system-settings
        elif getcmd == "system_values":
            reply = {}
            reply["system_values"] = self._system_settings.settings

        elif getcmd == "setpoints":
            reply = {}
            reply["setpoints"] = []
            for name in self._setpoint_control.set_points:
                reply["setpoints"].append(name)
            reply["status"] = self._setpoint_control.get_status()
            self._log.debug("Setpoints: %s", reply)

        elif getcmd == "controls":
            reply = {}
            reply["controls"] = []
            for control in self._control_chs:
                reply["controls"].append(control)
                reply[control] = self._control_chs[control].device

        elif getcmd == "monitors":
            reply = {}
            reply["monitors"] = []
            for monitor in self._monitors:
                reply["monitors"].append(monitor)
                reply[monitor] = self._monitors[monitor].device

        elif getcmd == "boards":
            reply = {
                "boards": [const.BoardTypes.carrier.name,
                           const.BoardTypes.left.name,
                           const.BoardTypes.bottom.name,
                           const.BoardTypes.plugin.name
                          ],
                const.BoardTypes.carrier.name: {
                    "name":           self._percival_params.board_name(const.BoardTypes.carrier),
                    "type":           self._percival_params.board_type(const.BoardTypes.carrier).name,
                    "controls_count": self._percival_params.control_channels_count(const.BoardTypes.carrier),
                    "monitors_count": self._percival_params.monitoring_channels_count(const.BoardTypes.carrier)
                },
                const.BoardTypes.left.name: {
                    "name": self._percival_params.board_name(const.BoardTypes.left),
                    "type": self._percival_params.board_type(const.BoardTypes.left).name,
                    "controls_count": self._percival_params.control_channels_count(const.BoardTypes.left),
                    "monitors_count": self._percival_params.monitoring_channels_count(const.BoardTypes.left)
                },
                const.BoardTypes.bottom.name: {
                    "name": self._percival_params.board_name(const.BoardTypes.bottom),
                    "type": self._percival_params.board_type(const.BoardTypes.bottom).name,
                    "controls_count": self._percival_params.control_channels_count(const.BoardTypes.bottom),
                    "monitors_count": self._percival_params.monitoring_channels_count(const.BoardTypes.bottom)
                },
                const.BoardTypes.plugin.name: {
                    "name": self._percival_params.board_name(const.BoardTypes.plugin),
                    "type": self._percival_params.board_type(const.BoardTypes.plugin).name,
                    "controls_count": self._percival_params.control_channels_count(const.BoardTypes.plugin),
                    "monitors_count": self._percival_params.monitoring_channels_count(const.BoardTypes.plugin)
                },
            }

        elif getcmd == "status":
            reply = {'detector': self._system_status.get_status()}
            for monitor in self._monitors:
                reply[monitor] = self._monitors[monitor].status

        elif getcmd == "channel_values":
            vals = {}
            for (name, device) in self._control_chs.items():
              vals[name] = device.get_value()
            reply = { 'channel_values' : vals }

        elif getcmd == "system_settings":
            vals = self._system_settings._reg_uart.fields.as_dict();
            reply = { 'system_settings' : vals }

        elif getcmd == "clock_settings":
            vals = self._clock_settings._reg_uart.fields.as_dict();
            reply = { 'clock_settings' : vals }

        elif getcmd == "chip_readout_settings":
            vals = self._chip_readout_settings._reg_uart.fields.as_dict();
            reply = { 'chip_readout_settings' : vals }

        elif getcmd == "sensor_debug":
            reply = {'sensor_debug' : None};
            if self._percival_params.sensor_debug_params:
                reply['sensor_debug'] = self._percival_params.sensor_debug_params.value_map

        # Check to see if the getcmd is a monitoring device that we own
        elif getcmd in self._monitors:
            reply = { getcmd : self._monitors[getcmd].status }

        else:
            reply = { "error": "Parameter not found" }

        return reply

    def update_monitors(self):
        """
        Return the status of the monitor devices. Seems to take ~150ms.
        """
        self._log.debug("Update monitors callback called")
        status_msg = {}
        if self._global_monitoring:
            try:
                status_msg.update(self.update_board_status(const.BoardTypes.carrier))
                status_msg.update(self.update_board_status(const.BoardTypes.bottom))
                status_msg.update(self.update_board_status(const.BoardTypes.left))
                status_msg.update(self.update_board_status(const.BoardTypes.plugin))
            except Exception as ex:
                self._log.error("Caught exception: %s", str(ex))

            self._log.debug("Status: %s", status_msg)
        return status_msg

    def update_board_status(self, board):
        status_msg = {}
        response = self._board_values[board].read_values()
        time_now = datetime.utcnow()
        self._log.debug(response)
        read_maps = generate_register_maps(response)
        self._log.debug(read_maps)

        readback_block = BoardValueRegisters[board]
        for addr, value in response:  # pylint: disable=W0612
            offset = addr - readback_block.start_address
            name = self._percival_params.monitoring_channel_name_by_index_and_board_type(offset, board)
            if name in self._monitors:
                self._monitors[name].update(read_maps[offset])
                status_msg[name] = self._monitors[name].status
                if self._db:
                    self._db.log_point(time_now, name, self._monitors[name].status)

        return status_msg
