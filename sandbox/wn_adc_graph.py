#!/usr/bin/env python3

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

#sys.path.append("/home/ulw43618/Projects/percivalui/user_scripts/LookAtFLast");
#import APy3_GENfuns;

# we only look at frames 2..9 of the acquisition which is assumed to have >=10 frames.
g_frames_to_process = range(2,10);
# select the regions you want to graph here. see getRegionPixels().
g_regions = ["top", "middle", "bottom"];

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
    elif name=="pix4":
      top = 810;
      left=1010;
      width = 1;
      height = 1;
    else:
      print("Error: bad region",region);
      exit(1);

    for r in range(0,height):
      for c in range(0,width):
        ret.append( (top+r,left+c));

    return ret;

def save_histo2D(X,Y, nbinsX,nbinsY, label_x,label_y,label_title, filename):
    ErrBelow = 0.1;
    ''' 2D histogram plot, set to white anything < ErrBelow (e.g. 0.1)'''
    # jet is the common heatmap
    cmap = matplotlib.pyplot.cm.cool;
    if "coarse" in filename:
      cmap = matplotlib.pyplot.cm.Blues;
    cmap.set_under(color='white')    
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist2d(X,Y, bins=[nbinsX,nbinsY], cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    print("saving", filename, "with {} samples".format(len(Y)));
    matplotlib.pyplot.savefig(filename);
  #  matplotlib.pyplot.show(block=False)
    return (fig);

class Item:
  # this is just a neat way to store a dac,fine,coarse triple.
  def __init__(self, dac, fine, coarse):
    self._dac = dac;
    self._fine = fine;
    self._coarse = coarse;

# this function linearly interpolates a dac value into a voltage.
# The figure is approximate, but the main thing is that it's linear.
def dac2Voltage(dac):
    return float(dac) * 2.5 / 33000;

def options():
    desc = "Script to make a 2d histograms (dac, adc vals) of a region of pixels across several acquisitions";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-l", "--label", default="VINSCAN", help="filename label to search for (default VINSCAN)")
    parser.add_argument("-i", "--indir", default="/dls/detectors/Percival/captures", help="folder for h5 files input (default captures)")
    parser.add_argument("-o", "--outdir", default=".", help="folder for png files output (default .)")
    parser.add_argument("--maxfiles", default=100000, help="max number of h5 files to read (useful for testing)", type=int);

    parser.add_argument("--reset", default=False, action="store_true", help="look at reset-frames (default sample)");
    parser.add_argument("--region", default="", help="run on a specific region");
    parser.add_argument("--scantype", default="", help="restrict to 'crsramp' or 'fnramp' files (default none)");
  #  parser.add_argument("--vin", default=False, action="store_true", help="show approx Vin instead of Dac value", type=int);
  # does he want to see coarse / fine, sample or reset?

    parser.add_argument("--no-verbose", dest="verbose", help="verbose logging", action="store_false", default=True);

    args = parser.parse_args()
    return args;


def main():
    global g_regions;
    args = options();

    indir = "";
    if os.path.isdir(args.indir):
      indir = args.indir;
    else:
      print ("invalid in directory ", args.indir);
      exit(1);

    outdir = "";
    if os.path.isdir(args.outdir):
      outdir = args.outdir;
    else:
      print ("invalid out directory ", args.outdir);
      exit(1);

    frametype = "sample";
    if args.reset:
      frametype = "reset";

    alldacs = [];
    # get list of filenames we are going to use. os.listdir is not sorted.
    allfiles = [];
    for filename in sorted(os.listdir(indir)):
      # the emptystring is in all strings apparently
      if args.label in filename and "combined" in filename and args.scantype in filename:
        allfiles.append(filename);

    # allfiles may not be sorted by dac-value as there may be two scans in there.

    for fname in allfiles:
      mat = re.search("_(\d+)_", fname);
      if mat:
        dac = int(mat.group(1));
        alldacs.append(dac);
      else:
        print("Error: could not find dac value in ", f);
        exit(1);

    mindac = min(alldacs);
    maxdac = max(alldacs);

    if args.region:
      g_regions = [args.region];

    region2items = {};
    for region in g_regions:
      region2items[region] = [];

    count = 0;
    print("processing these files:");
    for dac, fname in zip(alldacs, allfiles):
      # open each one and extract the pixels we want to view. Close the file to save RAM.
      fileh = h5py.File(os.path.join(indir,fname), "r");

      # load the entire dataset in advance as this is faster.
      sample_dset = fileh["data" if frametype=="sample" else "reset"];
      print ("{:05d} reading {} {} {}".format(count, fname, frametype, sample_dset.shape));
      for idx in g_frames_to_process:
        for region in g_regions:
          regionpixels = getRegionPixels(region);
          for pixel in regionpixels:
            pval = sample_dset[idx, pixel[0], pixel[1]];
            gain, fine, coarse = splitGFC(pval);
            region2items[region].append(Item(dac, fine, coarse));
          
      # reset frame goes here?
      fileh.close();
      count += 1;
      if count >= args.maxfiles:
        break;

    # create histogram of the data and save it to file?
    for region in g_regions:
      items = region2items[region];
      histoX = [];
      histoC = [];
      histoF = [];
      for item in items:
        histoX.append(item._dac);
        histoC.append(item._coarse);
        histoF.append(item._fine);

      # I could put the label into the filename - is that a good idea?
      plotname = "{}_coarse_region_{}.png".format(frametype, region);
      plotname = os.path.join(outdir, plotname);
      # now save histogram!
      number_of_points_along_X = 200;
      fig = save_histo2D(histoX, histoC, number_of_points_along_X, 32,"dac setting", "Coarse ADU", "{}-frame, pixels in '{}'".format(frametype, region), plotname);

      plotname = "{}_fine_region_{}.png".format(frametype, region);
      plotname = os.path.join(outdir, plotname);

      # we need to set the width of a block in dac units, not nth of the range. So we need to know the range.
      # now save histogram!
      number_of_points_along_X = 200;
      fig = save_histo2D(histoX, histoF, number_of_points_along_X, 200, "dac setting", "Fine ADU", "{}-frame, pixels in '{}'".format(frametype, region), plotname);

   # APy3_GENfuns.show_it();

if __name__ == '__main__':
    main()






