# -*- coding: utf-8 -*-
"""
# DLSraw file: ADUcorr, CDS/CMA Gn0 if needed, LatOvflw to electron, show

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
cd /home/marras/PercAuxiliaryTools/LookAtFLast

python3 ./xxx.py
or:
start python
# execfile("xxx.py") # this is in python 2.7
exec(open("./xxx.py").read()); print('Python3 is horrible')
"""

#%% imports and useful constants
from APy3_auxINIT import *

NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
NSmplRst= APy3_P2Mfuns.NSmplRst
NGnCrsFn= APy3_P2Mfuns.NGnCrsFn
ERRDLSraw= APy3_P2Mfuns.ERRDLSraw
ERRint16= APy3_P2Mfuns.ERRint16


numpy.seterr(divide='ignore', invalid='ignore')

#
interactiveGUIFlag= True; #interactiveGUIFlag= False; 
#
#---
#
#%% parameters
#
dflt_labFig= "BSI04"
#
'''
##### 7of7ADC biasBSI04.04 PGABBB 3G, 3rd #####
dflt_Folder='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_04_PGABBB/avg_xGn/'
#
#data_prefix= '2020.06.03.08.54.26_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_ODx.x_t012ms_100drk'
#data_prefix= '2020.06.03.09.16.20_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD6.0_t012ms_100lgh'
data_prefix= '2020.06.03.09.17.39_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD5.0_t012ms_100lgh'
#data_prefix= '2020.06.03.09.19.07_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD4.0_t012ms_100lgh' # Gn0
#data_prefix= '2020.06.03.09.20.59_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD3.0_t012ms_100lgh' #example Gn 0->1#
#data_prefix= '2020.06.03.09.21.58_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD2.0_t012ms_100lgh'
#data_prefix= '2020.06.03.09.23.33_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD1.0_t012ms_100lgh'
#data_prefix= '2020.06.03.09.24.17_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD0.0_t012ms_100lgh'
#
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file=dflt_Folder+data_prefix+'_Gn1_ADU_Smpl_avg.h5' 
dflt_avgGn2_data_file=dflt_Folder+data_prefix+'_Gn2_ADU_Smpl_avg.h5'
#
drk_prefix='2020.06.03.08.53.40_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_ODx.x_t012ms_100drk'
dflt_avgGn0_drk_file=dflt_Folder+drk_prefix+'_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_drk_file=dflt_Folder+drk_prefix+'_Gn1_ADU_Smpl_avg.h5'
dflt_avgGn2_drk_file=dflt_Folder+drk_prefix+'_Gn2_ADU_Smpl_avg.h5'
#dflt_avgGn0_drk_file='NONE'; dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5' # BAD calibration, do not use
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
#
#dflt_alternFile_Ped_Gn0_ADU= dflt_Folder+"2020.06.03.08.43.50_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_fixGn0_ODx.x_t012ms_100drk_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn1_ADU= dflt_Folder+"2020.06.03.08.49.43_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_fixGn1_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
#dflt_alternFile_Ped_Gn2_ADU= dflt_Folder+"2020.06.03.08.50.10_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_fixGn2_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
'''
##### 7of7ADC biasBSI04.05 PGA6BB 3G, 3rd #####
dflt_Folder='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_05_PGA6BB/avg_xGn/'
#
#data_prefix= '2020.06.03.09.38.46_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_ODx.x_t012ms_100drk'
data_prefix= '2020.06.03.10.07.13_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD6.0_t012ms_100lgh'
#data_prefix= '2020.06.03.10.08.02_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD5.0_t012ms_100lgh'
#data_prefix= '2020.06.03.10.08.57_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD4.0_t012ms_100lgh'
#data_prefix= '2020.06.03.10.10.17_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD3.0_t012ms_100lgh' #Gn1

#data_prefix= '2020.06.03.10.11.56_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD2.0_t012ms_100lgh'
#data_prefix= '2020.06.03.10.13.53_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD1.0_t012ms_100lgh'
#data_prefix= '2020.06.03.10.15.10_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_OD0.0_t012ms_100lgh'
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file=dflt_Folder+data_prefix+'_Gn1_ADU_Smpl_avg.h5' 
dflt_avgGn2_data_file=dflt_Folder+data_prefix+'_Gn2_ADU_Smpl_avg.h5'
#
drk_prefix='2020.06.03.09.37.29_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_3G_ODx.x_t012ms_100drk'
dflt_avgGn0_drk_file=dflt_Folder+drk_prefix+'_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_drk_file=dflt_Folder+drk_prefix+'_Gn1_ADU_Smpl_avg.h5'
dflt_avgGn2_drk_file=dflt_Folder+drk_prefix+'_Gn2_ADU_Smpl_avg.h5'
#dflt_avgGn0_drk_file='NONE'; dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal_gapsAvg.h5' # no sense in using extracted_only, as 7/7
#
dflt_alternFile_Ped_Gn0_ADU= dflt_Folder+"2020.06.03.09.31.27_BSI04_example_Tm20_7of7ADC_biasBSI04_05_PGA6BB_fixGn0_ODx.x_t012ms_100drk_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
'''
##### 3of7ADC biasBSI04.04 PGABBB 3G, 3rd #####
dflt_Folder='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_04_PGABBB/avg_xGn/'
#
#data_prefix= '2020.06.03.16.13.19_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_ODx.x_t012ms_100drk'
#data_prefix= '2020.06.03.16.26.16_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD6.0_t012ms_100lgh'
#data_prefix= '2020.06.03.16.28.06_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD4.0_t012ms_100lgh' #Gn0
data_prefix= '2020.06.03.16.28.59_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD3.0_t012ms_100lgh' #example Gn 0->1#
#data_prefix= '2020.06.03.16.29.55_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD2.0_t012ms_100lgh'
#data_prefix= '2020.06.03.16.30.40_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD1.0_t012ms_100lgh'
#data_prefix= '2020.06.03.16.31.17_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_OD0.0_t012ms_100lgh'
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file=dflt_Folder+data_prefix+'_Gn1_ADU_Smpl_avg.h5' 
dflt_avgGn2_data_file=dflt_Folder+data_prefix+'_Gn2_ADU_Smpl_avg.h5'
#
drk_prefix='2020.06.03.16.13.06_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_3G_ODx.x_t012ms_100drk'
dflt_avgGn0_drk_file=dflt_Folder+drk_prefix+'_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_drk_file=dflt_Folder+drk_prefix+'_Gn1_ADU_Smpl_avg.h5'
dflt_avgGn2_drk_file=dflt_Folder+drk_prefix+'_Gn2_ADU_Smpl_avg.h5'
#dflt_avgGn0_drk_file='NONE'; dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5' # BAD calibration, do not use
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
#
dflt_alternFile_Ped_Gn0_ADU= dflt_Folder+"2020.06.03.16.07.05_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_fixGn0_ODx.x_t012ms_100drk_Gn0_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn1_ADU= dflt_Folder+"2020.06.03.16.08.08_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_fixGn1_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
#dflt_alternFile_Ped_Gn2_ADU= dflt_Folder+"2020.06.03.16.08.29_BSI04_example_Tm20_3of7ADC_biasBSI04_04_PGABBB_fixGn2_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
#dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
'''
#
'''
##### 3of7ADC biasBSI04.05 PGA6BB 3G, 3rd #####
dflt_Folder='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_05_PGA6BB/avg_xGn/'
#
data_prefix= '2020.06.03.15.30.42_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_ODx.x_t012ms_100drk'
data_prefix= '2020.06.03.15.48.40_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD6.0_t012ms_100lgh'
data_prefix= '2020.06.03.15.49.48_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD5.0_t012ms_100lgh'
data_prefix= '2020.06.03.15.50.31_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD4.0_t012ms_100lgh' # Gn 0=>1
data_prefix= '2020.06.03.15.51.30_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD3.0_t012ms_100lgh' # Gn1
#data_prefix= '2020.06.03.15.52.22_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD2.0_t012ms_100lgh'
#data_prefix= '2020.06.03.15.53.12_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD1.0_t012ms_100lgh'
#data_prefix= '2020.06.03.15.54.12_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_OD0.0_t012ms_100lgh'
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file=dflt_Folder+data_prefix+'_Gn1_ADU_Smpl_avg.h5' 
dflt_avgGn2_data_file=dflt_Folder+data_prefix+'_Gn2_ADU_Smpl_avg.h5'
#
drk_prefix='2020.06.03.15.29.31_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_ODx.x_t012ms_100drk'
drk_prefix='2020.06.03.15.30.33_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_3G_ODx.x_t012ms_100drk'
dflt_avgGn0_drk_file=dflt_Folder+drk_prefix+'_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_drk_file=dflt_Folder+drk_prefix+'_Gn1_ADU_Smpl_avg.h5'
dflt_avgGn2_drk_file=dflt_Folder+drk_prefix+'_Gn2_ADU_Smpl_avg.h5'
#dflt_avgGn0_drk_file='NONE'; dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5' 
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal_gapsAvg.h5'

#
dflt_alternFile_Ped_Gn0_ADU= dflt_Folder+"2020.06.03.15.10.57_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_fixGn0_ODx.x_t012ms_100drk_Gn0_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn1_ADU= dflt_Folder+"2020.06.03.15.14.42_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_fixGn1_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
#dflt_alternFile_Ped_Gn2_ADU= dflt_Folder+"2020.06.03.15.15.57_BSI04_example_Tm20_3of7ADC_biasBSI04_05_PGA6BB_fixGn2_ODx.x_t012ms_100drk_ADU_Smpl_avg.h5"
#dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
'''
#
#---
#
'''
##### 7of7ADC biasBSI04.04 fixGn0,PGAB #####
dflt_Folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_04_PGABBB/avg_xGn/"
#
dflt_avgGn0_data_file=dflt_Folder+'2020.06.03.08.48.08_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_fixGn0_ODx.x_t012ms_100drk_ADU_CDS_avg.h5'
dflt_avgGn1_data_file='NONE'
dflt_avgGn2_data_file='NONE'
dflt_labFig= "BSI04 7of7 fixGn(high) drk"
#
dflt_avgGn0_data_file=dflt_Folder+'2020.06.03.09.17.39_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD5.0_t012ms_100lgh_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_data_file='NONE'
dflt_avgGn2_data_file='NONE'
dflt_labFig= "BSI04 7of7 fixGn(high) OD5.0, t012ms"
#
dflt_avgGn0_data_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/avg_std/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_OD4.0_t012ms_500lgh_CDS_avg.h5'
dflt_avgGn1_data_file='NONE'
dflt_avgGn2_data_file='NONE'
dflt_labFig= "BSI04 7of7 fixGn(high) OD4.0, t012ms"
#
dflt_avgGn0_data_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_7of7ADC_3rd/BSI04_04_PGABBB/avg_xGn/2020.06.03.09.19.07_BSI04_example_Tm20_7of7ADC_biasBSI04_04_PGABBB_3G_OD4.0_t012ms_100lgh_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_data_file='NONE'
dflt_avgGn2_data_file='NONE'
dflt_labFig= "BSI04 7of7 fixGn(high) OD3.0, t012ms"
#
dflt_avgGn0_drk_file='NONE';
dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/CalibrParam_fixGn/BSI04_Tm20_7of7ADC_biasBSI04.04_fixGn0_PGAB_2020.03.12b_fixGnCal_from3of7_ADU2eAvg.h5"
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGAB_2020.03.12_fixGnCal_from3of7gapsAvg.h5"


#
dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"

#'''



#
'''
##### 7of7ADC biasBSI04.05 fixGn0,PGA6 #####
dflt_Folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD4.0_t012ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(very-high) OD4.0 t12ms"
data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD4.0_t020ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(very-high) OD4.0 t20ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_OD5.0_t012ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(very-high) OD5.0 t12ms"
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5'
#dflt_avgGn0_data_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/avg_xGn/'+'2020.06.06.12.30.39_BSI04_Tm20_7of7_biasBSI04_05_fixGn0_PGA6_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_data_file='NONE'
dflt_avgGn2_data_file='NONE'
#
dflt_avgGn0_drk_file='NONE';
dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/CalibrParam_fixGn/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGA6_2020.06.06_fixGnCal_from3of7gapsAvg.h5"
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/CalibrParam_fixGn/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGA6_2020.06.06_fixGnCal_from3of7_ADU2eAvg.h5"
#
dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
'''
##### 7of7ADC biasBSI04.05 fixGn1,PGAB #####
dflt_labFig= "BSI04 7of7 fixGn(medium) OD4.0"
dflt_Folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD2.0_t012ms_30lgh"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD3.0_t012ms_30lgh"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_t012ms_30lgh"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_t030ms_30lgh"

data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_t020ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(medium) OD4.0 t20ms"
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
#dflt_avgGn0_data_file='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/avg_xGn/'+'2020.06.06.12.33.15_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5'
dflt_avgGn1_data_file='NONE' 
dflt_avgGn2_data_file='NONE'
#
dflt_avgGn0_drk_file='NONE'; 
dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/CalibrParam_fixGn/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn1_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_alternFile_Ped_Gn0_ADU= "NONE"
#dflt_alternFile_Ped_Gn0_ADU= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/avg_xGn/"+"2020.06.06.12.33.15_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn0_ADU= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/avg_xGn/"+"2020.06.06.22.12.17_BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_ODx.x_1kdrk_Gn0_ADU_CDS_avg.h5"
#dflt_alternFile_Ped_Gn0_ADU="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/"+"BSI04_Tm20_7of7_biasBSI04_05_fixGn1_PGAB_OD4.0_t028ms_30lgh"+'_Gn0_ADU_CDS_avg.h5'
#
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
'''
##### 7of7ADC biasBSI04.05 fixGn2,PGAB #####

dflt_Folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/avg_xGn/"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD3.0_t012ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(low) OD3.0 t012ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_t012ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(low) OD2.0 t012ms"
data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_t100ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(low) OD2.0 t100ms"
data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_t200ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(low) OD2.0 t200ms"
data_prefix="BSI04_Tm20_7of7_biasBSI04_05_fixGn2_PGAB_OD2.0_t300ms_30lgh"; dflt_labFig= "BSI04 7of7 fixGn(low) OD2.0 t300ms"
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file='NONE' 
dflt_avgGn2_data_file='NONE'
#
dflt_avgGn0_drk_file='NONE'; 
dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/ramps/CalibrParam_fixGn/"+"BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn2_PGAB_2020.06.06_fixGnCal_ADU2eAvg.h5"
#
dflt_alternFile_Ped_Gn0_ADU= "NONE"
dflt_alternFile_Ped_Gn1_ADU="NONE"
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
#'''
##### 7of7ADC biasBSI04.05 3G,PGA6BB, #####

dflt_Folder='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
#
data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD5.0_t012ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD5.0,t12ms"
###data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD4.0_t012ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD4.0,t12ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD4.0_t020ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD4.0,t20ms"
###data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD4.0_t030ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD4.0,t30ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD3.0_t012ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD3.0,t12ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD2.0_t012ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD2.0,t12ms"
###data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD2.0_t020ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD2.0,t20ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD2.0_t100ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD2.0,t100ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD2.0_t200ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD2.0,t200ms"
#data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_OD2.0_t300ms_30lgh"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,OD2.0,t300ms"
#
###data_prefix="BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk"; dflt_labFig= "BSI04,7of7ADC,3G,PGA6BB,drk,t12ms"
#
dflt_avgGn0_data_file=dflt_Folder+data_prefix+'_Gn0_ADU_CDS_avg.h5' 
dflt_avgGn1_data_file=dflt_Folder+data_prefix+'_Gn1_ADU_Smpl_avg.h5' 
dflt_avgGn2_data_file=dflt_Folder+data_prefix+'_Gn2_ADU_Smpl_avg.h5'
#
#
#
dflt_avgGn0_drk_file='NONE'; dflt_avgGn1_drk_file='NONE'; dflt_avgGn2_drk_file='NONE'
#drk_prefix='BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk'
#dflt_avgGn0_drk_file=dflt_Folder+drk_prefix+'_Gn0_ADU_CDS_avg.h5' 
#dflt_avgGn1_drk_file=dflt_Folder+drk_prefix+'_Gn1_ADU_Smpl_avg.h5' 
#dflt_avgGn2_drk_file=dflt_Folder+drk_prefix+'_Gn2_ADU_Smpl_avg.h5' 
#
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn01x_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD5.0_prelim.h5"
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_test.h5_Gnyy2.h5"
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_test.h5_backup2020.06.18.h5"
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_test.h5"
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD0.5_OD3.0_R2_0.85.h5"
#
dflt_alternFile_Ped_Gn0_ADU= "NONE"
#
dflt_alternFile_Ped_Gn1_ADU="NONE"
#dflt_alternFile_Ped_Gn1_ADU="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_2020.06.10_Gn1.ADU0_usingOD5.0.h5"
#dflt_alternFile_Ped_Gn1_ADU="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_2020.06.10_Gn1.ADU0_usingOD4.0.h5"
#dflt_alternFile_Ped_Gn1_ADU="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_2020.06.10_Gn1.ADU0_usingOD3.0.h5"
#dflt_alternFile_Ped_Gn1_ADU="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_2020.06.10_Gn1.ADU0_usingOD5.0_R2_0.90.h5"
#
dflt_alternFile_Ped_Gn2_ADU="NONE"
#
#
dflt_cols2CMA_str= 'NONE'
#
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#
#dflt_pngFolder= "/home/marras/auximg/"
dflt_pngFolder= "NONE"
#'''
#
#
#---
#
#%% functs
#
#
#---
#
#%% parameter loading
if interactiveGUIFlag:
    # interactive GUI
    GUIwin_arguments= []
    GUIwin_arguments+= ['avg-Gn0 data file to process [NONE not to]'];      GUIwin_arguments+= [dflt_avgGn0_data_file] 
    GUIwin_arguments+= ['avg-Gn1 data file to process [NONE not to]'];      GUIwin_arguments+= [dflt_avgGn1_data_file] 
    GUIwin_arguments+= ['avg-Gn2 data file to process [NONE not to]'];      GUIwin_arguments+= [dflt_avgGn2_data_file] 

    GUIwin_arguments+= ['avg-Gn0 dark file to process'];                    GUIwin_arguments+= [dflt_avgGn0_drk_file] 
    GUIwin_arguments+= ['avg-Gn1 dark file to process'];                    GUIwin_arguments+= [dflt_avgGn1_drk_file] 
    GUIwin_arguments+= ['avg-Gn2 dark file to process'];                    GUIwin_arguments+= [dflt_avgGn2_drk_file] 

    GUIwin_arguments+= ['Lateral Overflow (pedestal & e/ADU for Gn0/1/2): file']; GUIwin_arguments+= [dflt_multiGnCal_file]

    GUIwin_arguments+= ['alternate ADU0 offset [Gn0] file [none not to use it]'];           GUIwin_arguments+= [dflt_alternFile_Ped_Gn0_ADU]
    GUIwin_arguments+= ['alternate ADU0 offset [Gn1] file [none not to use it]'];           GUIwin_arguments+= [dflt_alternFile_Ped_Gn1_ADU]
    GUIwin_arguments+= ['alternate ADU0 offset [Gn2] file [none not to use it]'];           GUIwin_arguments+= [dflt_alternFile_Ped_Gn2_ADU]

    #
    GUIwin_arguments+= ['cols to use for CMA [from:to] [none not to use it]']; GUIwin_arguments+= [dflt_cols2CMA_str]

    GUIwin_arguments+= ['instead of showing images, save to path [NONE not to]']; GUIwin_arguments+= [dflt_pngFolder]

    GUIwin_arguments+= ['figure label']; GUIwin_arguments+= [dflt_labFig]


    GUIwin_arguments+= ['high memory usage? [Y/N]'];       GUIwin_arguments+= [str(dflt_highMemFlag)] 
    GUIwin_arguments+= ['clean mem when possible [Y/N]'];  GUIwin_arguments+= [str(dflt_cleanMemFlag)]
    GUIwin_arguments+= ['verbose? [Y/N]'];                 GUIwin_arguments+= [str(dflt_verboseFlag)]
    #---
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    avgGn0_data_file=       dataFromUser[i_param]; i_param+=1
    avgGn1_data_file=       dataFromUser[i_param]; i_param+=1
    avgGn2_data_file=       dataFromUser[i_param]; i_param+=1
    #
    avgGn0_drk_file=       dataFromUser[i_param]; i_param+=1
    avgGn1_drk_file=       dataFromUser[i_param]; i_param+=1
    avgGn2_drk_file=       dataFromUser[i_param]; i_param+=1
    #
    multiGnCal_file=        dataFromUser[i_param]; i_param+=1
    #
    alternFile_Ped_Gn0_ADU= dataFromUser[i_param]; i_param+=1
    alternFile_Ped_Gn1_ADU= dataFromUser[i_param]; i_param+=1
    alternFile_Ped_Gn2_ADU= dataFromUser[i_param]; i_param+=1
    #
    cols2CMA_str= dataFromUser[i_param]; i_param+=1
    #
    pngFolder= dataFromUser[i_param]; i_param+=1
    labFig= dataFromUser[i_param]; i_param+=1
    #
    highMemFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cleanMemFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #
else:
    # not interactiveGUIFlag
    avgGn0_data_file= dflt_avgGn0_data_file
    avgGn1_data_file= dflt_avgGn1_data_file
    avgGn2_data_file= dflt_avgGn2_data_file
    #
    avgGn0_drk_file= dflt_avgGn0_drk_file
    avgGn1_drk_file= dflt_avgGn1_drk_file
    avgGn2_drk_file= dflt_avgGn2_drk_file
    #
    multiGnCal_file= dflt_multiGnCal_file
    #
    alternFile_Ped_Gn0_ADU= dflt_alternFile_Ped_Gn0_ADU
    alternFile_Ped_Gn1_ADU= dflt_alternFile_Ped_Gn1_ADU
    alternFile_Ped_Gn2_ADU= dflt_alternFile_Ped_Gn2_ADU
    #
    cols2CMA_str= dflt_cols2CMA_str
    #
    pngFolder= dflt_pngFolder
    labFig= dflt_labFig
    #
    highMemFlag= APy3_GENfuns.isitYes(str(dflt_highMemFlag))
    cleanMemFlag= APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag= APy3_GENfuns.isitYes(str(dflt_verboseFlag))
#---
#
#%% understand parameters
if ( (avgGn0_drk_file in APy3_GENfuns.NOlist)&(avgGn1_drk_file in APy3_GENfuns.NOlist)&(avgGn2_drk_file in APy3_GENfuns.NOlist) ): drkPedFlag= False
else: drkPedFlag= True 

if cols2CMA_str in APy3_GENfuns.NOlist:
    CMAFlag=False
    cols2CMA=[]
else:
    CMAFlag= True
    cols2CMA= APy3_GENfuns.matlabLike_range(cols2CMA_str)
#
if multiGnCal_file in APy3_GENfuns.NOlist: ADU2eFlag= False
else: ADU2eFlag= True
#
if alternFile_Ped_Gn0_ADU in APy3_GENfuns.NOlist: alternPedGn0Flag= False
else: alternPedGn0Flag= True
if alternFile_Ped_Gn1_ADU in APy3_GENfuns.NOlist: alternPedGn1Flag= False
else: alternPedGn1Flag= True
if alternFile_Ped_Gn2_ADU in APy3_GENfuns.NOlist: alternPedGn2Flag= False
else: alternPedGn2Flag= True
#
if pngFolder in APy3_GENfuns.NOlist: pngFlag= False
else: pngFlag= True
#---
#
#%% profile it
#import cProfile
#cProfile.run('auxdata= descrambleLast(mainFolder, ...)', sort='cumtime')
#APy3_GENfuns.printcol("scripts took {0} sec".format(aux_length),'green')
#---
#%% or just execute it
#
# ---
# what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will process data images from:','blue')
    APy3_GENfuns.printcol('  Gn0: {0}'.format(avgGn0_data_file),'blue')
    APy3_GENfuns.printcol('  Gn1: {0}'.format(avgGn1_data_file),'blue')
    APy3_GENfuns.printcol('  Gn2: {0}'.format(avgGn2_data_file),'blue')

    if drkPedFlag: 
        APy3_GENfuns.printcol('will calculate a dark pedestal using:','blue')
        APy3_GENfuns.printcol('  Gn0: {0}'.format(avgGn0_drk_file),'blue')
        APy3_GENfuns.printcol('  Gn1: {0}'.format(avgGn1_drk_file),'blue')
        APy3_GENfuns.printcol('  Gn2: {0}'.format(avgGn2_drk_file),'blue')
    #
    APy3_GENfuns.printcol('multiGnCal file: {0}'.format(multiGnCal_file),'blue')
    #
    if alternPedGn0Flag: APy3_GENfuns.printcol('Gn0 alternate ADU0 offset: {0}'.format(alternFile_Ped_Gn0_ADU),'blue')
    if alternPedGn1Flag: APy3_GENfuns.printcol('Gn1 alternate ADU0 offset: {0}'.format(alternFile_Ped_Gn1_ADU),'blue')
    if alternPedGn2Flag: APy3_GENfuns.printcol('Gn2 alternate ADU0 offset: {0}'.format(alternFile_Ped_Gn2_ADU),'blue')
    #
    if CMAFlag: APy3_GENfuns.printcol('will apply CMA using cols {0} as reference'.format(cols2CMA_str),'blue')
    #
    if pngFlag: APy3_GENfuns.printcol('instead of showing images, will save as png in {0}'.format(pngFolder),'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    #
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#%% start
startTime = time.time()
if (verboseFlag): APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#% load calibr files
APy3_GENfuns.printcol("loading calibr files",'blue')
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
if verboseFlag: APy3_GENfuns.printcol("multiGnCal file loaded {0}".format(multiGnCal_file),'green')
#
if alternPedGn0Flag:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn0_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn0_ADU)
    PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn0_ADU, '/data/data')
    if verboseFlag: APy3_GENfuns.printcol("alternative Gn0 Pedestal ADU file loaded {0}".format(alternFile_Ped_Gn0_ADU),'green')
if alternPedGn1Flag:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn1_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn1_ADU)
    PedestalADU_multiGn[1,:,:]= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn1_ADU, '/data/data')
    if verboseFlag: APy3_GENfuns.printcol("alternative Gn1 Pedestal ADU file loaded {0}".format(alternFile_Ped_Gn1_ADU),'green')
if alternPedGn2Flag:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn2_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn2_ADU)
    PedestalADU_multiGn[2,:,:]= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn2_ADU, '/data/data')
    if verboseFlag: APy3_GENfuns.printcol("alternative Gn2 Pedestal ADU file loaded {0}".format(alternFile_Ped_Gn2_ADU),'green')
#---
#%% load data files
APy3_GENfuns.printcol("loading data file",'blue')
data_ADU_avgxGn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))

if ((avgGn0_data_file in APy3_GENfuns.NOlist)&(avgGn1_data_file in APy3_GENfuns.NOlist)&(avgGn2_data_file in APy3_GENfuns.NOlist)): APy3_GENfuns.printERR('at least one file should be given')

if (avgGn0_data_file in APy3_GENfuns.NOlist): data_ADU_avgxGn[0,:,:]= numpy.zeros((NRow,NCol))
else: 
    if APy3_GENfuns.notFound(avgGn0_data_file): APy3_GENfuns.printERR('not found '+avgGn0_data_file)
    data_ADU_avgxGn[0,:,:]= APy3_GENfuns.read_1xh5(avgGn0_data_file, '/data/data')

if (avgGn1_data_file in APy3_GENfuns.NOlist): data_ADU_avgxGn[1,:,:]= numpy.zeros((NRow,NCol))
else:
    if APy3_GENfuns.notFound(avgGn1_data_file): APy3_GENfuns.printERR('not found '+avgGn1_data_file)
    data_ADU_avgxGn[1,:,:]= APy3_GENfuns.read_1xh5(avgGn1_data_file, '/data/data')

if (avgGn2_data_file in APy3_GENfuns.NOlist): data_ADU_avgxGn[2,:,:]= numpy.zeros((NRow,NCol))
else:
    if APy3_GENfuns.notFound(avgGn2_data_file): APy3_GENfuns.printERR('not found '+avgGn2_data_file)
    data_ADU_avgxGn[2,:,:]= APy3_GENfuns.read_1xh5(avgGn2_data_file, '/data/data')
#---
#%% data: Gn,Crs,Fn => e
APy3_GENfuns.printcol('data: ADU => e','blue')
data_e= APy3_GENfuns.numpy_NaNs((NRow,NCol))
data_Gn= numpy.zeros((NRow,NCol)).astype(int)-256
data_e_avgxGn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))
for thisGn in range(3):
    if ((thisGn==0)&(CMAFlag==True)):
        if verboseFlag: APy3_GENfuns.printcol('  CMA-ing Gn0','blue')
        aux_data_CMAed= APy3_P2Mfuns.CMA(data_ADU_avgxGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
        aux_ped_CMAed= APy3_P2Mfuns.CMA(PedestalADU_multiGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
        data_e_avgxGn[thisGn,:,:]= (aux_data_CMAed-aux_ped_CMAed)*e_per_ADU_multiGn[thisGn,:,:]
        del aux_drk_CMAed; del aux_ped_CMAed
    else: 
        data_e_avgxGn[thisGn,:,:]= (data_ADU_avgxGn[thisGn,:,:]-PedestalADU_multiGn[thisGn,:,:])*e_per_ADU_multiGn[thisGn,:,:]
    auxmap= ~numpy.isnan(data_e_avgxGn[thisGn,:,:])
    data_Gn[auxmap]=thisGn
    data_e[auxmap]= data_e_avgxGn[thisGn,:,:][auxmap]
    del auxmap
del data_e_avgxGn
#---
#%% load data files
drk_ADU_avgxGn= numpy.zeros((3,NRow,NCol))
drkPed_e= numpy.zeros((NRow,NCol))
if drkPedFlag:
    APy3_GENfuns.printcol("loading drk file",'blue')
    if (avgGn0_drk_file not in APy3_GENfuns.NOlist):
        if APy3_GENfuns.notFound(avgGn0_drk_file): APy3_GENfuns.printERR('not found '+avgGn0_drk_file)
        drk_ADU_avgxGn[0,:,:]= APy3_GENfuns.read_1xh5(avgGn0_drk_file, '/data/data')
    if (avgGn1_drk_file not in APy3_GENfuns.NOlist):
        if APy3_GENfuns.notFound(avgGn1_drk_file): APy3_GENfuns.printERR('not found '+avgGn1_drk_file)
        drk_ADU_avgxGn[1,:,:]= APy3_GENfuns.read_1xh5(avgGn1_drk_file, '/data/data')
    if (avgGn2_drk_file not in APy3_GENfuns.NOlist):
        if APy3_GENfuns.notFound(avgGn2_drk_file): APy3_GENfuns.printERR('not found '+avgGn2_drk_file)
        drk_ADU_avgxGn[2,:,:]= APy3_GENfuns.read_1xh5(avgGn2_drk_file, '/data/data')
    #
    APy3_GENfuns.printcol('dark: ADU => e','blue')
    drk_e= APy3_GENfuns.numpy_NaNs((NRow,NCol))
    drk_e_avgxGn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))
    for thisGn in range(3):
        if ((thisGn==0)&(CMAFlag==True)):
            if verboseFlag: APy3_GENfuns.printcol('  CMA-ing Gn0','blue')
            aux_drk_CMAed= APy3_P2Mfuns.CMA(drk_ADU_avgxGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
            aux_ped_CMAed= APy3_P2Mfuns.CMA(PedestalADU_multiGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
            drk_e_avgxGn[thisGn,:,:]= (aux_data_CMAed-aux_ped_CMAed)*e_per_ADU_multiGn[thisGn,:,:]
            del aux_drk_CMAed; del aux_ped_CMAed
        else: 
            drk_e_avgxGn[thisGn,:,:]= (drk_ADU_avgxGn[thisGn,:,:]-PedestalADU_multiGn[thisGn,:,:])*e_per_ADU_multiGn[thisGn,:,:]
        auxmap= ~numpy.isnan(drk_e_avgxGn[thisGn,:,:])
        drkPed_e[auxmap]= drk_e_avgxGn[thisGn,:,:][auxmap]
        del auxmap
    del drk_e_avgxGn
#---
# reshape to (1,NRow,NCol to reuse code)
data_e= data_e.reshape((1,NRow,NCol))
data_Gn= data_Gn.reshape((1,NRow,NCol))
#
data_e_Orig= numpy.copy(data_e)
data_Gn_Orig= numpy.copy(data_Gn)
badPix_map= numpy.zeros_like(data_Gn[0,:,:]).astype(bool)
#---
#%% interactive showing images
APy3_GENfuns.printcol("interactively looking at data",'blue')
thisImg=0
#
APy3_GENfuns.printcol("there are {0} valid images in the array (the first has already been excluded if needed)".format(data_e.shape[0]),'green')
APy3_GENfuns.printcol("show [image number]/[N]ext/[P]recedent/in [L]og scale / find [M]in-max / mark [B]ad pixels / reload [O]riginal values/ [Q]uit",'green')
nextstep= input()
while (nextstep not in ['q','Q']):
    #
    if (nextstep.isdigit()):
        thisImg= int(nextstep)
        if thisImg >= data_e.shape[0]: 
            thisImg= thisImg%data_e.shape[0]
            APy3_GENfuns.printcol("there are {0} valid images in the array; will show Image {1}".format(data_e.shape[0],thisImg),'green')
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else:
            APy3_GENfuns.png_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True, pngFolder+"{0}_e_2D.png".format(labFig))
            APy3_GENfuns.png_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True, pngFolder+"{0}_pedSub_e_2D.png".format(labFig))
            #
            auxGn2show= numpy.copy(data_Gn[thisImg,:,:]) 
            auxmap= auxGn2show<-0.1
            auxGn2show=auxGn2show.astype(float)
            auxGn2show[auxmap]= numpy.NaN
            APy3_GENfuns.png_2D_all(auxGn2show, False, "col","row","{0} [Gn level]".format(labFig), True, pngFolder+"{0}_Gn_2D.png".format(labFig))
            del auxmap; del auxGn2show
            APy3_GENfuns.printcol("png saved to "+pngFolder,'green')
    #
    elif (nextstep in ['n','N',' ']):
        thisImg=+1
        if thisImg>= data_e.shape[0]: thisImg= thisImg%data_e.shape[0]
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    #
    elif (nextstep in ['p','P',]):
        thisImg=-1
        if thisImg<0: thisImg= thisImg%data_e.shape[0]
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    #
    elif (nextstep in ['l','L']):
        thisImg=+1
        if thisImg>= data_e.shape[0]: thisImg= thisImg%data_e.shape[0]
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], True, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, True, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    #
    elif (nextstep in ['m','M',]):
        APy3_GENfuns.printcol("looking for min/max Image {1}".format(data_e.shape[0],thisImg),'green')
        #
        minval= numpy.nanmin(data_e[thisImg,:,:].flatten())
        minvaladdr= numpy.unravel_index(numpy.nanargmin(data_e[thisImg,:,:]), data_e[thisImg,:,:].shape)
        APy3_GENfuns.printcol("raw image:", 'green')
        APy3_GENfuns.printcol("min val in is {0}e in ({1},{2})".format(minval,minvaladdr[0],minvaladdr[1]), 'green')
        APy3_GENfuns.printcol("Gn= {0} in ({1},{2})".format(data_Gn[thisImg,minvaladdr[0],minvaladdr[1]],minvaladdr[0],minvaladdr[1] ), 'green')
        #
        maxval= numpy.nanmax(data_e[thisImg,:,:].flatten())
        maxvaladdr= numpy.unravel_index(numpy.nanargmax(data_e[thisImg,:,:]), data_e[thisImg,:,:].shape)
        APy3_GENfuns.printcol("max val in is {0}e in ({1},{2})".format(maxval,maxvaladdr[0],maxvaladdr[1]), 'green')
        APy3_GENfuns.printcol("Gn= {0} in ({1},{2})".format(data_Gn[thisImg,maxvaladdr[0],maxvaladdr[1]],maxvaladdr[0],maxvaladdr[1] ), 'green')
        del minval; del minvaladdr; del maxval; del maxvaladdr
        APy3_GENfuns.printcol("-", 'green')
        #
        aux_data_pedsub= data_e[thisImg,:,:]-drkPed_e
        minval= numpy.nanmin(aux_data_pedsub[:,:].flatten())
        minvaladdr= numpy.unravel_index(numpy.nanargmin(aux_data_pedsub[:,:]), aux_data_pedsub[:,:].shape)
        #
        APy3_GENfuns.printcol("dark-subtracted image:", 'green')
        APy3_GENfuns.printcol("min val in is {0}e in ({1},{2})".format(minval,minvaladdr[0],minvaladdr[1]), 'green')
        APy3_GENfuns.printcol("Gn= {0} in ({1},{2})".format(data_Gn[thisImg,minvaladdr[0],minvaladdr[1]],minvaladdr[0],minvaladdr[1] ), 'green')
        #
        maxval= numpy.nanmax(aux_data_pedsub[:,:].flatten())
        maxvaladdr= numpy.unravel_index(numpy.nanargmax(data_e[thisImg,:,:]), data_e[thisImg,:,:].shape)
        APy3_GENfuns.printcol("max val in is {0}e in ({1},{2})".format(maxval,maxvaladdr[0],maxvaladdr[1]), 'green')
        APy3_GENfuns.printcol("Gn= {0} in ({1},{2})".format(data_Gn[thisImg,maxvaladdr[0],maxvaladdr[1]],maxvaladdr[0],maxvaladdr[1] ), 'green')
        del aux_data_pedsub; del minval; del minvaladdr; del maxval; del maxvaladdr
        APy3_GENfuns.printcol("--  --  --  --", 'green')

    #
    elif (nextstep in ['o','O',]):
        APy3_GENfuns.printcol("reloading original values",'green')
        data_e= numpy.copy(data_e_Orig)
        data_Gn= numpy.copy(data_Gn_Orig)
        badPix_map= numpy.zeros_like(data_Gn[0,:,:]).astype(bool)
        APy3_GENfuns.printcol("the bad pixel map has been resetted to nothing",'green')
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), '')
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    #
    elif nextstep in ['b','B']:
        APy3_GENfuns.printcol("will remove (mark as nan) pixels in a ROI", 'blue')
        Rows2rmv= numpy.array([])
        Cols2rmv= numpy.array([])
        #
        APy3_GENfuns.printcol("ROI Rows to delete [first:last] [default is {0}]".format(Rows2rmv), 'blue')
        Rows2rmv_in= input()
        if len(Rows2rmv_in)<1: APy3_GENfuns.printcol("will keep default ROI Rows to remove {0}".format(Rows2rmv), 'blue')
        elif Rows2rmv_in in APy3_GENfuns.NOlist: Rows2rmv=[]
        elif Rows2rmv_in.isdigit(): Rows2rmv= APy3_GENfuns.matlabLike_range(Rows2rmv_in+':'+Rows2rmv_in)
        else: Rows2rmv= APy3_P2Mfuns.matlabRow(Rows2rmv_in)
        #
        APy3_GENfuns.printcol("ROI Cols to delete [first:last] [default is {0}]".format(Cols2rmv), 'blue')
        Cols2rmv_in= input()
        if len(Cols2rmv_in)<1: APy3_GENfuns.printcol("will keep default ROI Rows to remove {0}".format(Cols2rmv), 'blue')
        elif Cols2rmv_in in APy3_GENfuns.NOlist: Cols2rmv=[]
        elif Cols2rmv_in.isdigit(): Cols2rmv= APy3_GENfuns.matlabLike_range(Cols2rmv_in+':'+Cols2rmv_in)
        else: Cols2rmv= APy3_P2Mfuns.matlabCol(Cols2rmv_in)
        #
        if (len(Rows2rmv)<1)|(len(Cols2rmv)<1): APy3_GENfuns.printcol("will not remove any pixels", 'blue')
        else:
            APy3_GENfuns.printcol("ROI removed ({0}:{1},{2}:{3})".format(Rows2rmv[0],Rows2rmv[-1],Cols2rmv[0],Cols2rmv[-1]), 'blue')
            #
            badPix_map[Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]=True
            data_e[:,Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]= numpy.NaN
            data_Gn[:,Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]= -256
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(badPix_map.astype(float), False, "col","row","bad pixel map", True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    elif nextstep in ['U','u']:
        APy3_GENfuns.printcol("Easter Egg! list: mark as bad the usual suspects:", 'green')
        APy3_GENfuns.printcol("(898,1197)", 'green')
        APy3_GENfuns.printcol("(0:6,:), (1476:1483,:), (:,32), (:,1439)", 'green')
        #
        UsualSuspectBaPixelMap= numpy.zeros_like(data_Gn[0,:,:]).astype(bool)
        UsualSuspectBaPixelMap[898, 1197]=True
        UsualSuspectBaPixelMap[0:7,:]=True
        UsualSuspectBaPixelMap[1476:1484,:]=True
        UsualSuspectBaPixelMap[:,32]=True
        UsualSuspectBaPixelMap[:,1439]=True
        #
        badPix_map[UsualSuspectBaPixelMap]=True
        for jImg in range(data_e.shape[0]):
            data_e[jImg,:,:][UsualSuspectBaPixelMap]= numpy.NaN
            data_Gn[jImg,:,:][UsualSuspectBaPixelMap]= -256
        #
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(badPix_map.astype(float), False, "col","row","bad pixel map", True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
        #
    elif nextstep in ['x','X']:
        APy3_GENfuns.printcol("Easter Egg! mark as bad cols :350, 1100:, and also", 'green')
        APy3_GENfuns.printcol("(898,1197)", 'green')
        APy3_GENfuns.printcol("(0:6,:), (1476:1483,:), (:,32), (:,1439)", 'green')
        #
        UsualSuspectBaPixelMap= numpy.zeros_like(data_Gn[0,:,:]).astype(bool)
        UsualSuspectBaPixelMap[898, 1197]=True
        UsualSuspectBaPixelMap[0:7,:]=True
        UsualSuspectBaPixelMap[1476:1484,:]=True
        UsualSuspectBaPixelMap[:,32]=True
        UsualSuspectBaPixelMap[:,1439]=True
        UsualSuspectBaPixelMap[:,0:351]=True
        UsualSuspectBaPixelMap[:,1100:1440]=True
        #
        badPix_map[UsualSuspectBaPixelMap]=True
        for jImg in range(data_e.shape[0]):
            data_e[jImg,:,:][UsualSuspectBaPixelMap]= numpy.NaN
            data_Gn[jImg,:,:][UsualSuspectBaPixelMap]= -256
        #
        if pngFlag== False:
            APy3_GENfuns.plot_2D_all(badPix_map.astype(float), False, "col","row","bad pixel map", True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:], False, "col","row","{0} [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_all(data_e[thisImg,:,:]-drkPed_e, False, "col","row","{0} (dark-pedestal subtracted) [e]".format(labFig), True)
            APy3_GENfuns.plot_2D_notBelow(data_Gn[thisImg,:,:], "col","row","{0} [Gn level]".format(labFig), True, -0.1)
            APy3_GENfuns.showIt()
        else: APy3_GENfuns.printcol("png saving not implemented yet",'green')
    #
    if (nextstep in ['A','a']):
        APy3_GENfuns.printcol("there are {0} valid images in the array; will show Image {1}".format(data_e.shape[0],thisImg),'green')
        data_ADU2show_avgxGn= numpy.copy(data_ADU_avgxGn)
        data_ADU2show_avgxGn[:,:,:]= data_ADU2show_avgxGn[:,:,:]-PedestalADU_multiGn[:,:,:] #Gn0/1/2, NRow, NCol  
        auxmap=numpy.isnan(data_e[thisImg,:,:])
        for jGn in range(3):
            data_ADU2show_avgxGn[jGn,:,:][auxmap]= numpy.NaN
        del auxmap
        #
        if pngFlag== False:
            for jGn in range(3):
                APy3_GENfuns.plot_2D_all(data_ADU2show_avgxGn[jGn,:,:], False, "col","row","{0} [ADU]".format(labFig), True)
            APy3_GENfuns.showIt()
        else:
            for jGn in range(3):
                APy3_GENfuns.png_2D_all(data_ADU2show_avgxGn[jGn,:,:], False, "col","row","{0} [ADU]".format(labFig), True, pngFolder+"{1}_ADU_Gn{0}_2D.png".format(jGn,labFig))
            #
            APy3_GENfuns.printcol("png saved to "+pngFolder,'green')
    #
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:" 'green')
        APy3_GENfuns.printcol("U: mark as bad the usual suspects" 'green')
        APy3_GENfuns.printcol("X: mark as bad the usual suspects + cols :350, 1100:" 'green')
        APy3_GENfuns.printcol("A: show ADU" 'green')       
    #
    APy3_GENfuns.printcol("show [image number]/[N]ext/[P]recedent/in [L]og scale / find [M]in-max / mark [B]ad pixels / reload [O]riginal values/ [Q]uit",'green')
    nextstep= input()
#
#%% that's all folks
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
endTime=time.time()
for i_aux in range(3): APy3_GENfuns.printcol('---------','blue')
#---    



