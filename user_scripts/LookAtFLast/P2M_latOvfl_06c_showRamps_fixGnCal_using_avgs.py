# -*- coding: utf-8 -*-
"""
avgxGn sweep in fixGn(n), and fixGn(n+1), 
also drks in fixGn(n), and fixGn(n+1) 
also e/ADU in fixGn(n), and fixGn(n+1) 
=> show ramps

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
#
'''
#### BSI04, 7/7ADC: FixGn0,PGA6 -> fixGn1,PGAB ####
dflt_folder_Gnknown= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/'
if dflt_folder_Gnknown[-1]!='/': dflt_folder_data2process+='/'
dflt_folder_Gnunkwn= dflt_folder_Gnknown
if dflt_folder_Gnunkwn[-1]!='/': dflt_folder_data2process+='/'
#
# tab-separated-text file: integr_time_in_ms<tab>GnX_avg
dflt_metaFile_avg_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD5.0_avg_meta.dat' 
dflt_metaFile_std_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD5.0_std_meta.dat' 
dflt_metaFile_avg_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD5.0_avg_meta.dat'
dflt_metaFile_std_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD5.0_std_meta.dat'
#
#dflt_metaFile_avg_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD4.0_avg_meta.dat' 
#dflt_metaFile_std_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD4.0_std_meta.dat' 
#dflt_metaFile_avg_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_avg_meta.dat'
#dflt_metaFile_std_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_std_meta.dat'
#
dflt_multiGnCal_file_Gnknown= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGA6_2020.06.06_fixGnCal_from3of7gapsAvg.h5"

dflt_multiGnCal_file_Gnunkwn= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn1_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"

#
dflt_alternPed_file_Gnknown='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.10.43_BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
dflt_alternPed_file_Gnunkwn='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.12.17_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_label_Gnknown='very-high gain'
dflt_label_Gnunkwn='medium gain'
#
#dflt_Rows2proc='0:1483'
#dflt_Cols2proc='32:1439'
dflt_Rows2proc='Interactive'  
dflt_Cols2proc='Interactive' 
#
dflt_showRampsFlag='Y'; dflt_showRampsFlag='N'
dflt_pngFolder= 'NONE'
#dflt_pngFolder= '/home/marras/auximg/'
#
dflt_fit_maxADU=0.75   #0.9 #up to 90% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=4 #10 #4pt for having 2ke v.high-> med gn pixels
dflt_fit_slope=0.0 #10 #4pt for having 2ke v.high-> med gn pixels
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'
#'''
#
#'''
#### BSI04, 7/7ADC: FixGn1,PGAB -> fixGn2,PGAB ####
dflt_folder_Gnknown= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/'
if dflt_folder_Gnknown[-1]!='/': dflt_folder_data2process+='/'
dflt_folder_Gnunkwn= dflt_folder_Gnknown
if dflt_folder_Gnunkwn[-1]!='/': dflt_folder_data2process+='/'
#
# tab-separated-text file: integr_time_in_ms<tab>GnX_avg 
#
dflt_metaFile_avg_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD3.0_avg_meta.dat'
dflt_metaFile_std_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD3.0_std_meta.dat' 
dflt_metaFile_avg_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD3.0_avg_meta.dat'
dflt_metaFile_std_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD3.0_std_meta.dat'
#
#dflt_metaFile_avg_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD2.0_avg_meta.dat'
#dflt_metaFile_std_Gnknown= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD2.0_std_meta.dat' 
#dflt_metaFile_avg_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_avg_meta.dat'
#dflt_metaFile_std_Gnunkwn= 'BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_std_meta.dat'
#
dflt_multiGnCal_file_Gnknown= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn1_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_multiGnCal_file_Gnunkwn= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn2_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_alternPed_file_Gnknown='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.12.17_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
dflt_alternPed_file_Gnunkwn='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'+'../avg_xGn/2020.06.06.22.13.33_BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_label_Gnknown='medium gain'
dflt_label_Gnunkwn='low gain'
#
#dflt_Rows2proc='0:1483'
#dflt_Cols2proc='32:1439'
dflt_Rows2proc='Interactive'  
dflt_Cols2proc='Interactive' 
#
dflt_showRampsFlag='Y'; dflt_showRampsFlag='N'
dflt_pngFolder= 'NONE'
#
dflt_fit_maxADU=0.75   #0.9 #up to 90% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=4 #10 #4pt for having 2ke v.high-> med gn pixels
dflt_fit_slope=0.0 #10 #4pt for having 2ke v.high-> med gn pixels
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'; dflt_verboseFlag='Y'
#'''
#

#
# ---
if interactiveGUIFlag:
    #%% pack arguments for GUI window
    GUIwin_arguments= []
    GUIwin_arguments+= ['known-Gn ADU data: folder'] 
    GUIwin_arguments+= [dflt_folder_Gnknown]
    GUIwin_arguments+= ['known-Gn ADU avg meta file: folder'] 
    GUIwin_arguments+= [dflt_metaFile_avg_Gnknown]
    GUIwin_arguments+= ['known-Gn ADU std meta file: folder'] 
    GUIwin_arguments+= [dflt_metaFile_std_Gnknown]
    GUIwin_arguments+= ['known-Gn multiGnCal (PedestalADU, e/ADU): file'] 
    GUIwin_arguments+= [dflt_multiGnCal_file_Gnknown]
    GUIwin_arguments+= ['known-Gn alternate PedestalADU (Gn0) file [NONE not to use]'] 
    GUIwin_arguments+= [dflt_alternPed_file_Gnknown]
    GUIwin_arguments+= ['known-Gn label [very-high gain/high gain/medium gain/low gain]'] 
    GUIwin_arguments+= [dflt_label_Gnknown]
    #
    GUIwin_arguments+= ['unknown-Gn ADU data: folder'] 
    GUIwin_arguments+= [dflt_folder_Gnunkwn]
    GUIwin_arguments+= ['unknown-Gn ADU avg meta file: folder'] 
    GUIwin_arguments+= [dflt_metaFile_avg_Gnunkwn]
    GUIwin_arguments+= ['unknown-Gn ADU std meta file: folder'] 
    GUIwin_arguments+= [dflt_metaFile_std_Gnunkwn]
    GUIwin_arguments+= ['unknown-Gn multiGnCal (PedestalADU, e/ADU): file [NONE not to use]']
    GUIwin_arguments+= [dflt_multiGnCal_file_Gnunkwn]
    GUIwin_arguments+= ['unknown-Gn alternate PedestalADU (Gn0) file'] 
    GUIwin_arguments+= [dflt_alternPed_file_Gnunkwn]
    GUIwin_arguments+= ['unknown-Gn label [very-high gain/high gain/medium gain/low gain]'] 
    GUIwin_arguments+= [dflt_label_Gnunkwn]
    #
    GUIwin_arguments+= ['process data: in Rows [from:to / Interactive]'] 
    GUIwin_arguments+= [dflt_Rows2proc]
    GUIwin_arguments+= ['process data: in columns [from:to / Interactive]'] 
    GUIwin_arguments+= [dflt_Cols2proc] 
    GUIwin_arguments+= ['show single ramps? [Y/N ; will be Y if interactive]']
    GUIwin_arguments+= [dflt_showRampsFlag]
    GUIwin_arguments+= ['sava png to folder instead of showing [NONE not to]']
    GUIwin_arguments+= [dflt_pngFolder]
    #
    GUIwin_arguments+= ['fit: (to avoid saturation): use up to x of the max ADU [between 0 and 1]']
    GUIwin_arguments+= [dflt_fit_maxADU]
    GUIwin_arguments+= ['fit: R2 at least?']
    GUIwin_arguments+= [dflt_fit_minR2]
    GUIwin_arguments+= ['fit: at least on how many points?']
    GUIwin_arguments+= [dflt_fit_minNpoints]
    GUIwin_arguments+= ['fit: minimum ADU/ms slope (if satutated, can give artefacts <0)']
    GUIwin_arguments+= [dflt_fit_slope]
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
    folder_Gnknown=       dataFromUser[i_param]; i_param+=1
    metaFile_avg_Gnknown= dataFromUser[i_param]; i_param+=1
    metaFile_std_Gnknown= dataFromUser[i_param]; i_param+=1
    multiGnCal_file_Gnknown= dataFromUser[i_param]; i_param+=1
    alternPed_file_Gnknown=  dataFromUser[i_param]; i_param+=1
    label_Gnknown=  dataFromUser[i_param]; i_param+=1
    #
    folder_Gnunkwn=       dataFromUser[i_param]; i_param+=1
    metaFile_avg_Gnunkwn= dataFromUser[i_param]; i_param+=1
    metaFile_std_Gnunkwn= dataFromUser[i_param]; i_param+=1
    multiGnCal_file_Gnunkwn= dataFromUser[i_param]; i_param+=1
    alternPed_file_Gnunkwn= dataFromUser[i_param]; i_param+=1
    label_Gnunkwn=  dataFromUser[i_param]; i_param+=1
    #
    Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1
    Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1
    showRampsFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    pngFolder= dataFromUser[i_param]; i_param+=1
    #
    fit_maxADU=     float(dataFromUser[i_param]); i_param+=1
    fit_minR2=      float(dataFromUser[i_param]); i_param+=1
    fit_minNpoints= int(dataFromUser[i_param]); i_param+=1
    fit_slope=      float(dataFromUser[i_param]); i_param+=1
    #
    highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #---
else:
    # non-GUI
    folder_Gnknown=       dflt_folder_Gnknown
    metaFile_avg_Gnknown= dflt_metaFile_avg_Gnknown
    metaFile_std_Gnknown= dflt_metaFile_std_Gnknown
    multiGnCal_file_Gnknown= dflt_multiGnCal_file_Gnknown
    alternPed_file_Gnknown=  dflt_alternPed_file_Gnknown
    label_Gnknown= dflt_label_Gnknown
    #
    folder_Gnunkwn=       dflt_folder_Gnunkwn
    metaFile_avg_Gnunkwn= dflt_metaFile_avg_Gnunkwn
    metaFile_std_Gnunkwn= dflt_metaFile_std_Gnunkwn
    multiGnCal_file_Gnunkwn= dflt_multiGnCal_file_Gnunkwn
    alternPed_file_Gnunkwn= dflt_alternPed_file_Gnunkwn
    label_Gnunkwn= dflt_label_Gnunkwn
    #
    Rows2proc_mtlb= dflt_Rows2proc
    Cols2proc_mtlb= dflt_Cols2proc
    showRampsFlag= APy3_GENfuns.isitYes(dflt_showRampsFlag)
    pngFolder= dflt_pngFolder
    #
    fit_maxADU=     float(dflt_fit_maxADU)
    fit_minR2=      float(dflt_fit_minR2)
    fit_minNpoints= int(dflt_fit_minNpoints)
    fit_slope=      float(dflt_fit_slope)
    #
    #
    highMemFlag=  APy3_GENfuns.isitYes(dflt_highMemFlag)
    cleanMemFlag= APy3_GENfuns.isitYes(dflt_cleanMemFlag)
    verboseFlag=  APy3_GENfuns.isitYes(dflt_verboseFlag)
#---
#%% understanding parameters
if (alternPed_file_Gnknown in APy3_GENfuns.NOlist): alternPedFlag_Gnknown= False
else: alternPedFlag_Gnknown= True
if (alternPed_file_Gnunkwn in APy3_GENfuns.NOlist): alternPedFlag_Gnunkwn= False
else: alternPedFlag_Gnunkwn= True
# 
if (Rows2proc_mtlb in APy3_GENfuns.INTERACTLVElist) or  (Cols2proc_mtlb in APy3_GENfuns.INTERACTLVElist):
    interactiveShowFlag=True; showRampsFlag=True
    Rows2proc_mtlb= 'Interactive'; Cols2proc_mtlb= 'Interactive'
    Rows2proc=numpy.arange(NRow); Cols2proc=numpy.arange(NCol)
else:
    interactiveShowFlag=False
    if Rows2proc_mtlb in APy3_GENfuns.ALLlist: Rows2proc= numpy.arange(NRow)
    else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 
    if Cols2proc_mtlb in APy3_GENfuns.ALLlist: Cols2proc= numpy.arange(32,NCol)
    else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
#
if (pngFolder in APy3_GENfuns.NOlist): pngFlag= False
else: pngFlag= True
#
#---
#
#%% what's up doc
if True:
    APy3_GENfuns.printcol('will process known-Gn ADU data:','blue')
    APy3_GENfuns.printcol('  avg: '+folder_Gnknown+metaFile_avg_Gnknown,'blue')
    APy3_GENfuns.printcol('  std: '+folder_Gnknown+metaFile_std_Gnknown,'blue')
    APy3_GENfuns.printcol('  e/ADU: '+multiGnCal_file_Gnknown,'blue')
    if alternPedFlag_Gnknown: APy3_GENfuns.printcol('  ADU0: '+alternPed_file_Gnknown,'blue')
    else: APy3_GENfuns.printcol('  ADU0: from '+multiGnCal_file_Gnknown,'blue')
    #
    APy3_GENfuns.printcol('will process unknown-Gn ADU data:','blue')
    APy3_GENfuns.printcol('  avg: '+folder_Gnunkwn+metaFile_avg_Gnunkwn,'blue')
    APy3_GENfuns.printcol('  std: '+folder_Gnunkwn+metaFile_std_Gnunkwn,'blue')
    APy3_GENfuns.printcol('  e/ADU: '+multiGnCal_file_Gnunkwn,'blue')
    APy3_GENfuns.printcol('  ADU0: '+alternPed_file_Gnunkwn,'blue')
    #
    APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}'.format(Cols2proc_mtlb,Rows2proc_mtlb),'blue')
    if interactiveShowFlag: 
        if pngFlag: APy3_GENfuns.printcol('saving png ramps in '.format(pngFolder),'blue')
        else: APy3_GENfuns.printcol('showing ramps','blue')
    #
    APy3_GENfuns.printcol('fitting:','blue')
    APy3_GENfuns.printcol('  using up to {0} of the max ADU (to avoid saturation)'.format(fit_maxADU),'blue')
    APy3_GENfuns.printcol('  using R2>= {0}'.format(fit_minR2),'blue')
    APy3_GENfuns.printcol('  at least {0} points'.format(fit_minNpoints),'blue')
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
#%% param and meta files
APy3_GENfuns.printcol('loading param and meta files:','blue')
if APy3_GENfuns.notFound(multiGnCal_file_Gnknown): APy3_GENfuns.printErr('not found: '+multiGnCal_file_Gnknown)
(PedestalADU_multiGn_Gnknown,e_per_ADU_multiGn_Gnknown)= APy3_GENfuns.read_2xh5(multiGnCal_file_Gnknown, '/Pedestal_ADU/', '/e_per_ADU/')
if alternPedFlag_Gnknown: PedestalADU_multiGn_Gnknown[0,:,:]= APy3_GENfuns.read_warn_1xh5(alternPed_file_Gnknown, '/data/data')
PedestalADU_multiGn_Gnknown[1:3,:,:]= numpy.NaN
e_per_ADU_multiGn_Gnknown[1:3,:,:]= numpy.NaN
#
if APy3_GENfuns.notFound(multiGnCal_file_Gnunkwn): APy3_GENfuns.printErr('not found: '+multiGnCal_file_Gnunkwn)
(PedestalADU_multiGn_Gnunkwn,e_per_ADU_multiGn_Gnunkwn)= APy3_GENfuns.read_2xh5(multiGnCal_file_Gnunkwn, '/Pedestal_ADU/', '/e_per_ADU/')
if alternPedFlag_Gnunkwn: PedestalADU_multiGn_Gnunkwn[0,:,:]= APy3_GENfuns.read_warn_1xh5(alternPed_file_Gnunkwn, '/data/data')
#
if APy3_GENfuns.notFound(folder_Gnknown+metaFile_avg_Gnknown): APy3_GENfuns.printErr('not found: '+folder_Gnknown+metaFile_avg_Gnknown)
fileContent_avg_Gnknown= APy3_GENfuns.read_tst(folder_Gnknown+metaFile_avg_Gnknown)
(NSets_avg,N2_avg)= numpy.array(fileContent_avg_Gnknown).shape
if N2_avg!=2: APy3_GENfuns.printErr("Gn known metafile: {0} columns (2 expected)".format(N2_avg))
APy3_GENfuns.printcol('Gn known avg metafile: {0} data sets'.format(NSets_avg),'green')
#
if APy3_GENfuns.notFound(folder_Gnknown+metaFile_std_Gnknown): APy3_GENfuns.printErr('not found: '+folder_Gnknown+metaFile_std_Gnknown)
fileContent_std_Gnknown= APy3_GENfuns.read_tst(folder_Gnknown+metaFile_std_Gnknown)
(NSets_std,N2_std)= numpy.array(fileContent_std_Gnknown).shape
if (N2_std!=2)  : APy3_GENfuns.printErr("Gn known std metafile: {0} columns, {1} rows ({2} cols, {3} rows expected)".format(N2_std, NSets_std, N2_avg, NSets_avg))
#
intTimes_ms_Gnknown=[]
fileList_avg_Gnknown=[]; fileList_std_Gnknown=[]
for iSet in range(NSets_avg):
    intTimes_ms_Gnknown+= [float(fileContent_avg_Gnknown[iSet][0])]
    fileList_avg_Gnknown+= [fileContent_avg_Gnknown[iSet][1]]
    fileList_std_Gnknown+= [fileContent_std_Gnknown[iSet][1]]
intTimes_ms_Gnknown= numpy.array(intTimes_ms_Gnknown)
#
del NSets_avg; del N2_avg; del NSets_std; del N2_std
del fileContent_avg_Gnknown; del fileContent_std_Gnknown
#
if APy3_GENfuns.notFound(folder_Gnunkwn+metaFile_avg_Gnunkwn): APy3_GENfuns.printErr('not found: '+folder_Gnunkwn+metaFile_avg_Gnunkwn)
fileContent_avg_Gnunkwn= APy3_GENfuns.read_tst(folder_Gnunkwn+metaFile_avg_Gnunkwn)
(NSets_avg,N2_avg)= numpy.array(fileContent_avg_Gnunkwn).shape
if N2_avg!=2: APy3_GENfuns.printErr("Gn unknown metafile: {0} columns (2 expected)".format(N2_avg))
APy3_GENfuns.printcol('Gn unknown avg metafile: {0} data sets'.format(NSets_avg),'green')
#
if APy3_GENfuns.notFound(folder_Gnunkwn+metaFile_std_Gnunkwn): APy3_GENfuns.printErr('not found: '+folder_Gnunkwn+metaFile_std_Gnunkwn)
fileContent_std_Gnunkwn= APy3_GENfuns.read_tst(folder_Gnunkwn+metaFile_std_Gnunkwn)
(NSets_std,N2_std)= numpy.array(fileContent_std_Gnunkwn).shape
if (N2_std!=2)  : APy3_GENfuns.printErr("Gn unknown std metafile: {0} columns, {1} rows ({2} cols, {3} rows expected)".format(N2_std, NSets_std, N2_avg, NSets_avg))
#
intTimes_ms_Gnunkwn=[]
fileList_avg_Gnunkwn=[]; fileList_std_Gnunkwn=[]
for iSet in range(NSets_avg):
    intTimes_ms_Gnunkwn+= [float(fileContent_avg_Gnunkwn[iSet][0])]
    fileList_avg_Gnunkwn+= [fileContent_avg_Gnunkwn[iSet][1]]
    fileList_std_Gnunkwn+= [fileContent_std_Gnunkwn[iSet][1]]
intTimes_ms_Gnunkwn= numpy.array(intTimes_ms_Gnunkwn)
#
del NSets_avg; del N2_avg; del NSets_std; del N2_std
del fileContent_avg_Gnunkwn; del fileContent_std_Gnunkwn
#---


#%% read data files
APy3_GENfuns.printcol("reading known-Gn data files",'blue')
NSets_Gnknown= len(fileList_avg_Gnknown)
dataADU_avg_Gnknown_3DAr= APy3_GENfuns.numpy_NaNs((NSets_Gnknown,NRow,NCol))
dataADU_std_Gnknown_3DAr= APy3_GENfuns.numpy_NaNs_like(dataADU_avg_Gnknown_3DAr)
for iFile in range(NSets_Gnknown):
    dataADU_avg_Gnknown_3DAr[iFile,:,:]=  APy3_GENfuns.read_warn_1xh5(folder_Gnknown+fileList_avg_Gnknown[iFile], '/data/data')
    dataADU_std_Gnknown_3DAr[iFile,:,:]=  APy3_GENfuns.read_warn_1xh5(folder_Gnknown+fileList_std_Gnknown[iFile], '/data/data')
    APy3_GENfuns.dot_every10th(iFile,NSets_Gnknown)
dataADU_avg_Gnknown_3DAr= numpy.copy(dataADU_avg_Gnknown_3DAr- PedestalADU_multiGn_Gnknown[0,:,:]) # note it is always 0, as it is fixGn
#
APy3_GENfuns.printcol("reading unknown-Gn data files",'blue')
NSets_Gnunkwn= len(fileList_avg_Gnunkwn)
dataADU_avg_Gnunkwn_3DAr= APy3_GENfuns.numpy_NaNs((NSets_Gnunkwn,NRow,NCol))
dataADU_std_Gnunkwn_3DAr= APy3_GENfuns.numpy_NaNs_like(dataADU_avg_Gnunkwn_3DAr)
for iFile in range(NSets_Gnunkwn):
    dataADU_avg_Gnunkwn_3DAr[iFile,:,:]=  APy3_GENfuns.read_warn_1xh5(folder_Gnunkwn+fileList_avg_Gnunkwn[iFile], '/data/data')
    dataADU_std_Gnunkwn_3DAr[iFile,:,:]=  APy3_GENfuns.read_warn_1xh5(folder_Gnunkwn+fileList_std_Gnunkwn[iFile], '/data/data')
    APy3_GENfuns.dot_every10th(iFile,NSets_Gnunkwn)
dataADU_avg_Gnunkwn_3DAr= numpy.copy(dataADU_avg_Gnunkwn_3DAr- PedestalADU_multiGn_Gnunkwn[0,:,:]) # note it is always 0, as it is fixGn
#
#---
#%% interactive:
if interactiveShowFlag:
    APy3_GENfuns.printcol("interactive show",'blue')
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("interactivly showing ramps",'blue')
    APy3_GENfuns.printcol("plot-fit [R]amp / [Q]uit",'green')
    nextstep= input()
    while (nextstep not in ['q','Q']):
        #
        if (nextstep in ['r','R']):
            APy3_GENfuns.printcol("plot pixel: Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("plot pixel: Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            #
            e_per_ADU_Gnknown= e_per_ADU_multiGn_Gnknown[0,thisRow,thisCol]
            e_per_ADU_Gnunkwn= e_per_ADU_multiGn_Gnunkwn[0,thisRow,thisCol]
            #
            data2fit_Gnknown_tint= numpy.copy(intTimes_ms_Gnknown)
            data2fit_Gnknown_ADU= numpy.copy(dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol])
            data2fit_Gnunkwn_tint= numpy.copy(intTimes_ms_Gnunkwn)
            data2fit_Gnunkwn_ADU= numpy.copy(dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol])
            #
            APy3_GENfuns.printcol("{0}:".format(label_Gnknown),'green')
            APy3_GENfuns.printcol("   {0}e/ADU".format(e_per_ADU_Gnknown),'green')
            APy3_GENfuns.printcol("   first point of the ramp (t={0}ms): {1}+/-{2}ADU , {3}+/-{4}e".format(data2fit_Gnknown_tint[0], dataADU_avg_Gnknown_3DAr[0,thisRow,thisCol],dataADU_std_Gnknown_3DAr[0,thisRow,thisCol], dataADU_avg_Gnknown_3DAr[0,thisRow,thisCol]*e_per_ADU_Gnknown,dataADU_std_Gnknown_3DAr[0,thisRow,thisCol]*e_per_ADU_Gnknown),'green')
            APy3_GENfuns.printcol("{0}:".format(label_Gnunkwn),'green')
            APy3_GENfuns.printcol("  {0}e/ADU".format(e_per_ADU_Gnunkwn),'green')
            APy3_GENfuns.printcol("   first point of the ramp (t={0}ms): {1}+/-{2}ADU , {3}+/-{4}e".format(data2fit_Gnunkwn_tint[0], dataADU_avg_Gnunkwn_3DAr[0,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[0,thisRow,thisCol], dataADU_avg_Gnunkwn_3DAr[0,thisRow,thisCol]*e_per_ADU_Gnunkwn,dataADU_std_Gnunkwn_3DAr[0,thisRow,thisCol]*e_per_ADU_Gnunkwn),'green')
            #
            if pngFlag:
                APy3_GENfuns.printcol("png-saving pixel ({0},{1})".format(thisRow,thisCol),'green')
                #APy3_GENfuns.png_1D_errbar(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]', '{0}, pix({1},{2})'.format(label_Gnknown,thisRow,thisCol), False, pngFolder+'ramp_ADU_{0}_pix({1},{2})_1D.png'.format(label_Gnknown,thisRow,thisCol) )
                #APy3_GENfuns.png_1D_errbar(intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]', '{0}, pix({1},{2})'.format(label_Gnunkwn,thisRow,thisCol), False, pngFolder+'ramp_ADU_{0}_pix({1},{2})_1D.png'.format(label_Gnunkwn,thisRow,thisCol) )
                #
                #APy3_GENfuns.png_1D_errbar(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,dataADU_std_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown, 'integration time [ms]','pixel output [e]', '{0}, pix({1},{2})'.format(label_Gnknown,thisRow,thisCol), False, pngFolder+'ramp_e_{0}_pix({1},{2})_1D.png'.format(label_Gnknown,thisRow,thisCol) )
                #APy3_GENfuns.png_1D_errbar(intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn, 'integration time [ms]','pixel output [e]', '{0}, pix({1},{2})'.format(label_Gnunkwn,thisRow,thisCol), False, pngFolder+'ramp_e_{0}_pix({1},{2})_1D.png'.format(label_Gnunkwn,thisRow,thisCol) )
                if label_Gnknown in ['high gain','very-high gain']: 
                    APy3_GENfuns.png_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,
                                                           dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           dataADU_std_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [e]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_e_pix({0},{1})_1Dx2.png'.format(thisRow,thisCol))
                    APy3_GENfuns.png_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_1Dx2.png'.format(thisRow,thisCol))

                    APy3_GENfuns.png_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_{2}_1D.png'.format(thisRow,thisCol,label_Gnunkwn))
                    APy3_GENfuns.png_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown,
                                                           [],[],[],[],
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_{2}_1D.png'.format(thisRow,thisCol,label_Gnknown))

                elif label_Gnknown in ['medium gain','med gain']:   
                    APy3_GENfuns.png_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,
                                                           dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           dataADU_std_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           label_Gnunkwn,
                                                           'integration time [ms]','pixel output [e]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_e_pix({0},{1})_1Dx2.png'.format(thisRow,thisCol))
                    APy3_GENfuns.png_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],label_Gnunkwn,
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_1Dx2.png'.format(thisRow,thisCol))




                    APy3_GENfuns.png_errbar_1Dx3_samecanva([],[],[],[],
                                                           [],[],[],[],
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           label_Gnunkwn,
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_{2}_1D.png'.format(thisRow,thisCol,label_Gnunkwn))
                    APy3_GENfuns.png_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False,
                                                           pngFolder+'ramp_ADU_pix({0},{1})_{2}_1D.png'.format(thisRow,thisCol,label_Gnknown))

            #    
            else:
                APy3_GENfuns.printcol("showing pixel ({0},{1})".format(thisRow,thisCol),'green')
                if label_Gnknown in ['high gain','very-high gain']: 
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,
                                                           dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           dataADU_std_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [e]','pix({0},{1})'.format(thisRow,thisCol), False)

                    APy3_GENfuns.plot_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)

                    APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           label_Gnunkwn,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva(intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown,
                                                           [],[],[],[],
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)

                elif label_Gnknown in ['medium gain','med gain']:   
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,
                                                           dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           dataADU_std_Gnknown_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnknown,
                                                           label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol]*e_per_ADU_Gnunkwn,
                                                           label_Gnunkwn,
                                                           'integration time [ms]','pixel output [e]','pix({0},{1})'.format(thisRow,thisCol), False)
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown, 
                                                           intTimes_ms_Gnunkwn,dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],label_Gnunkwn,
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],[],
                                                           [],[],[],[],
                                                           intTimes_ms_Gnunkwn,
                                                           dataADU_avg_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           dataADU_std_Gnunkwn_3DAr[:,thisRow,thisCol],
                                                           label_Gnunkwn,
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)
                    APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],[],
                                                           intTimes_ms_Gnknown,dataADU_avg_Gnknown_3DAr[:,thisRow,thisCol],dataADU_std_Gnknown_3DAr[:,thisRow,thisCol],label_Gnknown,
                                                           [],[],[],[],
                                                           'integration time [ms]','pixel output [ADU]','pix({0},{1})'.format(thisRow,thisCol), False)
                APy3_GENfuns.showIt()
        #
        APy3_GENfuns.printcol("plot-fit [R]amp / [Q]uit",'green')
        nextstep= input()

#---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




