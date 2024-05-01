# -*- coding: utf-8 -*-
"""
ADCcor (8 files) => 1 file (reset/sample  coarse/fine offset/slope)

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_ADCcorr_03_fileGrouper.py
or:
python3
exec(open("./P2M_ADCcorr_03_fileGrouper.py").read())

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

def read_warn_1xh5(fileNamePath):
    if APy3_GENfuns.notFound(fileNamePath): APy3_GENfuns.printErr(fileNamePath+' not found')
    out_data= APy3_GENfuns.read_1xh5(fileNamePath, '/data/data')
    return out_data



def write_ADCcor_h5(fileNamePath,
                    ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                    ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset
                    ):
    #outh5PathList=[]
    #outh5PathList+=['sample/coarse/slope/']
    #outh5PathList+=['sample/coarse/offset/']
    #outh5PathList+=['sample/fine/slope/']
    #outh5PathList+=['sample/fine/offset/']
    #outh5PathList+=['reset/coarse/slope/']
    #outh5PathList+=['reset/coarse/offset/']
    #outh5PathList+=['reset/fine/slope/']
    #outh5PathList+=['reset/fine/offset/']
    my5hfile= h5py.File(fileNamePath, 'w')
    my5hfile.create_dataset('sample/coarse/slope/',  data=ADCparam_Smpl_crs_slope) #
    my5hfile.create_dataset('sample/coarse/offset/', data=ADCparam_Smpl_crs_offset) #
    my5hfile.create_dataset('sample/fine/slope/',   data=ADCparam_Smpl_fn_slope) #
    my5hfile.create_dataset('sample/fine/offset/',  data=ADCparam_Smpl_fn_offset) #
    my5hfile.create_dataset('reset/coarse/slope/',   data=ADCparam_Rst_crs_slope) #
    my5hfile.create_dataset('reset/coarse/offset/',  data=ADCparam_Rst_crs_offset) #
    my5hfile.create_dataset('reset/fine/slope/',    data=ADCparam_Rst_fn_slope) #
    my5hfile.create_dataset('reset/fine/offset/',   data=ADCparam_Rst_fn_offset) #
    my5hfile.close()

def read_ADCcor_h5(fileNamePath):
    #outh5PathList=[]
    #outh5PathList+=['sample/corse/slope/']
    #outh5PathList+=['sample/corse/offset/']
    #outh5PathList+=['sample/fine/slope/']
    #outh5PathList+=['sample/fine/offset/']
    #outh5PathList+=['reset/corse/slope/']
    #outh5PathList+=['reset/corse/offset/']
    #outh5PathList+=['reset/fine/slope/']
    #outh5PathList+=['reset/fine/offset/']
    #
    my5hfile= h5py.File(fileNamePath, 'r')
    myh5dataset=my5hfile['sample/coarse/slope/'];  ADCparam_Smpl_crs_slope= numpy.array(myh5dataset)
    myh5dataset=my5hfile['sample/coarse/offset/']; ADCparam_Smpl_crs_offset= numpy.array(myh5dataset)
    myh5dataset=my5hfile['sample/fine/slope/'];   ADCparam_Smpl_fn_slope= numpy.array(myh5dataset)
    myh5dataset=my5hfile['sample/fine/offset/'];  ADCparam_Smpl_fn_offset= numpy.array(myh5dataset)
    myh5dataset=my5hfile['reset/coarse/slope/'];   ADCparam_Rst_crs_slope= numpy.array(myh5dataset)
    myh5dataset=my5hfile['reset/coarse/offset/'];  ADCparam_Rst_crs_offset= numpy.array(myh5dataset)
    myh5dataset=my5hfile['reset/fine/slope/'];    ADCparam_Rst_fn_slope= numpy.array(myh5dataset)
    myh5dataset=my5hfile['reset/fine/offset/'];   ADCparam_Rst_fn_offset= numpy.array(myh5dataset)
    my5hfile.close()
    return (ADCparam_Smpl_crs_slope,
            ADCparam_Smpl_crs_offset, 
            ADCparam_Smpl_fn_slope,
            ADCparam_Smpl_fn_offset,
            ADCparam_Rst_crs_slope,
            ADCparam_Rst_crs_offset,
            ADCparam_Rst_fn_slope,
            ADCparam_Rst_fn_offset
            )

def blockShow(): 
    matplotlib.pyplot.show(block=True)
    return

# ---
#
#%% start
APy3_GENfuns.clean()
APy3_GENfuns.printcol("--------------",'blue')
timeId= APy3_GENfuns.whatTimeIsIt()
APy3_GENfuns.printcol("script beginning at "+timeId,'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
'''
################################ FSI01_Tm20_dmuxSELsw ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190613_000_FSI01_Tm20_ADCcorrection/processed/2019.06.13_FSI01_ADCsweep_dmuxSELsw/ADCcorParam/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'FSI01_Tminus20_dmuxSELsw_2019.06.13_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
'''
#
'''
################################ FSI01_Tm20_dmuxSELHigh ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190613_000_FSI01_Tm20_ADCcorrection/processed/2019.06.15_FSI01_ADCsweep_dmuxSELHigh/ADCcorParam/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'FSI01_Tminus20_dmuxSELHigh_2019.06.15_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
'''
#
'''
################################ BSI02_Tm20_dmuxSELsw_ADCcor ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELsw/BSI02_Tm20_dmuxSELsw_ADCcor/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'BSI02_Tminus20_dmuxSELsw_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
'''
#
'''
################################ BSI02_Tm20_dmuxSELHigh_ADCcor ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_ADCcor/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'BSI02_Tminus20_dmuxSELHigh_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
'''
#
#
#'''
################################ BSI04Tm20_dmuxSELsw ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/v2_biasBSI04_02/BSI04_Tm20_dmuxSELsw_ADCramps/ADCParam_FLastScripts/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'BSI04_Tminus20_dmuxSELsw_2019.11.20_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
#'''
#
#
'''
################################ BSI04Tm20_dmuxSELHi ######################################################
ADCcorrFolder= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/BSI04_Tm20_dmuxSELHi_ADCramps/ADCParam_FLastScripts/'
if ADCcorrFolder[-1]!='/': ADCcorrFolder+='/'
ADCcorFileList=[]
aux_ADCcorFilePrefix= 'BSI04_Tminus20_dmuxSELHi_2019.11.18_'
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Smpl_fn_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_slope.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_crs_offset.h5']
ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_slope.h5']

ADCcorFileList+=[aux_ADCcorFilePrefix+'Rst_fn_offset.h5']
ADCfile_Smpl_crs_slope= ADCcorrFolder+ADCcorFileList[0]
ADCfile_Smpl_crs_offset= ADCcorrFolder+ADCcorFileList[1]
ADCfile_Smpl_fn_slope= ADCcorrFolder+ADCcorFileList[2]
ADCfile_Smpl_fn_offset= ADCcorrFolder+ADCcorFileList[3]
ADCfile_Rst_crs_slope= ADCcorrFolder+ADCcorFileList[4]
ADCfile_Rst_crs_offset= ADCcorrFolder+ADCcorFileList[5]
ADCfile_Rst_fn_slope= ADCcorrFolder+ADCcorFileList[6]
ADCfile_Rst_fn_offset= ADCcorrFolder+ADCcorFileList[7]
out_FileNamePath= ADCcorrFolder+aux_ADCcorFilePrefix+'ADCcor.h5'
'''
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will process ADCcor from:','blue')
APy3_GENfuns.printcol(' ADCfile_Smpl_crs_slope: {0}'.format(ADCfile_Smpl_crs_slope),'blue')
APy3_GENfuns.printcol(' ADCfile_Smpl_crs_offset: {0}'.format(ADCfile_Smpl_crs_offset),'blue')
APy3_GENfuns.printcol(' ADCfile_Smpl_fn_slope: {0}'.format(ADCfile_Smpl_fn_slope),'blue')
APy3_GENfuns.printcol(' ADCfile_Smpl_fn_offset: {0}'.format(ADCfile_Smpl_fn_offset),'blue')
APy3_GENfuns.printcol(' ADCfile_Rst_crs_slope: {0}'.format(ADCfile_Rst_crs_slope),'blue')
APy3_GENfuns.printcol(' ADCfile_Rst_crs_offset: {0}'.format(ADCfile_Rst_crs_offset),'blue')
APy3_GENfuns.printcol(' ADCfile_Rst_fn_slope: {0}'.format(ADCfile_Rst_fn_slope),'blue')
APy3_GENfuns.printcol(' ADCfile_Rst_fn_offset: {0}'.format(ADCfile_Rst_fn_offset),'blue')
APy3_GENfuns.printcol('save to {0}'.format(out_FileNamePath),'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
#
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
# ---
#
   
#%% ADCcor files 
ADCparam_Smpl_crs_slope= read_warn_1xh5(ADCfile_Smpl_crs_slope)
ADCparam_Smpl_crs_offset= read_warn_1xh5(ADCfile_Smpl_crs_offset)
ADCparam_Smpl_fn_slope= read_warn_1xh5(ADCfile_Smpl_fn_slope)
ADCparam_Smpl_fn_offset= read_warn_1xh5(ADCfile_Smpl_fn_offset)
ADCparam_Rst_crs_slope= read_warn_1xh5(ADCfile_Rst_crs_slope)
ADCparam_Rst_crs_offset= read_warn_1xh5(ADCfile_Rst_crs_offset)
ADCparam_Rst_fn_slope= read_warn_1xh5(ADCfile_Rst_fn_slope)
ADCparam_Rst_fn_offset= read_warn_1xh5(ADCfile_Rst_fn_offset)
#
#%% 8 => 1 file
write_ADCcor_h5(out_FileNamePath,
                    ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                    ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset
                    )
APy3_GENfuns.printcol('save to {0}'.format(out_FileNamePath),'green')
# ---
#

# test if needed
(reread_Smpl_crs_slope,reread_Smpl_crs_offset, reread_Smpl_fn_slope,reread_Smpl_fn_offset,
reread_Rst_crs_slope,reread_Rst_crs_offset,reread_Rst_fn_slope,reread_Rst_fn_offset)= read_ADCcor_h5(out_FileNamePath)
#
APy3_GENfuns.plot_2D_all(ADCparam_Smpl_crs_slope, False, 'col','row','orig Smpl_crs_slope', True)
APy3_GENfuns.plot_2D_all(  reread_Smpl_crs_slope, False, 'col','row','orig Smpl_crs_slope', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Smpl_crs_offset, False, 'col','row','orig Smpl_crs_offset', True)
APy3_GENfuns.plot_2D_all(  reread_Smpl_crs_offset, False, 'col','row','orig Smpl_crs_offset', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Smpl_fn_slope, False, 'col','row','orig Smpl_fn_slope', True)
APy3_GENfuns.plot_2D_all(  reread_Smpl_fn_slope, False, 'col','row','orig Smpl_fn_slope', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Smpl_fn_offset, False, 'col','row','orig Smpl_fn_offset', True)
APy3_GENfuns.plot_2D_all(  reread_Smpl_fn_offset, False, 'col','row','orig Smpl_fn_offset', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Rst_crs_slope, False, 'col','row','orig Rst_crs_slope', True)
APy3_GENfuns.plot_2D_all(  reread_Rst_crs_slope, False, 'col','row','orig Rst_crs_slope', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Rst_crs_offset, False, 'col','row','orig Rst_crs_offset', True)
APy3_GENfuns.plot_2D_all(  reread_Rst_crs_offset, False, 'col','row','orig Rst_crs_offset', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Rst_fn_slope, False, 'col','row','orig Rst_fn_slope', True)
APy3_GENfuns.plot_2D_all(  reread_Rst_fn_slope, False, 'col','row','orig Rst_fn_slope', True)
blockShow()
#
APy3_GENfuns.plot_2D_all(ADCparam_Rst_fn_offset, False, 'col','row','orig Rst_fn_offset', True)
APy3_GENfuns.plot_2D_all(  reread_Rst_fn_offset, False, 'col','row','orig Rst_fn_offset', True)
blockShow()
#
# ---
#
APy3_GENfuns.printcol("end", 'blue')

