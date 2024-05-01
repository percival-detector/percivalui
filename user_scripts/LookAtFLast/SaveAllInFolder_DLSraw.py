# -*- coding: utf-8 -*-
"""
descramble and visualize/save all scrambled dataset in a folder
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./SaveAllInFolder_DLSraw.py
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
lastFileOnlyFlag= False # alternatively: process all files in folder
#
swapSmplRstFlag= True
seqModHalfImgFlag= False # this actually means: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
refColH1_0_Flag = False # True if refcol data are streamed out as H1<0> data.
#
showFlag= False
manyImgFlag= True # select more than 1 digit image in interactive plot
#
saveFlag_1file= True # save descramble DLSraw to 1 big file
saveFlag_multiFile= False; #saveFlag_multiFile= False # save descramble DLSraw to multiple files, using metadata name
#
cleanMemFlag= True # this actually mean: save descrambled image (DLSraw standard)
highMemFlag= True; #highMemFlag= False
verboseFlag= True
#
#---
#
#

#%% data from here

#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_04_PGABBB/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_05_PGA6BB/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_04_PGABBB/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_05_PGA6BB/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_7of7ADC_biasBSI04_05_PGA6/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/scrmbld/"
#mainFolder= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/scrmbld/"

if mainFolder[-1]!='/': mainFolder+='/'
expected_suffix_fl0= '000000.h5'
expected_suffix_fl1= '000001.h5'

expected_suffix_metadata= 'xxx'
#
fromImg=0; toImg=-1 # negative==all/
#fromImg=500; toImg=550 # negative==all
#
outFolder=mainFolder+ '../DLSraw/'
if outFolder[-1]!='/': outFolder+='/'
#
out_1file_suffix= "DLSraw.h5"

out_multiFile_suffix= ".h5"
out_imgXFile_multiFile= 10
#
# ---
ADCcorrCDSFlag=False
pedSubtractFlag=False
saveAvgCDSFlag=False # save 2D img (float): avg of ADCcorr, CDS, possibly ped-Subtracted
#
ADCcorrFolder= 'xxx'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
pedestalFolder= 'xxx'
if pedestalFolder[-1]!='/': pedestalFolder+='/'
out_AvgCDSfile_suffix= "xxx.h5"

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
