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

def createGraph1x2d(filename, xvals,yvals,xlabel,ylabel):
    slope, inter, r2 = linear_fit(xvals, yvals);
    fig = matplotlib.pyplot.figure()
    # iff we use cds I think we can expect the 0 intensity to be the dark frame value.
    matplotlib.pyplot.plot(xvals, yvals,  'o', fillstyle='none')
  #  matplotlib.pyplot.plot(avg_per_acq, var_per_acq,  'o', fillstyle='none')
    matplotlib.pyplot.xlabel(xlabel)
    matplotlib.pyplot.ylabel(ylabel);
    matplotlib.pyplot.title("r2={:.2f}, slope={:.4f}, inter={:.2f}".format(r2, slope, inter) ); 
  #  matplotlib.pyplot.xlim((1,4));
  #  matplotlib.pyplot.ylim((0,4));

    # xvalues then y values
 #   matplotlib.pyplot.plot([0, 4], [1, 3.0], 'g-')
    xmax = max(xvals);
    matplotlib.pyplot.plot([0, xmax], [inter, inter + xmax * slope], 'r-')
    # haha ignore output dir!
    print("saving ",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.clf();
    matplotlib.pyplot.close();

class Acquisition:

  def  __init__(self, us, lightfile, darkfile):
    self._us = us;
    self._lightfile = lightfile;
    self._darkfile = darkfile;
    pass;

  def setExposureTime(self, us):
    self._us = us;
 
  def getLightFile(self):
    return self._lightfile;

  def getDir(self):
    return os.path.dirname(self._lightfile);

  def validate(self):
    ok = True;
    try:
      self.hlightfile = h5py.File(self._lightfile, "r");
      self.light_avg = numpy.asarray(self.hlightfile["avg"]);
      self.light_var = numpy.asarray(self.hlightfile["var"]);
      self.light_avg_by_row = numpy.asarray(self.hlightfile["avg_by_row"]);
      self.light_var_by_row = numpy.asarray(self.hlightfile["var_by_row"]);

      self.hdarkfile = h5py.File(self._darkfile, "r");
      self.dark_avg = numpy.asarray(self.hdarkfile["avg"]);
      self.dark_var = numpy.asarray(self.hdarkfile["var"]);
      self.dark_avg_by_row = numpy.asarray(self.hdarkfile["avg_by_row"]);
      self.dark_var_by_row = numpy.asarray(self.hdarkfile["var_by_row"]);

      if(self.light_avg.shape[1]!=1440 or self.dark_avg.shape[1]!=1440):
        ok = False;
    except:
      return False;

    return ok;

  # warning this often goes negative due to dodgy data
  def getVar(self, row, col):
    var = self.light_var[row, col] - self.dark_var[row,col];
    return var;
  # warning this often goes negative due to dodgy data
  def getAvg(self, row, col):
    # tempy
    avg = self.light_avg[row, col] - 0.5 * self.dark_avg[row,col];
    return avg

  def getRowVar(self, row):
    return self.light_var_by_row[0, row] - self.dark_var_by_row[0, row];

  def getRowAvg(self, row):
    return self.light_avg_by_row[0, row] - self.dark_avg_by_row[0, row];

def createEPerAduPixelwise(filestouse):
  r2min = 0.85;
  print("creating e_per_adu.h5; r2 demand is {:.2f}".format(r2min));
  outfile = filestouse[0].getDir() + "/e_per_adu.h5";
  with h5py.File(outfile, "w") as fout:
    out = numpy.zeros((1484, 1440), dtype=float) * numpy.nan;

    for r in range(0,1484):
      if r % 50 == 0:
        print("doing row",r);
      for c in range(736,1440):
   #   for c in range(32,1440):
        avg_per_acq = [0];
        var_per_acq = [0];
        for acq in filestouse:
          avg = acq.getAvg(r,c);
          var = acq.getVar(r,c);
          if(0<avg and 0<var):
            avg_per_acq.append(avg);
            var_per_acq.append(var);


        (slope, inter, r2) = linear_fit(avg_per_acq, var_per_acq);
        if(False):
          createGraph1x2d("egraph{:03d}-{:03d}.png".format(r,c), avg_per_acq, var_per_acq, "mean", "variance");
        if r2 < r2min:
          # tempy
          #print("warning pixel at ",r,c," has unusable r2 of {:.2f}; setting nan".format(r2));
          slope = numpy.nan;
        else:
          out[r,c] = slope;


    fout.create_dataset("e_per_adu", data = out);
    print("saving", outfile,"...");
    fout.close();

def createEPerAduRowwise(filestouse):
  for r in range(0,7):
    avg_per_acq = [0];
    var_per_acq = [0];
    for acq in filestouse:
      avg_per_acq.append(acq.getRowAvg(r));
      var_per_acq.append(acq.getRowVar(r));

    (slope, inter, r2) = linear_fit(avg_per_acq, var_per_acq);
    createGraph1x2d("egraph-row{}.png".format(r), avg_per_acq, var_per_acq, "mean", "variance");
    print("row {} has slope {:.2f} and r2 {:.2f}".format(r, slope, r2));

# I don't know if we need this function as we need pedestals from bias-mode
#  fixgainall4. However we'll keep it for reference.
def createPedestalPixelwise(filestouse):
  # the lines through both the dark and light points should intersect
  # the y axis at the same place. Since the dark points are flat, we
  # think the dark value of any acquisition should be the intersect.
  r2min = 0.85;
  print("saving pedestal.h5; r2 demand is {:.2f}".format(r2min));
  with h5py.File("pedestal.h5", "w") as fout:
    out = numpy.zeros((1484, 1440), dtype=float) * numpy.nan;

    for r in range(0,1484):
      if r % 50 == 0:
        print("doing row",r);
      for c in range(736,1440):
        avg_per_acq = [];
        us_per_acq = [];
        for acq in filestouse:
          us_per_acq.append(acq._us);
          avg_per_acq.append(acq.dark_avg[r,c]);

        if(False and r==13 and c==1002):
          createGraph1x2d("pedestalgraph.png", us_per_acq, avg_per_acq, "us", "pix reading");
          exit(1);

        (slope, inter, r2) = linear_fit(us_per_acq, avg_per_acq);
        if r2 < r2min:
          print("warning pixel at ",r,c," has unusable r2 of {:.2f}".format(r2));
          slope = numpy.nan;
        out[r,c] = inter;

    fout.create_dataset("Pedestal_g0", data = out);


def special(filestouse):
    acq = filestouse[-1];
    for r in range(0,7):
      print("time", acq._us, "row",r,"avg", acq.getRowAvg(r), "var", acq.getRowVar(r));

def options():
    desc = "Script to plot variance / mean against intensity. This can work with individual pixels. It can calculate e_per_adu on a pixelwise basis and saves the file as e_per_adu.h5. The script can do other things too if you alter it a little.";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i", "--indir", help="directory of files _mv that come from calib-mv", default="", required=True)
    parser.add_argument("-d", "--dklabel", help="input filename label of data from dark acquisition (default DKSCAN)", default="DKSCAN")
    parser.add_argument("-l", "--label", default="PTCSCAN", help="input filename label (default PTCSCAN)")

    args = parser.parse_args()
    return args;


def main():
    global g_regions;
    args = options();

    indir = args.indir;
    if not os.path.isdir(indir):
      print("Error input dir:",indir);
      exit(1);

    print("label to find is", args.label);

    allfiles = sorted(os.listdir(indir));

    filestouse = [];
    firstdkfile = None;
    for fil in allfiles:
      fil = os.path.join(indir, fil);
      if os.path.isfile(fil) and args.label in fil and "cds_mv.h5" in fil:
        us = 0;
        mat = re.search("_(\d+)us_", fil);
        if mat:
          us = int(mat.group(1));
          # we don't use us
        else:
          print("Error: could not find us value in ", f);
          exit(1);

        dkfil = fil.replace(args.label, args.dklabel);
        if os.path.isfile(dkfil):
          pass;
        else:
          print("Error can not find", dkfil);
          exit(1);

        if firstdkfile==None:
          # we found that darkframes should offer the same mean / var on all exposure times
          # we enforce that.
          print("using dark file for all:", dkfil);
          firstdkfile = dkfil;

        filestouse.append(Acquisition(us, fil, firstdkfile));

    for acq in filestouse:
      if(acq.validate()):
        print("using light file:", acq.getLightFile());
      else:
        print("could not validate file", acq._lightfile);
        exit(1);

    #filestouse.pop();
    createEPerAduPixelwise(filestouse);
 #   createEPerAduRowwise(filestouse);



if __name__ == '__main__':
    main()


