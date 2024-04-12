# -*- coding: utf-8 -*-
"""
general functions and fitting
(a half-decent language would have those functions already). Python is worth what it costs.
"""
#%% imports
#
import sys # command line argument, print w/o newline, version
import time
import numpy
from scipy import stats # linear regression
from scipy.optimize import curve_fit # non-linear fit
import math
import scipy
import matplotlib
import matplotlib.pyplot
matplotlib.pyplot.rcParams['image.cmap'] = 'jet'
import os # list files in a folder
import re # to sort naturally
import h5py # deal with HDF5
import tkinter
import APy3_GENfuns
#
from mpl_toolkits.mplot3d import Axes3D
#
#
#
#%% constant
VERYBIGNUMBER= 1e18
#
NSmplRst=2
NGrp=212
NPad=45
NADC=7
NColInBlock=32
NRowInBlock=NADC #7
NCol=NColInBlock*NPad # 32*45=1440, including RefCol
NRow= NADC*NGrp # 212*7=1484
NbitPerPix=15
#
iGn=0; iCrs=1; iFn=2; NGnCrsFn=3
iSmpl=0; iRst=1; NSmplRst=2 
NGn=3
#
ERRint16=-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw= -0.1
ERRDLSraw= 65535 # forbidden uint16, usable to track "pixel" from missing pack
#   
#
#
# percival-specific data reordering functions
#
# from P2M manual
N_xcolArray=4
N_ncolArray=8
NADC=7
colArray= numpy.arange(N_xcolArray*N_ncolArray).reshape((N_xcolArray,N_ncolArray)).transpose()
colArray= numpy.fliplr(colArray) # in the end it is colArray[ix,in]
#
# this gives the (iADC,iCol) indices of a pixel in a Rowblk, given its sequence in the streamout 
ADCcolArray_1DA=[]
for i_n in range(N_ncolArray):   
    for i_ADC in range(NADC)[::-1]:
        for i_x in range(N_xcolArray):
            ADCcolArray_1DA += [(i_ADC,colArray[i_n,i_x])]
ADCcolArray_1DA=numpy.array(ADCcolArray_1DA) #to use this:  for ipix in range(32*7): (ord_ADC,ord_col)=ADCcolArray_1DA[ipix]
#
iG=0
iH0= numpy.arange(21+1,0+1-1,-1)
iH1= numpy.arange(22+21+1,22+0+1-1,-1)
iP2M_ColGrp=numpy.append(numpy.array(iG),iH0)
iP2M_ColGrp=numpy.append(iP2M_ColGrp,iH1)
#
# percival-specific auxiliary functions
def matlabRow(matlabstring):
    """ 
    x:y =>[x,x+1, ...,y] 
    all => all the rows in a P2M
    """
    return APy3_GENfuns.matlabLike_range2(matlabstring, APy3_GENfuns.ALLlist,numpy.arange(NRow), True)
def matlabCol(matlabstring):
    """ 
    x:y =>[x,x+1, ...,y] 
    all => all the cols in a P2M (excluding refCols)
    """
    return APy3_GENfuns.matlabLike_range2(matlabstring, APy3_GENfuns.ALLlist,numpy.arange(32,NCol), True)
#
# percival-specific data conversion functions
#
def reorder_pixels_GnCrsFn(disord_4DAr,NADC,NColInRowBlk):
    ''' P2M pixel reorder for a image: (NGrp,NDataPads,NADC*NColInRowBlk,3),disordered =>  (NGrp,NDataPads,NADC,NColInRowBlk,3),ordered '''
    (aux_NGrp,aux_NPads,aux_pixInBlk, auxNGnCrsFn)= disord_4DAr.shape    
    ord_5DAr= numpy.zeros((aux_NGrp,aux_NPads,NADC,NColInRowBlk,auxNGnCrsFn), dtype='uint8')
    aux_pixOrd_padDisord_5DAr= numpy.zeros((aux_NGrp,aux_NPads,NADC,NColInRowBlk,auxNGnCrsFn), dtype='uint8')   
    # pixel reorder inside each block

    for ipix in range(NADC*NColInRowBlk):
        (ord_ADC,ord_Col)=ADCcolArray_1DA[ipix]
        aux_pixOrd_padDisord_5DAr[:,:,ord_ADC,ord_Col,:]= disord_4DAr[:,:,ipix,:]    
    # ColGrp order from chipscope to P2M
    for iColGrp in range(aux_NPads):
        ord_5DAr[:,iColGrp,:,:,:]= aux_pixOrd_padDisord_5DAr[:,iP2M_ColGrp[iColGrp],:,:,:]    
    return ord_5DAr    
#
def reorder_pixels_GnCrsFn_par(disord_6DAr,NADC,NColInRowBlk):
    ''' P2M pixel reorder for a image: (NImg,NSmplrst, NGrp,NDataPads,NADC*NColInRowBlk,3),disordered =>  ((NImg,NSmplrst, NGrp,NDataPads,NADC,NColInRowBlk,3),ordered '''
    (aux_NImg,aux_NSmplRst, aux_NGrp,aux_NPads,aux_pixInBlk, auxNGnCrsFn)= disord_6DAr.shape    
    ord_7DAr= numpy.zeros((aux_NImg,aux_NSmplRst, aux_NGrp,aux_NPads,NADC,NColInRowBlk,auxNGnCrsFn), dtype='uint8')
    aux_pixOrd_padDisord_7DAr= numpy.zeros((aux_NImg,aux_NSmplRst, aux_NGrp,aux_NPads,NADC,NColInRowBlk,auxNGnCrsFn), dtype='uint8')   
    # pixel reorder inside each block
    for ipix in range(NADC*NColInRowBlk):
        (ord_ADC,ord_Col)=ADCcolArray_1DA[ipix]
        aux_pixOrd_padDisord_7DAr[:,:, :,:,ord_ADC,ord_Col,:]= disord_6DAr[:,:, :,:,ipix,:]    
    ord_7DAr[:,:, :,:,:,:,:]= aux_pixOrd_padDisord_7DAr[:,:, :,iP2M_ColGrp[:],:,:,:]  
    return ord_7DAr 
#
def decode_dataset_8bit(arr_in, bit_mask, bit_shift):
    """ Masks out bits and shifts """
    arr_out = numpy.bitwise_and(arr_in, bit_mask)
    arr_out = numpy.right_shift(arr_out, bit_shift)
    arr_out = arr_out.astype(numpy.uint8)
    return arr_out
def aggregate_to_GnCrsFn(raw_dset):
    """Extracts the coarse, fine and gain bits.
    0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
    -   B0  B1  F0  F1  F2  F3  F4  F5  F6  F7  C0  C1  C2  C3  C4
    """
    coarse_adc = decode_dataset_8bit(arr_in=raw_dset,bit_mask=0x1F,bit_shift=0) # 0x1F   -> 0000000000011111
    fine_adc = decode_dataset_8bit(arr_in=raw_dset,bit_mask=0x1FE0,bit_shift=5) # 0x1FE0 -> 0001111111100000
    gain_bits = decode_dataset_8bit(arr_in=raw_dset,bit_mask=0x6000,bit_shift=5+8) # 0x6000 -> 0110000000000000
    return coarse_adc, fine_adc, gain_bits
#
def convert_GnCrsFn_2_DLSraw(in_GnCrsFn_int16, inErr, outERR):
    ''' (Nimg,Smpl/Rst,NRow,NCol,Gn/Crs/Fn),int16(err=inErr) => DLSraw: Smpl&Rst(Nimg,NRow,NCol),uint16(err=outErr):[X,GG,FFFFFFFF,CCCCC]'''
    multiImg_SmplRstGnGrsFn_u16=numpy.clip(in_GnCrsFn_int16,0,(2**8)-1)
    multiImg_SmplRstGnGrsFn_u16= multiImg_SmplRstGnGrsFn_u16.astype('uint16')
    # convert to DLSraw format
    (NImg,aux_NSmplRst,aux_NRow,aux_NCol,aux_NGnCrsFn)= in_GnCrsFn_int16.shape
    out_multiImg_Smpl_DLSraw= numpy.zeros((NImg, NGrp*NRowInBlock,NPad*NColInBlock)).astype('uint16')
    out_multiImg_Rst_DLSraw= numpy.zeros((NImg, NGrp*NRowInBlock,NPad*NColInBlock)).astype('uint16')  
    out_multiImg_Smpl_DLSraw[:,:,:]= ((2**13)*multiImg_SmplRstGnGrsFn_u16[:,iSmpl,:,:,iGn].astype('uint16'))+ \
                                ((2**5)*multiImg_SmplRstGnGrsFn_u16[:,iSmpl,:,:,iFn].astype('uint16'))+\
                                multiImg_SmplRstGnGrsFn_u16[:,iSmpl,:,:,iCrs].astype('uint16') 
    out_multiImg_Rst_DLSraw[:,:,:]= ((2**13)*multiImg_SmplRstGnGrsFn_u16[:,iRst,:,:,iGn].astype('uint16'))+ \
                                ((2**5)*multiImg_SmplRstGnGrsFn_u16[:,iRst,:,:,iFn].astype('uint16'))+\
                                multiImg_SmplRstGnGrsFn_u16[:,iRst,:,:,iCrs].astype('uint16')               
    #%% track errors in DLSraw mode with the ERRDLSraw (max of uint16) value (usually this in not reached because pixel= 15 bit)
    errMask= in_GnCrsFn_int16[:,iSmpl,:,:,iGn]==inErr
    out_multiImg_Smpl_DLSraw[errMask]= outERR
    errMask= in_GnCrsFn_int16[:,iRst,:,:,iGn]==inErr
    out_multiImg_Rst_DLSraw[errMask]= outERR
    #
    return (out_multiImg_Smpl_DLSraw,out_multiImg_Rst_DLSraw)  
#       
def convert_DLSraw_2_GnCrsFn(in_Smpl_DLSraw, in_Rst_DLSraw, inErr, outERR):
    ''' (Nimg,Smpl/Rst,NRow,NCol,Gn/Crs/Fn),int16(err=inErr) <= DLSraw: Smpl&Rst(Nimg,NRow,NCol),uint16(err=outErr):[X,GG,FFFFFFFF,CCCCC]'''
    in_Smpl_uint16=numpy.clip(in_Smpl_DLSraw,0,(2**15)-1).astype('uint16')
    in_Rst_uint16=numpy.clip(in_Rst_DLSraw,0,(2**15)-1).astype('uint16')
    #
    (aux_NImg,aux_NRow,aux_NCol)=in_Smpl_DLSraw.shape
    auxSmpl_multiImg_GnCrsFn= numpy.zeros((aux_NImg,aux_NRow,aux_NCol,3)).astype('uint8')
    auxRst_multiImg_GnCrsFn= numpy.zeros((aux_NImg,aux_NRow,aux_NCol,3)).astype('uint8')
    out_multiImg_GnCrsFn= numpy.zeros((aux_NImg,2,aux_NRow,aux_NCol,3)).astype('int16')
    #
    imgGn= numpy.zeros((aux_NRow, aux_NCol)).astype('uint8')
    imgCrs=numpy.zeros_like(imgGn).astype('uint8')
    imgFn=numpy.zeros_like(imgGn).astype('uint8')
    for iImg in range(aux_NImg):
        imgGn= in_Smpl_uint16[iImg,:,:]//(2**13)
        imgFn= (in_Smpl_uint16[iImg,:,:]-(imgGn.astype('uint16')*(2**13)))//(2**5)
        imgCrs= in_Smpl_uint16[iImg,:,:] -(imgGn.astype('uint16')*(2**13)) -(imgFn.astype('uint16')*(2**5))
        auxSmpl_multiImg_GnCrsFn[iImg,:,:,iGn]=imgGn
        auxSmpl_multiImg_GnCrsFn[iImg,:,:,iCrs]=imgCrs
        auxSmpl_multiImg_GnCrsFn[iImg,:,:,iFn]=imgFn
        #
        imgGn= in_Rst_uint16[iImg,:,:]//(2**13)
        imgFn= (in_Rst_uint16[iImg,:,:]-(imgGn.astype('uint16')*(2**13)))//(2**5)
        imgCrs= in_Rst_uint16[iImg,:,:] -(imgGn.astype('uint16')*(2**13)) -(imgFn.astype('uint16')*(2**5))
        auxRst_multiImg_GnCrsFn[iImg,:,:,iGn]=imgGn
        auxRst_multiImg_GnCrsFn[iImg,:,:,iCrs]=imgCrs
        auxRst_multiImg_GnCrsFn[iImg,:,:,iFn]=imgFn           
    #
    #%% track errors in GnCrsFn mode with the ERRint16 (-256) value (usually this in tot reached because all>0)
    auxSmpl_multiImg_GnCrsFn=auxSmpl_multiImg_GnCrsFn.astype('uint16')
    auxRst_multiImg_GnCrsFn=auxRst_multiImg_GnCrsFn.astype('uint16')
    errMask= in_Smpl_DLSraw[:,:,:]==inErr
    auxSmpl_multiImg_GnCrsFn[errMask,:]= outERR        
    errMask= in_Rst_DLSraw[:,:,:]==inErr
    auxRst_multiImg_GnCrsFn[errMask,:]= outERR 
    #             
    out_multiImg_GnCrsFn[:,iSmpl,:,:,:]= auxSmpl_multiImg_GnCrsFn[:,:,:,:]
    out_multiImg_GnCrsFn[:,iRst,:,:,:]= auxRst_multiImg_GnCrsFn[:,:,:,:]
    #    
    return(out_multiImg_GnCrsFn)
#
def descramble_odinDAQ_2links(dataSmpl_fl0,dataRst_fl0,dataSmpl_fl1,dataRst_fl1,
                              swapSmplRstFlag,seqModFlag, refColH1_0_Flag,
                              cleanMemFlag,verboseFlag):
    #%% what's up doc
    """
    descrambles the content of 2 h5-odinDAQ(raw) files, returns it in DLSraw format
    
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
        dataSmpl_fl0,dataRst_fl0,dataSmpl_fl1,dataRst_fl1
        swapSmplRstFlag,seqModFlag, refColH1_0_Flag,verboseFlag,cleanMemFlag
    
    Returns:
        descrambled array (DLSraw format)
    """
    #APy3_GENfuns.descramble_odinDAQ should always have highMemFlag==True
    #
    NColInBlk=NColInBlock
    NDataPad=NPad-1
    #
    thisFile_startTime= time.time()
    (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
    (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
    NImg = NImg_fl0 + NImg_fl0
    if verboseFlag: APy3_GENfuns.printcol("{0}+{1} Img to process".format(NImg_fl0,NImg_fl1), 'green')
    # ---
    # combine in one array: Img0-from-fl0, Img0-from-fl1, Img1-from-fl0...
    scrmblSmpl= numpy.zeros( (NImg,aux_NRow,aux_NCol), dtype='uint16')
    scrmblRst= numpy.zeros_like(scrmblSmpl, dtype='uint16') 
    scrmblSmpl[0::2,:,:]= dataSmpl_fl0[:,:,:]
    scrmblSmpl[1::2,:,:]= dataSmpl_fl1[:,:,:]
    scrmblRst[0::2,:,:]=  dataRst_fl0[:,:,:]
    scrmblRst[1::2,:,:]=  dataRst_fl1[:,:,:]
    if cleanMemFlag: del dataSmpl_fl0; del dataRst_fl0; del dataSmpl_fl1; del dataRst_fl1
    # ---
    # solving 4a DAQ-scrambling: byte swap in hex (By0,By1) => (By1,By0)
    if verboseFlag: APy3_GENfuns.printcol("solving DAQ-scrambling: byte-swapping and Smpl-Rst-swapping", 'blue')
    if swapSmplRstFlag:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
    else:
        scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
        scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)    
    if cleanMemFlag: del scrmblSmpl; del scrmblRst
    # ---
    # solving DAQ-scrambling: "pixel" reordering
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
    data2srcmbl_noRefCol[:,iSmpl,:,:]= (scrmblSmpl_byteSwap)
    data2srcmbl_noRefCol[:,iRst,:,:] = (scrmblRst_byteSwap)
    if cleanMemFlag: del scrmblSmpl_byteSwap; del scrmblRst_byteSwap
    #
    data2srcmbl_noRefCol= data2srcmbl_noRefCol.reshape((NImg,NSmplRst,NGrp,NADC,aux_NCol))
    #
    # track missing packets: False==RowGrp OK; True== packet(s) missing makes rowgroup moot
    # (1111 1111 1111 1111 instead of 0xxx xxxx xxxx xxxx)
    missingRowGrp_Tracker = data2srcmbl_noRefCol[:,:,:,0,0] == ERRDLSraw
    # ---    
    # descramble proper
    if verboseFlag: APy3_GENfuns.printcol("solving mezzanine&chip-scrambling: pixel descrambling", 'blue')
    multiImgWithRefCol= numpy.zeros((NImg,NSmplRst,NGrp,NPad,NADC*NColInBlk,NGnCrsFn), dtype='int16')
    #
    # refCol
    multiImgWithRefCol[:,:,:,0,:,:]= ERRint16
    #
    # descrambling
    if verboseFlag: APy3_GENfuns.printcol("descrambling", 'blue')
    data2srcmbl_noRefCol= data2srcmbl_noRefCol.reshape((NImg,NSmplRst,NGrp,NADC*aux_NCol //(NDataPad*2),NDataPad,2)) # 32bit=2"pix" from 1st pad, 2"pix" from 2nd pad, ...
    data2srcmbl_noRefCol= numpy.transpose(data2srcmbl_noRefCol, (0,1,2,4,3,5)).reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*aux_NCol//NDataPad)) # (NSmplRst,NGrp,NDataPad,NADC*aux_NCol//NDataPad)
    theseImg_bitted= APy3_GENfuns.convert_uint_2_bits_Ar(data2srcmbl_noRefCol,16)[:,:,:,:,:,-2::-1].astype('uint8') # n_smplrst,n_grp,n_data_pads,n_adc*aux_ncol//n_data_pads,15bits
    if cleanMemFlag: del data2srcmbl_noRefCol
    theseImg_bitted= theseImg_bitted.reshape((NImg, NSmplRst,NGrp,NDataPad,NbitPerPix,NADC*NColInBlk))
    theseImg_bitted= numpy.transpose(theseImg_bitted,(0,1,2,3,5,4)) # (NImg, n_smplrst,n_grp,n_data_pads,NPixsInRowBlk,15)
    theseImg_bitted= APy3_GENfuns.convert_britishBits_Ar(theseImg_bitted).reshape((NImg, NSmplRst*NGrp*NDataPad*NADC*NColInBlk, NbitPerPix))
    #
    theseImg_bitted=theseImg_bitted.reshape((NImg*NSmplRst*NGrp*NDataPad*NADC*NColInBlk, NbitPerPix))
    (aux_coarse,aux_fine,aux_gain)= aggregate_to_GnCrsFn( APy3_GENfuns.convert_bits_2_uint16_Ar(theseImg_bitted[:,::-1]) )
    multiImgWithRefCol[:,:,:,1:,:,iGn]=  aux_gain.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    multiImgWithRefCol[:,:,:,1:,:,iCrs]= aux_coarse.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    multiImgWithRefCol[:,:,:,1:,:,iFn]=  aux_fine.reshape((NImg,NSmplRst,NGrp,NDataPad,NADC*NColInBlk))
    if cleanMemFlag: del aux_gain; del aux_coarse; del aux_fine; del theseImg_bitted   
    # ---
    #
    # reorder pixels and pads
    if verboseFlag: APy3_GENfuns.printcol("solving chip-scrambling: pixel reordering", 'blue')
    multiImg_Grp_dscrmbld= reorder_pixels_GnCrsFn_par(multiImgWithRefCol,NADC,NColInBlk)
    if cleanMemFlag: del multiImgWithRefCol 
    # --- 
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
    if refColH1_0_Flag:
        if verboseFlag: APy3_GENfuns.printcol("moving RefCol data to G", 'blue')
        multiImg_Grp_dscrmbld[:,:,:,0,:,:,:]= multiImg_Grp_dscrmbld[:,:,:,44,:,:,:]
        multiImg_Grp_dscrmbld[:,:,:,44,:,:,:]= ERRint16
    # ---
    #
    # reshaping as an Img array: (NImg,Smpl/Rst,n_grp,n_adc,n_pad,NColInBlk,Gn/Crs/Fn)
    if verboseFlag: APy3_GENfuns.printcol("reshaping as an Img array", 'blue')
    dscrmbld_GnCrsFn = numpy.transpose(multiImg_Grp_dscrmbld, (0,1,2,4,3,5,6)).astype('int16').reshape((NImg,NSmplRst, NGrp*NADC,NPad*NColInBlk, NGnCrsFn))
    if cleanMemFlag: del multiImg_Grp_dscrmbld 
    # ---
    #
    # reorder rowgrp (SeqMode) if needed
    if seqModFlag:
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp,NADC, NCol,NGnCrsFn))
        aux_Seq= numpy.ones_like(dscrmbld_GnCrsFn, dtype='int16') * ERRint16
        aux_Seq[:,:,1:106,:,:,:]= dscrmbld_GnCrsFn[:,:,2:212:2,:,:,:]
        dscrmbld_GnCrsFn[:,:,:,:,:,:]= aux_Seq[:,:,:,:,:,:]
        dscrmbld_GnCrsFn= dscrmbld_GnCrsFn.reshape((NImg,NSmplRst, NGrp*NADC, NCol,NGnCrsFn))
        if cleanMemFlag: del aux_Seq
    # ---
    #
    # GnCrsFn to DLSraw
    if verboseFlag: APy3_GENfuns.printcol("converting to DLSraw", 'blue')
    (Smpl_DLSraw, Rst_DLSraw)= convert_GnCrsFn_2_DLSraw(dscrmbld_GnCrsFn, ERRint16, ERRDLSraw) 
    # ---
    #
    # that's all folks
    thisFile_endTime=time.time()
    if verboseFlag: APy3_GENfuns.printcol("script took {0} to process this file".format(thisFile_endTime-thisFile_startTime), 'green')
    return (Smpl_DLSraw, Rst_DLSraw)
#
def descramble(dataSmpl_fl0,dataRst_fl0,dataSmpl_fl1,dataRst_fl1,
               swapSmplRstFlag,seqModFlag, refColH1_0_Flag,
               highMemFlag,cleanMemFlag,verboseFlag):
    #%% what's up doc
    """
    descrambles the content of 2 h5-odinDAQ(raw) files, returns it in DLSraw format
    either fast,HighMemUse or slow(2Img at a time),LowMemUse
    """
    if highMemFlag: 
        (Smpl_DLSraw, Rst_DLSraw)= descramble_odinDAQ_2links(dataSmpl_fl0,dataRst_fl0,dataSmpl_fl1,dataRst_fl1,
                                                             swapSmplRstFlag,seqModFlag, refColH1_0_Flag,
                                                             cleanMemFlag,verboseFlag)
    else: 
        # 2 img at a time
        APy3_GENfuns.printcol("descrambling two img at a time", 'blue')
        (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
        (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
        if (NImg_fl0 != NImg_fl1): APy3_GENfuns.printErr("NImg_fl0 != NImg_fl1")
        Smpl_DLSraw= numpy.zeros((NImg_fl0+NImg_fl1,NRow,NCol),dtype= 'uint16')
        Rst_DLSraw=  numpy.zeros((NImg_fl0+NImg_fl1,NRow,NCol),dtype= 'uint16')
        for iImgCouple in range(NImg_fl0):
            thisSmpl_fl0= dataSmpl_fl0[iImgCouple,:,:].reshape((1, aux_NRow,aux_NCol))
            thisSmpl_fl1= dataSmpl_fl1[iImgCouple,:,:].reshape((1, aux_NRow,aux_NCol))
            thisRst_fl0=  dataRst_fl0[iImgCouple,:,:].reshape((1, aux_NRow,aux_NCol))
            thisRst_fl1=  dataRst_fl1[iImgCouple,:,:].reshape((1, aux_NRow,aux_NCol))
            (thisSmpl_DLSraw, thisRst_DLSraw)= descramble_odinDAQ_2links(thisSmpl_fl0,thisRst_fl0,thisSmpl_fl1,thisRst_fl1,
                                                                         swapSmplRstFlag,seqModFlag, refColH1_0_Flag,
                                                                         cleanMemFlag,False)
            auxFrom= iImgCouple*2
            auxToPlus1= (iImgCouple*2)+1+1
            Smpl_DLSraw[auxFrom:auxToPlus1, :,:]= thisSmpl_DLSraw[:, :,:]
            Rst_DLSraw[auxFrom:auxToPlus1, :,:]=  thisRst_DLSraw[:, :,:]
            APy3_GENfuns.dot_every10th(iImgCouple,NImg_fl0)
    return (Smpl_DLSraw, Rst_DLSraw)

#
#
#%% convert raw-raw data to ADC-cor data and manipulate 
def read_ADUh5(filenamepath):
    """ read ADU (sample-reset / coarse-fine / slope-offset) file """
    my5hfile= h5py.File(filenamepath, 'r')
    ADU_SmplCrsSlp= numpy.array(my5hfile["sample/coarse/slope/"])
    ADU_SmplCrsOff= numpy.array(my5hfile["sample/coarse/offset/"])
    ADU_SmplFnSlp=  numpy.array(my5hfile["sample/fine/slope/"])
    ADU_SmplFnOff=  numpy.array(my5hfile["sample/fine/offset/"])
    ADU_RstCrsSlp=  numpy.array(my5hfile["reset/coarse/slope/"])
    ADU_RstCrsOff=  numpy.array(my5hfile["reset/coarse/offset/"])
    ADU_RstFnSlp=   numpy.array(my5hfile["reset/fine/slope/"])
    ADU_RstFnOff=   numpy.array(my5hfile["reset/fine/offset/"])
    my5hfile.close()
    return (ADU_SmplCrsSlp,ADU_SmplCrsOff,ADU_SmplFnSlp,ADU_SmplFnOff , ADU_RstCrsSlp,ADU_RstCrsOff,ADU_RstFnSlp,ADU_RstFnOff)
#
def read_multiGnCalh5(multiGnCal_file):
    """ read PedestalADU,e/ADU for multiGn (3DArray of data, as (Gn0/1/2,Row,Col)  ) """
    (PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
    return (PedestalADU_multiGn,e_per_ADU_multiGn)
#
def ADCcorr_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol):
    ''' P2M ADC-corr: combine Coarse and Fine in numpy array image (ignore Gain)'''
    idealOffset = numpy.zeros((NRow, NCol)) + (128.0 * 32.0);
    idealSlope  = (idealOffset / 1.5); # mapped over over 1.5V Vin span
    #
    return ( idealOffset + ( (idealSlope/coarseGain)*(coarse+1.0-coarseOffset) - (idealSlope/fineGain)*(fine-fineOffset) ) )
    #
    #normalizedADU = idealOffset + ( (idealSlope/coarseGain)*(coarse+1.0-coarseOffset) - (idealSlope/fineGain)*(fine-fineOffset) );
    #return (normalizedADU);
"""
# old version
def ADCcorr_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol):
    ''' P2M ADC-corr: combine Coarse and Fine in numpy array image (ignore Gain)'''
    #
    idealOffset = numpy.zeros((NRow, NCol)) + (128.0 * 32.0);
    idealSlope  = (idealOffset / 1.5); # mapped over over 1.5V Vin span
    #
    overallADU = (fineGain / coarseGain) * (coarse +1.0)- (fine - fineOffset);
    normalizedADU = coarseOffset * (fineGain/coarseGain) - overallADU;
    normalizedADU = ( idealSlope / fineGain ) * normalizedADU;
    normalizedADU = idealOffset - normalizedADU;
    return (normalizedADU);
"""
#
def ADCcorr_from0_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol):
    ''' P2M ADC-corr: combine Coarse and Fine in numpy array image (ignore Gain); so that crs=0,Fn=255 => ~0ADU'''
    normalizedADU_from0= ADCcorr_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol)  - ADCcorr_NoGain(0,255, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol)
    return (normalizedADU_from0)
#
def CDS(data_ADCcorr):
    ''' CDS '''
    out_CDS= data_ADCcorr[1:,iSmpl,:,:] - data_ADCcorr[:-1,iRst,:,:] # NImg,NSmplRst,NRow,NCol =>  NImg,NRow,NCol
    return out_CDS
#
def CMA(in_CDS ,CMACols_Ar):
    '''  CMA using avg val (in each image) of pixels in (thatRow, CMAcols_Ar) '''
    CMACols_start= CMACols_Ar[0]
    CMACols_end= CMACols_Ar[-1]+1
    CMAvg= numpy.average(in_CDS[:,:,CMACols_start:CMACols_end], axis=2) # avg along Cols for CMAcols_Ar
    (auxNImg,auxNRow,auxNCol)= in_CDS.shape
    CMAvg= CMAvg.reshape(auxNImg,auxNRow,1)
    out_CDSCMA= in_CDS-CMAvg
    return out_CDSCMA      
#
#
#
#%% percival-specific debug-plot dunctions

def percDebug_plot_6x2D(GnSmpl,CrsSmpl,FnSmpl, GnRst,CrsRst,FnRst, label_title,ErrBelow):
    """ 2D plot of Smpl/Rst, Gn/Crs/Fn, give mark as error (white) the values << ErrBelow """ 
    cmap = matplotlib.pyplot.cm.jet
    cmap.set_under(color='white') 
    #fig = matplotlib.pyplot.figure(figsize=(18,12))
    fig = matplotlib.pyplot.figure()
    fig.canvas.set_window_title(label_title) 
    label_x="col"; label_y="row"
    #
    matplotlib.pyplot.subplot(2,3,1)
    matplotlib.pyplot.imshow(GnSmpl, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Sample Gain')
    matplotlib.pyplot.clim(-0.01,3)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    #
    matplotlib.pyplot.subplot(2,3,2)
    matplotlib.pyplot.imshow(CrsSmpl, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Sample Coarse')
    matplotlib.pyplot.clim(-0.01,31)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    #
    matplotlib.pyplot.subplot(2,3,3)
    matplotlib.pyplot.imshow(FnSmpl, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Sample Fine')
    matplotlib.pyplot.clim(-0.01,255)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    #
    matplotlib.pyplot.subplot(2,3,4)
    matplotlib.pyplot.imshow(GnRst, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Reset Gain (not relevant)')
    matplotlib.pyplot.clim(-0.01,3)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    #
    matplotlib.pyplot.subplot(2,3,5)
    matplotlib.pyplot.imshow(CrsRst, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Reset Coarse')
    matplotlib.pyplot.clim(-0.01,31)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    #
    matplotlib.pyplot.subplot(2,3,6)
    matplotlib.pyplot.imshow(FnRst, interpolation='none', cmap=cmap, vmin=ErrBelow)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title('Reset Fine')
    matplotlib.pyplot.clim(-0.01,255)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();
    matplotlib.pyplot.show(block=False)
    return fig
#
def percDebug_plot_2x2D_map(ShtLeft,ShtRight,goodPixMap, label_titleLeft,label_titleRight,label_titleAll):  
    ''' plot Smpl & Rst img, white if above ErrAbove (e.g. 33000)''' 
    cmap = matplotlib.pyplot.cm.jet
    #cmap.set_over(color='white') 
    fig = matplotlib.pyplot.figure()
    fig.canvas.set_window_title(label_titleAll)
    label_x="col"; label_y="row"
    #
    badPixMap= (goodPixMap==False)
    ShtLeft[badPixMap]= numpy.NAN
    ShtRight[badPixMap]= numpy.NAN
    #
    matplotlib.pyplot.subplot(1,2,1); 
    matplotlib.pyplot.imshow(ShtLeft, interpolation='none', cmap=cmap,)
    matplotlib.pyplot.title(label_titleLeft)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y) 
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();   
    #
    matplotlib.pyplot.subplot(1,2,2); 
    matplotlib.pyplot.imshow(ShtRight, interpolation='none', cmap=cmap)
    matplotlib.pyplot.title(label_titleRight)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.gca().invert_xaxis();  
    #
    matplotlib.pyplot.show(block=False)
    return fig
#
def percDebug_plot_interactive(data_GnCrsFn,data_CDSavg, manyImgFlag):
    (NImg,ignSR,ignR,ignC,ign3)= data_GnCrsFn.shape
    thisImg=-1
    APy3_GENfuns.printcol("plot [C]DS in lin / [L]og scale / [number] of raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
    if manyImgFlag: nextstep = input()
    else: nextstep = APy3_GENfuns.press_any_key()
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
        else:
            aux_title = "Img " + str(thisImg)
            aux_err_below = -0.1
            percDebug_plot_6x2D(data_GnCrsFn[thisImg,iSmpl,:,:,iGn],data_GnCrsFn[thisImg,iSmpl,:,:,iCrs],data_GnCrsFn[thisImg,iSmpl,:,:,iFn],
                                data_GnCrsFn[thisImg,iRst,:,:,iGn], data_GnCrsFn[thisImg,iRst,:,:,iCrs], data_GnCrsFn[thisImg,iRst,:,:,iFn],
                                aux_title, aux_err_below)
            APy3_GENfuns.maximize_plot() 
            matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
        APy3_GENfuns.printcol("plot [C]DS in lin / [L]og scale / [number] of raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
        if manyImgFlag: nextstep = input()
        else: nextstep = APy3_GENfuns.press_any_key()
        if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue') 
    return

#
#
#
def percDebug_plot_interactive_wCMA(data_GnCrsFn,data_CDSavg,data_CDSCMAavg, manyImgFlag):
    (NImg,ignSR,ignR,ignC,ign3)= data_GnCrsFn.shape
    thisImg=-1
    APy3_GENfuns.printcol("plot [C]DS in lin/[L]og scale / CDS-C[M]A in lin/lo[G] scale / [number] of raw image / [N]ext raw image / [P]revious raw image / [E]nd", 'black')
    if manyImgFlag: nextstep = input()
    else: nextstep = APy3_GENfuns.press_any_key()
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
#%% P2M often used scripts
def UseDLSraw_versatile(mainFolder, # where data is
                        img2proc_str, # 'all'==all
                        #
                        ADCcorrCDSFlag,
                        ADCfile_validMap,
                        ADCfile_crs_slope,
                        ADCfile_crs_offset,
                        ADCfile_fn_slope,     
                        ADCfile_fn_offset,
                        #
                        CMAFlag,
                        cols2CMA_str,
                        #
                        pedSubtractFlag,
                        pedestalCDSFile,
                        #
                        lastFileOnlyFlag, # alternatively: process all files in folder
                        refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                        #
                        showFlag,
                        manyImgFlag, # select more than 1 digit image in interactive plot
                        #
                        in_1file_suffix,
                        #
                        saveAvgFlag, # save 2D img (float): avg of ADCcorr, CDS, possibly CMA, possibly ped-Subtracted
                        outFolder,
                        out_AvgCDSfile_suffix,
                        #
                        highMemFlag,
                        cleanMemFlag,
                        verboseFlag):
    """ 
    this version is kept for retrocompatibility only 
    it uses the same ADCcorrection for Smpl and Rst
    better instad to use the UseDLSraw_versatile_SmplRst function
    """
    APy3_GENfuns.printERR('this version is kept for retrocompatibility only; it uses the same ADCcorrection for Smpl and Rst; better instad to use the UseDLSraw_versatile_SmplRst function')
    #
    startTime=time.time()
    APy3_GENfuns.printcol("UseDLSraw_versatile starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    # ---
    #
    #%% what's up doc
    APy3_GENfuns.printcol("will look at files {0} ... {1}".format(mainFolder,in_1file_suffix), 'blue')
    if lastFileOnlyFlag: APy3_GENfuns.printcol("will process only the most recent", 'blue')
    APy3_GENfuns.printcol("will process from in Img {0}".format(img2proc_str), 'blue')
    if refColH1_0_Flag: APy3_GENfuns.printcol("will H1<0> data as RefCol data", 'blue')
    if showFlag: APy3_GENfuns.printcol("will show images interactively", 'blue')
    #
    if ADCcorrCDSFlag: 
        APy3_GENfuns.printcol("will look ADCcor files:", 'blue')
        APy3_GENfuns.printcol(ADCfile_validMap, 'blue')
        APy3_GENfuns.printcol(ADCfile_crs_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_crs_offset, 'blue')
        APy3_GENfuns.printcol(ADCfile_fn_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_fn_offset, 'blue')
        if CMAFlag: APy3_GENfuns.printcol("will CMA using cols: {0}".format(cols2CMA_str), 'blue')
        if pedSubtractFlag: APy3_GENfuns.printcol("will look for pedestal file {0}".format(pedestalCDSFile), 'blue')
        if saveAvgFlag: 
            if pedSubtractFlag: APy3_GENfuns.printcol("will save an ADCcorr CDS avg (pedestal-subtracted) h5 file", 'blue') 
            else: APy3_GENfuns.printcol("will save an ADCcorr avg h5 files", 'blue')
            APy3_GENfuns.printcol("as {0} ... {1}".format(outFolder,out_AvgCDSfile_suffix), 'blue')
    if saveAvgFlag & (ADCcorrCDSFlag== False): APy3_GENfuns.printcol("cannot save an ADCcorr avg h5 file, if I am not allowed to ADCcor!", 'red')
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
        if APy3_GENfuns.notFound(ADCfile_validMap): APy3_GENfuns.printErr(ADCfile_validMap+' not found')
        ADCparam_validMap= APy3_GENfuns.read_1xh5(ADCfile_validMap, '/data/data/').astype(bool)
        if APy3_GENfuns.notFound(ADCfile_crs_slope): APy3_GENfuns.printErr(ADCfile_crs_slope+' not found')
        ADCparam_crs_slope= APy3_GENfuns.read_1xh5(ADCfile_crs_slope, '/data/data/')
        if APy3_GENfuns.notFound(ADCfile_crs_offset): APy3_GENfuns.printErr(ADCfile_crs_offset+' not found')
        ADCparam_crs_offset= APy3_GENfuns.read_1xh5(ADCfile_crs_offset, '/data/data/')
        if APy3_GENfuns.notFound(ADCfile_fn_slope): APy3_GENfuns.printErr(ADCfile_fn_slope+' not found')
        ADCparam_fn_slope= APy3_GENfuns.read_1xh5(ADCfile_fn_slope, '/data/data/')
        if APy3_GENfuns.notFound(ADCfile_fn_offset): APy3_GENfuns.printErr(ADCfile_fn_offset+' not found')
        ADCparam_fn_offset= APy3_GENfuns.read_1xh5(ADCfile_fn_offset, '/data/data/')
        if verboseFlag: APy3_GENfuns.printcol("ADCcor files loaded", 'green')
        #
        # modify load ADCparam to avoid /0
        goodPixMap= (ADCparam_validMap==True); badPixMap= (ADCparam_validMap==False) 
        ADCparam_crs_offset[badPixMap]=1.0
        ADCparam_crs_slope[badPixMap]=1.0
        ADCparam_fn_offset[badPixMap]=1.0
        ADCparam_fn_slope[badPixMap]=1.0
        #
        if CMAFlag: 
            cols2CMA = APy3_GENfuns.matlabLike_range(cols2CMA_str)
            if verboseFlag: APy3_GENfuns.printcol("will CMA using cols {0}".format(str(cols2CMA)), 'green')
        else: cols2CMA= numpy.array([0])
        #
        if pedSubtractFlag:
            if APy3_GENfuns.notFound(ADCfile_validMap): APy3_GENfuns.printErr(pedestalCDSFile+' not found')
            data_pedestal_CDS= APy3_GENfuns.read_1xh5(pedestalCDSFile, '/data/data/') 
            if verboseFlag: APy3_GENfuns.printcol("pedestal file loaded", 'green')
    if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    #
    #%% list or last data files
    filelist_in= APy3_GENfuns.list_files(mainFolder, '*', in_1file_suffix) # all files
    if verboseFlag: APy3_GENfuns.printcol("{0} image sets found in folder".format(len(filelist_in)), 'green')
    if lastFileOnlyFlag:   
        if verboseFlag: APy3_GENfuns.printcol("will only process the most recent", 'green') 
        aux_fileName= os.path.basename( APy3_GENfuns.last_file(mainFolder, '*'+in_1file_suffix) ) # filename only, no path
        filelist_in= [aux_fileName]
    # ---
    for ifile,file_in in enumerate(filelist_in):
        APy3_GENfuns.printcol("collection {0}/{1}:".format(ifile,len(filelist_in)-1), 'blue')
        if verboseFlag: APy3_GENfuns.printcol(mainFolder+file_in, 'green')
        (dataSmpl_in,dataRst_in) = APy3_GENfuns.read_2xh5(mainFolder+file_in, '/data/','/reset/')
        (NImg, aux_NRow, aux_NCol) = dataSmpl_in.shape
        if verboseFlag: APy3_GENfuns.printcol("{0} Img read from file".format(NImg), 'green')
        # ---
        # select images
        if img2proc_str in ['all','All','ALL',':','*','-1']: 
            if verboseFlag: APy3_GENfuns.printcol("will read all Img", 'green')
        else:
            img2proc= APy3_GENfuns.matlabLike_range(img2proc_str)
            fromImg= img2proc[0]
            toImg= img2proc[-1]
            NImg= toImg-fromImg+1
            if verboseFlag: APy3_GENfuns.printcol("will use Img from {0} to {1} (included), for a total of {2}".format(fromImg,toImg,NImg),'green')
            dataSmpl_in= dataSmpl_in[fromImg:toImg+1,:,:]
            dataRst_in=  dataRst_in[fromImg:toImg+1,:,:]
        # ---
        #%% convert to GnCrsFn 
        APy3_GENfuns.printcol("converting to Gn,Crs,Fn", 'blue')
        if highMemFlag: dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(dataSmpl_in,dataRst_in, ERRDLSraw,ERRint16)
        else:
            dscrmbld_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
            for thisImg in range(NImg):
                thisSmpl_DLSraw= Smpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
                thisRst_DLSraw=  Rst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
                this_dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
                dscrmbld_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
                if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
        # ---
        #%% ADCcor, CDS, CMA, pedSub
        if ADCcorrCDSFlag: 
            APy3_GENfuns.printcol("ADC-correcting, CDS-ing", 'blue')
            data_ADCcorr= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                         ADCparam_crs_slope,ADCparam_crs_offset,ADCparam_fn_slope,ADCparam_fn_offset, NRow,NCol)
            # flagging bad pixels to NaN
            missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
            data_ADCcorr[missingValMap]= numpy.NaN
            # set bad ADCcal values to NaN
            missingADCcorrMap= ADCparam_validMap==False    
            data_ADCcorr[:,:,missingADCcorrMap]= numpy.NaN # (both Smpl and Rst) 
            #
            # CDS & CMA
            #data_CDS= data_ADCcorr[1:,iSmpl,:,:] - data_ADCcorr[:-1,iRst,:,:]
            data_CDS= CDS(data_ADCcorr)
            if CMAFlag: data_CDSCMA= CMA(data_CDS,cols2CMA)
            else: data_CDSCMA= data_CDS* numpy.NaN
            #
            if pedSubtractFlag: 
                data_CDS= data_CDS-data_pedestal_CDS
                if CMAFlag: 
                    data_pedestal_CDSCMA= CMA(data_pedestal_CDS.reshape((1,NRow,NCol)),cols2CMA).reshape((NRow,NCol))
                    data_CDSCMA= data_CDSCMA-data_pedestal_CDSCMA
            #
            data_CDSavg= numpy.average(data_CDS[:,:,:],axis=0) # all img because already selected in the select images section
            data_CDSCMAavg= numpy.average(data_CDSCMA[:,:,:],axis=0) # all img because already selected in the select images section
            data_CDSCMAavg[:,cols2CMA[0]:cols2CMA[-1]+1]= numpy.NaN
            #
            if cleanMemFlag: del data_ADCcorr
        else: 
            data_CDSavg= numpy.ones((NRow,NCol))*numpy.NaN
            data_CDS= numpy.ones((NImg, NRow,NCol))*numpy.NaN
            data_CDSCMAavg= numpy.ones((NRow,NCol))*numpy.NaN
            data_CDSCMA= numpy.ones((NImg, NRow,NCol))*numpy.NaN
        # ---
        #%% show
        if showFlag:
            APy3_GENfuns.printcol("showing", 'blue')
            percDebug_plot_interactive_wCMA(dscrmbld_GnCrsFn, data_CDSavg,data_CDSCMAavg, manyImgFlag)
        # ---
        #%% save Avg
        if saveAvgFlag & ADCcorrCDSFlag:
            APy3_GENfuns.printcol("saving avg", 'blue')
            auxN= len(in_1file_suffix)*(-1)
            fileCDS_out=  file_in[:auxN] + out_AvgCDSfile_suffix
            if CMAFlag:
                APy3_GENfuns.write_1xh5(outFolder+fileCDS_out, data_CDSCMAavg, '/data/data/')
                if verboseFlag: APy3_GENfuns.printcol("CDS CMA avg saved as {0}".format(outFolder+fileCDS_out), 'green')
            else:
                APy3_GENfuns.write_1xh5(outFolder+fileCDS_out, data_CDSavg, '/data/data/')
                if verboseFlag: APy3_GENfuns.printcol("CDS avg saved as {0}".format(outFolder+fileCDS_out), 'green')
        # ---
        if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    #
    #%% that's all folks
    endTime=time.time()
    APy3_GENfuns.printcol("UseDLSraw_versatile ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    if verboseFlag: 
        APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green')
        for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
    #
    if CMAFlag: out_data= numpy.copy(data_CDSCMA)
    else: out_data= numpy.copy(data_CDS)
    #
    return out_data
# 
def UseDLSraw_versatile_SmplRst(mainFolder, # where data is
                        img2proc_str, # 'all'==all
                        #
                        ADCcorrCDSFlag,
                        #
                        ADCfile_Smpl_crs_slope,
                        ADCfile_Smpl_crs_offset,
                        ADCfile_Smpl_fn_slope,     
                        ADCfile_Smpl_fn_offset,
                        #
                        ADCfile_Rst_crs_slope,
                        ADCfile_Rst_crs_offset,
                        ADCfile_Rst_fn_slope,     
                        ADCfile_Rst_fn_offset,
                        #
                        CMAFlag,
                        cols2CMA_str,
                        #
                        pedSubtractFlag,
                        pedestalCDSFile,
                        #
                        lastFileOnlyFlag, # alternatively: process all files in folder
                        refColH1_0_Flag, # if refcol data are streamed out as H1<0> data.
                        #
                        showFlag,
                        manyImgFlag, # select more than 1 digit image in interactive plot
                        #
                        in_1file_suffix,
                        #
                        saveAvgFlag, # save 2D img (float): avg of ADCcorr, CDS, possibly CMA, possibly ped-Subtracted
                        outFolder,
                        out_AvgCDSfile_suffix,
                        #
                        highMemFlag,
                        cleanMemFlag,
                        verboseFlag):
    """ 
    DLSraw,ADCcor => CDS or CDS-CMA 
    this is obsolete and kept here only for retrocompatibility
    do not use it
    """
    startTime=time.time()
    APy3_GENfuns.printcol("UseDLSraw_versatile starting at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    # ---
    #
    #%% what's up doc
    APy3_GENfuns.printcol("will look at files {0} ... {1}".format(mainFolder,in_1file_suffix), 'blue')
    if lastFileOnlyFlag: APy3_GENfuns.printcol("will process only the most recent", 'blue')
    APy3_GENfuns.printcol("will process from in Img {0}".format(img2proc_str), 'blue')
    if refColH1_0_Flag: APy3_GENfuns.printcol("will H1<0> data as RefCol data", 'blue')
    if showFlag: APy3_GENfuns.printcol("will show images interactively", 'blue')
    #
    if ADCcorrCDSFlag: 
        APy3_GENfuns.printcol("will look ADCcor files:", 'blue')
        APy3_GENfuns.printcol(ADCfile_Smpl_crs_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_Smpl_crs_offset, 'blue')
        APy3_GENfuns.printcol(ADCfile_Smpl_fn_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_Smpl_fn_offset, 'blue')
        APy3_GENfuns.printcol(ADCfile_Rst_crs_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_Rst_crs_offset, 'blue')
        APy3_GENfuns.printcol(ADCfile_Rst_fn_slope, 'blue')
        APy3_GENfuns.printcol(ADCfile_Rst_fn_offset, 'blue')
        #
        if CMAFlag: APy3_GENfuns.printcol("will CMA using cols: {0}".format(cols2CMA_str), 'blue')
        if pedSubtractFlag: APy3_GENfuns.printcol("will look for pedestal file {0}".format(pedestalCDSFile), 'blue')
        if saveAvgFlag: 
            if pedSubtractFlag: APy3_GENfuns.printcol("will save an ADCcorr CDS avg (pedestal-subtracted) h5 file", 'blue') 
            else: APy3_GENfuns.printcol("will save an ADCcorr avg h5 files", 'blue')
            APy3_GENfuns.printcol("as {0} ... {1}".format(outFolder,out_AvgCDSfile_suffix), 'blue')
    if saveAvgFlag & (ADCcorrCDSFlag== False): APy3_GENfuns.printcol("cannot save an ADCcorr avg h5 file, if I am not allowed to ADCcor!", 'red')
    #
    if highMemFlag: APy3_GENfuns.printcol("fast, high memory usage", 'blue')
    else:  APy3_GENfuns.printcol("slow, small memory usage", 'blue')
    if cleanMemFlag: APy3_GENfuns.printcol("will try to free memory when possible", 'blue')
    if verboseFlag: APy3_GENfuns.printcol("verbose", 'blue')
    if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    # ---
    #
    #%% ADCcor files and pedestal files
    ADCparam_Smpl_crs_slope= numpy.ones((NRow,NCol))
    ADCparam_Smpl_crs_offset= numpy.ones((NRow,NCol))
    ADCparam_Smpl_fn_slope= numpy.ones((NRow,NCol))        
    ADCparam_Smpl_fn_offset= numpy.ones((NRow,NCol))
    ADCparam_Rst_crs_slope= numpy.ones((NRow,NCol))
    ADCparam_Rst_crs_Rst_offset= numpy.ones((NRow,NCol))
    ADCparam_Rst_fn_slope= numpy.ones((NRow,NCol))        
    ADCparam_Rst_fn_offset= numpy.ones((NRow,NCol))
    data_pedestal= numpy.zeros((NRow,NCol))
    #
    def aux_readh5(fileNamePath):
        if APy3_GENfuns.notFound(fileNamePath): APy3_GENfuns.printErr(fileNamePath+' not found')
        out_data= APy3_GENfuns.read_1xh5(fileNamePath, '/data/data/')
        return out_data
    #
    if ADCcorrCDSFlag:
        ADCparam_Smpl_crs_slope= aux_readh5(ADCfile_Smpl_crs_slope)
        ADCparam_Smpl_crs_offset= aux_readh5(ADCfile_Smpl_crs_offset)
        ADCparam_Smpl_fn_slope= aux_readh5(ADCfile_Smpl_fn_slope)
        ADCparam_Smpl_fn_offset= aux_readh5(ADCfile_Smpl_fn_offset)
        ADCparam_Rst_crs_slope= aux_readh5(ADCfile_Rst_crs_slope)
        ADCparam_Rst_crs_offset= aux_readh5(ADCfile_Rst_crs_offset)
        ADCparam_Rst_fn_slope= aux_readh5(ADCfile_Rst_fn_slope)
        ADCparam_Rst_fn_offset= aux_readh5(ADCfile_Rst_fn_offset)
        if verboseFlag: APy3_GENfuns.printcol("ADCcor files loaded", 'green')
        #
        if CMAFlag: 
            cols2CMA = APy3_GENfuns.matlabLike_range(cols2CMA_str)
            if verboseFlag: APy3_GENfuns.printcol("will CMA using cols {0}".format(str(cols2CMA)), 'green')
        else: cols2CMA= numpy.array([0])
        #
        if pedSubtractFlag:
            if APy3_GENfuns.notFound(pedestalCDSFile): APy3_GENfuns.printErr(pedestalCDSFile+' not found')
            data_pedestal_CDS= APy3_GENfuns.read_1xh5(pedestalCDSFile, '/data/data/') 
            if verboseFlag: APy3_GENfuns.printcol("pedestal file loaded", 'green')
    if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    #
    #%% list or last data files
    filelist_in= APy3_GENfuns.list_files(mainFolder, '*', in_1file_suffix) # all files
    if verboseFlag: APy3_GENfuns.printcol("{0} image sets found in folder".format(len(filelist_in)), 'green')
    if lastFileOnlyFlag:   
        if verboseFlag: APy3_GENfuns.printcol("will only process the most recent", 'green') 
        aux_fileName= os.path.basename( APy3_GENfuns.last_file(mainFolder, '*'+in_1file_suffix) ) # filename only, no path
        filelist_in= [aux_fileName]
    # ---
    for ifile,file_in in enumerate(filelist_in):
        APy3_GENfuns.printcol("collection {0}/{1}:".format(ifile,len(filelist_in)-1), 'blue')
        if verboseFlag: APy3_GENfuns.printcol(mainFolder+file_in, 'green')
        (dataSmpl_in,dataRst_in) = APy3_GENfuns.read_2xh5(mainFolder+file_in, '/data/','/reset/')
        (NImg, aux_NRow, aux_NCol) = dataSmpl_in.shape
        if verboseFlag: APy3_GENfuns.printcol("{0} Img read from file".format(NImg), 'green')
        # ---
        # select images
        if img2proc_str in ['all','All','ALL',':','*','-1']: 
            if verboseFlag: APy3_GENfuns.printcol("will read all Img", 'green')
        else:
            img2proc= APy3_GENfuns.matlabLike_range(img2proc_str)
            fromImg= img2proc[0]
            toImg= img2proc[-1]
            NImg= toImg-fromImg+1
            if verboseFlag: APy3_GENfuns.printcol("will use Img from {0} to {1} (included), for a total of {2}".format(fromImg,toImg,NImg),'green')
            dataSmpl_in= dataSmpl_in[fromImg:toImg+1,:,:]
            dataRst_in=  dataRst_in[fromImg:toImg+1,:,:]
        # ---
        #%% convert to GnCrsFn 
        APy3_GENfuns.printcol("converting to Gn,Crs,Fn", 'blue')
        if highMemFlag: dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(dataSmpl_in,dataRst_in, ERRDLSraw,ERRint16)
        else:
            dscrmbld_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
            for thisImg in range(NImg):
                thisSmpl_DLSraw= dataSmpl_in[thisImg,:,:].reshape((1, NRow,NCol))
                thisRst_DLSraw=  dataRst_in[thisImg,:,: ].reshape((1, NRow,NCol))
                this_dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
                dscrmbld_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
                if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
        # ---
        #%% ADCcor, CDS, CMA, pedSub
        if ADCcorrCDSFlag: 
            APy3_GENfuns.printcol("ADC-correcting, CDS-ing", 'blue')
            """
            data_ADCcorr= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                                  ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl only is correct
            """
            (auxNImg,ignNSR,ignNRow,ignNCol,ignNGCF)= dscrmbld_GnCrsFn.shape
            data_ADCcorr= numpy.zeros((auxNImg,NSmplRst,NRow,NCol))*numpy.NaN
            data_ADCcorr[:,iSmpl,:,:]= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iSmpl,:,:,iCrs],dscrmbld_GnCrsFn[:,iSmpl,:,:,iFn],
                                                              ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl            

            data_ADCcorr[:,iRst,:,:]= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                                              ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, NRow,NCol) # Rst
            # flagging bad pixels to NaN
            missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
            data_ADCcorr[missingValMap]= numpy.NaN
            # set bad ADCcal values to NaN
            #missingADCcorrMap= ADCparam_validMap==False    
            #data_ADCcorr[:,:,missingADCcorrMap]= numpy.NaN # (both Smpl and Rst) 
            #
            # CDS & CMA
            data_CDS= CDS(data_ADCcorr)
            if CMAFlag: data_CDSCMA= CMA(data_CDS,cols2CMA)
            else: data_CDSCMA= data_CDS* numpy.NaN
            #
            if pedSubtractFlag: 
                data_CDS= data_CDS-data_pedestal_CDS
                if CMAFlag: 
                    data_pedestal_CDSCMA= CMA(data_pedestal_CDS.reshape((1,NRow,NCol)),cols2CMA).reshape((NRow,NCol))
                    data_CDSCMA= data_CDSCMA-data_pedestal_CDSCMA
            #
            data_CDSavg= numpy.average(data_CDS[:,:,:],axis=0) # all img because already selected in the select images section
            data_CDSCMAavg= numpy.average(data_CDSCMA[:,:,:],axis=0) # all img because already selected in the select images section
            data_CDSCMAavg[:,cols2CMA[0]:cols2CMA[-1]+1]= numpy.NaN
            #
            if cleanMemFlag: del data_ADCcorr
        else: 
            data_CDSavg= numpy.ones((NRow,NCol))*numpy.NaN
            data_CDS= numpy.ones((NImg, NRow,NCol))*numpy.NaN
            data_CDSCMAavg= numpy.ones((NRow,NCol))*numpy.NaN
            data_CDSCMA= numpy.ones((NImg, NRow,NCol))*numpy.NaN
        # ---
        #%% show
        if showFlag:
            APy3_GENfuns.printcol("showing", 'blue')
            percDebug_plot_interactive_wCMA(dscrmbld_GnCrsFn, data_CDSavg,data_CDSCMAavg, manyImgFlag)
        # ---
        #%% save Avg
        if saveAvgFlag & ADCcorrCDSFlag:
            APy3_GENfuns.printcol("saving avg", 'blue')
            auxN= len(in_1file_suffix)*(-1)
            fileCDS_out=  file_in[:auxN] + out_AvgCDSfile_suffix
            if CMAFlag:
                APy3_GENfuns.write_1xh5(outFolder+fileCDS_out, data_CDSCMAavg, '/data/data/')
                if verboseFlag: APy3_GENfuns.printcol("CDS CMA avg saved as {0}".format(outFolder+fileCDS_out), 'green')
            else:
                APy3_GENfuns.write_1xh5(outFolder+fileCDS_out, data_CDSavg, '/data/data/')
                if verboseFlag: APy3_GENfuns.printcol("CDS avg saved as {0}".format(outFolder+fileCDS_out), 'green')
        # ---
        if verboseFlag: APy3_GENfuns.printcol("--  --  --  --", 'blue')
    #
    #%% that's all folks
    endTime=time.time()
    APy3_GENfuns.printcol("UseDLSraw_versatile ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    if verboseFlag: 
        APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green')
        for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
    #
    if CMAFlag: out_data= numpy.copy(data_CDSCMA)
    else: out_data= numpy.copy(data_CDS)
    #
    return out_data
#
def UseDLSraw_ADCcor_SmplRst(mainFolder,
                     in_1file_suffix,
                     img2proc_str,
                     #
                     ADCfile_Smpl_crs_slope,
                     ADCfile_Smpl_crs_offset,
                     ADCfile_Smpl_fn_slope,     
                     ADCfile_Smpl_fn_offset,
                     #
                     ADCfile_Rst_crs_slope,
                     ADCfile_Rst_crs_offset,
                     ADCfile_Rst_fn_slope,     
                     ADCfile_Rst_fn_offset,
                     #
                     cleanMemFlag,
                     verboseFlag):
    """ 
    DLSraw,ADCcor => corrected Smpl,Rst 
    this is obsolete and kept here only for retrocompatibility
    do not use it, use convert_DLSraw_2_e_wLatOvflw instead
    """
    # load ADCcor
    if APy3_GENfuns.notFound(ADCfile_Smpl_crs_slope):  APy3_GENfuns.printErr(ADCfile_Smpl_crs_slope+' not found')
    if APy3_GENfuns.notFound(ADCfile_Smpl_crs_offset): APy3_GENfuns.printErr(ADCfile_Smpl_crs_offset+' not found')
    if APy3_GENfuns.notFound(ADCfile_Smpl_fn_slope):   APy3_GENfuns.printErr(ADCfile_Smpl_fn_slope+' not found')
    if APy3_GENfuns.notFound(ADCfile_Smpl_fn_offset):  APy3_GENfuns.printErr(ADCfile_Smpl_fn_offset+' not found')
    if APy3_GENfuns.notFound(ADCfile_Rst_crs_slope):  APy3_GENfuns.printErr(ADCfile_Rst_crs_slope+' not found')
    if APy3_GENfuns.notFound(ADCfile_Rst_crs_offset): APy3_GENfuns.printErr(ADCfile_Rst_crs_offset+' not found')
    if APy3_GENfuns.notFound(ADCfile_Rst_fn_slope):   APy3_GENfuns.printErr(ADCfile_Rst_fn_slope+' not found')
    if APy3_GENfuns.notFound(ADCfile_Rst_fn_offset):  APy3_GENfuns.printErr(ADCfile_Rst_fn_offset+' not found')
    #
    ADCparam_Smpl_crs_slope= APy3_GENfuns.read_1xh5(ADCfile_Smpl_crs_slope, '/data/data/')
    ADCparam_Smpl_crs_offset= APy3_GENfuns.read_1xh5(ADCfile_Smpl_crs_offset, '/data/data/')
    ADCparam_Smpl_fn_slope= APy3_GENfuns.read_1xh5(ADCfile_Smpl_fn_slope, '/data/data/')        
    ADCparam_Smpl_fn_offset= APy3_GENfuns.read_1xh5(ADCfile_Smpl_fn_offset, '/data/data/')    
    ADCparam_Rst_crs_slope= APy3_GENfuns.read_1xh5(ADCfile_Rst_crs_slope, '/data/data/')
    ADCparam_Rst_crs_offset= APy3_GENfuns.read_1xh5(ADCfile_Rst_crs_offset, '/data/data/')
    ADCparam_Rst_fn_slope= APy3_GENfuns.read_1xh5(ADCfile_Rst_fn_slope, '/data/data/')        
    ADCparam_Rst_fn_offset= APy3_GENfuns.read_1xh5(ADCfile_Rst_fn_offset, '/data/data/')
    #
    #find DLSraw file 
    inputFile= APy3_GENfuns.last_file(mainFolder, "*"+in_1file_suffix)
    if verboseFlag: APy3_GENfuns.printcol("will read file: "+inputFile, 'green')
    #---
    #read file
    if verboseFlag: APy3_GENfuns.printcol("reading files", 'blue')
    if APy3_GENfuns.notFound(inputFile): APy3_GENfuns.printErr(inputFile+' not found')
    (dataSmpl_DLSraw, dataRst_DLSraw) = APy3_GENfuns.read_2xh5(inputFile, '/data/','/reset/')
    (NImg, aux_NRow, aux_NCol) = dataSmpl_DLSraw.shape
    if verboseFlag: APy3_GENfuns.printcol("{0} Img read from files".format(NImg), 'green')
    #---
    # select images
    if img2proc_str in ['all','All','ALL',':','*','-1']: 
        if verboseFlag: APy3_GENfuns.printcol("will read all Img", 'green')
    else:
        img2proc= APy3_GENfuns.matlabLike_range(img2proc_str)
        fromImg= img2proc[0]
        toImg= img2proc[-1]
        NImg= toImg-fromImg+1
        if verboseFlag: APy3_GENfuns.printcol("will use Img from {0} to {1} (included), for a total of {2}".format(fromImg,toImg,NImg),'green')
        dataSmpl_DLSraw= dataSmpl_DLSraw[fromImg:toImg+1,:,:]
        dataRst_DLSraw=  dataRst_DLSraw[fromImg:toImg+1,:,:]
    #---
    # DLSraw to GnCrsFn
    if verboseFlag: APy3_GENfuns.printcol("converting to GnCrsFn", 'blue')
    data_GnCrsFn= convert_DLSraw_2_GnCrsFn(dataSmpl_DLSraw,dataRst_DLSraw, ERRDLSraw, ERRint16)
    if cleanMemFlag: del dataSmpl_DLSraw; del dataRst_DLSraw
    #---    
    #%% ADCcorrect    
    if verboseFlag: APy3_GENfuns.printcol("ADC-correcting", 'blue')
    (auxNImg,ignNSR,ignNR,ignNC,ignNGCF)= data_GnCrsFn.shape
    data_ADCcorr= numpy.zeros((auxNImg,NSmplRst,NRow,NCol))
    data_ADCcorr[:,iSmpl,:,:]= ADCcorr_NoGain(data_GnCrsFn[:,iSmpl,:,:,iCrs],data_GnCrsFn[:,iSmpl,:,:,iFn],
                                              ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
    data_ADCcorr[:,iRst,:,:]=  ADCcorr_NoGain(data_GnCrsFn[:,iRst,:,:,iCrs], data_GnCrsFn[:,iRst,:,:,iFn],
                                              ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
    #---    
    # flagging bad pixels    
    if verboseFlag: APy3_GENfuns.printcol("flagging bad pixels", 'blue')
    # set the missing vales to NaN
    missingValMap= data_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
    data_ADCcorr[missingValMap]= numpy.NaN
    #---
    return data_ADCcorr
#
#
def convert_GnCrsFn_2_e_wLatOvflw(dscrmbld_GnCrsFn, CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,verboseFlag):
    """ data GnCrsFn => ADCcorr => CMA,CDS Gn0 (if needed) => Lat Ovflw Gn => data in e """
    #%% convert to GnCrsFn
    (NImg,ignNSR,ignNRow,ignNCol,ignN3)= dscrmbld_GnCrsFn.shape
    #%% ADCcor, CDS, CMA, pedSub
    if verboseFlag: APy3_GENfuns.printcol("  ADC-correcting", 'blue')
    data_ADU= APy3_GENfuns.numpy_NaNs((NImg,NSmplRst,NRow,NCol))
    data_ADU[:,iSmpl,:,:]= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iSmpl,:,:,iCrs],dscrmbld_GnCrsFn[:,iSmpl,:,:,iFn],
                                          ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,
                                          ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl            
    data_ADU[:,iRst,:,:]=  ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                          ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,
                                          ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, NRow,NCol) # Rst
    data_Gn= numpy.copy(dscrmbld_GnCrsFn[:,iSmpl,:,:,iGn])
    # flagging bad pixels to NaN
    missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
    data_ADU[missingValMap]= numpy.NaN
    if cleanMemFlag: del dscrmbld_GnCrsFn; del missingValMap
    #
    data_CMACDS_e= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded, and the array will be reduced to (NImg-1)
    #
    for thisGn in range(NGn):
        if verboseFlag: APy3_GENfuns.printcol('  checking data Gn{0}'.format(thisGn),'blue')
        data_xGn= numpy.copy(data_ADU)
        thisPedestalADU_multiGn= numpy.copy(PedestalADU_multiGn)
        GnX_map= data_Gn[:,:,:]==thisGn
        data_xGn[:,iSmpl,:,:][~GnX_map]= numpy.NaN
        #
        data_CDS_xGn= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded
        #
        if (numpy.sum(GnX_map)==0)|(numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all())|(numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all()): 
            if verboseFlag: APy3_GENfuns.printcol('    no valid values that for Gn','blue')
            #if (numpy.sum(GnX_map)==0)&verboseFlag: APy3_GENfuns.printcol('    as numpy.sum(GnX_map)==0','blue')
            #if (numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all())&verboseFlag: APy3_GENfuns.printcol('    as numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all()','blue')
            #if (numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all())&verboseFlag: APy3_GENfuns.printcol('    as numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all()','blue')

            data_xGn_e= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded
        else:
            #
            if thisGn==0:
                if CMAFlag:
                    if verboseFlag: APy3_GENfuns.printcol('    CMA-ing Gn0','blue')
                    data_xGn[:,iSmpl,:,:]= CMA(data_xGn[:,iSmpl,:,:] ,cols2CMA)
                    data_xGn[:,iRst,:,:]=  CMA(data_xGn[:,iRst,:,:]  ,cols2CMA)
                    data_xGn[thisGn,:,:,(cols2CMA[0]):(cols2CMA[-1]+1)]= numpy.NaN
                    #
                    thisPedestalADU_multiGn[thisGn,:,:]= CMA(PedestalADU_multiGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
                    thisPedestalADU_multiGn[thisGn,:,(cols2CMA[0]):(cols2CMA[-1]+1)]= numpy.NaN
                #
                if CDSFlag: 
                    if verboseFlag: APy3_GENfuns.printcol('    CDS-ing Gn0','blue')
                    data_CDS_xGn[1:,:,:]= CDS(data_xGn)
                else: 
                    if verboseFlag: APy3_GENfuns.printcol('    using Smpl for Gn0','blue')
                    data_CDS_xGn[1:,:,:]= numpy.copy(data_xGn[1:,iSmpl,:,:])
                    #
            else:
                if verboseFlag: APy3_GENfuns.printcol('    using Smpl for Gn>0','blue')
                data_CDS_xGn[1:,:,:]= numpy.copy(data_xGn[1:,iSmpl,:,:])
            #
            if verboseFlag: APy3_GENfuns.printcol('    ADU=>e','blue')
            data_xGn_e= (data_CDS_xGn-thisPedestalADU_multiGn[thisGn,:,:])*e_per_ADU_multiGn[thisGn,:,:]
        #
        data_CMACDS_e[GnX_map]= numpy.copy(data_xGn_e[GnX_map])
        if cleanMemFlag: del data_CDS_xGn; del data_xGn; del GnX_map; del data_xGn_e
    #
    data_CMACDS_e=  data_CMACDS_e[1:,:,:] # discard 1st img, which is NAN anyway (useless, as it is saturated)
    return data_CMACDS_e
#
def convert_DLSraw_2_e_wLatOvflw(dataSmpl_DLSraw,dataRst_DLSraw, CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,verboseFlag):
    """ data DLSraw => ADCcorr => CMA,CDS Gn0 (if needed) => Lat Ovflw Gn => data in e """
    #%% convert to GnCrsFn 
    if verboseFlag: APy3_GENfuns.printcol("  converting to Gn,Crs,Fn", 'blue')
    (NImg,ignNRow,ignNCol)= dataSmpl_DLSraw.shape
    if highMemFlag: dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(dataSmpl_DLSraw,dataRst_DLSraw, ERRDLSraw,ERRint16)
    else:
        dscrmbld_GnCrsFn= numpy.zeros((NImg,NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
        for thisImg in range(NImg):
            thisSmpl_DLSraw= dataSmpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
            thisRst_DLSraw=  dataRst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
            this_dscrmbld_GnCrsFn= convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
            dscrmbld_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
            if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,NImg)
            del thisSmpl_DLSraw; del thisRst_DLSraw; del this_dscrmbld_GnCrsFn
    if cleanMemFlag: del dataSmpl_DLSraw; del dataRst_DLSraw
    # ---
    #%% ADCcor, CDS, CMA, pedSub
    if verboseFlag: APy3_GENfuns.printcol("  ADC-correcting", 'blue')
    data_ADU= APy3_GENfuns.numpy_NaNs((NImg,NSmplRst,NRow,NCol))
    data_ADU[:,iSmpl,:,:]= ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iSmpl,:,:,iCrs],dscrmbld_GnCrsFn[:,iSmpl,:,:,iFn],
                                          ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,
                                          ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl            
    data_ADU[:,iRst,:,:]=  ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                          ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,
                                          ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, NRow,NCol) # Rst
    data_Gn= numpy.copy(dscrmbld_GnCrsFn[:,iSmpl,:,:,iGn])
    # flagging bad pixels to NaN
    missingValMap= dscrmbld_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
    data_ADU[missingValMap]= numpy.NaN
    if cleanMemFlag: del dscrmbld_GnCrsFn; del missingValMap
    #
    data_CMACDS_e= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded, and the array will be reduced to (NImg-1)
    #
    for thisGn in range(NGn):
        if verboseFlag: APy3_GENfuns.printcol('  checking data Gn{0}'.format(thisGn),'blue')
        data_xGn= numpy.copy(data_ADU)
        thisPedestalADU_multiGn= numpy.copy(PedestalADU_multiGn)
        GnX_map= data_Gn[:,:,:]==thisGn
        data_xGn[:,iSmpl,:,:][~GnX_map]= numpy.NaN
        #
        data_CDS_xGn= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded
        #data_xGn_e= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol))
        #
        if (numpy.sum(GnX_map)==0)|(numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all())|(numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all()): 
            if verboseFlag: APy3_GENfuns.printcol('    no valid values that for Gn','blue')
            if (numpy.sum(GnX_map)==0)&verboseFlag: APy3_GENfuns.printcol('    as numpy.sum(GnX_map)==0','blue')
            if (numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all())&verboseFlag: APy3_GENfuns.printcol('    as numpy.isnan(PedestalADU_multiGn[thisGn,:,:]).all()','blue')
            if (numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all())&verboseFlag: APy3_GENfuns.printcol('    as numpy.isnan(e_per_ADU_multiGn[thisGn,:,:]).all()','blue')

            data_xGn_e= APy3_GENfuns.numpy_NaNs((NImg,NRow,NCol)) # note that this is NImg, but in the end the 1st img will be discarded
            if cleanMemFlag: del data_xGn
        else:
            #
            if thisGn==0:
                if CMAFlag:
                    if verboseFlag: APy3_GENfuns.printcol('    CMA-ing Gn0','blue')
                    data_xGn[:,iSmpl,:,:]= CMA(data_xGn[:,iSmpl,:,:] ,cols2CMA)
                    data_xGn[:,iRst,:,:]=  CMA(data_xGn[:,iRst,:,:]  ,cols2CMA)
                    data_xGn[thisGn,:,:,(cols2CMA[0]):(cols2CMA[-1]+1)]= numpy.NaN
                    #
                    thisPedestalADU_multiGn[thisGn,:,:]= CMA(PedestalADU_multiGn[thisGn,:,:].reshape((1,NRow,NCol)) ,cols2CMA).reshape((NRow,NCol))
                    thisPedestalADU_multiGn[thisGn,:,(cols2CMA[0]):(cols2CMA[-1]+1)]= numpy.NaN
                #
                if CDSFlag: 
                    if verboseFlag: APy3_GENfuns.printcol('    CDS-ing Gn0','blue')
                    data_CDS_xGn[1:,:,:]= CDS(data_xGn)
                else: 
                    if verboseFlag: APy3_GENfuns.printcol('    using Smpl for Gn0','blue')
                    data_CDS_xGn[1:,:,:]= numpy.copy(data_xGn[1:,iSmpl,:,:])
                    #
            else:
                if verboseFlag: APy3_GENfuns.printcol('    using Smpl for Gn>0','blue')
                data_CDS_xGn[1:,:,:]= numpy.copy(data_xGn[1:,iSmpl,:,:])
            #
            if verboseFlag: APy3_GENfuns.printcol('    ADU=>e','blue')
            if cleanMemFlag: del data_xGn
            data_xGn_e= (data_CDS_xGn-thisPedestalADU_multiGn[thisGn,:,:])*e_per_ADU_multiGn[thisGn,:,:]
        #
        data_CMACDS_e[GnX_map]= numpy.copy(data_xGn_e[GnX_map])
        if cleanMemFlag: del data_CDS_xGn; del GnX_map; del data_xGn_e
    #
    data_CMACDS_e=  data_CMACDS_e[1:,:,:] # discard 1st img, which is NAN anyway (useless, as it is saturated)
    return data_CMACDS_e
