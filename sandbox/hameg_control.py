'''
Created on 25 Jan 2018

@author: gnx91527

Script for controlling the HAMEG power supply
'''

import time
import argparse
import socket

def options():
    desc = """Control of a HAMEG power supply"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="172.23.240.91:5025",
                        help="IP address of the power supply (default 172.23.240.91:5025)")
    power_up_help = "Power up the supply voltages"
    parser.add_argument("-u", "--power_up", action="store_true", help=power_up_help)
    power_down_help = "Power down the supply voltages"
    parser.add_argument("-d", "--power_down", action="store_true", help=power_down_help)
    read_status_help = "Read the current status of the supply"
    parser.add_argument("-s", "--status", action="store_true", help=read_status_help)
    args = parser.parse_args()
    return args


class HamegPowerSupply(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint
        address = endpoint.split(':')
        self._ps_ip_address = address[0]
        self._ps_port = int(address[1])
        self._client_sock = None

    def connect(self):
        self._client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_sock.settimeout(2.0)
        self._client_sock.connect((self._ps_ip_address, self._ps_port))

    def disconnect(self):
        self._client_sock.close()

    def beep(self):
        self.write('SYST:BEEP')

    def turn_channel_on(self, channel):
        self.write('INST:SEL OUTPut{}'.format(channel))
        self.write('OUTP:SEL ON')

    def turn_channel_off(self, channel):
        self.write('INST:SEL OUTPut{}'.format(channel))
        self.write('OUTP:SEL OFF')

    def set_channel_volts(self, channel, volts):
        self.write('INST:SEL OUTPut{}'.format(channel))
        self.write('SOUR:VOLT:LEV {}'.format(volts))

    def set_channel_current(self, channel, current):
        self.write('INST:SEL OUTPut{}'.format(channel))
        self.write('SOUR:CURR:LEV {}'.format(current))

    def write(self, msg):
        print("Sending message: ", msg)
        self._client_sock.send(msg + '\r\n')

    def write_read(self, msg):
        print("Sending message: ", msg)
        self._client_sock.send(msg + '\r\n')
        try:
            response = self._client_sock.recv(2048)
        except:
            self._client_sock.close()
            raise
        print("Got response (%d bytes): " % len(response), [response])
        return response


def main():
    args = options()

    ps = HamegPowerSupply(args.address)
    ps.connect()
    ps.beep()
    ps.write_read('*IDN?')

    if args.power_up:
        ps.set_channel_volts(1, 5.0)
        time.sleep(0.5)
        ps.set_channel_current(1, 0.5)
        time.sleep(0.5)
        ps.turn_channel_on(1)
        time.sleep(2.0)
        ps.set_channel_volts(2, 3.3)
        time.sleep(0.5)
        ps.set_channel_current(2, 0.1)
        time.sleep(0.5)
        ps.turn_channel_on(2)
        time.sleep(2.0)
        ps.set_channel_volts(3, 8.0)
        time.sleep(0.5)
        ps.set_channel_current(3, 0.3)
        time.sleep(0.5)
        ps.set_channel_volts(4, -8.0)
        time.sleep(0.5)
        ps.set_channel_current(4, 0.4)
        time.sleep(0.5)
        ps.turn_channel_on(3)
        ps.turn_channel_on(4)

    if args.power_down:
        ps.turn_channel_off(3)
        ps.turn_channel_off(4)
        time.sleep(0.5)
        ps.set_channel_volts(3, 0.0)
        time.sleep(0.5)
        ps.set_channel_current(3, 0.0)
        time.sleep(0.5)
        ps.set_channel_volts(4, 0.0)
        time.sleep(0.5)
        ps.set_channel_current(4, 0.0)
        time.sleep(0.5)
        ps.turn_channel_off(2)
        time.sleep(0.0)
        ps.set_channel_volts(2, 0.0)
        time.sleep(0.5)
        ps.set_channel_current(2, 0.0)
        time.sleep(0.5)
        ps.turn_channel_off(1)
        time.sleep(0.0)
        ps.set_channel_volts(1, 0.0)
        time.sleep(0.5)
        ps.set_channel_current(1, 0.0)


    ps.beep()
    time.sleep(0.5)
    ps.beep()
    ps.disconnect()


if __name__ == '__main__':
    main()

