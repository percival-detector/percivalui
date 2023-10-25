"""
Constants and enumerations for the Carrier Board firmware as defined in documentation.

Update this whenever there are any firmware/documentation changes regarding:

 * UART address space
 * Enumerations of:

  - Device families
  - Device functions
  - Device or system commands
  - Board types

 * Firmware version: :obj:`FIRMWARE_VERSION`
"""



from enum import Enum, unique

FIRMWARE_VERSION = "2018.02.05 CARRIER FULL NEW"
"""Elettra Firmware version is based on date"""


class UARTBlock(object):
    """
    Representation of a UART block of registers:

    * Start address
    * Number of elements (entries) in the block
    * Number of 32bit-words per element (entry) in the block
    """
    def __init__(self, entries, words_per_entry, start_address):
        self.entries = entries
        self.words_per_entry = words_per_entry
        self.start_address = start_address

    def is_address_valid(self, address):
        return self.start_address <= address < (self.start_address + self.words_per_entry * self.entries)

# note CONTROL_SETTINGS, MONITORING_SETTINGS are a misnomer, and should be called
#  CONTROL_CHANNELS and MONITORING_CHANNELS
HEADER_SETTINGS_LEFT = UARTBlock(1, 1, 0x0000)
CONTROL_SETTINGS_LEFT = UARTBlock(1, 4, 0x0001)
MONITORING_SETTINGS_LEFT = UARTBlock(1, 4, 0x0005)
HEADER_SETTINGS_BOTTOM = UARTBlock(1, 1, 0x0009)
CONTROL_SETTINGS_BOTTOM = UARTBlock(52, 4, 0x000A)
MONITORING_SETTINGS_BOTTOM = UARTBlock(84, 4, 0x00DA)
HEADER_SETTINGS_CARRIER = UARTBlock(1, 1, 0x022A)
CONTROL_SETTINGS_CARRIER = UARTBlock(1, 4, 0x022B)
MONITORING_SETTINGS_CARRIER = UARTBlock(4, 4, 0x022F)
HEADER_SETTINGS_PLUGIN = UARTBlock(1, 1, 0x023F)
CONTROL_SETTINGS_PLUGIN = UARTBlock(1, 4, 0x0240)
MONITORING_SETTINGS_PLUGIN = UARTBlock(1, 4, 0x0244)
CHIP_READOUT_SETTINGS = UARTBlock(1, 32, 0x0248)
CLOCK_SETTINGS = UARTBlock(1, 8, 0x0268)
SYSTEM_SETTINGS = UARTBlock(1, 18, 0x0270)
SAFETY_SETTINGS = UARTBlock(1, 8, 0x0282)
WRITE_BUFFER = UARTBlock(1, 64, 0x028A)
COMMAND = UARTBlock(1, 3, 0x02CA)
READ_VALUES_PERIPHERY_LEFT = UARTBlock(1, 1, 0x02CD)
READ_VALUES_PERIPHERY_BOTTOM = UARTBlock(84, 1, 0x02CE)
READ_VALUES_CARRIER = UARTBlock(4, 1, 0x0322)
READ_VALUES_PLUGIN = UARTBlock(1, 1, 0x0326)
READ_VALUES_STATUS = UARTBlock(1, 8, 0x0327)
READ_BUFFER = UARTBlock(1, 64, 0x032F)
READ_ECHO_WORD = UARTBlock(1, 1, 0x036F)
READBACK_HEADER_SETTINGS_LEFT = UARTBlock(1, 1, 0x0370)
READBACK_CONTROL_SETTINGS_LEFT = UARTBlock(1, 1, 0x0371)
READBACK_MONITORING_SETTINGS_LEFT = UARTBlock(1, 1, 0x0372)
READBACK_HEADER_SETTINGS_BOTTOM = UARTBlock(1, 1, 0x0373)
READBACK_CONTROL_SETTINGS_BOTTOM = UARTBlock(1, 1, 0x0374)
READBACK_MONITORING_SETTINGS_BOTTOM = UARTBlock(1, 1, 0x0375)
READBACK_HEADER_SETTINGS_CARRIER = UARTBlock(1, 1, 0x0376)
READBACK_CONTROL_SETTINGS_CARRIER = UARTBlock(1, 1, 0x0377)
READBACK_MONITORING_SETTINGS_CARRIER = UARTBlock(1, 1, 0x0378)
READBACK_HEADER_SETTINGS_PLUGIN = UARTBlock(1, 1, 0x0379)
READBACK_CONTROL_SETTINGS_PLUGIN = UARTBlock(1, 1, 0x037A)
READBACK_MONITORING_SETTINGS_PLUGIN = UARTBlock(1, 1, 0x037B)
READBACK_CHIP_READOUT_SETTINGS = UARTBlock(1, 1, 0x037C)
READBACK_CLOCK_SETTINGS = UARTBlock(1, 1, 0x037D)
READBACK_SYSTEM_SETTINGS = UARTBlock(1, 1, 0x037E)
READBACK_SAFETY_SETTINGS = UARTBlock(1, 1, 0x037F)
READBACK_WRITE_BUFFER = UARTBlock(1, 1, 0x0380)
READBACK_READ_VALUES_PERIPHERY_LEFT = UARTBlock(1, 1, 0x0381)
READBACK_READ_VALUES_PERIPHERY_BOTTOM = UARTBlock(1, 1, 0x0382)
READBACK_READ_VALUES_CARRIER = UARTBlock(1, 1, 0x0383)
READBACK_READ_VALUES_PLUGIN = UARTBlock(1, 1, 0x0384)
READBACK_READ_VALUES_STATUS = UARTBlock(1, 1, 0x0385)
READBACK_READ_BUFFER = UARTBlock(1, 1, 0x0386)
READBACK_READ_ECHO_WORD = UARTBlock(1, 1, 0x0387)



@unique
class SystemCmd(Enum):
    """Enumeration of all available system level commands

    This represents the documented "SYSTEM_CMD details"
    """
    no_operation = 0
    enable_global_monitoring = 1
    disable_global_monitoring = 2
    enable_device_level_safety_controls = 3
    disable_device_level_safety_controls = 4
    enable_system_level_safety_controls = 5
    disable_system_level_safety_controls = 6
    enable_experimental_level_safety_controls = 7
    disable_experimental_level_safety_controls = 8
    enable_safety_actions = 9
    disable_safety_actions = 10
    enter_acquisition_armed_status = 11
    exit_acquisition_armed_status = 12
    start_acquisition = 13
    stop_acquisition = 14
    forced_stop_acquisition = 15
    enable_LVDS_IOs = 16
    disable_LVDS_IOs = 17
    fast_sensor_powerup = 18
    fast_sensor_powerdown = 19
    fast_enable_control_standby = 20
    fast_disable_control_standby = 21
    enable_startup_mode = 22
    disable_startup_mode = 23
    assert_dmuxCDN = 24
    deassert_dmuxCDN = 25
    assert_sr7DIn_0 = 26
    deassert_sr7DIn_0 = 27
    assert_sr7DIn_1 = 28
    deassert_sr7DIn_1 = 29
    assert_horizDataIn_0 = 30
    deassert_horizDataIn_0 = 31
    assert_horizDataIn_1 = 32
    deassert_horizDataIn_1 = 33
    assert_sensor_PLL_Reset = 34
    deassert_sensor_PLL_Reset = 35
    assert_sensor_Master_Reset = 36
    deassert_sensor_Master_Reset = 37
    assert_mezzanine_board_A_hardware_Reset = 38
    deassert_mezzanine_board_A_hardware_Reset = 39
    assert_mezzanine_board_B_hardware_Reset = 40
    deassert_mezzanine_board_B_hardware_Reset = 41
    assert_plugin_board_hardware_Reset = 42
    deassert_plugin_board_hardware_Reset = 43
    assert_MARKER_OUT_0 = 44
    deassert_MARKER_OUT_0 = 45
    assert_MARKER_OUT_1 = 46
    deassert_MARKER_OUT_1 = 47
    assert_MARKER_OUT_2 = 48
    deassert_MARKER_OUT_2 = 49
    assert_MARKER_OUT_3 = 50
    deassert_MARKER_OUT_3 = 51
    assert_PERIPHERY_BOTTOM_IO_0 = 52
    deassert_PERIPHERY_BOTTOM_IO_0 = 53
    assert_PERIPHERY_BOTTOM_IO_1 = 54
    deassert_PERIPHERY_BOTTOM_IO_1 = 55
    assert_PERIPHERY_BOTTOM_IO_2 = 56
    deassert_PERIPHERY_BOTTOM_IO_2 = 57
    assert_PERIPHERY_BOTTOM_IO_3 = 58
    deassert_PERIPHERY_BOTTOM_IO_3 = 59
    assert_PERIPHERY_LEFT_IO_0 = 60
    deassert_PERIPHERY_LEFT_IO_0 = 61
    assert_PERIPHERY_LEFT_IO_1 = 62
    deassert_PERIPHERY_LEFT_IO_1 = 63
    assert_PERIPHERY_LEFT_IO_2 = 64
    deassert_PERIPHERY_LEFT_IO_2 = 65
    assert_PERIPHERY_LEFT_IO_3 = 66
    deassert_PERIPHERY_LEFT_IO_3 = 67
		   
		   
@unique
class BoardTypes(Enum):
    """Enumeration of the board types"

    Current list of board types:

    * `prototype`
    * `left`
    * `bottom`
    * `carrier`
    * `plugin`
    * `other`
    """
    prototype = 0
    left = 1
    bottom = 2
    carrier = 3
    plugin = 4
    other = 5


@unique
class RegisterMapType(Enum):
    header = 0
    control = 1
    monitoring = 2
    command = 3
    system = 4
    chip_readout = 5
    clock = 6


@unique
class DeviceCmd(Enum):
    """Equivalent enumeration as per the documented "Supported DEVICE_CMDs"

    Enumerated commands include:

    * `no_operation`
    * `reset`
    * `initialize`
    * `set_value`
    * `get_value`
    * `set_and_get_value`
    * `set_value_on`
    * `set_value_off`
    * `enable_standby_mode`
    * `disable_standby_mode`
    * `set_word_value`
    * `get_word_value`
    * `set_page_value`
    * `get_page_value`
    """
    no_operation = 0
    reset = 1
    initialize = 2
    set_value = 3
    get_value = 4
    set_and_get_value = 5
    set_value_on = 6
    set_value_off = 7
    enable_standby_mode = 8
    disable_standby_mode = 9
    set_word_value = 10
    get_word_value = 11
    set_page_value = 12
    get_page_value = 13


@unique
class DeviceFamily(Enum):
    """Enumeration of the available electronic component families"""
    """Digital potentiometer for control"""
    AD5242 = 0
    """Digital potentiometer for control"""
    AD5263 = 1
    """DAC for control"""
    AD5629 = 2
    """DAC for control"""
    AD5669 = 3
    """ADC for monitoring"""
    LTC2309 = 7
    """ADC for monitoring"""
    LTC2497 = 4
    """Temperature for monitoring"""
    MAX31730 = 5
    """EEPROM for on-board configuration storage"""
    AT24CM01 = 6


@unique
class DeviceFunction(Enum):
    """Equivalent enumeration as per the documented "Supported DEVICE_TYPEs"

    Enumerated functionalities include:

    * `control`
    * `monitoring`
    * `eeprom`
    * `none`
    """
    control = 0
    monitoring = 1
    eeprom = 2
    none = 3


@unique
class BufferTarget(Enum):
    """Enumeration of the BUFFER_TARGET type """
    none = 0
    mezzanine_board_A = 1
    mezzanine_board_B = 2
    both_mezzanine_boards = 3
    plugin_board = 4
    percival_sensor = 5


@unique
class BufferCmd(Enum):
    """Enumeration of buffer commands, not all accepted by all boards """
    no_operation = 0
    write = 1
    read = 2


@unique
class  SensorBufferCmd(Enum):
    """Enumeration of sensor specific buffer commands, only relevant to the sensor """
    no_operation = 0
    send_DACs_setup = 1
    send_CONFIGURATION_setup = 2
    send_CALIBRATION_setup = 3
    send_ROI_setup = 4
    send_DEBUG_setup = 5

 
BufferCommands = {
    BufferTarget.mezzanine_board_A: {
        BufferCmd.no_operation: {"command": int(0), "response": 1},
        BufferCmd.write:        {"command": int(0), "response": 2},
        BufferCmd.read:         {"command": int(1), "response": 2}
                                    },
    BufferTarget.mezzanine_board_B: {
        BufferCmd.no_operation: {"command": int(0), "response": 1},
        BufferCmd.write:        {"command": int(0), "response": 2},
        BufferCmd.read:         {"command": int(1), "response": 2}
                                    },
    BufferTarget.both_mezzanine_boards: {
        BufferCmd.no_operation: {"command": int(0), "response": 1},
        BufferCmd.write:        {"command": int(0), "response": 3}
                                    },
    BufferTarget.plugin_board: {
        BufferCmd.no_operation: {"command": int(0), "response": 1},
        BufferCmd.write:        {"command": int(0), "response": 2},
        BufferCmd.read:         {"command": int(1), "response": 2}
                               },
    BufferTarget.percival_sensor: {
        SensorBufferCmd.no_operation:             {"command": int(0), "response": 2},
        SensorBufferCmd.send_DACs_setup:          {"command": int(0), "response": 2},
        SensorBufferCmd.send_CONFIGURATION_setup: {"command": int(1), "response": 2},
        SensorBufferCmd.send_CALIBRATION_setup:   {"command": int(2), "response": 2},
        SensorBufferCmd.send_ROI_setup:           {"command": int(3), "response": 2},
        SensorBufferCmd.send_DEBUG_setup:         {"command": int(4), "response": 2}
    }
}

