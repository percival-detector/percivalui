#!/usr/bin/env python3

# this script is for showing a 2d image from the detector. It examines the datasets in the h5 file, and
# judges what kind of file it is and what is the best thing to do. If you supply a calibfile it will apply
# the calibration coefficients in getCADU in Alessandro's patent formula. If you don't it will show the
# raw coarse, fine, gain.
#
# The script has the enormous problem that matplotlib does not plot the images pixel-per-pixel. It applies
# some kind of filter over the image as it draws it on the canvas. This is a big problem, and it means that
# you don't get an accurate impression of the image on the canvas. The ways to improve this is to alter the
# dpi figure, figure size and set a small range of the image to look at (xpart,ypart).
# It is better to save the image as a png
# file, or separate the components crs, fn, gn into new datasets and use dawn.

import sys;
import numpy;
import matplotlib.pyplot;
import percival.carrier.const;
import h5py;
import argparse;
import os;
# import PIL;
import png;



iGn=0; iCrs=1; iFn=2;
g_NGnCrsFn = 3;
g_NRow = 1484;
g_NCol = 1408;
g_refcols = 32;


def splitGCF(pval):
    imgGn= pval >> 13;
    imgFn= (pval >> 5) & 0xff;
    imgCrs= pval & 0x1f;
    # ordering here is by iGn, iCrs, iFn
    return imgGn, imgCrs, imgFn;

def getCADU(coarse, fine, coarseGain, coarseOffset, fineGain, fineOffset):
    coarseGain = coarseGain[:,g_refcols:];
    coarseOffset = coarseOffset[:,g_refcols:];
    fineGain = fineGain[:,g_refcols:];
    fineOffset = fineOffset[:,g_refcols:];
    idealOffset = numpy.zeros( (coarseGain.shape[0], coarseGain.shape[1]) ) + (128.0 * 32.0);
    idealSlope  = (idealOffset / 1.5); # mapped over over 1.5V Vin span

    return ( idealOffset + ( (idealSlope/coarseGain)*(coarse+1.0-coarseOffset) - (idealSlope/fineGain)*(fine-fineOffset) ) )

def getCADU_scaler(coarse, fine, coarseGain, coarseOffset, fineGain, fineOffset):
    idealOffset = (128.0 * 32.0);
    idealSlope  = (idealOffset / 1.5); # mapped over over 1.5V Vin span

    return ( idealOffset + ( (idealSlope/coarseGain)*(coarse+1.0-coarseOffset) - (idealSlope/fineGain)*(fine-fineOffset) ) )


def plot_simpleXY(filename, cse, fn, array1):
    array1 = numpy.asarray(array1);
    array1 /= 5.0;
    matplotlib.pyplot.scatter(range(0,len(array1)), array1, c="y", label="cadu")
    matplotlib.pyplot.scatter(range(0,len(array1)), cse, c="b", label="coarse")
    matplotlib.pyplot.scatter(range(0,len(array1)), fn, c="r", label="fine");
    matplotlib.pyplot.legend(loc='upper left')
    print("saving",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.close();
    matplotlib.pyplot.clf();
    

def plot_1x2D(filename, array1, label_title1, maxval=0.0, logScaleFlag=False,  invertx_flag=True):
    matplotlib.pyplot.clf();
    label_x = "column";
    label_y = "row";
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    fig.tight_layout()
    matplotlib.pyplot.subplots_adjust(wspace = 0.5)
    #
    matplotlib.pyplot.subplot(1,1,1)
    if logScaleFlag: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    print("saving",filename);
    matplotlib.pyplot.savefig(filename);
    matplotlib.pyplot.close();
    matplotlib.pyplot.clf();

def plot_2x2D(filename, array1, array2, label_title1,label_title2, invertx_flag=True, logScaleFlag=False):
    ''' 2x2D image'''
    matplotlib.pyplot.clf();
    label_x = "column";
    label_y = "row";
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure(figsize=( 8, 4), dpi=1000)
    fig.tight_layout();
    matplotlib.pyplot.subplots_adjust(wspace = 0.5, bottom = 0.0, top = 1.0)
    axes = matplotlib.pyplot.gca();
    
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
    print("saving",filename);
    matplotlib.pyplot.savefig(filename);
  #  matplotlib.pyplot.show(block=True)
    return (fig)

def plot_3x2D(filename, array1, array2, array3, label_title1,label_title2, label_title3, invertx_flag=True, xpart=(0,0), ypart=(0,0)):
    ''' 2x2D image'''
    logScaleFlag = False;
    matplotlib.pyplot.clf();
    if xpart == (0,0):
      xpart = (0, array1.shape[1]);
    if ypart == (0,0):
      ypart = (0, array1.shape[0]);
    label_x = "column {}".format(xpart);
    label_y = "row {}".format(ypart);
    cmap = matplotlib.pyplot.cm.jet
    dpi = 100;
    # this sets the current figure, which seems to be the canvas
    fig = matplotlib.pyplot.figure(figsize=( 15, 7 ), dpi=dpi);
    fig.tight_layout();
    matplotlib.pyplot.subplots_adjust(wspace = 0.2, bottom = 0.01, top = 0.99)

    ax = matplotlib.pyplot.subplot(1,3,1)
    if logScaleFlag: img = ax.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: img = ax.imshow(array1, interpolation='none', cmap=cmap, resample=False)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    matplotlib.pyplot.xlim(xpart);
    matplotlib.pyplot.ylim(ypart);
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar(img, ax = ax)
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    #
    ax = matplotlib.pyplot.subplot(1,3,2);
    if logScaleFlag: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.xlim(xpart);
    matplotlib.pyplot.ylim(ypart);
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    ax = matplotlib.pyplot.subplot(1,3,3)
    if logScaleFlag: matplotlib.pyplot.imshow(array3, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array3, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.xlim(xpart);
    matplotlib.pyplot.ylim(ypart);
    matplotlib.pyplot.title(label_title3)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    print("saving",filename);
    matplotlib.pyplot.savefig(filename);
  #  matplotlib.pyplot.show(block=True)
    return (fig)

def draw_1x1D(outfile, array1):
    matplotlib.pyplot.imsave("snatch.png", array1, cmap="Greys");
    # the other way to save a png is with
    # img_colormapped = cv2.applyColorMap(img_scaled, cv2_colormap)
    #  img_encode = cv2.imencode('.png', img_colormapped, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])[1]


def graphCalibFile(h5):

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

def options():
    desc = "Script to create a sensor-image from an h5 file, ie it graphs some function on the pixels. This can be the calibration coefficients for the pixel or the gcf values of an image.";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-i", "--infile", default="", help="the h5 file input")
    parser.add_argument("--frame", default=2, help="the frame to process: a number or all (default 2)")
    parser.add_argument("--indir", default="/dls/detectors/Percival/captures", help="folder for h5 files input (default captures)")
    parser.add_argument("--calibfile", default="", help="file for calib coeffs to apply (default none)")

    parser.add_argument("--outfile", default="sensorim", help="output png file (default sensorim) used in some cases");

    args = parser.parse_args()
    return args;


def main():
    args = options();

    indir = "";
    if os.path.isdir(args.indir):
      indir = args.indir;
    else:
      print ("invalid in directory ", args.indir);
      exit(1);

    infile = args.infile;
    if not os.path.isfile(infile):
      infile = os.path.join(indir, infile);
    if not os.path.isfile(infile):
      print("invalid file", infile);
      exit(1);

    outfile = args.outfile;
    if not outfile.endswith(".png"):
      outfile += ".png";

    c5 = None;
    coarseslope = coarseoffset = fineslope = fineoffset = None;
    if args.calibfile:
      if os.path.isfile(args.calibfile):
        c5 = h5py.File(args.calibfile);
        coarseslope = numpy.asarray(c5.get("sample/coarse/slope"));
        coarseoffset = numpy.asarray(c5.get("sample/coarse/offset"));
        fineslope = numpy.asarray(c5.get("sample/fine/slope"));
        fineoffset = numpy.asarray(c5.get("sample/fine/offset"));
        pedestal = numpy.asarray(c5.get("Pedestal_ADU"));
        eperadu = numpy.asarray(c5.get("e_per_ADU"));
      else:
        print("Error no calibfile");
        exit(1);

    h5 = h5py.File(infile);
    datasets = list(h5.keys());

    if h5.get("data/data"):
      dset = h5.get("data/data");
      plot_2x2D(outfile, dset, dset, label_title1="dunno",label_title2="same", invertx_flag=True);
    elif "data" in datasets:
      arrayd = numpy.asarray(h5.get("data"));

      for fr in range(0,arrayd.shape[0]):
      # it's an image file:
        if "all" == args.frame or fr == int(args.frame):
          outfile = os.path.basename(infile).replace(".h5", "_fr{:03d}.png".format(fr));
          outfile2 = os.path.basename(infile).replace(".h5", "_ecount_fr{:03d}.png".format(fr));
          dsetG, dsetC, dsetF = splitGCF(arrayd[fr,:,:]);
          if c5:
            cadu_am = getCADU(dsetC, dsetF, coarseslope, coarseoffset, fineslope, fineoffset);
            plot_1x2D(outfile, cadu_am, "combined adu");
            # we go further here and create electons per pixel
            for r in range(0, cadu_am.shape[0]):
              for c in range(0, cadu_am.shape[1]):
                cadu_am[r,c] -= pedestal[dsetG[r, c],r,32+c];
                cadu_am[r,c] *= eperadu[dsetG[r, c],r,32+c];
            plot_1x2D(outfile2, cadu_am, "ecount", 1e6);
            
          else:
            xpart = (700,800);
            ypart = (500,600);
            plot_3x2D(outfile, dsetG, dsetC, dsetF, "Gn", "crs", "fn");

    elif "sample" in datasets:
      graphCalibFile(h5);

    elif "ecount" in datasets:
      arrayd = h5.get("ecount")[:];
      if 0<=args.frame and args.frame<arrayd.shape[0]:
        frame = args.frame;
      plot_1x2D("graph_ecount.png", arrayd[frame,:,:], "ecount");

    elif "avg" in datasets:
      arrayd1 = h5.get("avg")[:];
      arrayd2 = h5.get("var")[:];
      plot_2x2D("graph_mv.png", arrayd1, arrayd2, "Pixel-avg", "Pixel-variance");
    else:
      print("datasets are:", datasets);

    h5.close();


if __name__ == '__main__':
    main()






