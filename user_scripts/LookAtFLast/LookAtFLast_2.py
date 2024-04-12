#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Descramble and visualize small scrambled dataset (seq Mod)

for PhScStorage

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3

python3 ./LookAtFLast_2.py
or:
start python
# execfile("xxx.py") # this is in python 2.7
exec(open("./xxx.py").read()); print('Python3 is horrible')
"""

#%% imports and useful constants
from APy3_auxINIT import *
from APy3_P2Mfuns import *
numpy.seterr(divide='ignore', invalid='ignore')
#
interactiveFlag= False; interactiveFlag= True
#
def percDebug_plot_interactive_wCMA_2(data_GnCrsFn,data_CDSavg,data_CDSCMAavg, manyImgFlag):
    (NImg,ignSR,ignR,ignC,ign3)= data_GnCrsFn.shape
    thisImg=-1
    APy3_GENfuns.printcol("plot [C]DS in lin/[L]og scale / CDS-C[M]A in lin/lo[G] scale / [number] of raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
    if manyImgFlag: nextstep = input()
    else: nextstep = APy3_GENfuns.press_any_key()
    aux_add=0.0
    #
    while nextstep not in ['e','E','q','Q']:
        matplotlib.pyplot.close()
        #

        if nextstep in ['c','C','l','L']: APy3_GENfuns.printcol("showing CDS, close image to move on".format(thisImg), 'black')
        elif nextstep in ['n','N', ' ']: thisImg+=1; APy3_GENfuns.printcol("showing Raw: Img {0}, close image to move on".format(thisImg), 'black')
        elif nextstep in ['p','P']: thisImg-=1; APy3_GENfuns.printcol("showing Raw: image: {0}, close image to move on".format(thisImg), 'black')
        elif nextstep.isdigit(): thisImg= int(nextstep); APy3_GENfuns.printcol("showing Raw: image: {0}, close image to move on".format(thisImg), 'black')
        #
        if (thisImg>=NImg): thisImg= thisImg%NImg
        if (thisImg<0): thisImg= thisImg%NImg
        #
        if nextstep in ['c','C','l','L']:
            if nextstep in ['l','L']: logScaleFlag=True
            else: logScaleFlag= False
            APy3_GENfuns.plot_2D_all(data_CDSavg, logScaleFlag, 'col','row','avg CDS [ADU]', True) 
            APy3_GENfuns.maximize_plot() 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom 
        elif nextstep in ['m','M','g','G']:
            if nextstep in ['g','G']: logScaleFlag=True
            else: logScaleFlag= False
            APy3_GENfuns.plot_2D_all(data_CDSCMAavg, logScaleFlag, 'col','row','avg CDS-CMA [ADU]', True) 
            APy3_GENfuns.maximize_plot() 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom 
        elif nextstep in ['a','A']:
            APy3_GENfuns.printcol("easter egg: show (avg+added constant) in log scale", 'green')
            APy3_GENfuns.printcol("value for added constant [is now {0}]".format(aux_add), 'green')
            aux_add_str= input()
            if aux_add_str.isdigit(): 
                aux_add= float(aux_add_str)
                APy3_GENfuns.printcol("new value for added constant is now {0}".format(aux_add), 'green')
            else: APy3_GENfuns.printcol("will keep value for added constant = {0}".format(aux_add), 'green')
            APy3_GENfuns.plot_2D_all(data_CDSavg+aux_add, True, 'col','row','avg CDS +{0} [ADU]'.format(aux_add), True) 
            APy3_GENfuns.plot_2D_all(data_CDSCMAavg+aux_add, True, 'col','row','avg CDS-CMA +{0} [ADU]'.format(aux_add), True) 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom 
        else:
            aux_title = "Img " + str(thisImg)
            aux_err_below = -0.1
            percDebug_plot_6x2D(data_GnCrsFn[thisImg,iSmpl,:,:,iGn],data_GnCrsFn[thisImg,iSmpl,:,:,iCrs],data_GnCrsFn[thisImg,iSmpl,:,:,iFn],
                                data_GnCrsFn[thisImg,iRst,:,:,iGn], data_GnCrsFn[thisImg,iRst,:,:,iCrs], data_GnCrsFn[thisImg,iRst,:,:,iFn],
                                aux_title, aux_err_below)
            APy3_GENfuns.maximize_plot() 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
        APy3_GENfuns.printcol("plot [C]DS in lin/[L]og scale / CDS-C[M]A in lin/lo[G] scale / [number] of raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
        if manyImgFlag: nextstep = input()
        else: nextstep = APy3_GENfuns.press_any_key()
        if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue') 
    return



#
#---
#
#%% parameters
#dflt_mainFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/'
#dflt_mainFolder='/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/raw/'
#dflt_mainFolder='/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/scratch_bl/'
#
dflt_mainFolder='/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010254/raw/'
dflt_mainFolder='/dls/detectors/Percival/captures/'
#dflt_mainFolder='/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010254/scratch_bl/'
#
if dflt_mainFolder[-1]!='/': dflt_mainFolder+='/'
dflt_suffix_fl0='_000000.h5'
dflt_suffix_fl1='_000001.h5'
#dflt_img2proc_str= "0:9" # using the sensible matlab convention; "all",":","*" means all
dflt_img2proc_str= ":" # using the sensible matlab convention; "all",":","*" means all
#
dflt_swapSmplRstFlag= False;
dflt_seqModFlag= False # this actually mean: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
dflt_refColH0_21_Flag = False # True if refcol data are streamed out as H0<21> data.
dflt_cleanMemFlag= True # this actually mean: save descrambled image (DLSraw standard)
dflt_verboseFlag= True
dflt_wantDescramble = False;
#
dflt_ADCcorrFlag=False
ADCcorrFolder= '/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
dflt_ADUcorr_file= ADCcorrFolder+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'

#
dflt_pedSubtractFlag=False
#dflt_pedestal_CDSavg= dflt_mainFolder+'aux_CDS_avg.h5'
#dflt_pedestal_CDSavg= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_Tm20_drk/avg_std/'+'2019.11.25.19.50.41_BSI04_Tm20_dmuxSELsw_biasBSI04_02_3TGn0PGABBB_1kdrk_CDS_avg.h5'
#dflt_pedestal_CDSavg= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_Tm20_drk/avg_std/'+'2019.11.28.16.13.40_BSI04_Tm20_dmuxSELsw_biasBSI04_03_3TGn0_PGA666_1kdrk_CDS_avg.h5'
#
# beamtime P04 2019.12.11: pedestal 3G,PGABBB,7/7ADC
#dflt_pedestal_CDSavg= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/Pedestals/'+'2019.12.11.14.23.36_BSI04_7of7_3GPGABBB_012ms_toCreatePedestal_1kdrk_Gn0_CDS_ADU_drkavg.h5'
#
# beamtime P04 2019.12.11: pedestal 3T,PGA666,7/7ADC
dflt_pedestal_CDSavg= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/Pedestals/'+'2019.12.11.14.27.15_BSI04_7of7_3TPGA666_012ms_toCreatePedestal_1kdrk_Gn0_CDS_ADU_drkavg.h5'
#
dflt_cols2CMA_str= "32:63"
#
dflt_saveFlag= False
dflt_outFile=dflt_mainFolder+'aux_CDS_avg.h5'
#---
#
#%% functs
#
def read_partial_2xh5(filenamepath, path1_2read, path2_2read, fromImg, toImg):
    ''' read 2xXD h5 file (paths_2read: '/data/','/reset/' ) '''
    my5hfile= h5py.File(filenamepath, 'r')
    myh5dataset=my5hfile[path1_2read]
    if myh5dataset.shape[0] <= toImg: my5hfile.close(); APy3_GENfuns.printErr('only {0} img in fl0 file'.format(myh5dataset.shape[0]))
    my_data1= numpy.array(myh5dataset[fromImg:toImg+1,...])
    myh5dataset=my5hfile[path2_2read]
    if myh5dataset.shape[0] <= toImg: my5hfile.close(); APy3_GENfuns.printErr('only {0} img in fl1 file'.format(myh5dataset.shape[0]))
    my_data2= numpy.array(myh5dataset[fromImg:toImg+1,...])
    my5hfile.close()
    return (my_data1,my_data2)
#
def loadSomeImagesFromlast(mainFolder, img2proc_str, 
                           suffix_fl0, suffix_fl1,
                           verboseFlag):
    """ load some images from last file """
    #%% find file 
    suffLength= len(suffix_fl0)
    inputFile0= APy3_GENfuns.last_file(mainFolder,'*'+suffix_fl0)
    inputFile1= inputFile0[:-1*suffLength]+suffix_fl1
    inputFiles=[inputFile0,inputFile1]
    if verboseFlag:
        APy3_GENfuns.printcol("will read files:", 'green')
        APy3_GENfuns.printcol(inputFiles[0], 'green')
        APy3_GENfuns.printcol(inputFiles[1], 'green')
    #---
    #%% read file
    APy3_GENfuns.clean()
    if verboseFlag: APy3_GENfuns.printcol("reading files", 'blue')
    if APy3_GENfuns.notFound(inputFiles[0]): APy3_GENfuns.printErr(inputFiles[0]+' not found')
    if APy3_GENfuns.notFound(inputFiles[1]): APy3_GENfuns.printErr(inputFiles[1]+' not found')
    
    if img2proc_str in ['all','All','ALL',':','*','-1']: 
        if verboseFlag: APy3_GENfuns.printcol("will read all Img", 'green')
        (dataSmpl_fl0, dataRst_fl0) = APy3_GENfuns.read_2xh5(inputFiles[0], '/data/','/reset/')
        (dataSmpl_fl1, dataRst_fl1) = APy3_GENfuns.read_2xh5(inputFiles[1], '/data/','/reset/')
    else:
        img2proc= APy3_GENfuns.matlabLike_range(img2proc_str)
        fromImg_fl01= img2proc[0]//2
        toImg_fl01=(img2proc[-1]//2)
        if verboseFlag:
            APy3_GENfuns.printcol("will read img {0} to {1} in both files".format(fromImg_fl01,toImg_fl01), 'green')
            APy3_GENfuns.printcol("corresponding overall to img {0}".format(str(img2proc)), 'green')
        (dataSmpl_fl0, dataRst_fl0) = read_partial_2xh5(inputFiles[0], '/data/','/reset/', fromImg_fl01,toImg_fl01)
        (dataSmpl_fl1, dataRst_fl1) = read_partial_2xh5(inputFiles[1], '/data/','/reset/', fromImg_fl01,toImg_fl01)
    #
    (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
    (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
    NImg = NImg_fl0 + NImg_fl0
    if verboseFlag: APy3_GENfuns.printcol("{0}+{1} Img read from files".format(NImg_fl0,NImg_fl1), 'green')
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
    return (scrmblSmpl,scrmblRst)
#
def descrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH0_21_Flag, 
                   cleanMemFlag, verboseFlag):
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
        5D array, descrambled (Img,Smpl/Rst,Row,Col,Gn/Crs/Fn)
    """
    #
    startTime=time.time()
    (NImg, aux_NRow, aux_NCol) = scrmblSmpl.shape
    #---
    #%% solving 4a DAQ-scrambling: byte swap in hex (By0,By1) => (By1,By0)
    if verboseFlag: APy3_GENfuns.printcol("solving DAQ-scrambling: byte-swapping and Smpl-Rst-swapping", 'blue')
    if swapSmplRstFlag:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
    else:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)    
    if cleanMemFlag: del scrmblSmpl; del scrmblRst
    # - - -
    #%% solving DAQ-scrambling: "pixel" reordering
    if verboseFlag: APy3_GENfuns.printcol("solving DAQ-scrambling: reordering subframes", 'blue')

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
    if verboseFlag: APy3_GENfuns.printcol("solving mezzanine&chip-scrambling: pixel descrambling", 'blue')
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
    # - - -
    #
    #%% reorder pixels and pads
    if verboseFlag: APy3_GENfuns.printcol("solving chip-scrambling: pixel reordering", 'blue')
    multiImg_Grp_dscrmbld= APy3_P2Mfuns.reorder_pixels_GnCrsFn_par(multiImgWithRefCol,NADC,NColInBlk)
    # - - -        
    #
    # add error tracking
    if verboseFlag: APy3_GENfuns.printcol("lost packet tracking", 'blue')
    multiImg_Grp_dscrmbld= multiImg_Grp_dscrmbld.astype('int16') # -256 upto 255
    for iImg in range(NImg):
        for iGrp in range(NGrp):
            for iSmplRst in range(NSmplRst):
                if (missingRowGrp_Tracker[iImg,iSmplRst,iGrp]):
                    multiImg_Grp_dscrmbld[iImg,iSmplRst,iGrp,:,:,:,:]= ERRint16
                    
    # also err tracking for ref col
    multiImg_Grp_dscrmbld[:,:,:,0,:,:,:]= ERRint16
    if refColH0_21_Flag:
        if verboseFlag: APy3_GENfuns.printcol("moving RefCol data to G", 'blue')
        multiImg_Grp_dscrmbld[:,:,:,0,:,:,:]= multiImg_Grp_dscrmbld[:,:,:,1,:,:,:]
        multiImg_Grp_dscrmbld[:,:,:,1,:,:,:]= ERRint16
    # - - -
    #
    # reshaping as an Img array: (NImg,Smpl/Rst,n_grp,n_adc,n_pad,NColInBlk,Gn/Crs/Fn)
    dscrmbld_GnCrsFn = numpy.transpose(multiImg_Grp_dscrmbld, (0,1,2,4,3,5,6)).astype('int16').reshape((NImg,NSmplRst, NGrp*NADC,NPad*NColInBlk, NGnCrsFn))
    if cleanMemFlag: del multiImg_Grp_dscrmbld 
    # - - -
    #
    #%% reorder rowgrp (SeqMode) if needed
    if seqModFlag:
        if verboseFlag: APy3_GENfuns.printcol("rearranging RowGroup as per seqMod acquired with a stdMod Firmware", 'blue')
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp,NADC, NCol,NGnCrsFn))
        aux_Seq= numpy.ones_like(dscrmbld_GnCrsFn, dtype='int16') * ERRint16
        aux_Seq[:,:,1:106,:,:,:]= dscrmbld_GnCrsFn[:,:,2:212:2,:,:,:]
        dscrmbld_GnCrsFn[:,:,:,:,:,:]= aux_Seq[:,:,:,:,:,:]
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp*NADC, NCol,NGnCrsFn))
        if cleanMemFlag: del aux_Seq
    dscmblTime=time.time()
    if verboseFlag: 
        APy3_GENfuns.printcol("descrambling ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
        APy3_GENfuns.printcol("scripts took {0} sec to descramble images".format(dscmblTime-startTime),'green')
    return dscrmbld_GnCrsFn

def NOTdescrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH1_0_Flag, 
                   cleanMemFlag, verboseFlag):

    startTime=time.time()
    (NImg, aux_NRow, aux_NCol) = scrmblSmpl.shape

    if swapSmplRstFlag:
        aux_scrmblSmpl= numpy.copy(scrmblRst)
        aux_scrmblRst = numpy.copy(scrmblSmpl)
        #
        scrmblSmpl = numpy.copy(aux_scrmblSmpl)
        scrmblRst= numpy.copy(aux_scrmblRst)
        del aux_scrmblSmpl; del aux_scrmblRst


    #%% add RefCol
    scrmblSmpl_wRefCol= numpy.ones((NImg,NRow,NCol), dtype='uint16') * ERRDLSraw
    scrmblRst_wRefCol=  numpy.ones((NImg,NRow,NCol), dtype='uint16') * ERRDLSraw    
    scrmblSmpl_wRefCol[:,:,32:]= numpy.copy(scrmblSmpl[:,:,:])
    scrmblRst_wRefCol[:,:,32:]=  numpy.copy(scrmblRst[:,:,:])
    del scrmblSmpl; del scrmblRst
    dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(scrmblSmpl_wRefCol, scrmblRst_wRefCol, APy3_P2Mfuns.ERRDLSraw, APy3_P2Mfuns.ERRint16)
    #
    # mask RefCol
    dscrmbld_GnCrsFn[:,:,:,:32,:]=APy3_P2Mfuns.ERRint16
    #
    return dscrmbld_GnCrsFn

#
def ADCcorr_local(dscrmbld_GnCrsFn,
                  ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                  ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset):
    #
    (NImg,ignSR,ignNR,ignNR,ignNGCF)= dscrmbld_GnCrsFn.shape
    data_ADCcorr= numpy.zeros((NImg,NSmplRst,NRow,NCol))*numpy.NaN
    data_ADCcorr[:,iSmpl,:,:]= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iSmpl,:,:,iCrs],dscrmbld_GnCrsFn[:,iSmpl,:,:,iFn],
                                                 ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl
    data_ADCcorr[:,iRst,:,:]=  ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs], dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                              ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, NRow,NCol) # Rst
    return data_ADCcorr
#
#---
#
#%% parameter loading
if interactiveFlag:
    # interactive GUI
    GUIwin_arguments= []
    GUIwin_arguments+= ['data to process are in folder'];  GUIwin_arguments+= [dflt_mainFolder] 
    GUIwin_arguments+= ['suffix file_0'];                  GUIwin_arguments+= [dflt_suffix_fl0]
    GUIwin_arguments+= ['suffix file_1'];                  GUIwin_arguments+= [dflt_suffix_fl1]
    GUIwin_arguments+= ['images [first:last]'];            GUIwin_arguments+= [dflt_img2proc_str]

    GUIwin_arguments+= ['swap Smpl/Rst images? [Y/N]'];    GUIwin_arguments+= [str(dflt_swapSmplRstFlag)]
    GUIwin_arguments+= ['Seq with std Mezz_Firm? [Y/N]'];  GUIwin_arguments+= [str(dflt_seqModFlag)]
    GUIwin_arguments+= ['refCol in H0<21>? [Y/N]'];         GUIwin_arguments+= [str(dflt_refColH0_21_Flag)]
    GUIwin_arguments+= ['Descramble? [Y/N]'];              GUIwin_arguments+= [str(dflt_wantDescramble)]
    GUIwin_arguments+= ['ADC correction? [Y/N]'];          GUIwin_arguments+= [str(dflt_ADCcorrFlag)]
    GUIwin_arguments+= ['ADCcor (path and) file'];         GUIwin_arguments+= [dflt_ADUcorr_file]

    GUIwin_arguments+= ['pedestal-subtract? [Y/N]'];       GUIwin_arguments+= [str(dflt_pedSubtractFlag)]
    GUIwin_arguments+= ['if pedestal: pedestal CDS-avg'];  GUIwin_arguments+= [dflt_pedestal_CDSavg]  

    GUIwin_arguments+= ['RefCols for CMA [first:last]'];   GUIwin_arguments+= [dflt_cols2CMA_str]

    GUIwin_arguments+= ['save CDS avg? [Y/N]'];        GUIwin_arguments+= [str(dflt_saveFlag)]
    GUIwin_arguments+= ['if save CDS avg: as (path and file)'];              GUIwin_arguments+= [str(dflt_outFile)]

    GUIwin_arguments+= ['clean mem when possible [Y/N]'];  GUIwin_arguments+= [str(dflt_cleanMemFlag)]
    GUIwin_arguments+= ['verbose? [Y/N]'];                 GUIwin_arguments+= [str(dflt_verboseFlag)]
    #
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    mainFolder= dataFromUser[i_param]; i_param+=1
    suffix_fl0= dataFromUser[i_param]; i_param+=1
    suffix_fl1= dataFromUser[i_param]; i_param+=1
    img2proc_str= dataFromUser[i_param]; i_param+=1
    #
    swapSmplRstFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    seqModFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    refColH0_21_Flag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #
    wantDescramble = APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #
    ADCcorrFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    ADUcorr_file= dataFromUser[i_param]; i_param+=1
    #
    pedSubtractFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    pedestalCDSFile= dataFromUser[i_param]; i_param+=1
    #
    cols2CMA = APy3_GENfuns.matlabLike_range(dataFromUser[i_param]); i_param+=1
    #
    saveFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    outFile= dataFromUser[i_param]; i_param+=1
    #
    cleanMemFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
else:
    # not interactive
    mainFolder=dflt_mainFolder
    suffix_fl0= dflt_suffix_fl0
    suffix_fl1= dflt_suffix_fl1
    img2proc_str= dflt_img2proc_str
    #
    swapSmplRstFlag= dflt_swapSmplRstFlag
    seqModFlag= dflt_seqModFlag
    refColH0_21_Flag= dflt_refColH0_21_Flag
    cleanMemFlag= dflt_cleanMemFlag
    verboseFlag= dflt_verboseFlag
    #
    wantDescramble = dflt_wantDescramble;
    ADCcorrFlag= dflt_ADCcorrFlag
    ADUcorr_file= dflt_ADUcorr_file
    #
    pedSubtractFlag= dflt_pedSubtractFlag
    pedestalCDSFile= dflt_pedestal_CDSavg
    #
    cols2CMA= APy3_GENfuns.matlabLike_range(dflt_cols2CMA_str)
    #
    saveFlag= dflt_saveFlag
    outFile= dflt_outFile
#---
#%% profile it
#import cProfile
#cProfile.run('auxdata= descrambleLast(mainFolder, ...)', sort='cumtime')
#APy3_GENfuns.printcol("scripts took {0} sec".format(aux_length),'green')
#---
#%% or just execute it
(scrmblSmpl,scrmblRst)= loadSomeImagesFromlast(mainFolder, img2proc_str, 
                           suffix_fl0, suffix_fl1,
                           verboseFlag)
#


if(wantDescramble):
  data_GnCrsFn = descrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH0_21_Flag, 
                   cleanMemFlag, verboseFlag);
else:
  data_GnCrsFn = NOTdescrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH0_21_Flag, 
                   cleanMemFlag, verboseFlag);

if ADCcorrFlag:
    if verboseFlag: APy3_GENfuns.printcol("ADC-correction", 'blue')
    if APy3_GENfuns.notFound(ADUcorr_file): APy3_GENfuns.printErr('not found: '+ADUcorr_file)
    (ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
     ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
    data_ADCcorr= ADCcorr_local(data_GnCrsFn,
                                ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                                ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)

    if verboseFlag: APy3_GENfuns.printcol("CDS, CMA", 'blue')
    data_CDS= APy3_P2Mfuns.CDS(data_ADCcorr)
    data_CDSCMA= APy3_P2Mfuns.CMA(data_CDS,cols2CMA)
    #
    if pedSubtractFlag:
        if verboseFlag: APy3_GENfuns.printcol("pedestal", 'blue')
        if APy3_GENfuns.notFound(pedestalCDSFile): APy3_GENfuns.printErr(pedestalCDSFile+' not found')
        data_pedestal_CDS= APy3_GENfuns.read_1xh5(pedestalCDSFile, '/data/data/') 
        #
        data_CDS= data_CDS-data_pedestal_CDS
        data_pedestal_CDSCMA= CMA(data_pedestal_CDS.reshape((1,NRow,NCol)),cols2CMA).reshape((NRow,NCol))
        data_CDSCMA= data_CDSCMA-data_pedestal_CDSCMA
    #
    if verboseFlag: APy3_GENfuns.printcol("avg-ing", 'blue')
    data_CDSavg= numpy.average(data_CDS[:,:,:],axis=0) # all img because already selected in the select images section
    data_CDSCMAavg= numpy.average(data_CDSCMA[:,:,:],axis=0) # all img because already selected in the select images section
    data_CDSCMAavg[:,cols2CMA[0]:cols2CMA[-1]+1]= numpy.NaN
else:
    data_CDSavg=    numpy.zeros((NRow,NCol))*numpy.NaN
    data_CDSCMAavg= numpy.zeros((NRow,NCol))*numpy.NaN
#
percDebug_plot_interactive_wCMA_2(data_GnCrsFn,
                                data_CDSavg,
                                data_CDSCMAavg,
                                False #manyImgFlag
                                )
#
if ~ADCcorrFlag & saveFlag: APy3_GENfuns.printcol("cannot save CDS avg file if I am not allowed to ADC-correct", 'green')
if ADCcorrFlag & saveFlag:
    if verboseFlag: APy3_GENfuns.printcol("saving CDS avg", 'blue')
    APy3_GENfuns.write_1xh5(outFile, data_CDSavg, "/data/data/")
    APy3_GENfuns.printcol("CDS avg saved as {0}".format(outFile), 'green')
