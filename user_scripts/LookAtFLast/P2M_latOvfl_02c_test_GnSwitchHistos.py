# -*- coding: utf-8 -*-
"""
descrambled (DLSRaw) sweep, having 2 Gn => max & min switching point 

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_02c_test_GnSwitchHistos.py
or:
python3
exec(open("./P2M_latOvfl_02c_test_GnSwitchHistos.py").read())
"""
#
#%% imports and useful constants
from APy3_auxINIT import *
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#%% functions
#

# to FITfuns


# to FITfuns

def plot_errbar_1Dx2_andfit_samecanva(arrayX1,arrayY1,errbarY1,legend1, arrayX2,arrayY2,errbarY2,legend2, label_x,label_y, label_title):
    ''' 2x 1D scatter plot in the same canva ''' 
    (fit_slope1,fit_offset1)=     APy3_FITfuns.linear_fit(arrayX1,arrayY1)
    (fit_slope2,fit_offset2)=     APy3_FITfuns.linear_fit(arrayX2,arrayY2)
    #
    fig = matplotlib.pyplot.figure()
    #
    # stupid python tries to put plot before errorbar 
    matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5, label=legend1)
    matplotlib.pyplot.plot(arrayX1, APy3_FITfuns.linear_fun(arrayX1, fit_slope1,fit_offset1), '--b', label='fit')
    matplotlib.pyplot.errorbar(arrayX2, arrayY2,yerr=errbarY2, fmt='xg', fillstyle='none', capsize=5, label=legend2)
    matplotlib.pyplot.plot(arrayX2, APy3_FITfuns.linear_fun(arrayX2, fit_slope2,fit_offset2), '--g', label='fit')
    handles, labels = matplotlib.pyplot.gca().get_legend_handles_labels() 
    order = [2,0,3,1]
    matplotlib.pyplot.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    #
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)

#
# ---
#
#%% defaults for GUI window
#
#
'''
######################################### FSI01 PGABBB 0802h3, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_OD1.0_meta.dat' # tint<\tab>filename
#dflt_meta_file= 'reduced_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354'
#dflt_Row2proc='0:1439' 
#dflt_Col2proc='32:735'  
dflt_Row2proc=':' 
dflt_Col2proc=':'
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='Y'; dflt_normTo0='N';
dflt_plotLabel= "FSI01,PGABBB"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### FSI01 PGABBB 0802h3, Gn1->2 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_multiGnSweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.18_FSI01_Tm22_dmuxSELHigh_0802h3_3G_PGAB_OD0.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Img2proc='5:9' 
dflt_Row2proc='801:806' 
dflt_Col2proc='351:354'
dflt_Row2proc='0:1439' 
dflt_Col2proc='32:735' 
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='Y'; dflt_normTo0='N';
dflt_plotLabel= "FSI01,PGABBB"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
#'''
######################################### FSI01 PGA6BB 0802h4 Gn 0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190704_000_FSI01_Tm20_3G/processed/2019.07.30_FSI01_Tm20_dmuxSELHigh_0802h4_3G_PGA6BB_sweep/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= '2019.07.30_FSI01_Tm20_dmuxSELHigh_0802h4_3G_PGA6BB_OD2.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/FSI01/FSI01_Tm20_dmuxSELHigh/FSI01_Tm20_dmuxSELHigh_H0only_ADCcor/FSI01_Tminus20_dmuxSELHigh_2019.06.15_ADCcor.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='800:806' 
#dflt_Col2proc='350:354' 
#dflt_Row2proc='0:1439' 
#dflt_Col2proc='32:735' 
dflt_Row2proc=':' 
dflt_Col2proc=':'
dflt_Row2proc='808:808' 
dflt_Col2proc='350:350'
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='Y'; dflt_normTo0='N'
dflt_plotLabel= "FSI01,PGA6BB"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
#'''
#
'''
######################################### BSI02 PGABBB 0802k2, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190920_000_BSI02_Tm20_LatOvflw/processed/2019.09.20_Latovflw_BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI02_Tm20_dmuxSELHigh_0802k2_3G_PGABBB_OD1.5_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_ADCcor/BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
#dflt_Row2proc='801:806' 
#dflt_Col2proc='351:354' 
#dflt_Row2proc='0:1483' 
#dflt_Col2proc='32:1439' 
dflt_Row2proc=':' 
dflt_Col2proc=':'
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='N';
#
dflt_plotLabel= "BSI02,PGABBB"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### BSI02 PGA111 0802k2, Gn0->1 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190920_000_BSI02_Tm20_LatOvflw/processed/2019.09.20_Latovflw_BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI02_Tm20_dmuxSELHigh_0802k2_3G_PGA111_OD1.5_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_ADCcor/BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
#
dflt_Gn_to_calculate=1
#
dflt_Img2proc='5:9' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:354' 
dflt_Row2proc='0:1483' 
dflt_Col2proc='32:1439' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='N';
#
dflt_plotLabel= "BSI02,PGA111"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#
'''
######################################### BSI02 PGABBB 0802k2, Gn1->2 ##################################################################################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190920_000_BSI02_Tm20_LatOvflw/processed/2019.09.20_Latovflw_BSI02_Tm20_dmuxSELHigh_0802k2_PGABBB/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_meta_file= 'BSI02_Tm20_dmuxSELHigh_0802k2_3G_PGABBB_OD0.0_meta.dat' # tint<\tab>filename
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI02/BSI02_Tm20_dmuxSELHigh/BSI02_Tm20_dmuxSELHigh_H0,H1_ADCcor/BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
#
dflt_Gn_to_calculate=2
#
dflt_Img2proc='5:9' 
dflt_Row2proc='801:801' 
dflt_Col2proc='351:354' 
dflt_Row2proc='0:1483' 
dflt_Col2proc='32:1439' 
#dflt_Row2proc=':' 
#dflt_Col2proc=':'
#
dflt_debugFlag='Y'; dflt_debugFlag='N';
dflt_normTo0='N';
#
dflt_plotLabel= "BSI02,PGABBB"
#
dflt_highMemFlag='N'
dflt_cleanMemFlag='Y'
dflt_verboseFlag='Y'
'''
#



# ---
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['process data: from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['process data: metafile'] 
GUIwin_arguments+= [dflt_meta_file] 
#
GUIwin_arguments+= ['ADUcorr: file'] 
GUIwin_arguments+= [dflt_ADUcorr_file]
#GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
#GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['process data: in Cols [from:to]'] 
GUIwin_arguments+= [dflt_Col2proc]
#
GUIwin_arguments+= ['Gn_to_calculate [1/2]'] 
GUIwin_arguments+= [dflt_Gn_to_calculate]
#
GUIwin_arguments+= ['normalize (Crs=0,Fn=255) to ADU=0? [Y/N]'] 
GUIwin_arguments+= [dflt_normTo0]
#
GUIwin_arguments+= ['show individual pixel ramps? [Y/N]'] 
GUIwin_arguments+= [dflt_debugFlag]
GUIwin_arguments+= ['plot label'] 
GUIwin_arguments+= [dflt_plotLabel]
#
GUIwin_arguments+= ['high mem usage? [Y/N]'] 
GUIwin_arguments+= [dflt_highMemFlag] 
GUIwin_arguments+= ['clean mem when possible? [Y/N]'] 
GUIwin_arguments+= [dflt_cleanMemFlag]
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [dflt_verboseFlag]
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
i_param=0
folder_data2process= dataFromUser[i_param]; i_param+=1
meta_file= dataFromUser[i_param]; i_param+=1
ADUcorr_file= dataFromUser[i_param]; i_param+=1;  
#multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1];
#
Row2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Row2proc_mtlb in ['all','All','ALL',':','*','-1']: Row2proc= numpy.arange(NRow)
else: Row2proc=APy3_GENfuns.matlabLike_range(Row2proc_mtlb)
#
Col2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Col2proc_mtlb in ['all','All','ALL',':','*','-1']: Col2proc= numpy.arange(32,NCol)
else: Col2proc=APy3_GENfuns.matlabLike_range(Col2proc_mtlb)
#
Gn_to_calculate= int(dataFromUser[i_param]); i_param+=1;  
#
normTo0Flag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
debugFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1

plotLabel= dataFromUser[i_param]; i_param+=1;
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using metafile {0}'.format(meta_file),'blue')
    APy3_GENfuns.printcol('will ADU-correct using {0})'.format(ADUcorr_file),'blue')
    #
    APy3_GENfuns.printcol('will elaborate Img{0}, pix({1},{2})'.format(Img2proc_mtlb,Row2proc_mtlb,Col2proc_mtlb),'blue')
    #
    APy3_GENfuns.printcol('will try to calculate parameters for Gn{0}'.format(Gn_to_calculate),'blue')
    #APy3_GENfuns.printcol('  assuming Gn{0} Pedestal[ADU] and e/ADU data from {1}'.format(Gn_to_calculate-1,multiGnCal_file),'blue')
    if normTo0Flag: APy3_GENfuns.printcol('will show ADU values normalized (crs=0,fn=255->ADU=0)','blue')
    #
    if debugFlag: APy3_GENfuns.printcol('will show individual pixel ramps','blue')
    #
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
gainRatioMap= APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
unknown_ADU2e=APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
unknown_ADU0= APy3_GENfuns.numpy_NaNs((NRow,NCol)) 
# ---
if verboseFlag: APy3_GENfuns.printcol('load meta-file and calibr-files','blue')
if APy3_GENfuns.notFound(folder_data2process+meta_file): APy3_GENfuns.printErr('not found: '+folder_data2process+meta_file)
meta_content= APy3_GENfuns.read_tst(folder_data2process+meta_file)
meta_fileNameList= meta_content[:,1]
meta_tintAr= meta_content[:,0].astype(float)
meta_Nfiles= len(meta_fileNameList)
if verboseFlag: APy3_GENfuns.printcol("{0} entries in the metafile".format(meta_Nfiles),'green')
#
if APy3_GENfuns.notFound(ADUcorr_file): APy3_GENfuns.printErr('not found: '+ADUcorr_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
 ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADUcorr_file)
#
#if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
#(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
#known_ADU2e= e_per_ADU_multiGn[Gn_to_calculate-1,:,:]
#PedADU_knownGn= PedestalADU_multiGn[Gn_to_calculate-1,:,:] not used or usable here
#
# ---
#
#%% light file: DLSRaw => Gn,ADU
if verboseFlag: APy3_GENfuns.printcol('convert sequence files DLSRaw => Gn,ADU','blue')
allData_ADU= APy3_GENfuns.numpy_NaNs((meta_Nfiles,len(Img2proc),NSmplRst, NRow,NCol))
allData_Gn=  numpy.zeros((meta_Nfiles,len(Img2proc),NRow,NCol),dtype=int)-1
aux_theseADU= APy3_GENfuns.numpy_NaNs((len(Img2proc),NSmplRst, NRow,NCol))
allData_tintAr = numpy.transpose(numpy.tile(meta_tintAr, (len(Img2proc),1)), (1,0)) # NImg => (Nfile,NImg)
#
for iFile,thisFile in enumerate(meta_fileNameList):
    if verboseFlag: APy3_GENfuns.printcol("processing lgh file {0}/{1}".format(iFile,meta_Nfiles-1),'green')
    (dataSmpl_DLSraw,dataRst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+thisFile, '/data','/reset', fromImg, toImg)
    data_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(dataSmpl_DLSraw,dataRst_DLSraw, ERRDLSraw, ERRint16)
    if cleanMemFlag: del dataSmpl_DLSraw; del dataRst_DLSraw
    allData_Gn[iFile,:,:,:]=data_GnCrsFn[:,iSmpl,:,:,iGn].astype(int) 
    #
    aux_theseADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iSmpl,:,:,iCrs],data_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
    aux_theseADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_NoGain(data_GnCrsFn[:,iRst,:,:,iCrs], data_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
    aux_norm_str='Smpl'
    #
    if normTo0Flag: 
            aux_theseADU[:,iSmpl,:,:]= APy3_P2Mfuns.ADCcorr_from0_NoGain(data_GnCrsFn[:,iSmpl,:,:,iCrs],data_GnCrsFn[:,iSmpl,:,:,iFn],
                                                           ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, NRow,NCol)
            aux_theseADU[:,iRst,:,:]=  APy3_P2Mfuns.ADCcorr_from0_NoGain(data_GnCrsFn[:,iRst,:,:,iCrs], data_GnCrsFn[:,iRst,:,:,iFn],
                                                           ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset, ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset,  NRow,NCol)
            aux_norm_str='Smpl-norm'
    #
    missingValMap= data_GnCrsFn[:,:,:,:,iCrs]==ERRint16 #(Nimg, NSmplRst,NRow,NCol)
    aux_theseADU[missingValMap]= numpy.NaN
    allData_ADU[iFile,:,:,:,:]= numpy.copy(aux_theseADU)
    # ...
    if cleanMemFlag: del data_GnCrsFn; del missingValMap
if cleanMemFlag: del aux_theseADU
# ---
#
#%% elab data
Smpl_Gnswitch_min=[]; Smpl_Gnswitch_max=[]
Smpl_Gnswitch_min_2DAr= APy3_GENfuns.numpy_NaNs((NRow,NCol))
Smpl_Gnswitch_max_2DAr= APy3_GENfuns.numpy_NaNs((NRow,NCol))
for thisRow in Row2proc:
    for thisCol in Col2proc:
        #
        #auxmap_GnLow= (allData_Gn[:,:,thisRow,thisCol]==Gn_to_calculate-1)
        #auxmap_GnHigh= (allData_Gn[:,:,thisRow,thisCol]==Gn_to_calculate)
        #if (numpy.sum(auxmap_GnLow)>0)&(numpy.sum(auxmap_GnHigh)>0):
        #    Smpl_Gnswitch_max += [numpy.namax(allData_ADU[:,:,iSmpl,thisRow,thisCol][auxmap_GnLow])]
        #
        auxmapGnLow= numpy.argwhere(allData_Gn[:,:,thisRow,thisCol]==Gn_to_calculate-1)
        auxmapGnHigh= numpy.argwhere(allData_Gn[:,:,thisRow,thisCol]==Gn_to_calculate)
        if (len(auxmapGnLow)>0)&(len(auxmapGnHigh)>0):
            indices_maxGnLow=auxmapGnLow[-1]
            #print(indices_maxGnLow)
            iFile_maxGnLow=indices_maxGnLow[0]; iImg_maxGnLow=indices_maxGnLow[1]
            #print(str(iFile_maxGnLow))
            #print(str(iImg_maxGnLow))
            indices_minGnHigh=auxmapGnHigh[0]
            iFile_minGnHigh=indices_minGnHigh[0]; iImg_minGnHigh=indices_minGnHigh[1]
            #
            if iFile_minGnHigh>0:
                #Smpl_Gnswitch_max += [allData_ADU[iFile_maxGnLow,iImg_maxGnLow,iSmpl,thisRow,thisCol]]
                #Smpl_Gnswitch_min += [allData_ADU[iFile_minGnHigh-1,-1,iSmpl,thisRow,thisCol]] # last img of previous int time
                
                if ( numpy.isnan(allData_ADU[iFile_maxGnLow,:,iSmpl,thisRow,thisCol]).any()==False )&( numpy.isnan(allData_ADU[iFile_minGnHigh-1,:,iSmpl,thisRow,thisCol]).any()==False ):
                    Smpl_Gnswitch_max += [numpy.nanmax(allData_ADU[iFile_maxGnLow,:,iSmpl,thisRow,thisCol])] # max val of last int time of Gn_to_calculate-1
                    Smpl_Gnswitch_min += [numpy.nanmax(allData_ADU[iFile_minGnHigh-1,:,iSmpl,thisRow,thisCol])] # max val of previous int time to 1st Gn switch
                    Smpl_Gnswitch_max_2DAr[thisRow,thisCol]= numpy.nanmax(allData_ADU[iFile_maxGnLow,:,iSmpl,thisRow,thisCol]) 
                    Smpl_Gnswitch_min_2DAr[thisRow,thisCol]= numpy.nanmax(allData_ADU[iFile_minGnHigh-1,:,iSmpl,thisRow,thisCol])
        if debugFlag:
            map_knownGn=   allData_Gn[:,:,thisRow,thisCol]==(Gn_to_calculate-1)
            map_unknownGn= allData_Gn[:,:,thisRow,thisCol]==(Gn_to_calculate)
            tint_knownGn=  allData_tintAr[map_knownGn].flatten()
            tint_unknownGn=allData_tintAr[map_unknownGn].flatten()      
            aux_smpl= numpy.copy(allData_ADU[:,:,iSmpl,thisRow,thisCol])
            smpl_knownGn= aux_smpl[map_knownGn].flatten() 
            smpl_unknownGn= aux_smpl[map_unknownGn].flatten()
            if (len(smpl_knownGn)>0) & (len(smpl_unknownGn)>0):
                APy3_GENfuns.printcol("showing pix ({0},{1})".format(thisRow,thisCol),'green')
                if (Gn_to_calculate==1): APy3_GENfuns.plot_1Dx3_samecanva(tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_norm_str,Gn_to_calculate-1), 
                                               tint_unknownGn,smpl_unknownGn,'{0},Gn{1}'.format(aux_norm_str,Gn_to_calculate), 
                                               [],[],'Gn2',
                                               'tint [ms]','{0} [ADU]'.format(aux_norm_str), '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)
                else: APy3_GENfuns.plot_1Dx3_samecanva([],[],'Gn0',
                                               tint_knownGn,smpl_knownGn,'{0},Gn{1}'.format(aux_norm_str,Gn_to_calculate-1), 
                                               tint_unknownGn,smpl_unknownGn,'{0},Gn{1}'.format(aux_norm_str,Gn_to_calculate), 
                                               'tint [ms]','{0} [ADU]'.format(aux_norm_str), '{0}, pix({1},{2})'.format(plotLabel,thisRow,thisCol), False)
                APy3_GENfuns.showIt()
            else: APy3_GENfuns.printcol("no points to show for pix ({0},{1})".format(thisRow,thisCol),'orange')
         
#
Smpl_Gnswitch_min= numpy.array(Smpl_Gnswitch_min)
Smpl_Gnswitch_max= numpy.array(Smpl_Gnswitch_max)
#
APy3_GENfuns.plot_multihisto1D(numpy.transpose(numpy.vstack((Smpl_Gnswitch_min,Smpl_Gnswitch_max))), 100, False, ['min Gn-switch','max Gn-switch'], 'Gn-switch, {0} [ADU]'.format(aux_norm_str),'pixels','{0}, Gn{1}->{2}, pix({3},{4})'.format(plotLabel,Gn_to_calculate-1,Gn_to_calculate,Row2proc_mtlb,Col2proc_mtlb),False)

APy3_GENfuns.plot_histo1d(Smpl_Gnswitch_max-Smpl_Gnswitch_min, 100, False, 'max-min Gn-switch point , {0} [ADU]'.format(aux_norm_str),'pixels','{0}, Gn{1}->{2}: max-min Gn-switch point, pix({3},{4})'.format(plotLabel,Gn_to_calculate-1,Gn_to_calculate,Row2proc_mtlb,Col2proc_mtlb))

APy3_GENfuns.plot_2D_all(Smpl_Gnswitch_max_2DAr, False, 'col','row','{0}, Gn{1}->{2}: max Gn-switch [ADU], pix({3},{4})'.format(plotLabel,Gn_to_calculate-1,Gn_to_calculate,Row2proc_mtlb,Col2proc_mtlb), True)
APy3_GENfuns.plot_2D_all(Smpl_Gnswitch_min_2DAr, False, 'col','row','{0}, Gn{1}->{2}: min Gn-switch [ADU], pix({3},{4})'.format(plotLabel,Gn_to_calculate-1,Gn_to_calculate,Row2proc_mtlb,Col2proc_mtlb), True)
APy3_GENfuns.plot_2D_all(Smpl_Gnswitch_max_2DAr-Smpl_Gnswitch_min_2DAr, False, 'col','row','{0}, Gn{1}->{2}: max-min Gn-switch [ADU], pix({3},{4})'.format(plotLabel,Gn_to_calculate-1,Gn_to_calculate,Row2proc_mtlb,Col2proc_mtlb), True)


APy3_GENfuns.showIt()
#
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')
# ---
# ---
# ---

