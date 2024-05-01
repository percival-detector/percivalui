# -*- coding: utf-8 -*-
"""
from APy3_auxINIT import *
"""
#%% define P2M constants
ERRint16=-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw= -0.1
ERRDLSraw= 65535 # forbidden uint16, usable to track "pixel" from missing pack
#
iGn=0; iCrs=1; iFn=2; NGnCrsFn=3 
iSmpl=0; iRst=1; NSmplRst=2
#
NGrp= 212
NADC=7; NRowInBlk=NADC
NColInBlk=32
NPad=45; NDataPad=NPad-1
NCol= NColInBlk*NPad
NRow= NADC*NGrp
NbitPerPix=15
# ---
#
#%% import modules
#
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)
#
import sys # command line argument, print w/o newline, version
import time # to have time
import numpy
from scipy import stats # linear regression
from scipy.optimize import curve_fit # non-linear fit
import math
import scipy
import matplotlib
import matplotlib.pyplot
matplotlib.pyplot.rcParams['image.cmap'] = 'jet'
import os # list files in a folder
import glob # to find last file
import re # to sort naturally
import h5py # deal with HDF5
import tkinter
#
import ast # execute command
import collections # len(collections.Counter(A).keys()) n of distinct
#
from mpl_toolkits.mplot3d import Axes3D
#
import APy3_GENfuns
import APy3_P2Mfuns
import APy3_FITfuns

