#!/usr/bin/env python3

import sys;
import numpy;
import time;
import h5py;
import argparse;
import os;
import re;

# this script operates globally (all pixels the same). It can be adapted for pixelwise pedestals pretty easily.
# the datasets we need to add to the file of calib-constants are: e_per_ADU and Pedestal_ADU (1 frames per gain mode)

g0_e_per_adu = 12.24;
g1g0_multiplier = 8.2;
g2g1_multiplier = 8.1;
g0_pedestal = 15.25;
g1_pedestal = -1457.2;
g2_pedestal = -1667.1;

g0_file = "/dls/detectors/Percival/captures/darkframes/2022.05.09.18.42.01_G0_combined_mv.h5";
g1_file = "/dls/detectors/Percival/captures/darkframes/2022.05.09.18.44.43_G1_combined_mv.h5";
g2_file = "/dls/detectors/Percival/captures/darkframes/2022.05.09.18.47.22_G2_combined_mv.h5";

def visitor_func(name, node):
    if(isinstance(node, h5py.Dataset)):
      print(name, node);

def createOutputFromGlobalConstants(hout):
    dset = numpy.ones( (4,1484,1440) );
    dset[0,:,32:] *= g0_e_per_adu;
    dset[1,:,32:] *= g0_e_per_adu * g1g0_multiplier;
    dset[2,:,32:] *= g0_e_per_adu * g1g0_multiplier * g2g1_multiplier;
    dset[:,:,:32] = numpy.nan;
    hout.create_dataset("e_per_ADU", data = dset);
    dset = numpy.ones( (4,1484,1440) );
    dset[0,:,32:] *= g0_pedestal;
    dset[1,:,32:] *= g1_pedestal;
    dset[2,:,32:] *= g2_pedestal;
    dset[:,:,:32] = numpy.nan;

    if os.path.isfile(g0_file):
      pedfile = h5py.File(g0_file);
      dset[0,:,32:] = pedfile["avg"];
      pedfile.close();
    else:
      print("can not find a dark frame file for G0");

    if os.path.isfile(g1_file):
      pedfile = h5py.File(g1_file);
      dset[1,:,32:] = pedfile["avg"];
      pedfile.close();
    else:
      print("can not find a dark frame file for G1");

    if os.path.isfile(g2_file):
      pedfile = h5py.File(g2_file);
      dset[2,:,32:] = pedfile["avg"];
      pedfile.close();
    else:
      print("can not find a dark frame file for G2");

    hout.create_dataset("Pedestal_ADU", data = dset );

def createOutputPixelwise(hout, epadu, file0, file1):
    dset = numpy.ones( (4,1484,1440) ) * numpy.nan;
    dset[0,:,:] = epadu["e_per_adu"][:,:];
    dset[1,:,:] = epadu["e_per_adu"][:,:] * file0["gain"][:,:];
    dset[2,:,:] = epadu["e_per_adu"][:,:] * file0["gain"][:,:] * file1["gain"][:,:];
    hout.create_dataset("e_per_ADU", data = dset);

    dset = numpy.ones( (4,1484,1440) ) * numpy.nan;
    dset[0,:,:] = file0["pedestal0"][:,:];
    dset[1,:,:] = file0["pedestal1"][:,:];
    dset[2,:,:] = file1["pedestal1"][:,:];

    hout.create_dataset("Pedestal_ADU", data = dset );

def options():
    desc = """Script to create the calib.h5 file needed by the FP calib plugin. In global mode, you need to write the constants into this script first. 
    By convention, the output datasets are 1484 x 1440, and the reference columns [0,31] are NaN.
    """;
    parser = argparse.ArgumentParser(description=desc)

 #   parser.add_argument("-l", "--label", default="VINSCAN", help="filename label to search for (default VINSCAN)")
    parser.add_argument("--adcfile", default="calib.h5", help="infile name containing adc coefficients (default calib.h5)")
    parser.add_argument("-g", "--globall", default=False, action="store_true", help="global calibration (same values over all pixels)")
    # these are used in pixelwise mode:
    parser.add_argument("--eperadu", default="calib.h5", help="infile name containing e_per_adu values for Hi gain mode (default )")    
    parser.add_argument("--himedfile", default="calib.h5", help="infile name containing gain-factors hi-med and pedestals for Hi and Med gains (default )")    
    parser.add_argument("--medlofile", default="calib.h5", help="infile name containing gain-factors med-lo and pedestals for Med and Lo gains (default )")

    parser.add_argument("-o", "--outfile", default="calib_complete.h5", help="outfile name (default calib_complete.h5)")

    args = parser.parse_args()
    return args;


def main():
    args = options();

    adcfile = args.adcfile;
    outfile = args.outfile;
    if(os.path.isfile(adcfile)):
      hin = h5py.File(adcfile, "r");
      hout = h5py.File(outfile, "w");

      for dn in ["reset/coarse/offset", "reset/coarse/slope", "reset/fine/offset", "reset/fine/slope", "sample/coarse/offset", "sample/coarse/slope", "sample/fine/offset", "sample/fine/slope"]:
        hout.create_dataset(dn, data=hin[dn]);

      hin.close();

      if args.globall:
        createOutputFromGlobalConstants(hout);
      else:
        if os.path.isfile(args.eperadu) and os.path.isfile(args.medlofile) and os.path.isfile(args.himedfile):
          epadu = h5py.File(args.eperadu, "r");
          file1 = h5py.File(args.medlofile, "r");
          file0 = h5py.File(args.himedfile, "r");
          createOutputPixelwise(hout, epadu, file0, file1);
        else:
          print("missing file");
          exit(1);
      
      hout.close();
    else:
      print("can not find", adcfile);
      exit(1);

    print("saving", outfile);

if __name__ == '__main__':
    main()






