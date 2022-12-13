import json
import datetime
from future.utils import raise_with_traceback


class IpcMessageException(Exception):

    def __init__(self, msg, errno=None):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return str(self.msg)


class IpcMessage(object):

    MSG_TYPE_ILLEGAL = -1  # Illegal message
    MSG_TYPE_CMD = 0  # Command
    MSG_TYPE_ACK = 1  # Message acknowledgement
    MSG_TYPE_NACK = 2  # Message no - acknowledgement
    MSG_TYPE_NOTIFY = 3  # Message notification

    MSG_VAL_ILLEGAL = -1  # Illegal value
    MSG_VAL_CMD_RESET = 0  # Reset command message
    MSG_VAL_CMD_STATUS = 1  # Status command message
    MSG_VAL_NOTIFY_FRAME_READY = 2  # Frame ready notification message
    MSG_VAL_NOTIFY_FRAME_RELEASE = 3  # Frame release notification message
    MSG_VAL_CMD_CONFIGURE = 4  # Configure command message

    def __init__(self, msg_type=None, msg_val=None, from_str=None):

        self.attrs = {}

        if from_str is None:
            self.attrs['msg_type'] = msg_type
            self.attrs['msg_val']  = msg_val
            self.attrs['timestamp'] = datetime.datetime.now().isoformat()
            self.attrs['params'] = {}

        else:
            try:
                self.attrs = json.loads(from_str)
            except ValueError as e:
                raise IpcMessageException("Illegal message JSON format")

    def is_valid(self):

        is_valid = True

        try:
            is_valid = is_valid & (self._get_attr('msg_type') is not None)
            is_valid = is_valid & (self._get_attr("msg_val") is not None)
            is_valid = is_valid & (self._get_attr("timestamp") is not None)

        except IpcMessageException:
            is_valid = False

        return is_valid

    def get_msg_type(self):

        return self.attrs['msg_type']

    def get_msg_val(self):

        return self.attrs['msg_val']

    def get_msg_timestamp(self):

        return self.attrs['timestamp']

    def has_param(self, param_name):
        return_val = True
        if 'params' not in self.attrs:
            return_val = False
        elif param_name not in self.attrs['params']:
            return_val = False
        return return_val

    def get_param(self, param_name, default_value=None):

        try:
            param_value = self.attrs['params'][param_name]

        except KeyError:
            if default_value is None:
                raise_with_traceback(IpcMessageException("Missing parameter " + param_name))
            else:
                param_value = default_value

        return param_value

    def set_msg_type(self, msg_type):

        self.attrs['msg_type'] = msg_type

    def set_msg_val(self, msg_val):

        self.attrs['msg_val'] = msg_val

    def set_param(self, param_name, param_value):

        if 'params' not in self.attrs:
            self.attrs['params'] = {}

        self.attrs['params'][param_name] = param_value

    def encode(self):

        return json.dumps(self.attrs)

    def __eq__(self, other):

        return self.attrs == other.attrs

    def __ne__(self, other):

        return self.attrs != other.attrs

    def __str__(self):

        return json.dumps(self.attrs, sort_keys=True, indent=4, separators=(',', ': '))

    def _get_attr(self, attr_name, default_value=None):

        try:
            attr_value = self.attrs[attr_name]

        except KeyError:
            if default_value is None:
                raise_with_traceback(IpcMessageException("Missing attribute " + attr_name))
            else:
                attr_value = default_value

        return attr_value
