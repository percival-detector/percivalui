# -*- coding: utf-8 -*-
"""
descrambled (DLSRaw) collections => .h5 of Gn-dependent avg (ADUcor, not PedSub) for each collection. (NO pedestal subtraction)
avg independently for each Gn (if at least enough images (>=NImgGnX) with that Gn for that pixel)

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3

python3 ./xxx.py
or:
start python
# execfile("xxx.py") # this is in python 2.7
exec(open("./xxx.py").read()); print('Python3 is horrible')
"""

#%% imports and useful constants
from APy3_auxINIT import *

numpy.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings('ignore')
#
NRow= APy3_P2Mfuns.NRow
NCol= APy3_P2Mfuns.NCol
NGn=  APy3_P2Mfuns.NGn
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
#
# ---
interactiveFlag= False; interactiveFlag= True
# ---
#
#%% defaults for GUI window
#
#'''
##### BSI04 7of7 ####
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/fixGn_BSI04_Tm20_7of7_bSI04_05_PGA6BB/drk/DLSraw/'
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_7of7ADC_biasBSI04_05_PGA6/DLSraw/'
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/DLSraw/'

dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_000_BSI04_7of7_drk/processed/BSI04_7of7_drk/aux_DLSraw_1only/'


if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_inputFileSuffix='DLSraw.h5'
#
dflt_Img2proc='10:999'
#dflt_Img2proc='10:499'
#dflt_Img2proc='10:99'
#dflt_Img2proc='10:29' #########################################
dflt_NImgGnX= 'half' #'10'#'half'
#



dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'


#dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5' ##########################



#
dflt_multiGnCal_file= 'NONE'
dflt_alternFile_Ped_Gn0_ADU= 'NONE'
#
dflt_CMAFlag='N'; #dflt_CMAFlag='Y'
dflt_cols2CMA_str = '32:63'; #cols2CMA_str = '704:735'
dflt_CDSFlag='Y'; #dflt_CDSFlag='N' #########################################
#
# avgItForGn0/1/2Flag define saveFlag
dflt_avgItForGn0Flag= True
dflt_avgItForGn1Flag= False; #dflt_avgItForGn1Flag= True ## True for multiGn #########################################
dflt_avgItForGn2Flag= False; #dflt_avgItForGn2Flag= True ## True for multiGn #########################################
dflt_stdItFlag= False; dflt_stdItFlag= True #########################################
#



dflt_outFolder= dflt_folder_data2process +'../avg_xGn/'#############################



#
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
dflt_outputFileMidfix='ADU'
#
dflt_showFlag='Y'; dflt_showFlag='N'
dflt_highMemFlag='Y'; dflt_highMemFlag='N'  ################################################
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'
#'''
#
'''
#### BSI04 3of7 ####
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_04_PGABBB/DLSraw/'
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_05_PGA6BB/DLSraw/'
#dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_04_PGABBB/DLSraw_fixGn12/'
dflt_folder_data2process= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflwExamples_BSI04_Tm20_3of7ADC_3rd/BSI04_05_PGA6BB/DLSraw_fixGn12/'

#
if dflt_folder_data2process[-1]!='/': dflt_folder_data2process+='/'
dflt_inputFileSuffix='DLSraw.h5'
#
dflt_Img2proc='10:99'
dflt_NImgGnX= 'half' #'10'#'half'
#
dflt_ADCcor_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/' + 'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= 'NONE'
dflt_alternFile_Ped_Gn0_ADU= 'NONE'
#
dflt_CMAFlag='N'; #dflt_CMAFlag='Y'
dflt_cols2CMA_str = '32:63'; #cols2CMA_str = '704:735'
dflt_CDSFlag='Y'; dflt_CDSFlag='N'####################################################################################
#
# avgItForGn0/1/2Flag define saveFlag
dflt_avgItForGn0Flag= True
dflt_avgItForGn1Flag= False; #dflt_avgItForGn1Flag= True ## True for multiGn #########################################
dflt_avgItForGn2Flag= False; #dflt_avgItForGn2Flag= True ## True for multiGn ##########################################
dflt_stdItFlag= True; dflt_stdItFlag= False; 
#
#dflt_outFolder= dflt_folder_data2process +'../avg_xGn/'
dflt_outFolder= dflt_folder_data2process +'../avg_xGn_fixGn12/' ########################################################
if dflt_outFolder[-1]!='/': dflt_outFolder+='/'
dflt_outputFileMidfix='ADU'
#
dflt_showFlag='Y'; dflt_showFlag='N'
dflt_highMemFlag='Y'; #dflt_highMemFlag='N'  
dflt_cleanMemFlag= 'Y'
dflt_verboseFlag='Y'
'''
#
'''

'''




# ---
#%% parameter loading
if interactiveFlag:
    # interactive GUI
    GUIwin_arguments= []
    GUIwin_arguments+= ['use data from folder'];           GUIwin_arguments+= [dflt_folder_data2process] 
    GUIwin_arguments+= ['ending with'];                    GUIwin_arguments+= [dflt_inputFileSuffix] 
    GUIwin_arguments+= ['process data: in Img [from:to]']; GUIwin_arguments+= [dflt_Img2proc]
    GUIwin_arguments+= ['process data: at least NImg in GnX to make a valid avg [# / half / all]']; GUIwin_arguments+= [dflt_NImgGnX]
    #
    GUIwin_arguments+= ['ADCcor 1-file'];                                         GUIwin_arguments+= [dflt_ADCcor_file] 
    GUIwin_arguments+= ['Lateral Overflow (pedestal & e/ADU for Gn0/1/2): file']; GUIwin_arguments+= [dflt_multiGnCal_file]
    GUIwin_arguments+= ['PedestalADU [Gn0] file [none not to use it]'];           GUIwin_arguments+= [dflt_alternFile_Ped_Gn0_ADU]
    #
    GUIwin_arguments+= ['CMA? [Y/N]'];                    GUIwin_arguments+= [dflt_CMAFlag] 
    GUIwin_arguments+= ['cols to use for CMA [from:to]']; GUIwin_arguments+= [dflt_cols2CMA_str] 
    GUIwin_arguments+= ['CDS for Gn=0? [Y/N]'];           GUIwin_arguments+= [dflt_CDSFlag] 
    #
    GUIwin_arguments+= ['show results? [Y/N]']; GUIwin_arguments+= [dflt_showFlag] 
    #
    GUIwin_arguments+= ['save data to files: avg for Gn0? [Y/N]']; GUIwin_arguments+= [str(dflt_avgItForGn0Flag)]
    GUIwin_arguments+= ['save data to files: avg for Gn1? [Y/N]']; GUIwin_arguments+= [str(dflt_avgItForGn1Flag)]
    GUIwin_arguments+= ['save data to files: avg for Gn2? [Y/N]']; GUIwin_arguments+= [str(dflt_avgItForGn2Flag)]
    GUIwin_arguments+= ['save data to files: std for those Gn? [Y/N]'];  GUIwin_arguments+= [str(dflt_stdItFlag)]
    # 
    GUIwin_arguments+= ['save results: to folder']; GUIwin_arguments+= [dflt_outFolder] 
    GUIwin_arguments+= ['save results: midfix'];    GUIwin_arguments+= [dflt_outputFileMidfix] 
    #
    GUIwin_arguments+= ['high memory usage? [Y/N]'];          GUIwin_arguments+= [str(dflt_highMemFlag)] 
    GUIwin_arguments+= ['clean memory when possible? [Y/N]']; GUIwin_arguments+= [str(dflt_cleanMemFlag)] 
    GUIwin_arguments+= ['verbose? [Y/N]'];                    GUIwin_arguments+= [str(dflt_verboseFlag)] 
    # ---
    #
    GUIwin_arguments=tuple(GUIwin_arguments)
    dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
    #
    i_param=0
    folder_data2process= dataFromUser[i_param]; i_param+=1
    inputFileSuffix=     dataFromUser[i_param]; i_param+=1 
    Img2proc_mtlb=       dataFromUser[i_param]; i_param+=1
    NImgGnX_str=         dataFromUser[i_param]; i_param+=1
    #
    ADCcor_file=            dataFromUser[i_param]; i_param+=1
    multiGnCal_file=        dataFromUser[i_param]; i_param+=1
    alternFile_Ped_Gn0_ADU= dataFromUser[i_param]; i_param+=1
    #
    CMAFlag=      APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1 
    cols2CMA_str= dataFromUser[i_param]; i_param+=1

    CDSFlag=      APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
    showFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
    avgItForGn0Flag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    avgItForGn1Flag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    avgItForGn2Flag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    stdItFlag=       APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    # 
    outFolder=   dataFromUser[i_param]; i_param+=1 
    outputFileMidfix= dataFromUser[i_param]; i_param+=1  
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    cleanMemFlag= APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    verboseFlag=  APy3_GENfuns.isitYes(str(dataFromUser[i_param])); i_param+=1
    #
else:
    folder_data2process= dflt_folder_data2process 
    inputFileSuffix=     dflt_inputFileSuffix 
    Img2proc_mtlb=       dflt_Img2proc
    NImgGnX_str=         dflt_NImgGnX
    #
    ADCcor_file=            dflt_ADCcor_file
    multiGnCal_file=        dflt_multiGnCal_file
    alternFile_Ped_Gn0_ADU= dflt_alternFile_Ped_Gn0_ADU
    #
    CMAFlag=      APy3_GENfuns.isitYes(str(dflt_CMAFlag)) 
    cols2CMA_str= dflt_cols2CMA_str
    CDSFlag=      APy3_GENfuns.isitYes(str(dflt_CDSFlag))
    #
    showFlag= APy3_GENfuns.isitYes(str(dflt_showFlag))
    #
    avgItForGn0Flag= APy3_GENfuns.isitYes(str(dflt_avgItForGn0Flag))
    avgItForGn1Flag= APy3_GENfuns.isitYes(str(dflt_avgItForGn1Flag))
    avgItForGn2Flag= APy3_GENfuns.isitYes(str(dflt_avgItForGn2Flag))
    stdItFlag=       APy3_GENfuns.isitYes(str(dflt_stdItFlag))
    # 
    outFolder=        dflt_outFolder 
    outputFileMidfix= dflt_outputFileMidfix
    #
    highMemFlag=  APy3_GENfuns.isitYes(str(dflt_highMemFlag)) 
    cleanMemFlag= APy3_GENfuns.isitYes(str(dflt_cleanMemFlag))
    verboseFlag=  APy3_GENfuns.isitYes(str(dflt_verboseFlag))
# ---
Img2proc= APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1]
#
if NImgGnX_str in APy3_GENfuns.ALLlist: NImgGnX= len(Img2proc)
elif NImgGnX_str in ['half','Half','HALF','1/2']: NImgGnX= len(Img2proc)//2
else: NImgGnX= int(NImgGnX_str)
#
if multiGnCal_file in APy3_GENfuns.NOlist: ADU2eFlag= False
else: ADU2eFlag= True
if alternFile_Ped_Gn0_ADU in APy3_GENfuns.NOlist: alternPed= False
else: alternPed= True
if CMAFlag: cols2CMA= APy3_GENfuns.matlabLike_range(cols2CMA_str)
else:       cols2CMA=[]
#
avgItForGn= numpy.zeros(3).astype(bool)
avgItForGn[0]= avgItForGn0Flag
avgItForGn[1]= avgItForGn1Flag
avgItForGn[2]= avgItForGn2Flag
saveFlag= avgItForGn[0]|avgItForGn[1]|avgItForGn[2]
if outFolder in APy3_GENfuns.NOlist: saveFlag= False
#
# ---
# what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will process data from {0}...{1}'.format(folder_data2process,inputFileSuffix),'blue')
    APy3_GENfuns.printcol('will elaborate Img{0}'.format(Img2proc_mtlb),'blue')
    APy3_GENfuns.printcol('will calculate Gn-dependent avg, if there are at least {0} Img with the same Gn '.format(NImgGnX_str),'blue')
    #
    APy3_GENfuns.printcol('ADCcor file: {0}'.format(ADCcor_file),'blue')
    if ADU2eFlag: APy3_GENfuns.printcol('multiGnCal file: {0}'.format(multiGnCal_file),'blue')
    if alternPed: APy3_GENfuns.printcol('Pedestal-subtract: {0}'.format(alternFile_Ped_Gn0_ADU),'blue')
    #
    if CMAFlag: APy3_GENfuns.printcol('will apply CMA using cols {0} as reference'.format(cols2CMA_str),'blue')
    if CDSFlag: APy3_GENfuns.printcol('will apply CDS','blue')
    else: APy3_GENfuns.printcol('will use Sample','blue')
    #
    if saveFlag: 
        APy3_GENfuns.printcol('will save results as {0}...'.format(outFolder),'blue')
        if avgItForGn[0]: APy3_GENfuns.printcol('    will do it for Gn0','blue')
        if avgItForGn[1]: APy3_GENfuns.printcol('    will do it for Gn1','blue')
        if avgItForGn[2]: APy3_GENfuns.printcol('    will do it for Gn2','blue')
        if stdItFlag: APy3_GENfuns.printcol('    will also do it for std for those Gn','blue')
    #
    if highMemFlag: APy3_GENfuns.printcol('high mem use','blue')
    if cleanMemFlag: APy3_GENfuns.printcol('will clean memory when possible','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
if (verboseFlag): APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
# ---
#
#%% prepare h5 suffix for Gn0
if (CDSFlag & CMAFlag):    avgFileSuffix= outputFileMidfix+ '_CDSCMA({0})_avg.h5'.format(cols2CMA_str);  stdFileSuffix= outputFileMidfix+ '_CDSCMA({0})_sigma.h5'.format(cols2CMA_str)
elif (CDSFlag & ~CMAFlag): avgFileSuffix= outputFileMidfix+ '_CDS_avg.h5';                               stdFileSuffix= outputFileMidfix+ '_CDS_sigma.h5'
elif (CDSFlag & ~CDSFlag): avgFileSuffix= outputFileMidfix+ '_SmplCMA({0})_avg.h5'.format(cols2CMA_str); stdFileSuffix= outputFileMidfix+ '_SmplCMA({0})_sigma.h5'.format(cols2CMA_str)
else:                      avgFileSuffix= outputFileMidfix+ '_Smpl_avg.h5';                              stdFileSuffix= outputFileMidfix+ '_Smpl_sigma.h5'
# 
# now prepare h5 suffix for Gn12
avgFileSuffix_Gn12= outputFileMidfix+ '_Smpl_avg.h5'; stdFileSuffix_Gn12= outputFileMidfix+ '_Smpl_sigma.h5'

#---
#% load ADC calibr file
if APy3_GENfuns.notFound(ADCcor_file): APy3_GENfuns.printERR('not found '+ADCcor_file)
(ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset, ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
ADCparam_Rst_crs_slope, ADCparam_Rst_crs_offset,  ADCparam_Rst_fn_slope, ADCparam_Rst_fn_offset)= APy3_P2Mfuns.read_ADUh5(ADCcor_file)
if verboseFlag: APy3_GENfuns.printcol("ADC calibr file loaded {0}".format(ADCcor_file),'green')
#
#% load multiGnCal file if needed
if ADU2eFlag:
    if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
    (PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
    if verboseFlag: APy3_GENfuns.printcol("multiGnCal file loaded {0}".format(multiGnCal_file),'green')
else: 
    PedestalADU_multiGn= numpy.zeros((NGn,NRow,NCol))
    e_per_ADU_multiGn=   numpy.ones((NGn,NRow,NCol))
#
if alternPed:
    if APy3_GENfuns.notFound(alternFile_Ped_Gn0_ADU): APy3_GENfuns.printErr('not found: '+alternFile_Ped_Gn0_ADU)
    PedestalADU_multiGn[0,:,:]= APy3_GENfuns.read_1xh5(alternFile_Ped_Gn0_ADU, '/data/data')
    if verboseFlag: APy3_GENfuns.printcol("alternative Pedestal ADU file loaded {0}".format(alternFile_Ped_Gn0_ADU),'green')
#---
#% list files
fileList= APy3_GENfuns.list_files(folder_data2process, '*', inputFileSuffix)
if verboseFlag: APy3_GENfuns.printcol('{0} files to be processed'.format(len(fileList)),'green')
for iFile,thisFile in enumerate(fileList):
    if (verboseFlag): APy3_GENfuns.printcol("file {0}/{1}: {2}{3}".format(iFile,len(fileList)-1,folder_data2process,thisFile),'green')
    #
    (aux_NImgInFile,ignNRow,ignNCol)= APy3_GENfuns.size_1xh5(folder_data2process+thisFile, '/data')
    if (verboseFlag): APy3_GENfuns.printcol("  there are {0} images in this file".format(aux_NImgInFile),'green')
    if (verboseFlag): APy3_GENfuns.printcol("  will load {0}:{1}".format(fromImg,toImg),'green')
    if toImg >= aux_NImgInFile:
        APy3_GENfuns.printcol("there are only {0} images in the file: will load {1}:{2}".format(aux_NImgInFile, fromImg,aux_NImgInFile-1),'orange')
        (Smpl_DLSraw,Rst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+thisFile, '/data','/reset', fromImg,aux_NImgInFile-1)
    else: (Smpl_DLSraw,Rst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+thisFile, '/data','/reset', fromImg,toImg)
    #---
    # DLSraw => Gn,Crs,Fn
    if verboseFlag: APy3_GENfuns.printcol('DLSraw => Gn,Crs,Fn','blue')
    if highMemFlag: data_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(Smpl_DLSraw,Rst_DLSraw, ERRDLSraw, ERRint16)
    else:
        data_GnCrsFn= numpy.zeros((len(Img2proc),NSmplRst,NRow,NCol,NGnCrsFn), dtype='int16')
        for thisImg in range(len(Img2proc)):
            thisSmpl_DLSraw= Smpl_DLSraw[thisImg,:,:].reshape((1, NRow,NCol))
            thisRst_DLSraw=  Rst_DLSraw[thisImg,:,: ].reshape((1, NRow,NCol))
            this_dscrmbld_GnCrsFn= APy3_P2Mfuns.convert_DLSraw_2_GnCrsFn(thisSmpl_DLSraw,thisRst_DLSraw, ERRDLSraw,ERRint16)
            data_GnCrsFn[thisImg,:, :,:, :]= this_dscrmbld_GnCrsFn[0,:, :,:, :]    
            if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,len(Img2proc))
        if cleanMemFlag: del thisSmpl_DLSraw; del thisRst_DLSraw; del this_dscrmbld_GnCrsFn
    #---
    # Gn,Crs,Fn => ADU or e
    if verboseFlag: APy3_GENfuns.printcol('Gn,Crs,Fn => ADCcorr','blue')
    if highMemFlag: data_out= APy3_P2Mfuns.convert_GnCrsFn_2_e_wLatOvflw(data_GnCrsFn, CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,verboseFlag)
    else:
        # one at a time
        data_out= APy3_GENfuns.numpy_NaNs((len(Img2proc)-1,NRow,NCol))
        for thisImg in range(len(Img2proc)-1):
            # take 2 images, process them, (will use the one in position 1, eithter Sample or CDS, and out in position 0)
            this_data_out= APy3_P2Mfuns.convert_GnCrsFn_2_e_wLatOvflw(data_GnCrsFn[(thisImg):thisImg+2,:, :,:, :], 
                       CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,False) 
            data_out[thisImg,:,:]=this_data_out[0,:,:]
            del this_data_out
            if verboseFlag: APy3_GENfuns.dot_every10th(thisImg,len(Img2proc)-1)
    data_Gn= numpy.copy(data_GnCrsFn[1:,iSmpl,:,:,iGn])
    del data_GnCrsFn
    #---
    # avg by Gn
    for thisGn in range(3):
        if verboseFlag: APy3_GENfuns.printcol('avg-/std-ing data Gn{0}'.format(thisGn),'green')
        data_out_xGn= numpy.copy(data_out)
        GnX_map= data_Gn[:,:,:]==thisGn
        data_out_xGn[~GnX_map]= numpy.NaN
        data_avg=  numpy.nanmean(data_out_xGn, axis=0)
        data_std=  numpy.nanstd( data_out_xGn, axis=0)
        #
        enoughValid_map= numpy.sum(GnX_map,axis=0)>=NImgGnX
        data_avg[~enoughValid_map]= numpy.NaN
        data_std[~enoughValid_map]= numpy.NaN
        #
        if showFlag: 
            APy3_GENfuns.plot_2D_all(numpy.sum(GnX_map.astype(int),axis=0).astype(float), False, 'col','row','NImg Gn{0}'.format(thisGn), True)
            APy3_GENfuns.plot_2D_all(data_avg, False, 'col','row','avg {0} Gn{1} [{2}]'.format(avgFileSuffix[:-3],thisGn,outputFileMidfix), True)
            APy3_GENfuns.plot_2D_all(data_std, False, 'col','row','std {0} Gn{1} [{2}]'.format(avgFileSuffix[:-3],thisGn,outputFileMidfix), True)
            APy3_GENfuns.showIt()
        #
        del data_out_xGn; del GnX_map; del enoughValid_map
        # ---
        # save
        if (saveFlag & (avgItForGn[thisGn]==True) & (thisGn==0)):
            fileName_avg= thisFile[:(-len(inputFileSuffix))]+'Gn{0}_'.format(thisGn)+avgFileSuffix
            APy3_GENfuns.write_1xh5(outFolder+fileName_avg, data_avg, '/data/data')
            if (verboseFlag): APy3_GENfuns.printcol("saved avg {0}{1}".format(outFolder,fileName_avg),'green')
            #
            if stdItFlag:
                fileName_std= thisFile[:(-len(inputFileSuffix))]+'Gn{0}_'.format(thisGn)+stdFileSuffix
                APy3_GENfuns.write_1xh5(outFolder+fileName_std, data_std, '/data/data')
                if (verboseFlag): APy3_GENfuns.printcol("saved std {0}{1}".format(outFolder,fileName_std),'green')        
        elif (saveFlag & (avgItForGn[thisGn]==True) & (thisGn!=0)):
            fileName_avg= thisFile[:(-len(inputFileSuffix))]+'Gn{0}_'.format(thisGn)+avgFileSuffix_Gn12
            APy3_GENfuns.write_1xh5(outFolder+fileName_avg, data_avg, '/data/data')
            if (verboseFlag): APy3_GENfuns.printcol("saved avg {0}{1}".format(outFolder,fileName_avg),'green')
            #
            if stdItFlag:
                fileName_std= thisFile[:(-len(inputFileSuffix))]+'Gn{0}_'.format(thisGn)+stdFileSuffix_Gn12
                APy3_GENfuns.write_1xh5(outFolder+fileName_std, data_std, '/data/data')
                if (verboseFlag): APy3_GENfuns.printcol("saved std {0}{1}".format(outFolder,fileName_std),'green')

        if (verboseFlag): APy3_GENfuns.printcol("-",'green')    
        del data_avg; del data_std
#
#---
# that's all folks
if verboseFlag: 
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
    endTime=time.time()
    if verboseFlag: APy3_GENfuns.printcol("script took {0}s to finish".format(endTime-startTime),'green') 
    for i_aux in range(3): APy3_GENfuns.printcol('---------','blue')



