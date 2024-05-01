# -*- coding: utf-8 -*-
"""
set 3x.h5 of avg (xGn) light at different int times => eval charge to be used as x in multign plot

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
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---

INTERACTLVElist= ['i','I','interactive','Interactive','INTERACTIVE']

def read_warn_1xh5(filenamepath, path_2read):
    if APy3_GENfuns.notFound(filenamepath): APy3_GENfuns.printErr("not found: "+filenamepath)
    dataout= APy3_GENfuns.read_1xh5(filenamepath, path_2read)
    return dataout

def plot_errbar(arrayX1,arrayY1,errbarY1, label_x,label_y, label_title, loglogFlag):
    """ scatter plot (+errbars)""" 
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)
#---
#
#%% defaults for GUI window
#
#
'''
#### BSI04, T-20, dmuxSELHigh, biasBSI04_05, Lat Oflw PGA6BB ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
# tab-separated-text file: integr_time_in_ms<tab>Gn0_avg<tab>Gn1_avg<tab>Gn2_avg (same used for extraction)
dflt_metaFileName= 'BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_OD3.0_avg_meta.dat' #also OD1,2,3,4,5,6.0
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5"
#
dflt_alternPed_file='NONE'
#dflt_alternPed_file=dflt_folder_data2process+"BSI04_Tm20_3of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk_Gn0_ADU_CDS_avg.h5"
#
dflt_Rows2proc='0:1483'
dflt_Cols2proc='32:1439'
#dflt_Rows2proc='Interactive'  
#dflt_Cols2proc='Interactive' 
#
dflt_showFlag='Y'; dflt_showFlag='N'
#
dflt_fitFlag='Y'; #dflt_fitFlag='N'
dflt_fit_maxADU=0.9 #up to 90% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=4 #10 #4pt for having 2ke v.high-> med gn pixels
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_saveFolder=dflt_folder_data2process+'../fitCollCharge/'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
#'''
#
#
#'''
#### BSI04, T-20, 7/7, biasBSI04_05, Lat Oflw PGA6BB ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
# tab-separated-text file: integr_time_in_ms<tab>Gn0_avg<tab>Gn1_avg<tab>Gn2_avg (same used for extraction)
dflt_metaFileName= 'BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_OD5.0_avg_meta.dat' #also OD2,3,4,5.0
#
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"
#
dflt_alternPed_file='NONE'
#dflt_alternPed_file=dflt_folder_data2process+"BSI04_Tm20_3of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk_Gn0_ADU_CDS_avg.h5"
#
dflt_Rows2proc='0:1483'
dflt_Cols2proc='32:1439'
#dflt_Rows2proc='Interactive'  
#dflt_Cols2proc='Interactive' 
#
dflt_showFlag='Y'; dflt_showFlag='N'
#
dflt_fitFlag='Y'; #dflt_fitFlag='N'
dflt_fit_maxADU=0.9 #up to 90% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=4 #10 #4pt for having 2ke v.high-> med gn pixels
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_saveFolder=dflt_folder_data2process+'../fitCollCharge/'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
#'''
#
#
# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
#
GUIwin_arguments+= ['use data from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['metadata file (tint<tab>Gn0_avg<tab>Gn1_avg<tab>Gn2_avg)'] 
GUIwin_arguments+= [dflt_metaFileName] 
#
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
GUIwin_arguments+= ['alternate PedestalADU (Gn0) file [NONE not to use]'] 
GUIwin_arguments+= [dflt_alternPed_file]
#
GUIwin_arguments+= ['process data: in Rows [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Rows2proc]
GUIwin_arguments+= ['process data: in columns [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
#
GUIwin_arguments+= ['show results? [Y/N]']
GUIwin_arguments+= [dflt_showFlag] 
#
GUIwin_arguments+= ['fit e/ms? [Y/N]']
GUIwin_arguments+= [dflt_fitFlag]
GUIwin_arguments+= ['fit: (to avoid saturation): use up to x of the max ADU [between 0 and 1]']
GUIwin_arguments+= [dflt_fit_maxADU]
GUIwin_arguments+= ['fit: R2 at least?']
GUIwin_arguments+= [dflt_fit_minR2]
GUIwin_arguments+= ['fit: at least on how many points?']
GUIwin_arguments+= [dflt_fit_minNpoints]
#
GUIwin_arguments+= ['save estimated (fitted) charge? [Y/N]']
GUIwin_arguments+= [dflt_saveFlag]
GUIwin_arguments+= ['if save: folder']
GUIwin_arguments+= [dflt_saveFolder]
#
GUIwin_arguments+= ['high memory usage? [Y/N]']
GUIwin_arguments+= [str(dflt_highMemFlag)] 
GUIwin_arguments+= ['clean memory when possible? [Y/N]']
GUIwin_arguments+= [str(dflt_cleanMemFlag)] 
GUIwin_arguments+= ['verbose? [Y/N]']
GUIwin_arguments+= [str(dflt_verboseFlag)]
# ---
#
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0

folder_data2process= dataFromUser[i_param]; i_param+=1
metaFileName= dataFromUser[i_param]; i_param+=1

multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
alternPed_file= dataFromUser[i_param]; i_param+=1;
if alternPed_file in APy3_GENfuns.NOlist: alternPed_flag=False
else: alternPed_flag=True

Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if (Rows2proc_mtlb in INTERACTLVElist) or  (Cols2proc_mtlb in INTERACTLVElist):
    interactiveShowFlag=True
    Rows2proc_mtlb= 'Interactive'; Cols2proc_mtlb= 'Interactive'
    Rows2proc=numpy.arange(NRow); Cols2proc=numpy.arange(NCol)
else:
    interactiveShowFlag=False
    if Rows2proc_mtlb in APy3_GENfuns.ALLlist: Rows2proc= numpy.arange(NRow)
    else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 
    if Cols2proc_mtlb in APy3_GENfuns.ALLlist: Cols2proc= numpy.arange(32,NCol)
    else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
fitFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
fit_maxADU=float(dataFromUser[i_param]); i_param+=1
fit_minR2=float(dataFromUser[i_param]); i_param+=1
fit_minNpoints=float(dataFromUser[i_param]); i_param+=1
#
saveFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
saveFolder=dataFromUser[i_param]; i_param+=1;  
#

#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
if True:
    APy3_GENfuns.printcol('will process data from '+folder_data2process,'blue')
    APy3_GENfuns.printcol('will use {0} as the index file'.format(metaFileName),'blue')

    APy3_GENfuns.printcol('using e/ADU data from {0}'.format(multiGnCal_file),'blue')
    if alternPed_flag: APy3_GENfuns.printcol('  assuming Pedestal[ADU] from {0}'.format(alternPed_file),'blue')
    else: APy3_GENfuns.printcol('using Pedestal[ADU] from {0}'.format(multiGnCal_file),'blue')

    APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}'.format(Cols2proc_mtlb,Rows2proc_mtlb),'blue')

    if showFlag: APy3_GENfuns.printcol('will plot ramps','blue')

    if fitFlag: 
        APy3_GENfuns.printcol('will fit e/ms, using (ped-sub) ADUs <= {0} of max'.format(fit_maxADU),'blue')
        APy3_GENfuns.printcol('will considerate an acceptable fit if R2>={0}, Npoints>={1}'.format(fit_minR2,fit_minNpoints),'blue')
        if saveFlag: APy3_GENfuns.printcol('will save estimated (fitted) collected charge in {0}'.format(saveFolder),'blue')

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
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
#---
#% read param file
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
APy3_GENfuns.printcol("multiGnCal file read",'blue')
if alternPed_flag:
    if APy3_GENfuns.notFound(alternPed_file): APy3_GENfuns.printErr('not found: '+alternPed_file)
    PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(alternPed_file, '/data/data')
    APy3_GENfuns.printcol("alternate pedestal file read",'blue')
#---
#% read metadata file
APy3_GENfuns.printcol("reading metadata file",'blue')
if APy3_GENfuns.notFound(folder_data2process+metaFileName): APy3_GENfuns.printErr("not found: "+folder_data2process+metaFileName)
fileList_all= APy3_GENfuns.read_tst(folder_data2process+metaFileName)
(NSets,N4)= numpy.array(fileList_all).shape
if N4!=4: APy3_GENfuns.printErr("metafile: {0} columns (4 expected)".format(N4))
elif verboseFlag: APy3_GENfuns.printcol("{0} Sets in metafile".format(NSets),'green')
#---
#% read data files
APy3_GENfuns.printcol("reading avg files",'blue')

intTimes_ms=[]
for iSet in range(NSets):
    intTimes_ms+= [float(fileList_all[iSet][0])]
intTimes_ms= numpy.array(intTimes_ms)

alldata_ADU_4DAr= APy3_GENfuns.numpy_NaNs((3,NSets,NRow,NCol))
alldata_e_4DAr= APy3_GENfuns.numpy_NaNs((3,NSets,NRow,NCol))

for iSet in range(NSets):
    for jGn in range(3):
        alldata_ADU_4DAr[jGn,iSet,:,:]= read_warn_1xh5(folder_data2process+fileList_all[iSet][jGn+1], '/data/data') #jGn+1 because Gn0 is col 1, ...

for jGn in range(3):
    alldata_ADU_4DAr[jGn,:,:,:]= numpy.copy(alldata_ADU_4DAr[jGn,:,:,:] - PedestalADU_multiGn[jGn,:,:])  
    alldata_e_4DAr[jGn,:,:,:]=   numpy.copy(alldata_ADU_4DAr[jGn,:,:,:]*e_per_ADU_multiGn[jGn,:,:])
#---
#% show ramps
if (showFlag & (~interactiveShowFlag)): 
    if verboseFlag: APy3_GENfuns.printcol("showing ramps",'blue')
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            for jGn in range(3):
                APy3_GENfuns.plot_1D(intTimes_ms, alldata_ADU_4DAr[jGn,:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]','({0},{1}),Gn{2}'.format(thisRow,thisCol,jGn))
                APy3_GENfuns.plot_1D(intTimes_ms, alldata_e_4DAr[jGn,:,thisRow,thisCol], 'integration time [ms]','collected charge [e]','({0},{1}),Gn{2}'.format(thisRow,thisCol,jGn))
            APy3_GENfuns.showIt()
#
elif (showFlag & interactiveShowFlag): 
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("interactivly showing ramps",'blue')
    APy3_GENfuns.printcol("[P]lot/[F]it ramp / [Q]uit",'green')
    nextstep= input()
    while (nextstep not in ['q','Q']):
        #
        if (nextstep in ['p','P']):
            APy3_GENfuns.printcol("plot pixel: Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("plot pixel: Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            APy3_GENfuns.printcol("will plot pixel ({0},{1})".format(thisRow,thisCol),'green')
            for jGn in range(3):
                APy3_GENfuns.plot_1D(intTimes_ms, alldata_ADU_4DAr[jGn,:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]','({0},{1}),Gn{2}'.format(thisRow,thisCol,jGn))
                APy3_GENfuns.plot_1D(intTimes_ms, alldata_e_4DAr[jGn,:,thisRow,thisCol], 'integration time [ms]','collected charge [e]','({0},{1}),Gn{2}'.format(thisRow,thisCol,jGn))
            APy3_GENfuns.showIt()
        #
        elif (nextstep in ['f','F']):
            APy3_GENfuns.printcol("fit: pixel Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("fit: pixel Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            APy3_GENfuns.printcol("fit: max ADU (after ped-sub) to avoid saturation? [default is {0} of max]".format(fit_maxADU),'green')
            fit_maxADU_str= input()
            if len(fit_maxADU_str)>0: fit_maxADU=float(fit_maxADU_str)
            APy3_GENfuns.printcol("will fit pixel ({0},{1})".format(thisRow,thisCol),'green')
            APy3_GENfuns.printcol("will fit using ADU vals <={0} (after ped-sub)".format(fit_maxADU),'green')
            #
            for jGn in range(3):
                map2fit= alldata_ADU_4DAr[jGn,:,thisRow,thisCol]<=(fit_maxADU)*numpy.nanmax(alldata_ADU_4DAr[jGn,:,thisRow,thisCol])
                data2fit_tint= numpy.copy(intTimes_ms[map2fit])
                data2fit_e= numpy.copy(alldata_e_4DAr[jGn,:,thisRow,thisCol][map2fit])
                data2fit_ADU= numpy.copy(alldata_ADU_4DAr[jGn,:,thisRow,thisCol][map2fit])
                del map2fit
                #
                map2fit= ~numpy.isnan(data2fit_e)
                data2fit_tint= numpy.copy(data2fit_tint[map2fit])
                data2fit_e= numpy.copy(data2fit_e[map2fit])
                data2fit_ADU= numpy.copy(data2fit_ADU[map2fit])
                #
                if len(data2fit_tint)>=fit_minNpoints:
                    (fit_slope,fit_offset)= APy3_FITfuns.linear_fit(data2fit_tint,data2fit_e)
                    fit_R2= APy3_FITfuns.linear_fit_R2(data2fit_tint,data2fit_e)
                    APy3_GENfuns.printcol("Gn{4}, fit e(t): toffset={1}ms, slope={0}e/ms, R2={2}, Npoints={3}".format(fit_slope,fit_offset,fit_R2,len(data2fit_tint),jGn),'green')
                    if (fit_R2<fit_minR2): APy3_GENfuns.printcol("R2={0} < {1}".format(fit_R2,fit_minR2),'orange')
                    #APy3_GENfuns.plot_1D(APy3_FITfuns.linear_fun(intTimes_ms,fit_slope,fit_offset), alldata_ADU_4DAr[jGn,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]','({0},{1}),Gn{2}'.format(thisRow,thisCol,jGn))
                    #APy3_GENfuns.showIt()
                    #
                    del fit_slope; del fit_offset; del fit_R2
                else: APy3_GENfuns.printcol("Gn{2}, unable to fit Npoints={0}<{1}".format(len(data2fit_tint),fit_minNpoints,jGn),'orange')
                del map2fit; del data2fit_tint; del data2fit_e; del data2fit_ADU
        #
        APy3_GENfuns.printcol("[P]lot/[F]it ramp / [Q]uit",'green')
        nextstep= input()
#
#---
if fitFlag:
    APy3_GENfuns.printcol("fitting e/ms ramps",'blue')
    datafitted_e_4D= APy3_GENfuns.numpy_NaNs_like(alldata_ADU_4DAr)
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            for jGn in range(3):
                map2fit= alldata_ADU_4DAr[jGn,:,thisRow,thisCol]<=fit_maxADU*numpy.nanmax(alldata_ADU_4DAr[jGn,:,thisRow,thisCol])
                data2fit_tint= numpy.copy(intTimes_ms[map2fit])
                data2fit_e= numpy.copy(alldata_e_4DAr[jGn,:,thisRow,thisCol][map2fit])
                data2fit_ADU= numpy.copy(alldata_ADU_4DAr[jGn,:,thisRow,thisCol][map2fit])
                del map2fit
                #
                map2fit= ~numpy.isnan(data2fit_e)
                data2fit_tint= numpy.copy(data2fit_tint[map2fit])
                data2fit_e= numpy.copy(data2fit_e[map2fit])
                data2fit_ADU= numpy.copy(data2fit_ADU[map2fit])
                #

                if len(data2fit_tint)>=fit_minNpoints:
                    (fit_slope,fit_offset)= APy3_FITfuns.linear_fit(data2fit_tint,data2fit_e)
                    fit_R2= APy3_FITfuns.linear_fit_R2(data2fit_tint,data2fit_e)
                    if (fit_R2>=fit_minR2): 
                        datafitted_e_4D[jGn,:,thisRow,thisCol]= APy3_FITfuns.linear_fun(intTimes_ms,fit_slope,fit_offset)
                        aux_col='green'
                    else: aux_col='orange'
                    if verboseFlag: APy3_GENfuns.printcol("Gn{5}: pix({3},{4}): fit e(t): toffset={1}ms, slope={0}e/ms, R2={2}".format(fit_slope,fit_offset,fit_R2, thisRow,thisCol,jGn),aux_col)
                    del fit_slope; del fit_offset; del fit_R2
                #
                elif verboseFlag: APy3_GENfuns.printcol("Gn{4}: pix({2},{3}): unable to fit Npoints={0}<{1}".format(len(data2fit_tint),fit_minNpoints, thisRow,thisCol,jGn),'orange')
                del map2fit; del data2fit_tint; del data2fit_e; del data2fit_ADU
        if ~verboseFlag: APy3_GENfuns.printcol("fitted: Row {0}".format(thisRow),'green')
    #
    
    if saveFlag: 
        APy3_GENfuns.printcol('saving estimated(fitted) & measured collected charge in {0}'.format(saveFolder),'blue')
        for iSet in range(NSets):
            for jGn in range(3):
                thisFileNameOut= fileList_all[iSet][jGn+1][:-3]+'_estCharge.h5'
                APy3_GENfuns.write_1xh5(saveFolder+thisFileNameOut, datafitted_e_4D[jGn,iSet,:,:], '/data/data')
                if verboseFlag: APy3_GENfuns.printcol('saved {0}'.format(saveFolder+thisFileNameOut),'green')
                #
                thisFileNameOut= fileList_all[iSet][jGn+1][:-3]+'_measCharge.h5'
                APy3_GENfuns.write_1xh5(saveFolder+thisFileNameOut, alldata_e_4DAr[jGn,iSet,:,:], '/data/data')
                if verboseFlag: APy3_GENfuns.printcol('saved {0}'.format(saveFolder+thisFileNameOut),'green')
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




