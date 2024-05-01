# -*- coding: utf-8 -*-
"""
DLSraw => eval noise for Smpl/Rst,CDS,CDS-CMA
#
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./Tool_DLSraw_2_Noise_SmplRst_5_GnDependent.py
or:
python3
exec(open("./Tool_DLSraw_2_Noise_SmplRst_5_GnDependent.py").read())
"""
#%% imports and useful constants
from APy3_auxINIT import *
numpy.seterr(divide='ignore', invalid='ignore')

import warnings
warnings.simplefilter("ignore", category=RuntimeWarning) # numpy.nanstd warns if all NaN

# ---
# auxiliary functions

def png_1D(arrayX, arrayY, label_x,label_y,label_title, filenamepath):
    ''' 1D scatter plot: save(not show): e.g. filenamepath='/tmp/test0.png' ''' 
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(arrayX, arrayY, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_histo1D(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title, filenamepath):
    """ plot a histogram: save(not show) as png """
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist(array_2plot, bins=histobins)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_2D_all(array2D, logScaleFlag, label_x,label_y,label_title, invertx_flag, filenamepath):
    ''' 2D image: save(not show) as png''' 
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    if logScaleFlag: matplotlib.pyplot.imshow(array2D, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();  
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return
#---
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#
#%% data from here



'''
####################################### BSI04, BSI04_03 3TGn0 PGA666 T-20 7/7 #############################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200304_000_BSI04_drk_severaltint/processed/BSI04_3TPGA666_drk_severaltint_Tm20/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#
dflt_infile= "2020.03.04.17.10.07_BSI04_Tm20_dmuxSELsw_biasBSI04_03_012ms_Tm20_3TGn0_PGA666_1kdrk_DLSraw.h5" 
#dflt_infile= "2020.03.04.17.10.54_BSI04_Tm20_dmuxSELsw_biasBSI04_03_012ms_Tm20_3TGn0_PGA666_1kdrk_DLSraw.h5" 
#dflt_infile= "2020.03.04.17.11.51_BSI04_Tm20_dmuxSELsw_biasBSI04_03_012ms_Tm20_3TGn0_PGA666_1kdrk_DLSraw.h5" 
#dflt_infile= "2020.03.04.17.12.45_BSI04_Tm20_dmuxSELsw_biasBSI04_03_012ms_Tm20_3TGn0_PGA666_1kdrk_DLSraw.h5" 
#dflt_infile= "2020.03.04.17.13.16_BSI04_Tm20_dmuxSELsw_biasBSI04_03_012ms_Tm20_3TGn0_PGA666_1kdrk_DLSraw.h5" 
#
#dflt_infile= "" 
#dflt_infile= "" 
#dflt_infile= "" 
#dflt_infile= "" 
#dflt_infile= "" 
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'

dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse='same'
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True
dflt_saveFolder='/home/marras/auximg/'
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
####################################### BSI04, BSI04_03 3TGn0 PGABBB T-20 7/7 #############################################################
#dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/'
#if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#dflt_infile= "2019.12.11.23.53.30_BSI04_7of7_3GPGABBB_012ms_0250eV_5um_1kdrk_DLSraw.h5" 

#dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/LatOvlw_7of7ADC_3GPGABBB_higherFlux/DLSraw/'
#dflt_infile= '2019.12.11.22.54.45_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kdrk_DLSraw.h5'

dflt_folder_data2process="/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.00.44.04_BSI04_5um_0710eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/"
dflt_infile= "2019.12.12.01.16.46_BSI04_7of7_3GPGABBB_060ms_0710eV_5um_1kdrk_DLSraw.h5"
#gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/LatOvlw_7of7ADC_3GPGABBB_lowerFlux/DLSraw/
#2019.12.11.22.37.22_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kdrk_DLSraw.h5
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'

dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse='same'
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True
dflt_saveFolder='/home/marras/auximg/'
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
####################################### BSI04, BSI04_02 3/7 3Gdrk(Gn0 pixels) PGABBB, T-20 ################################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/DLSraw_1kdrk/'
#dflt_infile= "2020.03.16.18.07.51_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_DLSraw.h5" # 3G
#dflt_infile= "2020.03.16.18.08.16_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_DLSraw.h5"
#dflt_infile= "2020.03.16.18.08.44_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_DLSraw.h5"
#dflt_infile= "2020.03.16.18.09.08_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_DLSraw.h5"
dflt_infile= "2020.03.16.18.09.33_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_DLSraw.h5"
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse=0
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True; #dflt_CMAFlag=False
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True; dflt_showFlag= False
dflt_saveFolder='/home/marras/auximg/'
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
####################################### BSI04, BSI04_02 3/7 fixGn0 PGABBB, T-20 ################################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/DLSraw/'
dflt_infile= "BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_ODx.x_t012ms_500drk_DLSraw.h5" # fixGn0
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:499' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse=0
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True; #dflt_CMAFlag=False
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True; dflt_showFlag= False
dflt_saveFolder='/home/marras/auximg/'
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
####################################### BSI04, BSI04_02 3/7 fixGn1 PGABBB, T-20 ################################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn1_PGABBB/DLSraw/' 
dflt_infile= "BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn1_PGABBB_ODx.x_t012ms_500drk_DLSraw.h5" # Gn0 in the file, but actually fixGn1
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:499' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse=1
dflt_CDSFlag=True; dflt_CDSFlag=False
dflt_CMAFlag= True; dflt_CMAFlag=False
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True; dflt_showFlag= False
dflt_saveFolder='/home/marras/auximg/'
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
####################################### BSI04, BSI04_02 3/7 fixGn2 PGABBB, T-20 ################################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn2_PGABBB/DLSraw/' 
dflt_infile= "BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn2_PGABBB_ODx.x_t012ms_500drk_DLSraw.h5" # Gn0 in the file, but actually fixGn2
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:499' # 'all'==all
#
dflt_GnToUse=0
dflt_GnParamToUse=2
dflt_CDSFlag=True; dflt_CDSFlag=False
dflt_CMAFlag= True; dflt_CMAFlag=False
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True; dflt_showFlag= False
dflt_saveFolder='/home/marras/auximg/'
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
#'''
####################################### BSI04, BSI04_03 variousGn&PGA T-20 7/7 #############################################################
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_000_BSI04_7of7_drk/processed/BSI04_7of7_drk/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#
### 7/7 biasBSI04_04 3G,PGABBB t012ms
dflt_infile= "2020.04.06.07.38.08_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.38.08_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.38.32_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.38.54_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.39.18_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5" 

#dflt_infile= "2020.04.06.08.08.25_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3Gn_PGABBB_t025ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.06.08.09.12_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3Gn_PGABBB_t050ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.06.08.10.23_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3Gn_PGABBB_t075ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.06.08.11.55_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3Gn_PGABBB_t100ms_1kdk_DLSraw.h5"
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#dflt_GnToUse=0
#dflt_GnParamToUse='same'
# t12ms: 
#noise CMA(704:735),CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.745e +/- 28.939e  ; in ROI(:,:) = 84.622e +/- 28.381e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 118.247e +/- 43.938e  ; in ROI(:,:) = 118.381e +/- 43.934e
#noise CMA(704:735),CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.745e +/- 28.939e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 118.247e +/- 43.938e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.773e +/- 28.972e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 118.436e +/- 43.913e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.717e +/- 28.863e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 118.113e +/- 43.774e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.718e +/- 28.830e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 118.479e +/- 43.950e
#
# t25ms:
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.90095960301088e +/- 29.189345462275483e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.02215351623704e +/- 44.902165877082275e
#t50ms:
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.07863629655097e +/- 29.14453311445098e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.47382120533513e +/- 44.986394128006616e
#t75ms:
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.26746791727322e +/- 29.834481803182996e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.38915769250418e +/- 45.088134832628256e
#t100ms:
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.53686164961512e +/- 29.3551013758466e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.56891724517334e +/- 45.28022791921827e
#
### 7/7 biasBSI04_04 fixGn0,PGABBB t012ms
#dflt_infile= "2020.04.06.07.44.53_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn0_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.45.22_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn0_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.45.42_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn0_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.46.06_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn0_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.46.25_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn0_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#dflt_GnToUse=0
#dflt_GnParamToUse='same'
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.079e +/- 28.994e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.187e +/- 43.184e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 83.995e +/- 28.978e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.168e +/- 43.213e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.025e +/- 29.048e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.037e +/- 43.051e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 84.076e +/- 29.104e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.129e +/- 43.228e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 119.312e +/- 43.056e
#
### 7/7 biasBSI04_04 fixGn1,PGABBB t012ms
#dflt_infile= "2020.04.06.07.51.50_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn1_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.52.11_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn1_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.52.39_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn1_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.53.07_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn1_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.07.53.34_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn1_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#dflt_GnToUse=0
#dflt_GnParamToUse='1'
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn1= 593.714e +/- 355.317e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn1= 593.7062226102871e +/- 354.68854154713597e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn1= 593.6125257954602e +/- 354.6268700793355e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn1= 593.0534651525135e +/- 354.0777870736237e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn1= 591.8756910151931e +/- 353.6663834009979e
#
### 7/7 biasBSI04_04 fixGn2,PGABBB t012ms
#dflt_infile= "2020.04.06.08.01.04_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn2_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.01.31_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn2_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.01.53_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn2_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.02.14_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn2_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.02.35_BSI04_Tm20_dmuxSELsw_biasBSI04_04_fixGn2_PGABBB_t012ms_1kdk_DLSraw.h5" 
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#dflt_GnToUse=0
#dflt_GnParamToUse=2
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn2= 5231.862148181197e +/- 3172.568960472487e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn2= 5230.164742230352e +/- 3182.2770265643535e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn2= 5227.064344455864e +/- 3174.8411122960365e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn2= 5231.5859308649115e +/- 3171.5973846984634e
#noise Smpl, avg in ROI(0:1483,350:1100) with Gn2= 5243.35527796441e +/- 3186.0201085189133e
#
### 7/7 biasBSI04_04 fixGn0,PGA666 t012ms
#dflt_infile= "2020.04.06.08.18.39_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.19.00_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.19.27_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.19.47_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t012ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.20.12_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.06.08.20.39_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t025ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.21.18_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t050ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.22.23_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t075ms_1kdk_DLSraw.h5" 
#dflt_infile= "2020.04.06.08.23.57_BSI04_Tm20_dmuxSELsw_biasBSI04_03_fixGn0_PGA666_t100ms_1kdk_DLSraw.h5"
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#dflt_GnToUse=0
#dflt_GnParamToUse='same'
#
#t12ms
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 22.3871983268014e +/- 8.023685594469852e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.070145849668638e +/- 7.876809924216687e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 22.387354590433006e +/- 8.022185009110725e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.068905541927467e +/- 7.882620403536171e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 22.389341623382702e +/- 8.017622797261225e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.098403881379387e +/- 7.8796771562341394e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 22.48332112737654e +/- 7.977370679888493e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.815131855764832e +/- 8.149679540062488e
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 23.688133536211115e +/- 8.312916556383612e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 40.07548689890586e +/- 24.90840417948258e
#
#t25ms
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 23.55028678494336e +/- 8.15437440702935e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 38.81768791924418e +/- 23.07992936890114e
#t50
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.537335857118727e +/- 8.647785676013712e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 49.373602142690615e +/- 35.382776776670795e
#t75
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 24.351954559222637e +/- 8.338665421160545e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 44.60495457230699e +/- 29.380187954148898e
#100ms
#noise CMA,CDS, avg in ROI(0:1483,350:1100) with Gn0= 23.200467635779273e +/- 7.994007440418508e
#noise CDS, avg in ROI(0:1483,350:1100) with Gn0= 25.407615272746284e +/- 8.104024126495801e
#
# again 7/7, 3G, 12ms
#dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_000_BSI04_7of7_drk/processed/BSI04_7of7_drk_v2/DLSraw/'
#if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'

#dflt_infile= "2020.04.14.11.52.51_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.14.11.53.49_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.14.11.55.12_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.14.11.55.57_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.04.14.11.56.26_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"

dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'approx_BSI04_Tm20_dmuxSELsw_biasBSI04_05_PGA6BB_Gn012_MultiGnCal.h5'

dflt_GnToUse=0
dflt_GnParamToUse='same'
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#'''
#
'''
##### BSI04, BSI04_05 T-20 3/7 #####
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/drk_LatOvflow_PGA6BB_biasBSI04_05/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#dflt_infile= "2020.05.05.16.41.52_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.42.18_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.42.46_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.43.20_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
dflt_infile= "2020.05.05.16.43.42_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= ""
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
#
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
#dflt_GnToUse=0; dflt_GnParamToUse='same'
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
dflt_GnToUse=1; dflt_GnParamToUse='same'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= True; #dflt_CMAFlag=False
#dflt_cols2CMA = '32:63'
dflt_cols2CMA = '704:735'
#
dflt_showFlag= True; #dflt_showFlag= False

dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
#
#
#dflt_saveFolder='/home/marras/auximg/'
dflt_saveFolder='NONE'


#
#---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['DLSraw file to process'] 
GUIwin_arguments+= [dflt_infile]
#
GUIwin_arguments+= ['ADUcorr: file'] 
GUIwin_arguments+= [dflt_ADUcorr_file]
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
#
GUIwin_arguments+= ['data in Gn [0/1/2]'] 
GUIwin_arguments+= [str(dflt_GnToUse)]

GUIwin_arguments+= ['using parameters for Gn [0/1/2/same]'] 
GUIwin_arguments+= [str(dflt_GnParamToUse)]

GUIwin_arguments+= ['  if Gn0: CDS? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CDSFlag)]
GUIwin_arguments+= ['  if Gn0: CMA? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CMAFlag)]
GUIwin_arguments+= ['  if CMA: Reference Columns? [first:last]'] 
GUIwin_arguments+= [dflt_cols2CMA]
#
GUIwin_arguments+= ['show? [Y/N]'] 
GUIwin_arguments+= [str(dflt_showFlag)]

GUIwin_arguments+= ['save png instead of showing: folder [NONE noto to do it]']
GUIwin_arguments+= [str(dflt_saveFolder)]



#
GUIwin_arguments+= ['high mem usage? [Y/N]'] 
GUIwin_arguments+= [str(dflt_highMemFlag)] 
GUIwin_arguments+= ['clean mem when possible? [Y/N]'] 
GUIwin_arguments+= [str(dflt_cleanMemFlag)]
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [str(dflt_verboseFlag)]
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
i_param=0
folder_data2process= dataFromUser[i_param]; i_param+=1
infile= dataFromUser[i_param]; i_param+=1
#
ADUcorr_file= dataFromUser[i_param]; i_param+=1;  
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1];
#
GnToUse= int(dataFromUser[i_param]); i_param+=1
GnParamToUse_str= dataFromUser[i_param]; i_param+=1;
if GnParamToUse_str in ['same','Same','SAME']: GnParamToUse= GnToUse
else: GnParamToUse= int(GnParamToUse_str)
#
if (GnToUse==0)&(GnParamToUse==0): CDSFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
else: CDSFlag=False; i_param+=1

if (GnToUse==0)&(GnParamToUse==0): 
    CMAFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
else: CMAFlag=False; i_param+=1 

cols2CMA_mtlb= dataFromUser[i_param]; i_param+=1
cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1

saveFolder= dataFromUser[i_param]; i_param+=1;
if saveFolder in APy3_GENfuns.NOlist: saveFlag=False
else: saveFlag=True

#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#---
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using file {0}'.format(infile),'blue')
    APy3_GENfuns.printcol('will ADU-correct using {0}'.format(ADUcorr_file),'blue')
    APy3_GENfuns.printcol('  assuming Gn{0} Pedestal[ADU] and e/ADU data from {1}'.format(GnToUse,multiGnCal_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate Img{0} in Gn{1}'.format(Img2proc_mtlb,GnToUse),'blue')
    APy3_GENfuns.printcol('using LatOvflw params for Gn{0}'.format(GnParamToUse),'blue')
    #
    if (GnParamToUse==0)&(CDSFlag): APy3_GENfuns.printcol('  will use CDS for Gn0','blue')
    if (GnParamToUse==0)&(CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol{0}'.format(cols2CMA_mtlb),'blue')
    #
    if (showFlag & (~saveFlag)): APy3_GENfuns.printcol('will show plots','blue')
    elif (showFlag & (saveFlag)): APy3_GENfuns.printcol('will save plots to {0}'.format(saveFolder),'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#%% load file
if verboseFlag: APy3_GENfuns.printcol('load DLSraw-file and ADUcorr-files','blue')
if APy3_GENfuns.notFound(ADUcorr_file): APy3_GENfuns.printErr('not found: '+ADUcorr_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
 ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
if APy3_GENfuns.notFound(folder_data2process+infile): APy3_GENfuns.printErr('not found: '+folder_data2process+infile)
(drkSmpl_DLSraw,drkRst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+infile, '/data','/reset', fromImg,toImg)
#---
#%% DLSraw => Gn,Crs,Fn
if verboseFlag: APy3_GENfuns.printcol('DLSraw => Gn,Crs,Fn','blue')
if highMemFlag: drk_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(drkSmpl_DLSraw,drkRst_DLSraw, ERRDLSraw, ERRint16)
else:
    drk_GnCrsFn= numpy.zeros((len(Img2proc),NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
    for thisImg in range(len(Img2proc)):
        thisSmpl_DLSraw= drkSmpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
        thisRst_DLSraw=  drkRst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
        this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
        drk_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
        if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,len(Img2proc))
    if cleanMemFlag: del thisSmpl_DLSraw; del thisRst_DLSraw; del this_dscrmbld_GnCrsFn
#---
#%% ADUcorr, CMA,CDS,avg
if verboseFlag: APy3_GENfuns.printcol('ADU-correct','blue')
drkADU= APy3_GENfuns.numpy_NaNs((len(Img2proc),NSmplRst, NRow,NCol))
drkADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(drk_GnCrsFn[:,iSmpl,:,:,iCrs],drk_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
drkADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_NoGain(drk_GnCrsFn[:,iRst,:,:,iCrs], drk_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
#
mode_str=""
if CMAFlag:
    if verboseFlag: APy3_GENfuns.printcol('CMA-ing','blue')
    drkADU[:,iSmpl,:,:]= APy3_P2Mfuns.CMA(drkADU[:,iSmpl,:,:] ,cols2CMA)
    drkADU[:,iRst,:,:]=  APy3_P2Mfuns.CMA(drkADU[:,iRst,:,:]  ,cols2CMA)
    mode_str+="CMA,"
    PedestalADU_multiGn[GnToUse,:,:]= APy3_P2Mfuns.CMA(PedestalADU_multiGn[GnToUse,:,:].reshape((1,NRow,NCol))  ,cols2CMA).reshape((NRow,NCol))
#
# set to NaN what it is Smpl and not GnToUse
map_notThatGn_Smpl= drk_GnCrsFn[:,iSmpl,:,:,iGn] != GnToUse
drkADU[:,iSmpl,:,:][map_notThatGn_Smpl]= numpy.NaN
if cleanMemFlag: del drk_GnCrsFn
#
if CDSFlag: 
    if verboseFlag: APy3_GENfuns.printcol('CDS std-ing','blue')
    stdThatGn_ADU= numpy.nanstd(APy3_P2Mfuns.CDS(drkADU),axis=0)
    vals2avg= numpy.count_nonzero(~numpy.isnan(APy3_P2Mfuns.CDS(drkADU)),axis=0) # note this is not vals2avg, but rather vaild (non-NaN) samples to std
    drkThatGn_e= (APy3_P2Mfuns.CDS(drkADU) - PedestalADU_multiGn[GnParamToUse,:,:])*e_per_ADU_multiGn[GnParamToUse,:,:]
    mode_str+='CDS'
else: 
    if verboseFlag: APy3_GENfuns.printcol('Smpl std-ing','blue')
    stdThatGn_ADU= numpy.nanstd(drkADU[:,iSmpl,:,:],axis=0)
    vals2avg= numpy.count_nonzero(~numpy.isnan(drkADU[:,iSmpl,:,:]),axis=0) # note this is not vals2avg, but rather vaild (non-NaN) samples to std
    drkThatGn_e= (drkADU[:,iSmpl,:,:] - PedestalADU_multiGn[GnParamToUse,:,:])*e_per_ADU_multiGn[GnParamToUse,:,:]
    mode_str+='Smpl'
stdThatGn_e= stdThatGn_ADU*e_per_ADU_multiGn[GnParamToUse,:,:]
#---
#%% interactive show
APy3_GENfuns.printcol("interactive plotting", 'blue')
thisRow=280;thisCol=320;this_histobins=15; ROIrows_str=":"; ROIcols_str=":"; atleastNImg=len(Img2proc)/2; badPixNoiseThres=350.0 # init

APy3_GENfuns.printcol("plot [N]oise maps / marking [B]ad pixels / plot [F]ingerplot / [E]nd plotting", 'black')


nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['n','N']:
        this_histobins=100 #default
        APy3_GENfuns.printcol("plotting noise maps", 'blue')
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having atr least {1} valid images".format(ROIstring,atleastNImg), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #

        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnParamToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        if showFlag:
            if saveFlag:
                auxTitle="std {0} (Gn{1}) [e]".format(mode_str,GnToUse)
                png_2D_all(stdThatGn_e_2show, False, 'col','row',"std {0} (Gn{1}) [e]".format(mode_str,GnToUse), True, saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
                auxTitle="number of Gn{0}-images for noise estimation".format(GnToUse)
                png_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True, saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
                #
                stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
                stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
                auxTitle="noise {0} {1}".format(mode_str,ROIstring)
                png_histo1D(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring), saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
            else:
                APy3_GENfuns.plot_2D_all(stdThatGn_e_2show, False, 'col','row',"std {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
                APy3_GENfuns.plot_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True)
                #
                stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
                stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
                APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring))
                matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
    if nextstep in ['b','B']:
        this_histobins=100 #default
        APy3_GENfuns.printcol("plotting noise maps, marking bad pixels", 'blue')
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("marking as bad pixels the ones having a noise above [default is {0}]".format(badPixNoiseThres), 'black'); badPixNoiseThres_in= input(); 
        if (len(badPixNoiseThres_in)>0): badPixNoiseThres= float(badPixNoiseThres_in) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having at least {1} valid images, flagging as bad pixels the ones with noise above {0}e".format(ROIstring,atleastNImg,badPixNoiseThres), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #
        # show bad pixels
        badPixMap= stdThatGn_e_2show>badPixNoiseThres
        APy3_GENfuns.printcol("{0} pixels have a noise exceeding {1}e".format(numpy.sum(badPixMap),badPixNoiseThres), 'green')
        badPixNoiseMap_2show= numpy.copy(stdThatGn_e_2show)
        badPixNoiseMap_2show[~badPixMap]= numpy.NaN
        APy3_GENfuns.plot_2D_all(badPixNoiseMap_2show, False, 'col','row',"noise of bad pixels in {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
        #
        badPix_RowList,badPix_ColList=numpy.where(badPixMap)
        for iPix,thisRow in enumerate(badPix_RowList):
            thisRow= badPix_RowList[iPix]; thisCol= badPix_ColList[iPix]
            APy3_GENfuns.printcol("bad pix ({0},{1}): noise {2}e".format(thisRow,thisCol,stdThatGn_e_2show[thisRow,thisCol]), 'green')
        #
        # remove bad pixels
        stdThatGn_e_2show[badPixMap]= numpy.NaN
        #
        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnParamToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        #
        APy3_GENfuns.plot_2D_all(stdThatGn_e_2show, False, 'col','row',"noise {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
        APy3_GENfuns.plot_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True)
        #
        stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
        APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} (Gn{1}) {2}".format(mode_str,GnToUse,ROIstring))
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
    #
    elif nextstep in ['f','F',]:
        this_histobins=15 #default
        APy3_GENfuns.printcol("fingerplot spectrum:", 'black')
        APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("plotting fingerplot spectrum of pix ({0},{1}), {2} bins".format(thisRow,thisCol,this_histobins), 'blue')
        #
        if ( numpy.isnan(stdThatGn_e[thisRow,thisCol]) ) : 
            APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            APy3_GENfuns.printcol("noise {0} for pix({1},{2})= {3}e, evaluated on {4} samples".format(mode_str,thisRow,thisCol,stdThatGn_e[thisRow,thisCol],vals2avg[thisRow,thisCol]), 'green')
            #
            drkThatGnThatPix_2histo= numpy.copy(drkThatGn_e[:,thisRow,thisCol])
            drkThatGnThatPix_2histo= drkThatGnThatPix_2histo[~numpy.isnan(drkThatGnThatPix_2histo)]
            APy3_GENfuns.plot_histo1d(drkThatGnThatPix_2histo, this_histobins, False, "pixel output [e]","occurrences","pix({0},{1}), {2}".format(thisRow,thisCol,mode_str))
            matplotlib.pyplot.show(block=True)    
    #
    elif nextstep in ['a','A']:
        APy3_GENfuns.printcol("Easter egg: A to check Noise by ADC", 'black')
        this_histobins=100 #default
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if fromRow%7!=0: fromRow= (fromRow//7)*7
        if toRow%7!=6:   toRow=   ( (fromRow//7)*7 )+6
        ROIrows= numpy.arange(fromRow,toRow+1)
        #
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having atr least {1} valid images".format(ROIstring,atleastNImg), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #
        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
        APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring))
        #
        stdThatGn_e_2show_xADC= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].reshape((len(ROIrows)//7,7,len(ROIcols)))
        fig = matplotlib.pyplot.figure()
        for iADC in range(7):
            thisADCvals= stdThatGn_e_2show_xADC[:,iADC,:].flatten()
            thisADCvals= thisADCvals[~numpy.isnan(thisADCvals)]
            if len(thisADCvals)>0: 
                matplotlib.pyplot.hist(thisADCvals, 100, alpha=0.5, label='rows 7i + {0}'.format(iADC));
                APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}, rows 7i+{3} = {4}e +/- {5}e".format(mode_str, ROIstring, GnParamToUse, iADC, numpy.nanmean(thisADCvals), numpy.nanstd(thisADCvals)), 'green')
            del thisADCvals
        matplotlib.pyplot.legend(loc='upper right'); 
        matplotlib.pyplot.xlabel("noise {0} [e]".format(mode_str)); 
        matplotlib.pyplot.ylabel("pixels"); 
        matplotlib.pyplot.title("noise {0} {1}".format(mode_str,ROIstring))
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:", 'black')
        APy3_GENfuns.printcol("A to check Noise by ADC", 'black')
    #
    APy3_GENfuns.printcol("plot [N]oise maps / marking [B]ad pixels / plot [F]ingerplot / [E]nd plotting", 'black')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
#---
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')



