import unittest;
from unittest import TestCase

import os
from percival_detector.carrier.simulator import Simulator
from percival_detector.control.detector import PercivalDetector

@unittest.skip("need to review and fix this")
class TestPercivalDetector(TestCase):
    def setUp(self):
        self.sim = Simulator()
        self.sim.start(forever=False, blocking=False)

    def tearDown(self):
        self.sim.shutdown()

    def test_load_ini(self):
        """Createing a PercivalDetector object also runs load_ini, and setup_control methods and finally load_channels"""
        pcvl = PercivalDetector(initialise_hardware=False)
        pcvl.cleanup()

    def test_initialise_board(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        pcvl.cleanup()

    def test_set_global_monitoring(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        pcvl.set_global_monitoring(True)
        pcvl.set_global_monitoring(False)
        pcvl.set_global_monitoring(False)
        pcvl.cleanup()

    def test_system_command(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        pcvl.system_command('no_operation')
        self.assertRaises(KeyError, pcvl.system_command, 'blah')
        pcvl.cleanup()

    def test_set_value(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        pcvl.set_value('VCH1', 27)
        pcvl.cleanup()

    def test_read(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        result = pcvl.read('Temperature1')
        self.assertIsInstance(result, dict)
        pcvl.cleanup()

    def test_update_status(self):
        pcvl = PercivalDetector(initialise_hardware=True)
        result = pcvl.update_status()
        self.assertIsInstance(result, dict)
        pcvl.cleanup()

