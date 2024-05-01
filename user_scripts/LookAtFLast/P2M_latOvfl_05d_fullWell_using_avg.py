# -*- coding: utf-8 -*-
"""
set .h5 of avgADU and estQ at different int times => eval full will

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
cd /home/marras/PercAuxiliaryTools/LookAtFLast
python3 ./xxx.py
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

INTERACTLVElist= ['i','I','interactive','Interactive','INTERACTIVE']

def aux2histo(Ar2D):
    out2histo= numpy.copy(Ar2D.flatten())
    validMap= ~numpy.isnan(out2histo)
    out2histo= numpy.copy(out2histo[validMap])
    return out2histo


def read_warn_1xh5(filenamepath, path_2read):
    if APy3_GENfuns.notFound(filenamepath): APy3_GENfuns.printErr("not found: "+filenamepath)
    dataout= APy3_GENfuns.read_1xh5(filenamepath, path_2read)
    return dataout

def plot_errbar(arrayX1,arrayY1,errbarY1, label_x,label_y, label_title, loglogFlag):
    """ scatter plot (+errbars)""" 
    fig = matplotlib.pyplot.figure()
    if loglogFlag:
        matplotlib.pyplot.xscale('log', nonposx='clip')
        matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.errorbar(arrayX1, arrayY1,yerr=errbarY1, fmt='ob', fillstyle='none', capsize=5)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title) 
    matplotlib.pyplot.show(block=False)
    return (fig)

def png_1D(arrayX, arrayY, label_x,label_y,label_title, filenamepath):
    ''' 1D scatter plot: save(not show): e.g. filenamepath='/tmp/test0.png' '''
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.plot(arrayX, arrayY, 'o', fillstyle='none')
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_histo1D(array_2plot, histobins, logScaleFlag, label_x,label_y,label_title, filenamepath):
    """ plot a histogram: save(not show) as png """
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.hist(array_2plot, bins=histobins)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    if logScaleFlag: matplotlib.pyplot.yscale('log', nonposy='clip')
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

def png_2D_all(array2D, logScaleFlag, label_x,label_y,label_title, invertx_flag, filenamepath):
    ''' 2D image: save(not show) as png'''
    matplotlib.pyplot.ioff()
    #
    if filenamepath[-4:] in ['.png','.PNG']: filenamepath_out= filenamepath
    else:  filenamepath_out= filenamepath+'.png'
    #
    cmap = matplotlib.pyplot.cm.jet
    fig = matplotlib.pyplot.figure()
    if logScaleFlag: matplotlib.pyplot.imshow(array2D, norm=matplotlib.colors.LogNorm(), interpolation='none', cmap=cmap)
    else: matplotlib.pyplot.imshow(array2D, interpolation='none', cmap=cmap)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    matplotlib.pyplot.title(label_title)
    matplotlib.pyplot.colorbar()
    if (invertx_flag==True): matplotlib.pyplot.gca().invert_xaxis();
    matplotlib.pyplot.savefig(filenamepath_out)
    matplotlib.pyplot.close(fig)
    #
    matplotlib.pyplot.ion()
    return

#---
# local functions
def aux_fullwell(alldata_3DAr, thisRow,thisCol,
                 fit_maxADU,fit_minNpoints,fit_minR2,fullwell_dev_perc, 
                 showFlag,saveFlag,saveFolder,verboseFlag):
    j_ADU=1; j_estQ=0
    fullwellQ= numpy.NaN
    # prep to fit: reduce to <= fit_maxADU
    map2fit= alldata_3DAr[j_ADU,:,thisRow,thisCol]<=fit_maxADU*numpy.nanmax(alldata_3DAr[j_ADU,:,thisRow,thisCol])
    data2fit_X= numpy.copy(alldata_3DAr[j_estQ,:,thisRow,thisCol][map2fit])
    data2fit_Y= numpy.copy(alldata_3DAr[j_ADU,:,thisRow,thisCol][map2fit])
    del map2fit
    # prep to fit: exclude nan
    map2fit= ~numpy.isnan(data2fit_Y)
    data2fit_X= numpy.copy(data2fit_X[map2fit])
    data2fit_Y= numpy.copy(data2fit_Y[map2fit])
    del map2fit
    # fit: if >= fit_minNpoints
    if len(data2fit_X)>=fit_minNpoints:
        (fit_slope,fit_offset)= APy3_FITfuns.linear_fit(data2fit_X,data2fit_Y)
        fit_R2= APy3_FITfuns.linear_fit_R2(data2fit_X,data2fit_Y)
        if (fit_R2<fit_minR2)&verboseFlag: APy3_GENfuns.printcol("({2},{3}): R2={0} < {1}".format(fit_R2,fit_minR2,thisRow,thisCol),'orange')
        else:
            # if R2>=fit_minR2, find fullwell
            fittedX= numpy.copy(alldata_3DAr[j_estQ,:,thisRow,thisCol])
            fittedY= APy3_FITfuns.linear_fun(fittedX, fit_slope,fit_offset)
            deviation=numpy.abs(fittedY-alldata_3DAr[j_ADU,:,thisRow,thisCol])
            #
            # restrict search to >=aux_maxADU/2 to avoid noise or 0s on low vals
            aux_maxADU= numpy.nanmax(alldata_3DAr[j_ADU,:,thisRow,thisCol])
            aux_validmap=alldata_3DAr[j_ADU,:,thisRow,thisCol]>=(aux_maxADU/2.0)
            fittedX=numpy.copy(fittedX[aux_validmap])
            fittedY=numpy.copy(fittedY[aux_validmap])
            deviation=numpy.copy(deviation[aux_validmap])
            del aux_validmap
            # fullwell= minQ // above deviation
            deviation=numpy.copy(deviation/fittedY)*100.0 # perc deviation
            #
            dev_above_map= deviation>fullwell_dev_perc
            if numpy.sum(dev_above_map)>0:
                Qabovedev=numpy.copy(fittedX[dev_above_map])
                fullwellQ= numpy.nanmin(Qabovedev)
                if verboseFlag: APy3_GENfuns.printcol("({2},{3}): full-well ({0}% linearity): {1}e".format(fullwell_dev_perc,fullwellQ,thisRow,thisCol),'green')
            elif verboseFlag: APy3_GENfuns.printcol("({0},{1}): no saturation".format(thisRow,thisCol),'orange') 
            #
            # save/show
            if showFlag&(~saveFlag):
                APy3_GENfuns.plot_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]','pixel output ({0},{1})'.format(thisRow,thisCol))
                APy3_GENfuns.plot_1D(fittedX,deviation, 'collected charge [e]','deviation due to saturation [%]','deviation ({0},{1})'.format(thisRow,thisCol))
                APy3_GENfuns.showIt()
            if saveFlag:
                auxTitle= 'pixel output ({0},{1})'.format(thisRow,thisCol)
                png_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]',auxTitle, saveFolder+auxTitle)
                auxTitle= 'deviation ({0},{1})'.format(thisRow,thisCol)
                png_1D(fittedX,deviation, 'collected charge [e]','deviation due to saturation [%]','deviation ({0},{1})'.format(thisRow,thisCol))
    #
    elif verboseFlag: APy3_GENfuns.printcol("({0},{1}): too few point to fit".format(thisRow,thisCol),'orange')
    #
    return fullwellQ

#---
#
#%% defaults for GUI window
#
'''
######### BSI04, T-20, dmuxSELHigh, biasBSI04_04, fixGn0,PGA666 ###############
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGA666/fitCollCharge/'
dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGA666_estQ_meta.dat'
...
'''
#
'''
###################### BSI04, T-20, dmuxSELHigh, biasBSI04_04, fixGn0, PGABBB#############
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/fitCollCharge/'
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_estQ_meta.dat'
...
'''
#
'''
###################### BSI04, T-20, dmuxSELHigh, biasBSI04_04, fixGn1, PGABBB#############
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn1_PGABBB/fitCollCharge/'
dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn1_PGABBB_estQ_meta.dat'
...
'''
#
'''
###################### BSI04, T-20, dmuxSELHigh, biasBSI04_04, fixGn2, PGABBB#############
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn2_PGABBB/fitCollCharge/'
dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn2_PGABBB_estQ_meta.dat'
...
'''
#
'''
##### BSI04, T-20, dmuxSELHigh, biasBSI04_04, LatOvlw Gn2, PGABBB  ####
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/fitCollCharge/'
dflt_metaFileName= dflt_folder_data2process+'2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_LatOvfl_Gn2_OD12_PGABBB_estQ_meta.dat' 
dflt_ADU_folder=dflt_folder_data2process
dflt_estQ_folder=dflt_folder_data2process
dflt_alternPed_file= 'NONE'
dflt_fitFlag='Y'; #dflt_fitFlag='N'
dflt_fit_maxADU=0.9 # -10% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=5
#
dflt_fullwell_dev_perc=2
#
dflt_Rows2proc='Interactive'  
dflt_Cols2proc='Interactive' 
dflt_Rows2proc=':'
dflt_Cols2proc='350:1100'
#
dflt_showFlag='Y'; #dflt_showFlag='N'
dflt_saveFolder='/home/marras/auximg/'; #dflt_saveFolder='NONE'
#
dflt_highMemFlag='Y' 
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'; dflt_verboseFlag='N'
'''
#
#'''
##### BSI04, T-20, dmuxSELHigh, biasBSI04_05, LatOvlw Gn2, PGA6BB ####
dflt_folder_data2process= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/fitCollCharge/"
#
# estQ filenames <tab> ADU filenanes
dflt_metaFileName= dflt_folder_data2process+"2020.05.28_BSI04_Tm20_dmuxSELHi_biasBSI04_05_LatOvfl_Gn2_OD12_PGA6BB_estQvsADU_meta.dat"
dflt_ADU_folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/avg_xGn/"
dflt_estQ_folder="/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/fitCollCharge/"
dflt_alternPed_file= 'NONE'
dflt_fitFlag='Y'; #dflt_fitFlag='N'
dflt_fit_maxADU=0.9 # -10% of max
dflt_fit_minR2=0.9
dflt_fit_minNpoints=5
#
dflt_fullwell_dev_perc=2
#
dflt_Rows2proc='Interactive'
dflt_Cols2proc='Interactive'
dflt_Rows2proc=':'
dflt_Cols2proc=':'
#
dflt_showFlag='Y'; #dflt_showFlag='N'
dflt_saveFolder='/home/marras/auximg/'; #dflt_saveFolder='NONE'
#
dflt_highMemFlag='Y'
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'; dflt_verboseFlag='N'
#'''
#
#---
#%% pack arguments for GUI window
GUIwin_arguments= []
#
GUIwin_arguments+= ['metadata filePath (2 columns: estQ filename <tab> ADU filename)'] 
GUIwin_arguments+= [dflt_metaFileName] 
#
GUIwin_arguments+= ['ADU files in from folder']
GUIwin_arguments+= [dflt_ADU_folder]
GUIwin_arguments+= ['estQ files in from folder']
GUIwin_arguments+= [dflt_estQ_folder]
#
GUIwin_arguments+= ['PedestalADU file [NONE not to use]'] 
GUIwin_arguments+= [dflt_alternPed_file]
#
GUIwin_arguments+= ['process data: in Rows [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Rows2proc]
GUIwin_arguments+= ['process data: in columns [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
#
GUIwin_arguments+= ['fit: (to avoid saturation): use up to x of the max ADU [between 0 and 1]']
GUIwin_arguments+= [dflt_fit_maxADU]
GUIwin_arguments+= ['fit (to find fullwell): R2 at least?']
GUIwin_arguments+= [dflt_fit_minR2]
GUIwin_arguments+= ['fit (to find fullwell): at least on how many points?']
GUIwin_arguments+= [dflt_fit_minNpoints]
GUIwin_arguments+= ['fullwell: when the data deviate from fit by x%']
GUIwin_arguments+= [dflt_fullwell_dev_perc]
#
GUIwin_arguments+= ['show results? [Y/N]']
GUIwin_arguments+= [dflt_showFlag] 
GUIwin_arguments+= ['save to folder instead of showing [NONE not to]']
GUIwin_arguments+= [dflt_saveFolder] 

GUIwin_arguments+= ['high memory usage? [Y/N]']
GUIwin_arguments+= [str(dflt_highMemFlag)] 
GUIwin_arguments+= ['clean memory when possible? [Y/N]']
GUIwin_arguments+= [str(dflt_cleanMemFlag)] 
GUIwin_arguments+= ['verbose? [Y/N]']
GUIwin_arguments+= [str(dflt_verboseFlag)]
# ---
#
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
#
metaFileName= dataFromUser[i_param]; i_param+=1
#
ADU_folder= dataFromUser[i_param]; i_param+=1
estQ_folder= dataFromUser[i_param]; i_param+=1
#
#multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
alternPed_file= dataFromUser[i_param]; i_param+=1;
if alternPed_file in APy3_GENfuns.NOlist: alternPed_flag=False
else: alternPed_flag=True
#
Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if ( (Rows2proc_mtlb in INTERACTLVElist) | (Cols2proc_mtlb in INTERACTLVElist) ):
    interactiveShowFlag=True
    Rows2proc_mtlb= 'Interactive'; Cols2proc_mtlb= 'Interactive'
    Rows2proc=numpy.arange(NRow); Cols2proc=numpy.arange(NCol)
    Rows2proc=numpy.arange(0); Cols2proc=numpy.arange(0)
else:
    interactiveShowFlag=False
    Rows2proc= APy3_P2Mfuns.matlabRow(Rows2proc_mtlb)
    Cols2proc= APy3_P2Mfuns.matlabCol(Cols2proc_mtlb)
#
fit_maxADU=float(dataFromUser[i_param]); i_param+=1
fit_minR2=float(dataFromUser[i_param]); i_param+=1
fit_minNpoints=int(dataFromUser[i_param]); i_param+=1
fullwell_dev_perc= float(dataFromUser[i_param]); i_param+=1
#
showFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
saveFolder=dataFromUser[i_param]; i_param+=1; 
if saveFolder in APy3_GENfuns.NOlist: saveFlag=False
else: saveFlag=True

highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#%% what's up doc
if True:
    APy3_GENfuns.printcol('will use index file: {0}'.format(metaFileName),'blue')
    APy3_GENfuns.printcol('  ADU files from: {0}'.format(ADU_folder),'blue')
    APy3_GENfuns.printcol('  estQ files from: {0}'.format(estQ_folder),'blue')
    if interactiveShowFlag: APy3_GENfuns.printcol('will elaborate interactively','blue')
    else: APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}'.format(Cols2proc_mtlb,Rows2proc_mtlb),'blue')
    if alternPed_flag: APy3_GENfuns.printcol('will use as pedestal: {0} '.format(alternPed_file),'blue')
    APy3_GENfuns.printcol('to find full-well will fit ADU<={0} of max'.format(fit_maxADU),'blue')
    APy3_GENfuns.printcol('  will considerate an acceptable fit if R2>={0}, Npoints>={1}'.format(fit_minR2,fit_minNpoints),'blue')
    APy3_GENfuns.printcol('  will eval ful-well as the point where the curve deviates from fit by {0}%'.format(fullwell_dev_perc),'blue')
    if showFlag: APy3_GENfuns.printcol('will plot results','blue')
    if saveFlag: APy3_GENfuns.printcol('will save results in {0} (as .png)'.format(saveFolder),'blue')
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')


#%% read pedestal file
PedestalADU= numpy.zeros((NRow,NCol))
if alternPed_flag: 
    APy3_GENfuns.printcol("reading Pedestal file",'blue')
    PedestalADU= read_warn_1xh5(alternPed_file, '/data/data')
else: PedestalADU= numpy.zeros((NRow,NCol))

#---
#%% read metadata file
APy3_GENfuns.printcol("reading metadata file",'blue')
if APy3_GENfuns.notFound(metaFileName): APy3_GENfuns.printErr("not found: "+metaFileName)
fileList_all= APy3_GENfuns.read_tst(metaFileName)
(NSets,N2)= numpy.array(fileList_all).shape
if N2!=2: APy3_GENfuns.printErr("metafile: {0} columns".format(N2))
elif verboseFlag: APy3_GENfuns.printcol("{0} Sets in metafile".format(NSets),'green')

#---
#%% read data files
APy3_GENfuns.printcol("reading avg files",'blue')
alldata_3DAr= APy3_GENfuns.numpy_NaNs((2, NSets, NRow,NCol)) #estQ/ADU, Nsets, NRow,NCol
j_estQ=0
j_ADU=1
for iSet in range(NSets):
    alldata_3DAr[j_estQ,iSet,:,:]= read_warn_1xh5(estQ_folder +fileList_all[iSet][j_estQ], '/data/data')
    alldata_3DAr[j_ADU, iSet,:,:]= read_warn_1xh5(ADU_folder  +fileList_all[iSet][j_ADU],  '/data/data') - PedestalADU
    APy3_GENfuns.dot_every10th(iSet,NSets)
#
#---
#% process ramps, non interactive
if (interactiveShowFlag==False): 
    APy3_GENfuns.printcol("processing ramps",'blue')
    fullwellQ_2DAr= APy3_GENfuns.numpy_NaNs((NRow,NCol))
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            fullwellQ_2DAr[thisRow,thisCol]= aux_fullwell(alldata_3DAr, thisRow,thisCol,
                 fit_maxADU,fit_minNpoints,fit_minR2,fullwell_dev_perc,
                 False,False,saveFolder,verboseFlag)
        if (~verboseFlag): APy3_GENfuns.printcol("  row {0} done".format(thisRow),'green')
    fullwell_avg= numpy.nanmean(fullwellQ_2DAr.flatten())
    fullwell_std= numpy.nanstd(fullwellQ_2DAr.flatten()) 
    auxNpix= numpy.sum(~numpy.isnan(fullwellQ_2DAr.flatten()))
    APy3_GENfuns.printcol("full-well in ROI({0},{1})= {2}e +/- {3}e on {4}pixels".format(Rows2proc_mtlb,Cols2proc_mtlb,fullwell_avg,fullwell_std,auxNpix),'green')
    #
    if (showFlag & (~saveFlag)):
        APy3_GENfuns.plot_2D_all(fullwellQ_2DAr,False, 'col','row','full well [e]', True)
        APy3_GENfuns.plot_histo1D(aux2histo(fullwellQ_2DAr.flatten()), 100, False, 'full well [e]','pixels','full well({0},{1})'.format(Rows2proc_mtlb,Cols2proc_mtlb))
        APy3_GENfuns.showIt()
    elif (saveFlag):
         png_2D_all(fullwellQ_2DAr,False, 'col','row','full well [e]', True,saveFolder+'fullwell_2D.png')
         APy3_GENfuns.printcol('saved image: {0}'.format(saveFolder+'fullwell_2D.png'),'green')
         png_histo1D(aux2histo(fullwellQ_2DAr.flatten()), 100, False, 'full well [e]','pixels','full well({0},{1})'.format(Rows2proc_mtlb,Cols2proc_mtlb), saveFolder+'fullwell({0},{1})_1Dhisto.png'.format(Rows2proc_mtlb,Cols2proc_mtlb) )
         #
         APy3_GENfuns.printcol('saved images in {0}'.format(saveFolder),'green')
         #APy3_GENfuns.write_1xh5(saveFolder+'fullwell_2D.h5', fullwellQ_2DAr,'/data/data')
         #APy3_GENfuns.printcol('saved data: {0}'.format(saveFolder+'fullwell_2D.h5'),'green')
else:
    #---
    #% save/show ramps, interactive 
    APy3_GENfuns.printcol("interactively processing ramps",'blue')
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("[P]ocess ramp /  [Q]uit",'green')
    nextstep= input()
    while (nextstep not in ['q','Q']):
        #
        if (nextstep in ['p','P']):
            APy3_GENfuns.printcol("process pixel: Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("process pixel: Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            APy3_GENfuns.printcol("will process ({0},{1})".format(thisRow,thisCol),'green')
            #

            aux_fullwell(alldata_3DAr, thisRow,thisCol,
                 fit_maxADU,fit_minNpoints,fit_minR2,fullwell_dev_perc,
                 showFlag,saveFlag,saveFolder,True)
        #
        APy3_GENfuns.printcol("[P]rocess ramp /  [Q]uit",'green')
        nextstep= input()
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




