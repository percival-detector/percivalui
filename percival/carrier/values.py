"""
Created on 10 June 2016

:author: Alan Greer

A class representation for a Percival command to read the values shortcut.

An instance is initialised with a percival.carrier.txrx.TxRx object and
also the target board (const.BoardTypes).  The class can then be used to
read the values from the hardware.
"""


import logging
from percival.carrier.registers import UARTRegister, BoardValueRegisters


class BoardValues:
    """
    Represent a command to read a Percival board values shortcut.

    """
    def __init__(self, txrx, board):
        """
        Constructor

        :param txrx: Percival communication context
        :type  txrx: TxRx
        :param board: which board to read the value shortcut from
        :type  board: BoardTypes
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self._txrx = txrx
        self._board = board
        self._value_block = BoardValueRegisters[board]
        self._reg_monitoring_values = UARTRegister(self._value_block)
        self._cmd_msg = self._reg_monitoring_values.get_read_cmd_msg()

    def read_values(self):
        """Read all carrier monitor channels with one READ VALUES shortcut command

        Parse the resuling [(address, data), (address, data)...] array of tuples into a list of
        :class:`percival.carrier.register.ReadValueMap` objects.

        :returns: list of :class:`percival.carrier.register.ReadValueMap` objects.
        :rtype: list
        """
        response = self._txrx.send_recv_message(self._cmd_msg)
        return response
