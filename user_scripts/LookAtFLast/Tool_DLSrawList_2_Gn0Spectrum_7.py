# -*- coding: utf-8 -*-
"""
DLS file => spectrum
# 
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./Tool_DLSrawList_2_Gn0Spectrum_7.py
or:
python3
exec(open("./xxx.py").read())
"""
#%% imports and useful constants
from APy3_auxINIT import *
from APy3_P2Mfuns import *
import ast
#
import warnings
warnings.simplefilter("ignore", category=RuntimeWarning) # numpy.nanstd warns if all NaN
# ---


def versatile_1DLSrawFile_2_e(DLSraw_file,Img2proc_mtlb, CDSFlag, CMAFlag,cols2CMA,
                              ADCcor_file,multiGnCal_file,
                              flagUseAlternPed,alternPed_file,
                              highMemFlag,cleanMemFlag,verboseFlag):
    #%% load files
    if verboseFlag: APy3_GENfuns.printcol('load calibr files','blue')
    #
    if APy3_GENfuns.notFound(ADCcor_file): APy3_GENfuns.printErr('not found: '+ADCcor_file)
    (ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
     ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
    #
    if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
    (PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
    #
    if flagUseAlternPed:
        if APy3_GENfuns.notFound(alternPed_file): APy3_GENfuns.printErr('not found: '+alternPed_file)
        PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(alternPed_file, '/data/data')
    #
    if verboseFlag: APy3_GENfuns.printcol('load DLSraw file','blue')
    if APy3_GENfuns.notFound(DLSraw_file): APy3_GENfuns.printErr('not found: '+DLSraw_file)
    (auxNimgInFile,ignNRow,ignNCol)=APy3_GENfuns.size_1xh5(DLSraw_file, '/data')
    if verboseFlag: APy3_GENfuns.printcol('there are {0} images in {1}'.format(auxNimgInFile,DLSraw_file),'green')
    if Img2proc_mtlb in APy3_GENfuns.ALLlist: 
        Img2proc=numpy.arange(auxNimgInFile)
        if verboseFlag: APy3_GENfuns.printcol('will load all of them','green')
    else: 
        Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb)
        if verboseFlag: APy3_GENfuns.printcol('will load {0}:{1} of them'.format(Img2proc[0],Img2proc[-1]),'green')
    dataSmpl_DLSraw,dataRst_DLSraw= APy3_GENfuns.read_partial_2xh5(DLSraw_file, '/data','/reset', Img2proc[0],Img2proc[-1])
    #---
    if verboseFlag: APy3_GENfuns.printcol('elaborating data','blue')
    data_CMACDS_e= APy3_P2Mfuns.convert_DLSraw_2_e_wLatOvflw(dataSmpl_DLSraw,dataRst_DLSraw, CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,verboseFlag)
    return data_CMACDS_e

#
interactiveFlag=True; #interactiveFlag=False
#
#
#
#
'''
######################### BSI04_5um_1000eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.01.48.02_BSI04_5um_1000eV/airy_3of7ADC_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
#
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.02.12.50_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.02.13.07_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.02.13.31_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.02.13.49_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.02.14.06_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.02.11.03_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.02.11.22_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.02.11.45_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.02.12.02_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.02.12.21_BSI04_3of7_3TPGA666_012ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 1000
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="690:699"; ROIcols_str="530:539" # ~1.03 ph/img per pixel
#sigma_hint= 25
#A0_hint=1700; A1_hint=12000; A2_hint=4500; A3_hint=1000
#peak separation:253.967e; sigma:42.936e; separation=5.915sigma
#
ROIrows_str="710:719"; ROIcols_str="540:549" # ~0.3 ph/img per pixel
sigma_hint= 25
A0_hint=50000; A1_hint=10000; A2_hint=1000; A3_hint=100
#peak separation:256.69e; sigma:18.558e; separation=13.832sigma
'''
#
'''
######################### BSI04_5um_800eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.06.45.40_5um_800eV/airy_3of7ADU_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.06.54.14_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.54.31_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.54.48_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.55.04_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.55.21_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.06.52.48_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.53.05_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.53.22_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.53.39_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.53.56_BSI04_3of7_3TPGA666_012ms_0800eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_phEnergy_eV= 800
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="850:859"; ROIcols_str="480:489" #0.58ph/img per pix
#sigma_hint= 25
#A0_hint=40000; A1_hint=15000; A2_hint=3000; A3_hint=100
#peak separation:207.644e; sigma:23.845e; separation=8.708sigma
#
ROIrows_str="900:909"; ROIcols_str="540:549" #0.23ph/img per pix
sigma_hint= 25
A0_hint=40000; A1_hint=4000; A2_hint=400; A3_hint=40
#peak separation:203.113e; sigma:17.978e; separation=11.298sigma
'''
#
#
'''
######################### BSI04_5um_710eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.00.44.04_BSI04_5um_0710eV/airy_3of7ADC_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.01.04.51_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.01.05.13_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.01.05.30_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.01.05.48_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.01.06.07_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.01.03.06_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.01.03.27_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.01.03.45_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.01.04.03_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.01.04.22_BSI04_3of7_3TPGA666_012ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 710
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="710:719"; ROIcols_str="560:569"  #0.52ph/img per pix
#sigma_hint= 25
#A0_hint=400; A1_hint=150; A2_hint=50; A3_hint=10
#
ROIrows_str="720:729"; ROIcols_str="550:559"  #0.22ph/img per pix
sigma_hint= 25
A0_hint=40000; A1_hint=3000; A2_hint=300; A3_hint=30
#peak separation:181.123e; sigma:17.227e; separation=10.514sigma
'''
#
'''
######################### BSI04_5um_600eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.06.32.39_5um_600eV/airy_3of7ADU_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.06.41.15_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.41.33_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.41.52_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.42.09_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.42.26_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.06.39.33_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.39.51_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.40.10_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.40.26_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.40.44_BSI04_3of7_3TPGA666_012ms_0600eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 600
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#
#ROIrows_str="580:589"; ROIcols_str="600:609" #~0.61ph/img per pix
#sigma_hint= 25
#A0_hint=500; A1_hint=250; A2_hint=100; A3_hint=10
#
ROIrows_str="870:879"; ROIcols_str="550:559" #~0.22ph/img per pix
sigma_hint= 25
A0_hint=35000; A1_hint=500; A2_hint=400; A3_hint=10
#peak separation:145.069e; sigma:18.224e; separation=7.96sigma
'''
#
'''
######################### BSI04_5um_500eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.06.13.01_5um_500eV/airy_3of7ADU_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.06.27.49_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.28.07_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.28.28_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.28.45_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.29.02_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.06.26.11_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.26.30_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.26.48_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.27.05_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.06.27.24_BSI04_3of7_3TPGA666_012ms_0500eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 500
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="580:589"; ROIcols_str="550:559" #~0.70ph/img per pix
#sigma_hint= 25
#A0_hint=500; A1_hint=150; A2_hint=75; A3_hint=10
#
ROIrows_str="800:809"; ROIcols_str="540:549" #~0.19ph/img per pix
sigma_hint= 25
A0_hint=25000; A1_hint=2500; A2_hint=360; A3_hint=10
#peak separation:120.917e; sigma:17.235e; separation=7.016sigma
'''
#
'''
######################### BSI04_5um_399eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/airy_3of7ADC_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.11.22.19.58_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.22.22.08_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.22.24.18_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.22.26.27_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.22.28.37_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.11.22.08.04_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.22.11.14_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.22.13.24_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.22.15.41_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.22.17.49_BSI04_3of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 399
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="740:749"; ROIcols_str="560:569" #~0.71ph/img per pix
#sigma_hint= 25
#A0_hint=500; A1_hint=150; A2_hint=75; A3_hint=10
#
ROIrows_str="790:799"; ROIcols_str="550:559" #~0.19ph/img per pix
sigma_hint= 25
A0_hint=20000; A1_hint=2500; A2_hint=200; A3_hint=10
#2peak fit: peak separation:89.883e; sigma:16.792e; separation=5.353sigma
'''
#
'''
######################### BSI04_5um_350eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.05.14.12_5um_350eV/airy_3of7ADU_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.05.58.20_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.00.27_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.02.35_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.04.41_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.06.06.55_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.05.47.12_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.05.49.22_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.05.51.43_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.05.53.56_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.05.56.06_BSI04_3of7_3TPGA666_120ms_0350eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 350
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="590:599"; ROIcols_str="520:529" #0.65ph/img per pix
#sigma_hint= 25
#A0_hint=15000; A1_hint=8000; A2_hint=2000; A3_hint=10
#
ROIrows_str="810:819"; ROIcols_str="540:549" #0.22ph/img per pix
sigma_hint= 25
A0_hint=20000; A1_hint=2500; A2_hint=250; A3_hint=10
# 2peak-fit: peak separation:80.697e; sigma:18.338e; separation=4.4sigma
'''
#
'''
######################### BSI04_5um_300eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.04.42.26_5um_300eV/airy_3of7ADU_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.04.58.32_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.59.03_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.59.34_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.05.00.06_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.05.00.38_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.04.56.15_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.04.56.47_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.04.57.17_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.04.57.47_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.05.01.18_BSI04_3of7_3TPGA666_024ms_0300eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 300
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="830:839"; ROIcols_str="540:549" #0.54ph/img per pixel
#sigma_hint= 25
#A0_hint=14000; A1_hint=6000; A2_hint=2000; A3_hint=10 
#peak separation:69.262e; sigma:20.578e; separation=3.366sigma
#
ROIrows_str="890:899"; ROIcols_str="540:549" #0.18/img
sigma_hint= 25
A0_hint=25000; A1_hint=3200; A2_hint=3000; A3_hint=10 
# 2peak fit: peak separation:65.596e; sigma:16.729e; separation=3.921sigma
'''
#
#'''
######################### BSI04_5um_275eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.02.44.10_5um_275eV/airy_3of7ADC_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.12.04.01.11_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.01.28_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.01.46_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.02.03_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.12.04.02.23_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.12.03.59.15_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.03.59.36_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.03.59.56_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.04.00.15_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.12.04.00.40_BSI04_3of7_3TPGA666_012ms_0275eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 275
dflt_addId=", dmuxSELHigh"
this_histobins=100
#
dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#
#
#ROIrows_str="840:849"; ROIcols_str="540:549" #0.90e/img
#sigma_hint= 25
#A0_hint=10000; A1_hint=8000; A2_hint=4000; A3_hint=2000
#
ROIrows_str="910:919"; ROIcols_str="540:549" #0.32e/img
sigma_hint= 25
A0_hint=17000; A1_hint=4000; A2_hint=100; A3_hint=20
# 2peak fit: peak separation:61.486e; sigma:17.399e; separation=3.534sigma
#'''
#
'''
######################### BSI04_5um_250eV/airy_3of7ADC_3TPGA666 #########################
dflt_data_Folder='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/airy_3of7ADC_3TPGA666/DLSraw/'
if dflt_data_Folder[-1]!='/': dflt_data_Folder+='/'
dflt_data_fileList=[]
dflt_data_fileList+=["2019.12.11.23.42.36_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.23.42.56_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.23.43.18_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.23.43.39_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kpin_DLSraw.h5"]
dflt_data_fileList+=["2019.12.11.23.43.57_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kpin_DLSraw.h5"]
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_alternPed_Folder=dflt_data_Folder+'../avg_xGn/'
if dflt_alternPed_Folder[-1]!='/': dflt_alternPed_Folder+='/'
dflt_alternPed_fileList=[]
dflt_alternPed_fileList+=["2019.12.11.23.40.26_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.23.40.53_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.23.41.19_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.23.41.39_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"]
dflt_alternPed_fileList+=["2019.12.11.23.42.07_BSI04_3of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"]
#
dflt_phEnergy_eV= 250
dflt_addId=", dmuxSELHigh"
this_histobins=100
#

dflt_Img2proc='10:999'
dflt_CDSGn0Flag='Y'
dflt_CMAFlag= 'Y'
dflt_cols2CMA = '1152:1183'

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#
dflt_debugFlag=False; #dflt_debugFlag=True
#

ROIrows_str="860:869"; ROIcols_str="540:549" #1.02e/img
sigma_hint= 25
A0_hint=11000; A1_hint=10000; A2_hint=6000; A3_hint=2000
#
ROIrows_str="1000:1009"; ROIcols_str="540:549" #0.25e/img
sigma_hint= 25
A0_hint=14000; A1_hint=3300; A2_hint=100; A3_hint=20
#2peak fit: peak separation:57.01e; sigma:16.832e; separation=3.387sigma
'''
#
#
#
#---
#
if interactiveFlag:
    #%% pack arguments for GUI window
    GUIwin_arguments= []
    GUIwin_arguments+= ['folder with DLSraw files'] 
    GUIwin_arguments+= [dflt_data_Folder] 
    GUIwin_arguments+= ['data DLSraw file list'] 
    GUIwin_arguments+= [str(dflt_data_fileList)] 
    GUIwin_arguments+= ['use images [first:last]'] 
    GUIwin_arguments+= [dflt_Img2proc]
    #
    GUIwin_arguments+= ['ADC correction (Smpl/Rst,Crs/Fn,slope/offset): file'] 
    GUIwin_arguments+= [dflt_ADCcor_file]
    GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
    GUIwin_arguments+= [dflt_multiGnCal_file]
    #
    GUIwin_arguments+= ['alternative PedestalADU [Gn0] files Folder'] 
    GUIwin_arguments+= [dflt_alternPed_Folder]
    GUIwin_arguments+= ['alternative PedestalADU [Gn0] file list'] 
    GUIwin_arguments+= [str(dflt_alternPed_fileList)]
    #
    GUIwin_arguments+= ['CDS for Gn0? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_CDSGn0Flag)]
    GUIwin_arguments+= ['CMA? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_CMAFlag)]
    GUIwin_arguments+= ['if CMA: Reference Columns? [first:last]'] 
    GUIwin_arguments+= [dflt_cols2CMA]
    #
    GUIwin_arguments+= ['photon energy [eV]'] 
    GUIwin_arguments+= [str(dflt_phEnergy_eV)]
    #
    GUIwin_arguments+= ['additional id string? [if any]'] 
    GUIwin_arguments+= [str(dflt_addId)]
    #
    GUIwin_arguments+= ['high mem usage? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_highMemFlag)] 
    GUIwin_arguments+= ['clean mem when possible? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_cleanMemFlag)]
    GUIwin_arguments+= ['verbose? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_verboseFlag)]
    GUIwin_arguments+= ['debug? [Y/N]'] 
    GUIwin_arguments+= [str(dflt_debugFlag)]
    # ---
    #
    #%% GUI window
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    i_param=0
    # 
    data_Folder= dataFromUser[i_param]; i_param+=1; 
    data_fileList= APy3_GENfuns.str2list(dataFromUser[i_param]); i_param+=1; 
    #
    Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
    if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
    else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb)
    #
    ADCcor_file= dataFromUser[i_param]; i_param+=1; 
    multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
    #
    alternPed_Folder= dataFromUser[i_param]; i_param+=1; 
    alternPed_fileList= dataFromUser[i_param]; i_param+=1;
    if alternPed_Folder in APy3_GENfuns.NOlist: flagUseAlternPed=False
    elif alternPed_fileList in APy3_GENfuns.NOlist: flagUseAlternPed=False
    else: 
        flagUseAlternPed=True
        alternPed_fileList= APy3_GENfuns.str2list(alternPed_fileList)
    #
    CDSGn0Flag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    CMAFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cols2CMA_mtlb= dataFromUser[i_param]; i_param+=1
    if CMAFlag: cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
    else: cols2CMA=numpy.array([])
    #
    phEnergy_eV=float(dataFromUser[i_param]); i_param+=1
    addId= dataFromUser[i_param]; i_param+=1; 
    #
    highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    debugFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #---
else:
    # not interactive
    data_Folder= dflt_data_Folder; 
    data_fileList= dflt_data_fileList
    #
    Img2proc_mtlb= dflt_Img2proc;  
    if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
    else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb)
    #
    ADCcor_file= dflt_ADCcor_file
    multiGnCal_file= dflt_multiGnCal_file  
    #
    alternPed_Folder= dflt_alternPed_Folder 
    alternPed_fileList= dflt_alternPed_fileList
    if alternPed_Folder in APy3_GENfuns.NOlist: flagUseAlternPed=False; alternPed_fileList=[]
    elif alternPed_fileList in APy3_GENfuns.NOlist: flagUseAlternPed=False; alternPed_fileList=[]
    else: flagUseAlternPed=True
    #
    CDSGn0Flag=APy3_GENfuns.isitYes(str(dflt_CDSGn0Flag))
    CMAFlag=APy3_GENfuns.isitYes(str(dflt_CMAFlag))
    cols2CMA_mtlb= dflt_cols2CMA
    if CMAFlag: cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
    else: cols2CMA=numpy.array([])
    #
    phEnergy_eV=float(str(dflt_phEnergy_eV))
    addId= dflt_addId
    #
    highMemFlag=APy3_GENfuns.isitYes(str(dflt_highMemFlag))
    cleanMemFlag=APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag=APy3_GENfuns.isitYes(str(dflt_verboseFlag))
    debugFlag=APy3_GENfuns.isitYes(str(dflt_debugFlag))
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will use DLSraw files: {0}'.format(data_Folder),'blue')
    for thisFile in data_fileList: APy3_GENfuns.printcol('  {0}'.format(thisFile),'blue')
    APy3_GENfuns.printcol('  using images {0}'.format(Img2proc_mtlb),'blue')
    if (CDSGn0Flag): APy3_GENfuns.printcol('  will CDS for Gn0','blue')
    if (CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol{0}'.format(cols2CMA_mtlb),'blue')
    #
    APy3_GENfuns.printcol('will take ADCcor_file from {0}'.format(ADCcor_file),'blue')
    APy3_GENfuns.printcol('will take multiGnCal_file from {0}'.format(multiGnCal_file),'blue')
    if flagUseAlternPed: 
        APy3_GENfuns.printcol('will take Gn0 Pedestal from: {0}'.format(alternPed_Folder),'blue')
        for thisFile in alternPed_fileList: APy3_GENfuns.printcol('  {0}'.format(thisFile),'blue')
    else: APy3_GENfuns.printcol('will use Gn0 pedestal from multiGnCal_file','blue')
    #
    APy3_GENfuns.printcol('will consider {0}eV photons'.format(phEnergy_eV),'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if debugFlag: APy3_GENfuns.printcol('debug','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#%% load files
if verboseFlag: APy3_GENfuns.printcol('load files','blue')
#
if APy3_GENfuns.notFound(ADCcor_file): APy3_GENfuns.printErr('not found: '+ADCcor_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
 ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
#
if debugFlag:
    APy3_GENfuns.plot_2x2D(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, False,False, "col","row",
                           "ADCcorr: Smpl,crs,slope","ADCcorr: Smpl,crs,offset", True)
    APy3_GENfuns.plot_2x2D(ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, False,False, "col","row",
                           "ADCcorr: Smpl,fn,slope","ADCcorr: Smpl,fn,offset", True)
    APy3_GENfuns.plot_2x2D(ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset, False,False, "col","row",
                           "ADCcorr: Rst,crs,slope","ADCcorr: Rst,crs,offset", True)
    APy3_GENfuns.plot_2x2D(ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, False,False, "col","row",
                           "ADCcorr: Rst,fn,slope","ADCcorr: Rst,fn,offset", True)
    for thisGn in range(3):
        APy3_GENfuns.plot_2x2D(PedestalADU_multiGn[thisGn],e_per_ADU_multiGn[thisGn], False,False, "col","row",
                           "PTC: pedestal Gn{0} [ADU]".format(thisGn),"PTC: Gn{0} [e/ADU]".format(thisGn), True)
#
alternPed= APy3_GENfuns.numpy_NaNs((NRow,NCol))
if flagUseAlternPed:
    if APy3_GENfuns.notFound(alternPed_Folder): APy3_GENfuns.printErr('not found: '+alternPed_Folder)
    #alternPed_fileList= APy3_GENfuns.list_files(alternPed_Folder, '*', alternPed_suffix) # all files
    if verboseFlag: APy3_GENfuns.printcol("alternate Pedestal: {0} sets found in folder".format(len(alternPed_fileList)), 'green')
    alternPed_multiSet= APy3_GENfuns.numpy_NaNs((len(alternPed_fileList),NRow,NCol))
    for iFile,this_alternPed_file in enumerate(alternPed_fileList):
        if APy3_GENfuns.notFound(alternPed_Folder+this_alternPed_file): APy3_GENfuns.printErr('not found: '+alternPed_Folder+this_alternPed_file)
        alternPed_multiSet[iFile,:,:]= APy3_GENfuns.read_1xh5(alternPed_Folder+this_alternPed_file, '/data/data')
        if verboseFlag: APy3_GENfuns.printcol("  {0}".format(this_alternPed_file), 'green')
    PedestalADU_multiGn[0,:,:]= numpy.nanmean(alternPed_multiSet,axis=0)
    if verboseFlag: 
        APy3_GENfuns.printcol("alternate Gn0 Pedestal calculated", 'green')
        APy3_GENfuns.printcol("-", 'green')
    if cleanMemFlag: del alternPed_multiSet
# ---
#
if APy3_GENfuns.notFound(data_Folder): APy3_GENfuns.printErr('not found: '+data_Folder)
#data_fileList= APy3_GENfuns.list_files(data_Folder, '*', data_suffix) # all files
if verboseFlag: APy3_GENfuns.printcol("data: {0} image sets found in folder".format(len(data_fileList)), 'green')
data_all_e= numpy.zeros((0,NRow,NCol))
for iFile,this_data_file in enumerate(data_fileList):
    if verboseFlag: APy3_GENfuns.printcol(" {0}/{1}: {2}".format(iFile,len(data_fileList)-1,this_data_file), 'green')
    if APy3_GENfuns.notFound(data_Folder+this_data_file): APy3_GENfuns.printErr('not found: '+data_Folder+this_data_file)
    dataSmpl_in,dataRst_in= APy3_GENfuns.read_partial_2xh5(data_Folder+this_data_file, '/data','/reset', Img2proc[0],Img2proc[-1])
    # 
    data_CMACDS_e= APy3_P2Mfuns.convert_DLSraw_2_e_wLatOvflw(dataSmpl_in,dataRst_in, CDSGn0Flag, CMAFlag,cols2CMA,
                                                ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                                                ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                                                PedestalADU_multiGn,e_per_ADU_multiGn,
                                                highMemFlag,cleanMemFlag,verboseFlag)
    # ---
    # ---
    # ---
    data_all_e= numpy.append(data_all_e,data_CMACDS_e,axis=0)
    if cleanMemFlag: del data_CMACDS_e
    # ---
mode_str=""
if CMAFlag:mode_str+="CMA,"
if CDSGn0Flag:mode_str+='CDS'
else: mode_str+='Smpl'
mode_str+=addId
#
if verboseFlag: APy3_GENfuns.printcol("avg-ing", 'blue')
data_avg_e= numpy.nanmean(data_all_e, axis=0)
if verboseFlag: 
    APy3_GENfuns.printcol("data prepared", 'green')
    APy3_GENfuns.printcol("-", 'green')
# ---

#%% interactive show
APy3_GENfuns.printcol("interactive plotting", 'blue')
#
if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1; ROIrows=numpy.arange(fromRow,toRow+1)
else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
#
if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1; ROIcols=numpy.arange(fromCol,NCol+1)
else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
#
aux_min=phEnergy_eV*0.5/3.6; aux_max=phEnergy_eV*1.0/3.6
mu0_hint=0; mu1_hint=1*phEnergy_eV/3.6; mu2_hint=2*phEnergy_eV/3.6; mu3_hint=3*phEnergy_eV/3.6



#
APy3_GENfuns.printcol("show [A]vg / [F]ingerplot a pixel / [E]nd plotting", 'blue')
nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['a','A',' ']:
        APy3_GENfuns.printcol("plotting avg {0}".format(mode_str), 'blue')
        APy3_GENfuns.plot_2D_all(data_avg_e, False,'col','row','{0}eV photons: avg {1} [e]'.format(round(phEnergy_eV,1),mode_str), True)
        APy3_GENfuns.plot_2D_all(data_avg_e, True,'col','row','{0}eV photons: avg {1} [e]'.format(round(phEnergy_eV,1),mode_str), True)
        APy3_GENfuns.showIt()
    #---
    elif nextstep in ['f','F']:
        APy3_GENfuns.printcol("fingerplot spectrum:", 'blue')
        #
        APy3_GENfuns.printcol("which Rows? [first:last] [dflt is {0}]".format(ROIrows_str), 'green'); ROIrows_in= input(); 
        if len(ROIrows_in)==0: APy3_GENfuns.printcol("will keep ROIrows {0}".format(ROIrows_str), 'green')
        else: ROIrows_str= str(ROIrows_in); APy3_GENfuns.printcol("will use ROIrows {0}".format(ROIrows_str), 'green')
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]        
        #
        APy3_GENfuns.printcol("which Cols? [first:last] [dflt is {0}]".format(ROIcols_str), 'green'); ROIcols_in= input(); 
        if len(ROIcols_in)==0: APy3_GENfuns.printcol("will keep ROIcols {0}".format(ROIcols_str), 'green')
        else: ROIcols_str= str(ROIcols_in); APy3_GENfuns.printcol("will use ROIcols {0}".format(ROIcols_str), 'green')
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        #
        APy3_GENfuns.printcol("how many bins? [dflt is {0}]".format(this_histobins), 'green'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("plotting fingerplot spectrum of pix ({0},{1}), {2} bins".format(ROIrows_str,ROIcols_str,this_histobins), 'blue')
        #
        data_ROI_e= data_all_e[:,fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        aux_NofNaNs= numpy.sum(numpy.isnan(data_ROI_e))
        data_ROI_e= data_ROI_e[~numpy.isnan(data_ROI_e)]
        APy3_GENfuns.printcol("avg of ROI ({0},{1}) (ignoring nans)= {2}e/img per pixel".format(ROIrows_str,ROIcols_str,numpy.nanmean(data_ROI_e)), 'green')
        APy3_GENfuns.printcol("  equivalent to = {2}ph/img per pixel (photon energy: {3}eV)".format(ROIrows_str,ROIcols_str,numpy.nanmean(data_ROI_e)/(phEnergy_eV/3.6),phEnergy_eV), 'green')
        APy3_GENfuns.printcol("note that {0} NaN values had been excluded for this evaluation".format(aux_NofNaNs), 'green')
        #
        if ( len(data_ROI_e)==0 ) : APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            APy3_GENfuns.plot_histo1D(data_ROI_e, this_histobins, False, "collected charge [e]","occurrences",
                                       "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str,round(phEnergy_eV,1)))
            APy3_GENfuns.plot_histo1D(data_ROI_e, this_histobins, True,  "collected charge [e]","occurrences",
                                       "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str,round(phEnergy_eV,1)))
            APy3_GENfuns.showIt()
            #
            #APy3_GENfuns.plot_histo1D(data_ROI_e*3.6, this_histobins, False, "collected charge [eV]","occurrences",
            #                           "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str,round(phEnergy_eV,1)))
            #APy3_GENfuns.plot_histo1D(data_ROI_e*3.6, this_histobins, True,  "collected charge [eV]","occurrences",
            #                           "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str,round(phEnergy_eV,1)))
            #APy3_GENfuns.showIt()
            if cleanMemFlag: del data_ROI_e
    # ---
    elif nextstep in ['m','M','<','>']:
        APy3_GENfuns.printcol("Easter Egg! find region with avg output between Min and Max ", 'blue')
        APy3_GENfuns.printcol("which min? [e] [dflt is {0}]".format(aux_min), 'green'); aux_min_str= input(); 
        if aux_min_str.isdigit(): aux_min= int(aux_min_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("which max? [e] [dflt is {0}]".format(aux_max), 'green'); aux_max_str= input(); 
        if aux_max_str.isdigit(): aux_max= int(aux_max_str) # otherwise keeps the old value
        #
        aux_map= (data_avg_e >= aux_min)&(data_avg_e <= aux_max)
        data_avg_e_btwminmax= APy3_GENfuns.numpy_NaNs_like(data_avg_e)
        data_avg_e_btwminmax[aux_map]= numpy.copy(data_avg_e[aux_map])
        APy3_GENfuns.plot_2D_all(data_avg_e_btwminmax, False,'col','row',
                                 '{0}<=avg<={1} {2} [e]'.format(round(aux_min,2),round(aux_max,2),mode_str), True)
        APy3_GENfuns.showIt()
    # ---
    elif nextstep in ['s','S']:
        APy3_GENfuns.printcol("Easter Egg! superimposed fingerplot spectra of several pixels:", 'blue')
        #
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [dflt is {0}]".format(ROIrows_str), 'green'); 
        ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= str(ROIrows_in) # otherwise keeps the old value
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        #
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [dflt is {0}]".format(ROIcols_str), 'green'); 
        ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= str(ROIcols_in) # otherwise keeps the old value
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        #
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        #
        APy3_GENfuns.printcol("how many bins? [dflt is {0}]".format(this_histobins), 'green'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("will estimate noise using ROI {0}".format(ROIstring), 'green')
        APy3_GENfuns.printcol("plotting fingerplot spectrum of pix in {0}, {1} bins".format(ROIstring,this_histobins), 'blue')
        #
        legendList=[]
        for iRow in ROIrows:
            for iCol in ROIcols:
                legendList += ['('+str(iRow)+','+str(iCol)+')']
        (auxNImg,ROINRow,ROINCol)= data_all_e[:,fromRow:toRow+1,fromCol:toCol+1].shape
        multiPix_e= data_all_e[:,fromRow:toRow+1,fromCol:toCol+1].reshape((auxNImg,ROINRow*ROINCol))
        APy3_GENfuns.plot_multihisto1D(multiPix_e, this_histobins, False, legendList, "ROI output [e]","occurrences", "{2}eV photons: ROI {0}, {1}".format(ROIstring,mode_str,round(phEnergy_eV,1)) , True)
        APy3_GENfuns.showIt()
        #
        multiPix_e_together= data_all_e[:,fromRow:toRow+1,fromCol:toCol+1].reshape((auxNImg*ROINRow*ROINCol))
        if (numpy.isnan(multiPix_e_together).all()):
            APy3_GENfuns.printcol("no data to plot in ROI {0}".format(ROIstring), 'orange')
        else:
            APy3_GENfuns.plot_histo1D(multiPix_e_together, this_histobins, False, "collected charge [e]","occurrences",
                                       "{0}eV photons: ROI {1}, {2}".format(round(phEnergy_eV,1),ROIstring,mode_str))
            APy3_GENfuns.plot_histo1D(multiPix_e_together, this_histobins, True,  "collected charge [e]","occurrences",
                                       "{0}eV photons: ROI {1}, {2}".format(round(phEnergy_eV,1),ROIstring,mode_str))
            APy3_GENfuns.showIt()
            if cleanMemFlag: del multiPix_e_together
    #--- 
    elif nextstep in ['2']:
        APy3_GENfuns.printcol("Easter Egg! Fit of photon peaks as 2 gaussians (Noise,1ph):", 'green')
        #
        APy3_GENfuns.printcol("which Rows? [first:last] [dflt is {0}]".format(ROIrows_str), 'green'); ROIrows_in= input(); 
        if len(ROIrows_in)==0: APy3_GENfuns.printcol("will keep ROIrows {0}".format(ROIrows_str), 'green')
        else: ROIrows_str= str(ROIrows_in); APy3_GENfuns.printcol("will use ROIrows {0}".format(ROIrows_str), 'green')
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        #
        APy3_GENfuns.printcol("which Cols? [first:last] [dflt is {0}]".format(ROIcols_str), 'green'); ROIcols_in= input(); 
        if len(ROIcols_in)==0: APy3_GENfuns.printcol("will keep ROIcols {0}".format(ROIcols_str), 'green')
        else: ROIcols_str= str(ROIcols_in); APy3_GENfuns.printcol("will use ROIcols {0}".format(ROIcols_str), 'green')
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        #
        data_ROI_e= data_all_e[:,fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        data_ROI_e= data_ROI_e[~numpy.isnan(data_ROI_e)]
        #
        APy3_GENfuns.printcol("hint: 1-ph peak expected centered at: [default is {0}]".format(mu1_hint), 'green'); mu1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu1_hint_str): mu1_hint= float(mu1_hint_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("hint: sigma peaks expected: [default is {0}]".format(sigma_hint), 'green'); sigma_hint_str= input(); 
        if APy3_GENfuns.isitfloat(sigma_hint_str): sigma_hint= float(sigma_hint_str) # otherwise keeps the old value

        APy3_GENfuns.printcol("hint: 0-ph peak expected amplitude: [default is {0}]".format(A0_hint), 'green'); A0_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A0_hint_str): A0_hint= float(A0_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 1-ph peak expected amplitude: [default is {0}]".format(A1_hint), 'green'); A1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A1_hint_str): A1_hint= float(A1_hint_str) # otherwise keeps the old value
        #
        if ( len(data_ROI_e)==0 ) : APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            freq, edges = numpy.histogram(data_ROI_e,this_histobins) 
            midpoints= 0.5*(edges[1:]+ edges[:-1])
            (A0_fit,mu0_fit, A1_fit,mu1_fit, sigma_fit)= APy3_FITfuns.spectrum2peaks_fit(midpoints,freq, A0_hint,mu0_hint, A1_hint,mu1_hint, sigma_hint)
            fit_X= numpy.arange(int(min(midpoints)),int(max(midpoints)))
            fit_Y= APy3_FITfuns.spectrum2peaks_fun(fit_X, A0_fit,mu0_fit, A1_fit,mu1_fit, sigma_fit)
            APy3_GENfuns.printcol("0-ph peak:{0}e; 1-ph peak:{1}e; sigma:{2}e".format(round(mu0_fit,3),round(mu1_fit,3),round(sigma_fit,3)), 'green')
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, False, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.showIt() 
            #
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, True, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "meas peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.printcol("peak separation:{0}e ({3}% of expected); sigma:{1}e; separation={2}sigma".format(round(peakSepar,3),round(sigma_fit,3),round(peakSepar/sigma_fit,3),round(100*peakSepar/(phEnergy_eV/3.6),2)), 'green')
            APy3_GENfuns.showIt()
            if cleanMemFlag: del data_ROI_e
    #--- 
    elif nextstep in ['3']:
        APy3_GENfuns.printcol("Easter Egg! Fit of photon peaks as 3 gaussians (Noise,1ph,2ph):", 'green')
        #
        APy3_GENfuns.printcol("which Rows? [first:last] [dflt is {0}]".format(ROIrows_str), 'green'); ROIrows_in= input(); 
        if len(ROIrows_in)==0: APy3_GENfuns.printcol("will keep ROIrows {0}".format(ROIrows_str), 'green')
        else: ROIrows_str= str(ROIrows_in); APy3_GENfuns.printcol("will use ROIrows {0}".format(ROIrows_str), 'green')
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        #
        APy3_GENfuns.printcol("which Cols? [first:last] [dflt is {0}]".format(ROIcols_str), 'green'); ROIcols_in= input(); 
        if len(ROIcols_in)==0: APy3_GENfuns.printcol("will keep ROIcols {0}".format(ROIcols_str), 'green')
        else: ROIcols_str= str(ROIcols_in); APy3_GENfuns.printcol("will use ROIcols {0}".format(ROIcols_str), 'green')
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        #
        data_ROI_e= data_all_e[:,fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        data_ROI_e= data_ROI_e[~numpy.isnan(data_ROI_e)]
        #
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'green'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("hint: 1-ph peak expected centered at: [default is {0}]".format(mu1_hint), 'green'); mu1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu1_hint_str): mu1_hint= float(mu1_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 2-ph peak expected centered at: [default is {0}]".format(mu2_hint), 'green'); mu2_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu2_hint_str): mu2_hint= float(mu2_hint_str) # otherwise keeps the old value

        APy3_GENfuns.printcol("hint: sigma peaks expected: [default is {0}]".format(sigma_hint), 'green'); sigma_hint_str= input(); 
        if APy3_GENfuns.isitfloat(sigma_hint_str): sigma_hint= float(sigma_hint_str) # otherwise keeps the old value

        APy3_GENfuns.printcol("hint: 0-ph peak expected amplitude: [default is {0}]".format(A0_hint), 'green'); A0_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A0_hint_str): A0_hint= float(A0_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 1-ph peak expected amplitude: [default is {0}]".format(A1_hint), 'green'); A1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A1_hint_str): A1_hint= float(A1_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 2-ph peak expected amplitude: [default is {0}]".format(A2_hint), 'green'); A2_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A2_hint_str): A2_hint= float(A2_hint_str) # otherwise keeps the old value
        #
        if ( len(data_ROI_e)==0 ) : APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            freq, edges = numpy.histogram(data_ROI_e,this_histobins) 
            midpoints= 0.5*(edges[1:]+ edges[:-1])
            (A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, sigma_fit)= APy3_FITfuns.spectrum3peaks_fit(midpoints,freq, A0_hint,mu0_hint, A1_hint,mu1_hint, A2_hint,mu2_hint, sigma_hint)
            fit_X= numpy.arange(int(min(midpoints)),int(max(midpoints)))
            fit_Y= APy3_FITfuns.spectrum3peaks_fun(fit_X, A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, sigma_fit)
            APy3_GENfuns.printcol("0-ph peak:{0}e; 1-ph peak:{1}e; 2-ph peak:{2}e; sigma:{3}e".format(round(mu0_fit,3),round(mu1_fit,3),round(mu2_fit,3),round(sigma_fit,3)), 'green')
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, False, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "meas peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.showIt() 
            #
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, True, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "meas peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.printcol("peak separation:{0}e ({3}% of expected); sigma:{1}e; separation={2}sigma".format(round(peakSepar,3),round(sigma_fit,3),round(peakSepar/sigma_fit,3),round(100*peakSepar/(phEnergy_eV/3.6),2)), 'green')
            APy3_GENfuns.showIt()
            if cleanMemFlag: del data_ROI_e
    #--- 
    elif nextstep in ['4']:
        APy3_GENfuns.printcol("Easter Egg! Fit of photon peaks as 4 gaussians (Noise,1ph,2ph,3ph):", 'green')
        #
        APy3_GENfuns.printcol("which Rows? [first:last] [dflt is {0}]".format(ROIrows_str), 'green'); ROIrows_in= input(); 
        if len(ROIrows_in)==0: APy3_GENfuns.printcol("will keep ROIrows {0}".format(ROIrows_str), 'green')
        else: ROIrows_str= str(ROIrows_in); APy3_GENfuns.printcol("will use ROIrows {0}".format(ROIrows_str), 'green')
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        #
        APy3_GENfuns.printcol("which Cols? [first:last] [dflt is {0}]".format(ROIcols_str), 'green'); ROIcols_in= input(); 
        if len(ROIcols_in)==0: APy3_GENfuns.printcol("will keep ROIcols {0}".format(ROIcols_str), 'green')
        else: ROIcols_str= str(ROIcols_in); APy3_GENfuns.printcol("will use ROIcols {0}".format(ROIcols_str), 'green')
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        #
        data_ROI_e= data_all_e[:,fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        data_ROI_e= data_ROI_e[~numpy.isnan(data_ROI_e)]
        #
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'green'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("hint: 1-ph peak expected centered at: [default is {0}]".format(mu1_hint), 'green'); mu1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu1_hint_str): mu1_hint= float(mu1_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 2-ph peak expected centered at: [default is {0}]".format(mu2_hint), 'green'); mu2_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu2_hint_str): mu2_hint= float(mu2_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 3-ph peak expected centered at: [default is {0}]".format(mu3_hint), 'green'); mu3_hint_str= input(); 
        if APy3_GENfuns.isitfloat(mu3_hint_str): mu3_hint= float(mu3_hint_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("hint: sigma peaks expected: [default is {0}]".format(sigma_hint), 'green'); sigma_hint_str= input(); 
        if APy3_GENfuns.isitfloat(sigma_hint_str): sigma_hint= float(sigma_hint_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("hint: 0-ph peak expected amplitude: [default is {0}]".format(A0_hint), 'green'); A0_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A0_hint_str): A0_hint= float(A0_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 1-ph peak expected amplitude: [default is {0}]".format(A1_hint), 'green'); A1_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A1_hint_str): A1_hint= float(A1_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 2-ph peak expected amplitude: [default is {0}]".format(A2_hint), 'green'); A2_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A2_hint_str): A2_hint= float(A2_hint_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("hint: 3-ph peak expected amplitude: [default is {0}]".format(A3_hint), 'green'); A3_hint_str= input(); 
        if APy3_GENfuns.isitfloat(A3_hint_str): A3_hint= float(A3_hint_str) # otherwise keeps the old value
        #
        if ( len(data_ROI_e)==0 ) : APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            freq, edges = numpy.histogram(data_ROI_e,this_histobins) 
            midpoints= 0.5*(edges[1:]+ edges[:-1])
            (A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, A3_fit,mu3_fit, sigma_fit)= APy3_FITfuns.spectrum4peaks_fit(midpoints,freq, A0_hint,mu0_hint, A1_hint,mu1_hint, A2_hint,mu2_hint, A3_hint,mu3_hint, sigma_hint)
            fit_X= numpy.arange(int(min(midpoints)),int(max(midpoints)))
            fit_Y= APy3_FITfuns.spectrum4peaks_fun(fit_X, A0_fit,mu0_fit, A1_fit,mu1_fit, A2_fit,mu2_fit, A3_fit,mu3_fit, sigma_fit)
            APy3_GENfuns.printcol("0-ph peak:{0}e; 1-ph peak:{1}e; 2-ph peak:{2}e; 3-ph peak:{3}e; sigma:{4}e".format(round(mu0_fit,3),round(mu1_fit,3),round(mu2_fit,3),round(mu3_fit,3),round(sigma_fit,3)), 'green')
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, False, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "meas peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.showIt() 
            #
            APy3_GENfuns.plot_histo1D_and_curve(data_ROI_e,this_histobins, fit_X, fit_Y, True, "collected charge [e]", "occurrences", "{3}eV photons: pix({0},{1}), {2}".format(ROIrows_str,ROIcols_str,mode_str, round(phEnergy_eV,1)))
            peakSepar= mu1_fit-mu0_fit
            aux_separ_str= "meas peak separation= {0}e\n({1}% of expected)".format(round(peakSepar,3),round(100*peakSepar/(phEnergy_eV/3.6),2))
            matplotlib.pyplot.text(0.95, 0.95, aux_separ_str, transform=matplotlib.pyplot.gca().transAxes, va = "top", ha="right")
            APy3_GENfuns.printcol("peak separation:{0}e ({3}% of expected); sigma:{1}e; separation={2}sigma".format(round(peakSepar,3),round(sigma_fit,3),round(peakSepar/sigma_fit,3),round(100*peakSepar/(phEnergy_eV/3.6),2)), 'green')
            APy3_GENfuns.showIt()
            if cleanMemFlag: del data_ROI_e
    # ---
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:", 'blue')
        APy3_GENfuns.printcol(" M,<,>: find region with avg output between Min and Max", 'blue')
        APy3_GENfuns.printcol(" S: superimposed fingerplot spectra of individual pixels", 'blue')
        APy3_GENfuns.printcol(" 2: fingerplot fit: 0,1-photon peak ", 'blue')
        APy3_GENfuns.printcol(" 3: fingerplot fit: 0,1,2-photon peak ", 'blue')
        APy3_GENfuns.printcol(" 4: fingerplot fit: 0,1,2,3-photon peak ", 'blue')
    #
    APy3_GENfuns.printcol("show [A]vg / [F]ingerplot a pixel / [E]nd plotting", 'blue')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
#

#---
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')

