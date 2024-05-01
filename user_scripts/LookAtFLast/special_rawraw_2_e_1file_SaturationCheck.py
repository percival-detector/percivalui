# -*- coding: utf-8 -*-
"""
1 calibrated (e) file (from sbatch_rawraw_2_e_1k_4x250_ 1File/AllInFolder _fast_Launcher.sh)
fullWell h5 files
1 descrambled (GnCrsFn) file (from sbatch_rawraw_2_GnCrsFn_1k_4x250_ 1File/AllInFolder _fast_Launcher.sh)
 => estimate saturated pixels, save to h5 
#
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3

python3 xxx.py
or:
start python
# execfile("xxx.py") # this is in python 2.7
exec(open("./sbatch_rawraw_2_e_1k_4x250_PostViewer.py").read()); print('Python3 is horrible')
"""

#%% imports and useful constants
from APy3_auxINIT import *

numpy.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings('ignore')
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
NGn=  APy3_P2Mfuns.NGn
NSmplRst= APy3_P2Mfuns.NSmplRst
NGnCrsFn= APy3_P2Mfuns.NGnCrsFn
iGn=0; iCrs=1; iFn=2

ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
#
# ---
interactiveFlag= False; interactiveFlag= True
# ---
#
#%% defaults for GUI window
#
#### timing ####
#using /asap3 files
dflt_folder_data2process= '/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/processed/example2_of_data_processing/output_electrons/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_fileprefix="2019.12.11.23.37.16_BSI04_7of7_3TPGA666_012ms_0250eV_5um_1kpin"
#
dflt_e_file= dflt_fileprefix+"_1:249_e.h5"
#"_249:499_e.h5"
#"_499:749_e.h5"
#"_749:999_e.h5"
#
dflt_GnCrsFn_file= dflt_fileprefix+"_1:249_GnCrsFn.h5"
#"_249:499_GnCrsFn.h5"
#"_499:749_GnCrsFn.h5"
#"_749:999_GnCrsFn.h5"
#
dflt_fullWell_file= '/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGA6_2020.06.06_fixGn_approxFullWell.h5'
dflt_maxSmplCrs= 30
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_highMemFlag='Y'; dflt_highMemFlag='N'  
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'; #dflt_highMemFlag='N'
#'''

# ---
#%% parameter loading
if interactiveFlag:
    # interactive GUI
    GUIwin_arguments= []
    GUIwin_arguments+= ['use data from folder'];           GUIwin_arguments+= [dflt_folder_data2process] 
    GUIwin_arguments+= ['data in electrons file'];                   GUIwin_arguments+= [dflt_e_file]
    GUIwin_arguments+= ['raw data file'];                   GUIwin_arguments+= [dflt_GnCrsFn_file]

    GUIwin_arguments+= ['full-well file in electrons']; GUIwin_arguments+= [dflt_fullWell_file]
    GUIwin_arguments+= ['raw-data max Crs value']; GUIwin_arguments+= [dflt_maxSmplCrs]
    #
    GUIwin_arguments+= ['save saturated maps? [Y/N]']; GUIwin_arguments+= [dflt_saveFlag] 
    #
    GUIwin_arguments+= ['high memory usage? [Y/N]'];          GUIwin_arguments+= [str(dflt_highMemFlag)] 
    GUIwin_arguments+= ['clean memory when possible? [Y/N]']; GUIwin_arguments+= [str(dflt_cleanMemFlag)] 
    GUIwin_arguments+= ['verbose? [Y/N]'];                    GUIwin_arguments+= [str(dflt_verboseFlag)] 
    # ---
    #
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    folder_data2process= dataFromUser[i_param]; i_param+=1
    #
    e_file=       dataFromUser[i_param]; i_param+=1
    GnCrsFn_file= dataFromUser[i_param]; i_param+=1
    #
    fullWell_file=       dataFromUser[i_param]; i_param+=1
    maxSmplCrs=          int(dataFromUser[i_param]); i_param+=1
    #
    saveFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    cleanMemFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    verboseFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
else:
    folder_data2process= dflt_folder_data2process 
    e_file=       dflt_e_file
    GnCrsFn_file= dflt_GnCrsFn_file
    #
    fullWell_file=dflt_fullWell_file
    maxSmplCrs=  dflt_maxSmplCrs
    #
    saveFlag= APy3_GENfuns.isitYes(str(dflt_saveFlag))
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dflt_highMemFlag)) 
    cleanMemFlag= APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag=  APy3_GENfuns.isitYes(str(dflt_verboseFlag))
# ---
# what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will process data from {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  electron: {0}'.format(e_file),'blue')
    APy3_GENfuns.printcol('  rew data: {0}'.format(GnCrsFn_file),'blue')
    #
    APy3_GENfuns.printcol('will mark saturated values if: ','blue')
    APy3_GENfuns.printcol('  electron data exceed fullwell from {0}'.format(fullWell_file),'blue')
    APy3_GENfuns.printcol('  raw data exceed {0}'.format(maxSmplCrs),'blue')
    #
    if saveFlag: APy3_GENfuns.printcol('will save satrureted maps to {0}'.format(folder_data2process),'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
if (verboseFlag): APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
APy3_GENfuns.printcol("-",'blue')
#---
##% load files
APy3_GENfuns.printcol("loading files",'blue')
fullWell_e= APy3_GENfuns.read_warn_1xh5(fullWell_file, '/data/data')
APy3_GENfuns.printcol("loaded fullwell file {0}".format(fullWell_file),'green')
#
data_e= APy3_GENfuns.read_warn_1xh5(folder_data2process+e_file, '/data/data')
APy3_GENfuns.printcol("loaded electron file {0}".format(folder_data2process+e_file),'green')
#
data_GnCrsFn= APy3_GENfuns.read_warn_1xh5(folder_data2process+GnCrsFn_file, '/data/data')
APy3_GENfuns.printcol("loaded raw data file {0}".format(folder_data2process+GnCrsFn_file),'green')
APy3_GENfuns.printcol("-",'blue')
#
##% eval saturation
APy3_GENfuns.printcol("evaluing saturation",'blue')
data_Saturated= numpy.zeros_like(data_e).astype(bool)
#
map_aboveFullwell=  data_e>fullWell_e
data_Saturated[map_aboveFullwell]=True
#
map_above_maxSmplCrs= data_GnCrsFn[:,APy3_P2Mfuns.iSmpl,:,:,APy3_P2Mfuns.iCrs]>maxSmplCrs
data_Saturated[map_above_maxSmplCrs]=True
#
APy3_GENfuns.printcol("{0} pixels are saturated in this file".format(numpy.sum(data_Saturated.flatten())),'green')
#
##%% save data
if saveFlag:
    saturatedFile= e_file[:(-4)]+"Saturated.h5"
    APy3_GENfuns.write_1xh5(folder_data2process+saturatedFile, data_Saturated, '/data/data')
    APy3_GENfuns.printcol("Saturation map saved as {0}".format(folder_data2process+saturatedFile),'green')
#
#---
# that's all folks
if verboseFlag: 
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    endTime=time.time()
    if verboseFlag: APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green') 
    for i_aux in range(3): APy3_GENfuns.printcol('---------','blue')




