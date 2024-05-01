# -*- coding: utf-8 -*-
"""
sweep of avgs => show in e 

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
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#%% functions

INTERACTIVElist= ['i','I','interactive','Interactive','INTERACTIVE']

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

def png_errbar_1Dx3_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, arrayX3,arrayY3,errbarY3,legend3, label_x,label_y, label_title, loglogFlag, filenamepath):
    """ 3x 1D scatter plot (+errbars) in the same canva: save to png """
    #
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
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
'''
######### BSI04 PGABBB BSI04_04, Gn0->1 v1 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_std_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5'
#
dflt_altPedestalGn0= dflt_folder_data2process+ 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD1.0_t012ms_100drk_Gn0_ADU_CDS_avg.h5'
dflt_altPedestalGn0= 'NONE'
#
dflt_Row2proc='i'; dflt_Col2proc='i'; #dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_pngFolder='/home/marras/auximg/'
dflt_plotLabel= "BSI04,PGABBB"
dflt_Gn0Label= "high-gain"
dflt_Gn1Label= "medium-gain"
dflt_Gn2Label= "low-gain"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
#
'''
######### PO4 2019.12, BSI04,3G PGABB #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/processed/2019.12.12.02.44.10_5um_275eV/LinScan_3of7ADC_3GPGABBB/avg_xGn_3/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.12.12_BSI04_3of7_3GPGABBB_0275eV_5um_Linscan_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file='2019.12.12_BSI04_3of7_3GPGABBB_0275eV_5um_Linscan_std_meta.dat' 
#dflt_meta_std_file='NONE' 
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5'
dflt_altPedestalGn0= dflt_folder_data2process+ '2019.12.12.04.07.29_BSI04_3of7_3GPGABBB_012ms_0275eV_5um_1kdrk_Gn0_ADU_CDS_avg.h5'
#
dflt_Row2proc='i'; dflt_Col2proc='i'; #dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
#dflt_pngFolder='/home/marras/auximg/'
dflt_pngFolder='NONE'

dflt_plotLabel= "BSI04,PGABBB"
dflt_Gn0Label= "high-gain"
dflt_Gn1Label= "medium-gain"
dflt_Gn2Label= "low-gain"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
#### BSI04 PGABBB BSI04_04, Gn0->1 v2 ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD4.0_std_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
#
#dflt_altPedestalGn0= dflt_folder_data2process+ 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_ODx.x_t012ms_30drk_Gn0_ADU_CDS_avg.h5'
dflt_altPedestalGn0= 'NONE'
#
dflt_Row2proc='i'; dflt_Col2proc='i'; #dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_pngFolder='/home/marras/auximg/'
dflt_pngFolder='NONE'
#
dflt_plotLabel= "BSI04,PGABBB"
dflt_Gn0Label= "high-gain"
dflt_Gn1Label= "medium-gain"
dflt_Gn2Label= "low-gain"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######### BSI04 PGA6BB biasBSI04_05, Gn0->1->2 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
#Gn0->1
dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD6.0_sigma_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
#Gn1->2
#dflt_meta_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_std_file= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5"
#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal_gapsAvg.h5"
#
dflt_altPedestalGn0= 'NONE'
#dflt_altPedestalGn0= dflt_folder_data2process+ 'BSI04_Tm20_3of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk_Gn0_ADU_CDS_avg.h5'
#
dflt_Row2proc='i'; dflt_Col2proc='i'; #dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_pngFolder='/home/marras/auximg/'
dflt_pngFolder='NONE'
#
dflt_plotLabel= "BSI04,PGA6BB"
dflt_Gn0Label= "high-gain"
dflt_Gn1Label= "medium-gain"
dflt_Gn2Label= "low-gain"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#'''
#
#
#'''
######### BSI04 7/7 PGA6BB biasBSI04_05, Gn0->1->2 #################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
#Gn0->1
#dflt_meta_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_std_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_sigma_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD4.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_std_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD4.0_sigma_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#
#Gn1->2
# tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_file=     'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
#dflt_meta_std_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_sigma_meta.dat'
dflt_meta_file=     'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD2.0_avg_meta.dat' # tint<\tab>filenameGn0<\tab>filenameGn1<\tab>filenameGn0
dflt_meta_std_file= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD2.0_sigma_meta.dat'

#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"

#
dflt_altPedestalGn0= 'NONE'
#dflt_altPedestalGn0= xxx
#
dflt_Row2proc='i'; dflt_Col2proc='i'; #dflt_Row2proc='801:801'; dflt_Col2proc='700:700'#dflt_Row2proc=':'; dflt_Col2proc=':'
#
dflt_pngFolder='/home/marras/auximg/'
dflt_pngFolder='NONE'
#
dflt_plotLabel= "BSI04,7of7ADC,3G,PGA6BB"
dflt_Gn0Label= "high-gain"
dflt_Gn1Label= "medium-gain"
dflt_Gn2Label= "low-gain"
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
GUIwin_arguments+= ['process data: avg metafile'] 
GUIwin_arguments+= [dflt_meta_file] 
GUIwin_arguments+= ['process data: std metafile'] 
GUIwin_arguments+= [dflt_meta_std_file] 
#
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]

GUIwin_arguments+= ['alternate PedestalADU for Gn0: file [NONE not to use]']
GUIwin_arguments+= [dflt_altPedestalGn0]
#
GUIwin_arguments+= ['process data: in Rows [from:to / interactive]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['process data: in Cols [from:to / interactive]'] 
GUIwin_arguments+= [dflt_Col2proc]
#
GUIwin_arguments+= ['save png instead of showing: folder [NONE noto to do it]']
GUIwin_arguments+= [str(dflt_pngFolder)]
GUIwin_arguments+= ['plot label'] 
GUIwin_arguments+= [dflt_plotLabel]
#
GUIwin_arguments+= ['plot: Gn0 legend id']
GUIwin_arguments+= [dflt_Gn0Label]
GUIwin_arguments+= ['plot: Gn1 legend id']
GUIwin_arguments+= [dflt_Gn1Label]
GUIwin_arguments+= ['plot: Gn2 legend id']
GUIwin_arguments+= [dflt_Gn2Label]
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
if meta_std_file in APy3_GENfuns.NOlist: errbFlag=False
else: errbFlag=True
#
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
altPedestalGn0_file= dataFromUser[i_param]; i_param+=1;
if altPedestalGn0_file in APy3_GENfuns.NOlist: altPedestalGn0_Flag=False
else: altPedestalGn0_Flag=True
#
Row2proc_mtlb= dataFromUser[i_param]; i_param+=1;
Col2proc_mtlb= dataFromUser[i_param]; i_param+=1;
  
if ((Row2proc_mtlb in INTERACTIVElist)|(Col2proc_mtlb in INTERACTIVElist)):
    interactiveShowFlag= True
    Row2proc= numpy.arange(1); Col2proc=numpy.arange(1);
else:
    interactiveShowFlag= False
    Row2proc=APy3_P2Mfuns.matlabLike_Row(Row2proc_mtlb)
    Col2proc=APy3_P2Mfuns.matlabLike_Row(Col2proc_mtlb)
#
pngFolder= dataFromUser[i_param]; i_param+=1;
if (pngFolder in APy3_GENfuns.NOlist): pngFlag= False
else: pngFlag= True
plotLabel= dataFromUser[i_param]; i_param+=1;
#
Gn0Label= dataFromUser[i_param]; i_param+=1;
Gn1Label= dataFromUser[i_param]; i_param+=1;
Gn2Label= dataFromUser[i_param]; i_param+=1;
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
    if errbFlag: APy3_GENfuns.printcol('  using std metafile {0}'.format(meta_std_file),'blue') 
    #
    APy3_GENfuns.printcol('will take multiGnCal values from {0}'.format(multiGnCal_file),'blue')
    if altPedestalGn0_Flag: APy3_GENfuns.printcol('will take Gn0 Pedestal ADU values from {0}'.format(altPedestalGn0_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate pix({0},{1})'.format(Row2proc_mtlb,Col2proc_mtlb),'blue')
    #
    if pngFlag: APy3_GENfuns.printcol('  instead of showing plots, will save plot to '+pngFolder,'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
APy3_GENfuns.printcol("script starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
# ---
#
APy3_GENfuns.printcol('loading meta-file and calibr-files','blue')
#
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
#
if altPedestalGn0_Flag: 
    if APy3_GENfuns.notFound(altPedestalGn0_file): APy3_GENfuns.printErr('not found: '+altPedestalGn0_file)
    PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(altPedestalGn0_file, '/data/data')
#
if APy3_GENfuns.notFound(folder_data2process+meta_file): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_file)
meta_content= APy3_GENfuns.read_tst(folder_data2process+meta_file)
meta_tintAr= meta_content[:,0].astype(float)
meta_Nfiles= len(meta_tintAr)
if verboseFlag: APy3_GENfuns.printcol("{0} entries in the metafile".format(meta_Nfiles),'green')
meta_fileNameList = [[] for y in range(3)]
for jGn in range(3):
    meta_fileNameList[jGn]= meta_content[:,jGn+1]  #+1 because the 1ts col is tint
#
allData_tint= numpy.array(meta_tintAr)
allData_ADU_avg= APy3_GENfuns.numpy_NaNs((3,meta_Nfiles,NRow,NCol))
allData_ADU_std= APy3_GENfuns.numpy_NaNs((3,meta_Nfiles,NRow,NCol))
#
if errbFlag:
    if APy3_GENfuns.notFound(folder_data2process+meta_std_file): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_std_file)
    meta_std_content= APy3_GENfuns.read_tst(folder_data2process+meta_std_file)
    if len(meta_std_content[:,0])!=meta_Nfiles: APy3_GENfuns.printErr('avg metafile entries {0} != std metafile entries {0}'.format(meta_Nfiles,meta_std_content[:,0])) 
    meta_std_fileNameList = [[] for y in range(3)]
    for jGn in range(3):
        meta_std_fileNameList[jGn]= meta_std_content[:,jGn+1] #+1 because the 1ts col is tint
#
APy3_GENfuns.printcol("reading files",'blue')
for iFile in range(meta_Nfiles):
    for jGn in range(3):
        thisFile= meta_fileNameList[jGn][iFile]
        if APy3_GENfuns.notFound(folder_data2process+thisFile): APy3_GENfuns.printErr('not found: '+folder_data2process+thisFile)
        allData_ADU_avg[jGn,iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+thisFile, '/data/data')
        #
        if errbFlag:
            if APy3_GENfuns.notFound(folder_data2process+meta_std_fileNameList[jGn][iFile]): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_std_fileNameList[jGn][iFile]) 
            allData_ADU_std[jGn,iFile,:,:]= APy3_GENfuns.read_1xh5(folder_data2process+meta_std_fileNameList[jGn][iFile], '/data/data')
    #
    APy3_GENfuns.dot_every10th(iFile,meta_Nfiles)
    #
#---
#%% elab data
APy3_GENfuns.printcol("elaborating pixel data",'blue')
allData_e_avg= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
allData_e_std= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
allData_trackGn= numpy.zeros((meta_Nfiles,NRow,NCol)).astype(int)-1

for jGn in range(3): 
    auxvals_thisGn= APy3_GENfuns.numpy_NaNs((meta_Nfiles,NRow,NCol))
    auxvals_thisGn[:,:,:]= (allData_ADU_avg[jGn,:,:,:] - PedestalADU_multiGn[jGn,:,:])*e_per_ADU_multiGn[jGn,:,:]
    auxmap_thisGn= ~numpy.isnan(auxvals_thisGn)
    allData_e_avg[auxmap_thisGn]= auxvals_thisGn[auxmap_thisGn]
    allData_trackGn[auxmap_thisGn]= jGn
    #
    allData_e_std[auxmap_thisGn]= ((allData_ADU_std[jGn,:,:,:])*e_per_ADU_multiGn[jGn,:,:])[auxmap_thisGn]
    del auxvals_thisGn; del  auxmap_thisGn
#print('{0},{1}'.format(allData_e_avg.shape,allData_trackGn.shape))
#if cleanMemFlag: del allData_ADU_avg; del allData_ADU_std 
# ---
if interactiveShowFlag:
    APy3_GENfuns.printcol("show/saving pixel data interactively",'blue')

    thisRow=0;thisCol=0

    APy3_GENfuns.printcol("plot [R]amps / [E]nd plotting", 'black')
    nextstep= APy3_GENfuns.press_any_key()
    while nextstep not in ['e','E','q','Q']:
        if nextstep in ['r','R']:

            APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'black'); thisRow_str= input(); 
            if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
            APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'black'); thisCol_str= input(); 
            if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
            APy3_GENfuns.printcol("plotting/saving ramp pix ({0},{1})".format(thisRow,thisCol), 'blue')
            #
            Gn0map= allData_trackGn[:,thisRow,thisCol]==0
            Gn0Data_tint = allData_tint[ Gn0map]
            Gn0Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn0map]
            Gn0Data_e_std= allData_e_std[:,thisRow,thisCol][Gn0map]
            #
            Gn1map= allData_trackGn[:,thisRow,thisCol]==1
            Gn1Data_tint = allData_tint[ Gn1map]
            Gn1Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn1map]
            Gn1Data_e_std= allData_e_std[:,thisRow,thisCol][Gn1map]
            #
            Gn2map= allData_trackGn[:,thisRow,thisCol]==2
            Gn2Data_tint = allData_tint[ Gn2map]
            Gn2Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn2map]
            Gn2Data_e_std= allData_e_std[:,thisRow,thisCol][Gn2map]
            #
            #APy3_GENfuns.printcol("{0},{1},{2}".format(Gn0Data_tint.shape, Gn1Data_tint.shape, Gn2Data_tint.shape ), 'blue')
            #APy3_GENfuns.printcol("{0},{1},{2}".format(Gn0Data_e_avg.shape,Gn1Data_e_avg.shape,Gn2Data_e_avg.shape), 'blue')
            #APy3_GENfuns.printcol("{0},{1},{2}".format(Gn0Data_e_std.shape,Gn1Data_e_std.shape,Gn2Data_e_std.shape), 'blue')


            #
            auxTitle=plotLabel+" pix({0},{1})".format(thisRow,thisCol) 
            #
            if pngFlag:
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, False,
                                  pngFolder+auxTitle+'_Lin')
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, True,
                                  pngFolder+auxTitle+'_Log')
                APy3_GENfuns.printcol("png saved to "+pngFolder,'green')                                 
            else:
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, False)
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, True)
                APy3_GENfuns.showIt()
            #
            del Gn0map; del Gn0Data_tint; del Gn0Data_e_avg; del Gn0Data_e_std
            del Gn1map; del Gn1Data_tint; del Gn1Data_e_avg; del Gn1Data_e_std
            del Gn2map; del Gn2Data_tint; del Gn2Data_e_avg; del Gn2Data_e_std
            #
        #
        elif nextstep in ['a','A']:
            APy3_GENfuns.printcol("Easter Egg! ramp in ADU", 'green')
            #
            APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'black'); thisRow_str= input();
            if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
            APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'black'); thisCol_str= input();
            if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
            APy3_GENfuns.printcol("plotting/saving ramp pix ({0},{1})".format(thisRow,thisCol), 'blue')
            #
            PedSubData_ADU_avg= APy3_GENfuns.numpy_NaNs((3,meta_Nfiles,NRow,NCol))
            for jGn in range(3):
                PedSubData_ADU_avg[jGn,:,:,:]=  (allData_ADU_avg[jGn,:,:,:] - PedestalADU_multiGn[jGn,:,:])
            Gn0map= allData_trackGn[:,thisRow,thisCol]==0
            Gn0Data_tint = allData_tint[ Gn0map]
            Gn0Data_ADU_avg= PedSubData_ADU_avg[0,:,thisRow,thisCol][Gn0map]
            Gn0Data_ADU_std= allData_ADU_std[0,:,thisRow,thisCol][Gn0map]
            #
            Gn1map= allData_trackGn[:,thisRow,thisCol]==1
            Gn1Data_tint = allData_tint[ Gn1map]
            Gn1Data_ADU_avg= PedSubData_ADU_avg[1,:,thisRow,thisCol][Gn1map]
            Gn1Data_ADU_std= allData_ADU_std[1,:,thisRow,thisCol][Gn1map]
            #
            Gn2map= allData_trackGn[:,thisRow,thisCol]==2
            Gn2Data_tint = allData_tint[ Gn2map]
            Gn2Data_ADU_avg= PedSubData_ADU_avg[2,:,thisRow,thisCol][Gn2map]
            Gn2Data_ADU_std= allData_ADU_std[2,:,thisRow,thisCol][Gn2map]
            #
            auxTitle=plotLabel+" pix({0},{1})".format(thisRow,thisCol)
            if pngFlag:
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_ADU_avg,Gn0Data_ADU_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_ADU_avg,Gn1Data_ADU_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_ADU_avg,Gn2Data_ADU_std,Gn2Label,
                                  'integration time [ms]','detector output [ADU]', auxTitle, False,
                                  pngFolder+auxTitle+'_Lin')
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_ADU_avg,Gn0Data_ADU_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_ADU_avg,Gn1Data_ADU_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_ADU_avg,Gn2Data_ADU_std,Gn2Label,
                                  'integration time [ms]','detector output [ADU]', auxTitle, True,
                                  pngFolder+auxTitle+'_Log')
                APy3_GENfuns.printcol("png saved to "+pngFolder,'green')
            else:
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_ADU_avg,Gn0Data_ADU_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_ADU_avg,Gn1Data_ADU_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_ADU_avg,Gn2Data_ADU_std,Gn2Label,
                                  'integration time [ms]','detector output [ADU]', auxTitle, False)
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_ADU_avg,Gn0Data_ADU_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_ADU_avg,Gn1Data_ADU_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_ADU_avg,Gn2Data_ADU_std,Gn2Label,
                                  'integration time [ms]','detectro output [ADU]', auxTitle, True)
                APy3_GENfuns.showIt()
            #
            del Gn0map; del Gn0Data_tint; del Gn0Data_ADU_avg; del Gn0Data_ADU_std
            del Gn1map; del Gn1Data_tint; del Gn1Data_ADU_avg; del Gn1Data_ADU_std
            del Gn2map; del Gn2Data_tint; del Gn2Data_ADU_avg; del Gn2Data_ADU_std
            #
            del PedSubData_ADU_avg

        #
        elif nextstep in ['#']:
            APy3_GENfuns.printcol("Easter Egg list:", 'green')
            APy3_GENfuns.printcol("A : ramp in ADUi",'green')
        #
        APy3_GENfuns.printcol("plot [R]amps / [E]nd ", 'black')
        nextstep= APy3_GENfuns.press_any_key()
        if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
#
else: 
    APy3_GENfuns.printcol("show/saving pixel data in ({0}:{1})".format(Row2proc_mtlb,Col2proc_mtlb),'blue')
    for thisRow in Row2proc:
        for thisCol in Col2proc:
            Gn0map= allData_trackGn[:,thisRow,thisCol]==0
            Gn0Data_tint = allData_tint[ Gn0map]
            Gn0Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn0map]
            Gn0Data_e_std= allData_e_std[:,thisRow,thisCol][Gn0map]
            #
            Gn1map= allData_trackGn[:,thisRow,thisCol]==1
            Gn1Data_tint = allData_tint[ Gn1map]
            Gn1Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn1map]
            Gn1Data_e_std= allData_e_std[:,thisRow,thisCol][Gn1map]
            #
            Gn2map= allData_trackGn[:,thisRow,thisCol]==2
            Gn2Data_tint = allData_tint[ Gn2map]
            Gn2Data_e_avg= allData_e_avg[:,thisRow,thisCol][Gn2map]
            Gn2Data_e_std= allData_e_std[:,thisRow,thisCol][Gn2map]

            auxTitle=plotLabel+" pix({0},{1})".format(thisRow,thisCol)
            #
            if pngFlag:
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, False,
                                  pngFolder+auxTitle+'_Lin')
                png_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, True,
                                  pngFolder+auxTitle+'_Log')
                APy3_GENfuns.printcol("png saved to "+pngFolder,'green')
            else:
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, False)
                APy3_GENfuns.plot_errbar_1Dx3_samecanva(Gn0Data_tint,Gn0Data_e_avg,Gn0Data_e_std,Gn0Label,
                                  Gn1Data_tint,Gn1Data_e_avg,Gn1Data_e_std,Gn1Label,
                                  Gn2Data_tint,Gn2Data_e_avg,Gn2Data_e_std,Gn2Label,
                                  'integration time [ms]','collected charge [e]', auxTitle, True)
                APy3_GENfuns.showIt()
            #
            del Gn0map; del Gn0Data_tint; del Gn0Data_e_avg; del Gn0Data_e_std
            del Gn1map; del Gn1Data_tint; del Gn1Data_e_avg; del Gn1Data_e_std
            del Gn2map; del Gn2Data_tint; del Gn2Data_e_avg; del Gn2Data_e_std
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

