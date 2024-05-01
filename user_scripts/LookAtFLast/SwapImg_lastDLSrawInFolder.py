# -*- coding: utf-8 -*-
"""
descramble and visualize/save all scrambled dataset in a folder
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./WIP_SaveFLast_multiDLSraw.py
"""
#%% imports and useful constants
from APy3_auxINIT import *
# ---
#
#
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#%% Flags
#
lastFileOnlyFlag= False # alternatively: process all files in folder
#
refColH1_0_Flag = False # True if refcol data are streamed out as H1<0> data.
#
showFlag= True
manyImgFlag= False # select more than 1 digit image in interactive plot
#
highMemFlag= True
cleanMemFlag= True 
verboseFlag= True
#
#---
#
#%% data from here
mainFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190507_000_BSI02_darkCurrent/processed/2019.05.06_darkCurr/Tm20/DLSraw/'
if mainFolder[-1]!='/': mainFolder+='/'
#
#fromImg=0; toImg=-1 # negative==all
fromImg=0; toImg=10 # negative==all
#
in_1file_suffix= "DLSraw.h5"
#
# ---
ADCcorrCDSFlag=False
pedSubtractFlag=False
#
ADCcorrFolder= './LookAtFLast_CalibParam/ADUcorr/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
pedestalFolder= './LookAtFLast_CalibParam/Pedestal/'
if pedestalFolder[-1]!='/': pedestalFolder+='/'
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#
#
def ShowSwap_DLSrawInFolder(mainFolder, # where data is
                         fromImg, toImg, # negative==all
                         #
                         ADCcorrCDSFlag,
                         pedSubtractFlag,
                         ADCcorrFolder,
                         pedestalFolder,
                         #
                         lastFileOnlyFlag, # alternatively: process all files in folder
                         refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                         #
                         showFlag,
                         manyImgFlag, # select more than 1 digit image in interactive plot
                         #
                         in_1file_suffix,
                         #
                         highMemFlag,
                         cleanMemFlag,
                         verboseFlag):
    startTime=time.time()
    APy3_GENfuns.printcol("script starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    # ---
    #
    #%% what's up doc
    APy3_GENfuns.printcol("will look at files {0} ... {1}".format(mainFolder,in_1file_suffix), 'blue')
    if lastFileOnlyFlag: APy3_GENfuns.printcol("will process only the most recent", 'blue')
    APy3_GENfuns.printcol("will process from Img {0} to img {1} (negative=all)".format(fromImg,toImg), 'blue')
    if refColH1_0_Flag: APy3_GENfuns.printcol("will H1<0> data as RefCol data", 'blue')
    if showFlag: APy3_GENfuns.printcol("will show images interactively", 'blue')
    #
    if ADCcorrCDSFlag: 
        APy3_GENfuns.printcol("will look ADCcor files in {0}".format(ADCcorrFolder), 'blue')
        if pedSubtractFlag: APy3_GENfuns.printcol("will look for pedestal file in {0}".format(pedestalFolder), 'blue')
        if saveAvgCDSFlag: 
            if pedSubtractFlag: APy3_GENfuns.printcol("save an ADCcorr CDS avg (pedestal-subtracted) h5 file", 'blue') 
            else: APy3_GENfuns.printcol("save an ADCcorr CDS avg h5 file", 'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol("fast, high memory usage", 'blue')
    else:  APy3_GENfuns.printcol("slow, small memory usage", 'blue')
    if cleanMemFlag: APy3_GENfuns.printcol("will try to free memory when possible", 'blue')
    if verboseFlag: APy3_GENfuns.printcol("verbose", 'blue')
    if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    # ---
    #
    #%% ADCcor files and pedestal files
    ADCparam_validMap= numpy.zeros((NRow,NCol),dtype=bool)
    ADCparam_crs_slope= numpy.ones((NRow,NCol))
    ADCparam_crs_offset= numpy.ones((NRow,NCol))
    ADCparam_fn_slope= numpy.ones((NRow,NCol))        
    ADCparam_fn_offset= numpy.ones((NRow,NCol))
    data_pedestal= numpy.zeros((NRow,NCol))
    #
    if ADCcorrCDSFlag:
        ADCparam_validMap= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_ADCproc_Map.h5', '/data/data').astype(bool)
        ADCparam_crs_slope= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_crs_slope.h5', '/data/data')
        ADCparam_crs_offset= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_crs_offset.h5', '/data/data')
        ADCparam_fn_slope= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_fn_slope.h5', '/data/data')        
        ADCparam_fn_offset= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_fn_offset.h5', '/data/data')
        if verboseFlag: APy3_GENfuns.printcol("ADCcor files: {0}ADCcor _ADCproc_Map / _crs/fn _slope/offset.h5".format(ADCcorrFolder), 'green')
        #
        # modify load ADCparam to avoid /0
        goodPixMap= (ADCparam_validMap==True); badPixMap= (ADCparam_validMap==False) 
        ADCparam_crs_offset[badPixMap]=1.0
        ADCparam_crs_slope[badPixMap]=1.0
        ADCparam_fn_offset[badPixMap]=1.0
        ADCparam_fn_slope[badPixMap]=1.0
        #
        if pedSubtractFlag:
            data_pedestal= APy3_GENfuns.read_1xh5(pedestalFolder+'Pedestal.h5', '/data/data') 
            APy3_GENfuns.printcol("pedestal: {0}Pedestal.h5".format(pedestalFolder), 'green')
    #
    #%% list or last data files
    filelist_in= APy3_GENfuns.list_files(mainFolder, '*', in_1file_suffix) # all files
    APy3_GENfuns.printcol("{0} image sets found in folder".format(len(filelist_in)), 'green')
    if lastFileOnlyFlag:   
        APy3_GENfuns.printcol("will only process the most recent", 'green') 
        aux_fileName= os.path.basename( APy3_GENfuns.last_file(mainFolder, '*'+in_1file_suffix) ) # filename only, no path
        filelist_in= [aux_fileName]
    # ---
    for ifile,file_in in enumerate(filelist_in):
        APy3_GENfuns.printcol('collection {0}/{1}'.format(ifile,len(filelist_in)-1), 'blue')
        APy3_GENfuns.printcol(mainFolder+file_in, 'green')
        (dataSmpl_in,dataRst_in) = APy3_GENfuns.read_2xh5(mainFolder+file_in, '/data','/reset')
        (NImg, aux_NRow, aux_NCol) = dataSmpl_in.shape
        if verboseFlag: APy3_GENfuns.printcol("{0} Img read from file".format(NImg), 'green')
        # ---
        # select images
        if (fromImg<0)|(toImg<0)|(toImg<fromImg)|(NImg<=toImg): 
            if verboseFlag: APy3_GENfuns.printcol("will use all ({0}) Img in file".format(NImg), 'green')
        else: 
            NImg= toImg-fromImg+1
            if verboseFlag: APy3_GENfuns.printcol("will use Img from {0} to {1} (included), for a total of {2}".format(fromImg,toImg,NImg), 'green')
            dataSmpl_in= dataSmpl_in[fromImg:toImg+1,:,:]
            dataRst_in=  dataRst_in[fromImg:toImg+1,:,:]
        # ---
        #%% convert to GnCrsFn
        if True:
            if verboseFlag: APy3_GENfuns.printcol("converting to Gn,Crs,Fn", 'blue')
            #
            if highMemFlag: dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(dataSmpl_in,dataRst_in, ERRDLSraw,ERRint16)
            else:
                dscrmbld_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
                for thisImg in range(NImg):
                    thisSmpl_DLSraw= dataSmpl_in[thisImg,:,:].reshape((1, NRow,NCol))
                    thisRst_DLSraw=  dataRst_in[thisImg,:,: ].reshape((1, NRow,NCol))
                    this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
                    dscrmbld_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
                    if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
        # ---
        #%% ADCcor, CDS, pedSub
        if ADCcorrCDSFlag: 
            if verboseFlag: APy3_GENfuns.printcol("ADC-correcting", 'blue')
            data_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                                      ADCparam_crs_slope,ADCparam_crs_offset,ADCparam_fn_slope,ADCparam_fn_offset, NRow,NCol)
            # flagging bad pixels    
            #if verboseFlag: APy3_GENfuns.printcol("flagging bad pixels", 'blue')
            # set the missing vales to NaN
            missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
            data_ADCcorr[missingValMap]= numpy.NaN
            # set bad ADCcal values to NaN
            missingADCcorrMap= ADCparam_validMap==False    
            data_ADCcorr[:,:,missingADCcorrMap]= numpy.NaN # (both Smpl and Rst) 
            #
            #if verboseFlag: APy3_GENfuns.printcol("CDS", 'blue')
            data_CDS= data_ADCcorr[1:,iSmpl,:,:] - data_ADCcorr[:-1,iRst,:,:]
            if cleanMemFlag: del data_ADCcorr
            #
            if pedSubtractFlag:
                #if verboseFlag: APy3_GENfuns.printcol("subtracting pedestal", 'blue')
                data_CDS= data_CDS-data_pedestal
            #
            #if verboseFlag: APy3_GENfuns.printcol("avg", 'blue')
            data_CDSavg= numpy.average(data_CDS,axis=0)
            if cleanMemFlag: del data_CDS
        else: data_CDSavg= numpy.ones((NRow,NCol))*numpy.NaN
        # ---
        #%% show
        if showFlag:
            if verboseFlag: APy3_GENfuns.printcol("showing", 'blue')
            APy3_P2Mfuns.percDebug_plot_interactive(dscrmbld_GnCrsFn, data_CDSavg, manyImgFlag)
        # ---
        #%% swap
        APy3_GENfuns.printcol("swap odd and even images? [Y/N]", 'black')
        nextstep_swap = input()
        if nextstep_swap in ['y','Y','yes','YES','Y']:
            dataSmpl_swap= numpy.copy(dataSmpl_in)
            dataRst_swap=  numpy.copy(dataRst_in)
            dataSmpl_swap[0::2,:,:]= dataSmpl_in[1::2,:,:]
            dataRst_swap[ 0::2,:,:]= dataRst_in[ 1::2,:,:]
            dataSmpl_swap[1::2,:,:]= dataSmpl_in[0::2,:,:]
            dataRst_swap[ 1::2,:,:]= dataRst_in[0::2,:,:]
            # ---
            #%% swap
            if verboseFlag: APy3_GENfuns.printcol("converting to Gn,Crs,Fn the swapped Img set", 'blue')
            if highMemFlag: swap_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(dataSmpl_swap,dataRst_swap, ERRDLSraw,ERRint16)
            else:
                swap_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
                for thisImg in range(NImg):
                    thisSmpl_DLSraw= dataSmpl_swap[thisImg,:,:].reshape((1, NRow,NCol))
                    thisRst_DLSraw=  dataRst_swap[thisImg,:,: ].reshape((1, NRow,NCol))
                    this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
                    swap_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
                    if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
            if showFlag:
                if verboseFlag: APy3_GENfuns.printcol("showing swapped", 'blue')
                APy3_P2Mfuns.percDebug_plot_interactive(swap_GnCrsFn, data_CDSavg, manyImgFlag)
            # ---
            #%% eventually save swapped
            APy3_GENfuns.printcol("save the swapped img collection to file? [Y/N]", 'black')
            nextstep_saveswap = input()
            if nextstep_saveswap in ['y','Y','yes','YES','Y']:
                file_out= file_in+'_swap.h5'
                APy3_GENfuns.write_2xh5(mainFolder+file_out, dataSmpl_swap,'/data', dataRst_swap,'/reset')
                APy3_GENfuns.printcol("swapped img set saved to: {0}".format(mainFolder+file_out), 'green')
        # ---
        if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
        # ---
    #
    #%% that's all folks
    APy3_GENfuns.printcol("done",'blue')
    endTime=time.time()
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    if verboseFlag: APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
    #
    return dscrmbld_GnCrsFn
# ---
#
#%% exec it

ShowSwap_DLSrawInFolder(mainFolder, # where data is
                         fromImg, toImg, # negative==all
                         #
                         ADCcorrCDSFlag,
                         pedSubtractFlag,
                         ADCcorrFolder,
                         pedestalFolder,
                         #
                         lastFileOnlyFlag, # alternatively: process all files in folder
                         refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                         #
                         showFlag,
                         manyImgFlag, # select more than 1 digit image in interactive plot
                         #
                         in_1file_suffix,
                         #
                         highMemFlag,
                         cleanMemFlag,
                         verboseFlag)

#
#---
#%% profile it
#import cProfile
#cProfile.run('descramble_highMem(...)', sort='cumtime')
#%% or just execute it
#descramble_highMem(...)
