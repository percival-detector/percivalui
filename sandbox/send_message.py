'''
Created on 20 May 2016

@author: Alan Greer
'''


import argparse
import requests
import getpass

from percival_detector.log import log
from datetime import datetime
from percival_detector.control.ipc_channel import IpcChannel
from percival_detector.control.ipc_message import IpcMessage


def options():
    parser = argparse.ArgumentParser()
#    parser.add_argument("-w", "--write", action="store_true",
#                        help="Write the initialisation configuration to the board")
#    parser.add_argument("-o", "--output", action='store', help="Output HDF5 filename")
#    parser.add_argument("-p", "--period", action='store', type=float, default=1.0, help="Control the loop period time")
#    parser.add_argument("channel", action='store', help="Control Channel to scan")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    log.debug("Message")
#    msg = IpcMessage(IpcMessage.MSG_TYPE_CMD, IpcMessage.MSG_VAL_CMD_CONFIGURE)
#    msg.set_param("status_loop", "run")
#    msg.set_param("status_loop", "stop")
#    channel = IpcChannel(IpcChannel.CHANNEL_TYPE_PAIR)
#    channel.connect("tcp://127.0.0.1:8888")
    #time.sleep(1.0)
#    channel.send(msg.encode())


    url = "http://127.0.0.1:8888/api/0.1/percival/cmd_system_command?key=value&key2=value2"


    log.debug("Sending msg to: %s", url)
    try:
        result = requests.get(url,
                              data={
                                  'key1': 'value1',
                                  'key2': 'value2'
                              },
                              headers={
                                  'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                                  'User': getpass.getuser(),
                                  'Creation-Time': str(datetime.now()),
                                  'User-Agent': 'script_send_message'
                              }).json()
    except requests.exceptions.RequestException:
        result = {
            "error": "Exception during HTTP request, check address and Odin server instance"
        }
        log.exception(result['error'])
    return result


if __name__ == '__main__':
    main()
