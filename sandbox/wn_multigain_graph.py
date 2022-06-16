#!/usr/bin/env python3

import sys;
import numpy;
from scipy import stats;
import scipy;
import math;
import matplotlib.pyplot;
import time;
import h5py;
import argparse;
import os;
import re;

#sys.path.append("/home/ulw43618/Projects/percivalui/user_scripts/LookAtFLast");
#import APy3_GENfuns;

# we only look at frames 2..9 of the acquisition which is assumed to have >=10 frames.
g_frames_to_process = range(2,5);
# select the regions you want to graph here. see getRegionPixels().
g_regions = ["top", "middle", "bottom"];
g_showNaN = False;


def linear_fit(X,Y):
    '''fit linear'''
    slopefit, interceptfit, r_val, p_val, std_err = scipy.stats.linregress(X, Y);
    return (slopefit, interceptfit, r_val**2);


def parseTxt3(filename, highgain):
    exptimes = [];
    cadu0 = [];
    cadu1 = [];
    cadu2 = [];
    qty0 = [];
    qty1 = [];
    qty2 = [];
    with open(filename) as file1:
      lines = file1.readlines();
      for line in lines:
        mat = re.search("_(\\d+)us_", line);
        if mat:
          us = int(mat.group(1));
          exptimes.append(us);
        mat = re.search("Gain(\\d) pixels:(\\d+) mean avg is (.*)", line);
        if mat:
          qty = int(mat.group(2));
          thisPixel = float(mat.group(3));

          if mat.group(1) == "0":
            cadu0.append (thisPixel);
            qty0.append(qty);
          if mat.group(1) == "1":
            cadu1.append (thisPixel);
            qty1.append(qty);
          if mat.group(1) == "2":
            cadu2.append (thisPixel);
            qty2.append(qty);

    if(highgain):
      return numpy.asarray(exptimes), numpy.asarray(qty1), numpy.asarray(cadu1), numpy.asarray(qty2), numpy.asarray(cadu2);
    else:
      return numpy.asarray(exptimes), numpy.asarray(qty0), numpy.asarray(cadu0), numpy.asarray(qty1), numpy.asarray(cadu1);

def options():
    desc = "Script to plot some data from calib-mv on x=time vs y=cadu axes";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i", "--infile", help="filename of (gain, mean) data.txt file", default="", required=True)
 #   parser.add_argument("-d", "--dkfile", help="filename of data from dark acquisition", default="")
 #   parser.add_argument("--indir", default="/dls/detectors/Percival/captures/ptc_scans", help="folder for h5 files input (default captures/ptc_scans)")
    parser.add_argument("--highgain", help="compare med with high gain (default lo with med)", action="store_true", default=False );
    parser.add_argument("-l", "--label", default="foo", help="output filename label (default foo)")

    args = parser.parse_args()
    return args;


def main():
    global g_regions;
    args = options();

    infile = args.infile;
    if not os.path.isfile(infile):
      print("Error infile:",infile);
      exit(1);

    print("Reading file:", infile);
    ets, qtyfirst, cadufirst, qtysecond, cadusec = parseTxt3(infile, args.highgain);
    maxtime = ets.max() * 1.03;

    well_behaved_selection0 = (qtyfirst > 100) & (ets < 35000);
    well_behaved_selection1 = qtysecond > 100;

    # intensity graph
    fig = matplotlib.pyplot.figure(figsize=(10,10))
    (slope0, inter0, pear0) = linear_fit(ets[well_behaved_selection0], cadufirst[well_behaved_selection0]);
    matplotlib.pyplot.plot([0, maxtime], [0, maxtime * slope0], 'r--');
    (slope1, inter1, pear1) = linear_fit(ets[well_behaved_selection1], cadusec[well_behaved_selection1]);
    matplotlib.pyplot.plot([0, maxtime], [0, maxtime * slope1], 'b--');

    cadufirst -= inter0;
    cadusec -= inter1;

    name0 = "gain0";
    name1 = "gain1";
    if(args.highgain):
      name0 = "gain1";
      name1 = "gain2";

    print("{} Pedestal: {}".format(name0, inter0));
    print("{} Pedestal: {}".format(name1, inter1));

    matplotlib.pyplot.scatter(ets, cadufirst, label=name0)
    matplotlib.pyplot.plot(ets, cadusec, 'ob', fillstyle='none', label=name1)
    matplotlib.pyplot.legend(loc='upper left')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("cadu plus a constant");
    matplotlib.pyplot.title("gain comparision: ratio is {:0.2f}".format(slope0 / slope1));
    matplotlib.pyplot.xlim((0, maxtime));
    filename = "multigain-intensity-" + args.label + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();


if __name__ == '__main__':
    main()


