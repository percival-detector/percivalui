# -*- coding: utf-8 -*-
"""
4x250 calibrated (e) collections (from sbatch_rawraw_2_e_1k_4x250_ 1File/AllInFolder _fast_Launcher.sh) => load, show avg, sum 
(taking out the double images)
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3

python3 sbatch_rawraw_2_e_1k_4x250_PostViewer.py
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
dflt_folder_data2process= '/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/processed/example_of_data_processing/output_electrons/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_in_fileList=[]
dflt_in_fileList+=["2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_1:249_e.h5"]
dflt_in_fileList+=["2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_249:499_e.h5"]
dflt_in_fileList+=["2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_499:749_e.h5"]
dflt_in_fileList+=["2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_749:999_e.h5"]
#
dflt_Img2proc='10:998' # there are 999 images
#
dflt_showFlag='Y'; #dflt_showFlag='N'
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
    GUIwin_arguments+= ['000:249-file'];                   GUIwin_arguments+= [dflt_in_fileList[0]]
    GUIwin_arguments+= ['250:499-file'];                   GUIwin_arguments+= [dflt_in_fileList[1]]
    GUIwin_arguments+= ['500:749-file'];                   GUIwin_arguments+= [dflt_in_fileList[2]]
    GUIwin_arguments+= ['750:999-file'];                   GUIwin_arguments+= [dflt_in_fileList[3]]
    GUIwin_arguments+= ['process data: in Img [from:to]']; GUIwin_arguments+= [dflt_Img2proc]
    #
    GUIwin_arguments+= ['show results? [Y/N]']; GUIwin_arguments+= [dflt_showFlag] 
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
    in_fileList=[]
    in_fileList+=[dataFromUser[i_param]]; i_param+=1
    in_fileList+=[dataFromUser[i_param]]; i_param+=1
    in_fileList+=[dataFromUser[i_param]]; i_param+=1
    in_fileList+=[dataFromUser[i_param]]; i_param+=1
    #
    Img2proc_mtlb=       dataFromUser[i_param]; i_param+=1
    #
    showFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    cleanMemFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    verboseFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
else:
    folder_data2process= dflt_folder_data2process 
    in_fileList= dflt_in_fileList
    Img2proc_mtlb=       dflt_Img2proc
    #
    showFlag= APy3_GENfuns.isitYes(str(dflt_showFlag))
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dflt_highMemFlag)) 
    cleanMemFlag= APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag=  APy3_GENfuns.isitYes(str(dflt_verboseFlag))
# ---
Img2proc= APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1]
# ---
# what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will process data from {0}'.format(folder_data2process),'blue')
    for thisFile in in_fileList: APy3_GENfuns.printcol('  {0}'.format(thisFile),'blue')
    APy3_GENfuns.printcol('will elaborate Img{0}'.format(Img2proc_mtlb),'blue')
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
#---
##% load files
data_e= numpy.zeros((0,NRow,NCol))
for iFile,thisFile in enumerate(in_fileList):
    (thisNImg, ignNR,ignNC)= APy3_GENfuns.size_1xh5(folder_data2process+thisFile, '/data/data')
    if verboseFlag:
        if (iFile==0): APy3_GENfuns.printcol("loading and {0} Images from {1}".format(thisNImg,thisFile),'green')
        else: APy3_GENfuns.printcol("loading and 1+{0} Images from {1}".format(thisNImg-1,thisFile),'green')
    this_e= APy3_GENfuns.read_1xh5(folder_data2process+thisFile, '/data/data')
    if (iFile==0): data_e= numpy.append(data_e[:,:,:], this_e, axis=0)
    else: data_e= numpy.append(data_e[1:,:,:], this_e, axis=0) #need to take out the first
    del this_e
if verboseFlag: APy3_GENfuns.printcol("tot {0} Image put together".format(data_e.shape[0]),'green')
#
#%% CMA, CDS, LatOvlw, e

if showFlag: 
    APy3_GENfuns.plot_2D_all(numpy.mean(data_e[Img2proc[0]:(Img2proc[-1]+1),:,:], axis=0),False, 'col','row','avg {0} [e]'.format(Img2proc_mtlb),True)
    APy3_GENfuns.plot_2D_all(numpy.mean(data_e[Img2proc[0]:(Img2proc[-1]+1),:,:], axis=0),True, 'col','row','avg {0} [e]'.format(Img2proc_mtlb),True)
    APy3_GENfuns.plot_2D_all(numpy.sum(data_e[Img2proc[0]:(Img2proc[-1]+1),:,:], axis=0),False, 'col','row','sum {0} [e]'.format(Img2proc_mtlb),True)
    APy3_GENfuns.plot_2D_all(numpy.sum(data_e[Img2proc[0]:(Img2proc[-1]+1),:,:], axis=0),True, 'col','row','sum {0} [e]'.format(Img2proc_mtlb),True)

    APy3_GENfuns.showIt()

#---
# that's all folks
if verboseFlag: 
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    endTime=time.time()
    if verboseFlag: APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green') 
    for i_aux in range(3): APy3_GENfuns.printcol('---------','blue')




