# -*- coding: utf-8 -*-
"""
visualize small scrambled descrambled dataset (seq Mod)

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3

python3 ./LookAtDLSraw.py
or:
start python
# execfile("xxx.py") # this is in python 2.7
exec(open("./xxx.py").read()); print('Python3 is horrible')
"""

#%% imports and useful constants
from APy3_auxINIT import *
numpy.seterr(divide='ignore', invalid='ignore')
#
interactiveFlag= False; interactiveFlag= True
# ---
#
#%% parameters
dflt_file2show='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.15.23_first_5um_pinhole/examplesForWill/'+'example_1_10Img_DLSraw.h5'
dflt_img2proc_str= ":" # using the sensible matlab convention; "all",":","*" means all
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag= 'Y'
#---
#%% parameter loading
if interactiveFlag:
    # interactive GUI
    GUIwin_arguments= []
    GUIwin_arguments+= ['file to show'];         GUIwin_arguments+= [dflt_file2show] 
    GUIwin_arguments+= ['images [first:last]'];  GUIwin_arguments+= [dflt_img2proc_str]
    GUIwin_arguments+= ['clean mem when possible [Y/N]'];  GUIwin_arguments+= [str(dflt_cleanMemFlag)]
    GUIwin_arguments+= ['verbose? [Y/N]'];                 GUIwin_arguments+= [str(dflt_verboseFlag)]
    #
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    file2show= dataFromUser[i_param]; i_param+=1
    img2proc_str= dataFromUser[i_param]; i_param+=1
    cleanMemFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
else:
    file2show= dflt_file2show
    img2proc_str= dflt_img2proc_str
    cleanMemFlag= APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag= APy3_GENfuns.isitYes(str(dflt_verboseFlag))
# ---
# what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will read file {0}'.format(file2show),'blue')
    APy3_GENfuns.printcol('using images {0}'.format(img2proc_str),'blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean mem when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol('-','blue')
# ---
# load
if APy3_GENfuns.notFound(file2show): APy3_GENfuns.printErr('not found: '+file2show)
if verboseFlag:  APy3_GENfuns.printcol('reading all images from file'.format(img2proc_str),'blue')
if img2proc_str in APy3_GENfuns.ALLlist: 
    (inSmpl,inRst)= APy3_GENfuns.read_2xh5(file2show, '/data', '/reset')
else:
    aux_img2proc= APy3_GENfuns.matlab_like_range(img2proc_str)
    (inSmpl,inRst)= APy3_GENfuns.read_partial_2xh5(file2show, '/data', '/reset', aux_img2proc[0], aux_img2proc[-1])
(NImg,ignNRow,ignNCol)= inSmpl.shape
if verboseFlag: APy3_GENfuns.printcol('{0} image read from file'.format(NImg),'green')
# ---
# DLSraw => GnCrsFn
data_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(inSmpl,inRst, APy3_P2Mfuns.ERRDLSraw,APy3_P2Mfuns.ERRint16)
data_CDSavg=    APy3_GENfuns.numpy_NaNs((NRow,NCol))
data_CDSCMAavg= APy3_GENfuns.numpy_NaNs((NRow,NCol))
# ---
# interactive show
if verboseFlag:  APy3_GENfuns.printcol('interactive plot','blue')
APy3_P2Mfuns.percDebug_plot_interactive_wCMA(data_GnCrsFn,
                                data_CDSavg,data_CDSCMAavg,
                                False #manyImgFlag
                                )
#---
# that's all folks
if verboseFlag:  
    for i_aux in range(3): APy3_GENfuns.printcol('---------','blue')



