import unittest, logging, time
from mock import MagicMock, call
from percival_detector.control.set_point import SetPointControl


class TestSetPointControl(unittest.TestCase):
    def setUp(self):
        self._detector = MagicMock()
        self._spc = SetPointControl(self._detector)

    def test_set_point(self):
        ini = MagicMock()
        sections = ["sp1", "sp2"]
        sp_names = ["sp_name_1", "sp_name_2"]
        sp_dict = {sp_names[0]: sections[0],
                   sp_names[1]: sections[1]}
        ini.sections = sections
        ini.get_description = MagicMock(return_value="Test Desc 1")
        ini.get_setpoints = MagicMock(return_value={"device1": 1.0, "device2": 2.0, "device3": 3.0})
        ini.get_name = MagicMock()
        ini.get_name.side_effect = sp_names
        self._spc.load_ini(ini)
        self.assertEqual(self._spc.set_points, list(sp_dict.keys()))
        self.assertEqual(self._spc.get_description("sp_name_1"), "Test Desc 1")
        ini.get_description.assert_called_once_with("sp1")

        self._detector.set_value = MagicMock()
        self._spc.apply_set_point("sp_name_1")
        calls = [call("device1", 1.0), call("device2", 2.0), call("device3", 3.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)

        self._detector.set_value.reset_mock()
        self._spc.apply_set_point("sp_name_1", "device2")
        calls = [call("device2", 2.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)

        self._detector.set_value.reset_mock()
        self._spc.apply_set_point("sp_name_1", ["device2", "device3"])
        calls = [call("device2", 2.0), call("device3", 3.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)

    def test_scan_setpoints(self):
        ini = MagicMock()
        sections = ["sp1", "sp2"]
        sp_names = ["sp_name_1", "sp_name_2"]
        sp_dict = {sp_names[0]: sections[0],
                   sp_names[1]: sections[1]}
        ini.get_name = MagicMock()
        ini.get_name.side_effect = sp_names
        ini.sections = sections
        ini.get_description = MagicMock(return_value="Test Desc 1")
        ini.get_setpoints = MagicMock()
        ini.get_setpoints.side_effect = [{"device1": 1.0, "device2": 2.0, "device3": 3.0},
                                         {"device1": 10.0, "device2": 20.0, "device3": 30.0}]
        self._spc.load_ini(ini)
        self._spc.start_scan_loop()
        self._spc.scan_set_points(["sp_name_1", "sp_name_2"], 10, 100)
        # Wait for 2 seconds
        time.sleep(2.0)

        # Verify all of the set-points have been applied to all of the channels
        calls = [call("device1", 1.0),
                 call("device1", 2.0),
                 call("device1", 3.0),
                 call("device1", 4.0),
                 call("device1", 5.0),
                 call("device1", 6.0),
                 call("device1", 7.0),
                 call("device1", 8.0),
                 call("device1", 9.0),
                 call("device1", 10.0),
                 call("device2", 2.0),
                 call("device2", 4.0),
                 call("device2", 6.0),
                 call("device2", 8.0),
                 call("device2", 10.0),
                 call("device2", 12.0),
                 call("device2", 14.0),
                 call("device2", 16.0),
                 call("device2", 18.0),
                 call("device2", 20.0),
                 call("device3", 3.0),
                 call("device3", 6.0),
                 call("device3", 9.0),
                 call("device3", 12.0),
                 call("device3", 15.0),
                 call("device3", 18.0),
                 call("device3", 21.0),
                 call("device3", 24.0),
                 call("device3", 27.0),
                 call("device3", 30.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)

        # Now scan again but only with a single device
        ini.get_setpoints.side_effect = [{"device1": 1.0, "device2": 2.0, "device3": 3.0},
                                         {"device1": 10.0, "device2": 20.0, "device3": 30.0}]
        self._detector.set_value.reset_mock()

        self._spc.scan_set_points(["sp_name_1", "sp_name_2"], 10, 100, "device2")
        # Wait for 2 seconds
        time.sleep(2.0)
        # Stop the scan
        self._spc.stop_scan_loop()

        # Verify all of the set-points have been applied to all of the channels
        calls = [call("device2", 2.0),
                 call("device2", 4.0),
                 call("device2", 6.0),
                 call("device2", 8.0),
                 call("device2", 10.0),
                 call("device2", 12.0),
                 call("device2", 14.0),
                 call("device2", 16.0),
                 call("device2", 18.0),
                 call("device2", 20.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)
        # Verify no other calls were made to the Mock
        self.assertEqual(self._detector.set_value.call_count, 10)

