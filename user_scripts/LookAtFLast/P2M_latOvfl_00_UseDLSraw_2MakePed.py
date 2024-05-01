# -*- coding: utf-8 -*-
"""
DLSraw (descrambled) => avg (CDS or Smpl) , (useful to make a pedestal)
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_00_UseDLSraw_2MakePed.py
or:
python3
exec(open("./P2M_latOvfl_00_UseDLSraw_2MakePed.py").read())
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
'''
#%% data from here
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.09_FSI01_Tm20_3G_PGAB_dmuxSELHigh_prelim/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#dflt_infile= "2019.07.09_10.00.xx_FSI01_Tm20_dmuxSELHigh_0802h_3G_Gn0_PGAB_ODx.x_t012ms_1kdrk_DLSraw.h5"
dflt_infile= "2019.07.09_10.00.xx_FSI01_Tm20_dmuxSELHigh_0802h_3T_Gn1_PGAB_ODx.x_t012ms_1kdrk_DLSraw.h5"
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
#
dflt_CDSFlag=True; dflt_CDSFlag=False
dflt_CMAFlag= False
dflt_cols2CMA = '32:63'
#
dflt_showFlag= True
#
dflt_saveAvgFlag=True # save 2D img (float): avg of ADCcorr, CDS, possibly CMA, possibly ped-Subtracted;  avg of Smpl, Rst
dflt_outFolder='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.09_FSI01_Tm20_3G_PGAB_dmuxSELHigh_prelim/pedestal_ADU/'
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
#dflt_out_avgFile=  "2019.07.09_10.00.xx_FSI01_Tm20_dmuxSELHigh_0802h_3G_Gn0_PGAB_ODx.x_t012ms_CDS_ADU_drkavg.h5"
dflt_out_avgFile=  "2019.07.09_10.00.xx_FSI01_Tm20_dmuxSELHigh_0802h_3T_Gn1_PGAB_ODx.x_t012ms_Smpl_ADU_drkavg.h5"
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
#'''
#%% data from here
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.28_FSI01_Tm20_dmuxSELHigh_0802h4_3G_PGA6BB_sweep_onlyUpTo253ms/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_infile= "2019.07.28_FSI01_Tm20_dmuxSELHigh_0802h4_Gn0_PGA6BB_ODx.x_t012ms_1kdrk_DLSraw.h5"
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
dflt_CMAFlag= False
dflt_cols2CMA = '32:63'
#
dflt_showFlag= True
#
dflt_saveAvgFlag=True # save 2D img (float): avg of ADCcorr, CDS, possibly CMA, possibly ped-Subtracted;  avg of Smpl, Rst
dflt_outFolder= dflt_folder_data2process+'../LatOvflw/'
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
dflt_out_avgFile=  "2019.07.28_FSI01_Tm20_dmuxSELHigh_0802h4_Gn0_PGA6BB_ODx.x_t012ms_CDS_ADU_drkavg.h5"
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
#'''
#---
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['DLSraw file to process'] 
GUIwin_arguments+= [dflt_infile]
#
GUIwin_arguments+= ['ADUcorr: file'] 
GUIwin_arguments+= [dflt_ADUcorr_file]
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
#
GUIwin_arguments+= ['CDS? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CDSFlag)]
GUIwin_arguments+= ['CMA? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CMAFlag)]
GUIwin_arguments+= ['if CMA: Reference Columns? [first:last]'] 
GUIwin_arguments+= [dflt_cols2CMA]
#
GUIwin_arguments+= ['show? [Y/N]'] 
GUIwin_arguments+= [str(dflt_showFlag)]
#
GUIwin_arguments+= ['save avg file? [Y/N]'] 
GUIwin_arguments+= [str(dflt_saveAvgFlag)]
GUIwin_arguments+= ['if save avg: in which folder?'] 
GUIwin_arguments+= [dflt_outFolder]
GUIwin_arguments+= ['if save avg: output filename?'] 
GUIwin_arguments+= [dflt_out_avgFile]
#
GUIwin_arguments+= ['high mem usage? [Y/N]'] 
GUIwin_arguments+= [str(dflt_highMemFlag)] 
GUIwin_arguments+= ['clean mem when possible? [Y/N]'] 
GUIwin_arguments+= [str(dflt_cleanMemFlag)]
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [str(dflt_verboseFlag)]
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
i_param=0
folder_data2process= dataFromUser[i_param]; i_param+=1
infile= dataFromUser[i_param]; i_param+=1
#
ADUcorr_file= dataFromUser[i_param]; i_param+=1;  
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1];
#
CDSFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
CMAFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cols2CMA_mtlb= dataFromUser[i_param]; i_param+=1
cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_mtlb)
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
saveAvgFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
outFolder= dataFromUser[i_param]; i_param+=1
out_avgFile= dataFromUser[i_param]; i_param+=1
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using file {0}'.format(infile),'blue')
    APy3_GENfuns.printcol('will ADU-correct using {0})'.format(ADUcorr_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate Img{0}'.format(Img2proc_mtlb),'blue')
    #
    if (CDSFlag): APy3_GENfuns.printcol('  will use CDS','blue')
    if (CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol(0)'.format(cols2CMA_mtlb),'blue')
    #
    if showFlag: APy3_GENfuns.printcol('will show avg','blue')
    #
    if saveAvgFlag: 
        APy3_GENfuns.printcol('will save to folder {0}'.format(outFolder),'blue')
        APy3_GENfuns.printcol('  as file {0}'.format(out_avgFile),'blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#%% load file
if verboseFlag: APy3_GENfuns.printcol('load DLSraw-file and ADUcorr-files','blue')
if APy3_GENfuns.notFound(ADUcorr_file): APy3_GENfuns.printErr('not found: '+ADUcorr_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
 ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
if APy3_GENfuns.notFound(folder_data2process+infile): APy3_GENfuns.printErr('not found: '+folder_data2process+infile)
(drkSmpl_DLSraw,drkRst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+infile, '/data','/reset', fromImg,toImg)
#---
#%% DLSraw => Gn,Crs,Fn
if verboseFlag: APy3_GENfuns.printcol('DLSraw => Gn,Crs,Fn','blue')
if highMemFlag: drk_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(drkSmpl_DLSraw,drkRst_DLSraw, ERRDLSraw, ERRint16)
else:
    drk_GnCrsFn= numpy.zeros((len(Img2proc),NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
    for thisImg in range(len(Img2proc)):
        thisSmpl_DLSraw= drkSmpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
        thisRst_DLSraw=  drkRst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
        this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
        drk_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
        if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,len(Img2proc))
    if cleanMemFlag: del thisSmpl_DLSraw; del thisRst_DLSraw; del this_dscrmbld_GnCrsFn
#---
#%% ADucorr, CMA,CDS,avg
if verboseFlag: APy3_GENfuns.printcol('ADU-correct','blue')
drkADU= APy3_GENfuns.numpy_NaNs((len(Img2proc),NSmplRst, NRow,NCol))
drkADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(drk_GnCrsFn[:,iSmpl,:,:,iCrs],drk_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
drkADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_NoGain(drk_GnCrsFn[:,iRst,:,:,iCrs], drk_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
if cleanMemFlag: del drk_GnCrsFn
#
mode_str=""
if CMAFlag:
    if verboseFlag: APy3_GENfuns.printcol('CMA','blue')
    drkADU[:,iSmpl,:,:]= APy3_P2Mfuns.CMA(drkADU[:,iSmpl,:,:] ,cols2CMA)
    drkADU[:,iRst,:,:]=  APy3_P2Mfuns.CMA(drkADU[:,iRst,:,:]  ,cols2CMA)
    mode_str+="CMA,"
#
if CDSFlag: 
    if verboseFlag: APy3_GENfuns.printcol('CDS avg','blue')
    PedGn0_ADU= numpy.average(APy3_P2Mfuns.CDS(drkADU),axis=0)
    mode_str+='CDS'
else: 
    if verboseFlag: APy3_GENfuns.printcol('Smpl avg','blue')
    PedGn0_ADU= numpy.average(drkADU[:,iSmpl,:,:],axis=0)
    mode_str+='Smpl'
#---
if showFlag: 
    APy3_GENfuns.plot_2D_all(PedGn0_ADU, False, 'col','row',"{0} [ADU]".format(mode_str), True)
    APy3_GENfuns.show_it()
#---
if saveAvgFlag: 
    APy3_GENfuns.write_1xh5(outFolder+out_avgFile, PedGn0_ADU, '/data/data')
    APy3_GENfuns.printcol("{0}-avg saved as {1}".format(mode_str,outFolder+out_avgFile),'green')
#---
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




# ---
#
#%% exec it


