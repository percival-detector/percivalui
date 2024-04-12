# -*- coding: utf-8 -*-
"""
# this file: descramble, GnCrsFn,  ADUcorr, CDS/CMA Gn0 if needed, LatOvflw to electron, 
save to file : e; GnCrsFn

load environment on cfeld-perc02 is:
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root

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
interactiveFlag= False; #interactiveFlag= True  # KEEP IT FALSE FOR SBATCH !!!
#
#---
#
#%% parameters
#dflt_mainFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190517_000_PTC_BSI02_Tm20_0802i_dmuxSELHigh_Gn0_PGAB/processed/v1/scrmbld/' 
dflt_mainFolder=sys.argv[1]
if dflt_mainFolder[-1]!='/': dflt_mainFolder+='/'
#
#expected_prefix_fl='2019.05.17_xx.xx.xx_BSI02_Tm20_0802i_dmuxSELHigh_Gn0_PGAB_GrndGls_ODx.x_t200_500drk_'
expected_prefix_fl=sys.argv[2]
#
#dflt_suffix_fl0= '000001.h5'
#dflt_suffix_fl1= '000002.h5'
dflt_suffix_fl0= sys.argv[3]
dflt_suffix_fl1= sys.argv[4]
#
#dflt_img2proc_str= "0:9" # using the sensible matlab convention; "all",":","*" means all
#dflt_img2proc_str= ":" 
dflt_img2proc_str= sys.argv[6]
#
dflt_swapSmplRstFlag= True
dflt_seqModFlag= False # this actually mean: SeqMod image taken with a stdMod mezzfirm, so that only hal image is relevand data
dflt_refColH1_0_Flag = False # True if refcol data are streamed out as H1<0> data.

dflt_ADCcor_file= sys.argv[7]
dflt_multiGnCal_file= sys.argv[8]
dflt_alternFile_Ped_Gn0_ADU= sys.argv[9]
#
dflt_cols2CMA_str= sys.argv[10]
dflt_CDSFlag= sys.argv[11]
#
dflt_cleanMemFlag= True
dflt_verboseFlag= False # KEEP IT FALSE FOR SBATCH !!!
#
dflt_saveFlag= True
#dflt_outFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190517_000_PTC_BSI02_Tm20_0802i_dmuxSELHigh_Gn0_PGAB/scratch/marras/'
dflt_outFolder=sys.argv[5]
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
labelImg="{0}:{1}".format( (APy3_GENfuns.matlabLike_range(dflt_img2proc_str)[0])+1,(APy3_GENfuns.matlabLike_range(dflt_img2proc_str)[-1]) ) # 1st image not in array
dflt_outFileNamePath= dflt_outFolder+expected_prefix_fl+ labelImg+'_e.h5'
dflt_outGnCrsFn_FileNamePath= dflt_outFolder+expected_prefix_fl+ labelImg+'_GnCrsFn.h5'

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
def loadSomeImagesFromFile(mainFolder, name_fl0, name_fl1,
                           img2proc_str, 
                           verboseFlag):
    """ load some images from file """
    #%% read file
    APy3_GENfuns.clean()
    if verboseFlag: APy3_GENfuns.printcol("reading files", 'blue')
    #if APy3_GENfuns.notFound(inputFiles[0]): APy3_GENfuns.printErr(inputFiles[0]+' not found')  # KEEP IT COMMENTED FOR SBATCH !!!
    #if APy3_GENfuns.notFound(inputFiles[1]): APy3_GENfuns.printErr(inputFiles[1]+' not found')  # KEEP IT COMMENTED FOR SBATCH !!!
    
    if img2proc_str in ['all','All','ALL',':','*','-1']: 
        if verboseFlag: APy3_GENfuns.printcol("will read all Img", 'green')
        (dataSmpl_fl0, dataRst_fl0) = APy3_GENfuns.read_2xh5(mainFolder+name_fl0, '/data/','/reset/')
        (dataSmpl_fl1, dataRst_fl1) = APy3_GENfuns.read_2xh5(mainFolder+name_fl1, '/data/','/reset/')
    else:
        img2proc= APy3_GENfuns.matlabLike_range(img2proc_str)
        fromImg_fl01= img2proc[0]//2
        toImg_fl01=(img2proc[-1]//2)
        if verboseFlag:
            APy3_GENfuns.printcol("will read img {0} to {1} in both files".format(fromImg_fl01,toImg_fl01), 'green')
            APy3_GENfuns.printcol("corresponding overall to img {0}".format(str(img2proc)), 'green')
        (dataSmpl_fl0, dataRst_fl0) = read_partial_2xh5(mainFolder+name_fl0, '/data/','/reset/', fromImg_fl01,toImg_fl01)
        (dataSmpl_fl1, dataRst_fl1) = read_partial_2xh5(mainFolder+name_fl1, '/data/','/reset/', fromImg_fl01,toImg_fl01)
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
    data2srcmbl_noRefCol[:,iSmpl,:,:]= (scrmblSmpl_byteSwap)
    data2srcmbl_noRefCol[:,iRst,:,:] = (scrmblRst_byteSwap)
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
    if refColH1_0_Flag:
        if verboseFlag: APy3_GENfuns.printcol("moving RefCol data to G", 'blue')
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
    GUIwin_arguments+= ['refCol in H1<0>? [Y/N]'];         GUIwin_arguments+= [str(dflt_refColH1_0_Flag)]

    GUIwin_arguments+= ['ADCcor 1-file'];                                         GUIwin_arguments+= [dflt_ADCcor_file]
    GUIwin_arguments+= ['Lateral Overflow (pedestal & e/ADU for Gn0/1/2): file']; GUIwin_arguments+= [dflt_multiGnCal_file]
    GUIwin_arguments+= ['PedestalADU [Gn0] file [none not to use it]'];           GUIwin_arguments+= [dflt_alternFile_Ped_Gn0_ADU]
    #
    GUIwin_arguments+= ['cols to use for CMA [from:to] [none not to use it]']; GUIwin_arguments+= [dflt_cols2CMA_str]
    GUIwin_arguments+= ['CDS for Gn=0? [Y/N]'];           GUIwin_arguments+= [dflt_CDSFlag]

    GUIwin_arguments+= ['save descrambled? [Y/N]'];        GUIwin_arguments+= [str(dflt_saveFlag)]
    GUIwin_arguments+= ['if save: electron file path/name']; GUIwin_arguments+= [str(dflt_outFileNamePath)]
    GUIwin_arguments+= ['if save: GnCrsFn file path/name']; GUIwin_arguments+= [str(dflt_outGnCrsFn_FileNamePath)]

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
    refColH1_0_Flag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #
    ADCcor_file=            dataFromUser[i_param]; i_param+=1
    multiGnCal_file=        dataFromUser[i_param]; i_param+=1
    alternFile_Ped_Gn0_ADU= dataFromUser[i_param]; i_param+=1
    #
    cols2CMA_str= dataFromUser[i_param]; i_param+=1
    CDSFlag=      APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
    saveFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    outFileNamePath= dataFromUser[i_param]; i_param+=1
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
    #
    ADCcor_file= dflt_ADCcor_file
    multiGnCal_file= dflt_multiGnCal_file
    alternFile_Ped_Gn0_ADU= dflt_alternFile_Ped_Gn0_ADU
    #
    cols2CMA_str= dflt_cols2CMA_str
    CDSFlag=      APy3_GENfuns.isitYes(str(dflt_CDSFlag))
    #
    cleanMemFlag= dflt_cleanMemFlag
    verboseFlag= dflt_verboseFlag
    #
    saveFlag= dflt_saveFlag
    outFileNamePath= dflt_outFileNamePath
    outGnCrsFn_FileNamePath= dflt_outGnCrsFn_FileNamePath
#---
if cols2CMA_str in APy3_GENfuns.NOlist:
    CMAFlag=False
    cols2CMA=[]
else:
    CMAFlag= True
    cols2CMA= APy3_GENfuns.matlabLike_range(cols2CMA_str)
#
if multiGnCal_file in APy3_GENfuns.NOlist: ADU2eFlag= False
else: ADU2eFlag= True
#
if alternFile_Ped_Gn0_ADU in APy3_GENfuns.NOlist: alternPed= False
else: alternPed= True
#---
#%% profile it
#import cProfile
#cProfile.run('auxdata= descrambleLast(mainFolder, ...)', sort='cumtime')
#APy3_GENfuns.printcol("scripts took {0} sec".format(aux_length),'green')
#---
#%% or just execute it
name_fl0= expected_prefix_fl+suffix_fl0
name_fl1= expected_prefix_fl+suffix_fl1
(scrmblSmpl,scrmblRst)= loadSomeImagesFromFile(mainFolder, name_fl0, name_fl1,
                           img2proc_str, 
                           verboseFlag)
#
data_GnCrsFn= descrambleSome(scrmblSmpl,scrmblRst,
                   swapSmplRstFlag,seqModFlag, refColH1_0_Flag, 
                   cleanMemFlag, verboseFlag)
#(DLSraw_Smpl,DLSraw_Rst)= convert_GnCrsFn_2_DLSraw(data_GnCrsFn, ERRint16, ERRDLSraw)
#
#---
#---
##% load ADC calibr file
#if APy3_GENfuns.notFound(ADCcor_file): APy3_GENfuns.printERR('not found '+ADCcor_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
#if verboseFlag: APy3_GENfuns.printcol("ADC calibr file loaded {0}".format(ADCcor_file),'green')
#
##% load multiGnCal file if needed
if ADU2eFlag:
    #if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
    (PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
    #if verboseFlag: APy3_GENfuns.printcol("multiGnCal file loaded {0}".format(multiGnCal_file),'green')
else:
    PedestalADU_multiGn= numpy.zeros((NGn,NRow,NCol))
    e_per_ADU_multiGn=   numpy.ones((NGn,NRow,NCol))
#
if alternPed:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn0_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn0_ADU)
    PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn0_ADU, '/data/data/')
    #if verboseFlag: APy3_GENfuns.printcol("alternative Pedestal ADU file loaded {0}".format(alternFile_Ped_Gn0_ADU),'green')
#---
#%% to e
data_e= APy3_P2Mfuns.convert_GnCrsFn_2_e_wLatOvflw(data_GnCrsFn,
                       CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       True,cleanMemFlag,verboseFlag)
#---
#%% GnCrsFs to out
(auxNImg,ignNSR,ignNCol,ignNR,ignNGCF)=  data_GnCrsFn.shape
dataout_GnCrsFn= numpy.zeros((auxNImg-1,ignNSR,ignNCol,ignNR,ignNGCF)).astype('int16') -256
dataout_GnCrsFn[:,APy3_P2Mfuns.iSmpl,:,:,:]= data_GnCrsFn[1:,APy3_P2Mfuns.iSmpl,:,:,:]
dataout_GnCrsFn[:,APy3_P2Mfuns.iRst,:,:,:]= data_GnCrsFn[:(-1),APy3_P2Mfuns.iRst,:,:,:]

#---
if saveFlag:
    #APy3_GENfuns.write_2xh5(outFileNamePath, DLSraw_Smpl, '/data/', DLSraw_Rst, '/reset/')
    APy3_GENfuns.write_1xh5(outFileNamePath, data_e, '/data/data/')
    if verboseFlag: APy3_GENfuns.printcol("e data saved to {0}".format(outFileNamePath), 'green')
    #
    APy3_GENfuns.write_1xh5(outGnCrsFn_FileNamePath, dataout_GnCrsFn, '/data/data/')
    if verboseFlag: APy3_GENfuns.printcol("GnCrsFn data saved to {0}".format(outGnCrsFn_FileNamePath), 'green')
#%% that's all folks
#---    



