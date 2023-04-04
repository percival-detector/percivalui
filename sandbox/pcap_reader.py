#!/usr/bin/env python3

# This is a helpful little script which allows you to analyze a pcap file containing a Percival
# acquisition. So catch your acquisition with tcpdump at the FR, and then this will tell you
# the number of packets, which frames they are for and whatever else you want.

import sys;
import numpy as np;
from scipy import stats;
import math;
import random;
import matplotlib.pyplot;
import time;
import threading;
import percival_detector.carrier.const;
from collections import OrderedDict;
import h5py;
import argparse;
import os;
import re;
import scapy.utils;
from scapy.utils import *;
from scapy.all import *;


def options():
    desc = "Script to check packets arriving at DAQ by reading them from a pcap file";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-f", "--file", default="", help="filename of pcap file to open")

    parser.add_argument("-c", "--count", default=False, action="store_true", help="print packet-count and exit")

    args = parser.parse_args()
    return args;

def process_pcap2(file_name):
    print('Opening {} for count'.format(file_name))
    frame_num2packet_count = {};
    count = 0

    myreader = RawPcapReader(file_name);
    for (pkt_data, pkt_metadata,) in myreader:
        count +=1;

    print("packet count: ", count);

def process_pcap(file_name):
    print('Opening {}'.format(file_name))
    frame_num2packet_count = {};
    count = 0
    """
        for (pkt_data, pkt_metadata,) in scapy.utils.RawPcapReader(file_name):
            print(dir(pkt_metadata));
            exit(0);

            count += 1
    """

    myreader = PcapReader(file_name);
    for p in myreader:
      pkt = p;
      if UDP in pkt and 1000 < pkt[UDP].len:
        payload = pkt[UDP].payload.load;
        datablock_size = int.from_bytes(payload[0:2], "big");
        frame_number = int.from_bytes(payload[4:8], "big");
        packet_number = int.from_bytes(payload[8:10], "big");
       # print(count, frame_number, packet_number);
        key = "{}".format(frame_number);

        if(key in frame_num2packet_count):
          frame_num2packet_count[key] += 1;
        else:
          frame_num2packet_count[key] = 1;
        count += 1;

    print("total packet count: ", count, " = ", count // 1696, " frames plus ", count % 1696);
    print("frame-number, packet-count");
    for (fn, ct) in frame_num2packet_count.items():
      if ct == 1696:
        print(fn,ct);
      else:
        print(fn,ct, "error");

    # print('{} contains {} packets'.format(file_name, count))

def main():

    args = options();
    if os.path.isfile(args.file):
      if args.count:
        process_pcap2(args.file);
      else:
        process_pcap(args.file);
    else:
      print("could not open ", args.file);


if __name__ == '__main__':
    main()






