# -*- coding: utf-8 -*-
"""
set .h5 of avg light at different int times => eval charge to be used as x in multign plot

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
'''
#### BSI04, T-20, dmuxSELHigh, biasBSI04_04, Lat Oflw PGAB v1 ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn_2/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
# tab-separated-text file, having 2 colums (integr time in ms, _avg)
#dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn0_PGABBB_OD2.0_meta.dat'
#dflt_useGn=0
#dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn1_PGABBB_OD2.0_meta.dat'
#dflt_useGn=1
dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn2_PGABBB_OD5.0_meta.dat'
dflt_useGn=2
#
#dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2019.12.02_Gn012_MultiGnCal.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn012_MultiGnCal.h5'
#
dflt_alternPed_file='NONE'
#dflt_alternPed_file=dflt_folder_data2process+'xxx'
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
dflt_fit_minNpoints=4
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_saveFolder=dflt_folder_data2process+'../fitCollCharge2/'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
'''
#
'''
#### BSI04, T-20, dmuxSELHigh, biasBSI04_04, Lat Oflw PGAB v2 ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
# tab-separated-text file, having 2 colums (integr time in ms, _avg)
dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn0_PGABBB_OD1.0_avg_meta.dat' #also OD1,2,3,4,5.0
dflt_useGn=0
#dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn1_PGABBB_OD1.0_avg_meta.dat' #also OD1,2,3,4,5.0
#dflt_useGn=1
#dflt_metaFileName= 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_Gn2_PGABBB_OD1.0_avg_meta.dat' #also OD1,2,3,4,5.0
#dflt_useGn=2
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5'
#
dflt_alternPed_file='NONE'
#dflt_alternPed_file=dflt_folder_data2process+'xxx'
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
dflt_fit_minNpoints=10 #4
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_saveFolder=dflt_folder_data2process+'../fitCollCharge/'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
'''
#
#
#'''
#### BSI04, T-20, dmuxSELHigh, biasBSI04_05, Lat Oflw PGA6BB ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#
# tab-separated-text file: integr_time_in_ms<tab>_avg
#dflt_metaFileName= 'BSI04_Tm20_3of7ADC_biasBSI04_05_Gn0_PGA6BB_OD6.0_avg_meta.dat' #also OD1,2,3,4,5,6.0
#dflt_useGn=0
#dflt_metaFileName= 'BSI04_Tm20_3of7ADC_biasBSI04_05_Gn1_PGA6BB_OD6.0_avg_meta.dat' #also OD1,2,3,4,5,6.0
#dflt_useGn=1
dflt_metaFileName= 'BSI04_Tm20_3of7ADC_biasBSI04_05_Gn2_PGA6BB_OD6.0_avg_meta.dat' #also OD1,2,3,4,5,6.0
dflt_useGn=2
#
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14_MultiGnCal.h5'
#
dflt_alternPed_file='NONE'
#dflt_alternPed_file=dflt_folder_data2process+'xxx'
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
dflt_fit_minNpoints=10 #4
#
dflt_saveFlag='Y'; #dflt_saveFlag='N'
dflt_saveFolder=dflt_folder_data2process+'../fitCollCharge/'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
#'''
#
# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
#
GUIwin_arguments+= ['use data from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['metadata file'] 
GUIwin_arguments+= [dflt_metaFileName] 
#
GUIwin_arguments+= ['assume all data in Gn [0/1/2]'] 
GUIwin_arguments+= [str(dflt_useGn)]
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
useGn= int(dataFromUser[i_param]); i_param+=1

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
    APy3_GENfuns.printcol('  assuming those data are in Gn{0}'.format(useGn),'blue')

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
(NSets,N2)= numpy.array(fileList_all).shape
if N2!=2: APy3_GENfuns.printErr("metafile: {0} columns".format(N2))
elif verboseFlag: APy3_GENfuns.printcol("{0} Sets in metafile".format(NSets),'green')
#---
#% read data files
APy3_GENfuns.printcol("reading avg files",'blue')

intTimes_ms=[]
for iSet in range(NSets):
    intTimes_ms+= [float(fileList_all[iSet][0])]
intTimes_ms= numpy.array(intTimes_ms)

alldata_3DAr= APy3_GENfuns.numpy_NaNs((NSets,NRow,NCol))
for iSet in range(NSets):
    alldata_3DAr[iSet,:,:]= read_warn_1xh5(folder_data2process+fileList_all[iSet][1], '/data/data')

alldata_ADU= (alldata_3DAr-PedestalADU_multiGn[useGn,:,:])
alldata_e= (alldata_3DAr-PedestalADU_multiGn[useGn,:,:])*e_per_ADU_multiGn[useGn,:,:]
#---
#% show ramps
if (showFlag & (~interactiveShowFlag)): 
    if verboseFlag: APy3_GENfuns.printcol("showing ramps",'blue')
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            APy3_GENfuns.plot_1D(intTimes_ms, alldata_ADU[:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]','({0},{1})'.format(thisRow,thisCol))
            APy3_GENfuns.plot_1D(intTimes_ms, alldata_e[:,thisRow,thisCol], 'integration time [ms]','collected charge [e]','({0},{1})'.format(thisRow,thisCol))
            APy3_GENfuns.showIt()
#
elif (showFlag & interactiveShowFlag): 
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("interactivly showing ramps",'blue')
    APy3_GENfuns.printcol("[P]lot/[F]it ramp / find [M]ax ADU / [Q]uit",'green')
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
            APy3_GENfuns.plot_1D(intTimes_ms, alldata_ADU[:,thisRow,thisCol], 'integration time [ms]','pixel output [ADU]','({0},{1})'.format(thisRow,thisCol))
            APy3_GENfuns.plot_1D(intTimes_ms, alldata_e[:,thisRow,thisCol], 'integration time [ms]','collected charge [e]','({0},{1})'.format(thisRow,thisCol))
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
            map2fit= alldata_ADU[:,thisRow,thisCol]<=(fit_maxADU)*numpy.nanmax(alldata_ADU[:,thisRow,thisCol])
            data2fit_tint= numpy.copy(intTimes_ms[map2fit])
            data2fit_e= numpy.copy(alldata_e[:,thisRow,thisCol][map2fit])
            data2fit_ADU= numpy.copy(alldata_ADU[:,thisRow,thisCol][map2fit])
            del map2fit
            map2fit= ~numpy.isnan(data2fit_e)
            data2fit_tint= numpy.copy(data2fit_tint[map2fit])
            data2fit_e= numpy.copy(data2fit_e[map2fit])
            data2fit_ADU= numpy.copy(data2fit_ADU[map2fit])
            if len(data2fit_tint)>=fit_minNpoints:
                (fit_slope,fit_offset)= APy3_FITfuns.linear_fit(data2fit_tint,data2fit_e)
                fit_R2= APy3_FITfuns.linear_fit_R2(data2fit_tint,data2fit_e)
                APy3_GENfuns.printcol("fit e(t): toffset={1}ms, slope={0}e/ms, R2={2}, Npoints={3}".format(fit_slope,fit_offset,fit_R2,len(data2fit_tint)),'green')
                if (fit_R2<fit_minR2): APy3_GENfuns.printcol("R2={0} < {1}".format(fit_R2,fit_minR2),'orange')
                APy3_GENfuns.plot_1D(APy3_FITfuns.linear_fun(intTimes_ms,fit_slope,fit_offset), alldata_ADU[:,thisRow,thisCol], 
                                 'collected charge [e]','pixel output [ADU]','({0},{1})'.format(thisRow,thisCol))
                APy3_GENfuns.showIt()
            else: APy3_GENfuns.printcol("unable to fit Npoints={0}<{1}".format(len(data2fit_tint),fit_minNpoints),'orange')
            del map2fit; del data2fit_tint; del data2fit_e; del data2fit_ADU
        #
        elif (nextstep in ['m','M']):
            APy3_GENfuns.printcol("eval max ADU (ignoring nans) not above a common level",'green')
            aux2_maxADU= numpy.nanmax(alldata_ADU.flatten())*(fit_maxADU)

            APy3_GENfuns.printcol("what value to use for the common level? [default {0}]".format(aux_maxADU),'green')
            aux_maxADU_str= input()
            if len(aux_maxADU_str)>0: aux_maxADU= float(aux_maxADU_str)
            else: aux_maxADU=aux2_maxADU
            APy3_GENfuns.printcol("eval max ADU (ignoring nans) <= {0}".format(aux_maxADU),'green')
            auxdata_ADU= numpy.copy(alldata_ADU)
            badmap= auxdata_ADU>aux_maxADU
            auxdata_ADU[badmap]= numpy.NaN
            auxmax= numpy.nanmax(auxdata_ADU)
            auxargmax= numpy.unravel_index(numpy.nanargmax(auxdata_ADU), auxdata_ADU.shape)
            APy3_GENfuns.printcol("max= {0}ADU in set {1} pixel ({2},{3})".format(auxmax,auxargmax[0],auxargmax[1],auxargmax[2]), 'green')
            del auxdata_ADU
        #
        APy3_GENfuns.printcol("[P]lot/[F]it ramp / find [M]ax ADU / [Q]uit",'green')
        nextstep= input()
#---
if fitFlag:
    APy3_GENfuns.printcol("fitting e/ms ramps",'blue')
    datafitted_e= APy3_GENfuns.numpy_NaNs_like(alldata_ADU)
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            map2fit= alldata_ADU[:,thisRow,thisCol]<=fit_maxADU*numpy.nanmax(alldata_ADU[:,thisRow,thisCol])
            data2fit_tint= numpy.copy(intTimes_ms[map2fit])
            data2fit_e= numpy.copy(alldata_e[:,thisRow,thisCol][map2fit])
            data2fit_ADU= numpy.copy(alldata_ADU[:,thisRow,thisCol][map2fit])
            del map2fit
            map2fit= ~numpy.isnan(data2fit_e)
            data2fit_tint= numpy.copy(data2fit_tint[map2fit])
            data2fit_e= numpy.copy(data2fit_e[map2fit])
            data2fit_ADU= numpy.copy(data2fit_ADU[map2fit])
            if len(data2fit_tint)>=fit_minNpoints:
                (fit_slope,fit_offset)= APy3_FITfuns.linear_fit(data2fit_tint,data2fit_e)
                fit_R2= APy3_FITfuns.linear_fit_R2(data2fit_tint,data2fit_e)
                if (fit_R2>=fit_minR2): 
                    datafitted_e[:,thisRow,thisCol]= APy3_FITfuns.linear_fun(intTimes_ms,fit_slope,fit_offset)
                    aux_col='green'
                else: aux_col='orange'
                if verboseFlag: APy3_GENfuns.printcol("pix({3},{4}): fit e(t): toffset={1}ms, slope={0}e/ms, R2={2}".format(fit_slope,fit_offset,fit_R2, thisRow,thisCol),aux_col)
            elif verboseFlag: APy3_GENfuns.printcol("pix({2},{3}): unable to fit Npoints={0}<{1}".format(len(data2fit_tint),fit_minNpoints, thisRow,thisCol),'orange')
            del map2fit; del data2fit_tint; del data2fit_e; del data2fit_ADU
        if ~verboseFlag: APy3_GENfuns.printcol("fitted: Row {0}".format(thisRow),'green')

    if saveFlag: 
        APy3_GENfuns.printcol('saving estimated (fitted) collected charge in {0}'.format(saveFolder),'blue')
        for iSet in range(NSets):
            thisFileNameOut= fileList_all[iSet][1][:-3]+'_estCharge.h5'
            APy3_GENfuns.write_1xh5(saveFolder+thisFileNameOut, datafitted_e[iSet,:,:], '/data/data')
            if verboseFlag: APy3_GENfuns.printcol('saved {0}'.format(saveFolder+thisFileNameOut),'green')

            thisFileNameOut= fileList_all[iSet][1][:-3]+'_measCharge.h5'
            APy3_GENfuns.write_1xh5(saveFolder+thisFileNameOut, alldata_e[iSet,:,:], '/data/data')
            if verboseFlag: APy3_GENfuns.printcol('saved {0}'.format(saveFolder+thisFileNameOut),'green')



#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




