"""
Created on 8 June 2017

:author: gnx91527

A class representation for a Percival command.  This class provides
an easy way to parse, query and log the command.
"""


from enum import Enum, unique
from tornado import escape

import json
import logging
from datetime import datetime


@unique
class PercivalCommandNames(Enum):
    """Enumeration of Percival pre-defined command names
    """
    cmd_connect_db = 0            # Put only
    cmd_apply_setpoint = 1        # Put only
    cmd_scan_setpoints = 2        # Put only
    cmd_system_command = 3        # Put only
    cmd_initialise_channels = 4   # Put only
    cmd_apply_sensor_dacs = 5     # Put only
    cmd_load_config = 6           # Put only
    cmd_set_channel = 7           # Put only
    cmd_update_monitors = 8       # Put only
    cmd_status = 9                # Get only
    cmd_download_channel_cfg = 10 # Put only TODO: This is a temporary command
    cmd_connect_hardware = 11     # Put only
    cmd_system_setting = 12       # Put only
    cmd_apply_roi = 13            # Put only
    cmd_abort_scan = 14           # Put only
    cmd_write_buffer = 15         # Put only
    cmd_read_buffer = 16          # Put only
    cmd_refresh_write_buffer = 17 # Put only
    cmd_refresh_read_buffer = 18  # Put only
    cmd_buffer_transfer = 19      # Put only


@unique
class CommandTrace(Enum):
    """
    Enumeration of trace keys for a Percival Command
    """
    user = 0
    creation_time = 1
    origin_address = 2
    origin_type = 3


class Command(object):
    """
    Represent a command for a percival detector control application.
    """

    def __init__(self, request):
        """ Command Object constructor.
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._command_type = None
        self._command_name = None
        self._command_active = False
        self._command_state = 'Unknown'
        self._command_message = ''
        self._parameters = {}
        self._trace = {
            CommandTrace.user: "unknown",
            CommandTrace.creation_time: str(datetime.now()),
            CommandTrace.origin_address: "unknown",
            CommandTrace.origin_type: "unknown"
        }
        if request:
            self.parse_request(request)

    @property
    def command_type(self):
        return self._command_type

    @property
    def command_name(self):
        return self._command_name

    @property
    def command_time(self):
        return self._trace[CommandTrace.creation_time]

    @property
    def active(self):
        return self._command_active

    @property
    def state(self):
        return self._command_state

    @property
    def message(self):
        return self._command_message

    @property
    def param_names(self):
        return list(self._parameters.keys())

    @property
    def parameters(self):
        parsed_params = {}
        for key in self._parameters:
            param_value = str(self._parameters[key])
            if key == 'config':
                if len(param_value) > 1024:
                    param_value = "{ too long to display }"
            parsed_params[key] = param_value
        return parsed_params

    @property
    def log_parameters(self):
        parsed_params = {}
        for key in self._parameters:
            param_value = str(self._parameters[key])
            parsed_params[key] = param_value
        return parsed_params

    @property
    def format_trace(self):
        return {'Username': self._trace[CommandTrace.user],
                'Created': self._trace[CommandTrace.creation_time],
                'Source_Address': self._trace[CommandTrace.origin_address],
                'Source_ID': self._trace[CommandTrace.origin_type]}

    def activate(self):
        self._command_active = True
        self._command_state = 'Active'

    def complete(self, success, message=''):
        if success:
            self._command_state = 'Completed'
        else:
            self._command_state = 'Failed'
        self._command_message = message

    def has_param(self, name):
        found_name = False
        if name in self._parameters:
            found_name = True
        return found_name

    def get_param(self, name):
        return self._parameters[name]

    def parse_path(self, path):
        # We might be passed a path through the HTTP API
        # The path would contain as the first value the command, followed by parameters as follows
        # /write?channel=c1&value=10.0
        tokens = path.rstrip('/').split("/")
        self._command_name = tokens[-1]
        self._log.debug("Parsed path, command [%s]", self._command_name)

    def parse_parameters(self, param_string):
        if param_string:
            params = param_string.split("&")
            for param in params:
                pv = param.split("=")
                pv[0] = pv[0].replace("[]", "")
                # Check if the parameter already exists
                if pv[0] in self._parameters:
                    # It does, so check if it is a list
                    if isinstance(self._parameters[pv[0]], list):
                        # It is a list, so append the value
                        self._parameters[pv[0]].append(pv[1])
                    else:
                        # It is not a list but it should be
                        prev_value = self._parameters[pv[0]]
                        self._parameters[pv[0]] = [prev_value, pv[1]]
                else:
                    # New parameter
                    self._parameters[pv[0]] = pv[1]

        self._log.debug("Parsed parameters for [%s]: %s", self._command_name, self._parameters)

    def parse_request(self, request):
        self._log.debug("Path: %s", request.path)
        self._log.debug("Query: %s", request.query)
        self._log.debug("Body: %s", request.body)
        # If a request object exists then it contains the method type
        self._command_type = request.method

        # Parse the command name
        self.parse_path(request.path)

        # If a request object exists then it should contain useful trace information
        # Check for the remote IP
        if request.remote_ip:
            self._trace[CommandTrace.origin_address] = request.remote_ip
        # Check for the username of the client
        if 'User' in request.headers:
            self._trace[CommandTrace.user] = request.headers['User']
        # Check for the creation time of the request
        if 'Creation-Time' in request.headers:
            self._trace[CommandTrace.creation_time] = request.headers['Creation-Time']
        # Check for the user agent (client application)
        if 'User-Agent' in request.headers:
            self._trace[CommandTrace.origin_type] = request.headers['User-Agent']

        self._log.debug("Parsed request [%s], trace: %s", self._command_type, self._trace)

        # Parse any parameters in the ?foo=bar part of the url
        if request.query:
          self.parse_parameters(request.query)

        # Check any parameters in the body (which will be in json not url-formencoded)
        # body is a bytes object.
        if request.body and request.body != b"null":
            try:
                self._parameters.update(json.loads(request.body))
            except:
                self._log.warn("could not parse http-body as json");

