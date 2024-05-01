# -*- coding: utf-8 -*-
"""
avg per Gn => switching points (min)  

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./xxx.py
or:
python3
exec(open("./xxx.py").read())
"""
#
#%% imports and useful constants
from APy3_auxINIT import *
import APy3_WIPfunsFromHome
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#%% functions
#
def aux2histo(Ar2D):
    out2histo= numpy.copy(Ar2D.flatten())
    validMap= ~numpy.isnan(out2histo) 
    out2histo= numpy.copy(out2histo[validMap])
    return out2histo

# to FITfuns
#
# ---
#
#%% defaults for GUI window
#
#

#
'''
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn/'
dflt_suffix_Gn0= 'Gn0_ADU_CDS_avg.h5'
dflt_suffix_Gn1= 'Gn1_ADU_CDS_avg.h5'
dflt_suffix_Gn2= 'Gn2_ADU_CDS_avg.h5'
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5'
#
dflt_Row2proc=':'; dflt_Col2proc='350:1100' 
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'
dflt_pngFolder='/home/marras/auximg/'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
dflt_suffix_Gn0= 'Gn0_ADU_CDS_avg.h5'
dflt_suffix_Gn1= 'Gn1_ADU_Smpl_avg.h5'
dflt_suffix_Gn2= 'Gn1_ADU_Smpl_avg.h5'
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Row2proc=':'; dflt_Col2proc='350:1100'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'
dflt_pngFolder='/home/marras/auximg/'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
#### BSI04 3/7 bias BSI04_04 PGABBB v2 ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
dflt_suffix_Gn0= 'Gn0_ADU_CDS_avg.h5'
dflt_suffix_Gn1= 'Gn1_ADU_Smpl_avg.h5'
dflt_suffix_Gn2= 'Gn1_ADU_Smpl_avg.h5'
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
#
dflt_Row2proc=':'; dflt_Col2proc='350:1100'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'
dflt_pngFolder='/home/marras/auximg/'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
#'''
#### BSI04 3/7 bias BSI04_05 PGA6BB ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
dflt_suffix_Gn0= 'Gn0_ADU_CDS_avg.h5'
dflt_suffix_Gn1= 'Gn1_ADU_Smpl_avg.h5'
dflt_suffix_Gn2= 'Gn1_ADU_Smpl_avg.h5'
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5"
#
#dflt_Row2proc=':'; dflt_Col2proc='350:1100'
dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'
dflt_pngFolder='/home/marras/auximg/'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#'''


# ---
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['suffix of Gn0 files'] 
GUIwin_arguments+= [dflt_suffix_Gn0] 
GUIwin_arguments+= ['suffix of Gn1 files'] 
GUIwin_arguments+= [dflt_suffix_Gn1] 
GUIwin_arguments+= ['suffix of Gn2 files'] 
GUIwin_arguments+= [dflt_suffix_Gn2] 
#
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['process data: in Cols [from:to]'] 
GUIwin_arguments+= [dflt_Col2proc]
#
GUIwin_arguments+= ['show images? [Y/N]'] 
GUIwin_arguments+= [dflt_showFlag]
GUIwin_arguments+= ['save as png to a folder instad of saving [NONE not to]'] 
GUIwin_arguments+= [dflt_pngFolder]
#
GUIwin_arguments+= ['high mem usage? [Y/N]'] 
GUIwin_arguments+= [dflt_highMemFlag] 
GUIwin_arguments+= ['clean mem when possible? [Y/N]'] 
GUIwin_arguments+= [dflt_cleanMemFlag]
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [dflt_verboseFlag]
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
i_param=0
folder_data2process= dataFromUser[i_param]; i_param+=1

suffix_Gn0= dataFromUser[i_param]; i_param+=1
suffix_Gn1= dataFromUser[i_param]; i_param+=1
suffix_Gn2= dataFromUser[i_param]; i_param+=1
#
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
Row2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
Row2proc=APy3_P2Mfuns.matlabRow(Row2proc_mtlb)
#
Col2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
Col2proc=APy3_P2Mfuns.matlabCol(Col2proc_mtlb)
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
pngFolder= dataFromUser[i_param]; i_param+=1;
if pngFolder in APy3_GENfuns.NOlist: pngFlag= False
else: pngFlag= True
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
if True: 
    APy3_GENfuns.printcol('will process data: {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('ending in: {0} / {1} / {2}'.format(suffix_Gn0,suffix_Gn1,suffix_Gn2),'blue')
    APy3_GENfuns.printcol('will using multiGnCal_file {0})'.format(multiGnCal_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate pix({0},{1})'.format(Row2proc_mtlb,Col2proc_mtlb),'blue')
    #
    if (showFlag & (~pngFlag)): APy3_GENfuns.printcol('will show plots','blue')
    elif (showFlag & pngFlag):APy3_GENfuns.printcol('will save plots as png in '+pngFolder,'blue')
    #
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
# ---
APy3_GENfuns.printcol("reading files",'blue')
#%% read calibr
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
# ---
#%% read files
list_filesGn0= APy3_GENfuns.list_files(folder_data2process, '*', suffix_Gn0)
list_filesGn1= APy3_GENfuns.list_files(folder_data2process, '*', suffix_Gn1)
list_filesGn2= APy3_GENfuns.list_files(folder_data2process, '*', suffix_Gn2)
if verboseFlag: APy3_GENfuns.printcol("{0}+{1}+{2} files to be looked into".format(len(list_filesGn0),len(list_filesGn1),len(list_filesGn2)),'green')
alldataADU_Gn0= APy3_GENfuns.numpy_NaNs((len(list_filesGn0),NRow,NCol))
alldataADU_Gn1= APy3_GENfuns.numpy_NaNs((len(list_filesGn1),NRow,NCol))
alldataADU_Gn2= APy3_GENfuns.numpy_NaNs((len(list_filesGn2),NRow,NCol))
for iFile,thisFile in enumerate(list_filesGn0):
    alldataADU_Gn0[iFile, Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile,'/data/data')[Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]
    APy3_GENfuns.dot_every10th(iFile,len(list_filesGn0))
for iFile,thisFile in enumerate(list_filesGn1):
    alldataADU_Gn1[iFile,Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile,'/data/data')[Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]
    APy3_GENfuns.dot_every10th(iFile,len(list_filesGn1))
for iFile,thisFile in enumerate(list_filesGn2):
    alldataADU_Gn2[iFile,Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile,'/data/data')[Row2proc[0]:(Row2proc[-1]+1), Col2proc[0]:(Col2proc[-1]+1)]
    APy3_GENfuns.dot_every10th(iFile,len(list_filesGn2))
# ---
#%% proc data
APy3_GENfuns.printcol("processing data",'blue')
alldata_e_Gn0= (alldataADU_Gn0 - PedestalADU_multiGn[0,:,:])*e_per_ADU_multiGn[0,:,:]
alldata_e_Gn1= (alldataADU_Gn1 - PedestalADU_multiGn[1,:,:])*e_per_ADU_multiGn[1,:,:]
alldata_e_Gn2= (alldataADU_Gn2 - PedestalADU_multiGn[2,:,:])*e_per_ADU_multiGn[2,:,:]

sw01_min= APy3_GENfuns.numpy_NaNs((NRow,NCol))
sw12_min= APy3_GENfuns.numpy_NaNs((NRow,NCol))
#sw01_max= APy3_GENfuns.numpy_NaNs((NRow,NCol))
#sw12_max= APy3_GENfuns.numpy_NaNs((NRow,NCol))

sw01_min= numpy.nanmin(alldata_e_Gn1, axis=0)
sw12_min= numpy.nanmin(alldata_e_Gn2, axis=0)

#sw01_max= numpy.nanmax(alldata_e_Gn0, axis=0)
#sw12_max= numpy.nanmax(alldata_e_Gn1, axis=0)
# ---
#%% report
APy3_GENfuns.printcol("--  --  --  --",'green')
APy3_GENfuns.printcol("first switching Gn 0->1 in ({0},{1}):".format(Row2proc_mtlb,Col2proc_mtlb),'green')
APy3_GENfuns.printcol("  {0}e +/- {1}e".format(numpy.nanmean(sw01_min.flatten()),numpy.nanstd(sw01_min.flatten())),'green')
APy3_GENfuns.printcol("  calculated on {0} pixels".format(numpy.sum(~numpy.isnan(sw01_min))),'green')
APy3_GENfuns.printcol("--  --  --  --",'green')
APy3_GENfuns.printcol("first switching Gn 1->2 in ({0},{1}):".format(Row2proc_mtlb,Col2proc_mtlb),'green')
APy3_GENfuns.printcol("  {0}e +/- {1}e".format(numpy.nanmean(sw12_min.flatten()),numpy.nanstd(sw12_min.flatten())),'green')
APy3_GENfuns.printcol("  calculated on {0} pixels".format(numpy.sum(~numpy.isnan(sw12_min))),'green')
APy3_GENfuns.printcol("--  --  --  --",'green')
APy3_GENfuns.printcol("--  --  --  --",'green')
APy3_GENfuns.printcol("--  --  --  --",'green')
#APy3_GENfuns.printcol("last switching Gn 0->1 in ({0},{1}):".format(Row2proc_mtlb,Col2proc_mtlb),'green')
#APy3_GENfuns.printcol("  {0}e +/- {1}e".format(numpy.nanmean(sw01_max.flatten()),numpy.nanstd(sw01_max.flatten())),'green')
#APy3_GENfuns.printcol("  calculated on {0} pixels".format(numpy.sum(~numpy.isnan(sw01_max))),'green')
#APy3_GENfuns.printcol("--  --  --  --",'green')
#APy3_GENfuns.printcol("last switching Gn 1->2 in ({0},{1}):".format(Row2proc_mtlb,Col2proc_mtlb),'green')
#APy3_GENfuns.printcol("  {0}e +/- {1}e".format(numpy.nanmean(sw12_max.flatten()),numpy.nanstd(sw12_max.flatten())),'green')
#APy3_GENfuns.printcol("  calculated on {0} pixels".format(numpy.sum(~numpy.isnan(sw12_max))),'green')
#APy3_GENfuns.printcol("--  --  --  --",'green')
# ---
#%% show
Nhistobins=100
if (showFlag & (~pngFlag)):
    APy3_GENfuns.plot_histo1D(aux2histo(sw01_min), Nhistobins, False, 'switching point [e]','pixels','very high->medium Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb))
    APy3_GENfuns.plot_histo1D(aux2histo(sw12_min), Nhistobins, False, 'switching point [e]','pixels','medium->low Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb))
    #
    APy3_GENfuns.plot_2D_all(sw01_min,False, 'col','row','high->medium Gn: switching point [e]',True)
    APy3_GENfuns.plot_2D_all(sw12_min,False, 'col','row','medium->low Gn: switching point [e]',True)
    #
    #APy3_GENfuns.plot_histo1D(aux2histo(sw01_max), Nhistobins, False, 'MAX switching point [e]','pixels','MAX high->medium Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb) )
    #APy3_GENfuns.plot_histo1D(aux2histo(sw12_max), Nhistobins, False, 'MAX switching point [e]','pixels','MAX medium->low Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb) )
    #
    APy3_GENfuns.showIt()
elif (showFlag & pngFlag):
    APy3_GENfuns.png_histo1D(aux2histo(sw01_min), Nhistobins, False, 'switching point [e]','pixels','very high->medium Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb),pngFolder+'switchGn0to1_({0},{1})_1Dhisto.png'.format(Row2proc_mtlb,Col2proc_mtlb))
    APy3_GENfuns.png_histo1D(aux2histo(sw12_min), Nhistobins, False, 'switching point [e]','pixels','medium->low Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb),pngFolder+'switchGn1to2_({0},{1})_1Dhisto.png'.format(Row2proc_mtlb,Col2proc_mtlb))
    #
    APy3_GENfuns.png_2D_all(sw01_min,False, 'col','row','high->medium Gn: switching point [e]',True,pngFolder+'switchGn0to1_({0},{1})_2D.png'.format(Row2proc_mtlb,Col2proc_mtlb))
    APy3_GENfuns.png_2D_all(sw12_min,False, 'col','row','medium->low Gn: switching point [e]',True,pngFolder+'switchGn1to2_({0},{1})_2D.png'.format(Row2proc_mtlb,Col2proc_mtlb))

    #
    # max switching point makes no sense in this context
    #APy3_WIPfunsFromHome.png_histo1D(aux2histo(sw01_max), Nhistobins, False, 'MAX switching point [e]','pixels','MAX high->medium Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb), pngFolder+'MAXsw01')
    #APy3_WIPfunsFromHome.png_histo1D(aux2histo(sw12_max), Nhistobins, False, 'MAX switching point [e]','pixels','MAX medium->low Gn ({0},{1}):'.format(Row2proc_mtlb,Col2proc_mtlb),pngFolder+'MAXsw12')
    #
    APy3_GENfuns.printcol("png files saved to "+pngFolder,'green')
#
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
# ---
# ---
# ---

