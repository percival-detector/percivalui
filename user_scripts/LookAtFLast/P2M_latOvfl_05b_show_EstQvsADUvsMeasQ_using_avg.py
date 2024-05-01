# -*- coding: utf-8 -*-
"""
set .h5 of estQ, measQ, avgADU => plot/save (.png), extract (.csv,.h5)

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
interactiveGUIflag=True; #interactiveGUIflag=False
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

#---
#
#%% defaults for GUI window
#
'''
#### BSI04, T-20, dmuxSELHigh, biasBSI04_05, PGAB ####
dflt_estQ_folder=  "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_3of7ADC_biasBSI04_05_PGA6BB/fitCollCharge/"
dflt_measQ_folder= dflt_estQ_folder
dflt_ADU_folder=   dflt_estQ_folder + "../avg_xGn/"

dflt_estQ_suffixes=  ["_Gn0_ADU_CDS_avg_estCharge.h5", "_Gn1_ADU_Smpl_avg_estCharge.h5", "_Gn2_ADU_Smpl_avg_estCharge.h5"]
dflt_measQ_suffixes= ["_Gn0_ADU_CDS_avg_measCharge.h5","_Gn1_ADU_Smpl_avg_measCharge.h5","_Gn2_ADU_Smpl_avg_measCharge.h5"]
dflt_ADU_suffixes=   ["_Gn0_ADU_CDS_avg.h5",           "_Gn1_ADU_Smpl_avg.h5",           "_Gn2_ADU_Smpl_avg.h5"]

#dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal_gapsAvg.h5"
dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5"
dflt_alternPed_file='NONE'

dflt_Rows2proc='500:502'  
dflt_Cols2proc='500:502' 
#dflt_Rows2proc='Interactive'  
#dflt_Cols2proc='Interactive' 
#
dflt_saveFolder='/home/marras/auximg/'
#dflt_saveFolder='NONE
#
dflt_highMemFlag='Y' 
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
#'''
#
#'''
#### BSI04, T-20, 7/7, biasBSI04.05, PGA6BB ####
dflt_estQ_folder=  "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/fitCollCharge/"
dflt_measQ_folder= dflt_estQ_folder
dflt_ADU_folder=   dflt_estQ_folder + "../avg_xGn/"

dflt_estQ_suffixes=  ["_Gn0_ADU_CDS_avg_estCharge.h5", "_Gn1_ADU_Smpl_avg_estCharge.h5", "_Gn2_ADU_Smpl_avg_estCharge.h5"]
dflt_measQ_suffixes= ["_Gn0_ADU_CDS_avg_measCharge.h5","_Gn1_ADU_Smpl_avg_measCharge.h5","_Gn2_ADU_Smpl_avg_measCharge.h5"]
dflt_ADU_suffixes=   ["_Gn0_ADU_CDS_avg.h5",           "_Gn1_ADU_Smpl_avg.h5",           "_Gn2_ADU_Smpl_avg.h5"]

dflt_multiGnCal_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/../LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"
dflt_alternPed_file='NONE'

dflt_Rows2proc='700:704'  
dflt_Cols2proc='700:700' 
dflt_Rows2proc='Interactive'  ; dflt_Cols2proc='Interactive' 
#
dflt_saveFolder='/home/marras/auximg/'
dflt_saveFolder='NONE'
#
dflt_highMemFlag='Y' 
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='N'
#'''
#
#---
if interactiveGUIflag:
    #%% pack arguments for GUI window
    GUIwin_arguments= []
    #
    GUIwin_arguments+= ['estimated Q: folder'] 
    GUIwin_arguments+= [dflt_estQ_folder] 
    GUIwin_arguments+= ['estimated Q: Gn0,1,2 suffixes'] 
    GUIwin_arguments+= [str(dflt_estQ_suffixes)] 
    #
    GUIwin_arguments+= ['measured Q folder'] 
    GUIwin_arguments+= [dflt_measQ_folder] 
    GUIwin_arguments+= ['measured Q: Gn0,1,2 suffixes'] 
    GUIwin_arguments+= [str(dflt_measQ_suffixes)] 
    #
    GUIwin_arguments+= ['measured ADU folder'] 
    GUIwin_arguments+= [dflt_ADU_folder]
    GUIwin_arguments+= ['ADU: Gn0,1,2 suffixes'] 
    GUIwin_arguments+= [str(dflt_ADU_suffixes)] 
    #
    GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file']
    GUIwin_arguments+= [dflt_multiGnCal_file]
    GUIwin_arguments+= ['alternate PedestalADU for Gn0: file [NONE not to use]']
    GUIwin_arguments+= [dflt_alternPed_file]
    #
    GUIwin_arguments+= ['process data: in Rows [from:to / Interactive]'] 
    GUIwin_arguments+= [dflt_Rows2proc]
    GUIwin_arguments+= ['process data: in columns [from:to / Interactive]'] 
    GUIwin_arguments+= [dflt_Cols2proc] 
    #
    GUIwin_arguments+= ['save to folder instead of showing [NONE not to]']
    GUIwin_arguments+= [dflt_saveFolder] 
    #
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
    estQ_folder= dataFromUser[i_param]; i_param+=1
    estQ_suffixList=  APy3_GENfuns.str2list(dataFromUser[i_param]); i_param+=1
    measQ_folder= dataFromUser[i_param]; i_param+=1
    measQ_suffixList= APy3_GENfuns.str2list(dataFromUser[i_param]); i_param+=1
    ADU_folder= dataFromUser[i_param]; i_param+=1
    ADU_suffixList=   APy3_GENfuns.str2list(dataFromUser[i_param]); i_param+=1
    #
    multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
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
    saveFolder=dataFromUser[i_param]; i_param+=1; 
    if saveFolder in APy3_GENfuns.NOlist: saveFlag=False
    else: saveFlag=True
    #
    highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
    #---
else:
    # skip the interactive GUI
    estQ_folder= dflt_estQ_folder
    estQ_suffixList= APy3_GENfuns.str2list(str(dflt_estQ_suffixes))
    measQ_folder= dflt_measQ_folder
    measQ_suffixList= APy3_GENfuns.str2list(str(dflt_measQ_suffixes))
    ADU_folder= dflt_ADU_folder
    ADU_suffixList= APy3_GENfuns.str2list(str(dflt_ADU_suffixes))
    #
    multiGnCal_file=dflt_multiGnCal_file
    alternPed_file= dflt_alternPed_file
    if alternPed_file in APy3_GENfuns.NOlist: alternPed_flag=False
    else: alternPed_flag=True
    #
    Rows2proc_mtlb= dflt_Rows2proc
    Cols2proc_mtlb= dflt_Cols2proc
    if (Rows2proc_mtlb in INTERACTLVElist) or  (Cols2proc_mtlb in INTERACTLVElist):
        interactiveShowFlag=True
        RowsRows2proc_mtlb= 'Interactive'; Cols2proc_mtlb= 'Interactive'
        Rows2proc=numpy.arange(NRow); Cols2proc=numpy.arange(NCol)
    else:
        interactiveShowFlag=False
        Rows2proc= APy3_P2Mfuns.matlabRow(Rows2proc_mtlb)
        Cols2proc= APy3_P2Mfuns.matlabCol(Cols2proc_mtlb)
    #
    saveFolder= dflt_saveFolder
    if saveFolder in APy3_GENfuns.NOlist: saveFlag=False
    else: saveFlag=True
    #
    highMemFlag=APy3_GENfuns.isitYes(str(dflt_highMemFlag))
    cleanMemFlag=APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag=APy3_GENfuns.isitYes(str(dflt_verboseFlag))

# ---

#%% what's up doc
if True:
    APy3_GENfuns.printcol('will process estQ data from '+estQ_folder,'blue')
    for jGn in range(3): 
        APy3_GENfuns.printcol('  Gn{0}: *{1}'.format(jGn,estQ_suffixList[jGn]),'blue')

    APy3_GENfuns.printcol('will process measQ data from '+measQ_folder,'blue')
    for jGn in range(3): 
        APy3_GENfuns.printcol('  Gn{0}: *{1}'.format(jGn,measQ_suffixList[jGn]),'blue')

    APy3_GENfuns.printcol('will process ADU data from '+ADU_folder,'blue')
    for jGn in range(3): 
        APy3_GENfuns.printcol('  Gn{0}: *{1}'.format(jGn,ADU_suffixList[jGn]),'blue')

    APy3_GENfuns.printcol('will elaborate ({0},{1})'.format(Rows2proc_mtlb,Cols2proc_mtlb),'blue')
    if alternPed_flag: APy3_GENfuns.printcol('will use as pedestal: {0} '.format(alternPed_file),'blue')
    if saveFlag: APy3_GENfuns.printcol('will save ramps in {0} (as .png)'.format(saveFolder),'blue')
    else: APy3_GENfuns.printcol('will plot ramps','blue')
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    if verboseFlag: APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#
#%% read ADU pedestals
APy3_GENfuns.printcol("reading ADU Pedestals",'blue')
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
if alternPed_flag: 
    PedestalADU_multiGn[0,:,:]= read_warn_1xh5(alternPed_file, '/data/data')
#
#%% list files
estQ_Gn0_fileList= APy3_GENfuns.list_files(estQ_folder, '*', estQ_suffixList[0])
estQ_Gn1_fileList= APy3_GENfuns.list_files(estQ_folder, '*', estQ_suffixList[1])
estQ_Gn2_fileList= APy3_GENfuns.list_files(estQ_folder, '*', estQ_suffixList[2])
#for iaux in range(len(estQ_Gn0_List)): print("{0},{1},{2}".format(estQ_Gn0_List[iaux],estQ_Gn1_List[iaux],estQ_Gn2_List[iaux]))
NSets= len(estQ_Gn0_fileList)

#%% read data files
APy3_GENfuns.printcol("reading avg files",'blue')
estQdata_4DAr=   APy3_GENfuns.numpy_NaNs((3, NSets, NRow,NCol)) #Gn, Nsets, NRow,NCol
measQdata_4DAr= APy3_GENfuns.numpy_NaNs((3, NSets, NRow,NCol)) #Gn, Nsets, NRow,NCol
ADUdata_4DAr=   APy3_GENfuns.numpy_NaNs((3, NSets, NRow,NCol)) #Gn, Nsets, NRow,NCol
#
for iSet in range(NSets):
    estQdata_4DAr[0,iSet,:,:]= read_warn_1xh5(estQ_folder+estQ_Gn0_fileList[iSet], '/data/data')
    lensuffix=len(estQ_suffixList[0])
    measQdata_4DAr[0,iSet,:,:]= read_warn_1xh5(measQ_folder+ estQ_Gn0_fileList[iSet][:-lensuffix]+measQ_suffixList[0], '/data/data')
    ADUdata_4DAr[0,iSet,:,:]   = read_warn_1xh5(ADU_folder+ estQ_Gn0_fileList[iSet][:-lensuffix]+ADU_suffixList[0], '/data/data')
    #
    estQdata_4DAr[1,iSet,:,:]= read_warn_1xh5(estQ_folder+estQ_Gn1_fileList[iSet], '/data/data')
    lensuffix=len(estQ_suffixList[1])
    measQdata_4DAr[1,iSet,:,:]= read_warn_1xh5(measQ_folder+ estQ_Gn1_fileList[iSet][:-lensuffix]+measQ_suffixList[1], '/data/data')
    ADUdata_4DAr[1,iSet,:,:]   = read_warn_1xh5(ADU_folder+ estQ_Gn1_fileList[iSet][:-lensuffix]+ADU_suffixList[1], '/data/data')
    #
    estQdata_4DAr[2,iSet,:,:]= read_warn_1xh5(estQ_folder+estQ_Gn2_fileList[iSet], '/data/data')
    lensuffix=len(estQ_suffixList[2])
    measQdata_4DAr[2,iSet,:,:]= read_warn_1xh5(measQ_folder+ estQ_Gn2_fileList[iSet][:-lensuffix]+measQ_suffixList[2], '/data/data')
    ADUdata_4DAr[2,iSet,:,:]   = read_warn_1xh5(ADU_folder+ estQ_Gn2_fileList[iSet][:-lensuffix]+ADU_suffixList[2], '/data/data')
    #
    APy3_GENfuns.dot()
APy3_GENfuns.printcol(" ",'blue')


#---
#% save/show ramps, non interactive
if (interactiveShowFlag==False): 
    APy3_GENfuns.printcol("showing/saving ramps",'blue')
    for thisRow in Rows2proc:
        for thisCol in Cols2proc:
            if (saveFlag==False):
                APy3_GENfuns.plot_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],ADUdata_4DAr[0,:,thisRow,thisCol]-PedestalADU_multiGn[0,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],ADUdata_4DAr[1,:,thisRow,thisCol]-PedestalADU_multiGn[1,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],ADUdata_4DAr[2,:,thisRow,thisCol]-PedestalADU_multiGn[2,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [ADU]', 'pixel output ({0},{1})'.format(thisRow,thisCol),False,saveFolder)
                APy3_GENfuns.plot_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],measQdata_4DAr[0,:,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],measQdata_4DAr[1,:,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],measQdata_4DAr[2,:,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [e]', 'pixel output ({0},{1})'.format(thisRow,thisCol),True)
                APy3_GENfuns.showIt()
            #
            else: 
                auxFileName= 'ADUxGnvsEstQ_pix({0},{1})_1Dlin'.format(thisRow,thisCol)
                APy3_GENfuns.png_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],ADUdata_4DAr[0,:,thisRow,thisCol]-PedestalADU_multiGn[0,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],ADUdata_4DAr[1,:,thisRow,thisCol]-PedestalADU_multiGn[1,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],ADUdata_4DAr[2,:,thisRow,thisCol]-PedestalADU_multiGn[2,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [ADU]', 'pixel output ({0},{1})'.format(thisRow,thisCol),False,saveFolder+auxFileName) 
                #
                auxFileName= 'MeasQxGnvsEstQ_pix({0},{1})_1Dlog'.format(thisRow,thisCol)
                APy3_GENfuns.png_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],measQdata_4DAr[0,:,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],measQdata_4DAr[1,:,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],measQdata_4DAr[2,:,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [e]', 'pixel output ({0},{1})'.format(thisRow,thisCol),True,saveFolder+auxFileName)
                #
                APy3_GENfuns.printcol("ramp images saved as png in {0}".format(saveFolder),'green')
                #
                for jGn in range(3):
                    APy3_GENfuns.write_csv(saveFolder+'pix({0},{1})_Gn{2}_estQ.csv'.format(thisRow,thisCol,jGn), estQdata_4DAr[jGn,:,thisRow,thisCol])
                    APy3_GENfuns.write_csv(saveFolder+'pix({0},{1})_Gn{2}_measQ.csv'.format(thisRow,thisCol,jGn), measQdata_4DAr[jGn,:,thisRow,thisCol])
                    APy3_GENfuns.write_csv(saveFolder+'pix({0},{1})_Gn{2}_ADU.csv'.format(thisRow,thisCol,jGn), ADUdata_4DAr[jGn,:,thisRow,thisCol]-PedestalADU_multiGn[jGn,thisRow,thisCol])
                APy3_GENfuns.printcol("ramp data saved as csv in {0}".format(saveFolder),'green')
#---
#
elif (interactiveShowFlag==True): 
    APy3_GENfuns.printcol("interactively showing/saving ramps",'blue')
    thisRow=0; thisCol=0
    APy3_GENfuns.printcol("interactivly showing ramps",'blue')
    APy3_GENfuns.printcol("[P]lot ramp / export to [C]sv /  [Q]uit",'green')
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
            #
            if (saveFlag==False):
                APy3_GENfuns.plot_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],ADUdata_4DAr[0,:,thisRow,thisCol]-PedestalADU_multiGn[0,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],ADUdata_4DAr[1,:,thisRow,thisCol]-PedestalADU_multiGn[1,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],ADUdata_4DAr[2,:,thisRow,thisCol]-PedestalADU_multiGn[2,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [ADU]', 'pixel output ({0},{1})'.format(thisRow,thisCol),False)
                APy3_GENfuns.plot_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],measQdata_4DAr[0,:,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],measQdata_4DAr[1,:,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],measQdata_4DAr[2,:,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [e]', 'pixel output ({0},{1})'.format(thisRow,thisCol),True)
                APy3_GENfuns.showIt()
            #
            else:
                auxFileName= 'ADUxGnvsEstQ_pix({0},{1})_1Dlin'.format(thisRow,thisCol)
                APy3_GENfuns.png_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],ADUdata_4DAr[0,:,thisRow,thisCol]-PedestalADU_multiGn[0,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],ADUdata_4DAr[1,:,thisRow,thisCol]-PedestalADU_multiGn[1,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],ADUdata_4DAr[2,:,thisRow,thisCol]-PedestalADU_multiGn[2,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [ADU]', 'pixel output ({0},{1})'.format(thisRow,thisCol),False,saveFolder+auxFileName)
                #
                auxFileName= 'MeasQxGnvsEstQ_pix({0},{1})_1Dlog'.format(thisRow,thisCol)
                APy3_GENfuns.png_1Dx3_samecanva(estQdata_4DAr[0,:,thisRow,thisCol],measQdata_4DAr[0,:,thisRow,thisCol],'very-high gain', estQdata_4DAr[1,:,thisRow,thisCol],measQdata_4DAr[1,:,thisRow,thisCol],'medium gain', estQdata_4DAr[2,:,thisRow,thisCol],measQdata_4DAr[2,:,thisRow,thisCol],'low gain', 'collected charge [e]','pixel output [e]', 'pixel output ({0},{1})'.format(thisRow,thisCol),True,saveFolder+auxFileName)
                #
                APy3_GENfuns.printcol("ramp images saved as png in {0}".format(saveFolder),'green')
        #
        elif (nextstep in ['c','C']):
            APy3_GENfuns.printcol("export: pixel Row? [default is {0}]".format(thisRow),'green')
            thisRow_str= input()
            if len(thisRow_str)>0: thisRow=int(thisRow_str)
            APy3_GENfuns.printcol("export: pixel Col? [default is {0}]".format(thisCol),'green')
            thisCol_str= input()
            if len(thisCol_str)>0: thisCol=int(thisCol_str)
            #
            csvFolder= saveFolder
            APy3_GENfuns.printcol("export: to folder? [default is {0}]".format(csvFolder),'green')
            csvFolder_in=input()
            if len(csvFolder_in)>0: csvFolder= csvFolder_in
            APy3_GENfuns.printcol("will export to folder {0}".format(csvFolder),'green')
            #
            for jGn in range(3):
                APy3_GENfuns.write_csv(csvFolder+'pix({0},{1})_Gn{2}_estQ.csv'.format(thisRow,thisCol,jGn), estQdata_4DAr[jGn,:,thisRow,thisCol])
                APy3_GENfuns.write_csv(csvFolder+'pix({0},{1})_Gn{2}_measQ.csv'.format(thisRow,thisCol,jGn), measQdata_4DAr[jGn,:,thisRow,thisCol])
                APy3_GENfuns.write_csv(csvFolder+'pix({0},{1})_Gn{2}_ADU.csv'.format(thisRow,thisCol,jGn), ADUdata_4DAr[jGn,:,thisRow,thisCol]-PedestalADU_multiGn[jGn,thisRow,thisCol])
            APy3_GENfuns.printcol("ramp data saved as csv in {0}".format(csvFolder),'green')
        #
        APy3_GENfuns.printcol("[P]lot ramp / export to [C]sv /  [Q]uit",'green')
        nextstep= input()
#
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




