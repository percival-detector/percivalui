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

rows = 1484;
cols = 1440;

def linear_fit(X,Y):
    '''fit linear'''
    slopefit, interceptfit, r_val, p_val, std_err = scipy.stats.linregress(X, Y);
    return (slopefit, interceptfit, r_val**2);

class Acquisition:

  def  __init__(self, us, lightfile):
    self._us = us;
    self._lightfile = lightfile;
    pass;

  def setExposureTime(self, us):
    self._us = us;
  
  def setLightFile(self,lightfile):
    self._lightfile = lightfile;

  def validate(self):
    try:
      self.hlightfile = h5py.File(self._lightfile, "r");
      self.light_avg = numpy.asarray(self.hlightfile["avg"]);
      self.light_var = numpy.asarray(self.hlightfile["var"]);
      self.light_avg_by_row = numpy.asarray(self.hlightfile["avg_by_row"]);
      self.light_var_by_row = numpy.asarray(self.hlightfile["var_by_row"]);
      self.hlightfile.close();
    except:
      return False;

    return True;

  def getExposureTime(self):
    return self._us;

  def getAvg(self, row, col):
    return self.light_avg[row, col];

  def getRowAvg(self, row):
    row = row % 7;
    return self.light_avg_by_row[0, row];

  def getAvgGlobal(self):
    tot = 0.0;
    for i in range(0,7):
      tot += self.getRowAvg(i);

    return tot / 7;

# this takes:
# filename: label in the graph file to save
# ets: array of exposure times
# cadu: a combined-adu for each exposure time
# name: a name for these points
def drawGraph(filename, ets, cadu, extra_x, extra_y, name):
    ets = numpy.asarray(ets);
    maxtime = max(extra_x, ets.max()) * 1.03;
    fig = matplotlib.pyplot.figure(figsize=(10,10))

    (slope1, inter1, rsq1) = linear_fit(ets, cadu);
    matplotlib.pyplot.plot([0, maxtime], [inter1, inter1 + maxtime * slope1], 'r--');

    matplotlib.pyplot.scatter(ets, cadu, label=name, c="blue");
    if(extra_x):
      matplotlib.pyplot.scatter(extra_x, extra_y, marker='+', label="extra acquisition", c="green" )
      
 #   matplotlib.pyplot.plot(ets, cadusec, 'ob', fillstyle='none', label=name1)
    matplotlib.pyplot.legend(loc='upper left')
    matplotlib.pyplot.xlabel("us exposure time")
    matplotlib.pyplot.ylabel("cadu");
 #   matplotlib.pyplot.title("gain comparision: ratio is {:0.2f}".format(slope0 / slope1));
    matplotlib.pyplot.xlim((0, maxtime));
    filename = "graph-time-intensity-" + filename + ".png";
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();

def saveCoefficients(set1, set2, acq3, outfile):

    resultsG = numpy.zeros((rows,cols)) * numpy.nan;
    resultsPedHI = numpy.zeros((rows,cols)) * numpy.nan;
    resultsPedMED = numpy.zeros((rows,cols)) * numpy.nan;

    for r in range(0,rows):
      for c in range(32+704,cols):
        ets1 = [];
        cadu1 = [];
        ets2 = [];
        cadu2 = [];
        for acq in set1:
          ets1.append(acq.getExposureTime());
          cadu1.append(acq.getAvg(r,c));

        for acq in set2:
          ets2.append(acq.getExposureTime());
          cadu2.append(acq.getAvg(r,c));

        (slope1, inter1, rsq1) = linear_fit(ets1, cadu1);
        (slope2, inter2, rsq2) = linear_fit(ets2, cadu2);
        
        # test for bad data
        if slope1 == 0 or slope2 == 0 or rsq1 < 0.5 or rsq2 < 0.5:
          print("bad data at ",r,c);
          resultsG[r,c] = numpy.nan;
          resultsPedHI[r,c] = numpy.nan;
          resultsPedMED[r,c] = numpy.nan;
        else:
          x = acq3.getExposureTime();
          y = acq3.getAvg(r,c);
          x2 = (y - inter1) / slope1;
          phi = x2 / x;
          res = slope1 * phi / slope2;

          if r==600 and c==818:
            print(" pixel at",r,c);
            print(" equivalent exposure time of point3 in lower-light is:{:.2f}us which is {:.1f}x more".format(x2, phi));
            print(" slope1 low light: {:.10f} slope2 med light: {:.10f}".format(slope1, slope2));
            print(" gain difference is: {:.10f}".format(res));
            drawGraph("acq1", ets1, cadu1, x2, y, "set1r{}c{}".format(r,c));
            drawGraph("acq2", ets2, cadu2, x, y, "set2r{}c{}".format(r,c));

          resultsG[r,c] = res;
          resultsPedHI[r,c] = inter1;
          resultsPedMED[r,c] = inter2;

    print ("saving", outfile);
    h = h5py.File(outfile, "w");
    h.create_dataset("gain", data=resultsG);
    h.create_dataset("pedestal0", data=resultsPedHI);
    h.create_dataset("pedestal1", data=resultsPedMED);
    h.close();

def options():
    desc = "Script to plot some data from calib-mv on x=time vs y=cadu axes, but actually it calculates e_per_adu on a pixelwise basis";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-d", "--indir", help="directory of _mv.h5 files", default="", required=True)
    parser.add_argument("-o", "--outfile", help="filename of output file (default latgain_output.h5)", default="latgain_output.h5")
 #   parser.add_argument("--indir", default="/dls/detectors/Percival/captures/ptc_scans", help="folder for h5 files input (default captures/ptc_scans)")
 #   parser.add_argument("--highgain", help="compare med with high gain (default lo with med)", action="store_true", default=False );
    parser.add_argument("--label1", default="GAINHI", help="input filename label for hi-gain acquisition")
    parser.add_argument("--label2", default="GAINMED", help="input filename label for medium-gain acquisition")
    parser.add_argument("--label3", default="CAPHI", help="input filename label for special point")
    parser.add_argument("--dry", default=False, help="just print filenames and stop", action="store_true")

    args = parser.parse_args()
    return args;


def main():
    global g_regions;
    args = options();

    indir = args.indir;
    if not os.path.isdir(indir):
      print("Error input dir:",indir);
      exit(1);

    allfiles = sorted(os.listdir(indir));

    set1 = [];
    set2 = [];
    acq3 = None;
    for fil in allfiles:
      us = 0;
      mat = re.search("_(\d+)us_", fil);
      if mat:
        us = int(mat.group(1));
      fil = os.path.join(indir, fil);
      if os.path.isfile(fil) and "_mv.h5" in fil:
        if us == 0:
          print("Error: could not find us value in ", fil);
          exit(1);

        if args.label1 in fil:
          set1.append(Acquisition(us, fil));
        if args.label2 in fil:
          set2.append(Acquisition(us, fil));
        if args.label3 in fil:
          acq3 = (Acquisition(us, fil));

    print("Set1 acquisitions:");
    for acq in set1:
      if(acq.validate()==False):
        print("could not validate file", acq._lightfile);
        exit(1);
      print(acq._lightfile);

    print("Set2 acquisitions:");
    for acq in set2:
      if(acq.validate()==False):
        print("could not validate file", acq._lightfile);
        exit(1);
      print(acq._lightfile);

    if(acq3 and acq3.validate()):
      print("acq3 file:\n",acq3._lightfile);
    else:
      print("could not find acq3");
      exit(1);

    if(args.dry):
      print("dry stop");
      exit(0);

    saveCoefficients(set1, set2, acq3, args.outfile);


if __name__ == '__main__':
    main()


