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
#
def descramble_versatile(mainFolder, # where data is
                         expected_suffix_fl0,
                         expected_suffix_fl1,
                         expected_suffix_metadata,
                         fromImg, toImg, # negative==all
                         #
                         ADCcorrCDSFlag,
                         pedSubtractFlag,
                         ADCcorrFolder,
                         pedestalFolder,
                         #
                         lastFileOnlyFlag, # alternatively: process all files in folder
                         swapSmplRstFlag,
                         seqModHalfImgFlag, # this actually means: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
                         refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                         #
                         showFlag,
                         manyImgFlag, # select more than 1 digit image in interactive plot
                         #
                         saveFlag_1file, # save descramble DLSraw to 1 big file
                         saveFlag_multiFile, #saveFlag_multiFile= False # save descramble DLSraw to multiple files, using metadata name
                         saveAvgCDSFlag, # save 2D img (float): avg of ADCcorr, CDS, possibly ped-Subtracted
                         #
                         outFolder,
                         out_1file_suffix,
                         out_multiFile_suffix, 
                         out_imgXFile_multiFile,
                         out_AvgCDSfile_suffix,
                         #
                         cleanMemFlag,
                         highMemFlag,
                         verboseFlag):
    startTime=time.time()
    APy3_GENfuns.printcol("script starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    # ---
    #
    #%% what's up doc
    APy3_GENfuns.printcol("will look at files {0} ... {1}/{2}".format(mainFolder,expected_suffix_fl0,expected_suffix_fl1), 'blue')
    if lastFileOnlyFlag: APy3_GENfuns.printcol("will process only the most recent", 'blue')
    APy3_GENfuns.printcol("will process from Img {0} to img {1} (negative=all)".format(fromImg,toImg), 'blue')
    if swapSmplRstFlag: APy3_GENfuns.printcol("will correct for OdinDAQ Sample/Reset swap", 'blue')
    if seqModHalfImgFlag: APy3_GENfuns.printcol("will consider images as as SeqMod data taken with a stdMod Firmware", 'blue')
    if refColH1_0_Flag: APy3_GENfuns.printcol("will H1<0> data as RefCol data", 'blue')
    if showFlag: APy3_GENfuns.printcol("will show images interactively", 'blue')
    if saveFlag_1file: APy3_GENfuns.printcol("will save 1 descrambled DLSraw file as {0} ... {1}".format(outFolder,out_1file_suffix), 'blue')
    if saveFlag_multiFile: APy3_GENfuns.printcol("will save multiple descrambled DLSraw files in {0}, using file names in ...{1} ({2} img/file)".format(outFolder,out_1file_suffix, out_imgXFile_multiFile), 'blue')
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
    filelist_fl0= APy3_GENfuns.list_files(mainFolder, '*', expected_suffix_fl0) # all files
    APy3_GENfuns.printcol("{0} image sets found in folder".format(len(filelist_fl0)), 'green')
    if lastFileOnlyFlag:   
        APy3_GENfuns.printcol("will only process the most recent", 'green') 
        aux_fileName= os.path.basename( APy3_GENfuns.last_file(mainFolder, '*'+expected_suffix_fl0) ) # filename only, no path
        filelist_fl0= [aux_fileName]
    # ---
    #
    #%% read and descramble data file
    for ifile,file_fl0 in enumerate(filelist_fl0):
        if verboseFlag: APy3_GENfuns.printcol("descrambling set {0}/{1}".format(ifile,len(filelist_fl0)-1), 'blue')
        auxN= len(expected_suffix_fl0)*(-1)
        file_fl1= file_fl0[:auxN]+expected_suffix_fl1
        if APy3_GENfuns.notFound(mainFolder+file_fl1): APy3_GENfuns.printErr('unable to find ' + mainFolder+file_fl1)
        #
        file_1file_out= file_fl0[:auxN]+out_1file_suffix
        # ---
        #
        # if needed, delete the previous out data
        if ( ('dscrmbld_GnCrsFn' in locals())&(cleanMemFlag) ): del dscrmbld_GnCrsFn
        #
        # read data
        #
        if verboseFlag: 
            APy3_GENfuns.printcol("reading files", 'blue')
            APy3_GENfuns.printcol(mainFolder+file_fl0, 'green')
            APy3_GENfuns.printcol(mainFolder+file_fl1, 'green')
        (dataSmpl_fl0, dataRst_fl0) = APy3_GENfuns.read_2xh5(mainFolder+file_fl0, '/data','/reset')
        (dataSmpl_fl1, dataRst_fl1) = APy3_GENfuns.read_2xh5(mainFolder+file_fl1, '/data','/reset')
        (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
        (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
        NImg = NImg_fl0 + NImg_fl0
        if verboseFlag: APy3_GENfuns.printcol("{0}+{1}={2} Img read from files".format(NImg_fl0,NImg_fl1,NImg), 'green')
        # ---
        # select images
        if (fromImg<0)|(toImg<0)|(toImg<fromImg)|(NImg_fl0<=toImg): 
            if verboseFlag: APy3_GENfuns.printcol("will use all ({0}) Img in file".format(NImg), 'green')
        else: 
            NImg= toImg-fromImg+1
            if verboseFlag: APy3_GENfuns.printcol("will use Img from {0} to {1} (included) on both scrambled files, for a total of {2}".format(fromImg,toImg,NImg*2), 'green')
            dataSmpl_fl0= dataSmpl_fl0[fromImg:toImg+1,:,:]
            dataRst_fl0=  dataRst_fl0[fromImg:toImg+1,:,:]
            dataSmpl_fl1= dataSmpl_fl1[fromImg:toImg+1,:,:]
            dataRst_fl1=  dataRst_fl1[fromImg:toImg+1,:,:]
        # ---
        #
        # read metadata if needed
        file_metadata = file_fl0[:auxN]+expected_suffix_metadata
        if saveFlag_multiFile:
            if APy3_GENfuns.notFound(mainFolder+file_metadata): APy3_GENfuns.printErr('unable to find ' + mainFolder+file_metadata)
            metadata_content= APy3_GENfuns.read_tst(mainFolder+file_metadata)
            if verboseFlag: APy3_GENfuns.printcol("{0} items found in metadata file: {1}".format(len(metadata_content),mainFolder+file_metadata), 'green')
            Nmultifiles2write= len(metadata_content)
            if (Nmultifiles2write * out_imgXFile_multiFile != NImg): APy3_GENfuns.printErr('Nmultifiles2write * out_imgXFile_multiFile != NImg')
        #
        #
        # if ( saveMultiFile & lowMem ), do it 1 file at a time
        if (saveFlag_multiFile & (highMemFlag==False)):
            dataSmpl_fl0= dataSmpl_fl0.reshape((Nmultifiles2write,out_imgXFile_multiFile//2,aux_NRow,aux_NCol)) # ..,..,1484,1408
            dataRst_fl0=  dataRst_fl0.reshape((Nmultifiles2write,out_imgXFile_multiFile//2,aux_NRow,aux_NCol))
            dataSmpl_fl1= dataSmpl_fl1.reshape((Nmultifiles2write,out_imgXFile_multiFile//2,aux_NRow,aux_NCol))
            dataRst_fl1=  dataRst_fl1.reshape((Nmultifiles2write,out_imgXFile_multiFile//2,aux_NRow,aux_NCol))
            #
            for iFile,thisFile in enumerate(metadata_content[:,1]): 
                (thisSmpl_DLSraw, thisRst_DLSraw)= APy3_P2Mfuns.descramble(dataSmpl_fl0[iFile,:,:,:],
                                                                   dataRst_fl0[iFile,:,:,:],
                                                                   dataSmpl_fl1[iFile,:,:,:],
                                                                   dataRst_fl1[iFile,:,:,:],
                                                                   swapSmplRstFlag,seqModHalfImgFlag, refColH1_0_Flag,
                                                                   True,cleanMemFlag,False) #Highmem, notverbose since 1 img at a time
                APy3_GENfuns.write_2xh5(outFolder+thisFile+out_multiFile_suffix, 
                                        thisSmpl_DLSraw,'/data', 
                                        thisRst_DLSraw,'/reset')
                if verboseFlag: APy3_GENfuns.printcol("{0} descrambled img saved in file: {1}".format(out_imgXFile_multiFile,outFolder+thisFile+out_multiFile_suffix), 'green')
                #
                # show content of the file that has been saved
                if showFlag:
                    (rereadSmpl_DLSraw,rereadRst_DLSraw)= APy3_GENfuns.read_2xh5(outFolder+thisFile+out_multiFile_suffix,'/data','/reset')
                    reread_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(rereadSmpl_DLSraw,rereadRst_DLSraw, ERRDLSraw,ERRint16)
                    aux_nodata= numpy.ones((NRow,NCol))*numpy.NaN
                    if verboseFlag: APy3_GENfuns.printcol("showing it", 'blue')
                    APy3_P2Mfuns.percDebug_plot_interactive(rereadSmpl_GnCrsFn, aux_nodata, manyImgFlag)
            dscrmbld_GnCrsFn= numpy.ones((1,NSmplRst,NRow,NCol,NGnCrsFn),dtype='int16')*ERRint16 # give something to stream out
        # ---
        #
        # if not ( saveMultiFile & lowMem ) 
        else:
            # descramble
            (Smpl_DLSraw, Rst_DLSraw)= APy3_P2Mfuns.descramble(dataSmpl_fl0,dataRst_fl0,dataSmpl_fl1,dataRst_fl1,
                                                               swapSmplRstFlag,seqModHalfImgFlag, refColH1_0_Flag,
                                                               highMemFlag,cleanMemFlag,verboseFlag)
            # ---
            #%% convert to GnCrsFn if needed
            if showFlag | ADCcorrCDSFlag:
                if verboseFlag: APy3_GENfuns.printcol("converting to Gn,Crs,Fn", 'blue')
                #
                if highMemFlag: dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(Smpl_DLSraw,Rst_DLSraw, ERRDLSraw,ERRint16)
                else:
                    dscrmbld_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
                    for thisImg in range(NImg):
                        thisSmpl_DLSraw= Smpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
                        thisRst_DLSraw=  Rst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
                        this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
                        dscrmbld_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
                        if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
            else: dscrmbld_GnCrsFn= numpy.ones((NImg,NSmplRst,NRow,NCol,NGnCrsFn),dtype='int16')*ERRint16
            # ---
            #
            #%% ADCcor, CDS, pedSub
            if ADCcorrCDSFlag: 
                if verboseFlag: APy3_GENfuns.printcol("ADC-correcting", 'blue')
                data_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                                          ADCparam_crs_slope,ADCparam_crs_offset,ADCparam_fn_slope,ADCparam_fn_offset, NRow,NCol)
                # flagging bad pixels    
                if verboseFlag: APy3_GENfuns.printcol("flagging bad pixels", 'blue')
                # set the missing vales to NaN
                missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
                data_ADCcorr[missingValMap]= numpy.NaN
                # set bad ADCcal values to NaN
                missingADCcorrMap= ADCparam_validMap==False    
                data_ADCcorr[:,:,missingADCcorrMap]= numpy.NaN # (both Smpl and Rst) 
                #
                if verboseFlag: APy3_GENfuns.printcol("CDS", 'blue')
                data_CDS= data_ADCcorr[1:,iSmpl,:,:] - data_ADCcorr[:-1,iRst,:,:]
                if cleanMemFlag: del data_ADCcorr
                #
                if pedSubtractFlag:
                    if verboseFlag: APy3_GENfuns.printcol("subtracting pedestal", 'blue')
                    data_CDS= data_CDS-data_pedestal
                #
                if verboseFlag: APy3_GENfuns.printcol("avg", 'blue')
                data_CDSavg= numpy.average(data_CDS,axis=0)
                if cleanMemFlag: del data_CDS
            else: data_CDSavg= numpy.ones((NRow,NCol))*numpy.NaN
            # ---
            #
            #%% show
            if showFlag:
                if verboseFlag: APy3_GENfuns.printcol("showing", 'blue')
                APy3_P2Mfuns.percDebug_plot_interactive(dscrmbld_GnCrsFn, data_CDSavg, manyImgFlag)
            # ---
            #
            #%% save DLSraw to 1 file
            if saveFlag_1file:
                APy3_GENfuns.write_2xh5(outFolder+file_1file_out, Smpl_DLSraw,'/data', Rst_DLSraw,'/reset')
                if verboseFlag: APy3_GENfuns.printcol("descrambled file file saved: {0}".format(outFolder+file_1file_out), 'green')
            # ---
            #
            # save DLSraw to multiple files
            if saveFlag_multiFile:
                for iFile,thisFile in enumerate(metadata_content[:,1]): 
                    iImgStart= iFile*out_imgXFile_multiFile
                    iImgEndPlus1= (iFile+1)*out_imgXFile_multiFile
                    thisSmpl_DLSraw= numpy.copy(Smpl_DLSraw[iImgStart:iImgEndPlus1,:,:].astype('uint16'))
                    thisRst_DLSraw=  numpy.copy(Rst_DLSraw[ iImgStart:iImgEndPlus1,:,:].astype('uint16'))
                    APy3_GENfuns.write_2xh5(outFolder+thisFile+out_multiFile_suffix, 
                                            thisSmpl_DLSraw,'/data', 
                                            thisRst_DLSraw,'/reset')
                    if verboseFlag: APy3_GENfuns.printcol("{0}:{1} descrambled img saved in file: {2}".format(iImgStart,iImgEndPlus1,outFolder+thisFile+out_multiFile_suffix), 'green')
            # ---
            #
            # save CDS avg file
            if ADCcorrCDSFlag & saveAvgCDSFlag:
                file_AvgCDSfile_out= file_fl0[:auxN]+out_AvgCDSfile_suffix
                APy3_GENfuns.write_1xh5(outFolder+file_AvgCDSfile_out, data_CDSavg, '/data/data')
                if verboseFlag: APy3_GENfuns.printcol("CDS avg file file saved: {0}".format(outFolder+file_AvgCDSfile_out), 'green')
            #
            if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    #
    #%% that's all folks
    APy3_GENfuns.printcol("done",'blue')
    endTime=time.time()
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    if verboseFlag: APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
    #
    return dscrmbld_GnCrsFn




#
#---
#%% profile it
#import cProfile
#cProfile.run('descramble_highMem(...)', sort='cumtime')
#%% or just execute it
#descramble_highMem(...)
