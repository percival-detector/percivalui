'''
Created on 13 June 2016

@author: gnx91527
'''


import unittest, sys, logging
from mock import MagicMock
from builtins import bytes

from percival_detector.control.detector import PercivalParameters
from percival_detector.carrier import const
from percival_detector.carrier.settings import BoardSettings


class TestBoardSettings(unittest.TestCase):

    def setUp(self):
        # Perform any setup here
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(logging.DEBUG)
        self.txrx = MagicMock()
        self.parameters = PercivalParameters()
        self.parameters.load_ini()

    def TestInitialiseBoardLeft(self):
        bs = BoardSettings(self.txrx, const.BoardTypes.left)
        bs.initialise_board(self.parameters)

    def TestInitialiseBoardBottom(self):
        bs = BoardSettings(self.txrx, const.BoardTypes.bottom)
        bs.initialise_board(self.parameters)

    def TestInitialiseBoardCarrier(self):
        bs = BoardSettings(self.txrx, const.BoardTypes.carrier)
        bs.initialise_board(self.parameters)

    def TestInitialiseBoardPlugin(self):
        bs = BoardSettings(self.txrx, const.BoardTypes.plugin)
        bs.initialise_board(self.parameters)
