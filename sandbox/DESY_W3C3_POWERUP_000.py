'''
Created on 17 May 2016

@author: gnx91527
'''


import sys
import argparse
import logging
import xlrd

from percival_detector.log import log
from percival_detector.carrier import const
from percival_detector.scripts.util import PercivalClient
from percival_detector.control.spreadsheet_parser import ControlGroupGenerator, MonitorGroupGenerator, SetpointGroupGenerator


SCRIPT_NAME = "DESY_W3C3_POWERUP_000"
CONFIG_PATH = './W3C3/config/'


def options():
    desc = """DESY Power Up Sequence
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    args = parser.parse_args()
    return args


def read_ini_file(filename):
    full_path = CONFIG_PATH + filename
    with open(full_path, 'r') as ini_file:
        ini_str = ini_file.read()
    return ini_str


def read_xls_file(type, filename):
    full_path = CONFIG_PATH + filename
    workbook = xlrd.open_workbook(full_path)
    gg = None
    if type == 'control':
        gg = ControlGroupGenerator(workbook)
    if type == 'monitor':
        gg = MonitorGroupGenerator(workbook)
    if type == 'setpoint':
        gg = SetpointGroupGenerator(workbook)
    ini_str = gg.generate_ini()
    return ini_str


def parse_response(response):
    log.info("Response: %s", response['response'])
    if response['response'] != 'Completed':
        log.info("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    args = options()
    log.setLevel(logging.INFO)
    pc = PercivalClient(args.address)

    log.info("PERCIVAL POWERUP STARTED / DESY")
    log.info("Applies to detector head with sensor Wafer 3,Chip 3")

    log.info("Downloading device settings...")
    log.info("Send download_channel_cfg command")
    parse_response(pc.send_command('cmd_download_channel_cfg', SCRIPT_NAME, wait=True))
    log.info("Send system_command [enable_global_monitoring]")
    parse_response(pc.send_system_command(const.SystemCmd['enable_global_monitoring'], SCRIPT_NAME, wait=True))

    log.info("Loading initial safe status...")
    log.info("Send configure_clock_settings command")
    parse_response(pc.send_configuration('clock_settings',
                                         read_ini_file('01_Clock_Settings/ClockSettings_N00_SAFE_START.ini'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send configure_chip_readout_settings command")
    parse_response(pc.send_configuration('chip_readout_settings',
                                         read_ini_file('02_Chip_Readout_Settings/ChipReadoutSettings_N00_SAFEstart.ini'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send configure_system_settings command")
    parse_response(pc.send_configuration('system_settings',
                                         read_ini_file('03_System_Settings/SystemSettings_N00_SAFE_START.ini'),
                                         SCRIPT_NAME,
                                         wait=True))

    log.info("Perparing powerboard...")
    log.info("Send system_command [disable_LVDS_IOs]")
    parse_response(pc.send_system_command(const.SystemCmd['disable_LVDS_IOs'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [stop_acquisition]")
    parse_response(pc.send_system_command(const.SystemCmd['stop_acquisition'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [exit_acquisition_armed_status]")
    parse_response(pc.send_system_command(const.SystemCmd['exit_acquisition_armed_status'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [fast_disable_control_standby]")
    parse_response(pc.send_system_command(const.SystemCmd['fast_disable_control_standby'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [disable_startup_mode]")
    parse_response(pc.send_system_command(const.SystemCmd['disable_startup_mode'], SCRIPT_NAME, wait=True))
    log.info("Send initialise_channels command")
    parse_response(pc.send_command('cmd_initialise_channels', SCRIPT_NAME, wait=True))
    log.info("Send system_command [fast_sensor_powerdown]")
    parse_response(pc.send_system_command(const.SystemCmd['fast_sensor_powerdown'], SCRIPT_NAME, wait=True))

    log.info("Initializing...")
    log.info("Send system_command [disable_safety_actions]")
    parse_response(pc.send_system_command(const.SystemCmd['disable_safety_actions'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [enable_device_level_safety_controls]")
    parse_response(pc.send_system_command(const.SystemCmd['enable_device_level_safety_controls'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [enable_system_level_safety_controls]")
    parse_response(pc.send_system_command(const.SystemCmd['enable_system_level_safety_controls'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [enable_experimental_level_safety_controls]")
    parse_response(pc.send_system_command(const.SystemCmd['enable_experimental_level_safety_controls'], SCRIPT_NAME, wait=True))
    log.info("Send control_groups command [05_Spreadsheets/DESY_W3C3_Group_Definitions.xls]")
    parse_response(pc.send_configuration('control_groups',
                                         read_xls_file('control', '05_Spreadsheets/DESY_W3C3_Group_Definitions.xls'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send monitor_groups command [05_Spreadsheets/DESY_W3C3_Group_Definitions.xls]")
    parse_response(pc.send_configuration('monitor_groups',
                                         read_xls_file('monitor', '05_Spreadsheets/DESY_W3C3_Group_Definitions.xls'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send setpoints command [05_Spreadsheets/DESY_W3C3_Setpoint_Definitions.xls]")
    parse_response(pc.send_configuration('setpoints',
                                         read_xls_file('setpoint', '05_Spreadsheets/DESY_W3C3_Setpoint_Definitions.xls'),
                                         SCRIPT_NAME,
                                         wait=True))

    log.info("Ramp UP Voltage Supplies and LVDS IOs...")
    log.info("Scanning [-i 00_0_0V0A -f 01_0_VDD_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['00_0_0V0A', '01_0_VDD_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Scanning [-i 01_0_VDD_ON -f 02_0_LVDS_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['01_0_VDD_ON', '02_0_LVDS_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Send system_command [enable_LVDS_IOs]")
    parse_response(pc.send_system_command(const.SystemCmd['enable_LVDS_IOs'], SCRIPT_NAME, wait=True))

    log.info("Reset sensor...")
    log.info("Send system_command [assert_sensor_Master_Reset]")
    parse_response(pc.send_system_command(const.SystemCmd['assert_sensor_Master_Reset'], SCRIPT_NAME, wait=True))
    log.info("Send system_command [deassert_sensor_Master_Reset]")
    parse_response(pc.send_system_command(const.SystemCmd['deassert_sensor_Master_Reset'], SCRIPT_NAME, wait=True))

    log.info("Ramp Up PixelVoltages...")
    log.info("Scanning [-i 02_0_LVDS_ON -f 03_0_PixelVoltages_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['02_0_LVDS_ON', '03_0_PixelVoltages_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Scanning [-i 03_0_PixelVoltages_ON -f 04_0_PixelVoltages_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['03_0_PixelVoltages_ON', '04_0_PixelVoltages_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Scanning [-i 04_0_PixelVoltages_ON -f 05_0_PixelVoltages_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['04_0_PixelVoltages_ON', '05_0_PixelVoltages_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Scanning [-i 05_0_PixelVoltages_ON -f 06_0_PixelVoltages_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['05_0_PixelVoltages_ON', '06_0_PixelVoltages_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))

    log.info("Ramp Up Voltage References...")
    log.info("Scanning [-i 06_0_PixelVoltages_ON -f 07_0_VoltageReferences_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['06_0_PixelVoltages_ON', '07_0_VoltageReferences_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))

    log.info("Ramp Up Current Biases...")
    log.info("Scanning [-i 07_0_VoltageReferences_ON -f 08_0_CurrentBiases_ON -n 4 -d 2000]")
    data = {
               'setpoints': ['07_0_VoltageReferences_ON', '08_0_CurrentBiases_ON'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))
    log.info("Scanning [-i 08_0_CurrentBiases_ON -f 08_1_CurrentBiases_ON_ready3T -n 4 -d 2000]")
    data = {
               'setpoints': ['08_0_CurrentBiases_ON', '08_1_CurrentBiases_ON_ready3T'],
               'dwell': 2000,
               'steps': 4
           }
    parse_response(pc.send_command('cmd_scan_setpoints', SCRIPT_NAME, arguments=data, wait=True))

    log.info("Additional Operations:")
    log.info("Load default operating status...")
    log.info("Send configure_clock_settings command")
    parse_response(pc.send_configuration('clock_settings',
                                         read_ini_file('01_Clock_Settings/ClockSettings_N05_120MHz.ini'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send configure_chip_readout_settings command")
    parse_response(pc.send_configuration('chip_readout_settings',
                                         read_ini_file('02_Chip_Readout_Settings/ChipReadoutSettings_N05_3T_120MHz.ini'),
                                         SCRIPT_NAME,
                                         wait=True))
    log.info("Send configure_system_settings command")
    parse_response(pc.send_configuration('system_settings',
                                         read_ini_file('03_System_Settings/SystemSettings_N05_pixel_Test.ini'),
                                         SCRIPT_NAME,
                                         wait=True))

    log.info("Enter Armed Status...")
    log.info("Send apply_roi command")
    parse_response(pc.send_command('cmd_apply_roi', SCRIPT_NAME, wait=True))
    log.info("Send system_command [enter_acquisition_armed_status]")
    parse_response(pc.send_system_command(const.SystemCmd['enter_acquisition_armed_status'], SCRIPT_NAME, wait=True))


if __name__ == '__main__':
    main()
