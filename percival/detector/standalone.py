'''
Created on 20 May 2016

@author: Alan Greer
'''
from __future__ import print_function
from future.utils import raise_with_traceback

import logging
from percival.detector.detector import PercivalDetector

from percival.detector.ipc_channel import IpcChannel
from percival.detector.ipc_message import IpcMessage
from percival.detector.ipc_reactor import IpcReactor


class PercivalStandalone(object):
    def __init__(self):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._detector = PercivalDetector()
        self._ctrl_channel = None
        self._status_channel = None
        self._reactor = IpcReactor()

    def initialise_board(self):
        self._detector.initialise_board()

    def load_channels(self):
        self._detector.load_channels()

    def setup_control_channel(self, endpoint):
        self._ctrl_channel = IpcChannel(IpcChannel.CHANNEL_TYPE_PAIR)
        self._ctrl_channel.bind(endpoint)
        self._reactor.register_channel(self._ctrl_channel, self.configure)

    def setup_status_channel(self, endpoint):
        self._status_channel = IpcChannel(IpcChannel.CHANNEL_TYPE_PUB)
        self._status_channel.bind(endpoint)

    def start_reactor(self):
        self._reactor.register_timer(100, 0, self.update_status)
        self._reactor.run()

    def update_status(self):
        status_msg = IpcMessage(IpcMessage.MSG_TYPE_NOTIFY, IpcMessage.MSG_VAL_CMD_STATUS)
        status_msg.set_param("status", self._detector.update_status())
        self._log.debug("Publishing: %s", status_msg.encode())
        self._status_channel.send(status_msg.encode())

    def configure(self, msg):
        self._log.critical("Received message on configuration channel: %s", msg)
        if msg.get_msg_type() == IpcMessage.MSG_TYPE_CMD and msg.get_msg_val() == IpcMessage.MSG_VAL_CMD_CONFIGURE:
            if msg.has_param("status_loop"):
                if msg.get_param("status_loop") == "run":
                    self._detector.set_global_monitoring(True)
                if msg.get_param("status_loop") == "stop":
                    self._detector.set_global_monitoring(False)

            if msg.has_param("list"):
                # What are we listing
                list = msg.get_param("list")
                self._log.critical("Requested list of %s", list)
                reply = self._detector.list(list)
                # Reply with the list of control devices
                reply_msg = IpcMessage(IpcMessage.MSG_TYPE_ACK, IpcMessage.MSG_VAL_CMD_CONFIGURE)
                reply_msg.set_param(list, reply)
                self._log.critical("Reply with list: %s", reply_msg.encode())
                self._ctrl_channel.send(reply_msg.encode())

            if msg.has_param("system_command"):
                self._detector.system_command(msg.get_param("system_command"))
