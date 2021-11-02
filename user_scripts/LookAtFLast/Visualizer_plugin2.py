# -*- coding: utf-8 -*-
"""
Not Descramble, not reorder; just visualize small dataset (seq Mod)
SerFri 2020 09 07 version includes: britisBits translation, big-to-small-endian translation, pad ordering ?7x32[44 times] => 7x(32*44)
plugin2 should include : Smp/Rst reorder, avoid DAQ disorder


load environment on cfeld-perc02 is:
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
load environment on cfeld-perc06 is:
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/bin/activate root

on my laptop
source ~/Utili/Anaconda3/bin/activate root

python3 ./xxx.py
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
#---
#
#%% functs
#
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
    
    if img2proc_str in APy3_GENfuns.ALLlist: 
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
        (dataSmpl_fl0, dataRst_fl0) = APy3_GENfuns.read_partial_2xh5(inputFiles[0], '/data/','/reset/', fromImg_fl01,toImg_fl01)
        (dataSmpl_fl1, dataRst_fl1) = APy3_GENfuns.read_partial_2xh5(inputFiles[1], '/data/','/reset/', fromImg_fl01,toImg_fl01)
    #
    (NImg_fl0, aux_NRow, aux_NCol) = dataSmpl_fl0.shape
    (NImg_fl1, aux_NRow, aux_NCol) = dataSmpl_fl1.shape
    NImg = NImg_fl0 + NImg_fl1
    if verboseFlag: APy3_GENfuns.printcol("Smpl: {0}+{1} Img read from files".format(NImg_fl0,NImg_fl1), 'green')
    #
    (NImg_R_fl0, aux_NRow, aux_NCol) = dataRst_fl0.shape
    (NImg_R_fl1, aux_NRow, aux_NCol) = dataRst_fl1.shape
    if verboseFlag: APy3_GENfuns.printcol("Rst: {0}+{1} Img read from files".format(NImg_R_fl0,NImg_R_fl1), 'green')
    #
    if not(NImg_fl0==NImg_fl1==NImg_R_fl0==NImg_R_fl1): APy3_GENfuns.printcol("different number of images in Smpl/Rst/file1/file2", 'red')
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
def NOTdescrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH1_0_Flag, 
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
    #%% swapSmplRstFlag # set to False
    if swapSmplRstFlag:
        aux_scrmblSmpl= numpy.copy(scrmblRst)
        aux_scrmblRst = numpy.copy(scrmblSmpl)
        #
        scrmblSmpl = numpy.copy(aux_scrmblSmpl)
        scrmblRst= numpy.copy(aux_scrmblRst)
        del aux_scrmblSmpl; del aux_scrmblRst
    #
    '''
    #%% solving 4a DAQ-scrambling: byte swap in hex (By0,By1) => (By1,By0)
    # no need to do it, because SerFir does it
    if verboseFlag: APy3_GENfuns.printcol("solving DAQ-scrambling: byte-swapping and Smpl-Rst-swapping", 'blue')
    scrmblSmpl_byteSwap= APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblSmpl)
    scrmblRst_byteSwap = APy3_GENfuns.convert_hex_byteSwap_2nd(scrmblRst)  
    scrmblSmpl= numpy.copy(scrmblSmpl_byteSwap)
    scrmblRst= numpy.copy(scrmblRst_byteSwap)
    del scrmblSmpl_byteSwap; del scrmblRst_byteSwap
    '''
    # ---
    '''
    #######################################################################################################################################
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
    data2srcmbl_noRefCol[:,iSmpl,:,:]= convert_odin_daq_2_mezzanine(scrmblSmpl)
    data2srcmbl_noRefCol[:,iRst,:,:] = convert_odin_daq_2_mezzanine(scrmblRst)
    #
    scrmblSmpl= numpy.copy(data2srcmbl_noRefCol[:,iSmpl,:,:])
    scrmblRst=  numpy.copy(data2srcmbl_noRefCol[:,iRst ,:,:])
    if cleanMemFlag: del data2srcmbl_noRefCol
    #####################################################################################################################################
    #'''
    #
    # ---
    #
    '''
    # reorder pixels as described by SerFri
    APy3_GENfuns.printcol(str(scrmblSmpl.shape),'orange')
    scrmblSmpl_xpack= scrmblSmpl.reshape((NImg, 212,4, 11, 7,32))
    scrmblRst_xpack=  scrmblRst.reshape( (NImg, 212,4, 11, 7,32))
    #
    scrmblSmpl_NoRefCol= numpy.ones((NImg,212,44,7,32), dtype='uint16') * ERRDLSraw
    scrmblRst_NoRefCol=  numpy.ones((NImg,212,44,7,32), dtype='uint16') * ERRDLSraw
    
    for iImg in range(NImg):
        for iRowGrp in range(212):
            scrmblSmpl_NoRefCol[iImg,iRowGrp,0:22:2,:,:]=  scrmblSmpl_xpack[iImg,iRowGrp,0,0:11,:,:]
            scrmblSmpl_NoRefCol[iImg,iRowGrp,1:22:2,:,:]=  scrmblSmpl_xpack[iImg,iRowGrp,1,0:11,:,:]
            scrmblSmpl_NoRefCol[iImg,iRowGrp,22:44:2,:,:]= scrmblSmpl_xpack[iImg,iRowGrp,2,0:11,:,:]
            scrmblSmpl_NoRefCol[iImg,iRowGrp,23:44:2,:,:]= scrmblSmpl_xpack[iImg,iRowGrp,3,0:11,:,:]
            #
            scrmblRst_NoRefCol[iImg,iRowGrp,0:22:2,:,:]=  scrmblRst_xpack[iImg,iRowGrp,0,0:11,:,:]
            scrmblRst_NoRefCol[iImg,iRowGrp,1:22:2,:,:]=  scrmblRst_xpack[iImg,iRowGrp,1,0:11,:,:]
            scrmblRst_NoRefCol[iImg,iRowGrp,22:44:2,:,:]= scrmblRst_xpack[iImg,iRowGrp,2,0:11,:,:]
            scrmblRst_NoRefCol[iImg,iRowGrp,23:44:2,:,:]= scrmblRst_xpack[iImg,iRowGrp,3,0:11,:,:]
    #
    scrmblSmpl_NoRefCol= numpy.transpose(scrmblSmpl_NoRefCol,(0,1,3,2,4)) # (NImg,212,7,44,32)
    scrmblRst_NoRefCol=  numpy.transpose(scrmblRst_NoRefCol, (0,1,3,2,4)) # (NImg,212,7,44,32)
    scrmblSmpl_NoRefCol= scrmblSmpl_NoRefCol.reshape((NImg,NRow,44*32))
    scrmblRst_NoRefCol=  scrmblRst_NoRefCol.reshape( (NImg,NRow,44*32))
    #
    scrmblSmpl= numpy.copy(scrmblSmpl_NoRefCol)
    scrmblRst= numpy.copy(scrmblRst_NoRefCol)
    APy3_GENfuns.printcol(str(scrmblSmpl.shape),'orange')
    if cleanMemFlag: del scrmblSmpl_xpack; del scrmblRst_xpack; del scrmblSmpl_NoRefCol; del scrmblRst_NoRefCol
    '''
    #
    #---
    #
    '''
    #%% 7x32,7x32,7x32,...[44 times] => 7x(32*44)
    scrmblSmpl=scrmblSmpl.reshape((NImg,212,44,7,32)) 
    scrmblRst= scrmblRst.reshape((NImg,212,44,7,32))
    #
    scrmblSmpl= numpy.transpose(scrmblSmpl,(0,1,3,2,4)) # (NImg,212,7,44,32)
    scrmblRst= numpy.transpose( scrmblRst,(0,1,3,2,4))  # (NImg,212,7,44,32)
    scrmblSmpl= scrmblSmpl.reshape((NImg,212*7,44*32))    
    scrmblRst=  scrmblRst.reshape((NImg,212*7,44*32))    
    '''
    #
    '''
    #%% alternative 7x32,7x32,7x32,...[44 times] => 7x(32*44)
    def rearrange4packets(inputArr, showFlag):
        """ 44pads*224pixels => 7row,(44pad*32col) """
        # e.g. inputarr=numpy.arange(44*7*32)
        outputarr= inputArr.reshape((44,7,32))            # (44,7*32) => (44,7,32)
        outputarr= numpy.transpose( outputarr,(1,0,2))  # (44,7,32) =>(7,44,32)
        outputarr= outputarr.reshape(44*7*32)
        if showFlag:
            APy3_GENfuns.plot_2D_stretched(inputArr.reshape(1,len(inputArr)),  '','','before processing',True,-1)
            APy3_GENfuns.plot_2D_stretched(outputarr.reshape(1,len(outputarr)),'','','after processing',True,-1)
        return outputarr

    scrmblSmpl=scrmblSmpl.reshape((NImg,212,44*7*32))
    scrmblRst= scrmblRst.reshape((NImg,212,44*7*32))
    for iImg in range(NImg):
        for iGrp in range(212):
            #print("iImg{0},iGrp{1}".format(iImg,iGrp))
            scrmblSmpl[iImg,iGrp,:]= rearrange4packets(scrmblSmpl[iImg,iGrp,:],False)
            scrmblRst[iImg,iGrp,:]=  rearrange4packets(scrmblRst[iImg,iGrp,:], False)
    scrmblSmpl= scrmblSmpl.reshape((NImg,212*7,44*32))    
    scrmblRst=  scrmblRst.reshape((NImg,212*7,44*32)) 
    '''
    #
    # ---
    #
    '''
    #%% do not know why, but all pads in a row in a H seem inverted right-to-left    
    scrmblSmpl= scrmblSmpl.reshape((NImg,NRow, 44,32))
    scrmblRst=  scrmblRst.reshape( (NImg,NRow, 44,32))
    aux_Smpl= numpy.copy(scrmblSmpl)
    aux_Rst=  numpy.copy(scrmblRst)
    for frompad,topad in enumerate(numpy.arange(21,-1,-1)):
        scrmblSmpl[:,:,topad,:]= aux_Smpl[:,:,frompad,:]
        scrmblRst[:,:,topad,:]=  aux_Rst[ :,:,frompad,:]
    for frompad,topad in enumerate(numpy.arange(43,21,-1)):
        scrmblSmpl[:,:,topad,:]= aux_Smpl[:,:,22+frompad,:]
        scrmblRst[:,:,topad,:]=  aux_Rst[:,:,22+frompad,:]
    scrmblSmpl= scrmblSmpl.reshape((NImg,NRow, 44*32))
    scrmblRst=  scrmblRst.reshape( (NImg,NRow, 44*32))
    del aux_Smpl; del aux_Rst
    '''
    # ---
    #
    '''
    #%% reverse bit order [abcd] becomes [dcba] 
    # in older versions, no need to do it, because SerFir did it (not implemented here)
    Smpl_bitted= numpy.copy(APy3_GENfuns.convert_uint_2_bits_Ar(scrmblSmpl,16) )
    scrmblSmpl= numpy.copy(APy3_GENfuns.convert_bits_2_uint16_Ar(Smpl_bitted[:,:,:,14::-1]) )
    Rst_bitted= numpy.copy(APy3_GENfuns.convert_uint_2_bits_Ar(scrmblRst,16) )
    scrmblRst= numpy.copy(APy3_GENfuns.convert_bits_2_uint16_Ar(Rst_bitted[:,:,:,14::-1]) )
    del Smpl_bitted; del Rst_bitted
    '''
    # ---
    #
    '''
    #%% british bits : 11000=>00111
    # no need to do it, because SerFir does it
    aux_Smpl= numpy.copy(scrmblSmpl)
    aux_Rst=  numpy.copy(scrmblRst)
    scrmblSmpl= ((2**15)-1) - aux_Smpl
    scrmblRst=  ((2**15)-1) - aux_Rst
    del aux_Smpl; del aux_Rst
    '''    
    #---
    
    
    '''
    #%% moving stuff around, v3
    
    quarter= 1408//4 #352     #0,352,704,1056
    
    aux_Smpl= numpy.copy( scrmblSmpl.reshape((NImg,212,7,44*32)) )
    #aux_Smpl= numpy.copy( scrmblRst.reshape((NImg,212,7,44*32)) )
    #
    aux_Rst= numpy.zeros_like(aux_Smpl)
    aux_Rst[:,:,:]= ERRDLSraw     
 
    
    #%%ADC0
    #startFrom=0
    #aux_Rst[:,:,0,0:(quarter)]= numpy.copy(aux_Smpl[:,:,0,(startFrom):(startFrom+quarter)])
    #aux_Rst[:,:,0,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,0,(startFrom+quarter):(startFrom+quarter+quarter)])  
    #aux_Rst[:,:,0,(quarter+quarter):(quarter+quarter+quarter)]= numpy.copy(aux_Smpl[:,:,0,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) 
    #aux_Rst[:,:,0,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,0,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)])
    aux_Rst[:,:,0,:]= aux_Smpl[:,:,0,:]
   
    #%%ADC1
    #startFrom=0
    #aux_Rst[:,:,1,0:(quarter)]= numpy.copy(aux_Smpl[:,:,1,(startFrom):(startFrom+quarter)])
    #aux_Rst[:,:,1,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,1,(startFrom+quarter):(startFrom+quarter+quarter)])  
    #aux_Rst[:,:,1,(quarter+quarter):(quarter+quarter+quarter)]= numpy.copy(aux_Smpl[:,:,1,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) 
    #aux_Rst[:,:,1,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,1,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)])
    aux_Rst[:,:,1,:]= aux_Smpl[:,:,1,:]



    #%%ADC2
    startFrom=0
    aux_Rst[:,:,2,0:(quarter)]= numpy.copy(aux_Smpl[:,:,2,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)]) # 0 <=3

    aux_Rst[:,:,2,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,2,(startFrom):(startFrom+quarter)]) # 1<=0

    aux_Rst[:,:,2,(quarter+quarter):(quarter+quarter+quarter)]=  numpy.copy(aux_Smpl[:,:,2,(startFrom+quarter):(startFrom+quarter+quarter)]) #  2<=1

    aux_Rst[:,:,2,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,2,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) # 3<=2
    

    #%%ADC3
    startFrom=0
    #aux_Rst[:,:,3,0:(quarter)]= 

    aux_Rst[:,:,3,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,3,(startFrom):(startFrom+quarter)]) # 1<=0
    # also the same:  aux_Rst[:,:,3,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,3,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) #  1<=2 

    aux_Rst[:,:,3,(quarter+quarter):(quarter+quarter+quarter)]=  numpy.copy(aux_Smpl[:,:,3,(startFrom+quarter):(startFrom+quarter+quarter)]) #  2<=1 
    #also the same: aux_Rst[:,:,3,(quarter+quarter):(quarter+quarter+quarter)]=  numpy.copy(aux_Smpl[:,:,3,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)]) #  2<=3 

    #aux_Rst[:,:,3,(1408-quarter):(1408)]= 


    
    #%%ADC4
    #startFrom=0
    #aux_Rst[:,:,4,0:(quarter)]= numpy.copy(aux_Smpl[:,:,4,(startFrom):(startFrom+quarter)])
    #aux_Rst[:,:,4,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,4,(startFrom+quarter):(startFrom+quarter+quarter)])  
    #aux_Rst[:,:,4,(quarter+quarter):(quarter+quarter+quarter)]= numpy.copy(aux_Smpl[:,:,4,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) 
    #aux_Rst[:,:,4,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,4,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)])
    aux_Rst[:,:,4,:]= aux_Smpl[:,:,4,:]


    #%%ADC5
    #startFrom=0
    #aux_Rst[:,:,5,0:(quarter)]= numpy.copy(aux_Smpl[:,:,5,(startFrom):(startFrom+quarter)])
    #aux_Rst[:,:,5,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,5,(startFrom+quarter):(startFrom+quarter+quarter)])  
    #aux_Rst[:,:,5,(quarter+quarter):(quarter+quarter+quarter)]= numpy.copy(aux_Smpl[:,:,5,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) 
    #aux_Rst[:,:,5,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,5,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)])
    aux_Rst[:,:,5,:]= aux_Smpl[:,:,5,:]


    
    #%%ADC6
    startFrom=0
    aux_Rst[:,:,6,0:(quarter)]= numpy.copy(aux_Smpl[:,:,6,(startFrom+quarter+quarter+quarter):(startFrom+quarter+quarter+quarter+quarter)]) # 0 <=3
    aux_Rst[:,:,6,(quarter):(quarter+quarter)]= numpy.copy(aux_Smpl[:,:,6,(startFrom):(startFrom+quarter)]) # 1<=0
    aux_Rst[:,:,6,(quarter+quarter):(quarter+quarter+quarter)]=  numpy.copy(aux_Smpl[:,:,6,(startFrom+quarter):(startFrom+quarter+quarter)]) #  2<=1
    aux_Rst[:,:,6,(1408-quarter):(1408)]= numpy.copy(aux_Smpl[:,:,6,(startFrom+quarter+quarter):(startFrom+quarter+quarter+quarter)]) # 3<=2
        
    scrmblRst= numpy.copy( aux_Rst.reshape((NImg,212*7,44*32)) )
    del aux_Smpl; del aux_Rst
    '''     
    
    
    
    
    #
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
#%% parameters
dflt_mainFolder='/home/prcvlusr/PercAuxiliaryTools/temp_data/' 
#dflt_mainFolder='/home/io/Desktop/PERCIVAL/PercPython/auxil/SerFri_2020.04.09/'
if dflt_mainFolder[-1]!='/': dflt_mainFolder+='/'
dflt_suffix_fl0='001.h5'
dflt_suffix_fl1='002.h5'
dflt_img2proc_str= ":" # using the sensible matlab convention; "all",":","*" means all
#
################################################################################################################
dflt_swapSmplRstFlag= True; dflt_swapSmplRstFlag= False
################################################################################################################
#
dflt_seqModFlag= False # this actually mean: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
dflt_refColH1_0_Flag = False # True if refcol data are streamed out as H1<0> data.
dflt_cleanMemFlag= True # this actually mean: save descrambled image (DLSraw standard)
dflt_verboseFlag= True
#
dflt_ADCcorrFlag=False
ADCcorrFolder= 'xxx'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
dflt_ADUcorr_file= ADCcorrFolder+'xxx'
#
dflt_pedSubtractFlag=False
dflt_pedestal_CDSavg= 'xxx'
#
dflt_cols2CMA_str= "32:63"
#
dflt_saveFlag= False
dflt_outFolder='xxx'
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
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
    GUIwin_arguments+= ['refCol in H1<0>? [Y/N]'];         GUIwin_arguments+= [str(dflt_refColH1_0_Flag)]

    GUIwin_arguments+= ['ADC correction? [Y/N]'];          GUIwin_arguments+= [str(dflt_ADCcorrFlag)]
    GUIwin_arguments+= ['ADCcor (path and) file'];         GUIwin_arguments+= [dflt_ADUcorr_file]

    GUIwin_arguments+= ['pedestal-subtract? [Y/N]'];       GUIwin_arguments+= [str(dflt_pedSubtractFlag)]
    GUIwin_arguments+= ['if pedestal: pedestal CDS-avg'];  GUIwin_arguments+= [dflt_pedestal_CDSavg]  

    GUIwin_arguments+= ['RefCols for CMA [first:last]'];   GUIwin_arguments+= [dflt_cols2CMA_str]

    GUIwin_arguments+= ['save descrambled? [Y/N]'];        GUIwin_arguments+= [str(dflt_saveFlag)]
    GUIwin_arguments+= ['if save: infolder'];              GUIwin_arguments+= [str(dflt_outFolder)]

    GUIwin_arguments+= ['clean mem when possible [Y/N]'];  GUIwin_arguments+= [str(dflt_cleanMemFlag)]
    GUIwin_arguments+= ['verbose? [Y/N]'];                 GUIwin_arguments+= [str(dflt_verboseFlag)]
    #
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    mainFolder= dataFromUser[i_param]; i_param+=1
    if mainFolder[-1] != '/': mainFolder+='/'
    suffix_fl0= dataFromUser[i_param]; i_param+=1
    suffix_fl1= dataFromUser[i_param]; i_param+=1
    img2proc_str= dataFromUser[i_param]; i_param+=1
    #
    swapSmplRstFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    seqModFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    refColH1_0_Flag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #
    ADCcorrFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    ADUcorr_file= dataFromUser[i_param]; i_param+=1
    #
    pedSubtractFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    pedestalCDSFile= dataFromUser[i_param]; i_param+=1
    #
    if ADCcorrFlag:
        cols2CMA = APy3_GENfuns.matlabLike_range(dataFromUser[i_param]); i_param+=1
    #
    saveFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    outFolder= dataFromUser[i_param]; i_param+=1
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
    refColH1_0_Flag= dflt_refColH1_0_Flag
    cleanMemFlag= dflt_cleanMemFlag
    verboseFlag= dflt_verboseFlag
    #
    ADCcorrFlag= dflt_ADCcorrFlag
    ADUcorr_file= dflt_ADUcorr_file
    #
    pedSubtractFlag= dflt_pedSubtractFlag
    pedestalCDSFile= dflt_pedestal_CDSavg
    #
    cols2CMA= APy3_GENfuns.matlabLike_range(dflt_cols2CMA_str)
    #
    saveFlag= dflt_saveFlag
    outFolder= dflt_outFolder
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
data_GnCrsFn= NOTdescrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH1_0_Flag, 
                   cleanMemFlag, verboseFlag)
#
if ADCcorrFlag:
    if verboseFlag: APy3_GENfuns.printcol("ADC-correction", 'blue')
    (ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
     ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
    #
    data_ADCcorr= ADCcorr_local(data_GnCrsFn,
                                ADCfile_Smpl_crs_slope,ADCfile_Smpl_crs_offset,ADCfile_Smpl_fn_slope,ADCfile_Smpl_fn_offset,
                                ADCfile_Rst_crs_slope, ADCfile_Rst_crs_offset, ADCfile_Rst_fn_slope, ADCfile_Rst_fn_offset)
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
APy3_P2Mfuns.percDebug_plot_interactive_wCMA(data_GnCrsFn,
                                data_CDSavg,
                                data_CDSCMAavg,
                                True #False #manyImgFlag
                                )
