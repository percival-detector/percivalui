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

# This script was developed on a half-head and ignores cols [0,703].

g_showNaN = False;

# ar stands for acceptable range.
arSampleCoarseSlope = (17,21);
arSampleCoarseOffset = (41,55);
arSampleFineSlope = (900,1920);
arSampleFineOffset = (60,160);
arResetCoarseSlope = (17,22);
arResetCoarseOffset = (41,55);
arResetFineSlope = (900, 1920);
arResetFineOffset = (60,160);

def plot_2x2D(filename, array1, array2, logScaleFlag, label_title1,label_title2, invertx_flag=True):
    ''' 2x2D image'''
    matplotlib.pyplot.clf();
    label_x = "column";
    label_y = "row";
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    fig.tight_layout()
    matplotlib.pyplot.subplots_adjust(wspace = 0.5)
    #
    matplotlib.pyplot.subplot(1,2,1)
    if logScaleFlag: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(1,2,2)
    if logScaleFlag: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    print("saving", filename);
    matplotlib.pyplot.savefig(filename);
  #  matplotlib.pyplot.show(block=True)
    return (fig)

def plotHisto(h5, dset):
  matplotlib.pyplot.clf();
  cs = numpy.array(h5.get(dset)[:]);
  allvals = [];
  for r in range(0,1484):
    for c in range(704,1408):
      v = cs[r,c];
      allvals.append(v);

  n, bins, patches = matplotlib.pyplot.hist(allvals, 100, density=False, facecolor='g')

  matplotlib.pyplot.xlabel(dset)
  matplotlib.pyplot.ylabel('qty')
  matplotlib.pyplot.title('Histogram of values')
 # matplotlib.pyplot.xlim((0,1000));
  filename = "histo-" + dset.replace("/","-") + ".png";
  print("saving ", filename);
  matplotlib.pyplot.savefig(filename);
  matplotlib.pyplot.clf();

def graphFile(h5filename):
    h5 = h5py.File(h5filename, 'r');
    a1 = h5['sample/coarse/slope'];
    a2 = h5['sample/coarse/offset'];
    plot_2x2D("graph_sc.png", a1, a2, False, "sample/coarse/slope", "sample/coarse/offset");
    a1 = h5['sample/fine/slope'];
    a2 = h5['sample/fine/offset'];
    plot_2x2D("graph_sf.png", a1, a2, False, "sample/fine/slope", "sample/fine/offset");

    a1 = h5['reset/coarse/slope'];
    a2 = h5['reset/coarse/offset'];
    plot_2x2D("graph_rc.png", a1, a2, False, "reset/coarse/slope", "reset/coarse/offset");
    a1 = h5['reset/fine/slope'];
    a2 = h5['reset/fine/offset'];
    plot_2x2D("graph_rf.png", a1, a2, False, "reset/fine/slope", "reset/fine/offset");

    plotHisto(h5, "sample/coarse/slope");
    plotHisto(h5, "sample/fine/slope");
    plotHisto(h5, "reset/coarse/slope");
    plotHisto(h5, "reset/fine/slope");
    plotHisto(h5, "sample/coarse/offset");
    plotHisto(h5, "sample/fine/offset");
    plotHisto(h5, "reset/coarse/offset");
    plotHisto(h5, "reset/fine/offset");
    h5.close();

def outlier(val, rangey):
    # this will treat NaN as outlier.
    if val > rangey[0] and val < rangey[1]:
      return False;

    print("{:.2f} outside {}".format(val, rangey));
    return True;

def fixFile(h5filename):
    # this has a problem in that we don't know how many columns we have.
    h5 = h5py.File(h5filename, 'r');
    scs = h5['sample/coarse/slope'];
    sco = h5['sample/coarse/offset'];

    sfs = h5['sample/fine/slope'];
    sfo = h5['sample/fine/offset'];

    rcs = h5['reset/coarse/slope'];
    rco = h5['reset/coarse/offset'];

    rfs = h5['reset/fine/slope'];
    rfo = h5['reset/fine/offset'];

    if scs.shape != (1484,1408):
      print("Your input file has the wrong dimensions. Please review");
      exit(1);

    badpix = [];

    for r in range(0,1484):
      for c in range(704,1408):
        if outlier(scs[r,c], arSampleCoarseSlope):
          badpix.append( (r,c) );
        elif outlier(sco[r,c], arSampleCoarseOffset):
          badpix.append( (r,c) );
        elif outlier(sfs[r,c], arSampleFineSlope):
          badpix.append( (r,c) );
        elif outlier(sfo[r,c], arSampleFineOffset):
          badpix.append( (r,c) );
        elif outlier(rcs[r,c], arResetCoarseSlope):
          badpix.append( (r,c) );
        elif outlier(rco[r,c], arResetCoarseOffset):
          badpix.append( (r,c) );
        elif outlier(rfs[r,c], arResetFineSlope):
          badpix.append( (r,c) );
        elif outlier(rfo[r,c], arResetFineOffset):
          badpix.append( (r,c) );


    print ("badpix are:", badpix);

    newname = h5filename.replace(".h5","_fixed.h5");
    print("saving", newname);
    if(len(newname) != len(h5filename)):
      h6 = h5py.File(newname, 'w');
      scs2 = h6.create_dataset('sample/coarse/slope', shape=(1484,1440), dtype=numpy.double );
      sco2 = h6.create_dataset('sample/coarse/offset', shape=(1484,1440), dtype=numpy.double);
      sfs2 = h6.create_dataset('sample/fine/slope', shape=(1484,1440), dtype=numpy.double);
      sfo2 = h6.create_dataset('sample/fine/offset', shape=(1484,1440), dtype=numpy.double);

      rcs2 = h6.create_dataset('reset/coarse/slope', shape=(1484,1440), dtype=numpy.double);
      rco2 = h6.create_dataset('reset/coarse/offset', shape=(1484,1440), dtype=numpy.double);
      rfs2 = h6.create_dataset('reset/fine/slope', shape=(1484,1440), dtype=numpy.double);
      rfo2 = h6.create_dataset('reset/fine/offset', shape=(1484,1440), dtype=numpy.double);

      scs2[:,:32] = numpy.nan;
      scs2[:,32:] = scs[:,:];
      sco2[:,:32] = numpy.nan;
      sco2[:,32:] = sco[:,:];
      sfs2[:,:32] = numpy.nan;
      sfs2[:,32:] = sfs[:,:];
      sfo2[:,:32] = numpy.nan;
      sfo2[:,32:] = sfo[:,:];

      rcs2[:,:32] = numpy.nan;
      rcs2[:,32:] = rcs[:,:];
      rco2[:,:32] = numpy.nan;
      rco2[:,32:] = rco[:,:];
      rfs2[:,:32] = numpy.nan;
      rfs2[:,32:] = rfs[:,:];
      rfo2[:,:32] = numpy.nan;
      rfo2[:,32:] = rfo[:,:];

      for (r,c) in badpix:
        scs2[r,c+32] = numpy.nan;
        sco2[r,c+32] = numpy.nan;
        sfs2[r,c+32] = numpy.nan;
        sfo2[r,c+32] = numpy.nan;
        rcs2[r,c+32] = numpy.nan;
        rco2[r,c+32] = numpy.nan;
        rfs2[r,c+32] = numpy.nan;
        rfo2[r,c+32] = numpy.nan;

      h6.close();

    h5.close();



def options():
    desc = "Script to graph an h5 file of Percival calibration coefficient (eg as produced by distiller). You can set inlier-ranges, and create a file_fixed.h5 where coefficients for outlier pixels have been set NaN.";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--graph", metavar="H5FILE", default="", help="show graphs of this file instead");
    parser.add_argument("--fixfile", metavar="H5FILE", default="", help="check the outlier values in all 8 calib datasets of this file, and save a new file as <file_fixed.h5>");

    args = parser.parse_args()
    return args;


def main():
    args = options();

    if(args.graph):
      graphFile(args.graph);
      exit(0);

    elif(args.fixfile):
      fixFile(args.fixfile);
      
      

if __name__ == '__main__':
    main()






