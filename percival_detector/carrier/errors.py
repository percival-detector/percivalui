"""
Percival detector errors and exceptions
"""


class PercivalCommsError(Exception):
    pass


class PercivalProtocolError(Exception):
    pass


class PercivalControlDeviceError(Exception):
    pass


class PercivalSystemCommandError(Exception):
    pass
