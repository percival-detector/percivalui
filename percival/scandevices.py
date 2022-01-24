"""
Created on 19 May 2015

@author: Ulrik Pedersen
"""


import os, time
import argparse
import numpy as np
import h5py
from collections import OrderedDict

from percival.log import log, get_exclusive_file_logger
from percival.carrier import const
from percival.carrier.registers import UARTRegister, generate_register_maps
from percival.carrier.settings import BoardSettings
from percival.carrier.txrx import TxRxContext, hexify
from percival.carrier.channels import ControlChannel
from percival.detector.detector import PercivalParameters

#log = get_exclusive_file_logger('percival-scan-devices.log')


class ReadMonitors(object):
    def __init__(self, txrx, uart_block, ini_params, board_type):
        """

        :param txrx:
        :param uart_block:
        :type: :obj:`percival.carrier.const.UARTBlock`
        """
        self._txrx = txrx
        self._uart_block = uart_block
        self._board_type = board_type
        self._uart_register_block = UARTRegister(uart_block)
        self._cmd_msg = self._uart_register_block.get_read_cmd_msg()
        self._channel_data = OrderedDict()
        self._set_channel_names(ini_params)

    def _set_channel_names(self, ini_params):
        response = self._txrx.send_recv_message(self._cmd_msg)
        self._channel_names = []
        for addr, _ in response:
            index = addr - self._uart_block.start_address
            #      addr is just a READ VALUES register address - not the channels base address.
            name = ini_params.monitoring_channel_name_by_index_and_board_type(index, self._board_type)
            self._channel_data.update({name: []})

    def read_monitors_devices(self):
        """Read all carrier monitor channels with one READ VALUES shortcut command

        Parse the resuling [(address, data), (address, data)...] array of tuples into a list of
        :class:`percival.carrier.register.ReadValueMap` objects.

        :returns: list of :class:`percival.carrier.register.ReadValueMap` objects.
        :rtype: list
        """
        response = self._txrx.send_recv_message(self._cmd_msg)
        read_maps = generate_register_maps(response)
        result = dict(list(zip(list(self._channel_data.keys()), read_maps)))
        for name, value in list(result.items()):
            self._channel_data[name].append(value)
        return result

    @property
    def channel_data(self):
        """
        Get all the recorded channel data as a (channel) dict of (field) dicts with numpy arrays:

            { "channel one": { "field_one": numpy.array([1,2,3]), "field_two": numpy.array([4,5,6])},
              "channel two": { "field_one": numpy.array([1,1,1]), "field_two": numpy.array([0,0,0])} }


        :return: dictionary of dictionaries of numpy arrays
        """
        result = {}
        for channel_name, channel_data in list(self._channel_data.items()):
            fields = channel_data[0].map_fields
            channel = {}
            for read_value_field in fields:
                num_bits = channel_data[0][read_value_field].num_bits
                dtype = np.uint8
                if num_bits > 8: dtype = np.uint16
                data = np.array([readvalue[read_value_field].value for readvalue in channel_data], dtype=dtype)
                channel.update({read_value_field: data})
            result.update({channel_name: channel})
        return result


def store_monitor_data(args, data_dict):
    """
    Store recorded ReadMonitor data to a HDF5 file.

    :param args: command line arguments supplied to the file.
    :param data_dict: dictionary of `ReadData` objects.
    :return:
    """
    filename = args.output
    with h5py.File(filename, 'w') as f:
        f.attrs["range"] = bytes(args.range)
        f.attrs["channel"] = bytes(args.channel)
        for channel_name, channel_fields in list(data_dict.items()):
            #log.debug("=========== Creating group %s ============", channel_name)
            group = f.create_group(channel_name)
            for field_name, data_array in list(channel_fields.items()):
                # log.debug("--- Writing %s data: %s ", field_name, data_array)
                group.create_dataset(field_name, data=data_array)


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range", default="0,100,20",
                        help="Scan range in integers formatted like this: start,stop,step")
    parser.add_argument("-o", "--output", action='store', help="Output HDF5 filename")
    parser.add_argument("-p", "--period", action='store', type=float, default=1.0, help="Control the loop period time")
    parser.add_argument("-s", "--status", action='store_true', default=False,
                        help="Print status report at the end of scan")
    parser.add_argument("channel", action='store', help="Control Channel to scan")
    args = parser.parse_args()

    args.range = [int(x) for x in args.range.split(',')]
    return args


def main():
    args = options()
    log.info(args)

    percival_params = PercivalParameters()
    percival_params.load_ini()
    log.debug("INI parameters: %s", percival_params)

    with TxRxContext(percival_params.carrier_ip) as trx:
        channel_ini = percival_params.control_channel_by_name(args.channel)
        log.info("ini: %s", channel_ini)

        board_type = const.BoardTypes(channel_ini.Board_type)
        bs = BoardSettings(trx, board_type)
        bs.readback_control_settings()
        cc_settings = bs.device_control_settings(channel_ini.UART_address)
        log.info("Control Channel settings from board: %s", hexify(cc_settings))

        log.debug("Creating ControlChannel object: %s, %s", channel_ini, cc_settings)
        cc = ControlChannel(trx, channel_ini, cc_settings)

        readmons = [ReadMonitors(trx, const.READ_VALUES_CARRIER, percival_params, const.BoardTypes.carrier),
                    ReadMonitors(trx, const.READ_VALUES_PERIPHERY_BOTTOM, percival_params, const.BoardTypes.bottom),
                    ReadMonitors(trx, const.READ_VALUES_PERIPHERY_LEFT, percival_params, const.BoardTypes.left),
                    ReadMonitors(trx, const.READ_VALUES_PLUGIN, percival_params, const.BoardTypes.plugin)]

        tstamp = time.time()

        # Create the list of scan points from the users range arg
        scan_range = list(range(*args.range))
        # Ensure that the last point of the range is always included in the list
        # even if the last step is not a full step size.
        if args.range[1] > scan_range[-1]:
            scan_range.append(args.range[1])

        print(" | ".join(["Demand", "ECHO value", "Sample Number", "I2C Error", "Notice"]))
        for new_value in scan_range:
            log.info("Writing Control Channel \'%s\' value = %d", args.channel, new_value)
            echo_result = cc.set_value(new_value, timeout=1.0)
            log.info("ECHO: %s", echo_result)
            comment = ""
            if echo_result.read_value != new_value:
                log.warning("  Echo result does not match demanded value (%d != %d)", echo_result.read_value, new_value)
                comment += "WARNING readback does not match demand! "
            if echo_result.i2c_communication_error:
                log.warning("  I2C communication error")
                comment += "I2C comms error!"
            print(" | ".join([str(field) for field in [new_value, echo_result.read_value, echo_result.sample_number,
                                                       echo_result.i2c_communication_error, comment]]))

            dt = time.time() - tstamp
            if args.period - dt > 0.0:
                time.sleep(args.period - dt)
                log.debug("sleeping: %f sec", args.period - dt)
            tstamp = time.time()
            adcs = {}
            [adcs.update(rm.read_monitors_devices()) for rm in readmons]
            log.info("Read carrier monitoring channels: %s", list(adcs.keys()))

        #log.info(adcs)

    if args.output:
        print("Writing recorded data to file: ", args.output)
        mon_data = {}
        [mon_data.update(rm.channel_data) for rm in readmons]
        store_monitor_data(args, mon_data)

    if args.status:
        print("\n  Error status report. Any monitoring channel with any error flag is reported here. "
              "Each status parameter is reported with a count of the number of samples where the status flag was set.")
        print(" | ".join(["Channel", 'i2c_communication_error',
                        'above_extreme_high_threshold', 'above_high_threshold',
                        'below_extreme_low_threshold', 'below_low_threshold',
                        'safety_exception_detected']))
        for ch in mon_data:
            status_list = [mon_data[ch]['i2c_communication_error'],
                          mon_data[ch]['above_extreme_high_threshold'],
                          mon_data[ch]['above_high_threshold'],
                          mon_data[ch]['below_extreme_low_threshold'],
                          mon_data[ch]['below_low_threshold'],
                          mon_data[ch]['safety_exception_detected']]

            errors = [sta.any() for sta in status_list]
            if True in errors:
                print(" | ".join([ch] + [str(len(sta.nonzero()[0])) for sta in status_list]))

if __name__ == '__main__':
    main()