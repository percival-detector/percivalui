import unittest, logging, time
from mock import MagicMock, call
from percival_detector.control.set_point import SetPointControl
from percival_detector.carrier.configuration import SetpointGroupParameters;


class TestSetPointControl(unittest.TestCase):
    def setUp(self):
        self._detector = MagicMock()
        self._spc = SetPointControl(self._detector)

    def test_apply_set_point(self):

        ini = """
        [sp1]
        Setpoint_name="sp_name_1"
        Setpoint_description="Test Desc 1"
        device1 = 1
        device2 = 2
        device3 = 3

        [sp2]
        Setpoint_name="sp_name_2"
        device1 = 10
        device2 = 20
        device3 = 30

        """;

        sg_params = SetpointGroupParameters();
        sg_params.load_ini(ini);
        self._spc.set_params(sg_params);
        self.assertEqual(sg_params.get_all_setpoints(), ["sp_name_1", "sp_name_2"]);
        self.assertEqual(sg_params.get_description("sp_name_1"), "Test Desc 1")

        self._detector.set_value = MagicMock()
        self._spc.apply_set_point("sp_name_1")
        # some confusion over type here: int or float? magicmock doesn't seem to care.
        calls = [call("device1", 1), call("device2", 2), call("device3", 3.0)]
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
        ini = """
        [sp1]
        Setpoint_name="sp_name_1"
        Setpoint_description="Test Desc 1"
        device1 = 1
        device2 = 2
        device3 = 28

        [sp2]
        Setpoint_name="sp_name_2"
        device1 = 10
        device2 = 20
        device3 = 30

        """;

        sg_params = SetpointGroupParameters();
        sg_params.load_ini(ini);
        self._spc.set_params(sg_params);

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
                 call("device3", 28.0),
                 call("device3", 28.0),
                 call("device3", 28.0),
                 call("device3", 28.0),
                 call("device3", 28.0),
                 call("device3", 29.0),
                 call("device3", 29.0),
                 call("device3", 29.0),
                 call("device3", 29.0),
                 call("device3", 30.0)]
        self._detector.set_value.assert_has_calls(calls, any_order=True)

        # Now scan again but only with a single device
        self._detector.set_value.reset_mock()

        self._spc.scan_set_points(["sp_name_1", "sp_name_2"], 10, 100, "device2")
        # Wait for 2 seconds
        time.sleep(2.0)
        # Stop the scan thread
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

