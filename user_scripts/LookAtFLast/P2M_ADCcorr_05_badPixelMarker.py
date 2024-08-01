# -*- coding: utf-8 -*-
"""
ADCcor files + sample image => interactive judge bad pixels, set as nan in  ADCcor

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_ADCcorr_05_badPixelMarker.py
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
#
def plot_2x2D(array1,array2, logScaleFlag, label_x,label_y, label_title1,label_title2, invertx_flag):
    ''' 2x2D image''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    #
    matplotlib.pyplot.subplot(1,2,1)
    if logScaleFlag: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(1,2,2)
    if logScaleFlag: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    matplotlib.pyplot.show(block=False)
    return (fig)

def plot_4x2D(array1,array2,array3,array4, logScaleFlag, label_x,label_y, label_title1,label_title2,label_title3,label_title4, invertx_flag):
    ''' 2x2D image''' 
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    #
    matplotlib.pyplot.subplot(2,2,1)
    if logScaleFlag: matplotlib.pyplot.imshow(array1, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array1, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title1)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(2,2,2)
    if logScaleFlag: matplotlib.pyplot.imshow(array2, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title2)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(2,2,3)
    if logScaleFlag: matplotlib.pyplot.imshow(array3, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array3, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title3)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.subplot(2,2,4)
    if logScaleFlag: matplotlib.pyplot.imshow(array4, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array4, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title4)    
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis(); 
    #
    matplotlib.pyplot.show(block=False)
    return (fig)

def write_8xh5(filenamepath, 
               data1,path1, data2,path2, data3,path3, data4,path4,
               data5,path5, data6,path6, data7,path7, data8,path8):
    ''' write 8xXD h5 file (paths_2write: '/sample/coarse/slope/','/sample/coarse/offset/',... ) '''
    my5hfile= h5py.File(filenamepath, 'w')
    my5hfile.create_dataset(path1, data=data1)
    my5hfile.create_dataset(path2, data=data2)
    my5hfile.create_dataset(path3, data=data3)
    my5hfile.create_dataset(path4, data=data4)
    my5hfile.create_dataset(path5, data=data5)
    my5hfile.create_dataset(path6, data=data6)
    my5hfile.create_dataset(path7, data=data7)
    my5hfile.create_dataset(path8, data=data8)
    my5hfile.close()

# ---
#
#%% defaults for GUI window
'''
dflt_ADCcor_1file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELsw/' + 'BSI02_Tm20_dmuxSELsw_H0,H1_ADCcor/BSI02_Tminus20_dmuxSELsw_2019.09.04_ADCcor.h5'
dflt_DLSraw_infile=  '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190904_001_BSI02_Tm20_ADCcorrection/processed/2019.09.04_BSI02_ADCsweep_dmuxSELsw/DLSraw/' + 'fn-scan_Vin=20000_DLSraw.h5'
dflt_thisImg= '5'
'''
#
#'''
#dflt_ADCcor_1file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/v2_biasBSI04_02/BSI04_Tm20_dmuxSELsw_ADCramps/ADCParam_FLastScripts/BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
dflt_ADCcor_1file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
dflt_DLSraw_infile=  '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/v2_biasBSI04_02/BSI04_Tm20_dmuxSELsw_ADCramps/DLSraw/' + '2019.11.20_BSI04_Tm20_dmuxSELsw_BSI04_02_VRST_PGABBB_VRSTfromVin20000_10adc_fnramp_DLSraw.h5'
dflt_thisImg= '5'
#'''


# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['ADCcor_1file'] 
GUIwin_arguments+= [dflt_ADCcor_1file] 
#
GUIwin_arguments+= ['DLSraw_infile'] 
GUIwin_arguments+= [dflt_DLSraw_infile] 
GUIwin_arguments+= ['look at image'] 
GUIwin_arguments+= [dflt_thisImg] 
#
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
ADCcor_1file= dataFromUser[i_param]; i_param+=1
DLSraw_infile= dataFromUser[i_param]; i_param+=1
thisImg= int(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will use ADCcor from'+ADCcor_1file,'blue')
if APy3_GENfuns.notFound(ADCcor_1file): APy3_GENfuns.printErr('not found: '+ADCcor_1file)
APy3_GENfuns.printcol('will use image {0} from DLSraw file {1}'.format(thisImg,DLSraw_infile),'blue')
if APy3_GENfuns.notFound(DLSraw_infile): APy3_GENfuns.printErr('not found: '+DLSraw_infile)
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#% read data files
(dataSmpl_in,dataRst_in)= APy3_GENfuns.read_partial_2xh5(DLSraw_infile, '/data','/reset', thisImg, thisImg+1)

dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(dataSmpl_in,dataRst_in, ERRDLSraw,ERRint16)

(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, 
ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_1file)


data_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                      ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol) # Smpl only is correct
data_ADCcorr[:,iRst,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                                  ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset, NRow,NCol) # Rst
#
changed_Smpl_crs_slope=  numpy.copy(ADCparam_Smpl_crs_slope)
changed_Smpl_crs_offset= numpy.copy(ADCparam_Smpl_crs_offset)
changed_Smpl_fn_slope=   numpy.copy(ADCparam_Smpl_fn_slope)
changed_Smpl_fn_offset=  numpy.copy(ADCparam_Smpl_fn_offset)
changed_Rst_crs_slope=   numpy.copy(ADCparam_Rst_crs_slope)
changed_Rst_crs_offset=  numpy.copy(ADCparam_Rst_crs_offset)
changed_Rst_fn_slope=    numpy.copy(ADCparam_Rst_fn_slope)
changed_Rst_fn_offset=   numpy.copy(ADCparam_Rst_fn_offset)
#
APy3_GENfuns.printcol("show [O]riginal/[C]hanged data / find [M]in-max / mark [B]ad pixel ROI / save to [F]ile / [E]nd", 'black')
nextstep = input()
#
logScaleFlag=False; invertx_flag=True
label_x='col'; label_y='row'
while nextstep not in ['e','E','q','Q']:
    matplotlib.pyplot.close()
    #
    if nextstep in ['o','O']: 
        APy3_GENfuns.printcol("showing image processed with original values, close image to move on", 'black')
        plot_2x2D(data_ADCcorr[0,iSmpl,:,:],data_ADCcorr[0,iRst,:,:], False, 'col','row', 'original Smpl [ADU]','original Rst [ADU]', True)
        APy3_GENfuns.plot_2D_all(data_ADCcorr[0,iSmpl,:,:]-data_ADCcorr[0,iRst,:,:], False, 'col','row', 'original not-C DS [ADU]', True)
        #
        plot_4x2D(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'orig ADCparam_Smpl_crs_slope','orig ADCparam_Smpl_crs_offset','orig ADCparam_Smpl_fn_slope','orig ADCparam_Smpl_fn_offset',
                  invertx_flag)
        plot_4x2D(ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'orig ADCparam_Rst_crs_slope','orig ADCparam_Rst_crs_offset','orig ADCparam_Rst_fn_slope','orig ADCparam_Rst_fn_offset',
                  invertx_flag)
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['c','C']: 
        APy3_GENfuns.printcol("showing image processed with changed values, close image to move on", 'black')
        changed_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                      changed_Smpl_crs_slope,changed_Smpl_crs_offset,changed_Smpl_fn_slope,changed_Smpl_fn_offset, NRow,NCol) # Smpl only is correct
        changed_ADCcorr[:,iRst,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                      changed_Rst_crs_slope, changed_Rst_crs_offset, changed_Rst_fn_slope, changed_Rst_fn_offset,  NRow,NCol) # Rst
        plot_2x2D(changed_ADCcorr[0,iSmpl,:,:],changed_ADCcorr[0,iRst,:,:], False, 'col','row', 'changed Smpl [ADU]','changed Rst [ADU]', True)
        APy3_GENfuns.plot_2D_all(changed_ADCcorr[0,iSmpl,:,:]-changed_ADCcorr[0,iRst,:,:], False, 'col','row', 'changed not-C, but DS [ADU]', True)
        #
        plot_4x2D(changed_Smpl_crs_slope,changed_Smpl_crs_offset,changed_Smpl_fn_slope,changed_Smpl_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'changed ADCparam_Smpl_crs_slope','changed ADCparam_Smpl_crs_offset','changed ADCparam_Smpl_fn_slope','changed ADCparam_Smpl_fn_offset',
                  invertx_flag)
        plot_4x2D(changed_Rst_crs_slope, changed_Rst_crs_offset, changed_Rst_fn_slope, changed_Rst_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'changed ADCparam_Rst_crs_slope','changed ADCparam_Rst_crs_offset','changed ADCparam_Rst_fn_slope','changed ADCparam_Rst_fn_offset',
                  invertx_flag)
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    elif nextstep in ['b','B']: 
        APy3_GENfuns.printcol("bad pixel ROI: rows [first:last]", 'black')
        Rows2proc_mtlb = input()
        if Rows2proc_mtlb in ['all','All','ALL',':','*','-1']: Rows2proc= numpy.arange(NRow)
        else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 
        fromRow= Rows2proc[0]; toRowp1= Rows2proc[-1]+1
        #
        APy3_GENfuns.printcol("bad pixel ROI: cols [first:last]", 'black')
        Cols2proc_mtlb = input()
        if Cols2proc_mtlb in ['all','All','ALL',':','*','-1']: Cols2proc= numpy.arange(NCol)
        else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
        fromCol= Cols2proc[0]; toColp1= Cols2proc[-1]+1
        #
        changed_Smpl_crs_slope[fromRow:toRowp1,fromCol:toColp1]=  numpy.NaN
        changed_Smpl_crs_offset[fromRow:toRowp1,fromCol:toColp1]= numpy.NaN
        changed_Smpl_fn_slope[fromRow:toRowp1,fromCol:toColp1]=   numpy.NaN
        changed_Smpl_fn_offset[fromRow:toRowp1,fromCol:toColp1]=  numpy.NaN
        changed_Rst_crs_slope[fromRow:toRowp1,fromCol:toColp1]=  numpy.NaN
        changed_Rst_crs_offset[fromRow:toRowp1,fromCol:toColp1]= numpy.NaN
        changed_Rst_fn_slope[fromRow:toRowp1,fromCol:toColp1]=   numpy.NaN
        changed_Rst_fn_offset[fromRow:toRowp1,fromCol:toColp1]=  numpy.NaN
        #
        plot_4x2D(changed_Smpl_crs_slope,changed_Smpl_crs_offset,changed_Smpl_fn_slope,changed_Smpl_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'changed ADCparam_Smpl_crs_slope','changed ADCparam_Smpl_crs_offset','changed ADCparam_Smpl_fn_slope','changed ADCparam_Smpl_fn_offset',
                  invertx_flag)
        plot_4x2D(changed_Rst_crs_slope, changed_Rst_crs_offset, changed_Rst_fn_slope, changed_Rst_fn_offset, 
                  logScaleFlag, label_x,label_y, 
                  'changed ADCparam_Rst_crs_slope','changed ADCparam_Rst_crs_offset','changed ADCparam_Rst_fn_slope','changed ADCparam_Rst_fn_offset',
                  invertx_flag)
        #
        changed_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                      changed_Smpl_crs_slope,changed_Smpl_crs_offset,changed_Smpl_fn_slope,changed_Smpl_fn_offset, NRow,NCol) # Smpl only is correct
        changed_ADCcorr[:,iRst,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                      changed_Rst_crs_slope, changed_Rst_crs_offset, changed_Rst_fn_slope, changed_Rst_fn_offset,  NRow,NCol) # Rst
        plot_2x2D(changed_ADCcorr[0,iSmpl,:,:],changed_ADCcorr[0,iRst,:,:], False, 'col','row', 'changed Smpl [ADU]','changed Rst [ADU]', True)
        #
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    elif nextstep in ['m','M']:
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Smpl_crs_slope, axis=None), changed_Smpl_crs_slope.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Smpl_crs_slope, axis=None), changed_Smpl_crs_slope.shape)
        APy3_GENfuns.printcol("Smpl_crs_slope: min={0} in pix {1}; max={2} in pix {3}".format(changed_Smpl_crs_slope[auxmin_index],auxmin_index,
                                                                                              changed_Smpl_crs_slope[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Rst_crs_slope, axis=None), changed_Rst_crs_slope.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Rst_crs_slope, axis=None), changed_Rst_crs_slope.shape)
        APy3_GENfuns.printcol("Rst_crs_slope: min={0} in pix {1}; max={2} in pix {3}".format(changed_Rst_crs_slope[auxmin_index],auxmin_index,
                                                                                             changed_Rst_crs_slope[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Smpl_crs_offset, axis=None), changed_Smpl_crs_offset.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Smpl_crs_offset, axis=None), changed_Smpl_crs_offset.shape)
        APy3_GENfuns.printcol("Smpl_crs_offset: min={0} in pix {1}; max={2} in pix {3}".format(changed_Smpl_crs_offset[auxmin_index],auxmin_index,
                                                                                              changed_Smpl_crs_offset[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Rst_crs_offset, axis=None), changed_Rst_crs_offset.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Rst_crs_offset, axis=None), changed_Rst_crs_offset.shape)
        APy3_GENfuns.printcol("Rst_crs_offset: min={0} in pix {1}; max={2} in pix {3}".format(changed_Rst_crs_offset[auxmin_index],auxmin_index,
                                                                                             changed_Rst_crs_offset[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Smpl_fn_slope, axis=None), changed_Smpl_fn_slope.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Smpl_fn_slope, axis=None), changed_Smpl_fn_slope.shape)
        APy3_GENfuns.printcol("Smpl_fn_slope: min={0} in pix {1}; max={2} in pix {3}".format(changed_Smpl_fn_slope[auxmin_index],auxmin_index,
                                                                                              changed_Smpl_fn_slope[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Rst_fn_slope, axis=None), changed_Rst_fn_slope.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Rst_fn_slope, axis=None), changed_Rst_fn_slope.shape)
        APy3_GENfuns.printcol("Rst_crs_slope: min={0} in pix {1}; max={2} in pix {3}".format(changed_Rst_fn_slope[auxmin_index],auxmin_index,
                                                                                             changed_Rst_fn_slope[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Smpl_fn_offset, axis=None), changed_Smpl_fn_offset.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Smpl_fn_offset, axis=None), changed_Smpl_fn_offset.shape)
        APy3_GENfuns.printcol("Smpl_fn_offset: min={0} in pix {1}; max={2} in pix {3}".format(changed_Smpl_fn_offset[auxmin_index],auxmin_index,
                                                                                              changed_Smpl_fn_offset[auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_Rst_fn_offset, axis=None), changed_Rst_fn_offset.shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_Rst_fn_offset, axis=None), changed_Rst_fn_offset.shape)
        APy3_GENfuns.printcol("Rst_fn_offset: min={0} in pix {1}; max={2} in pix {3}".format(changed_Rst_fn_offset[auxmin_index],auxmin_index,
                                                                                             changed_Rst_fn_offset[auxmax_index],auxmax_index), 'green')
        #
        changed_ADCcorr= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,:,:,:,iCrs],dscrmbld_GnCrsFn[:,:,:,:,iFn],
                                      changed_Smpl_crs_slope,changed_Smpl_crs_offset,changed_Smpl_fn_slope,changed_Smpl_fn_offset, NRow,NCol) # Smpl only is correct
        changed_ADCcorr[:,iRst,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(dscrmbld_GnCrsFn[:,iRst,:,:,iCrs],dscrmbld_GnCrsFn[:,iRst,:,:,iFn],
                                      changed_Rst_crs_slope, changed_Rst_crs_offset, changed_Rst_fn_slope, changed_Rst_fn_offset,  NRow,NCol) # Rst
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_ADCcorr[0,iSmpl,:,:], axis=None), changed_ADCcorr[0,iSmpl,:,:].shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_ADCcorr[0,iSmpl,:,:], axis=None), changed_ADCcorr[0,iSmpl,:,:].shape)
        APy3_GENfuns.printcol("Smpl [ADU]: min={0} in pix {1}; max={2} in pix {3}".format(changed_ADCcorr[0,iSmpl,:,:][auxmin_index],auxmin_index,
                                                                                          changed_ADCcorr[0,iSmpl,:,:][auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_ADCcorr[0,iRst,:,:], axis=None), changed_ADCcorr[0,iRst,:,:].shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_ADCcorr[0,iRst,:,:], axis=None), changed_ADCcorr[0,iRst,:,:].shape)
        APy3_GENfuns.printcol("Rst [ADU]: min={0} in pix {1}; max={2} in pix {3}".format(changed_ADCcorr[0,iRst,:,:][auxmin_index],auxmin_index,
                                                                                          changed_ADCcorr[0,iRst,:,:][auxmax_index],auxmax_index), 'green')
        auxmax_index= numpy.unravel_index(numpy.nanargmax(changed_ADCcorr[0,iSmpl,:,:]-changed_ADCcorr[0,iRst,:,:], axis=None), changed_ADCcorr[0,iRst,:,:].shape) 
        auxmin_index= numpy.unravel_index(numpy.nanargmin(changed_ADCcorr[0,iSmpl,:,:]-changed_ADCcorr[0,iRst,:,:], axis=None), changed_ADCcorr[0,iRst,:,:].shape)
        APy3_GENfuns.printcol("non-C, but DS [ADU]: min={0} in pix {1}; max={2} in pix {3}".format(changed_ADCcorr[0,iSmpl,:,:][auxmin_index]-changed_ADCcorr[0,iRst,:,:][auxmin_index],
                                                                                                   auxmin_index,
                                                                                                   changed_ADCcorr[0,iSmpl,:,:][auxmax_index]-changed_ADCcorr[0,iRst,:,:][auxmax_index],
                                                                                                   auxmax_index), 'green')
        #
    elif nextstep in ['f','F']: 
        out_ADCcor_1file= ADCcor_1file+'_changed.h5'
        write_8xh5(out_ADCcor_1file, 
                   changed_Smpl_crs_slope, '/sample/coarse/slope/',
                   changed_Smpl_crs_offset,'/sample/coarse/offset/',
                   changed_Smpl_fn_slope,  '/sample/fine/slope/',
                   changed_Smpl_fn_offset, '/sample/fine/offset/',
                   changed_Rst_crs_slope,  '/reset/coarse/slope/',
                   changed_Rst_crs_offset, '/reset/coarse/offset/',
                   changed_Rst_fn_slope,   '/reset/fine/slope/',
                   changed_Rst_fn_offset,  '/reset/fine/offset/')
        APy3_GENfuns.printcol("ADC file changed as "+out_ADCcor_1file, 'black')
    # ...
    #
    APy3_GENfuns.printcol("show [O]riginal/[C]hanged data / find [M]in-max / mark [B]ad pixel ROI / save to [F]ile / [E]nd", 'black')
    nextstep = input()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end", 'blue')

# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




