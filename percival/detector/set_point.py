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
        self._sp_dict = {}
        self._executing = False
        self._scanning = False
        self._start_scan = threading.Event()
        self._stop_scan = threading.Event()
        self._start_time = None
        self._scan_index = 0
        self._scan_delay = 0.0
        self._scan_steps = 0
        self._thread = None
        self._scan_points = None
        self._log.info("SetPointControl object created")

    def load_ini(self, set_point_ini):
        if set_point_ini:
            self._log.info("Ini loaded for setpoints: %s", set_point_ini)
            self._set_point_ini = set_point_ini
            for section in self._set_point_ini.sections:
                self._sp_dict[self._set_point_ini.get_name(section)] = section

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

    @property
    def set_points(self):
        return self._sp_dict.keys()

    def get_description(self, set_point):
        return self._set_point_ini.get_description(self._sp_dict[set_point])

    def apply_set_point(self, set_point, device_list=None):
        self._log.info("Apply set point called with: %s", set_point)
        self._log.info("Set point names: %s", self.set_points)
        if set_point in self.set_points:
            sps = self._set_point_ini.get_setpoints(self._sp_dict[set_point])
            self._log.info("Set points: %s", sps)
            # If device_list is left as default then apply all values in the set_point
            if not device_list:
                for sp in sps:
                    value = int(float(sps[sp]))
                    self._log.info("Applying set_point [%s] = %d", sp, value)
                    self._detector.set_value(sp, value)
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
        set_point_map = {}
        for set_point in set_points:
            if set_point in self.set_points:
                sps = self._set_point_ini.get_setpoints(self._sp_dict[set_point])
                # If device_list is left as default then append all values in the set_point
                if not device_list:
                    for sp in sps:
                        value = int(float(sps[sp]))
                        self._log.info("Construct scan over set_point [%s] = %d", sp, value)
                        if sp not in set_point_map:
                            set_point_map[sp] = []
                        set_point_map[sp].append(value)
                elif isinstance(device_list, list):
                    # Iterate through the list appending the set point
                    for item in device_list:
                        if item in sps:
                            self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                            if item not in set_point_map:
                                set_point_map[item] = []
                            set_point_map[item].append(sps[item])
                else:
                    # Single item requested, so append the set point
                    if device_list in sps:
                        item = device_list
                        self._log.debug("Construct scan over set_point [%s] = %d", item, sps[item])
                        if item not in set_point_map:
                            set_point_map[item] = []
                        set_point_map[item].append(sps[item])
            else:
                # Serious error, generate exception
                self._log.error("The set point [%s] is not available", set_point)
                raise ValueError("Set point is not available", set_point)
        self._log.debug("Setpoints: %s", set_point_map)
        # Now use the steps value to create the full scan range
        self._scan_points = {}
        for sp in set_point_map:
            self._scan_points[sp] = numpy.empty([0], dtype=float)
            for index in range(0, len(set_point_map[sp])-1):
                start_value = set_point_map[sp][index]
                stop_value = set_point_map[sp][index+1]
                self._scan_points[sp] = numpy.append(self._scan_points[sp],
                                                     numpy.linspace(start_value, stop_value, steps))
        self._log.debug("Scan description: %s", self._scan_points)
        self._scan_delay = float(delay) / 1000.0
        self._scan_steps = steps
        # Now that the set of scan points have been generated for each device notify the scan_loop
        # that we are ready to begin the scan
        # Set the scanning flag to True
        self._scanning = True
        self._start_scan.set()

    def scan_loop(self):
        while self._executing:
            if not self._scanning:
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
                for sp in self._scan_points:
                    self._detector.set_value(sp, int(self._scan_points[sp][self._scan_index]))
                # Increment the scan index
                self._scan_index += 1
                if self._scan_index == self._scan_steps:
                    self._scanning = False

            if self._scanning:
                # Calculate the time delay required for the next scan point
                delta_t = datetime.now() - self._start_time
                delta_t = (self._scan_index * self._scan_delay) - delta_t.total_seconds()
                self._log.debug("Pausing for %f seconds", delta_t)
                # Wait for either a stop scan or the calculated time delay
                self._stop_scan.wait(delta_t)
                self._stop_scan.clear()

        self._log.debug("Scan set-point thread exiting...")

    def get_status(self):
        status = {
            "scanning": self._scanning,
            "scan_index": self._scan_index,
            "scan": self._scan_points
        }
        return status