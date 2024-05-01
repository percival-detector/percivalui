# -*- coding: utf-8 -*-
"""
set .h5 of avgADU and estQ at different int times => plot/save (.png), extract (.csv,.h5)

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
cd /home/marras/PercAuxiliaryTools/LookAtFLast
python3 ./WIP_latOvfl_05_ramps_show_ADU_Charge.py
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
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
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
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
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
    if filenamepath[-4:] in ['png','PNG']: filenamepath_out= filenamepath
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
#
#%% defaults for GUI window
#
#'''
###################### BSI04, T-20, dmuxSELHigh, biasBSI04_04, PGAB #############################################

#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGA666/fitCollCharge/'
#dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGA666_estQ_meta.dat'
#dflt_metaFileName=THIS IS MISSING!
#dflt_alternPed_file=dflt_folder_data2process + 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGA666_OD5.0_t012ms_500drk_CDS_avg.h5'

#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/fitCollCharge/'
#if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
#dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_estQ_meta.dat'
#dflt_metaFileName=THIS IS MISSING!
#dflt_alternPed_file=dflt_folder_data2process + 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn0_PGABBB_ODx.x_t012ms_500drk_CDS_avg.h5'

#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn1_PGABBB/fitCollCharge/'
#dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn1_PGABBB_estQ_meta.dat'
#dflt_metaFileName=THIS IS MISSING!
#dflt_alternPed_file=dflt_folder_data2process + 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn1_PGABBB_ODx.x_t012ms_500drk_Smpl_avg.h5'

#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn2_PGABBB/fitCollCharge/'
#dflt_metaFileName= '2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn2_PGABBB_estQ_meta.dat'
#dflt_metaFileName=THIS IS MISSING!
#dflt_alternPed_file=dflt_folder_data2process + 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_fixGn2_PGABBB_ODx.x_t012ms_500drk_Smpl_avg.h5'


dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/fitCollCharge2/'
dflt_metaFileName='2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_LatOvflw_Gn2_estQ_meta.dat' # repeat also foir Gn0, Gn1
dflt_metaFileName_measQ='2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_LatOvflw_Gn2_measQ_meta.dat'

dflt_alternPed_file='NONE'

#dflt_metaFileName='2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_LatOvflw_Gn0_estQ_meta.dat'
#dflt_alternPed_file=dflt_folder_data2process + 'BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD1.0_t012ms_100drk_Gn0_ADU_CDS_avg.h5'

#dflt_Rows2proc='603:603'  
#dflt_Cols2proc='502:502' 
dflt_Rows2proc='Interactive'  
dflt_Cols2proc='Interactive' 
#
dflt_showFlag='Y'; #dflt_showFlag='N'
dflt_saveFolder='/home/marras/auximg/'
#dflt_saveFolder='NONE
#
dflt_highMemFlag='Y' 
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'





#---
#%% pack arguments for GUI window
GUIwin_arguments= []
#
GUIwin_arguments+= ['use data from folder'] 
GUIwin_arguments+= [dflt_folder_data2process] 
#
GUIwin_arguments+= ['metadata file (2 columns: estQ filenames <tab> ADU filenanes)'] 
GUIwin_arguments+= [dflt_metaFileName] 
#
GUIwin_arguments+= ['metadata file measQ (2 columns: measQ filenames <tab> ADU filenanes)']
GUIwin_arguments+= [dflt_metaFileName_measQ]
#
GUIwin_arguments+= ['PedestalADU file [NONE not to use]'] 
GUIwin_arguments+= [dflt_alternPed_file]
#
GUIwin_arguments+= ['process data: in Rows [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Rows2proc]
GUIwin_arguments+= ['process data: in columns [from:to / Interactive]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
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
folder_data2process= dataFromUser[i_param]; i_param+=1
metaFileName= dataFromUser[i_param]; i_param+=1
metaFileName_measQ= dataFromUser[i_param]; i_param+=1
#
#multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
alternPed_file= dataFromUser[i_param]; i_param+=1;
if alternPed_file in APy3_GENfuns.NOlist: alternPed_flag=False
else: alternPed_flag=True
#
Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if (Rows2proc_mtlb in INTERACTLVElist) or  (Cols2proc_mtlb in INTERACTLVElist):
    interactiveShowFlag=True
    RowsRows2proc_mtlb= 'Interactive'; Cols2proc_mtlb= 'Interactive'
    Rows2proc=numpy.arange(NRow); Cols2proc=numpy.arange(NCol)
else:
    interactiveShowFlag=False
    Rows2proc= APy3_P2Mfuns.matlabRow(Rows2proc_mtlb)
    Cols2proc= APy3_P2Mfuns.matlabCol(Cols2proc_mtlb)
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
    APy3_GENfuns.printcol('will process data from '+folder_data2process,'blue')
    APy3_GENfuns.printcol('will use {0} as the estQ index file'.format(metaFileName),'blue')
    APy3_GENfuns.printcol('will use {0} as the measQ index file'.format(metaFileName_measQ),'blue')
    APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}'.format(Cols2proc_mtlb,Rows2proc_mtlb),'blue')
    if alternPed_flag: APy3_GENfuns.printcol('will use as pedestal: {0} '.format(alternPed_file),'blue')
    if showFlag: APy3_GENfuns.printcol('will plot ramps','blue')
    if saveFlag: APy3_GENfuns.printcol('will save ramps in {0} (as .png)'.format(saveFolder),'blue')
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
if APy3_GENfuns.notFound(folder_data2process+metaFileName): APy3_GENfuns.printErr("not found: "+folder_data2process+metaFileName)
fileList_all= APy3_GENfuns.read_tst(folder_data2process+metaFileName)
(NSets,N2)= numpy.array(fileList_all).shape
if N2!=2: APy3_GENfuns.printErr("metafile: {0} columns".format(N2))
elif verboseFlag: APy3_GENfuns.printcol("{0} Sets in metafile".format(NSets),'green')
#
if APy3_GENfuns.notFound(folder_data2process+metaFileName_measQ): APy3_GENfuns.printErr("not found: "+folder_data2process+metaFileName_measQ)
fileList_measQ_all= APy3_GENfuns.read_tst(folder_data2process+metaFileName_measQ)


#---
#%% read data files
APy3_GENfuns.printcol("reading avg files",'blue')
alldata_3DAr= APy3_GENfuns.numpy_NaNs((2, NSets, NRow,NCol)) #estQ/ADU, Nsets, NRow,NCol
measQ_3DAr= APy3_GENfuns.numpy_NaNs((NSets, NRow,NCol)) #Nsets, NRow,NCol
j_estQ=0
j_ADU=1
for iSet in range(NSets):
    alldata_3DAr[j_estQ,iSet,:,:]= read_warn_1xh5(folder_data2process+fileList_all[iSet][j_estQ], '/data/data')
    alldata_3DAr[j_ADU, iSet,:,:]= read_warn_1xh5(folder_data2process+fileList_all[iSet][j_ADU],  '/data/data') - PedestalADU
    measQ_3DAr[iSet,:,:]=read_warn_1xh5(folder_data2process+fileList_measQ_all[iSet][0], '/data/data')
    APy3_GENfuns.dot_every10th(iSet,NSets)
#---
#% save/show ramps, non interactive
if ((showFlag | saveFlag) & (~interactiveShowFlag)): 
    APy3_GENfuns.printcol("showing/saving ramps",'blue')
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            if (~saveFlag): 
                APy3_GENfuns.plot_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]','pixel output ({0},{1})'.format(thisRow,thisCol))
                APy3_GENfuns.showIt()
            if saveFlag: 
                auxTitle= 'pixel output ({0},{1})'.format(thisRow,thisCol)
                png_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]',auxTitle, saveFolder+auxTitle)
                APy3_GENfuns.printcol("ramp image saved as png: {0}".format(saveFolder+auxTitle),'green')
                #
                APy3_GENfuns.write_csv(saveFolder+auxTitle+'.csv', numpy.transpose(alldata_3DAr[:,:,thisRow,thisCol],(1,0)) ) #traspose to have data per col
                APy3_GENfuns.printcol("data exported: {0}".format(saveFolder+auxTitle+'.csv'),'green')
                APy3_GENfuns.printcol("  as 2-col csv file: estQ,ADU",'green')
                #
                APy3_GENfuns.write_2xh5(saveFolder+auxTitle+'.h5', alldata_3DAr[j_estQ,:,thisRow,thisCol],'estQ',  alldata_3DAr[j_ADU,:,thisRow,thisCol],'ADU')
                APy3_GENfuns.printcol("data exported: {0}".format(saveFolder+auxTitle+'.h5'),'green')
                APy3_GENfuns.printcol("  as 2-folders h5 file: estQ,ADU",'green')
#---
#% save/show ramps, interactive
elif ((showFlag | saveFlag) & (interactiveShowFlag)): 
    APy3_GENfuns.printcol("interactively showing/saving ramps",'blue')
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("interactivly showing ramps",'blue')
    APy3_GENfuns.printcol("[P]lot ramp / export to [C]sv/[H]df5 /  [Q]uit",'green')
    nextstep= input()
    while (nextstep not in ['q','Q']):
        #
        if (nextstep in ['p','P']):
            APy3_GENfuns.printcol("plot/save pixel: Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("plot/save pixel: Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            APy3_GENfuns.printcol("will plot/save pixel ({0},{1})".format(thisRow,thisCol),'green')
            if showFlag&(~saveFlag): 
                APy3_GENfuns.plot_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]','pixel output ({0},{1})'.format(thisRow,thisCol))
                #
                APy3_GENfuns.plot_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],measQ_3DAr[:,thisRow,thisCol], 'collected charge [e]','pixel output [e]','pixel output ({0},{1})'.format(thisRow,thisCol))
                #
                APy3_GENfuns.showIt()
            if saveFlag: 
                auxTitle= 'pixel output ({0},{1})'.format(thisRow,thisCol)
                png_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],alldata_3DAr[j_ADU,:,thisRow,thisCol], 'collected charge [e]','pixel output [ADU]',auxTitle, saveFolder+auxTitle+'ADU_vs_estQ.png')
                png_1D(alldata_3DAr[j_estQ,:,thisRow,thisCol],measQ_3DAr[:,thisRow,thisCol], 'collected charge [e]','pixel output [e]',auxTitle, saveFolder+auxTitle+'measQ_vs_estQ.png')
        #
        elif (nextstep in ['c','C','h','H']):
            APy3_GENfuns.printcol("export: pixel Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("export: pixel Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            #
            fileNamePath= saveFolder+'pixel output ({0},{1})'.format(thisRow,thisCol)
            APy3_GENfuns.printcol("export: file name? [default is {0}.csv/h5]".format(fileNamePath),'green')
            fileNamePath_str= input()
            if len(fileNamePath_str)>0: fileNamePath=fileNamePath_str
            APy3_GENfuns.printcol("will export to {2}: pixel ({0},{1})".format(thisRow,thisCol,nextstep),'green')
            APy3_GENfuns.printcol("to file: {0}".format(fileNamePath),'green')
            #
            if (nextstep in ['c','C']): 
                APy3_GENfuns.write_csv(fileNamePath+'.csv', numpy.transpose(alldata_3DAr[:,:,thisRow,thisCol],(1,0)) ) # transpose to have data per col
                APy3_GENfuns.printcol("2-col csv file:(estQ,ADU) saved: {0}".format(fileNamePath+'.csv'),'green')
                #
                APy3_GENfuns.write_csv(fileNamePath+'measQ.csv', measQ_3DAr[:,thisRow,thisCol] ) # transpose to have data per col
                APy3_GENfuns.printcol("1-col csv file (measQ) file saved {0}".format(fileNamePath+'measQ.csv'),'green')

            elif (nextstep in ['h','H']): 
                APy3_GENfuns.write_2xh5(fileNamePath+'.h5', alldata_3DAr[j_estQ,:,thisRow,thisCol],'estQ',  alldata_3DAr[j_ADU,:,thisRow,thisCol],'ADU')
                APy3_GENfuns.printcol("2-folders h5 file: (estQ,ADU) saved: {0}".format(fileNamePath+'.h5'),'green')

                APy3_GENfuns.write_1xh5(fileNamePath+'measQ.h5', measQ_3DAr[:,thisRow,thisCol] ,'/data/data')
                APy3_GENfuns.printcol("1-folder h5 file (measQ in /data/data/) file saved {0}".format(fileNamePath+'measQ.h5'),'green')
            #
        #
        APy3_GENfuns.printcol("[P]lot ramp / export to [C]sv/[H]df5 /  [Q]uit",'green')
        nextstep= input()
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




