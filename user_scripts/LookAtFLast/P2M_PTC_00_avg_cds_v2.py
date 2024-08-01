# -*- coding: utf-8 -*-
"""
descrambled (DLSRaw) collections => .h5 of avg and rms (ADUcor, not PedSub) for each collection (useful to prepare data for PTC) 

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
cd /home/marras/PercAuxiliaryTools/LookAtFLast
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_PTC_00_avg_cds_v2.py
or:
python3
exec(open("./xxx.py").read())

"""

#%% imports and useful constants
from APy3_auxINIT import *
import ast
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#
#%% defaults for GUI window
#
#'''
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_Tm20_drk/DLSraw'
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_inputFileSuffix='DLSraw.h5'
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
#
dflt_Img2proc='10:499'
#dflt_Img2proc='10:999'
#
dflt_CDSFlag='Y'; #dflt_CDSFlag='N'
dflt_CMAFlag='Y'; dflt_CMAFlag='N'
cols2CMA_str = '32:63'; #cols2CMA_str = '704:735'
#
dflt_saveFlag='Y'
dflt_outFolder= dflt_folder_data2process +'../avg_std/'
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
#'''
#
#
dflt_showFlag='N'; #dflt_showFlag='y';
#
dflt_highMemFlag='Y' 
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'
# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['use data from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['ending with'] 
GUIwin_arguments+= [dflt_inputFileSuffix] 
#
GUIwin_arguments+= ['ADCcor 1-file'] 
GUIwin_arguments+= [dflt_ADCcor_file] 
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
#
GUIwin_arguments+= ['CDS? [Y/N]']
GUIwin_arguments+= [dflt_CDSFlag] 
GUIwin_arguments+= ['CMA? [Y/N]']
GUIwin_arguments+= [dflt_CMAFlag] 
GUIwin_arguments+= ['cols to use for CMA [from:to]']
GUIwin_arguments+= [cols2CMA_str] 
#
GUIwin_arguments+= ['show results? [Y/N]']
GUIwin_arguments+= [dflt_showFlag] 
#
GUIwin_arguments+= ['save results to files? [Y/N]']
GUIwin_arguments+= [dflt_saveFlag] 
GUIwin_arguments+= ['save results: to folder'] 
GUIwin_arguments+= [dflt_outFolder] 
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
inputFileSuffix= dataFromUser[i_param]; i_param+=1
#
ADCcor_file= dataFromUser[i_param]; i_param+=1
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg= Img2proc[0]; toImg= Img2proc[-1]
#
CDSFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
CMAFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cols2CMA_str=  dataFromUser[i_param]; i_param+=1
if CMAFlag: cols2CMA = APy3_GENfuns.matlabLike_range(cols2CMA_str)
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
saveFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
outFolder=  dataFromUser[i_param]; i_param+=1
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will process data from {0}...{1}'.format(folder_data2process,inputFileSuffix),'blue')
#
APy3_GENfuns.printcol('ADCcor file: {0}'.format(ADCcor_file),'blue')
if APy3_GENfuns.notFound(ADCcor_file): APy3_P2M.printErr('not found: '+ADCcor_file)
#
APy3_GENfuns.printcol('will elaborate Img{0}'.format(Img2proc_mtlb),'blue')
#
if CDSFlag: APy3_GENfuns.printcol('will apply CDS','blue')
else: APy3_GENfuns.printcol('will use Sample','blue')
#
if CMAFlag: APy3_GENfuns.printcol('will apply CMA using cols {0} as reference'.format(cols2CMA_str),'blue')
if showFlag: APy3_GENfuns.printcol('will show results','blue')
#
if saveFlag: APy3_GENfuns.printcol('will save results as {0}...'.format(outFolder),'blue')
#
if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
if (verboseFlag): APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
# ---
#
#%% prepare h5 files for PTC
if (CDSFlag & CMAFlag):    avgFileSuffix= 'CDSCMA_avg.h5';  stdFileSuffix= 'CDSCMA_sigma.h5'
elif (CDSFlag & ~CMAFlag): avgFileSuffix= 'CDS_avg.h5';     stdFileSuffix= 'CDS_sigma.h5'
elif (CMAFlag & ~CDSFlag): avgFileSuffix= 'SmplCMA_avg.h5'; stdFileSuffix= 'SmplCMA_sigma.h5'
else:                      avgFileSuffix= 'Smpl_avg.h5';    stdFileSuffix= 'Smpl_sigma.h5'
#---
#% read ADC file
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
#---
#% list files
fileList= APy3_GENfuns.list_files(folder_data2process, '*', inputFileSuffix)
if verboseFlag: APy3_GENfuns.printcol('{0} files to be processed'.format(len(fileList)),'green')
for iFile,thisFile in enumerate(fileList):
    if (verboseFlag): APy3_GENfuns.printcol("file {0}/{1}: {2}{3}".format(iFile,len(fileList)-1,folder_data2process,thisFile),'green')
    (Smpl_DLSraw,Rst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+thisFile, '/data','/reset', fromImg,toImg)
    #
    # DLSraw => Gn,Crs,Fn
    if verboseFlag: APy3_GENfuns.printcol('DLSraw => Gn,Crs,Fn','blue')
    if highMemFlag: data_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(Smpl_DLSraw,Rst_DLSraw, ERRDLSraw, ERRint16)
    else:
        data_GnCrsFn= numpy.zeros((len(Img2proc),NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
        for thisImg in range(len(Img2proc)):
            thisSmpl_DLSraw= Smpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
            thisRst_DLSraw=  Rst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
            this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
            data_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
            if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,len(Img2proc))
        if cleanMemFlag: del thisSmpl_DLSraw; del thisRst_DLSraw; del this_dscrmbld_GnCrsFn
    #---
    #%% ADUcorr, CMA,CDS,avg
    if verboseFlag: APy3_GENfuns.printcol('ADU-correct','blue')
    data_ADU= APy3_GENfuns.numpy_NaNs((len(Img2proc),NSmplRst, NRow,NCol))
    data_ADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iSmpl,:,:,iCrs],data_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
    data_ADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iRst,:,:,iCrs], data_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
    if cleanMemFlag: del data_GnCrsFn
    #
    mode_str=""
    if CMAFlag:
        if verboseFlag: APy3_GENfuns.printcol('CMA-ing','blue')
        data_ADU[:,iSmpl,:,:]= APy3_P2Mfuns.CMA(data_ADU[:,iSmpl,:,:] ,cols2CMA)
        data_ADU[:,iRst,:,:]=  APy3_P2Mfuns.CMA(data_ADU[:,iRst,:,:]  ,cols2CMA)
        mode_str+="CMA,"
    #
    if CDSFlag: 
        if verboseFlag: APy3_GENfuns.printcol('CDS std-ing','blue')
        data2PTC_avg=  numpy.average(APy3_P2Mfuns.CDS(data_ADU), axis=0)
        data2PTC_std=  numpy.std(APy3_P2Mfuns.CDS(data_ADU), axis=0)
        mode_str+='CDS'
    else: 
        if verboseFlag: APy3_GENfuns.printcol('Smpl std-ing','blue')
        data2PTC_avg=  numpy.average(data_ADU[:,iSmpl,:,:], axis=0)
        data2PTC_std=  numpy.std(data_ADU[:,iSmpl,:,:], axis=0)
        mode_str+='Smpl'
    #---
    # if needed, show
    if showFlag:
        APy3_GENfuns.plot_2D_all(data2PTC_avg, False, 'col','row','{0} avg [ADU] {1}'.format(mode_str,thisFile[:(-len(inputFileSuffix))]), True)
        APy3_GENfuns.plot_2D_all(data2PTC_std, False, 'col','row','{0} std [ADU] {1}'.format(mode_str,thisFile[:(-len(inputFileSuffix))]), True)
        matplotlib.pyplot.show(block=True)
    #---
    # save
    if saveFlag:
        fileName_avg= thisFile[:(-len(inputFileSuffix))]+avgFileSuffix
        fileName_std= thisFile[:(-len(inputFileSuffix))]+stdFileSuffix
        APy3_GENfuns.write_1xh5(outFolder+fileName_avg, data2PTC_avg, '/data/data')
        APy3_GENfuns.write_1xh5(outFolder+fileName_std, data2PTC_std, '/data/data')
        if (verboseFlag): APy3_GENfuns.printcol("saving avg {0}{1}".format(outFolder,fileName_avg),'green')
        if (verboseFlag): APy3_GENfuns.printcol("saving std {0}{1}".format(outFolder,fileName_std),'green')
    if (verboseFlag): APy3_GENfuns.printcol("--  --  --  --",'green')
# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
# ---
# ---
# ---

