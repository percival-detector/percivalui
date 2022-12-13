

import unittest

import percival_detector.carrier.const as const


class TestConstants(unittest.TestCase):
    def TestUARTBlock(self):
        # Verify a valid address
        self.assertEqual(const.HEADER_SETTINGS_LEFT.is_address_valid(0x0), True)
        # Verify an invalid address
        self.assertEqual(const.HEADER_SETTINGS_CARRIER.is_address_valid(0x0), False)
