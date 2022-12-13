# more tests for configuration
# by wnichols

import unittest;
import os
from percival_detector.carrier.configuration import find_file, ChannelParameters, BoardParameters, ControlParameters,\
    SensorConfigurationParameters, SensorCalibrationParameters, SensorDebugParameters
from percival_detector.carrier.const import BoardTypes
import percival_detector.carrier.configuration;


class TestSetpointGroupParameters(unittest.TestCase):

  def test_basic_retrieval(self):
      sgp = percival_detector.carrier.configuration.SetpointGroupParameters();
      ini1 = "[s<1>]\nSetpoint_name=setp1\nSetpoint_description=desc\na=1";
      ini2 = "[s<2>]\nSetpoint_name=setp2\nSetpoint_description=desc\na=3";

      sgp.load_ini(ini1);
      sgp.load_ini(ini2);

      self.assertEqual(len(sgp.get_all_setpoints()),2);
      self.assertEqual(sgp.get_setpoint("setp1").get("a"), "1");
      self.assertEqual(sgp.get_setpoint("setp2").get("a"), "3");

      sgp.clear_ini();
      self.assertEqual(len(sgp.get_all_setpoints()),0);

  def test_basic_replacement(self):
      sgp = percival_detector.carrier.configuration.SetpointGroupParameters();
      ini1 = "[s<1>]\nSetpoint_name=setp1\nSetpoint_description=desc\na=1";
      ini2 = "[s<1>]\nSetpoint_name=setp1\nSetpoint_description=desc\na=3";

      sgp.load_ini(ini1);
      sgp.load_ini(ini2);

      self.assertEqual(len(sgp.get_all_setpoints()),1);
      self.assertEqual(sgp.get_setpoint("setp1").get("a"), "3");


if __name__ == '__main__':
  unittest.main()
