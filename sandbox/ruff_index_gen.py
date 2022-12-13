#!/usr/bin/env python3

import sys;
import numpy;
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

#sys.path.append("/home/ulw43618/Projects/percivalui/user_scripts/LookAtFLast");
#import APy3_GENfuns;



# this function linearly interpolates a dac value into a voltage.
# The figure is approximate, but the main thing is that it's linear.
def dac2Voltage(dac):
    return float(dac) * 2.5 / 33000;


def getFilenames(indir, label, maxfiles):
    alldacs = [];
    # get list of filenames we are going to use. os.listdir is not sorted.
    allfiles = [];
    for filename in sorted(os.listdir(indir)):
      # the emptystring is in all strings apparently
      if label in filename and "combined" in filename:
        allfiles.append(filename);
      if(len(allfiles) == maxfiles):
        break;

    # allfiles may not be sorted by dac-value as there may be two scans in there!

    for fname in allfiles:
      mat = re.search("_(\d+)_", fname);
      if mat:
        dac = int(mat.group(1));
        alldacs.append(dac);
      else:
        print("oh dear could not find dac value in ", f);
        exit(1);

    return alldacs, allfiles;

def options():
    desc = "Script to create the index.dat file needed for AM's distiller.py";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-l", "--label", default="VINSCAN", help="filename label to search for (default VINSCAN)")
    parser.add_argument("-i", "--indir", default="/dls/detectors/Percival/captures", help="folder for h5 files input (default /dls/detectors/Percival/captures)")
  #  parser.add_argument("-o", "--outdir", default=".", help="folder for files output (default .)")
    parser.add_argument("-m", "--maxfiles", default=100000, help="max number of h5 files to read (useful for testing)", type=int);
    parser.add_argument("--usedac", default=False, action="store_true", help="print dac value instead of Vin");

    args = parser.parse_args()
    return args;


def main():
    args = options();

    indir = "";
    if os.path.isdir(args.indir):
      indir = args.indir;
    else:
      print ("invalid in directory ", args.indir);
      exit(1);

    alldacs, allfiles = getFilenames(indir, args.label, args.maxfiles);

 ##   with open('index.dat', 'w') as f:
    for dac, filename in zip(alldacs, allfiles):
      vin = dac2Voltage(dac);
      if args.usedac:
        print("{} {}".format(dac, filename));
      else:
        print("{} {}".format(vin, filename));


if __name__ == '__main__':
    main()






