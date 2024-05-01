# -*- coding: utf-8 -*-
"""
ADCcor files + ADC ramp => show ramps

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_ADCcorr_04_checkRamps.py
or:
python3
exec(open("./P2M_ADCcorr_04_checkRamps.py").read())
"""

#%% imports and useful constants
from APy3_auxINIT import *
import ast # ast.literal_eval()
#
import warnings
#with warnings.catch_warnings():
#    warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
warnings.filterwarnings('ignore')
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

# ---
#
#%% defaults for GUI window
'''
######################### T-20, dmuxSELsw #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190904_001_BSI02_Tm20_ADCcorrection/processed/2019.09.04_BSI02_ADCsweep_dmuxSELsw/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.06.xx_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True
#dflt_Row2proc='0:1483' # means: [all]
#dflt_Cols2proc='32:735' # means: [H0]  
dflt_Row2proc='500:501' # means: [all]
dflt_Cols2proc='600:606' # means: [H0]  
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCcorParam/' +'/BSI02_Tminus20_dmuxSELsw_2019.09.04_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
'''
#
'''
######################### T-20, dmuxSELHigh #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190904_001_BSI02_Tm20_ADCcorrection/processed/2019.09.04_BSI02_ADCsweep_dmuxSELHigh/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.06.xx_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True 
dflt_Row2proc='500:501' # means: [all]
dflt_Cols2proc='600:606' # means: [H0]  
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCcorParam/' + 'BSI02_Tminus20_dmuxSELHigh_2019.09.04_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
'''
#
'''
######################### T-30, dmuxSELsw #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190905_000_BSI02_Tm30_ADCcorrection/processed/2019.09.05_BSI02_Tminus30_0802i_PGAB_dmuxSELsw/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.06.xx_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True  
dflt_Row2proc='500:501' # means: [all]
dflt_Cols2proc='600:606' # means: [H0]  
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCcorParam/' +'/BSI02_Tminus30_dmuxSELsw_2019.09.05_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
'''
#
'''
######################### T-30, dmuxSELHigh #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190905_000_BSI02_Tm30_ADCcorrection/processed/2019.09.05_BSI02_Tminus30_0802i_PGAB_dmuxSELHigh/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.06.xx_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True  
dflt_Row2proc='500:501' # means: [all]
dflt_Cols2proc='600:606' # means: [H0]  
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCcorParam/' +'/BSI02_Tminus30_dmuxSELHigh_2019.09.05_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
'''
#
'''
######################### BSI04 T-20, dmuxSELsw #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/v2_biasBSI04_02/BSI04_Tm20_dmuxSELsw_ADCramps/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.11.20_dmuxSELsw_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True  
dflt_Row2proc='500:501' # 
dflt_Cols2proc='600:606' # 
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCParam_FLastScripts/' +'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
'''
#
#'''
######################### BSI04 T-20, dmuxSELHi #########################
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191119_000_BSI04_ADCcorr/processed/v2_biasBSI04_02/BSI04_Tm20_dmuxSELHi_ADCramps/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_indexFileName='2019.11.20_dmuxSELHi_all_600x10_meta.dat'
dflt_inputFileSuffix='.h5'
dflt_showFlag= True  
dflt_Row2proc='500:501' # 
dflt_Cols2proc='600:606' # 
dflt_Img2proc='2:9'#
dflt_ADCcor_file= dflt_folder_data2process + '../ADCParam_FLastScripts/' +'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_debugFlag= True
dflt_verboseFlag= True
#'''

# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['data to process are in folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
GUIwin_arguments+= ['index file'] 
GUIwin_arguments+= [dflt_indexFileName]
GUIwin_arguments+= ['inputFileSuffix'] 
GUIwin_arguments+= [dflt_inputFileSuffix]
#
GUIwin_arguments+= ['show graphs for each pixel? [Y/N]']
GUIwin_arguments+= [str(dflt_showFlag)]
GUIwin_arguments+= ['process data: in columns [from:to]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Row2proc] 
GUIwin_arguments+= ['show data: using images [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc]
#
GUIwin_arguments+= ['ADCcor_1file'] 
GUIwin_arguments+= [dflt_ADCcor_file] 
#
GUIwin_arguments+= ['debug? [Y/N]'] 
GUIwin_arguments+= [str(dflt_debugFlag)] 
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [str(dflt_verboseFlag)]
#
# ---

# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
folder_data2process= dataFromUser[i_param]; i_param+=1
indexFileName= dataFromUser[i_param]; i_param+=1
inputFileSuffix= dataFromUser[i_param]; i_param+=1
#
showFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Cols2proc_mtlb in ['all','All','ALL',':','*','-1']: Cols2proc= numpy.arange(NCol)
else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
#
Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Rows2proc_mtlb in ['all','All','ALL',':','*','-1']: Rows2proc= numpy.arange(NRow)
else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printERR('you need to give an explicit range to the process data: using images [from:to]')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); NImg2procxFile=len(Img2proc)
#
ADCcor_file= dataFromUser[i_param]; i_param+=1
#
debugFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will process data from '+folder_data2process,'blue')
APy3_GENfuns.printcol('index file: {0}'.format(indexFileName),'blue')
if APy3_GENfuns.notFound(folder_data2process+indexFileName): APy3_P2M.printErr('not found: '+folder_data2process+indexFileName)
APy3_GENfuns.printcol('  assuming a file suffix: {0}'.format(inputFileSuffix),'blue')
APy3_GENfuns.printcol('will use ADCcor from'+ADCcor_file,'blue')
if (showFlag): APy3_GENfuns.printcol('will show graphs for pixels ({0},{1})'.format(Rows2proc_mtlb,Cols2proc_mtlb),'blue')
if APy3_GENfuns.notFound(ADCcor_file): APy3_P2Mfuns.printErr('not found: '+ADCcor_file)
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#%% read ADCparam files, show if needed
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset, 
ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
if debugFlag:
    plot_2x2D(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, False, 'row','col', 'ADCparam_Smpl_crs_slope','ADCparam_Smpl_crs_offset', True)
    plot_2x2D(ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,   False, 'row','col', 'ADCparam_Smpl_fn_slope','ADCparam_Smpl_fn_offset', True)
    plot_2x2D(ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,   False, 'row','col', 'ADCparam_Rst_crs_slope','ADCparam_Rst_crs_offset', True)
    plot_2x2D(ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,     False, 'row','col', 'ADCparam_Rst_fn_slope','ADCparam_Rst_fn_offset', True)
    APy3_GENfuns.showIt()
# ---
#%% read files
APy3_GENfuns.printcol('reading metadata file','blue')
indexFileList= APy3_GENfuns.read_tst(folder_data2process+indexFileName)
idCollList=indexFileList[:,0]
CollList=indexFileList[:,1]
NColl= len(CollList)
if (verboseFlag): APy3_GENfuns.printcol('{0} collections detailed in the index file'.format(len(CollList)),'green')
#
dataSmplRst2proc= numpy.zeros((NColl,NImg2procxFile,NSmplRst,NRow,NCol,NGnCrsFn),dtype='int16') 
Id_allData= numpy.zeros((NColl,NImg2procxFile)) 
#
for thisColl in range(len(CollList)):
    thisCollFile= folder_data2process+CollList[thisColl]+inputFileSuffix
    thisCollId_nameFromFile= idCollList[thisColl]
    if (verboseFlag): APy3_GENfuns.printcol('{0}/{1}: reading {2}'.format(thisColl,len(CollList)-1, thisCollFile),'green')
    (thisSmpl,thisRst)= APy3_GENfuns.read_2xh5(thisCollFile, '/data', '/reset')
    dataSmplRst2proc[thisColl,:,:,:,:,:]= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl,thisRst, ERRDLSraw,ERRint16)[Img2proc,:,:,:,:] # [coll,Img,row,col,gn/cs/fn] <- [Img,SmplRst,row,col,gn/cs/fn]
    Id_allData[thisColl,:]= float(idCollList[thisColl])
dataSmplRst2proc= dataSmplRst2proc.reshape((NColl*NImg2procxFile,NSmplRst,NRow,NCol,NGnCrsFn))
Id_allData= Id_allData.reshape((NColl*NImg2procxFile))
# ---
#%% show pixel evols 
thisRow=Rows2proc[0]; thisCol=Cols2proc[0]
minFn_acceptable=1; maxFn_acceptable=254
APy3_GENfuns.printcol("plot individual [P]ixel ramps / find [M]in-max of fine ramps / [E]nd plotting", 'blue')
nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['p','P']:
        APy3_GENfuns.printcol("which Row? [default is {0}]".format(thisRow), 'black'); thisRow_in= input(); 
        if (len(thisRow_in)>0): thisRow= int(thisRow_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col? [default is {0}]".format(thisCol), 'black'); thisCol_in= input(); 
        if (len(thisCol_in)>0): thisCol= int(thisCol_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will show pix ({0},{1})".format(thisRow,thisCol), 'black'); thisCol_in= input(); 
        #
        data2Show_Smpl_ADCcor= APy3_P2Mfuns.ADCcorr_from0_NoGain(dataSmplRst2proc[:,iSmpl,thisRow,thisCol,iCrs],dataSmplRst2proc[:,iSmpl,thisRow,thisCol,iFn],
                                                                     ADCparam_Smpl_crs_slope[thisRow,thisCol],ADCparam_Smpl_crs_offset[thisRow,thisCol],
                                                                     ADCparam_Smpl_fn_slope[thisRow,thisCol],ADCparam_Smpl_fn_offset[thisRow,thisCol], 1,1)[0,:]
        APy3_GENfuns.plot_1D(Id_allData, dataSmplRst2proc[:,iSmpl,thisRow,thisCol,iCrs],'VRST','Crs','({0},{1}),Smpl,Crs'.format(thisRow,thisCol))
        APy3_GENfuns.plot_1D(Id_allData, dataSmplRst2proc[:,iSmpl,thisRow,thisCol,iFn], 'VRST','Fn','({0},{1}),Smpl,Crs'.format(thisRow,thisCol))
        APy3_GENfuns.plot_1D(Id_allData, data2Show_Smpl_ADCcor,'VRST','ADCcorr [ADU]','({0},{1}),Smpl, ADC-corrected values'.format(thisRow,thisCol))
        #
        aux_nbinsX_max= max(Id_allData); aux_nbinsX_min= min(Id_allData); aux_nbinsX_Nsteps= len(Id_allData)
        aux_nbinsX= numpy.linspace(aux_nbinsX_min,aux_nbinsX_max, aux_nbinsX_Nsteps)
        aux_nbinsY_max= max(data2Show_Smpl_ADCcor); aux_nbinsY_min= min(data2Show_Smpl_ADCcor); aux_nbinsY_Nsteps= len(Id_allData)
        aux_nbinsY= numpy.linspace(aux_nbinsY_min,aux_nbinsY_max, aux_nbinsY_Nsteps)     
        if numpy.isnan(data2Show_Smpl_ADCcor).any()==False: APy3_GENfuns.plot_histo2D(Id_allData,data2Show_Smpl_ADCcor, aux_nbinsX,aux_nbinsY, "VRST [V]",
                                                                                     "ADCcorr [ADU]",'({0},{1}),Smpl, ADC-corrected values'.format(thisRow,thisCol), 0.1) 

        APy3_GENfuns.showIt()
        #
        data2Show_Rst_ADCcor=  APy3_P2Mfuns.ADCcorr_from0_NoGain(dataSmplRst2proc[:,iRst,thisRow,thisCol,iCrs],dataSmplRst2proc[:,iRst,thisRow,thisCol,iFn],
                                                                     ADCparam_Rst_crs_slope[thisRow,thisCol],ADCparam_Rst_crs_offset[thisRow,thisCol],
                                                                     ADCparam_Rst_fn_slope[thisRow,thisCol],ADCparam_Rst_fn_offset[thisRow,thisCol], 1,1)[0,:]
        APy3_GENfuns.plot_1D(Id_allData, dataSmplRst2proc[:,iRst,thisRow,thisCol,iCrs],'VRST','Crs','({0},{1}),Rst,Crs'.format(thisRow,thisCol))
        APy3_GENfuns.plot_1D(Id_allData, dataSmplRst2proc[:,iRst,thisRow,thisCol,iFn], 'VRST','Fn','({0},{1}),Rst,Crs'.format(thisRow,thisCol))
        APy3_GENfuns.plot_1D(Id_allData, data2Show_Rst_ADCcor, 'VRST','ADCcorr [ADU]','({0},{1}),Rst, ADC-corrected values'.format(thisRow,thisCol))
        #
        aux_nbinsX_max= max(Id_allData); aux_nbinsX_min= min(Id_allData); aux_nbinsX_Nsteps= len(Id_allData)
        aux_nbinsX= numpy.linspace(aux_nbinsX_min,aux_nbinsX_max, aux_nbinsX_Nsteps)
        aux_nbinsY_max= max(data2Show_Rst_ADCcor); aux_nbinsY_min= min(data2Show_Rst_ADCcor); aux_nbinsY_Nsteps= len(Id_allData)
        aux_nbinsY= numpy.linspace(aux_nbinsY_min,aux_nbinsY_max, aux_nbinsY_Nsteps)     
        if numpy.isnan(data2Show_Rst_ADCcor).any()==False: APy3_GENfuns.plot_histo2D(Id_allData,data2Show_Rst_ADCcor, aux_nbinsX,aux_nbinsY, "VRST [V]",
                                                                                     "ADCcorr [ADU]",'({0},{1}),Smpl, ADC-corrected values'.format(thisRow,thisCol), 0.1) 
        APy3_GENfuns.showIt()
    #
    elif nextstep in ['m','M']:
        valid_Crs_range= numpy.arange(5,26)
        APy3_GENfuns.printcol("will look for min,max in Fn ramps, for {0}<=crs<={1}".format(valid_Crs_range[0], valid_Crs_range[-1]), 'blue')
        APy3_GENfuns.printcol("which min fine is acceptable? [default is {0}]".format(minFn_acceptable), 'black'); minFn_acceptable_in= input();
        if (len(minFn_acceptable_in)>0): minFn_acceptable= int(minFn_acceptable_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("which max fine is acceptable? [default is {0}]".format(maxFn_acceptable), 'black'); maxFn_acceptable_in= input();
        if (len(maxFn_acceptable_in)>0): maxFn_acceptable= int(maxFn_acceptable_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will alert if minFn<{0} or maxFn>{1} in Fn ramps, for {2}<=crs<={3}".format(minFn_acceptable,maxFn_acceptable,valid_Crs_range[0], valid_Crs_range[-1]), 'blue')
        #
        valid_crs_map= (dataSmplRst2proc[:,:,:,:,iCrs] >= valid_Crs_range[0]) & (dataSmplRst2proc[:,:,:,:,iCrs] <= valid_Crs_range[-1])
        dataSmplRst2invest= numpy.copy(dataSmplRst2proc[:,:,:,:,iFn])+0.0
        dataSmplRst2invest[~valid_crs_map]= numpy.NaN
        maxFnSmpl= numpy.nanmax(dataSmplRst2invest[:,iSmpl,:,:],axis=0)
        maxFnRst= numpy.nanmax(dataSmplRst2invest[:,iRst,:,:],axis=0)
        minFnSmpl= numpy.nanmin(dataSmplRst2invest[:,iSmpl,:,:],axis=0)
        minFnRst= numpy.nanmin(dataSmplRst2invest[:,iRst,:,:],axis=0)
        #
        NbadPix= numpy.sum(maxFnSmpl[~numpy.isnan(maxFnSmpl)]>maxFn_acceptable)
        if NbadPix>0: APy3_GENfuns.printcol("{0} pixels maxFnSmpl > {1}".format(NbadPix, maxFn_acceptable), 'orange')
        NbadPix= numpy.sum(maxFnRst[~numpy.isnan(maxFnRst)]>maxFn_acceptable)
        if NbadPix>0: APy3_GENfuns.printcol("{0} pixels maxFnRst > {1}".format(NbadPix, maxFn_acceptable), 'orange')
        #
        NbadPix= numpy.sum(minFnSmpl[~numpy.isnan(minFnSmpl)]<minFn_acceptable)
        if NbadPix>0: APy3_GENfuns.printcol("{0} pixels minFnSmpl < {1}".format(NbadPix, minFn_acceptable), 'orange')
        NbadPix= numpy.sum(minFnRst[~numpy.isnan(minFnRst)]<minFn_acceptable)
        if NbadPix>0: APy3_GENfuns.printcol("{0} pixels minFnRst < {1}".format(NbadPix, minFn_acceptable), 'orange')
        #
        if ( numpy.sum(maxFnSmpl[~numpy.isnan(maxFnSmpl)]>maxFn_acceptable) + numpy.sum(maxFnRst[~numpy.isnan(maxFnRst)]>maxFn_acceptable) + 
             numpy.sum(minFnSmpl[~numpy.isnan(minFnSmpl)]<minFn_acceptable) + numpy.sum(minFnRst[~numpy.isnan(minFnRst)]<minFn_acceptable) ) <1: 
            APy3_GENfuns.printcol("all pixels have values {0} <= Fn <= {1} , in the crs range".format(minFn_acceptable, maxFn_acceptable), 'green')
        #
        plot_2x2D(minFnSmpl,maxFnSmpl, False, 'col','row', 'Smpl,minFn','Smpl,maxFn', True)
        plot_2x2D(minFnRst,maxFnRst, False, 'col','row', 'Rst,minFn','Rst,maxFn', True)
        APy3_GENfuns.showIt()

    #
    APy3_GENfuns.printcol("plot individual [P]ixel ramps / find [M]in-max of fine ramps / [E]nd plotting", 'blue')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




