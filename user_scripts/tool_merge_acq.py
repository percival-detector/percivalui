#!/usr/bin/env python3

# Merge the 2 files created by the DAQ into one

import sys
import argparse
import time
import os.path;
import h5py;
import numpy as np;
import collections;

# change this to insert ref cols with value zero at the left if you want.
numrefcols = 32;

def splitGFC(pval):
    imgGn= pval >> 13;
    imgFn= (pval >> 5) & 0xff;
    imgCrs= pval & 0x1f;

    return imgGn, imgFn, imgCrs;

def merge_files_and_save(filename1, filename2, outfile, delete=True, split=False):
  f1 = h5py.File(filename1, "r");
  f2 = h5py.File(filename2, "r");
  of = h5py.File(outfile, "w");

  for dset in ["data", "reset", "ecount"]:
    if dset in f1:
      shape1 = f1[dset].shape;
      if shape1[1] != 1484 or shape1[2] != 1408:
        print("oh dear wrong shape on input", shape1);
        exit(1);
      # we are going to expand the frame to have ref cols at the left
      numfr1 = shape1[0];
      numfr2 = f2[dset].shape[0];
      outshape = (numfr1+numfr2, 1484, 1408 + numrefcols);

      dtp = "float32" if dset=="ecount" else "uint16";

      output = np.zeros(outshape, dtype=dtp) * np.nan;

      for i in range(0, numfr1):
        output[i*2,:,numrefcols:] = f1[dset][i,:,:];

      for i in range(0, numfr2):
        output[i*2+1,:, numrefcols:] = f2[dset][i,:,:];

     # output[0::2,:,:] = f1[:,:,:]; would also work

      of.create_dataset(dset, data = output);

      if(split):
        if dset in ["data", "reset"]:
          gain, fine, crs = splitGFC(output);
          of.create_dataset(dset + "-gain", data=gain);
          of.create_dataset(dset + "-coarse", data=crs);
          of.create_dataset(dset + "-fine", data=fine);
          

  # should also do info field here.

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
    parser.add_argument("-s", "--split", default=False, action="store_true", help="add datasets for g,f,c too");
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


    allfiles = collections.OrderedDict();
    for filename in sorted(os.listdir(indir)):
      if args.label in filename and not "combined" in filename:
        allfiles[filename] = 1;

    count = 0;
    for filename1 in allfiles.keys():
      if filename1.endswith("01.h5"):
        filename2 = filename1.replace("01.h5", "02.h5");
        if os.path.exists(os.path.join(indir,filename2)) and count < args.maxfiles:
          outname = filename1.replace("000001.h5", "combined.h5");
          if False and os.path.exists(os.path.join(outdir, outname)):
            print("already done ", outname);
          else:
            print("Merging{} {} and {} into\n *** {}".format("+s" if args.split else "",filename1, filename2, outname));
            merge_files_and_save(os.path.join(indir, filename1), os.path.join(indir, filename2),
                os.path.join(outdir, outname), args.delete, args.split);
            count += 1;



if __name__ == '__main__':
    main()
