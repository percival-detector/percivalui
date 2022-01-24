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

# This is the first version of the ptc-code we wrote and it can do log-log graphs.
# The data-source could be updated to read the datasets var-by-row and avg-by-row instead
# of reading a text file.

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


def parseTxt2(filename):
    exptimes = [];
    varians = [];
    avgs = [];
    with open(filename) as file1:
      lines = file1.readlines();
      for line in lines:
        mat = re.search("_(\\d+)us_", line);
        if mat:
          us = int(mat.group(1));
          exptimes.append(us);
        mat = re.search("mean avg is (.*), mean var is (.*)", line);
        if mat:
          avgs.append (float(mat.group(1)));
          varians.append (float(mat.group(2)));
          
    return numpy.asarray(exptimes), numpy.asarray(avgs), numpy.asarray(varians);

def options():
    desc = "Script to plot some data from calib-mv on intensity - noise axes (aka the PTC)";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i", "--infile", help="filename of (mean, variance) data.txt fille", default="", required=True)
    parser.add_argument("-d", "--dkfile", help="filename of data from dark acquisition", default="")
 #   parser.add_argument("--indir", default="/dls/detectors/Percival/captures/ptc_scans", help="folder for h5 files input (default captures/ptc_scans)")
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
    ets1, avgs1, varians1 = parseTxt2(infile);
  #  offset = -1.0 * min(avgs1);
  #  avgs1 += offset;
    (avgs2, varians2) = (numpy.ones_like(avgs1), numpy.ones_like(avgs1));
    ets2 = numpy.copy(ets1);

    haveDk = False;
    dkfile = args.dkfile;
    if os.path.isfile(dkfile):
      print("Reading dk file:", dkfile);
      ets2, avgs2, varians2 = parseTxt2(dkfile);
      haveDk = True;
    else:
      # make up our own dark frames, which is quite helpful.
        avgs2 *= -1627;
        varians2 *= 40;
        for i in range(0,len(avgs2)):
          avgs2[i] += i*7.0/len(avgs2);
     #     varians2[i] += ;

    if(not numpy.array_equal(ets1, ets2)):
      print("times differ");
      exit(1);

    # making this bigger will a) reduce the intercept on the mean-variance graph and b) increase the slope of the loglog graph
    # c) increase the e-per-adu on the loglog graph.
    my_darkframe_correction = 40.0;
    avgs1 = (avgs1 - avgs2) + my_darkframe_correction;
   # varians1 = varians1 - varians2;

  #  need to plot avgs3 vs stddevs2;
    valid = (varians1>0);
    print("number of ok variances: ", numpy.count_nonzero(valid));

    et_per_acq = ets1[valid];
    avg_per_acq = avgs1[valid];
    var_per_acq = varians1[valid];
    std_per_acq = numpy.sqrt(varians1[valid]);

    print("avg var / intn is", numpy.average(avg_per_acq / var_per_acq) );

    log_avg_per_acq = numpy.log10(avg_per_acq);
    log_stddev_per_acq = numpy.log10(std_per_acq);


    # intensity graph
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(ets1, avgs1, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("intensity");
    matplotlib.pyplot.title("intensity");
   # matplotlib.pyplot.xlim((0,1000));
    filename = "ptc-intensity-" + args.label + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();

    # dark intensity graph
    (slope, inter, r2) = linear_fit(ets2, avgs2);
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(ets2, avgs2, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("dk intensity");
    matplotlib.pyplot.title("dk intensity");
    matplotlib.pyplot.plot([0, ets2[-1]], [inter, inter + ets2[-1] * slope], 'r-')
   # matplotlib.pyplot.xlim((0,1000));
    filename = "ptc-intensity-dk-" + args.label + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();

    # variance graph
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(et_per_acq, var_per_acq, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("variance");
    matplotlib.pyplot.title("variance"); 
   # matplotlib.pyplot.xlim((0,1000));
    filename = "ptc-variance-" + args.label + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();

    # dark variance graph
    (slope, inter, r2) = linear_fit(ets2, varians2);
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(ets2, varians2, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("dk variance");
    matplotlib.pyplot.title("dk variance");
    matplotlib.pyplot.plot([0, ets2[-1]], [inter, inter + ets2[-1] * slope], 'r-')
   # matplotlib.pyplot.xlim((0,1000));
    filename = "ptc-variance-dk-" + args.label + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();
     
    # loglog graph
    (slope, inter, r2) = linear_fit(log_avg_per_acq, log_stddev_per_acq);
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(log_avg_per_acq, log_stddev_per_acq, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel("log mean intensity")
    matplotlib.pyplot.ylabel("log std dev");
    matplotlib.pyplot.title("r2={:.2f}, slope={:.3f}, eperadu={:.2f}".format(r2, slope, (10.0**(-inter/slope))) ); 
    matplotlib.pyplot.xlim((1,4));
    matplotlib.pyplot.ylim((0,4));
    filename = "ptc-loglog-" + args.label + ".png";
    # xvalues then y values
    matplotlib.pyplot.plot([0, 4], [1, 3.0], 'g-')
    matplotlib.pyplot.plot([0, 4], [inter, inter + 4.0 * slope], 'r-')
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();

    # intensity - variance graph
    (slope, inter, r2) = linear_fit(avg_per_acq, var_per_acq);
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(numpy.append(avg_per_acq,0), numpy.append(var_per_acq, 0),  'o', fillstyle='none')
    matplotlib.pyplot.xlabel("mean intensity")
    matplotlib.pyplot.ylabel("variance");
    matplotlib.pyplot.title("r2={:.2f}, 1/slope={:.4f}, inter={:.2f}".format(r2, 1.0/slope, inter) ); 
  #  matplotlib.pyplot.xlim((1,4));
  #  matplotlib.pyplot.ylim((0,4));
    filename = "ptc-mean-var-" + args.label + ".png";
    # xvalues then y values
 #   matplotlib.pyplot.plot([0, 4], [1, 3.0], 'g-')
    matplotlib.pyplot.plot([0, 4000], [inter, inter + 4000.0 * slope], 'r-')
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();


if __name__ == '__main__':
    main()


