'''
Created on 17 July 2017

@author: gnx91527
'''



import unittest, sys, logging
from mock import MagicMock, call
from builtins import bytes

import percival_detector.carrier.const as const
from percival_detector.control.command import PercivalCommandNames, Command
from percival_detector.carrier.txrx import TxMessage


class TestPercivalCommand(unittest.TestCase):

    def setUp(self):
        # Perform any setup here
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(logging.DEBUG)

    def TestCommandParsing(self):
        request = MagicMock()
        request.path = "/test"
        request.query = "item1=value1"
        request.remote_ip = "1.2.3.4"
        request.method = "PUT"
        request.headers = {
            'User': 'test_user',
            'Creation-Time': 'test_time',
            'User-Agent': 'test_user_agent'
        }
        request.body="item2=value2&item2=value3&item2=value4"
        self.command = Command(request)
        self.assertEqual(self.command.command_name, 'test')
        self.assertEqual(self.command.command_type, 'PUT')
        self.assertEqual(self.command.has_param('item1'), True)
        self.assertEqual(self.command.has_param('item2'), True)
        self.assertEqual(self.command.has_param('item3'), False)
        self.assertEqual(self.command.get_param('item1'), 'value1')
        self.assertEqual('value2' in self.command.get_param('item2'), True)
        self.assertEqual('value3' in self.command.get_param('item2'), True)
        self.assertEqual('value4' in self.command.get_param('item2'), True)
        data = self.command.format_trace
        self.assertEqual(data['Username'], 'test_user')
        self.assertEqual(data['Created'], 'test_time')
        self.assertEqual(data['Source_Address'], '1.2.3.4')
        self.assertEqual(data['Source_ID'], 'test_user_agent')

