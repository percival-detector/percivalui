#!/usr/bin/env python3

import sys;
import numpy;
from scipy import stats;
import math;
import random;
import matplotlib.pyplot;
import time;
import threading;
import percival.carrier.const;
from collections import OrderedDict;
import h5py;
import argparse;
import os;
import re;

#sys.path.append("/home/ulw43618/Projects/percivalui/user_scripts/LookAtFLast");
#import APy3_GENfuns;

# select the regions you want to graph here. see getRegionPixels().
g_regions = ["top", "middle", "bottom"];
g_showNaN = False;

def splitGFC(pval):
    imgGn= pval >> 13;
    imgFn= (pval >> 5) & 0xff;
    imgCrs= pval & 0x1f;

    return imgGn, imgFn, imgCrs;

def getRegionPixels(name):

    width = 3;
    height = 3;
    ret = [];

    if name=="top":
      top = 100;
      left = 1000;
    elif name=="bottom":
      top = 800;
      left = 1000;
    elif name=="middle":
      top = 1300;
      left = 1000;
    # specific pixels are often those that produce dodgy calibration coefficients
    elif name=="pix1":
      top = 800;
      left=1000;
      width = 1;
      height = 1;
    elif name=="pix2s":
      top = 1061;
      left = 908;
      width = 1;
      height = 1;
    elif name=="pix3r":
      top = 1075;
      left = 908;
      width = 1;
      height = 1;
    elif name=="half":
      top = 0;
      left = 704;
      width = 704;
      height = 1480;
    else:
      print("Error: bad region",name);
      exit(1);

    for r in range(0,height):
      for c in range(0,width):
        ret.append( (top+r,left+c));

    return ret;


def options():
    desc = "Script to Histogram some pixels across one dataset, across the whole frame if it's a 2d dataset, or across frames if it's a 3d dataset, which is assumed to be (frame, row, col)";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i", "--infile", help="filename h5 to open")
    parser.add_argument("--indir", default="/dls/detectors/Percival/captures", help="folder for h5 files input (default captures)")
    parser.add_argument("-o", "--outfile", default="foo", help="output label (default foo)")

    parser.add_argument("--region", default="half", help="run on a specific region (default half)");
    parser.add_argument("--dset", default="data", help="dataset to examine (default data)");
    parser.add_argument("--startframe", default=2, help="first frame to use", type=int);
    parser.add_argument("--endframe", default=10, help="last frame+1 to use", type=int);

    args = parser.parse_args()
    return args;


def main():
    global g_regions;
    args = options();

    filepath = args.infile;
    if(not os.path.isfile(filepath)):
      filepath = os.path.join(args.indir,args.infile);

    if not os.path.isfile(filepath):
      print ("invalid input file", filepath);
      exit(1);

    regionpixels = getRegionPixels(args.region);
    print("processing this file:", filepath);

    dset = args.dset;
    h5 = h5py.File(filepath);
    cs = numpy.asarray(h5.get(dset));

    if(cs.size <= 2):
      print("no such dset");
      exit(1);
    print("dset has shape",cs.shape);

    # we only look at frames .. of the acquisition.
    frames_to_process = range(2,10);

    if(cs.size==3):
      if (0<=args.startframe and cs.shape[2]<=args.endframe):
        frames_to_process = range(args.startframe, args.endframe-1);
      else:
        print("error in start or end frames");
        exit(1);

    matplotlib.pyplot.clf();
    allvals = [];

    if 2==len(cs.shape):
      # 2d dataset: use the only frame
        for pix in regionpixels:
          r,c = pix;
          v = cs[r,c];
          allvals.append(v);
    else:
      # 3d dataset: restrict to frames specified
      for frame in frames_to_process:
        print("doing frame", frame);
        for pix in regionpixels:
          r,c = pix;
          v = cs[frame,r,c];
          allvals.append(v);

    print("total num values: {} in range[{},{}]".format(len(allvals), min(allvals), max(allvals)) );

    #    v = cs[frame,r,c];
    #    ga,fn,cs = splitGFC(v);
    #    allvals.append(cs);

    matplotlib.pyplot.hist(allvals, 320, density=False, facecolor='g')
    matplotlib.pyplot.ylabel('qty')
    matplotlib.pyplot.title('Histogram of values')
   # matplotlib.pyplot.xlim((0,1000));
    filename = "pixelhisto-" + args.outfile + "-" + dset.replace("/","-") + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();


if __name__ == '__main__':
    main()


