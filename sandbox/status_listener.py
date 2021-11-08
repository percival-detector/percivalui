"""
Created on 15 June 2016

@author: Alan Greer
"""


import argparse

from percival.log import log
from percival.detector.ipc_channel import IpcChannel


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", default="tcp://127.0.0.1:8889",
                        help="Subscribe to this ZeroMQ endpoint")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    log.debug("Subscribing to channel %s", args.endpoint)
    channel = IpcChannel(IpcChannel.CHANNEL_TYPE_SUB)
    channel.connect(args.endpoint)
    channel.subscribe("")

    while True:
        raw_msg = channel.recv()
        log.debug(raw_msg)

if __name__ == '__main__':
    main()
