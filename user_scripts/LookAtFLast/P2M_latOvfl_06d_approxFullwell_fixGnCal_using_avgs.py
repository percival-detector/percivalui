# -*- coding: utf-8 -*-
"""
avgxGn (ADU) sweeps in fixGn => e => fing max - x% => use an approx for full well => h5

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
cd /home/marras/PercAuxiliaryTools/LookAtFLast
python3 ./LatOvfl_04a_fixGn_evalCharge.py
or:
python3
exec(open("./xxx.py").read())
"""

#%% imports and useful constants
from APy3_auxINIT import *
import ast # ast.literal_eval()
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
#
interactiveGUIFlag= True; #interactiveGUIFlag= False
#
# ---
# functions if any
#---
#
#%% defaults for GUI window
#
#'''
#### BSI04, 7/7ADC: FixGn0,PGAB ####
dflt_datafolder= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/avg_std/'
if dflt_datafolder[-1]!='/': dflt_datafolder+='/'
dflt_File_prefix= "BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_"
dflt_File_suffix= "_500lgh_CDS_avg.h5"
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12c_Gn012_MultiGnCal_excludeBadPix.h5"
#
dflt_alternPed_file='NONE'
#
dflt_label_plot='BSI04,fixGn(high),approx'
#dflt_pngFolder= 'NONE'
dflt_pngFolder= '/home/marras/auximg/'
#
dflt_max_e=0.9   #0.9 #up to 90% of max
dflt_saveFile=dflt_multiGnCal_file+ '_approxFullWell.h5'
#dflt_saveFile= 'NONE'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'


#'''
#
'''
#### BSI04, 7/7ADC: FixGn0,PGA6 ####
dflt_datafolder= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/'
if dflt_datafolder[-1]!='/': dflt_datafolder+='/'
#
dflt_File_prefix= "BSI04_Tm20_7of7_biasBSI04_05_fixGn0_"
dflt_File_suffix= "_30lgh_Gn0_ADU_CDS_avg.h5"
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGA6_2020.06.06_fixGnCal_from3of7gapsAvg.h5"
dflt_alternPed_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.10.43_BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_label_plot='BSI04,fixGn(very-high)'
#dflt_pngFolder= 'NONE'
dflt_pngFolder= '/home/marras/auximg/'
#
dflt_max_e=0.9   #0.9 #up to 90% of max
dflt_saveFile=dflt_multiGnCal_file+ '_approxFullWell.h5'
#dflt_saveFile= 'NONE'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'
#'''
#
'''
#### BSI04, 7/7ADC: FixGn1,PGAB ####
dflt_datafolder= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/'
if dflt_datafolder[-1]!='/': dflt_datafolder+='/'
#
dflt_File_prefix= "BSI04_Tm20_7of7_biasBSI04_05_fixGn1_"
dflt_File_suffix= "_30lgh_Gn0_ADU_CDS_avg.h5"
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn1_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_alternPed_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.12.17_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_label_plot='BSI04,fixGn(medium)'
#dflt_pngFolder= 'NONE'
dflt_pngFolder= '/home/marras/auximg/'
#
dflt_max_e=0.9   #0.9 #up to 90% of max
dflt_saveFile=dflt_multiGnCal_file+ '_approxFullWell.h5'
#dflt_saveFile= 'NONE'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'
#'''
#
'''
#### BSI04, 7/7ADC: FixGn2,PGAB ####
dflt_datafolder= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/'
if dflt_datafolder[-1]!='/': dflt_datafolder+='/'
#
dflt_File_prefix= "BSI04_Tm20_7of7_biasBSI04_05_fixGn2_"
dflt_File_suffix= "_30lgh_Gn0_ADU_CDS_avg.h5"
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn2_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_alternPed_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.13.33_BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_label_plot='BSI04,fixGn(low)'
#dflt_pngFolder= 'NONE'
dflt_pngFolder= '/home/marras/auximg/'
#
dflt_max_e=0.9   #0.9 #up to 90% of max
dflt_saveFile=dflt_multiGnCal_file+ '_approxFullWell.h5'
#dflt_saveFile= 'NONE'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'
#'''

#
# ---
if interactiveGUIFlag:
    #%% pack arguments for GUI window
    GUIwin_arguments= []
    GUIwin_arguments+= ['ADU data: folder'] 
    GUIwin_arguments+= [dflt_datafolder]
    GUIwin_arguments+= ['ADU data: file prefix'] 
    GUIwin_arguments+= [dflt_File_prefix]
    GUIwin_arguments+= ['ADU data: file suffix'] 
    GUIwin_arguments+= [dflt_File_suffix]
    GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
    GUIwin_arguments+= [dflt_multiGnCal_file]
    GUIwin_arguments+= ['alternate PedestalADU (Gn0) file [NONE not to use]'] 
    GUIwin_arguments+= [dflt_alternPed_file]
    GUIwin_arguments+= ['plot label'] 
    GUIwin_arguments+= [dflt_label_plot]
    #
    GUIwin_arguments+= ['sava png to folder instead of showing [NONE not to]']
    GUIwin_arguments+= [dflt_pngFolder]
    #
    GUIwin_arguments+= ['fit: (to avoid saturation): use up to x of the max e [between 0 and 1]']
    GUIwin_arguments+= [dflt_max_e]
    #
    GUIwin_arguments+= ['save estimated full well to file [NONE not to]']
    GUIwin_arguments+= [dflt_saveFile]
    #
    GUIwin_arguments+= ['high memory usage? [Y/N]']
    GUIwin_arguments+= [str(dflt_highMemFlag)] 
    GUIwin_arguments+= ['clean memory when possible? [Y/N]']
    GUIwin_arguments+= [str(dflt_cleanMemFlag)] 
    GUIwin_arguments+= ['verbose? [Y/N]']
    GUIwin_arguments+= [str(dflt_verboseFlag)]
    #---
    #%% GUI window
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    i_param=0
    #
    datafolder=       dataFromUser[i_param]; i_param+=1
    File_prefix=      dataFromUser[i_param]; i_param+=1
    File_suffix=      dataFromUser[i_param]; i_param+=1
    multiGnCal_file= dataFromUser[i_param]; i_param+=1
    alternPed_file=  dataFromUser[i_param]; i_param+=1
    label_plot=  dataFromUser[i_param]; i_param+=1
    #
    pngFolder= dataFromUser[i_param]; i_param+=1
    #
    max_e=     float(dataFromUser[i_param]); i_param+=1
    #
    saveFile= dataFromUser[i_param]; i_param+=1
    #
    highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #---
else:
    # non-GUI
    datafolder=       dflt_datafolder
    File_prefix=      dflt_File_prefix
    File_suffix=      dflt_File_suffix
    multiGnCal_file= dflt_multiGnCal_file
    alternPed_file=  dflt_alternPed_file
    label_plot= dflt_label_plot
    #
    pngFolder= dflt_pngFolder
    #
    max_e=     float(dflt_max_e)
    #
    saveFile= dflt_saveFile
    #
    highMemFlag=  APy3_GENfuns.isitYes(dflt_highMemFlag)
    cleanMemFlag= APy3_GENfuns.isitYes(dflt_cleanMemFlag)
    verboseFlag=  APy3_GENfuns.isitYes(dflt_verboseFlag)
#---
#%% understanding parameters
if (alternPed_file in APy3_GENfuns.NOlist): alternPedFlag= False
else: alternPedFlag= True
#
if (pngFolder in APy3_GENfuns.NOlist): pngFlag= False
else: pngFlag= True
#
if (saveFile in APy3_GENfuns.NOlist): saveFlag= False
else: saveFlag= True
#---
#
#%% what's up doc
if True:
    APy3_GENfuns.printcol('will process ADU data:','blue')
    APy3_GENfuns.printcol('  from folder: '+datafolder,'blue')
    APy3_GENfuns.printcol('  files: '+File_prefix+ " * " +File_prefix,'blue')
    APy3_GENfuns.printcol('  e/ADU: '+multiGnCal_file,'blue')
    if alternPedFlag: APy3_GENfuns.printcol('  ADU0: '+alternPed_file,'blue')
    else: APy3_GENfuns.printcol('  ADU0: from '+multiGnCal_file,'blue')
    #
    APy3_GENfuns.printcol('will use the value {0} of the max e (to avoid saturation) to eval the full-well'.format(max_e),'blue')
    if saveFlag: APy3_GENfuns.printcol('will save fullwell parameters to '+saveFile,'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')

#---
#%% param files
APy3_GENfuns.printcol('loading param files:','blue')
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
if alternPedFlag: PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_warn_1xh5(alternPed_file, '/data/data')
#---
#%% data files
APy3_GENfuns.printcol('loading data files:','blue')
fileList= APy3_GENfuns.list_files(datafolder, File_prefix, File_suffix)
APy3_GENfuns.printcol("{0} files found to evaluate".format(len(fileList)),'green')
data_e_3D= APy3_GENfuns.numpy_NaNs( (len(fileList),NRow,NCol) )
evalFullWell= APy3_GENfuns.numpy_NaNs( (NRow,NCol) )

for iFile,thisFile in enumerate(fileList):
    thisADU= APy3_GENfuns.read_warn_1xh5(datafolder+thisFile, '/data/data')
    data_e_3D[iFile,:,:]= (thisADU - PedestalADU_multiGn[0,:,:])*e_per_ADU_multiGn[0,:,:]
    del thisADU
    APy3_GENfuns.dot_every10th(iFile,len(fileList))
#---
#%% eval
evalFullWell= numpy.nanmax(data_e_3D, axis=0)*max_e
#---
#%% show
if pngFlag:
    APy3_GENfuns.png_2D_all(evalFullWell, False, 'col','row',"{0}: eval full-well [e]".format(label_plot), True, pngFolder+label_plot+'approxFullWell_2D.png')
    APy3_GENfuns.printcol("png saved to {0}".format(pngFolder),'green')
else:
    APy3_GENfuns.plot_2D_all(evalFullWell, False, 'col','row',"{0}: eval full-well [e]".format(label_plot), True)
    APy3_GENfuns.showIt()
#---
#%% save
if saveFile:
    APy3_GENfuns.write_1xh5(saveFile, evalFullWell, '/data/data')
    APy3_GENfuns.printcol("data saved to {0}".format(saveFile),'blue')
#---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




