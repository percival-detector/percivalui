# -*- coding: utf-8 -*-
"""
load avg , pedestal => airy
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./UseSpecAvg_2Airy_3.py
or
python3
exec(open("./UseSpecAvg_2Airy_3.py").read())
"""
#%% imports and useful constants
from APy3_auxINIT import *
pixPitch= 27e-6
# ---
#
def AiryDiskProfile_plusC_fun(X, Energy_eV, pin_diam,pin_Dist, J0, Const):
    '''Airy Disk profile + constant'''
    Y= APy3_FITfuns.AiryDiskProfile_fun(X, Energy_eV, pin_diam,pin_Dist, J0)+ Const
    return Y+ Const

def AiryDiskProfile_plusC_fit(X,Y, Energy_eV, pin_diam, pin_Dist, J0_hint, Const_hint):
    '''fit Airy + constant (fit only J0,Const)'''
    p0= [J0_hint, Const_hint] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(lambda X,J0_hint,Const_hint: AiryDiskProfile_plusC_fun(X, Energy_eV, pin_diam,pin_Dist, J0_hint, Const_hint), X, Y, p0=p0)
    J0_fit= coeff[0]
    Const_fit= coeff[1]
    return (Energy_eV, pin_diam,pin_Dist, J0_fit, Const_fit)

def AiryDiskProfile_plusC_pindiam_fit(X,Y, Energy_eV, pin_diam_hint, pin_Dist, J0_hint, Const_hint):
    '''fit Airy + constant (fit only pin_diam,J0,Const)'''
    p0= [pin_diam_hint, J0_hint, Const_hint] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(lambda X, pin_diam_hint,J0_hint,Const_hint: AiryDiskProfile_plusC_fun(X, Energy_eV, pin_diam_hint,pin_Dist, J0_hint, Const_hint), X, Y, p0=p0)
    pin_diam_fit= coeff[0]
    J0_fit= coeff[1]
    Const_fit= coeff[2]
    return (Energy_eV, pin_diam_fit,pin_Dist, J0_fit, Const_fit)

def AiryDiskProfile_2harm_plusC_fun(X, Energy_eV, pin_diam,pin_Dist, J0_1stHarm, J0_2ndHarm, C0):
    '''Airy Disk profile + constant'''
    Y= APy3_FITfuns.AiryDiskProfile_fun(X, Energy_eV, pin_diam,pin_Dist, J0_1stHarm)+ APy3_FITfuns.AiryDiskProfile_fun(X, 2*Energy_eV, pin_diam,pin_Dist, J0_2ndHarm)+ C0
    return Y+ C0

def AiryDiskProfile_2harm_plusC_fit(X,Y, Energy_eV, pin_diam ,pin_Dist, J0_1stHarm_hint,J0_2ndHarm_hint, C0_hint):
    '''fit Airy(1st_harm) + Airy(2nd_harm) + constant (fit only J0_1stHarm,J0_2ndHarm,C0)'''
    p0= [J0_1stHarm_hint,J0_2ndHarm_hint, C0_hint] # initial guess for the fitting coefficients
    coeff, var_matrix = curve_fit(lambda X,J0_1stHarm_hint,J0_2ndHarm_hint,C0_hint: AiryDiskProfile_2harm_plusC_fun(X, Energy_eV, pin_diam ,pin_Dist, J0_1stHarm_hint,J0_2ndHarm_hint, C0_hint), X, Y, p0=p0)
    J0_1stHarm_fit= coeff[0]
    J0_2ndHarm_fit= coeff[1]
    C0_fit= coeff[2]
    return (Energy_eV, pin_diam ,pin_Dist, J0_1stHarm_fit, J0_2ndHarm_fit, C0_fit)
#
def plot_1D_data_nd_Airy_2(arrayX,arrayY,logFlag,
                 pix0,pixPitch,
                 Energy_eV, pin_diam,pin_Dist,J0,upLim,
                 label_x,label_y,label_title):
    fig = matplotlib.pyplot.figure()
    if logFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    aux_map= arrayY<=upLim
    matplotlib.pyplot.plot(arrayX[aux_map], arrayY[aux_map], 'o', label='measured data')
    #
    #matplotlib.pyplot.gca().set_ylim(top=upLim)
    matplotlib.pyplot.ylim(ymax=upLim)
    #
    arrayAX_SI= (arrayX-pix0)*pixPitch
    arrayAY= APy3_FITfuns.AiryDiskProfile_fun(arrayAX_SI, Energy_eV, pin_diam,pin_Dist, J0)
    matplotlib.pyplot.plot(arrayX, arrayAY, '-', label='expected diffraction\n({0}eV photons, {1}um pinhole)'.format(Energy_eV, pin_diam/(1e-6)))
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.show(block=False)
    return (fig)





#
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#%% Flags
#---
#
#%% data from here

'''
####################################### BSI04, 3TGn0 PGA666 T-20 250eV, 12ms, 5um pinhole ################################################################
dflt_inFileADU_Gn0="/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/airy_7of7ADC_3TPGA666/avg_xGn/"+"2019.12.11.23.37.16_BSI04_7of7_3TPGA666_012ms_0250eV_5um_1kpin_Gn0_CDS_avg.h5" # fixed Gn=0
dflt_inFileADU_Gn1="none" # fixed Gn=0
dflt_inFileADU_Gn2="none" # fixed Gn=0
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
dflt_alternFile_Ped_Gn0_ADU= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/airy_7of7ADC_3TPGA666/avg_xGn/"+"2019.12.11.23.36.48_BSI04_7of7_3TPGA666_012ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5" 
#
dflt_phEnergy_eV= 250 # eV
dflt_thisRow= 678; dflt_thisCol= 545; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 17000; dflt_C0=0; dflt_upLim= 4000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#
'''
####################################### BSI04, 3G PGABBB T-20 250eV, 120ms , 5um pinhole ################################################################
dflt_inFileADU_Gn0="/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/../avg_xGn/2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1="/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/../avg_xGn/2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2="/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/../avg_xGn/2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
dflt_alternFile_Ped_Gn0_ADU= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/DLSraw/../avg_xGn/2019.12.11.23.57.21_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5" 
#
dflt_phEnergy_eV= 250 # eV
dflt_thisRow= 678; dflt_thisCol= 545; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 140000; dflt_C0=0; dflt_upLim= 400000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#
'''
####################################### BSI04, 3G PGABBB T-20 250eV, 240ms , 5um pinhole ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.23.21.44_5um_250eV/LatOvflw_7of7ADC_3GPGABBB/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.12.00.08.43_BSI04_7of7_3GPGABBB_240ms_0250eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= dflt_dataFolder+"2019.12.12.00.08.43_BSI04_7of7_3GPGABBB_240ms_0250eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2= dflt_dataFolder+"2019.12.12.00.08.43_BSI04_7of7_3GPGABBB_240ms_0250eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.12.00.13.53_BSI04_7of7_3GPGABBB_240ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_phEnergy_eV= 250 # eV
dflt_thisRow= 678; dflt_thisCol= 545; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 250000; dflt_C0=0; dflt_upLim= 800000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#
#
'''
####################################### BSI04, 3T PGA666 T-20 399eV, 120ms lower flux ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/airy_7of7ADC_3TPGA666/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.11.21.54.27_BSI04_7of7_3TPGA666_120ms_0399eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= "none"
dflt_inFileADU_Gn2= "none"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.11.21.52.05_BSI04_7of7_3TPGA666_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_03_PGA666_2019.12.06_Gn0xx_MultiGnCal.h5'
dflt_phEnergy_eV= 399 # eV
dflt_thisRow= 675; dflt_thisCol= 549; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 3390; dflt_C0=0; dflt_upLim= 800000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#

'''
####################################### BSI04, 3G PGABBB T-20 399eV, 120ms lower flux, 5um pinhole  ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/LatOvlw_7of7ADC_3GPGABBB_lowerFlux/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.11.22.39.57_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= dflt_dataFolder+"2019.12.11.22.39.57_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2= dflt_dataFolder+"2019.12.11.22.39.57_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.11.22.37.22_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_phEnergy_eV= 399 # eV
dflt_thisRow= 675; dflt_thisCol= 549; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 270000; dflt_C0=0; dflt_upLim= 800000.0
flt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
#'''
#
#'''
####################################### BSI04, 3G PGABBB T-20 399eV, 120ms higher flux, 5um pinhole  ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.11.21.23_5um_0399eV/LatOvlw_7of7ADC_3GPGABBB_higherFlux/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.11.22.56.58_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= dflt_dataFolder+"2019.12.11.22.56.58_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2= dflt_dataFolder+"2019.12.11.22.56.58_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.11.22.54.45_BSI04_7of7_3GPGABBB_120ms_0399eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_phEnergy_eV= 399 # eV
dflt_thisRow= 675; dflt_thisCol= 549; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 270000; dflt_C0=0; dflt_upLim= 800000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
#'''
#

#
'''
####################################### BSI04, 3G PGABBB T-20 710eV, 240ms  ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.00.44.04_BSI04_5um_0710eV/LatOvflw_7of7ADC_3GPGABBB/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.12.01.20.30_BSI04_7of7_3GPGABBB_240ms_0710eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= dflt_dataFolder+"2019.12.12.01.20.30_BSI04_7of7_3GPGABBB_240ms_0710eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2= dflt_dataFolder+"2019.12.12.01.20.30_BSI04_7of7_3GPGABBB_240ms_0710eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.12.01.24.39_BSI04_7of7_3GPGABBB_240ms_0710eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_phEnergy_eV= 710 # eV
dflt_thisRow= 675; dflt_thisCol= 549; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 135000; dflt_C0=0; dflt_upLim= 800000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#
'''
####################################### BSI04, 3G PGABBB T-20 1000eV, 120ms  ################################################################
dflt_dataFolder= "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.01.48.02_BSI04_5um_1000eV/LatOvflw_7of7ADC_3TPGABBB/avg_xGn/"
dflt_inFileADU_Gn0= dflt_dataFolder+"2019.12.12.02.21.34_BSI04_7of7_3GPGABBB_120ms_1000eV_5um_1kpin_Gn0_CDS_avg.h5"
dflt_inFileADU_Gn1= dflt_dataFolder+"2019.12.12.02.21.34_BSI04_7of7_3GPGABBB_120ms_1000eV_5um_1kpin_Gn1_CDS_avg.h5"
dflt_inFileADU_Gn2= dflt_dataFolder+"2019.12.12.02.21.34_BSI04_7of7_3GPGABBB_120ms_1000eV_5um_1kpin_Gn2_CDS_avg.h5"
dflt_alternFile_Ped_Gn0_ADU= dflt_dataFolder+"2019.12.12.02.28.07_BSI04_7of7_3GPGABBB_120ms_1000eV_5um_1kdrk_Gn0_CDS_avg.h5" 
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
dflt_phEnergy_eV= 1000 # eV
dflt_thisRow= 672; dflt_thisCol= 549; dflt_ROICol_str='200:1200'; dflt_ROIRow_str='200:1200'
dflt_J0= 185000; dflt_C0=0; dflt_upLim= 800000.0
dflt_pin_Dist= 2.155; dflt_pin_diam= 5.5e-6 
'''
#
#
#
dflt_CMAFlag= False
dflt_cols2CMA = '32:63'
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['Gn0 avg [ADU] data [none not to use it]'] 
GUIwin_arguments+= [dflt_inFileADU_Gn0] 
GUIwin_arguments+= ['Gn1 avg [ADU] data [none not to use it]'] 
GUIwin_arguments+= [dflt_inFileADU_Gn1] 
GUIwin_arguments+= ['Gn2 avg [ADU] data [none not to use it]'] 
GUIwin_arguments+= [dflt_inFileADU_Gn2] 
#
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['alternative PedestalADU [Gn0] file [none not to use it]'] 
GUIwin_arguments+= [dflt_alternFile_Ped_Gn0_ADU]
#
GUIwin_arguments+= ['CMA? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CMAFlag)]
GUIwin_arguments+= ['if CMA: Reference Columns? [first:last]'] 
GUIwin_arguments+= [dflt_cols2CMA]
#
GUIwin_arguments+= ['photon energy [eV]'] 
GUIwin_arguments+= [str(dflt_phEnergy_eV)]
GUIwin_arguments+= ['Airy fit: pinhole diameter [m]'] 
GUIwin_arguments+= [str(dflt_pin_diam)]
GUIwin_arguments+= ['Airy fit: pinhole distance [m]'] 
GUIwin_arguments+= [str(dflt_pin_Dist)]
#
GUIwin_arguments+= ['Airy fit: ROI Rows [first:last]'] 
GUIwin_arguments+= [dflt_ROIRow_str]
GUIwin_arguments+= ['Airy fit: ROI Col [first:last]'] 
GUIwin_arguments+= [dflt_ROICol_str]
GUIwin_arguments+= ['Airy fit: peak position [Row]'] 
GUIwin_arguments+= [str(dflt_thisRow)]
GUIwin_arguments+= ['Airy fit: peak position [Col]'] 
GUIwin_arguments+= [str(dflt_thisCol)]
GUIwin_arguments+= ['Airy fit: peak level [e]'] 
GUIwin_arguments+= [str(dflt_J0)]
GUIwin_arguments+= ['Airy fit: constant base level [e]'] 
GUIwin_arguments+= [str(dflt_C0)]
GUIwin_arguments+= ['Airy fit: ignore values above [e]'] 
GUIwin_arguments+= [str(dflt_upLim)]
#
#
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
i_param=0
#
flagUseGn= numpy.zeros(3).astype(bool)

#
inFileADU_Gn=[]
inFileADU_Gn+= [dataFromUser[i_param]]; i_param+=1
inFileADU_Gn+= [dataFromUser[i_param]]; i_param+=1
inFileADU_Gn+= [dataFromUser[i_param]]; i_param+=1
#
for thisGn in range(3):
    if inFileADU_Gn[thisGn] in ['','none','None','NONE','no','No','NO']: flagUseGn[thisGn]= False
    else: flagUseGn[thisGn]= True
if numpy.sum(flagUseGn)<1:APy3_GENfuns.printErr('there should be at least 1 avg')
# 
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
alternFile_Ped_Gn0_ADU= dataFromUser[i_param]; i_param+=1; 
if alternFile_Ped_Gn0_ADU in ['','none','None','NONE','no','No','NO']: flagUseAlternPed=False
else: flagUseAlternPed=True
#
CMAFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cols2CMA_mtlb= dataFromUser[i_param]; i_param+=1
cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
#
Energy_eV=float(dataFromUser[i_param]); i_param+=1
pin_diam=float(dataFromUser[i_param]); i_param+=1
pin_Dist=float(dataFromUser[i_param]); i_param+=1
#
ROIRow_str= dataFromUser[i_param]; i_param+=1
if ROIRow_str in [':','*','all','All','ALL']: ROIRow= numpy.arange(NRow)
else: ROIRow=APy3_GENfuns.matlabLike_range(ROIRow_str)
Row_1st=ROIRow[0]; Row_last=ROIRow[-1];
#
ROICol_str= dataFromUser[i_param]; i_param+=1
if ROICol_str in [':','*','all','All','ALL']: ROICol= numpy.arange(NCol)
else: ROICol=APy3_GENfuns.matlabLike_range(ROICol_str)
Col_1st=ROICol[0];Col_last=ROICol[-1];
#
thisRow= int(dataFromUser[i_param]); i_param+=1
thisCol= int(dataFromUser[i_param]); i_param+=1
J0= float(dataFromUser[i_param]); i_param+=1
C0= float(dataFromUser[i_param]); i_param+=1
upLim= float(dataFromUser[i_param]); i_param+=1
#---
#
#%% what's up doc
for thisGn in range(3):
    if flagUseGn[thisGn]: APy3_GENfuns.printcol('will use Gn{0} avg [ADU] file: {1}'.format(thisGn,inFileADU_Gn[thisGn]),'blue')
APy3_GENfuns.printcol('will take multiGnCal_file from {0}'.format(multiGnCal_file),'blue')
if flagUseAlternPed: APy3_GENfuns.printcol('will take Gn0 Pedestal from {0}'.format(alternFile_Ped_Gn0_ADU),'blue')
else: APy3_GENfuns.printcol('will use Gn0 pedestal from multiGnCal_file','blue')
#
if (CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol{0}'.format(cols2CMA_mtlb),'blue')
APy3_GENfuns.printcol('will consider {0}eV photons, pinhole of {1}m diameter at {2}m distance'.format(Energy_eV,pin_diam,pin_Dist),'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
#
startTime=time.time()
APy3_GENfuns.printcol("script starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
#
#%% load files
APy3_GENfuns.printcol('load files','blue')
inDataADU_Gn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))
inDataAltPedGn0= APy3_GENfuns.numpy_NaNs((NRow,NCol))
#
for thisGn in range(3):
    if flagUseGn[thisGn]: 
        if APy3_GENfuns.notFound(inFileADU_Gn[thisGn]): APy3_GENfuns.printErr('not found: '+inFileADU_Gn[thisGn])
        inDataADU_Gn[thisGn,:,:]= APy3_GENfuns.read_1xh5(inFileADU_Gn[thisGn], '/data/data')
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
#
if flagUseAlternPed:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn0_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn0_ADU)
    inDataAltPedGn0= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn0_ADU, '/data/data')
# ---
if CMAFlag:
    APy3_GENfuns.printcol('CMA','blue')
    inDataADU_Gn= APy3_P2Mfuns.CMA(inDataADU_Gn,cols2CMA)
    PedestalADU_multiGn= APy3_P2Mfuns.CMA(PedestalADU_multiGn,cols2CMA)
    inDataAltPedGn0= APy3_P2Mfuns.CMA(inDataAltPedGn0.reshape((1,NRow,NCol)),cols2CMA).reshape((NRow,NCol))

#---
#%% data in electrons
outData_e_Gn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))
totData_e= numpy.zeros((NRow,NCol))
totData_e[:,0:32]=numpy.NaN
#
for thisGn in range(3):
    if flagUseGn[thisGn]:
        if ((thisGn==0) & (flagUseAlternPed)): 
            outData_e_Gn[thisGn,:,:]=inDataADU_Gn[thisGn,:,:]-inDataAltPedGn0
        else: 
            outData_e_Gn[thisGn,:,:]=inDataADU_Gn[thisGn,:,:]-PedestalADU_multiGn[thisGn,:,:]
        #
        outData_e_Gn[thisGn,:,:]=outData_e_Gn[thisGn,:,:]*e_per_ADU_multiGn[thisGn,:,:]
        #
        aux_goodmap= ~numpy.isnan(outData_e_Gn[thisGn,:,:])
        #totData_e[aux_goodmap]= totData_e[aux_goodmap]+outData_e_Gn[thisGn,:,:][aux_goodmap]
        totData_e[aux_goodmap]= outData_e_Gn[thisGn,:,:][aux_goodmap]
#
inData=numpy.copy(totData_e)
#
# ---
#%% interactive show
APy3_GENfuns.printcol("interactive plotting", 'blue')
#
APy3_GENfuns.printcol("plot avg [C]DS / [A]iry along a cut / [E]nd plotting", 'black')
nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['c','C',' ']:
        APy3_GENfuns.printcol("plotting avg CDS", 'blue')
        APy3_GENfuns.plot_2D_all(inData,False,'col','row','avg [e]', True)
        APy3_GENfuns.plot_2D_all(inData,True,'col','row','avg [e]', True)
        APy3_GENfuns.showIt()
    elif nextstep in ['a','A']:
        APy3_GENfuns.printcol("Airy show:", 'black')
        APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("Energy? [eV] [default is {0}]".format(Energy_eV), 'black'); Energy_eV_str= input(); 
        if APy3_GENfuns.isitfloat(Energy_eV_str): Energy_eV= float(Energy_eV_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("pinhole diameter? [m] [default is {0}]".format(pin_diam), 'black'); pin_diam_str= input(); 
        if APy3_GENfuns.isitfloat(pin_diam_str): pin_diam= float(pin_diam_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("pinhole distance from detector? [m] [default is {0}]".format(pin_Dist), 'black'); pin_Dist_str= input(); 
        if APy3_GENfuns.isitfloat(pin_Dist_str): pin_Dist= float(pin_Dist_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("J0 (max of Airy main peak) [default is {0}]".format(J0), 'black'); J0_str= input(); 
        if APy3_GENfuns.isitfloat(J0_str): J0= float(J0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("plotting for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5}".format(thisRow,thisCol,Energy_eV,pin_diam,pin_Dist,J0), 'blue')
        #
        plot_1D_data_nd_Airy_2(ROICol, inData[thisRow,ROICol[0]:ROICol[-1]+1],True,
                 thisCol,pixPitch,
                 Energy_eV, pin_diam,pin_Dist,J0,upLim,
                 'cols','e','{0}eV, {1}um pinhole (Row={2})'.format(Energy_eV,pin_diam*(1e6),thisRow))
        plot_1D_data_nd_Airy_2(ROIRow, inData[ROIRow[0]:ROIRow[-1]+1,thisCol],True,
                 thisRow,pixPitch,
                 Energy_eV, pin_diam,pin_Dist,J0,upLim,
                 'rows','e','{0}eV, {1}um pinhole (Col={2})'.format(Energy_eV,pin_diam*(1e6),thisCol))
        APy3_GENfuns.showIt()
    #
    elif nextstep in ['1']:
        APy3_GENfuns.printcol("Easter Egg! Airy + constant fit:", 'black')
        #
        APy3_GENfuns.printcol("peak in which Row? [default={0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("peak in which Col? [default={0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("Energy? [eV] [default={0}]".format(Energy_eV), 'black'); Energy_eV_str= input(); 
        if APy3_GENfuns.isitfloat(Energy_eV_str): Energy_eV= float(Energy_eV_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("pinhole diameter? [m] [default={0}]".format(pin_diam), 'black'); pin_diam_str= input(); 
        if APy3_GENfuns.isitfloat(pin_diam_str): pin_diam= float(pin_diam_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("pinhole distance from detector? [m] [default={0}]".format(pin_Dist), 'black'); pin_Dist_str= input(); 
        if APy3_GENfuns.isitfloat(pin_Dist_str): pin_Dist= float(pin_Dist_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("J0 (max of Airy main peak) estimation? [default={0}]".format(J0), 'black'); J0_str= input(); 
        if APy3_GENfuns.isitfloat(J0_str): J0= float(J0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("C0 (constant) estimation? [default={0}]".format(C0), 'black'); C0_str= input(); 
        if APy3_GENfuns.isitfloat(C0_str): C0= float(C0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("ignore data above? (to avoid saturation) [default={0}]".format(upLim), 'black'); upLim_str= input(); 
        if APy3_GENfuns.isitfloat(upLim_str): upLim= float(upLim_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("which Col Range for a cutline along a Row? [first:last] [default={0}]".format(ROICol_str), 'black'); ROICol_str_justRead= input(); 
        if len(ROICol_str_justRead)>2: ROICol_str=ROICol_str_justRead  # otherwise keeps the old value
        ROICol= APy3_GENfuns.matlabLike_range(ROICol_str); Col_1st=ROICol[0];Col_last=ROICol[-1];
        #
        APy3_GENfuns.printcol("which Row Range for a cutline along a Col? [first:last] [default={0}]".format(ROIRow_str), 'black'); ROIRow_str_justRead= input(); 
        if len(ROIRow_str_justRead)>2: ROIRow_str=ROIRow_str_justRead  # otherwise keeps the old value
        ROIRow= APy3_GENfuns.matlabLike_range(ROIRow_str); Row_1st=ROIRow[0];Row_last=ROIRow[-1];
        #
        X2fit=numpy.arange(Col_1st,Col_last+1)
        Y2fit=numpy.copy(inData[thisRow, Col_1st:Col_last+1])
        Y2fit[Y2fit>upLim]=numpy.NaN
        X2fit= X2fit[~numpy.isnan(Y2fit)]
        Y2fit= Y2fit[~numpy.isnan(Y2fit)]
        (Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit)= AiryDiskProfile_plusC_fit((X2fit-thisCol)*pixPitch,Y2fit, Energy_eV, pin_diam,pin_Dist, J0,C0)
        APy3_GENfuns.printcol("plotting cutline along a Row for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5}, C0={6}, limited to {7} to avoid saturation".format(thisRow,thisCol,Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit,upLim), 'blue')
        APy3_GENfuns.plot_1D(X2fit, Y2fit, 'cols','e','{0}eV, {1}um pinhole (Row={2})'.format(Energy_eV,round(pin_diam*(1e6),2),thisRow))
        Xfitted= numpy.arange(min(X2fit),max(X2fit),0.1)
        Yfitted= AiryDiskProfile_plusC_fun((Xfitted-thisCol)*pixPitch, Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit)
        matplotlib.pyplot.plot(Xfitted, Yfitted, '-')
        #
        X2fit=numpy.arange(Row_1st,Row_last+1)
        Y2fit=numpy.copy(inData[Row_1st:Row_last+1, thisCol])
        Y2fit[Y2fit>upLim]=numpy.NaN
        X2fit= X2fit[~numpy.isnan(Y2fit)]
        Y2fit= Y2fit[~numpy.isnan(Y2fit)]
        (Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit)= AiryDiskProfile_plusC_fit((X2fit-thisRow)*pixPitch,Y2fit, Energy_eV, pin_diam,pin_Dist, J0,C0)
        APy3_GENfuns.printcol("plotting cutline along a Col for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5}, C0={6}, limited to {7} to avoid saturation".format(thisRow,thisCol,Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit,upLim), 'blue')
        APy3_GENfuns.plot_1D(X2fit, Y2fit, 'rows','e','{0}eV, {1}um pinhole (Col={2})'.format(Energy_eV,round(pin_diam*(1e6),2),thisCol))
        Xfitted= numpy.arange(min(X2fit),max(X2fit),0.1)
        Yfitted= AiryDiskProfile_plusC_fun((Xfitted-thisRow)*pixPitch, Energy_eV,pin_diam,pin_Dist,J0_fit,C0_fit)
        matplotlib.pyplot.plot(Xfitted, Yfitted, '-')
        matplotlib.pyplot.show(block=True)
    #
    elif nextstep in ['d']:
        APy3_GENfuns.printcol("Easter Egg! Airy + constant & pinhole diameter fit:", 'black')
        #
        APy3_GENfuns.printcol("peak in which Row? [default={0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("peak in which Col? [default={0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("Energy? [eV] [default={0}]".format(Energy_eV), 'black'); Energy_eV_str= input(); 
        if APy3_GENfuns.isitfloat(Energy_eV_str): Energy_eV= float(Energy_eV_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("pinhole diameter estimation? [m] [default={0}]".format(pin_diam), 'black'); pin_diam_str= input(); 
        if APy3_GENfuns.isitfloat(pin_diam_str): pin_diam= float(pin_diam_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("pinhole distance from detector? [m] [default={0}]".format(pin_Dist), 'black'); pin_Dist_str= input(); 
        if APy3_GENfuns.isitfloat(pin_Dist_str): pin_Dist= float(pin_Dist_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("J0 (max of Airy main peak) estimation? [default={0}]".format(J0), 'black'); J0_str= input(); 
        if APy3_GENfuns.isitfloat(J0_str): J0= float(J0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("C0 (constant) estimation? [default={0}]".format(C0), 'black'); C0_str= input(); 
        if APy3_GENfuns.isitfloat(C0_str): C0= float(C0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("ignore data above? (to avoid saturation) [default={0}]".format(upLim), 'black'); upLim_str= input(); 
        if APy3_GENfuns.isitfloat(upLim_str): upLim= float(upLim_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("which Col Range for a cutline along a Row? [first:last] [default={0}]".format(ROICol_str), 'black'); ROICol_str_justRead= input(); 
        if len(ROICol_str_justRead)>2: ROICol_str=ROICol_str_justRead  # otherwise keeps the old value
        ROICol= APy3_GENfuns.matlabLike_range(ROICol_str); Col_1st=ROICol[0];Col_last=ROICol[-1];
        #
        APy3_GENfuns.printcol("which Row Range for a cutline along a Col? [first:last] [default={0}]".format(ROIRow_str), 'black'); ROIRow_str_justRead= input(); 
        if len(ROIRow_str_justRead)>2: ROIRow_str=ROIRow_str_justRead  # otherwise keeps the old value
        ROIRow= APy3_GENfuns.matlabLike_range(ROIRow_str); Row_1st=ROIRow[0];Row_last=ROIRow[-1];
        #
        X2fit=numpy.arange(Col_1st,Col_last+1)
        Y2fit=numpy.copy(inData[thisRow, Col_1st:Col_last+1])
        Y2fit[Y2fit>upLim]=numpy.NaN
        X2fit= X2fit[~numpy.isnan(Y2fit)]
        Y2fit= Y2fit[~numpy.isnan(Y2fit)]
        (Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit)= AiryDiskProfile_plusC_pindiam_fit((X2fit-thisCol)*pixPitch,Y2fit, Energy_eV, pin_diam,pin_Dist, J0,C0)
        APy3_GENfuns.printcol("plotting cutline along a Row for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5}, C0={6}, limited to {7} to avoid saturation".format(thisRow,thisCol,Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit,upLim), 'blue')
        APy3_GENfuns.plot_1D(X2fit, Y2fit, 'cols','e','{0}eV, {1}um pinhole (Row={2})'.format(Energy_eV,round(pin_diam_fit*(1e6),2),thisRow))
        Xfitted= numpy.arange(min(X2fit),max(X2fit),0.1)
        Yfitted= AiryDiskProfile_plusC_fun((Xfitted-thisCol)*pixPitch, Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit)
        matplotlib.pyplot.plot(Xfitted, Yfitted, '-')
        #
        X2fit=numpy.arange(Row_1st,Row_last+1)
        Y2fit=numpy.copy(inData[Row_1st:Row_last+1, thisCol])
        Y2fit[Y2fit>upLim]=numpy.NaN
        X2fit= X2fit[~numpy.isnan(Y2fit)]
        Y2fit= Y2fit[~numpy.isnan(Y2fit)]
        (Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit)= AiryDiskProfile_plusC_pindiam_fit((X2fit-thisRow)*pixPitch,Y2fit, Energy_eV, pin_diam,pin_Dist, J0,C0)
        APy3_GENfuns.printcol("plotting cutline along a Col for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5}, C0={6}, limited to {7} to avoid saturation".format(thisRow,thisCol,Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit,upLim), 'blue')
        APy3_GENfuns.plot_1D(X2fit, Y2fit, 'rows','e','{0}eV, {1}um pinhole (Col={2})'.format(Energy_eV,round(pin_diam_fit*(1e6),2),thisCol))
        Xfitted= numpy.arange(min(X2fit),max(X2fit),0.1)
        Yfitted= AiryDiskProfile_plusC_fun((Xfitted-thisRow)*pixPitch, Energy_eV,pin_diam_fit,pin_Dist,J0_fit,C0_fit)
        matplotlib.pyplot.plot(Xfitted, Yfitted, '-')
        matplotlib.pyplot.show(block=True)
    #
    elif nextstep in ['2']:
        APy3_GENfuns.printcol("Easter Egg! 1st-harm-Airy + 2nd-harm-Airy + constant fit:", 'black')
        #
        APy3_GENfuns.printcol("peak in which Row? [default={0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("peak in which Col? [default={0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("Energy? (main harmonic) [eV] [default={0}]".format(Energy_eV), 'black'); Energy_eV_str= input(); 
        if APy3_GENfuns.isitfloat(Energy_eV_str): Energy_eV= float(Energy_eV_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("pinhole diameter? [m] [default={0}]".format(pin_diam), 'black'); pin_diam_str= input(); 
        if APy3_GENfuns.isitfloat(pin_diam_str): pin_diam= float(pin_diam_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("pinhole distance from detector? [m] [default={0}]".format(pin_Dist), 'black'); pin_Dist_str= input(); 
        if APy3_GENfuns.isitfloat(pin_Dist_str): pin_Dist= float(pin_Dist_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("J0 of main harm estimation? [default={0}]".format(J0), 'black'); J0_str= input(); 
        if APy3_GENfuns.isitfloat(J0_str): J0= float(J0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("J0 of 2nd harm estimation? [default={0}]".format(J2), 'black'); J2_str= input(); 
        if APy3_GENfuns.isitfloat(J2_str): J2= float(J2_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("C0 (constant) estimation? [default={0}]".format(C0), 'black'); C0_str= input(); 
        if APy3_GENfuns.isitfloat(C0_str): C0= float(C0_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("ignore data above? (to avoid saturation) [default={0}]".format(upLim), 'black'); upLim_str= input(); 
        if APy3_GENfuns.isitfloat(upLim_str): upLim= float(upLim_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("which Col Range for a cutline along a Row? [first:last] [default={0}]".format(ROICol_str), 'black'); ROICol_str_justRead= input(); 
        if len(ROICol_str_justRead)>2: ROICol_str=ROICol_str_justRead  # otherwise keeps the old value
        ROICol= APy3_GENfuns.matlabLike_range(ROICol_str); Col_1st=ROICol[0];Col_last=ROICol[-1];
        #
        APy3_GENfuns.printcol("which Row Range for a cutline along a Col? [first:last] [default={0}]".format(ROIRow_str), 'black'); ROIRow_str_justRead= input(); 
        if len(ROIRow_str_justRead)>2: ROIRow_str=ROIRow_str_justRead  # otherwise keeps the old value
        ROIRow= APy3_GENfuns.matlabLike_range(ROIRow_str); Row_1st=ROIRow[0];Row_last=ROIRow[-1];
        #
        X2fit=numpy.arange(Col_1st,Col_last+1)
        Y2fit=numpy.copy(inData[thisRow, Col_1st:Col_last+1])
        Y2fit[Y2fit>upLim]=numpy.NaN
        X2fit= X2fit[~numpy.isnan(Y2fit)]
        Y2fit= Y2fit[~numpy.isnan(Y2fit)]
        (Energy_eV,pin_diam,pin_Dist,J0_fit,J2_fit,C0_fit)= AiryDiskProfile_2harm_plusC_fit((X2fit-thisCol)*pixPitch,Y2fit, Energy_eV, pin_diam,pin_Dist, J0,J2,C0)
        APy3_GENfuns.printcol("plotting cutline along a Row for peak=({0},{1}), Energy={2}eV, pinhole diameter={3}m, Distance= {4}m, J0={5},J2={6}, C0={7}, limited to {8} to avoid saturation".format(thisRow,thisCol,Energy_eV,pin_diam,pin_Dist,J0_fit,J2_fit,C0_fit,upLim), 'blue')
        APy3_GENfuns.plot_1D(X2fit, Y2fit, 'cols','e','{0}eV, {1}um pinhole (Row={2})'.format(Energy_eV,round(pin_diam*(1e6),2),thisRow))
        Xfitted= numpy.arange(min(X2fit),max(X2fit),0.1)
        Yfitted= AiryDiskProfile_2harm_plusC_fun((Xfitted-thisCol)*pixPitch, Energy_eV,pin_diam,pin_Dist,J0_fit,J2_fit,C0_fit)
        matplotlib.pyplot.plot(Xfitted, Yfitted, '-')
        #
        matplotlib.pyplot.show(block=True)
    #
    elif  nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:", 'black')
        APy3_GENfuns.printcol("1: Airy + constant fit", 'black')
        APy3_GENfuns.printcol("2: 1st-harm-Airy + 2nd-harm-Airy + constant fit", 'black')
        APy3_GENfuns.printcol("d: Airy + constant & pinhole diameter fit", 'black')
    #
    APy3_GENfuns.printcol("plot avg [C]DS / [A]iry along a cut / [E]nd plotting", 'black')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
'''
'''
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')


#
#---
#%% profile it
#import cProfile
#cProfile.run('descramble_highMem(...)', sort='cumtime')
#%% or just execute it
#descramble_highMem(...)
