# -*- coding: utf-8 -*-
"""
Descramble and visualize (and save )small scrambled dataset (seq Mod)

load environmentL on cfeld-perc02 is:
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root

python3 ./LookAtFLast.py
or:
start python
# execfile("WIP_UseFLastDLSraw_Fingerplot_WIP.py") # this is in python 2.7
exec(open("./LookAtFLast_FullImg_ADCcor_CDS_pedSub_avg.py").read()); print('Python3 is horrible')
"""
#%% imports and useful constants
from APy3_auxINIT import *
#
#
ERRint16=-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw= -0.1
ERRDLSraw= 65535 # forbidden uint16, usable to track "pixel" from missing pack
iGn=0; iCrs=1; iFn=2; NGnCrsFn=3 
iSmpl=0; iRst=1; NSmplRst=2
#
NGrp= 212
NADC=7; NRowInBlk=NADC
NColInBlk=32
NPad=45; NDataPad=NPad-1
NCol= NColInBlk*NPad
NRow= NADC*NGrp
NbitPerPix=15
#---
def descrambleLast(mainFolder, 
                   swapSmplRstFlag,seqModFlag, refColH1_0_Flag, 
                   ADCcorrFlag,CDSFlag,avgFlag,pedSubtractFlag,saveAvgFlag,
                   showFlag,saveFlag, detailFlag,cleanMemFlag):
    #%% what's up doc
    """
    descrambles h5-odinDAQ(raw) files, save to h5 in standard format and/or shows
    
    Here is how data are scrambled:
    
    1a) the chips send data out interleaving RowGroups
        (7row x (32 Col x 45 pads) ) from Sample/Reset, as:
        Smpl, Smpl,   Smpl, Rst, Smpl, Rst, ... , Smpl, Rst,   Rst, Rst
    1b) the position of pixels (pix0/1/2 in the next point) is mapped to
        the (7row x 32 Col) block according to the adc_cols lost
    1c) inside a (7row x 32 Col) block, the data are streamed out as:
        bit0-of-pix0, bit0-of-pix1, bit0-of-pix2, ... , bit0-of-pix1, ...
    1d) all the data coming from the sensor are bit-inverted: 0->1; 1->0
    2a) the mezzanine takes the data coming from each (7 x 32) block,
        and add a "0" it in front of every 15 bits:
        xxx xxxx xxxx xxxx  yyy ... => 0xxx xxxx xxxx xxxx 0yyy ...
    2b) the mezzanine takes the data coming from a 44x (7 x 32) blocks
        (this corresponds to a complete RowCrp, ignoring RefCol )
        and interleaves 32 bits at a time:
        32b-from-pad1, 32b-from-pad2, ... , 32b-from-pad44,
        next-32b-from-pad1, next-32b-from-pad2, ...
    2c) the mezzanine packs the bits in Bytes, and the Bytes in UDPackets
        4 UDPackets contain all the bits of a 44x (7 x 32) Rowgrp.
        A complete image (Smpl+Rst) = 1696 UDPackets
        each UDPack has 4928Byte of information, and 112Byte of header.
        each UDPack is univocally identified by the header:
        - which Img (frame) the packet belongs to
        - datatype: whether it is part of a Smpl/Rst (respect. 1 or 0)
        - subframenumber (0 or 1)
        - packetnumber (0:423), which determines the RowGrp the
        packet's data goes into
        there are 1696 packets in an image; a packet is identified by the
        triplet (datatype,subframenumber,packetnumber)
    3a) the packets are sent from 2 mezzanine links (some on one link, some
        on the other), and are saved to 2 h5 files by odinDAQ
    4a) OdinDAQ byte-swaps every 16-bit sequence (A8 B8 becomes B8 A8)
    5a) OdinDAQ rearranges the 4 quarters of each rowblock
    6a) OdinDAQ seems to invert Smpl and Rst
    
    Args:
        filenamepath_in0/1: name of scrambled h5 files
        output_fname: name of h5 descrambled file to generate
        save_file/debugFlag/clean_memory/verbose: no need to explain
    
    Returns:
        creates a h5 file (if save_file) in DLSraw standard format
            no explicit return()
    """
    #
    APy3_GENfuns.printcol("----------------",'blue')
    startTime=time.time()
    APy3_GENfuns.printcol("script starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    #---
    #%% ADCcor files
    ADCcorrFolder= '/home/prcvlusr/PercAuxiliaryTools/LookAtFLast/LookAtFLast_CalibParam/ADUcorr/'
    if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
    if ADCcorrFlag:
        ADCparam_validMap= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_ADCproc_Map.h5', '/data/data').astype(bool)
        ADCparam_crs_slope= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_crs_slope.h5', '/data/data')
        ADCparam_crs_offset= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_crs_offset.h5', '/data/data')
        ADCparam_fn_slope= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_fn_slope.h5', '/data/data')        
        ADCparam_fn_offset= APy3_GENfuns.read_1xh5(ADCcorrFolder+'ADCcor_fn_offset.h5', '/data/data')
        APy3_GENfuns.printcol("ADCcor files: {0}ADCcor _ADCproc_Map / _crs/fn _slope/offset.h5".format(ADCcorrFolder), 'green')
        #
        # modify load ADCparam to avoid /0
        goodPixMap= (ADCparam_validMap==True) 
        badPixMap= (ADCparam_validMap==False) 
        ADCparam_crs_offset[badPixMap]=1.0
        ADCparam_crs_slope[badPixMap]=1.0
        ADCparam_fn_offset[badPixMap]=1.0
        ADCparam_fn_slope[badPixMap]=1.0
    pedestalFolder= '/home/prcvlusr/PercAuxiliaryTools/LookAtFLast/LookAtFLast_CalibParam/Pedestal/'
    if pedestalFolder[-1]!='/': pedestalFolder+='/'
    if pedSubtractFlag:
        data_pedestal= APy3_GENfuns.read_1xh5(pedestalFolder+'Pedestal.h5', '/data/data') 
        APy3_GENfuns.printcol("pedestal: {0}Pedestal.h5".format(pedestalFolder), 'green')
    #---
    #%% find file 
    inputFile0= APy3_GENfuns.last_file(mainFolder,'*_fl0.h5')
    inputFile1= inputFile0[:-7]+'_fl1.h5'
    inputFiles=[inputFile0,inputFile1]
    APy3_GENfuns.printcol("will read files:", 'green')
    APy3_GENfuns.printcol(inputFiles[0], 'green')
    APy3_GENfuns.printcol(inputFiles[1], 'green')
    #---
    #%% read file
    APy3_GENfuns.clean()
    APy3_GENfuns.printcol("reading files", 'blue')
    if APy3_GENfuns.notFound(inputFiles[0]): APy3_GENfuns.printErr(inputFiles[0]+' not found')
    if APy3_GENfuns.notFound(inputFiles[1]): APy3_GENfuns.printErr(inputFiles[1]+' not found')
    
    (dataSmpl_fl0, dataRst_fl0) = APy3_GENfuns.read_2xh5(inputFiles[0], '/data','/reset')
    (dataSmpl_fl1, dataRst_fl1) = APy3_GENfuns.read_2xh5(inputFiles[1], '/data','/reset')
    (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
    (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
    NImg = NImg_fl0 + NImg_fl0
    APy3_GENfuns.printcol("{0}+{1} Img read from files".format(NImg_fl0,NImg_fl1), 'green')
    #---
    #%% combine in one array: Img0-from-fl0, Img0-from-fl1, Img1-from-fl0...
    scrmblSmpl= numpy.zeros( (NImg,aux_NRow,aux_NCol), dtype='uint16')
    scrmblRst= numpy.zeros_like(scrmblSmpl, dtype='uint16') 
    scrmblSmpl[0::2,:,:]= dataSmpl_fl0[:,:,:]
    scrmblSmpl[1::2,:,:]= dataSmpl_fl1[:,:,:]
    scrmblRst[0::2,:,:]=  dataRst_fl0[:,:,:]
    scrmblRst[1::2,:,:]=  dataRst_fl1[:,:,:]
    if cleanMemFlag: del dataSmpl_fl0; del dataRst_fl0; del dataSmpl_fl1; del dataRst_fl1
    #---
    #%% solving 4a DAQ-scrambling: byte swap in hex (By0,By1) => (By1,By0)
    APy3_GENfuns.printcol("solving DAQ-scrambling: byte-swapping and Smpl-Rst-swapping", 'blue')
    if swapSmplRstFlag:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
    else:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)    
    if cleanMemFlag: del scrmblSmpl; del scrmblRst
    # - - -
    #%% solving DAQ-scrambling: "pixel" reordering
    APy3_GENfuns.printcol("solving DAQ-scrambling: reordering subframes", 'blue')

    def convert_odin_daq_2_mezzanine(shot_in):
        ' descrambles the OdinDAQ-scrambling '
        (aux_n_img,aux_nrow,aux_ncol)= shot_in.shape
        aux_reord= shot_in.reshape((aux_n_img,NGrp,NADC,2,aux_ncol//2))
        aux_reord= numpy.transpose(aux_reord, (0,1,3,2,4))
        aux_reord= aux_reord.reshape((aux_n_img,NGrp,2,2,NADC*aux_ncol//4))
        aux_reordered = numpy.ones((aux_n_img,NGrp,4,NADC*aux_ncol//4), dtype='uint16') * ERRDLSraw
        aux_reordered[:,:,0,:]= aux_reord[:,:,0,0,:]
        aux_reordered[:,:,1,:]= aux_reord[:,:,1,0,:]
        aux_reordered[:,:,2,:]= aux_reord[:,:,0,1,:]
        aux_reordered[:,:,3,:]= aux_reord[:,:,1,1,:]
        aux_reordered= aux_reordered.reshape((aux_n_img,NGrp*NADC,aux_ncol))        
        return aux_reordered
    #
    data2srcmbl_noRefCol= numpy.ones((NImg,NSmplRst,NRow,aux_NCol), dtype='uint16') * ERRDLSraw
    data2srcmbl_noRefCol[:,iSmpl,:,:]= scrmblSmpl_byteSwap
    data2srcmbl_noRefCol[:,iRst,:,:] = scrmblRst_byteSwap
    if cleanMemFlag: del scrmblSmpl_byteSwap; del scrmblRst_byteSwap
    #
    data2srcmbl_noRefCol= data2srcmbl_noRefCol.reshape((NImg,NSmplRst,NGrp,NADC,aux_NCol))
    #
    # track missing packets: False==RowGrp OK; True== packet(s) missing makes rowgroup moot
    # (1111 1111 1111 1111 instead of 0xxx xxxx xxxx xxxx)
    missingRowGrp_Tracker = data2srcmbl_noRefCol[:,:,:,0,0] == ERRDLSraw
    # - - -    
    #%% descramble proper
    APy3_GENfuns.printcol("solving mezzanine&chip-scrambling: pixel descrambling", 'blue')
    multiImgWithRefCol= numpy.zeros((NImg,NSmplRst,NGrp,NPad,NADC*NColInBlk,NGnCrsFn), dtype='int16')
    #
    # refCol
    multiImgWithRefCol[:,:,:,0,:,:]= ERRint16
    #
    data2srcmbl_noRefCol= data2srcmbl_noRefCol.reshape((NImg,NSmplRst,NGrp,NADC*aux_NCol //(NDataPad*2),NDataPad,2)) # 32bit=2"pix" from 1st pad, 2"pix" from 2nd pad, ...
    data2srcmbl_noRefCol= numpy.transpose(data2srcmbl_noRefCol, (0,1,2,4,3,5)).reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*aux_NCol//NDataPad)) # (NSmplRst,NGrp,NDataPad,NADC*aux_NCol//NDataPad)
    theseImg_bitted= APy3_GENfuns.convert_uint_2_bits_Ar(data2srcmbl_noRefCol,16)[:,:,:,:,:,-2::-1].astype('uint8') # n_smplrst,n_grp,n_data_pads,n_adc*aux_ncol//n_data_pads,15bits
    if cleanMemFlag: del data2srcmbl_noRefCol
    theseImg_bitted= theseImg_bitted.reshape((NImg, NSmplRst,NGrp,NDataPad,NbitPerPix,NADC*NColInBlk))
    theseImg_bitted= numpy.transpose(theseImg_bitted,(0,1,2,3,5,4)) # (NImg, n_smplrst,n_grp,n_data_pads,NPixsInRowBlk,15)
    theseImg_bitted= APy3_GENfuns.convert_britishBits_Ar(theseImg_bitted).reshape((NImg, NSmplRst*NGrp*NDataPad*NADC*NColInBlk, NbitPerPix))
    #
    theseImg_bitted=theseImg_bitted.reshape((NImg*NSmplRst*NGrp*NDataPad*NADC*NColInBlk, NbitPerPix))
    (aux_coarse,aux_fine,aux_gain)= APy3_P2Mfuns.aggregate_to_GnCrsFn( APy3_GENfuns.convert_bits_2_uint16_Ar(theseImg_bitted[:,::-1]) )
    multiImgWithRefCol[:,:,:,1:,:,iGn]=  aux_gain.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    multiImgWithRefCol[:,:,:,1:,:,iCrs]= aux_coarse.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    multiImgWithRefCol[:,:,:,1:,:,iFn]=  aux_fine.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    if cleanMemFlag: del aux_gain; del aux_coarse; del aux_fine; del theseImg_bitted    
    #
    # - - -
    #
    #%% reorder pixels and pads
    APy3_GENfuns.printcol("solving chip-scrambling: pixel reordering", 'blue')
    multiImg_Grp_dscrmbld= APy3_P2Mfuns.reorder_pixels_GnCrsFn_par(multiImgWithRefCol,NADC,NColInBlk)
    # - - -        
    #
    # add error tracking
    APy3_GENfuns.printcol("lost packet tracking", 'blue')
    multiImg_Grp_dscrmbld= multiImg_Grp_dscrmbld.astype('int16') # -256 upto 255
    for iImg in range(NImg):
        for iGrp in range(NGrp):
            for iSmplRst in range(NSmplRst):
                if (missingRowGrp_Tracker[iImg,iSmplRst,iGrp]):
                    multiImg_Grp_dscrmbld[iImg,iSmplRst,iGrp,:,:,:,:]= ERRint16
                    
    # also err tracking for ref col
    multiImg_Grp_dscrmbld[:,:,:,0,:,:,:]= ERRint16
    if refColH1_0_Flag:
        APy3_GENfuns.printcol("moving RefCol data to G", 'blue')
        multiImg_Grp_dscrmbld[:,:,:,0,:,:,:]= multiImg_Grp_dscrmbld[:,:,:,44,:,:,:]
        multiImg_Grp_dscrmbld[:,:,:,44,:,:,:]= ERRint16
    # - - -
    #
    # reshaping as an Img array: (NImg,Smpl/Rst,n_grp,n_adc,n_pad,NColInBlk,Gn/Crs/Fn)
    dscrmbld_GnCrsFn = numpy.transpose(multiImg_Grp_dscrmbld, (0,1,2,4,3,5,6)).astype('int16').reshape((NImg,NSmplRst, NGrp*NADC,NPad*NColInBlk, NGnCrsFn))
    if cleanMemFlag: del multiImg_Grp_dscrmbld 
    # - - -
    #
    #%% reorder rowgrp (SeqMode) if needed
    if seqModFlag:
        APy3_GENfuns.printcol("rearranging RowGroup as per seqMod acquired with a stdMod Firmware", 'blue')
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp,NADC, NCol,NGnCrsFn))
        aux_Seq= numpy.ones_like(dscrmbld_GnCrsFn, dtype='int16') * ERRint16
        aux_Seq[:,:,1:106,:,:,:]= dscrmbld_GnCrsFn[:,:,2:212:2,:,:,:]
        dscrmbld_GnCrsFn[:,:,:,:,:,:]= aux_Seq[:,:,:,:,:,:]
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp*NADC, NCol,NGnCrsFn))
        if cleanMemFlag: del aux_Seq
    dscmblTime=time.time()
    if detailFlag: APy3_GENfuns.printcol("descrambling ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    if detailFlag: APy3_GENfuns.printcol("scripts took {0} sec to descramble images".format(dscmblTime-startTime),'green')
    # - - -
    #
    #%% show descrambled data GnCrsFn
    if showFlag and not(ADCcorrFlag):
        APy3_GENfuns.printcol("showing images", 'blue')
        nextstep='0'; thisImg=-1
        APy3_GENfuns.printcol("press [N]ext/[P]revious/[0-9 image number]/[E]nd", 'blue')
        nextstep = APy3_GENfuns.press_any_key()
        while nextstep not in ['e','E','q','Q']:
            matplotlib.pyplot.close()
            #
            if nextstep in ['n','N',' ']: thisImg+=1; #APy3_GENfuns.printcol("next image: {0}".format(thisImg), 'yellow')
            elif nextstep in ['p','P']: thisImg-=1; #APy3_GENfuns.printcol("previous image: {0}".format(thisImg), 'yellow')
            elif nextstep.isdigit(): thisImg= int(nextstep); #APy3_GENfuns.printcol("image: {0}".format(thisImg), 'yellow')

            if thisImg>=NImg: thisImg= thisImg%NImg
            if thisImg<0: thisImg= thisImg%NImg
            #
            aux_title = "Img " + str(thisImg)
            aux_err_below = -0.1
            APy3_P2Mfuns.percDebug_plot_6x2D(
                dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iGn],
                dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iCrs],
                dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iFn],
                dscrmbld_GnCrsFn[thisImg,iRst,:,:,iGn],
                dscrmbld_GnCrsFn[thisImg,iRst,:,:,iCrs],
                dscrmbld_GnCrsFn[thisImg,iRst,:,:,iFn],
                aux_title, aux_err_below)
            APy3_GENfuns.maximize_plot() 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom
            #
            APy3_GENfuns.printcol("press [N]ext/[P]revious/[0-9 image number]/[E]nd", 'blue')
            nextstep = APy3_GENfuns.press_any_key()
            #nextstep = input("[N]ext/[P]revious/[image number]/[E]nd: ")
            if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
    # - - -
    #
    #%% save descrambled data GnCrsFn
    if saveFlag and not(ADCcorrFlag):
        APy3_GENfuns.printcol("converting to DLSraw", 'blue')
        (Smpl_DLSraw, Rst_DLSraw)= APy3_P2Mfuns.convert_GnCrsFn_2_DLSraw(dscrmbld_GnCrsFn, ERRint16, ERRDLSraw)
        #
        APy3_GENfuns.printcol("saving descrambled file", 'blue')
        outFile=inputFiles[0][:-6]+"dscrmbld_DLSraw.h5"
        APy3_GENfuns.write_2xh5(outFile, Smpl_DLSraw,'/data', Rst_DLSraw,'/reset')
        APy3_GENfuns.printcol("descrambled data saved in {0}".format(outFile), 'green')
    # - - -
    #
    #%% ADCcor
    if ADCcorrFlag: 
        APy3_GENfuns.printcol("ADC-correcting", 'blue')
        (ignNimg,ignSmplRst, auxNRow,auxNCol, ignGnCrsFn)=dscrmbld_GnCrsFn.shape
        data_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                                  ADCparam_crs_slope,ADCparam_crs_offset,ADCparam_fn_slope,ADCparam_fn_offset, auxNRow,auxNCol)
        ADCcorTime=time.time()
        if detailFlag: APy3_GENfuns.printcol("scripts took {0} sec to ADC-correct images".format(ADCcorTime-dscmblTime),'green')
        if showFlag and not CDSFlag:
            APy3_GENfuns.printcol("showing images", 'blue')
            for thisImg in range(NImg):
                aux_title = "Img " + str(thisImg)
                APy3_P2Mfuns.percDebug_plot_2x2D_map(data_ADCcorr[thisImg,iSmpl,:,:],data_ADCcorr[thisImg,iRst,:,:], goodPixMap,
                                                 'Sample[ADU]','Reset[ADU]',aux_title+' ADC-corrected')
                APy3_GENfuns.maximize_plot() #maximize window
                matplotlib.pyplot.show(block=True)
        #
        #%% flagging bad pixels    
        APy3_GENfuns.printcol("flagging bad pixels", 'blue')
        # set the missing vales to NaN
        missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
        data_ADCcorr[missingValMap]= numpy.NaN
        # set bad ADCcal values to NaN
        missingADCcorrMap= ADCparam_validMap==False
        data_ADCcorr[:,:,missingADCcorrMap]= numpy.NaN # (bothSmpl and Rst)
        # - - -
        #
        #%% CDS
        if CDSFlag: 
            data_CDS= data_ADCcorr[1:,iSmpl,:,:] - data_ADCcorr[:-1,iRst,:,:]
            if showFlag and not avgFlag:
                APy3_GENfuns.printcol("showing images", 'blue')
                (auxNImg,ignNRow,ignNCol)= data_CDS.shape
                for thisImg in range(auxNImg):
                    aux_title = "Img " + str(thisImg)
                    APy3_P2Mfuns.percDebug_plot_2x2D_map(data_CDS[thisImg,:,:],dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iGn].astype(float), goodPixMap,
                                                 'CDS [ADU]','Gn (Smpl)',aux_title+' CDS')
                    #maximize window
                    APy3_GENfuns.maximize_plot() #maximize window
                    matplotlib.pyplot.show(block=True)
            # - - -
            #
            #%% avg
            if avgFlag: 
                data_avg= numpy.average(data_CDS,axis=0)
                if pedSubtractFlag:
                    data_avg= data_avg-data_pedestal
                    APy3_GENfuns.printcol("subtracting pedestal", 'blue')
                avgTime=time.time()
                if detailFlag: APy3_GENfuns.printcol("script took {0} sec to CDS and avg images".format(avgTime-ADCcorTime),'green')
                APy3_GENfuns.printcol("script took total of {0} sec to load and process images".format(avgTime-startTime),'green')
                if showFlag:
                    thisImg=-1
                    APy3_GENfuns.printcol("plot [C]DS in lin / [L]og scale / 1st [R]aw image / [N]ext raw image / [P]revious raw image / [0-9] raw image / [E]nd", 'black')
                    nextstep = APy3_GENfuns.press_any_key()
                    #
                    while nextstep not in ['e','E','q','Q']:
                        matplotlib.pyplot.close()
                        #
                        if nextstep in ['c','C','l','L']: APy3_GENfuns.printcol("showing CDS, close image to move on".format(thisImg), 'black')
                        elif nextstep in ['n','N', ' ']: thisImg+=1; APy3_GENfuns.printcol("showing Raw: Img {0}, close image to move on".format(thisImg), 'black')
                        elif nextstep in ['p','P']: thisImg-=1; APy3_GENfuns.printcol("showing Raw: image: {0}, close image to move on".format(thisImg), 'black')
                        elif nextstep.isdigit(): thisImg= int(nextstep); APy3_GENfuns.printcol("showing Raw: image: {0}, close image to move on".format(thisImg), 'black')
                        #
                        #if (nextstep not in ['c','C'])&((thisImg>=NImg)|thisImg<0): thisImg= thisImg%NImg
                        if (thisImg>=NImg): thisImg= thisImg%NImg
                        if (thisImg<0): thisImg= thisImg%NImg
                        #
                        if nextstep in ['c','C','l','L']:
                            if nextstep in ['l','L']: logScaleFlag=True
                            else: logScaleFlag= False
                            APy3_GENfuns.plot_2D_all(data_avg, logScaleFlag, 'col','row','avg CDS [ADU]', True) 
                            APy3_GENfuns.maximize_plot() 
                            matplotlib.pyplot.show(block=True) # to allow for interactive zoom 
                        else:
                            aux_title = "Img " + str(thisImg)
                            aux_err_below = -0.1
                            APy3_P2Mfuns.percDebug_plot_6x2D(dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iGn],dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iCrs],dscrmbld_GnCrsFn[thisImg,iSmpl,:,:,iFn],
                                                             dscrmbld_GnCrsFn[thisImg,iRst,:,:,iGn], dscrmbld_GnCrsFn[thisImg,iRst,:,:,iCrs], dscrmbld_GnCrsFn[thisImg,iRst,:,:,iFn],
                                                             aux_title, aux_err_below)
                            APy3_GENfuns.maximize_plot() 
                            matplotlib.pyplot.show(block=True) # to allow for interactive zoom
                        #
                        APy3_GENfuns.printcol("plot [C]DS in lin / [L]og scale / [0-9] raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
                        nextstep = APy3_GENfuns.press_any_key()
                        #nextstep = input("[N]ext/[P]revious/[image number]/[E]nd: ")
                        if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue') 
            # ---
            #
            # % save avg%
            if saveAvgFlag:
                APy3_GENfuns.printcol("saving CDS averaged file", 'blue')
                outFile_CDS=inputFiles[0][:-6]+"CDS_avg.h5"
                APy3_GENfuns.write_1xh5(outFile_CDS, data_avg, '/data/data')
                APy3_GENfuns.printcol("CDS averaged data saved in {0}".format(outFile_CDS), 'green')
    #---
    #
    #%% that's all folks
    APy3_GENfuns.printcol("done",'blue')
    endTime=time.time()
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    #APy3_GENfuns.printcol("scripts took {0} sec".format(endTime-startTime),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
    return dscrmbld_GnCrsFn
#---
#%% profile it
#import cProfile
#cProfile.run('auxdata= descrambleLast(mainFolder, swapSmplRstFlag,seqModFlag,refColH1_0_Flag, showFlag,saveFlag, cleanMemFlag)', sort='cumtime')
#---
#%% or just execute it
#auxdata= descrambleLast(mainFolder, swapSmplRstFlag,seqModFlag,refColH1_0_Flag, showFlag,saveFlag, cleanMemFlag)
