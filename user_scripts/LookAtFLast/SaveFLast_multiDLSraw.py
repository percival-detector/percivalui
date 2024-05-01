# -*- coding: utf-8 -*-
"""
descramble and visualize/save all scrambled dataset in a folder
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./SaveFLast_multiDLSraw.py
"""
#%% imports and useful constants
from APy3_auxINIT import *
from APy3_descramble_versatile import descramble_versatile
#
#
#
#---
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#%% Flags
#
lastFileOnlyFlag= True # alternatively: process all files in folder
#
swapSmplRstFlag= True
seqModHalfImgFlag= False # this actually means: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
refColH1_0_Flag = False # True if refcol data are streamed out as H1<0> data.
#
showFlag= False
manyImgFlag= False # select more than 1 digit image in interactive plot
#
saveFlag_1file= False # save descramble DLSraw to 1 big file
saveFlag_multiFile= True; #saveFlag_multiFile= False # save descramble DLSraw to multiple files, using metadata name
#
cleanMemFlag= True # this actually mean: save descrambled image (DLSraw standard)
highMemFlag= False; #highMemFlag= True
verboseFlag= True
#
#---
#
#%% data from here
mainFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190613_000_FSI01_Tm20_ADCcorrection/processed/2019.06.13_FSI01_ADCsweep_dmuxSELsw/scrmbld/'
if mainFolder[-1]!='/': mainFolder+='/'
#expected_suffix_fl0= '000000.h5'
#expected_suffix_fl1= '000001.h5'
#expected_suffix_metadata= 'meta.dat'
#
expected_suffix_fl0= '2019.06.14_15.48.xx_FSI01_Tm20_dmuxSELsw_0802g_PGAB_VRSTscan_fn_300x10_000000.h5'
expected_suffix_fl1= '2019.06.14_15.48.xx_FSI01_Tm20_dmuxSELsw_0802g_PGAB_VRSTscan_fn_300x10_000001.h5'
expected_suffix_metadata= '2019.06.14_15.48.xx_FSI01_Tm20_dmuxSELsw_0802g_PGAB_VRSTscan_fn_300x10_meta.dat'
#
fromImg=0; toImg=-1 # negative==all
#fromImg=500; toImg=550 # negative==all
#
outFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190613_000_FSI01_Tm20_ADCcorrection/processed/2019.06.13_FSI01_ADCsweep_dmuxSELsw/DLSraw/'
if outFolder[-1]!='/': outFolder+='/'
#
out_1file_suffix= "xxx"
out_multiFile_suffix= ".h5"
out_imgXFile_multiFile= 10
#
# ---
ADCcorrCDSFlag=False
pedSubtractFlag=False
saveAvgCDSFlag=False # save 2D img (float): avg of ADCcorr, CDS, possibly ped-Subtracted
#
ADCcorrFolder= '/LookAtFLast_CalibParam/ADUcorr/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
pedestalFolder= '/LookAtFLast_CalibParam/Pedestal/'
if pedestalFolder[-1]!='/': pedestalFolder+='/'
out_AvgCDSfile_suffix= "xxx"
#
#---
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#
#%% auxiliary functs 
# ---
#
descramble_versatile(mainFolder, # where data is
                         expected_suffix_fl0,
                         expected_suffix_fl1,
                         expected_suffix_metadata,
                         fromImg, toImg, # negative==all
                         #
                         ADCcorrCDSFlag,
                         pedSubtractFlag,
                         ADCcorrFolder,
                         pedestalFolder,
                         #
                         lastFileOnlyFlag, # alternatively: process all files in folder
                         swapSmplRstFlag,
                         seqModHalfImgFlag, # this actually means: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
                         refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                         #
                         showFlag,
                         manyImgFlag, # select more than 1 digit image in interactive plot
                         #
                         saveFlag_1file, # save descramble DLSraw to 1 big file
                         saveFlag_multiFile, #saveFlag_multiFile= False # save descramble DLSraw to multiple files, using metadata name
                         saveAvgCDSFlag, # save 2D img (float): avg of ADCcorr, CDS, possibly ped-Subtracted
                         #
                         outFolder,
                         out_1file_suffix,
                         out_multiFile_suffix, 
                         out_imgXFile_multiFile,
                         out_AvgCDSfile_suffix,
                         #
                         cleanMemFlag,
                         highMemFlag,
                         verboseFlag)
#
#---
#%% profile it
#import cProfile
#cProfile.run('descramble_highMem(...)', sort='cumtime')
#%% or just execute it
#descramble_highMem(...)
