#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Qt-version of liveview for Percival Detector

  :author based on the original version by SangYoun Park, PAL, Korea.
  :date Jan 2024
"""

import os
import sys
import time

import numpy as np
import struct
import json
import zmq
import collections
import argparse;


from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PG_ImageView import PG_ImageView2

# we can also import by using sys.path.append
from user_scripts.liveview.descrambler import descramble_to_gn_crs_fn, aggregate_to_GnCrsFn

import pyqtgraph as pg


class Communicate(QtCore.QObject):
  signal1=QtCore.pyqtSignal(object)
  signal2=QtCore.pyqtSignal(object,object)

class DataReceiver(QtCore.QThread):
  def __init__(self, sub_port, parent = None):
    QtCore.QThread.__init__(self, parent=None)
    self.transferPts=Communicate()
    self.ctx = zmq.Context.instance()
    self.receiver = None

    self.sub_port = sub_port

    self.exiting = False
    self.updating = False

    self.resetHeader = None;
    self.resetData = None;
    self.resetFrameNumber = None;

    self.dataHeader = None;
    self.dataData = None;
    self.dataFrameNumber = None;

  def __del__(self):
    self.ctx.term()
    self.exiting = True
    self.wait()

  def updateStart(self):
    if False == self.updating:
      self.updating = True
      self.start()

  def updateStop(self):
    if True == self.updating  :
      self.updating = False

  def run(self):
    self.receiver = self.ctx.socket(zmq.SUB)
    self.receiver.setsockopt(zmq.SUBSCRIBE, b'')
    self.receiver.setsockopt(zmq.RCVTIMEO, 500) # 0.5 sec
    print("zmq subscribing to", self.sub_port);
    self.receiver.connect(self.sub_port)

    while self.updating:
      try:
        rd = self.receiver.recv_multipart()
      except zmq.Again:
        continue
      except:
        print('Data Receiver Error (%s)' % (self.sub_port))
        break

      try:
        header = json.loads(rd[0])
        if 'dataset' in header.keys():
          data = np.frombuffer(rd[1], dtype=header['dtype'])
          assert(data.dtype == np.uint16);
          rows = int(header['shape'][0])
          cols = int(header['shape'][1])
          data = data.reshape( rows, cols)
          if header['dataset'] == 'reset':
            self.resetHeader = header;
            self.resetData = data;
            self.resetFrameNumber = header['frame_num'];
          if header['dataset'] == 'data':
            self.dataHeader = header
            self.dataData = data;
            self.dataFrameNumber = header['frame_num'];

        #pulse_id = header['ts'] & 0x000000000001FFFF
        #print(header)
        #print('\x1b[K\r%d' % (pulse_id), end='')
        #print('%d %d\n' % (pulse_id, pulse_id % 12), end='')

        if(self.resetFrameNumber == self.dataFrameNumber):
          self.transferPts.signal2.emit(self.dataHeader, [self.dataData, self.resetData])
        elif self.dataFrameNumber:
          self.transferPts.signal2.emit(self.dataHeader, [self.dataData, None])

      except:
        print('Data Error')
        print(header)
        raise;

    self.receiver.close()
    self.receiver = None


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parsed_args, name=None):
    super(MainWindow, self).__init__()
    self.ui=uic.loadUi('pcv_viewer.ui',self)
    self.setWindowTitle('PERCIVAL Live-Viewer2')

    self.Header = None

    self.randomDataBase = np.random.randint(0, 0x7fff, (1484, 1408), dtype=np.uint16);

    self.want_descramble = parsed_args.descramble
    self.mgv = {}

    self.data_names = ('sample_gain', 'sample_coarse', 'sample_fine', 'reset_gain', 'reset_coarse', 'reset_fine')

    mgv_uis = (self.ui.mgv_1, self.ui.mgv_2, self.ui.mgv_3, self.ui.mgv_4, self.ui.mgv_5, self.ui.mgv_6)
    mgv_range_max = (2**2 -1, 2**5 -1, 2**8 -1 , 2**2 -1, 2**5 -1, 2**8 -1)
    for mgv_name, mgv_ui, range_max in zip(self.data_names, mgv_uis, mgv_range_max):
      self.mgv[mgv_name] = PG_ImageView2(mgv_ui, invertY=True, invertX=True)
      hl = QtWidgets.QHBoxLayout(mgv_ui)
      hl.setContentsMargins(0, 0, 0, 0)
      hl.setSpacing(0)
      hl_l = QtWidgets.QGridLayout()
      hl.addLayout(hl_l)
      hl_l.setSpacing(0)
      hl_l.addWidget(self.mgv[mgv_name], 0, 0, 1, 1)

      self.randomData = self.split_raw_image([self.randomDataBase, self.randomDataBase]);
      self.mgv[mgv_name].setImage((self.randomData[mgv_name]), update_hist = True)
      self.mgv[mgv_name].setHistRange(0, range_max)

    self.DataThread = DataReceiver(parsed_args.endpoint)
    self.DataThread.transferPts.signal2.connect(self.updateData)

    self.update_flags = False
    self.update_timer = QtCore.QTimer()
    self.update_timer.timeout.connect(self.updatePlot)

    self.update_timer.start(200)
    self.DataThread.updateStart()


  def closeEvent(self, event):
    self.DataThread.updateStop()
    time.sleep(0.5)
    del self.DataThread
    #print('close event')

  """ This is indirectly called when a zmq message arrives
  """
  @QtCore.pyqtSlot(object,object)
  def updateData(self, Header, Data):
    self.Header = Header.copy()
    self.Data = Data.copy()
    str_time = None;
    if 'timestamp' in self.Header:
      tm = time.localtime(self.Header['timestamp'])
      str_time = time.strftime('%Y-%m-%d %H:%M:%S', tm)
    status_msg = '%s  fn: %u' % (str_time, self.Header['frame_num'])
    if 'ts' in self.Header:
      pulse_id = self.Header['ts'] & 0x000000000001FFFF
      status_msg = status_msg + '    TS : %ld    Pulse-ID : %d' % ( self.Header['ts'], pulse_id)
    """
    These are not odin fields
    if 'sraw'== self.Header['data_type']:
      status_msg = status_msg + '    S-RAW'
    elif 'raw' == self.Header['data_type']:
      status_msg = status_msg + '    RAW'
    else: #'calibrated' == self.Header['data_type']:
      status_msg = status_msg + '    Calibrated.'
    """
    self.ui.statusbar.showMessage(status_msg)

    self.update_flags = True

  """ this is called regularly every n ms by a QtTimer
  """
  def updatePlot(self):
    if self.update_flags:
      data = self.Data.copy()
    #  data  = [self.randomDataBase, self.randomDataBase];
      if data[1] is None:
        data[1] = self.randomDataBase;
      if self.want_descramble:
        (sgn,scrs,sfn) = descramble_to_gn_crs_fn(data[0], False, True, False)
        self.mgv['sample_gain'].setImage(sgn, update_hist = False)
        self.mgv['sample_coarse'].setImage(scrs, update_hist = False)
        self.mgv['sample_fine'].setImage(sfn, update_hist = False)
        (rgn, rcrs, rfn) = descramble_to_gn_crs_fn(data[1], False, True, False)
        self.mgv['reset_gain'].setImage(rgn, update_hist = False)
        self.mgv['reset_coarse'].setImage(rcrs, update_hist = False)
        self.mgv['reset_fine'].setImage(rfn, update_hist = False)
      else:
        raw = self.split_raw_image(data)
        for n in raw:
          self.mgv[n].setImage(raw[n], update_hist = False)

    self.update_flags = False

  def split_raw_image(self, data):
    ret = {}
    ret['sample_gain']   = np.right_shift(np.bitwise_and(data[0], 0x6000), 13)
    ret['sample_coarse'] = np.right_shift(np.bitwise_and(data[0], 0x001F),  0)
    ret['sample_fine']   = np.right_shift(np.bitwise_and(data[0], 0x1FE0),  5)
    ret['reset_gain']    = np.right_shift(np.bitwise_and(data[1], 0x6000), 13)
    ret['reset_coarse']  = np.right_shift(np.bitwise_and(data[1], 0x001F),  0)
    ret['reset_fine']    = np.right_shift(np.bitwise_and(data[1], 0x1FE0),  5)

    for key in ret:
      assert( ret.get(key).shape == (1484, 1408) );
    return ret

def process_cl_args():
  # could also use QCommandLineParser Class
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--swallow', action='store')
  parser.add_argument('-e', '--endpoint', action='store', default="tcp://127.0.0.1:5020",
      help="endpoint zmq socket to connect to (tcp://127.0.0.1:5020)")
  parser.add_argument('--descramble', default=False, dest="descramble", action="store_true",
                      help='Employ software descrambling (use PercivalProcess2Plugin)')

  parsed_args, unparsed_args = parser.parse_known_args()
  return parsed_args, unparsed_args

def main():
  parsed_args, unparsed_args = process_cl_args()

  # QApplication expects the first argument to be the program name.
  qt_args = sys.argv[:1] + unparsed_args
  app = QtWidgets.QApplication(qt_args)
  ex = MainWindow(parsed_args)
  ex.show()
  sys.exit(app.exec())

if __name__ == '__main__':
  main()

