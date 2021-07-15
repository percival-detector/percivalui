"""
Created on 30 May 2017

:author: gnx91527

A class to provide set-point scanning capability for a Percival group of channels.  This class allows set-points
to be defined along with a number of steps and delay times and executes the required scan for the specified
control channels.
"""
from __future__ import print_function

from datetime import datetime
import logging
import threading
import numpy


class SetPointControl(object):
    """
    Represent a group of device channels on any of the control boards.
    """

    def __init__(self, detector):
        """ SetPointControl constructor.

        :param detector: Channel configuration parameters from INI file
        :type  detector: percival.detector.detector.PercivalDetector
        """
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._detector = detector
        self._set_point_ini = None
        # this is a lookup of strings: setpointname 2 setpointExcelName which is the key in the ini functions
        self._name2name = {}
        self._executing = False
        self._scanning = False
        self._start_scan = threading.Event()
        self._stop_scan = threading.Event()
        self._wait_for_scan_complete = threading.Event()
        self._start_time = None
        self._scan_index = 0
        self._scan_delay = 0.0
        self._scan_steps = 0
        self._thread = None
        self._dev2steps = None
        self._error = None
        self._log.info("SetPointControl object created")

    # this takes a SetpointGroupParameters object
    def load_ini(self, set_point_ini):
        if set_point_ini:
            self._log.info("Ini loaded for setpoints: %s", set_point_ini)
            self._set_point_ini = set_point_ini
            for section in self._set_point_ini.sections:
                self._name2name[self._set_point_ini.get_name(section)] = section

    def start_scan_loop(self):
        if not self._executing:
            self._start_scan.clear()
            self._stop_scan.clear()
            self._executing = True
            self._scanning = False
            self._thread = threading.Thread(target=self.scan_loop)
            self._thread.start()

    def stop_scan_loop(self):
        self._executing = False
        self._scanning = False
        self._start_scan.set()
        self._stop_scan.set()

    def abort_scan(self):
        self._scanning = False
        self._stop_scan.set()

    @property
    def set_points(self):
        return self._name2name.keys()

    def get_description(self, set_point):
        return self._set_point_ini.get_description(self._name2name[set_point])

    def apply_set_point(self, set_point, device_list=None):
        self._log.info("Apply set point called with: %s", set_point)
        self._log.info("Set point names: %s", self.set_points)
        if set_point in self.set_points:
            sps = self._set_point_ini.get_setpoints(self._name2name[set_point])
            self._log.info("Set points: %s", sps)
            # If device_list is left as default then apply all values in the set_point
            if not device_list:
                for dv in sps:
                    value = int(float(sps[dv]))
                    self._log.debug("Applying set_point [%s] = %d", dv, value)
                    self._detector.set_value(dv, value)
            elif isinstance(device_list, list):
                # Iterate through the list setting the set point
                for item in device_list:
                    if item in sps:
                        self._log.debug("Applying set_point [%s] = %d", item, sps[item])
                        self._detector.set_value(item, sps[item])
            else:
                # Single item requested, so execute the set point
                if device_list in sps:
                    self._log.debug("Applying set_point [%s] = %d", device_list, sps[device_list])
                    self._detector.set_value(device_list, sps[device_list])
        else:
            self._log.error("The set point [%s] is not available", set_point)

    def scan_set_points(self, set_points, steps, delay, device_list=None):
        # Need to create a dictionary of discrete position steps for each channel
        self._log.info("Scan setpoints: %s", str(set_points));
        dev2setpoints = {}
        for set_point in set_points:
            if set_point in self.set_points:
                sps = self._set_point_ini.get_setpoints(self._name2name[set_point])
                # If device_list is left as default then append all values in the set_point
                if not device_list:
                    for dv in sps:
                        value = int(float(sps[dv]))
                        self._log.debug("Construct scan over set_point [%s] = %d", dv, value)
                        if dv not in dev2setpoints:
                            dev2setpoints[dv] = []
                        dev2setpoints[dv].append(value)
                elif isinstance(device_list, list):
                    # Iterate through the list appending the set point
                    for item in device_list:
                        if item in sps:
                            self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                            if item not in dev2setpoints:
                                dev2setpoints[item] = []
                            dev2setpoints[item].append(sps[item])
                else:
                    # Single item requested, so append the set point
                    if device_list in sps:
                        item = device_list
                        self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                        if item not in dev2setpoints:
                            dev2setpoints[item] = []
                        dev2setpoints[item].append(sps[item])
            else:
                # Serious error, generate exception
                self._log.error("The set point [%s] is not available", set_point)
                raise ValueError("Set point is not available", set_point)
        self._log.debug("Setpoints: %s", dev2setpoints)
        # Now use the steps value to create the full scan range
        # rename this device2scanpoints
        self._dev2steps = {}
        for dv in dev2setpoints:
            self._dev2steps[dv] = numpy.empty([0], dtype=float)
            if len(dev2setpoints[dv]) < 2:
                # Serious error, generate exception
                self._log.error("Invalid set point values given, check they map the same devices")
                raise ValueError("Invalid set point values given, check they map the same devices")
            for index in range(0, len(dev2setpoints[dv])-1):
                start_value = dev2setpoints[dv][index]
                stop_value = dev2setpoints[dv][index+1]
                self._dev2steps[dv] = numpy.append(self._dev2steps[dv],
                                                     numpy.linspace(start_value, stop_value, steps, dtype=int))
        self._log.debug("Scan description: %s", self._dev2steps)
        self._scan_delay = float(delay) / 1000.0
        self._scan_steps = steps
        # Now that the set of scan points have been generated for each device notify the scan_loop
        # that we are ready to begin the scan
        # First clear the waiting flag
        self._wait_for_scan_complete.clear()
        # Set the scanning flag to True
        self._error = None
        self._scanning = True
        self._start_scan.set()

    def safety_scan_set_point(self, set_point, steps, delay, device_list=None):
        # Need to create a dictionary of discrete position steps for each channel
        self._log.info("!!! Safety scan initiated to setpoint %s !!!", set_point)
        dev2setpoints = {}
        if set_point in self.set_points:
            sps = self._set_point_ini.get_setpoints(self._name2name[set_point])
            # If device_list is left as default then append all values in the set_point
            if not device_list:
                for dv in sps:
                    value = int(float(sps[dv]))
                    self._log.info("Construct scan over set_point [%s] = %d", dv, value)
                    if dv not in dev2setpoints:
                        dev2setpoints[dv] = []
                    dev2setpoints[dv].append(value)
            elif isinstance(device_list, list):
                # Iterate through the list appending the set point
                for item in device_list:
                    if item in sps:
                        self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                        if item not in dev2setpoints:
                            dev2setpoints[item] = []
                        dev2setpoints[item].append(sps[item])
            else:
                # Single item requested, so append the set point
                if device_list in sps:
                    item = device_list
                    self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                    if item not in dev2setpoints:
                        dev2setpoints[item] = []
                    dev2setpoints[item].append(sps[item])
        else:
            # Serious error, generate exception
            self._log.error("The set point [%s] is not available", set_point)
            raise ValueError("Set point is not available", set_point)

        self._log.debug("Setpoints: %s", dev2setpoints)
        # Now use the steps value to create the full scan range
        self._dev2steps = {}
        for dv in dev2setpoints:
            self._dev2steps[dv] = numpy.empty([0], dtype=float)
            start_value = self._detector.get_value(dv)
            stop_value = dev2setpoints[dv][0]
            self._dev2steps[dv] = numpy.append(self._dev2steps[dv],
                                                 numpy.linspace(start_value, stop_value, steps, dtype=int))
        self._log.debug("Scan description: %s", self._dev2steps)
        self._scan_delay = float(delay) / 1000.0
        self._scan_steps = steps
        # Now that the set of scan points have been generated for each device notify the scan_loop
        # that we are ready to begin the scan
        # First clear the waiting flag
        self._wait_for_scan_complete.clear()
        # Set the scanning flag to True
        self._error = None
        self._scanning = True
        self._start_scan.set()

    def wait_for_scan_to_complete(self):
        while self._scanning:
            self._wait_for_scan_complete.wait(1.0)
        if self._error is not None:
            raise self._error

    def scan_loop(self):
        while self._executing:
            if not self._scanning:
                # Notify any waiting threads a scan is complete
                self._wait_for_scan_complete.set()
                # Wait for the scan event
                self._start_scan.wait()
                # Reset the scan event
                self._start_scan.clear()
                # Reset the scan index to 0
                self._scan_index = 0
                # Record the time of scan start
                self._start_time = datetime.now()

            # Main loop of set-point scan
            # Apply the current set of set-points
            if self._scanning:
                for dv in self._dev2steps:
                    try:
                        # For a scan index of greater than 0 check to see if we are being asked to scan to the
                        # same point.  If we are then do not actually send the demand
                        if self._scan_index == 0 or int(self._dev2steps[dv][self._scan_index]) != \
                                    int(self._dev2steps[dv][self._scan_index - 1]):
                            self._detector.set_value(dv, int(self._dev2steps[dv][self._scan_index]))
                    except Exception as ex:
                        # Caught an exception whilst scanning, so exit out and set error
                        self._scanning = False
                        self._error = ex

                    if not self._scanning:
                        break

                # Increment the scan index
                self._scan_index += 1
                if self._scan_index == self._scan_steps:
                    self._scanning = False

            if self._scanning:
                self._log.info("Pausing for %f seconds", self._scan_delay)
                # Wait for either a stop scan or the calculated time delay
                self._stop_scan.wait(self._scan_delay)
                self._stop_scan.clear()

        self._log.debug("Scan set-point thread exiting...")

    def get_status(self):
        status = {
            "scanning": self._scanning,
            "scan_index": self._scan_index
        }
        if self._dev2steps:
            status["scan"] = str(self._dev2steps)
        self._log.debug("Status: %s", status)
        return status
