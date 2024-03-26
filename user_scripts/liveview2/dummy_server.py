#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import numpy as np
import h5py
import zmq
import json


def main():

  fi = h5py.File('R0005_sraw.h5', 'r')
  sraw_reset_data = fi['/P2M_FSI02_PAL/sc_raw_reset_data'][...]
  sraw_sample_data = fi['/P2M_FSI02_PAL/sc_raw_sample_data'][...]
  fi.close()

  sraw = np.concatenate((sraw_sample_data.reshape((1,10,1484,1408)), sraw_reset_data.reshape(1,10,1484,1408)))
  sraw = sraw.transpose(1,0,2,3)

  fi = h5py.File('R0005_raw.h5', 'r')
  raw_reset_data = fi['/P2M_FSI02_PAL/raw_reset_data'][...]
  raw_sample_data = fi['/P2M_FSI02_PAL/raw_sample_data'][...]
  fi.close()

  raw = np.concatenate((raw_sample_data.reshape((1,10,1484,1408)), raw_reset_data.reshape(1,10,1484,1408)))
  raw = raw.transpose(1,0,2,3)

  zctx = zmq.Context()

  sraw_sock = zctx.socket(zmq.PUB)
  sraw_sock.bind('tcp://127.0.0.1:41200')

  raw_sock = zctx.socket(zmq.PUB)
  raw_sock.bind('tcp://127.0.0.1:41300')

  nimg = sraw.shape[0]

  sraw_header = {}
  sraw_header['data_type'] = 'sraw'
  sraw_header['dtype'] = '<u2'
  sraw_header['dim1'] = sraw.shape[1] # 2
  sraw_header['dim2'] = sraw.shape[2] # 1484
  sraw_header['dim3'] = sraw.shape[3] # 1408

  raw_header = {}
  raw_header['data_type'] = 'raw'
  raw_header['dtype'] = '<u2'
  raw_header['dim1'] = raw.shape[1]
  raw_header['dim2'] = raw.shape[2] # 1484
  raw_header['dim3'] = raw.shape[3] # 1408


  frame_number = -1
  while True:
    time_ns = time.clock_gettime_ns(time.CLOCK_REALTIME)
    frame_number = (frame_number + 1) % nimg

    sraw_header['time_ns'] = time_ns
    raw_header['time_ns'] = time_ns
    sraw_header['frame_number'] = frame_number
    raw_header['frame_number'] = frame_number

    sraw_sock.send_multipart( [json.dumps(sraw_header).encode(), sraw[frame_number].tobytes()] )
    raw_sock.send_multipart( [json.dumps(raw_header).encode(), raw[frame_number].tobytes()] )

    time.sleep(1)


  sraw_sock.close()
  raw_sock.close()

  zctx.term()


if __name__ == '__main__':
  main()
