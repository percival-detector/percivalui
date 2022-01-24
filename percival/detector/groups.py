"""
Created on 24 May 2017

:author: gnx91527

A class representation for a Percival group of channels.  This class provides
the ability to set values for a group of channels with a single set command.
"""


import logging


class Group(object):
    """
    Represent a group of device channels on any of the control boards.
    """

    def __init__(self, group_ini):
        """ Channel constructor. Call this from derived classes

        Keeps a reference to the txrx communication object and initialises itself based on the parameters in channel_ini.

        :param group_ini: Channel configuration parameters from INI file
        :type  group_ini: percival.carrier.configuration.ControlGroupParameters
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._group_ini = group_ini
        self._groups = {}
        if self._group_ini:
            for section in group_ini.sections:
                self._groups[group_ini.get_name(section)] = {"description": group_ini.get_description(section)}
                self._groups[group_ini.get_name(section)]["channels"] = group_ini.get_channels(section)

    @property
    def group_names(self):
        return list(self._groups.keys())

    def get_description(self, group):
        return self._groups[group]["description"]

    def get_channels(self, group):
        return self._groups[group]["channels"]

