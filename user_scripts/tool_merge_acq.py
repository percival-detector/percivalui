#!/usr/bin/env python3

# Merge the 2 files created by the DAQ into one

import sys
import argparse
import time
import os.path;
import h5py;
import numpy as np;
import collections;
import re;
from liveview.descrambler import *;

def addrefcols(frames):
  # change this to insert ref cols with value zero at the left if you want.
  numrefcols = 32;

  refcols = np.zeros((frames.shape[0], frames.shape[1], numrefcols), dtype=frames.dtype);
  return np.concatenate((refcols, frames), axis=2);


def splitGFC(pval):
    imgGn= pval >> 13;
    imgFn= (pval >> 5) & 0xff;
    imgCrs= pval & 0x1f;

    return imgGn, imgFn, imgCrs;

def saveGCF(of, dset, ileaved, split, descramble):
    gain = crs = fine = None;
    if (descramble):
        (gain, crs,fine) = descramble_to_GnCrsFn(ileaved);
    elif (split):
      #  (gain, fine, crs) = splitGFC(ileaved);
        (gain, crs, fine) = aggregate_to_GnCrsFn(ileaved);

    if (gain is not None):
      of.create_dataset(dset + "-gain", data=addrefcols(gain));
      of.create_dataset(dset + "-coarse", data=addrefcols(crs));
      of.create_dataset(dset + "-fine", data=addrefcols(fine));


# filename1 and filename2 do need to be in the right order
def merge_files_and_save(filename1, filename2, outfile, delete, split, descramble):
  f1 = h5py.File(filename1, "r");
  f2 = h5py.File(filename2, "r");
  of = h5py.File(outfile, "w");

  for dset in ["data", "reset", "ecount"]:
    if dset in f1:
      shape1 = f1[dset].shape;
      if shape1[1] != 1484 or shape1[2] != 1408:
        print("oh dear wrong shape on input", shape1);
        exit(1);

      numfr1 = shape1[0];
      numfr2 = f2[dset].shape[0];
      outshape = (numfr1+numfr2, 1484, 1408);

      ileaved = np.zeros(outshape, f1[dset].dtype);

      for i in range(0, numfr1):
        ileaved[i*2,:,:] = f1[dset][i,:,:];

      for i in range(0, numfr2):
        ileaved[i*2+1,:,:] = f2[dset][i,:,:];

     # ileaved[0::2,:,:] = f1[:,:,:]; would also work
      saveGCF(of, dset, ileaved, split, descramble);
      ileaved = addrefcols(ileaved);

      of.create_dataset(dset, data = ileaved);

  for dset in ["info"]:
    if dset in f1:
      shape1 = f1[dset].shape;

      numfr1 = shape1[0];
      numfr2 = f2[dset].shape[0];
      outshape = (numfr1+numfr2, shape1[1], shape1[2]);

      ileaved = np.zeros(outshape, dtype=np.uint8);

      for i in range(0, numfr1):
        ileaved[i*2,:,:] = f1[dset][i,:,:];

      for i in range(0, numfr2):
        ileaved[i*2+1,:,:] = f2[dset][i,:,:];

      of.create_dataset(dset, data = ileaved);


  if delete:
    print("deleting {} and its pair".format(filename1));
    os.remove(filename1);
    os.remove(filename2);


def options():
    desc = "Script to combine files like blah_0001.h5 and blah_0002.h5 by interleaving frames. datasets data and reset are kept. Frame-numbering is preserved.";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-l", "--label", default="VINSCAN", help="filename label to search for in the filename (default VINSCAN)");
    parser.add_argument("-i", "--indir", default="/dls/detectors/Percival/captures", help="folder for h5 files input\n  (default /dls/detectors/Percival/captures)")
    parser.add_argument("--no-delete", action="store_false", help="delete original capture files after merge (default on)", default=True, dest="delete")
    parser.add_argument("-o", "--outdir", default="", help="folder for h5 files output (default same as indir)")
    parser.add_argument("-s", "--split", default=False, action="store_true", help="add datasets for g,c,f too");
    parser.add_argument("-d", "--descramble", default=False, action="store_true", help="add datasets for g,c,f and descramble image data into them");
    parser.add_argument("-v", "--verbose", help="verbose logging (default F)", action="store_true", default=False);
    parser.add_argument("-m", "--maxfiles", help="max number of files to create", type=int, default=100000);

    args = parser.parse_args()
    return args


def main():
    args = options();

    indir = "";
    if os.path.isdir(args.indir):
      indir = args.indir;
    else:
      print ("invalid directory ", args.indir);
      exit(1);

    outdir = args.indir;

    if os.path.isdir(args.outdir):
      outdir = args.outdir;
    elif args.outdir:
      print ("invalid directory ", args.outdir);
      exit(1);

    split_desc = "";
    if args.split:
      split_desc = "+s";  
    elif args.descramble:
      split_desc = "+d";


    allfiles = collections.OrderedDict();
    for filename in sorted(os.listdir(indir)):
      if args.label in filename and not "combined" in filename:
        allfiles[filename] = 1;

    # in the odin-data update to 1.8, the numbering started at zero instead of 1.
    count = 0;
    for filename1 in allfiles.keys():
      if filename1.endswith("01.h5"):
        filename_oth = filename1.replace("01.h5", "02.h5");
        if(filename_oth not in allfiles):
          filename_oth = filename1.replace("01.h5", "00.h5");
          filename1, filename_oth = filename_oth, filename1;
        if os.path.exists(os.path.join(indir,filename1)) and os.path.exists(os.path.join(indir,filename_oth)) and count < args.maxfiles:
          outname = re.sub("\d{6}\.h5", "combined.h5", filename1);
          if False and os.path.exists(os.path.join(outdir, outname)):
            print("already done ", outname);
          else:
            print("Merging{} {} and {} into\n *** {}".format(split_desc,filename1, filename_oth, outname));
            merge_files_and_save(os.path.join(indir, filename1), os.path.join(indir, filename_oth),
                os.path.join(outdir, outname), args.delete, args.split, args.descramble);
            count += 1;



if __name__ == '__main__':
    main()
