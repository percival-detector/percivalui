# -*- coding: utf-8 -*-
"""
descrambled (DLSRaw) sweep, having 2 Gn => calculate pedestal_ADU, e/ADU of higher Gn  

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_02_sweepCompare_multiGnCal.py
or:
python3
exec(open("./P2M_latOvfl_02_sweepCompare_multiGnCal.py").read())
"""
#
#%% imports and useful constants
from APy3_auxINIT import *
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

# to FITfuns


# to FITfuns

def plot_errbar_1Dx2_andfit_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, label_x,label_y, label_title):
    ''' 2x 1D scatter plot in the same canva ''' 
    (fit_slope1,fit_offset1)=     APy3_FITfuns.linear_fit(arrayX1,arrayY1)
    (fit_slope2,fit_offset2)=     APy3_FITfuns.linear_fit(arrayX2,arrayY2)
    #
    fig = matplotlib.pyplot.figure()
    #
    # stupid python tries to put plot before errorbar 
    matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5, label=legend1)
    matplotlib.pyplot.plot(arrayX1, APy3_FITfuns.linear_fun(arrayX1, fit_slope1,fit_offset1), '--b', label='fit')
    matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xg', fillstyle='none', capsize=5, label=legend2)
    matplotlib.pyplot.plot(arrayX2, APy3_FITfuns.linear_fun(arrayX2, fit_slope2,fit_offset2), '--g', label='fit')
    handles, labels = matplotlib.pyplot.gca().get_legend_handles_labels() 
    order = [2,0,3,1]
    matplotlib.pyplot.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    #
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)

#
# ---
#
#%% defaults for GUI window
#
#
'''
######################################### FSI01 PGABBB 0802h3, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_OD1.0_meta.dat' # tint<\tab>filename
#dflt_meta_file= 'reduced_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/LatOvflw/'+'FSI01_Tm20_dmuxSELHigh_0802h3_PGAB_2019.07.22_Gn012_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
dflt_Row2proc='801:806' 
dflt_Col2proc='351:354' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:351' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "FSI01,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/LatOvflw/'+'xxx'#'FSI01_Tm20_dmuxSELHigh_0802h3_PGAB_2019.07.22_Gn01_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### FSI01 PGABBB 0802h3, Gn1->2 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_OD0.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/LatOvflw/'+'FSI01_Tm20_dmuxSELHigh_0802h3_PGAB_2019.07.22_Gn012_MultiGnCal.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:351' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "FSI01,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/LatOvflw/'+'xxx'#'FSI01_Tm20_dmuxSELHigh_0802h3_PGAB_2019.07.22_Gn01_MultiGnCal.h5'

#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### FSI01 PGA6BB 0802h4 Gn 0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.30_FSI01_Tm20_dmuxSELHigh_0802h4_3G_PGA6BB_sweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.30_FSI01_Tm20_dmuxSELHigh_0802h4_3G_PGA6BB_OD2.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
dflt_multiGnCal_file= dflt_folder_data2process+ '../LatOvflw/'+'FSI01_Tm20_dmuxSELHigh_0802h4_PGA6BB_2019.07.30_Gn0_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
dflt_Row2proc='800:806' 
dflt_Col2proc='350:354' 
dflt_Row2proc='800:801' 
dflt_Col2proc='350:351'
dflt_Row2proc='808:808' 
dflt_Col2proc='350:350'
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #flt_debugFlag='N';
dflt_plotLabel= "FSI01,PGA6BB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'

dflt_minNpoints2fit=10

dflt_maxADU2fit=1500
dflt_minR22fit=0.95
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out=   dflt_folder_data2process+ '../LatOvflw/'+'FSI01_Tm20_dmuxSELHigh_0802h4_PGA6BB_2019.07.30_Gn01_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#

#
'''
######################################### BSI02 PGABBB 0802k2, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/2019.09.20_Latovflw_BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI02_Tm20_dmuxSELHigh_0802k2_3G_PGABBB_OD1.5_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_ADCcor/'+'BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_multiGn/'+'BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB_2019.09.15_Gn0xx_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:351' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI02,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'

dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_multiGn/'+'BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB_2019.09.15_Gn01x_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### BSI02 PGABBB 0802k2, Gn1->2 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/2019.09.20_Latovflw_BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI02_Tm20_dmuxSELHigh_0802k2_3G_PGABBB_OD0.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_ADCcor/'+'BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_multiGn/'+'BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB_2019.09.15_Gn0xx_MultiGnCal.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:351' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI02,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_multiGn/'+'BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB_2019.09.15_Gn01x_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
#
'''
######################################### BSI04 PGABBB BSI04_02, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHigh_BSI04_04_3G_PGABBB_OD2.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'

dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/LatOvflw_param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn0xx_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
#dflt_Img2proc='45:49' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
dflt_Row2proc='801:801' 
dflt_Col2proc='700:700' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/LatOvflw_param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn01x_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'

dflt_verboseFlag='Y'
'''
#
#'''
######################################### BSI04 PGABBB BSI04_02, Gn1->2 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHigh_BSI04_04_3G_PGABBB_OD1.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'

dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/LatOvflw_param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn01x_MultiGnCal.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Img2proc='5:9' 
#dflt_Img2proc='45:49' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
#dflt_Row2proc='801:801' 
#dflt_Col2proc='700:700' 
dflt_Row2proc=':' 
dflt_Col2proc=':'
#
dflt_showFlag='Y'; dflt_showFlag='N';
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_CDSGn0Flag='Y'
dflt_CMAFlag='N'
dflt_cols2CMA='0:32'
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
dflt_maxADU2fit=1500
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_file_out=   '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_04_3G_Latovflw/LatOvflw_param/'+'prelim_BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'

dflt_verboseFlag='Y'
#'''
#
# ---
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['process data: metafile'] 
GUIwin_arguments+= [dflt_meta_file] 
#
GUIwin_arguments+= ['ADUcorr: file'] 
GUIwin_arguments+= [dflt_ADUcorr_file]
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['process data: in Cols [from:to]'] 
GUIwin_arguments+= [dflt_Col2proc]
#
GUIwin_arguments+= ['Gn_to_calculate [1/2]'] 
GUIwin_arguments+= [dflt_Gn_to_calculate]
#
GUIwin_arguments+= ['CDS for Gn0? [Y/N]'] 
GUIwin_arguments+= [dflt_CDSGn0Flag]
GUIwin_arguments+= ['CMA? [Y/N]'] 
GUIwin_arguments+= [dflt_CMAFlag]
GUIwin_arguments+= ['if CMA: Reference Columns? [first:last]'] 
GUIwin_arguments+= [dflt_cols2CMA]
#
GUIwin_arguments+= ['fit? [Y/N]'] 
GUIwin_arguments+= [dflt_fitFlag]
GUIwin_arguments+= ['fit: at least Npoints'] 
GUIwin_arguments+= [dflt_minNpoints2fit]
GUIwin_arguments+= ['fit: below ADU'] 
GUIwin_arguments+= [dflt_maxADU2fit]
GUIwin_arguments+= ['fit: at least R2'] 
GUIwin_arguments+= [dflt_minR22fit]
#
GUIwin_arguments+= ['show individual pixel ramps? [Y/N]'] 
GUIwin_arguments+= [dflt_showFlag]
GUIwin_arguments+= ['debug info (will not calculate paremeters, only show ramps in ADU)? [Y/N]'] 
GUIwin_arguments+= [dflt_debugFlag]

GUIwin_arguments+= ['plot label'] 
GUIwin_arguments+= [dflt_plotLabel]
#
GUIwin_arguments+= ['save results? [Y/N]'] 
GUIwin_arguments+= [dflt_saveFlag]
GUIwin_arguments+= ['save results: in file'] 
GUIwin_arguments+= [dflt_file_out]
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
meta_file= dataFromUser[i_param]; i_param+=1
ADUcorr_file= dataFromUser[i_param]; i_param+=1;  
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1];
#
Row2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Row2proc_mtlb in ['all','All','ALL',':','*','-1']: Row2proc= numpy.arange(NRow)
else: Row2proc=APy3_GENfuns.matlabLike_range(Row2proc_mtlb)
#
Col2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Col2proc_mtlb in ['all','All','ALL',':','*','-1']: Col2proc= numpy.arange(32,NCol)
else: Col2proc=APy3_GENfuns.matlabLike_range(Col2proc_mtlb)
#
Gn_to_calculate= int(dataFromUser[i_param]); i_param+=1;  
#
CDSGn0Flag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
CMAFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cols2CMA_mtlb= dataFromUser[i_param]; i_param+=1
cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
#
fitFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
minNpoints2fit= int(dataFromUser[i_param]); i_param+=1;  
maxADU2fit= float(dataFromUser[i_param]); i_param+=1;  
minR22fit= float(dataFromUser[i_param]); i_param+=1;  
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
debugFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
plotLabel= dataFromUser[i_param]; i_param+=1;
#
saveFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
file_out= dataFromUser[i_param]; i_param+=1
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using metafile {0}'.format(meta_file),'blue')
    APy3_GENfuns.printcol('will ADU-correct using {0})'.format(ADUcorr_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate Img{0}, pix({1},{2})'.format(Img2proc_mtlb,Row2proc_mtlb,Col2proc_mtlb),'blue')
    #
    APy3_GENfuns.printcol('will try to calculate parameters for Gn{0}'.format(Gn_to_calculate),'blue')
    APy3_GENfuns.printcol('  assuming Gn{0} Pedestal[ADU] and e/ADU data from {1}'.format(Gn_to_calculate-1,multiGnCal_file),'blue')
    #
    if debugFlag: 
        APy3_GENfuns.printcol('will show debug info, will not calculate the coefficient','orange')
        APy3_GENfuns.printcol('    also will force not to use CDS on Gn0, and not to subtract pedestal','orange')
        CDSGn0Flag=False
    else:
        if (Gn_to_calculate==1)&(CDSGn0Flag): APy3_GENfuns.printcol('  will use CDS for Gn0 values','blue')
    #
    if (CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol(0)'.format(cols2CMA_mtlb),'blue')
    #
    if fitFlag: APy3_GENfuns.printcol('will fit, at least {0} points, below {1}ADU, R2>={2})'.format(minNpoints2fit,maxADU2fit,minR22fit),'blue')
    #
    if showFlag: APy3_GENfuns.printcol('will show plots','blue')
    #
    if saveFlag: APy3_GENfuns.printcol('will save results in {0})'.format(file_out),'blue')
    if saveFlag & debugFlag: APy3_GENfuns.printcol('if debug info, will not calculate the coefficient, so can not save','orange')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
gainRatioMap= APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
unknown_ADU2e=APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
unknown_ADU0= APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
# ---
if verboseFlag: APy3_GENfuns.printcol('load meta-file and calibr-files','blue')
if APy3_GENfuns.notFound(folder_data2process+meta_file): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_file)
meta_content= APy3_GENfuns.read_tst(folder_data2process+meta_file)
meta_fileNameList= meta_content[:,1]
meta_tintAr= meta_content[:,0].astype(float)
meta_Nfiles= len(meta_fileNameList)
if verboseFlag: APy3_GENfuns.printcol("{0} entries in the metafile".format(meta_Nfiles),'green')
#
if APy3_GENfuns.notFound(ADUcorr_file): APy3_GENfuns.printErr('not found: '+ADUcorr_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
 ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
known_ADU2e= e_per_ADU_multiGn[Gn_to_calculate-1,:,:]
PedADU_knownGn= PedestalADU_multiGn[Gn_to_calculate-1,:,:]
if debugFlag: 
    APy3_GENfuns.printcol('since debug, will not to subtract pedestal','orange')
    PedADU_knownGn=numpy.zeros((NRow,NCol))
# ---
#
#%% light file: DLSRaw => Gn,ADU
if verboseFlag: APy3_GENfuns.printcol('convert sequence files DLSRaw => Gn,ADU','blue')
allData_ADU= APy3_GENfuns.numpy_NaNs((meta_Nfiles,len(Img2proc),NSmplRst, NRow,NCol))
allData_Gn=  numpy.zeros((meta_Nfiles,len(Img2proc),NRow,NCol),dtype=int)-1
aux_theseADU= APy3_GENfuns.numpy_NaNs((len(Img2proc),NSmplRst, NRow,NCol))
allData_tintAr = numpy.transpose(numpy.tile(meta_tintAr, (len(Img2proc),1)), (1,0)) # NImg => (Nfile,NImg)
#
allData_GnCrsFn=  numpy.ones((meta_Nfiles,len(Img2proc),NSmplRst,NRow,NCol,NGnCrsFn),dtype='int16')*(ERRint16)
#
for iFile,thisFile in enumerate(meta_fileNameList):
    if verboseFlag: APy3_GENfuns.printcol("processing lgh file {0}/{1}".format(iFile,meta_Nfiles-1),'green')
    (dataSmpl_DLSraw,dataRst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+thisFile, '/data','/reset', fromImg, toImg)
    data_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(dataSmpl_DLSraw,dataRst_DLSraw, ERRDLSraw, ERRint16)
    allData_GnCrsFn[iFile,:,:,:,:,:]=numpy.copy(data_GnCrsFn).astype(int) 
    if cleanMemFlag: del dataSmpl_DLSraw; del dataRst_DLSraw
    allData_Gn[iFile,:,:,:]=data_GnCrsFn[:,iSmpl,:,:,iGn].astype(int) 
    #

    aux_theseADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iSmpl,:,:,iCrs],data_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
    aux_theseADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iRst,:,:,iCrs], data_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
    missingValMap= data_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
    aux_theseADU[missingValMap]= numpy.NaN
    allData_ADU[iFile,:,:,:,:]= numpy.copy(aux_theseADU)
    # ...
    if cleanMemFlag: del data_GnCrsFn; del missingValMap
if cleanMemFlag: del aux_theseADU; 
# ---
#
#%% elab data
for thisRow in Row2proc:
    for thisCol in Col2proc:
        map_knownGn=   allData_Gn[:,:,thisRow,thisCol]==(Gn_to_calculate-1)
        map_unknownGn= allData_Gn[:,:,thisRow,thisCol]==(Gn_to_calculate)

        tint_knownGn=  allData_tintAr[map_knownGn].flatten()
        tint_unknownGn=allData_tintAr[map_unknownGn].flatten()
        
        aux_smpl= numpy.copy(allData_ADU[:,:,iSmpl,thisRow,thisCol])
        smpl_knownGn= aux_smpl[map_knownGn].flatten() 
        smpl_unknownGn= aux_smpl[map_unknownGn].flatten()

        aux_Gn= numpy.copy(allData_Gn[:,:,thisRow,thisCol])
        Gn_knownGn=   aux_Gn[map_knownGn] # technically useless, but easier for CDS,Gn0
        Gn_unknownGn= aux_Gn[map_unknownGn]
        #
        if CMAFlag:
            for iFile in range(meta_Nfiles):
                allData_ADU[iFile,:,iSmpl,:,:]= APy3_P2Mfuns.CMA(allData_ADU[iFile,:,iSmpl,:,:] ,cols2CMA)
                allData_ADU[iFile,:,iRst,:,:]=  APy3_P2Mfuns.CMA(allData_ADU[iFile,:,iRst,:,:]  ,cols2CMA)
        #
        if CDSGn0Flag & (Gn_to_calculate-1==0):
            smpl_knownGn=[]; tint_knownGn=[]; Gn_knownGn=[]
            for iFile in range(meta_Nfiles):
                for iImg in range(1,len(Img2proc)):
                    # scratch 1st img because CDS
                    if allData_Gn[iFile,iImg,thisRow,thisCol]== (Gn_to_calculate-1):
                        tint_knownGn+= [allData_tintAr[iFile,iImg]]
                        smpl_knownGn+= [allData_ADU[iFile,iImg,iSmpl,thisRow,thisCol] - allData_ADU[iFile,iImg-1,iRst,thisRow,thisCol]]
                        Gn_knownGn+=   [Gn_to_calculate-1]
            tint_knownGn= numpy.array(tint_knownGn)
            smpl_knownGn= numpy.array(smpl_knownGn)
            Gn_knownGn=   numpy.array(Gn_knownGn)
        #
        if CDSGn0Flag: aux_str= 'CDS'
        else: aux_str= 'Smpl'
        if CMAFlag: aux_str+=',CMA'
        #
        # pedestal-subtract
        smpl_knownGn=   smpl_knownGn -   PedADU_knownGn[thisRow,thisCol]
        smpl_unknownGn= smpl_unknownGn
        #
        if (len(smpl_knownGn)>0) & (len(smpl_unknownGn)>0):
            #if fitFlag & (APy3_GENfuns.count_distinct_elements(tint_knownGn)>minNpoints2fit) & (APy3_GENfuns.count_distinct_elements(tint_unknownGn)>minNpoints2fit):
            if fitFlag & (APy3_GENfuns.count_distinct_elements(tint_knownGn[smpl_knownGn<maxADU2fit])>minNpoints2fit) & (APy3_GENfuns.count_distinct_elements(tint_unknownGn[smpl_unknownGn<maxADU2fit])>minNpoints2fit):
                (slopefit_knownGn, interceptfit_knownGn)=     APy3_FITfuns.linear_fit(   tint_knownGn[smpl_knownGn<maxADU2fit],smpl_knownGn[smpl_knownGn<maxADU2fit])
                R2_knownGn=                                   APy3_FITfuns.linear_fit_R2(tint_knownGn[smpl_knownGn<maxADU2fit],smpl_knownGn[smpl_knownGn<maxADU2fit])
                (slopefit_unknownGn, interceptfit_unknownGn)= APy3_FITfuns.linear_fit(   tint_unknownGn[smpl_unknownGn<maxADU2fit],smpl_unknownGn[smpl_unknownGn<maxADU2fit])
                R2_unknownGn=                                 APy3_FITfuns.linear_fit_R2(tint_unknownGn[smpl_unknownGn<maxADU2fit],smpl_unknownGn[smpl_unknownGn<maxADU2fit])
                if (R2_knownGn>=minR22fit)&(R2_unknownGn>=minR22fit):
                    gainRatioMap[thisRow,thisCol]= slopefit_knownGn/slopefit_unknownGn
                    unknown_ADU2e[thisRow,thisCol]= known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol]
                    unknown_ADU0[thisRow,thisCol]=interceptfit_unknownGn
                    #
                    if verboseFlag:
                        if ~debugFlag: 
                            APy3_GENfuns.printcol("pix({0},{1}):".format(thisRow,thisCol),'green')
                            APy3_GENfuns.printcol("  Gn{0}: {1}steps, fit_slope={2}ADU/ms,fit_intercept={3}ADU,R2={4}, e/ADU:{5}".format(Gn_to_calculate-1, APy3_GENfuns.count_distinct_elements(tint_knownGn),slopefit_knownGn,interceptfit_knownGn,R2_knownGn, round(known_ADU2e[thisRow,thisCol],3)),'green')
                            APy3_GENfuns.printcol("  Gn{0}: {1}steps, fit_slope={2}ADU/ms,fit_intercept={3}ADU,R2={4}, e/ADU:{5}".format(Gn_to_calculate, APy3_GENfuns.count_distinct_elements(tint_unknownGn),slopefit_unknownGn,interceptfit_unknownGn,R2_unknownGn, round(unknown_ADU2e[thisRow,thisCol],3)),'green')
                        #
                        else: APy3_GENfuns.printcol("pix({0},{1}), Gn{2}->{3} ({4},{5} steps): ,R2={6},{7}".format(thisRow,thisCol, Gn_to_calculate-1,Gn_to_calculate, APy3_GENfuns.count_distinct_elements(tint_knownGn), APy3_GENfuns.count_distinct_elements(tint_unknownGn), R2_knownGn,R2_unknownGn),'green')
                elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2}: R2={3}; Gn{4}: R2={5}".format(thisRow,thisCol, Gn_to_calculate-1, R2_knownGn,Gn_to_calculate, R2_unknownGn ),'orange')
            #
            elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2}: {3} steps; Gn{4}: {5} steps".format(thisRow,thisCol, Gn_to_calculate-1, APy3_GENfuns.count_distinct_elements(tint_knownGn),Gn_to_calculate, APy3_GENfuns.count_distinct_elements(tint_unknownGn) ),'orange')
            #
            # calculate avg vals of same tint, same Gn
            (tint_xavg_knownGn,smpl_xavg_knownGn,smpl_std_knownGn)=       APy3_GENfuns.avgY_of_sameX_1D(tint_knownGn,smpl_knownGn)
            (tint_xavg_unknownGn,smpl_xavg_unknownGn,smpl_std_unknownGn)= APy3_GENfuns.avgY_of_sameX_1D(tint_unknownGn,smpl_unknownGn)
            #
            if showFlag & ~debugFlag:
                if (Gn_to_calculate==1): 
                    APy3_GENfuns.plot_1Dx3_samecanva(tint_knownGn,smpl_knownGn*known_ADU2e[thisRow,thisCol],'Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                                            tint_unknownGn,(smpl_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                            [],[],'Gn2', 
                                            'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)
                    APy3_GENfuns.plot_1Dx3_samecanva(tint_knownGn,smpl_knownGn*known_ADU2e[thisRow,thisCol],'Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                                            tint_unknownGn,(smpl_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                            [],[],'Gn2', 
                                            'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), True)
                else: 
                    APy3_GENfuns.plot_1Dx3_samecanva([],[],'Gn0', 
                                  tint_knownGn,smpl_knownGn*known_ADU2e[thisRow,thisCol],'Gn{1}'.format(aux_str,Gn_to_calculate-1),
                                  tint_unknownGn,(smpl_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate), 
                                  'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)
                    APy3_GENfuns.plot_1Dx3_samecanva([],[],'Gn0', 
                                  tint_knownGn,smpl_knownGn*known_ADU2e[thisRow,thisCol],'Gn{1}'.format(aux_str,Gn_to_calculate-1),
                                  tint_unknownGn,(smpl_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate), 
                                  'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), True)
                APy3_GENfuns.show_it()
            #
            elif showFlag & debugFlag:
                if (Gn_to_calculate==1): 
                    #APy3_GENfuns.plot_errbar_1Dx3_samecanva(
                    #                           tint_xavg_knownGn,smpl_xavg_knownGn*known_ADU2e[thisRow,thisCol],smpl_std_knownGn*known_ADU2e[thisRow,thisCol],
                    #                           'Gn{1} (avg)'.format(aux_str,Gn_to_calculate-1), 
                    #                           tint_xavg_unknownGn,(smpl_xavg_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],
                    #                           smpl_std_unknownGn*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],
                    #                           'Gn{0} (avg)'.format(Gn_to_calculate),
                    #                           [],[],[],'', 
                    #                           'tint [ms]','reconstructed avg output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                    #
                    APy3_GENfuns.plot_1Dx3_samecanva(tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                                               tint_unknownGn,smpl_unknownGn,'Smpl,Gn{0}'.format(Gn_to_calculate), 
                                               [],[],'Gn2',
                                               'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)                    
                    #
                    #APy3_FITfuns.plot_1Dx3_andfit_samecanva(tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                    #                           tint_unknownGn,smpl_unknownGn,'Smpl,Gn{0}'.format(Gn_to_calculate), 
                    #                           [],[],'Gn2',
                    #                           'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                    #
                    #APy3_GENfuns.plot_errbar_1Dx3_samecanva(tint_xavg_knownGn,  smpl_xavg_knownGn,  smpl_std_knownGn,  '{0},Gn{1} (avg)'.format(aux_str,Gn_to_calculate-1), 
                    #                                            tint_xavg_unknownGn,smpl_xavg_unknownGn,smpl_std_unknownGn,'{0},Gn{1} (avg)'.format(aux_str,Gn_to_calculate), 
                    #                                            [],[],[],'',
                    #                                            'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                else: 
                    #APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],'', 
                    #                           tint_xavg_knownGn,smpl_xavg_knownGn*known_ADU2e[thisRow,thisCol],smpl_std_knownGn*known_ADU2e[thisRow,thisCol],
                    #                           'Gn{1} (avg)'.format(aux_str,Gn_to_calculate-1),
                    #                           tint_xavg_unknownGn,(smpl_xavg_unknownGn-unknown_ADU0[thisRow,thisCol])*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],
                    #                           smpl_std_unknownGn*known_ADU2e[thisRow,thisCol]*gainRatioMap[thisRow,thisCol],
                    #                           'Gn{0} (avg)'.format(Gn_to_calculate), 
                    #                           'tint [ms]','reconstructed avg output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                    #
                    APy3_GENfuns.plot_1Dx3_samecanva([],[],'Gn0',
                                               tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                                               tint_unknownGn,smpl_unknownGn,'Smpl,Gn{0}'.format(Gn_to_calculate), 
                                               'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)
                    #
                    #APy3_FITfuns.plot_1Dx3_andfit_samecanva([],[],[],'Gn0',
                    #                           tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_str,Gn_to_calculate-1), 
                    #                           tint_unknownGn,smpl_unknownGn,'Smpl,Gn{0}'.format(Gn_to_calculate), 
                    #                           'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                    #
                    #APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],'',
                    #                                            tint_xavg_knownGn,  smpl_xavg_knownGn,  smpl_std_knownGn,  '{0},Gn{1}  (avg)'.format(aux_str,Gn_to_calculate-1), 
                    #                                            tint_xavg_unknownGn,smpl_xavg_unknownGn,smpl_std_unknownGn,'{0},Gn{1}  (avg)'.format(aux_str,Gn_to_calculate), 
                    #                                            'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                    #
                    #plot_errbar_1Dx2_andfit_samecanva(tint_xavg_knownGn,smpl_xavg_knownGn,smpl_std_knownGn,'{0},Gn{1} (avg)'.format(aux_str,Gn_to_calculate-1), 
                    #                           tint_xavg_unknownGn,smpl_xavg_unknownGn,smpl_std_unknownGn,'Smpl,Gn{0} (avg)'.format(Gn_to_calculate), 
                    #                           'tint [ms]','ADU', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                #
                APy3_GENfuns.plot_1D_2scales(allData_tintAr.flatten(), allData_GnCrsFn[:,:,iSmpl,thisRow,thisCol,iCrs].flatten(), allData_GnCrsFn[:,:,iSmpl,thisRow,thisCol,iFn].flatten(), 
                                             'tint [ms]', 'crs values', 'crs values', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol))
                APy3_GENfuns.show_it()
        elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2} or Gn{3}: no steps".format(thisRow,thisCol, Gn_to_calculate-1, Gn_to_calculate),'orange')
        if cleanMemFlag: del aux_smpl; del aux_Gn; 
if cleanMemFlag: del allData_GnCrsFn
#
e_per_ADU_multiGn_out= numpy.copy(e_per_ADU_multiGn)
e_per_ADU_multiGn_out[Gn_to_calculate]= unknown_ADU2e
#
PedestalADU_multiGn_out= numpy.copy(PedestalADU_multiGn)
PedestalADU_multiGn_out[Gn_to_calculate]= unknown_ADU0
#
if (debugFlag==False):
    for iGn in range(3):
        APy3_GENfuns.plot_2D_all(e_per_ADU_multiGn_out[iGn], False, 'col','row',"Gn{0}: e/ADU".format(iGn), True)
        APy3_GENfuns.plot_2D_all(PedestalADU_multiGn_out[iGn], False, 'col','row',"Gn{0}: pedestal [ADU]".format(iGn), True)
    APy3_GENfuns.show_it()
#---
if saveFlag & ~debugFlag:
    APy3_GENfuns.write_2xh5(file_out, 
           PedestalADU_multiGn_out, '/Pedestal_ADU/', 
           e_per_ADU_multiGn_out, '/e_per_ADU/')
    if verboseFlag: APy3_GENfuns.printcol("data saved in {0} under /Pedestal_ADU/ , /e_per_ADU/".format(file_out),'green')
#---
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
# ---
# ---
# ---

