#!/usr/bin/env python3

# split gcf values
# I don't know as yet whether this script is meant to output another h5 file,
# or print the pixel output to std out.

import sys
import argparse
import time
import os.path;
import h5py;
import numpy as np;

def splitGFC(img):
    imgGn= img[:,:]//(2**13)
    imgFn= (img[:,:]-(imgGn.astype('uint16')*(2**13)))//(2**5)
    imgCrs= img[:,:] -(imgGn.astype('uint16')*(2**13)) -(imgFn.astype('uint16')*(2**5))

    return imgGn, imgFn, imgCrs;


def options():
    desc = "Script to extract Gain Fine Course values from the pixel in Percival frames.";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-r", help="row coord", default=1000, type=int);
    parser.add_argument("-c", help="col coord", default=500, type=int);
    parser.add_argument("-i", "--infile", help="h5 file input")
    # todo are we saving to file or printing?
 #   parser.add_argument("-o", "--outdir", default="", help="folder for h5 files output (default same as infile)")
    parser.add_argument("-v", "--verbose", help="verbose logging (default F)", action="store_true", default=False);

    args = parser.parse_args()
    return args


def main():
    args = options();

    infile = os.path.join("/dls/detectors/Percival/captures", args.infile);
    if os.path.exists(infile):
      infile = infile;
    else:
      print ("invalid file ", args.infile);
      exit(1);

    """
        if os.path.isdir(args.outdir):
          outdir = args.outdir;
        elif args.outdir:
          print ("invalid directory ", args.outdir);
          exit(1);
    """

    row = int(args.r);
    col = int(args.c);
    h5 = h5py.File(infile, "r");
    if "data" in h5:
      inarray = h5["data"][3];
     # inarray = np.full((1,1), 0xff, dtype="uint16");
      (imgGn, imgFn, imgCrs) = splitGFC(inarray);

      print ("pixel at ({},{}) has g:{} f:{} c:{})".format(row,col, imgGn[row,col], imgFn[row,col], imgCrs[row,col]));
    elif "sample/coarse/slope" in h5:
      inarray = h5["sample/coarse/slope"];
      print ("coarse/slope at ({},{}) has val {}".format(row,col,inarray[row,col]));
      inarray = h5["sample/coarse/offset"];
      print ("coarse/offset at ({},{}) has val {}".format(row,col,inarray[row,col]));  
      



if __name__ == '__main__':
    main()
