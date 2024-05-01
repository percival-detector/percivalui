 # -*- coding: utf-8 -*-
"""
avgxGn sweep, having 2 Gn => calculate pedestal_ADU, e/ADU of higher Gn  

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_02b_sweepCompare_multiGnCal_using_avgs.py
or:
python3
exec(open("./P2M_latOvfl_02b_sweepCompare_multiGnCal_using_avgs.py").read())
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
def png_1D(arrayX, arrayY, label_x,label_y,label_title, filenamepath):
    ''' 1D scatter plot: save(not show): e.g. filenamepath='/tmp/test0.png' ''' 
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
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
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
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
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
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

def png_errbar_1Dx3_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, arrayX3,arrayY3,errbarY3,legend3, label_x,label_y, label_title, loglogFlag, filenamepath):
    """ 3x 1D scatter plot (+errbars) in the same canva: save to png """
    #
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyP2M_latOvfl_02b_Extract_multiGnCal_using_avgs.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    if len(arrayX1)>0: matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='^r', fillstyle='none', capsize=5, label=legend1)
    if len(arrayX2)>0: matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xb', fillstyle='none', capsize=5, label=legend2)
    if len(arrayX3)>0: matplotlib.pyplot.errorbar(arrayX3, arrayY3,yerr=errbarY3, fmt='ok', fillstyle='none', capsize=5, label=legend3)
    matplotlib.pyplot.legend(loc='best')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return 







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
#
'''
######### BSI04 PGABBB BSI04_02, Gn0->1 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_std_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn0xx_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn01x_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
'''
#
'''
######### BSI04 PGABBB BSI04_02, Gn1->2 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD3.0_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD3.0_std_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn01x_MultiGnCal.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit= 10 
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5_usingOD3.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
'''
#
'''
######### BSI04 PGABBB BSI04_02, Gn0->1 (v2) #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2pirocess+='/'
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_std_meta.dat' 
#
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn0xx_MultiGnCal.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn01x_MultiGnCal.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
'''
#
'''
######### BSI04 PGABBB BSI04_02, Gn1->2 (v2) #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2pirocess+='/'
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD3.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD3.0_std_meta.dat' 
#
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn01x_MultiGnCal.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGABBB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5_prelim.h5'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
'''
#
'''
######### BSI04 PGABBB BSI04_05, Gn0->1->2 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2pirocess+='/'
#
# Gn0->1
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_sigma_meta.dat' 
dflt_Gn_to_calculate=1
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn0xx_2020.05.14_MultiGnCal.h5'
dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn01x_2020.05.14_MultiGnCal.h5_prelim.h5'
#
# Gn1->2
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
#dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' 
#dflt_meta_std_file='BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat' 
#dflt_Gn_to_calculate=2
#dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn01x_2020.05.14_MultiGnCal.h5'
#dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14_MultiGnCal.h5_prelim.h5'
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; #dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGA6BB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.99
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
'''
#
'''
######### 3/7 BSI04 PGABBB BSI04_05, Gn0->1->2 alternate extractions #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2pirocess+='/'
#
# Gn0->1
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
#dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_avg_meta.dat' 
#dflt_meta_std_file='BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_sigma_meta.dat' 
#dflt_Gn_to_calculate=1
#dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn0xx_2020.05.14b_MultiGnCal.h5'
#dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn01x_2020.05.14b_MultiGnCal.h5_prelim.h5'
#
# Gn1->2
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat' 
dflt_Gn_to_calculate=2
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn01x_2020.05.14b_MultiGnCal.h5_prelim.h5'
dflt_file_out= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_prelim.h5'
#
dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGA6BB"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=10
#dflt_maxADU2fit=1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.95
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
#'''
#
#
'''
######### 7/7 BSI04 PGA6BB BSI04_05, Gn0->1->2 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
# Gn0->1
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
dflt_meta_file=    'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_sigma_meta.dat'
dflt_Gn_to_calculate=1
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn0xx_2020.06.10_MultiGnCal_ADU2eAvg.h5'
dflt_file_out=        dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn01x_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD5.0_prelim.h5'
#
# Gn1->2
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
#dflt_meta_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' 
#dflt_meta_std_file='BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat' 
#dflt_Gn_to_calculate=2
#dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn01x_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD5.0_prelim.h5'
#dflt_file_out=        dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5'
#
#dflt_Row2proc='700:705'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGA6BB, 7of7ADC"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=4 #10
#dflt_maxADU2fit=2500 #1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.95
#
dflt_saveFlag='Y'; dflt_saveFlag='N'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder= "NONE"
#dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
#'''
#
#
#'''
######### 7/7 BSI04 PGA6BB BSI04_05, Gn0->1->2 reduced R2#################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
# Gn0->1
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
#dflt_meta_file=    'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_avg_meta.dat' 
#dflt_meta_std_file='BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_sigma_meta.dat'
#dflt_Gn_to_calculate=1
#dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn0xx_2020.06.10_MultiGnCal_ADU2eAvg.h5'
#dflt_file_out=        dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn01x_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD5.0_R2_0.85_prelim.h5'
#
# Gn1->2
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn2
dflt_meta_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' 
dflt_meta_std_file='BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat' 
dflt_Gn_to_calculate=2
dflt_multiGnCal_file= dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn01x_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD5.0_R2_0.85.h5'
dflt_file_out=        dflt_folder_data2process + '../LatOvflw_Param/'+'BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD0.5_OD3.0_R2_0.85_prelim.h5'
#
#dflt_Row2proc='700:705'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N';
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_plotLabel= "BSI04,PGA6BB, 7of7ADC"
#
dflt_fitFlag='Y'
dflt_minNpoints2fit=4 #10
#dflt_maxADU2fit=2500 #1500
dflt_maxADU2fit=0.75   # 75% of max #0.9 #up to 90% of max
dflt_minslope2fit=0.0 # slope non-negative
dflt_minR22fit=0.85 #0.95
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#
dflt_saveInsteadOfPlotting_Folder= "NONE"
#dflt_saveInsteadOfPlotting_Folder='/home/marras/auximg/'
#'''
#
#
#
# ---
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['process data: avg metafile'] 
GUIwin_arguments+= [dflt_meta_file] 
GUIwin_arguments+= ['process data: std metafile'] 
GUIwin_arguments+= [dflt_meta_std_file] 
#
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['process data: in Cols [from:to]'] 
GUIwin_arguments+= [dflt_Col2proc]
#
GUIwin_arguments+= ['Gn_to_calculate [1/2]'] 
GUIwin_arguments+= [dflt_Gn_to_calculate]
#
GUIwin_arguments+= ['fit? [Y/N]'] 
GUIwin_arguments+= [dflt_fitFlag]
GUIwin_arguments+= ['fit: at least Npoints'] 
GUIwin_arguments+= [dflt_minNpoints2fit]
#
#GUIwin_arguments+= ['fit: below ADU'] 
#GUIwin_arguments+= [dflt_maxADU2fit]
GUIwin_arguments+= ['fit: (to avoid saturation): use up to x of the max ADU [between 0 and 1]']
GUIwin_arguments+= [dflt_maxADU2fit]
GUIwin_arguments+= ['fit: minimum ADU/ms slope (if saturated, can give artefacts <0)']
GUIwin_arguments+= [dflt_minslope2fit]
#
GUIwin_arguments+= ['fit: at least R2'] 
GUIwin_arguments+= [dflt_minR22fit]
#
GUIwin_arguments+= ['show values? [Y/N]'] 
GUIwin_arguments+= [dflt_showFlag]

GUIwin_arguments+= ['save png instead of showing: folder [NONE noto to do it]']
GUIwin_arguments+= [str(dflt_saveInsteadOfPlotting_Folder)]

GUIwin_arguments+= ['debug info (individual pixel ramps)? [Y/N]'] 
GUIwin_arguments+= [dflt_debugFlag]
#
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
meta_std_file= dataFromUser[i_param]; i_param+=1
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
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
fitFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
minNpoints2fit= int(dataFromUser[i_param]); i_param+=1;  
maxADU2fit= float(dataFromUser[i_param]); i_param+=1;  
minslope2fit= float(dataFromUser[i_param]); i_param+=1;  
minR22fit= float(dataFromUser[i_param]); i_param+=1;  
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1

saveInsteadOfPlotting_Folder=dataFromUser[i_param]; i_param+=1;
if saveInsteadOfPlotting_Folder in APy3_GENfuns.NOlist: saveInsteadOfPlotting_Flag=False
else: saveInsteadOfPlotting_Flag=True

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
if True: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using avg metafile {0}'.format(meta_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate pix({0},{1})'.format(Row2proc_mtlb,Col2proc_mtlb),'blue')
    #
    APy3_GENfuns.printcol('will try to calculate parameters for Gn{0}'.format(Gn_to_calculate),'blue')
    APy3_GENfuns.printcol('  assuming Gn{0} Pedestal[ADU] and e/ADU data from {1}'.format(Gn_to_calculate-1,multiGnCal_file),'blue')
    #
    if debugFlag: 
        APy3_GENfuns.printcol('will show debug info','blue')
        APy3_GENfuns.printcol('  using std metafile {0}'.format(meta_std_file),'blue')
        if saveInsteadOfPlotting_Flag: APy3_GENfuns.printcol('  instad of showing debug plots, will save them to {0}'.format(saveInsteadOfPlotting_Folder),'blue')

    #
    if fitFlag: APy3_GENfuns.printcol('will fit, at least {0} points, ADU below {1} of max, R2>={2}, slope>={3})'.format(minNpoints2fit,maxADU2fit,minR22fit,minslope2fit),'blue')
    #
    if showFlag: APy3_GENfuns.printcol('will show/save-png plots 2D-results','blue')
    #
    if saveFlag: APy3_GENfuns.printcol('will save results in {0})'.format(file_out),'blue')
    if saveFlag & debugFlag: APy3_GENfuns.printcol('if debug info, will not calculate the coefficient, so can not save','orange')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
# ---
#
APy3_GENfuns.printcol('loading meta-file and calibr-files','blue')
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
knownGn_ADU2e=  e_per_ADU_multiGn[Gn_to_calculate-1,:,:]
knwGn_ADU0= PedestalADU_multiGn[Gn_to_calculate-1,:,:]
unknwGn_ADU2e=APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
unknwGn_ADU0= APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
#
if APy3_GENfuns.notFound(folder_data2process+meta_file): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_file)
meta_content= APy3_GENfuns.read_tst(folder_data2process+meta_file)
meta_tintAr= meta_content[:,0].astype(float)
meta_Nfiles= len(meta_tintAr)
if verboseFlag: APy3_GENfuns.printcol("{0} entries in the metafile".format(meta_Nfiles),'green')
meta_fileNameList = [[] for y in range(3)]
for iGn in range(3):
    meta_fileNameList[iGn]= meta_content[:,iGn+1]
#for ifile in range(meta_Nfiles):
#    APy3_GENfuns.printcol("{0} {1} {2} {3}".format(meta_tintAr[ifile],meta_fileNameList[0][ifile],meta_fileNameList[1][ifile],meta_fileNameList[2][ifile]),'green')
#
allData_tint= numpy.array(meta_tintAr)
allData_Gnknown= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
allData_Gnunknw= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
#

meta_std_content= APy3_GENfuns.read_tst(folder_data2process+meta_std_file)
if len(meta_std_content[:,0])!=meta_Nfiles: APy3_GENfuns.printErr('avg metafile entries {0} != std metafile entries {0}'.format(meta_Nfiles,meta_std_content[:,0])) 
meta_std_fileNameList = [[] for y in range(3)]
for iGn in range(3):
    meta_std_fileNameList[iGn]= meta_std_content[:,iGn+1]
allData_std_Gnknown= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
allData_std_Gnunknw= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
#
APy3_GENfuns.printcol("reading files",'blue')
for iFile in range(meta_Nfiles):
    thisFile= meta_fileNameList[Gn_to_calculate-1][iFile]
    allData_Gnknown[iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile, '/data/data')
    thisFile= meta_fileNameList[Gn_to_calculate][iFile]
    allData_Gnunknw[iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile, '/data/data')
    #
    allData_std_Gnknown[iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+meta_std_fileNameList[Gn_to_calculate-1][iFile], '/data/data')
    allData_std_Gnunknw[iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+meta_std_fileNameList[Gn_to_calculate][iFile],   '/data/data')
    #
    APy3_GENfuns.dot_every10th(iFile,meta_Nfiles)
    #
APy3_GENfuns.printcol("elaborating pixel data",'blue')
for thisRow in Row2proc:
    if (verboseFlag==False): APy3_GENfuns.printcol('doing row {0}'.format(thisRow),'green')
    for thisCol in Col2proc:
        #if (verboseFlag==False): APy3_GENfuns.dot_every10th(thisCol-Col2proc[0],len(Col2proc))

        smpl_knownGn= allData_Gnknown[:,thisRow,thisCol]
        smpl_unknwGn= allData_Gnunknw[:,thisRow,thisCol]
        y_knownGn= smpl_knownGn[~numpy.isnan(smpl_knownGn)]
        x_knownGn= allData_tint[~numpy.isnan(smpl_knownGn)]
        y_unknwGn= smpl_unknwGn[~numpy.isnan(smpl_unknwGn)]
        x_unknwGn= allData_tint[~numpy.isnan(smpl_unknwGn)]
        #
        smpl_std_knownGn= allData_std_Gnknown[:,thisRow,thisCol]
        smpl_std_unknwGn= allData_std_Gnunknw[:,thisRow,thisCol]
        y_std_knownGn= smpl_std_knownGn[~numpy.isnan(smpl_knownGn)]
        y_std_unknwGn= smpl_std_unknwGn[~numpy.isnan(smpl_unknwGn)]
        #
        if cleanMemFlag: del smpl_knownGn; del smpl_unknwGn; del smpl_std_knownGn; del smpl_std_unknwGn
        #
        if (debugFlag & (~saveInsteadOfPlotting_Flag)):
            if (Gn_to_calculate==1): 
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(x_knownGn,y_knownGn,y_std_knownGn,'Gn{0}'.format(Gn_to_calculate-1), 
                                                        x_unknwGn,y_unknwGn,y_std_unknwGn,'Gn{0}'.format(Gn_to_calculate),
                                                        [],[],[],'Gn2',
                                                        'tint [ms]','pixel output (non pedestal-subtracted) [ADU]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False )
                APy3_GENfuns.show_it()
            else:
                APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                                        x_knownGn,y_knownGn,y_std_knownGn,'Gn{0}'.format(Gn_to_calculate-1), 
                                                        x_unknwGn,y_unknwGn,y_std_unknwGn,'Gn{0}'.format(Gn_to_calculate),
                                                        'tint [ms]','pixel output (non pedestal-subtracted) [ADU]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False )
                APy3_GENfuns.show_it()
        elif (debugFlag & saveInsteadOfPlotting_Flag):
            aux_png= '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol)
            if (Gn_to_calculate==1):
                png_errbar_1Dx3_samecanva(x_knownGn,y_knownGn,y_std_knownGn,'Gn{0}'.format(Gn_to_calculate-1),
                                          x_unknwGn,y_unknwGn,y_std_unknwGn,'Gn{0}'.format(Gn_to_calculate),
                                          [],[],[],'Gn2',
                                          'tint [ms]','pixel output (non pedestal-subtracted) [ADU]', 
                                          aux_png, False, saveInsteadOfPlotting_Folder+aux_png+'.png' )
            else:
                png_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                          x_knownGn,y_knownGn,y_std_knownGn,'Gn{0}'.format(Gn_to_calculate-1),
                                          x_unknwGn,y_unknwGn,y_std_unknwGn,'Gn{0}'.format(Gn_to_calculate),
                                          'tint [ms]','pixel output (non pedestal-subtracted) [ADU]', 
                                          aux_png, False, saveInsteadOfPlotting_Folder+aux_png+'.png' )
            APy3_GENfuns.printcol("png saved: "+saveInsteadOfPlotting_Folder+aux_png+'.png','blue')
        #
        if fitFlag:
            if (len(y_knownGn)>=minNpoints2fit) & (len(y_unknwGn)>=minNpoints2fit):
                y_knownGn2fit_map= y_knownGn<=(maxADU2fit*numpy.nanmax(y_knownGn))
                y_knownGn2fit= y_knownGn[y_knownGn2fit_map]
                x_knownGn2fit= x_knownGn[y_knownGn2fit_map]
                #
                y_unknwGn2fit_map= y_unknwGn<=(maxADU2fit*numpy.nanmax(y_unknwGn))
                y_unknwGn2fit= y_unknwGn[y_unknwGn2fit_map]
                x_unknwGn2fit= x_unknwGn[y_unknwGn2fit_map]
                #
                y_std2fit_knownGn= y_std_knownGn[y_knownGn2fit_map]
                y_std2fit_unknwGn= y_std_unknwGn[y_unknwGn2fit_map]
                #
                if cleanMemFlag: del y_knownGn2fit_map; del y_unknwGn2fit_map;
                #
                if (len(y_knownGn2fit)>=minNpoints2fit) & (len(y_unknwGn2fit)>=minNpoints2fit):
                    (knownGn_slope, knownGn_offset)= APy3_FITfuns.linear_fit(x_knownGn2fit,y_knownGn2fit)
                    knownGn_R2=                      APy3_FITfuns.linear_fit_R2(x_knownGn2fit,y_knownGn2fit)
                    (unknwGn_slope, unknwGn_offset)= APy3_FITfuns.linear_fit(x_unknwGn2fit,y_unknwGn2fit)
                    unknwGn_R2=                      APy3_FITfuns.linear_fit_R2(x_unknwGn2fit,y_unknwGn2fit)
                    #
                    if ((knownGn_slope<minslope2fit)|(unknwGn_slope<minslope2fit)): 
                        if verboseFlag: APy3_GENfuns.printcol("bad fit: slope=({0},{1})ADU/ms < {2}ADU/ms".format(knownGn_slope,unknwGn_slope, minslope2fit),'orange')
                    #
                    elif (knownGn_R2>=minR22fit) & (unknwGn_R2>=minR22fit):
                        unknwGn_ADU2e[thisRow,thisCol]= knownGn_ADU2e[thisRow,thisCol] * (knownGn_slope/unknwGn_slope)
                        unknwGn_ADU0[thisRow,thisCol]=  unknwGn_offset
                        if verboseFlag: 
                            APy3_GENfuns.printcol("pix({0},{1}):".format(thisRow,thisCol),'green')
                            APy3_GENfuns.printcol("  Gn{0}: {1}steps, fit_slope={2}ADU/ms,fit_intercept={3}ADU,R2={4}, e/ADU:{5}".format(Gn_to_calculate-1, len(x_knownGn2fit),knownGn_slope, knownGn_offset, knownGn_R2, round(knownGn_ADU2e[thisRow,thisCol],3) ),'green')
                            APy3_GENfuns.printcol("  Gn{0}: {1}steps, fit_slope={2}ADU/ms,fit_intercept={3}ADU,R2={4}, e/ADU:{5}, offset:{6}ADU".format(Gn_to_calculate, len(x_unknwGn2fit), unknwGn_slope, unknwGn_offset, unknwGn_R2, round(unknwGn_ADU2e[thisRow,thisCol],3), round(unknwGn_ADU0[thisRow,thisCol],3) ),'green')
                        #
                        if (debugFlag & (~saveInsteadOfPlotting_Flag)):
                            if (Gn_to_calculate==1): 
                                #
                                APy3_GENfuns.plot_errbar_1Dx3_samecanva(x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                                                        y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                                                        x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                                                        y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                                                        [],[],[],'Gn2',
                                                                        'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False )
                                APy3_GENfuns.plot_errbar_1Dx3_samecanva(x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                                                        y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                                                        x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                                                        y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                                                        [],[],[],'Gn2',
                                                                        'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), True )
                                APy3_GENfuns.show_it()

                            else: 
                                APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                                                        x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                                                        y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                                                        x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                                                        y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                                                        'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False )
                                APy3_GENfuns.plot_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                                                        x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                                                        y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                                                        x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                                                        y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                                                        'tint [ms]','reconstructed output [e]', '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), True )
                            APy3_GENfuns.show_it()



                        elif (debugFlag & saveInsteadOfPlotting_Flag):
                            aux_png= '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol)
                            if (Gn_to_calculate==1):
                                png_errbar_1Dx3_samecanva(
                                           x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                           y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                           x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                           y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                           [],[],[],'Gn2',
                                           'tint [ms]','reconstructed output [e]',
                                           aux_png, False, saveInsteadOfPlotting_Folder+aux_png+'_fit_Lin'+'.png')

                                png_errbar_1Dx3_samecanva(
                                           x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                           y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                           x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                           y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                           [],[],[],'Gn2',
                                           'tint [ms]','reconstructed output [e]', 
                                           aux_png, True, saveInsteadOfPlotting_Folder+aux_png+'_fit_Log'+'.png')
                            else:
                                png_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                           x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                           y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                           x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                           y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                           'tint [ms]','reconstructed output [e]', 
                                           aux_png, False, saveInsteadOfPlotting_Folder+aux_png+'_fit_Lin'+'.png')
                                png_errbar_1Dx3_samecanva([],[],[],'Gn0',
                                           x_knownGn, (y_knownGn-knwGn_ADU0[thisRow,thisCol])*knownGn_ADU2e[thisRow,thisCol], 
                                           y_std_knownGn*knownGn_ADU2e[thisRow,thisCol], 'Gn{0}'.format(Gn_to_calculate-1), 
                                           x_unknwGn, (y_unknwGn-unknwGn_ADU0[thisRow,thisCol])*unknwGn_ADU2e[thisRow,thisCol],
                                           y_std_unknwGn*unknwGn_ADU2e[thisRow,thisCol],'Gn{0}'.format(Gn_to_calculate),
                                           'tint [ms]','reconstructed output [e]', 
                                           aux_png, True, saveInsteadOfPlotting_Folder+aux_png+'_fit_Log'+'.png')
                            APy3_GENfuns.printcol("png saved: "+saveInsteadOfPlotting_Folder+aux_png+'_fit_Lin/LogLog'+'.png','blue')
                        #
                    elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2}: R^2={3}; Gn{4}: R^2={5}; insufficient fit quality".format(thisRow,thisCol, Gn_to_calculate-1,knownGn_R2, Gn_to_calculate,unknwGn_R2),'orange')
                elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2} or Gn{3}: not enough points to fit".format(thisRow,thisCol, Gn_to_calculate-1, Gn_to_calculate),'orange')
                #
                if cleanMemFlag: del y_knownGn; del x_knownGn; del y_unknwGn; del x_unknwGn
                #
            elif verboseFlag: APy3_GENfuns.printcol("pix({0},{1}), Gn{2} or Gn{3}: not enough points to fit".format(thisRow,thisCol, Gn_to_calculate-1, Gn_to_calculate),'orange')
            #
            e_per_ADU_multiGn[Gn_to_calculate]=   unknwGn_ADU2e
            PedestalADU_multiGn[Gn_to_calculate]= unknwGn_ADU0
#
if (showFlag & fitFlag & (~saveInsteadOfPlotting_Flag)):
    for iGn in range(3):
        APy3_GENfuns.plot_2D_all(e_per_ADU_multiGn[iGn], False, 'col','row',  "{0}, Gn{1}: e/ADU".format(plotLabel,iGn), True)
        APy3_GENfuns.plot_2D_all(PedestalADU_multiGn[iGn], False, 'col','row',"{0}, Gn{1}: pedestal [ADU]".format(plotLabel,iGn), True)
    APy3_GENfuns.show_it()
elif (showFlag & fitFlag & saveInsteadOfPlotting_Flag):
    for iGn in range(3):
        aux_png= "{0}, Gn{1} e per ADU".format(plotLabel,iGn)
        png_2D_all(e_per_ADU_multiGn[iGn], False, 'col','row',aux_png, True, saveInsteadOfPlotting_Folder+aux_png+'.png')
        aux_png="{0}, Gn{1} pedestal ADU".format(plotLabel,iGn)
        png_2D_all(PedestalADU_multiGn[iGn], False, 'col','row',aux_png, True, saveInsteadOfPlotting_Folder+aux_png+'.png')
    APy3_GENfuns.printcol("png saved in"+saveInsteadOfPlotting_Folder,'green')

#---
if saveFlag:
    APy3_GENfuns.write_2xh5(file_out, 
           PedestalADU_multiGn, '/Pedestal_ADU/', 
           e_per_ADU_multiGn, '/e_per_ADU/')
    APy3_GENfuns.printcol("data saved in {0} under /Pedestal_ADU/ , /e_per_ADU/".format(file_out),'green')
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

