"""
The detector interface module contains a number of abstract interface definitions
which are to be implemented by classes that support control and communication
with detectors.

The interface classes do not implement any real functionality, but are used to define
the methods (and their args) and properties, required to support a certain
interface.

The interface classes rely on the python :mod:`abc` module to support Abstract Base
Classes
"""

from future.utils import with_metaclass
import logging

import abc
from inspect import ismethod, getargspec
from . import parameter

logger = logging.getLogger(__name__)


class IABCMeta(object):
    """
    Abstract Base Meta Class which implements checking for required methods and
    properties, even when the class is not directly subclassed.
    The Interface class which uses this metaclass will need to define a property
    called :py:attr:`_iface_requirements` which is a list of properties that must be implemented.

    This class is intended to work together with the :py:class:`abc.ABCMeta` class:
    Subclass :class:`IABCMeta` into your own class and set the :py:const:`__metaclass__` = :py:class:`abc.ABCMeta`
    The :py:meth:`__subclasshook__` will automatically be called when a class
    interface need to be verified.
    """
    
    _iface_requirements = []
    '''Interface requirements list. The members listed here must be implemented
       by subclasses'''
    
    @classmethod
    def __subclasshook__(cls, C):
        """Iterate through the :py:attr:`_iface_requirements` list of members and check
        whether they are implemented by the current class or parent.

        For requirement functions:
        Check if the functions arguments match the required arguments
        of the interface function.

        Rules for implementation of interface functions:
            1) Must have at least the main (non-defaulted) named args
            2) Can extend the list of arguments

        Default value arguments are discouraged in interfaces as the
        interface does not implement any functionality. Implementations
        can assign default values to the arguments if desired.
        """
        if not cls._iface_requirements:
            return NotImplemented
        
        checks = []
        for req in cls._iface_requirements:
            has_req = any(req in B.__dict__ for B in C.__mro__)
            result = has_req
            if has_req:
                if ismethod(getattr(cls, req)):
                    # Check if the functions arguments match the required arguments
                    interface_func_args = getargspec( getattr(cls, req) ).args
                    impl_func_args = getargspec(getattr(C,req)).args
                    try:
                        result = interface_func_args == impl_func_args[:len(interface_func_args)]
                    except IndexError:
                        result = False
            checks.append(result)
        return False not in checks


class IDetector(with_metaclass(abc.ABCMeta, IABCMeta)):
    """
    Abstract Interface to a detector class
    """
    #__metaclass__ = abc.ABCMeta
    __iproperties__ = ['exposure']
    __imethods__ = ['acquire']
    _iface_requirements = __imethods__ + __iproperties__
    
    @property
    def exposure(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def acquire(self, exposure, nframes):
        '''
        Start the detector acquiring data
        '''
        raise NotImplementedError


class IParameter(with_metaclass(abc.ABCMeta, object)):
    """Base class interface to describe a detector parameter

    The :obj:`value` object is a :class:`detector.parameter.Observable` instance
    to which callbacks can be registerred to provide notification updates
    """
    #__metaclass__ = abc.ABCMeta
    value = parameter.Observable('value')
    

class IControl(with_metaclass(abc.ABCMeta, IABCMeta)):
    #__metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def start_acquisition(self, exposure, nframes):
        raise NotImplementedError
    
    @abc.abstractmethod
    def stop_acquisition(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_nframes(self):
        raise NotImplementedError


class IData(with_metaclass(abc.ABCMeta, IABCMeta)):
    #__metaclass__ = abc.ABCMeta
    
    def get_filename(self):
        return self.filename

    def set_filename(self, fname):
        self.filename = fname
    filename = abc.abstractproperty(get_filename, set_filename)
    
    def get_datasetname(self):
        return self.datasetname

    def set_datasetname(self, value):
        self.datasetname = value
    datasetname = abc.abstractproperty(get_datasetname, set_datasetname)
    
    @abc.abstractmethod
    def start_capture(self, filename, nframes):
        '''
        Start capturing data frames into a filename.
        
        :param filename: Name of file to capture and store frames in.
        :param nframes: Numbef of frames, expected to be acquired and stored.
        '''
        raise NotImplementedError
    
    @abc.abstractmethod
    def wait_complete(self, timeout):
        """
        Wait and return once the current capture session has completed.
        This function will return when the required number of frames has been captured
        into the file - or throw Timeout exception after a timeout.

        :param timeout: Number of seconds to block before timing out.
        """
        raise NotImplementedError
