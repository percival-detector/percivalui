"""
Created on 19 May 2015

@author: up45
"""


import os, time, signal
import numpy, h5py

from percival.log import log

from percival.carrier import const
from percival.carrier.registers import UARTRegister, ReadValueMap
from percival.carrier.txrx import TxRxContext

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")


class ReadDevice:
    def __init__(self):
        self.keep_running = True
        signal.signal(signal.SIGINT, self.ctrl_c_handler)

    def ctrl_c_handler(self, signal, frame):  # pylint: disable=W0613
        log.info("Caught CTRL-C")
        self.keep_running = False

    def run(self):
        log.debug("Creating comms context...")

        with TxRxContext(board_ip_address) as trx:

            cmd = UARTRegister(const.COMMAND)  # CommandMap register
            cmd.fields.parse_map([0, 0, 0]) # initialise all registers to 0

            # First generate and send a no-op system command
            cmd.fields.system_cmd = 0 # no-op system command
            cmd.fields.system_cmd_data = 0  # not used
            no_op_cmd_msg = cmd.get_write_cmd_msg(eom=True)[2]
            log.info("System no-op command: %s", str(no_op_cmd_msg))
            response = trx.send_recv_message(no_op_cmd_msg)

            cmd.fields.system_cmd = 0  # disable global monitoring
            disable_global_mon_cmd_msg = cmd.get_write_cmd_msg(eom=True)[2]
            log.info("System enable global monitoring command: %s", str(disable_global_mon_cmd_msg))
            response = trx.send_recv_message(disable_global_mon_cmd_msg)

            sample_data = []  # list of tuples: (sample, data)
            #previous_sample = 0
            while self.keep_running:
                cmd.fields.device_cmd = 0  # device no-op
                cmd.fields.device_type = 1  # device monitoring
                cmd.fields.device_index = 18  # T sensor...
                device_no_op_cmd_msg = cmd.get_write_cmd_msg(eom=True)[0]
                log.info("Device no-op command: %s", str(device_no_op_cmd_msg))
                response = trx.send_recv_message(device_no_op_cmd_msg)

                cmd.fields.device_cmd = 5 # device set and get
                log.debug("cmd map: %s", cmd.fields.generate_map())
                log.debug("       : %s", cmd.fields.mem_map)
                device_set_and_get_cmd_msg = cmd.get_write_cmd_msg(eom=True)[0]
                log.info("Device get and set command: %s", str(device_set_and_get_cmd_msg))
                response = trx.send_recv_message(device_set_and_get_cmd_msg)

                echo_word_cmd = UARTRegister(const.READ_ECHO_WORD)
                read_echo_cmd_msg = echo_word_cmd.get_read_cmd_msg()  # READ ECHO WORD
                log.info("READ ECHO WORD command: %s", str(read_echo_cmd_msg))
                response = trx.send_recv_message(read_echo_cmd_msg)
                log.info("    response: 0x%04X: 0x%08X", response[0][0], response[0][1])

                read_word = ReadValueMap()
                read_word.parse_map_from_tuples(response)
                log.info("    Sample, read value: %d, %d", read_word.sample_number, read_word.read_value)

                # In FW version 2016.04.20 the sample number does not increment. So we can't use it to discover and
                # filter out double readings and have to store every single sample instead.
                #if read_word.sample_number != previous_sample:
                if True:
                    log.info("    Appending: (%d, %d)", read_word.sample_number, read_word.read_value)
                    sample_data.append((read_word.sample_number, read_word.read_value))
                #previous_sample = read_word.sample_number
                time.sleep(0.2)

            log.debug("Got data: %s", str(sample_data))

            with h5py.File("readdevice.h5", "w") as f:
                numbers = numpy.array(list(zip(*sample_data))[0], dtype=numpy.uint8)
                f.create_dataset("sample", data=numbers)
                data = numpy.array(list(zip(*sample_data))[1], dtype=numpy.uint16)
                f.create_dataset("data", data=data)

            log.info("File written. Use one of the following commands to analyse:")
            log.info("  h5dump readdevice.h5")
            log.info("  hdfview readdevice.h5")

if __name__ == '__main__':
    rd = ReadDevice()
    rd.run()