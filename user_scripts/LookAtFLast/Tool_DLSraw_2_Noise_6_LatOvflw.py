# -*- coding: utf-8 -*-
"""
DLSraw => eval noise for Smpl/Rst,CDS,CDS-CMA
#
# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./Tool_DLSraw_2_Noise_SmplRst_5_GnDependent.py
or:
python3
exec(open("./Tool_DLSraw_2_Noise_SmplRst_5_GnDependent.py").read())
"""
#%% imports and useful constants
from APy3_auxINIT import *
numpy.seterr(divide='ignore', invalid='ignore')

import warnings
warnings.simplefilter("ignore", category=RuntimeWarning) # numpy.nanstd warns if all NaN

NRow= APy3_P2Mfuns.NRow; NCol= APy3_P2Mfuns.NCol
iGn= APy3_P2Mfuns.iGn; iCrs= APy3_P2Mfuns.iCrs; iFn= APy3_P2Mfuns.iFn
iSmpl= APy3_P2Mfuns.iSmpl; iRst= APy3_P2Mfuns.iRst;
# ---
# auxiliary functions
def prep_hist(Array_xD):
    out_1D= numpy.copy(Array_xD).flatten()
    out_1D= out_1D[~numpy.isnan(out_1D)]
    return out_1D
#---
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#
#%% data from here
#
#'''
##### BSI04, BSI04_04 approx T-20 7/7 #####
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_000_BSI04_7of7_drk/processed/BSI04_7of7_drk/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
dflt_infile= "2020.04.06.07.38.08_BSI04_Tm20_dmuxSELsw_biasBSI04_04_3G_PGABBB_t012ms_1kdk_DLSraw.h5"
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'approx_BSI04_Tm20_dmuxSELsw_biasBSI04_04_PGABBB_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
#
#dflt_cols2CMA = '32:63' #dflt_cols2CMA = '704:735'
dflt_cols2CMA='NONE'
#
dflt_pngFolder='/home/marras/auximg/'
#dflt_pngFolder='/home/marras/ignimg/'
#dflt_pngFolder='NONE'
#
dflt_imageLabel= 'BSI04,3G,PGABBB'
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True
dflt_verboseFlag= True
#'''



#
'''
##### BSI04, BSI04_05 approx T-20 3/7 #####
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/drk_LatOvflow_PGA6BB_biasBSI04_05/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#dflt_infile= "2020.05.05.16.41.52_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.42.18_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.42.46_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.43.20_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
dflt_infile= "2020.05.05.16.43.42_BSI04_Tm20_3of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELHi_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'approx_BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
#
#dflt_cols2CMA = '32:63' #dflt_cols2CMA = '704:735'
dflt_cols2CMA='NONE'
#
dflt_pngFolder='/home/marras/auximg/'
#dflt_pngFolder='/home/marras/ignimg/'
#dflt_pngFolder='NONE'
#
dflt_imageLabel= 'BSI04'
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True 
dflt_verboseFlag= True
'''
#
'''
##### BSI04, BSI04_05 approx T-20 7/7 #####
dflt_folder_data2process='/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/drk_LatOvflow_PGA6BB_biasBSI04_05/DLSraw/'
if dflt_folder_data2process[-1]!='/': dflt_mainFolder+='/'
#dflt_infile= "2020.05.05.16.36.56_BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.37.22_BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.37.43_BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#dflt_infile= "2020.05.05.16.38.07_BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
dflt_infile= "2020.05.05.16.38.28_BSI04_Tm20_7of7ADC_biasBSI04_05_3G_PGA6BB_t012ms_1kdk_DLSraw.h5"
#
dflt_ADUcorr_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/'+'BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5'
dflt_multiGnCal_file= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/'+'approx_BSI04_Tm20_dmuxSELsw_biasBSI04_05_PGA6BB_Gn012_MultiGnCal.h5'
#
dflt_Img2proc= '10:999' # 'all'==all
#
dflt_CDSFlag=True; #dflt_CDSFlag=False
#
#dflt_cols2CMA = '32:63' #dflt_cols2CMA = '704:735'
dflt_cols2CMA='NONE'
#
dflt_pngFolder='/home/marras/auximg/'
#dflt_pngFolder='/home/marras/ignimg/'
#dflt_pngFolder='NONE'
#
dflt_imageLabel= 'BSI04'
#
dflt_highMemFlag= True; dflt_highMemFlag= False
dflt_cleanMemFlag= True
dflt_verboseFlag= True
'''
#
#
#---
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
GUIwin_arguments+= ['multiGnCal (PedestalADU, e/ADU): file'] 
GUIwin_arguments+= [dflt_multiGnCal_file]
#
GUIwin_arguments+= ['process data: in Img [from:to]'] 
GUIwin_arguments+= [dflt_Img2proc] 
#
GUIwin_arguments+= ['  if Gn0: CDS? [Y/N]'] 
GUIwin_arguments+= [str(dflt_CDSFlag)]
GUIwin_arguments+= ['  if Gn0: CMA Reference Columns? [first:last / NONE not to]'] 
GUIwin_arguments+= [dflt_cols2CMA]
#
GUIwin_arguments+= ['save png instead of showing: folder [NONE noto to do it]']
GUIwin_arguments+= [str(dflt_pngFolder)]
GUIwin_arguments+= ['label for images']
GUIwin_arguments+= [str(dflt_imageLabel)]
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
multiGnCal_file= dataFromUser[i_param]; i_param+=1;  
#
Img2proc_mtlb= dataFromUser[i_param]; i_param+=1;  
if Img2proc_mtlb in ['all','All','ALL',':','*','-1']: APy3_GENfuns.printErr('you  do not want to use all img')
else: Img2proc=APy3_GENfuns.matlabLike_range(Img2proc_mtlb); fromImg=Img2proc[0]; toImg=Img2proc[-1];
#
CDSFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#
cols2CMA_str= dataFromUser[i_param]; i_param+=1;  
if cols2CMA_str in APy3_GENfuns.NOlist: CMAFlag= False; cols2CMA=[]
else: CMAFlag= True; cols2CMA=APy3_GENfuns.matlabLike_range(cols2CMA_str);
#
pngFolder= dataFromUser[i_param]; i_param+=1;
if pngFolder in APy3_GENfuns.NOlist: pngFlag=False
else: pngFlag=True
#
imageLabel= dataFromUser[i_param]; i_param+=1;
#
highMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
cleanMemFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag=APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
#---
#
#%% what's up doc
if verboseFlag: 
    APy3_GENfuns.printcol('will process data from folder {0}'.format(folder_data2process),'blue')
    APy3_GENfuns.printcol('  using file {0}'.format(infile),'blue')
    APy3_GENfuns.printcol('will ADU-correct using {0}'.format(ADUcorr_file),'blue')
    APy3_GENfuns.printcol('using Pedestal[ADU] and e/ADU data from {0}'.format(multiGnCal_file),'blue')
    #
    if (CDSFlag): APy3_GENfuns.printcol('  will use CDS for Gn0','blue')
    if (CMAFlag): APy3_GENfuns.printcol('  will use CMA using RefCol{0}'.format(cols2CMA_str),'blue')
    #
    if pngFlag: APy3_GENfuns.printcol('will save plots to {0}'.format(pngFolder),'blue')
    else: APy3_GENfuns.printcol('will show plots','blue')

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
if APy3_GENfuns.notFound(multiGnCal_file): APy3_GENfuns.printErr('not found: '+multiGnCal_file)
(PedestalADU_multiGn,e_per_ADU_multiGn)= APy3_GENfuns.read_2xh5(multiGnCal_file, '/Pedestal_ADU/', '/e_per_ADU/')
if APy3_GENfuns.notFound(folder_data2process+infile): APy3_GENfuns.printErr('not found: '+folder_data2process+infile)
(drkSmpl_DLSraw,drkRst_DLSraw) = APy3_GENfuns.read_partial_2xh5(folder_data2process+infile, '/data','/reset', fromImg,toImg)

#---
#%% DLSraw => Gn
if verboseFlag: APy3_GENfuns.printcol('DLSraw => Gn','blue')
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
data_Gn= drk_GnCrsFn[1:,iSmpl,:,:,iGn] # starts from 2nd image
if cleanMemFlag: del drk_GnCrsFn
#---
#%% DLSraw => e
if verboseFlag: APy3_GENfuns.printcol('DLSraw => e','blue')
data_e= APy3_P2Mfuns.convert_DLSraw_2_e_wLatOvflw(drkSmpl_DLSraw,drkRst_DLSraw, CDSFlag, CMAFlag,cols2CMA,
                       ADCparam_Smpl_crs_slope,ADCparam_Smpl_crs_offset,ADCparam_Smpl_fn_slope,ADCparam_Smpl_fn_offset,
                       ADCparam_Rst_crs_slope,ADCparam_Rst_crs_offset,ADCparam_Rst_fn_slope,ADCparam_Rst_fn_offset,
                       PedestalADU_multiGn,e_per_ADU_multiGn,
                       highMemFlag,cleanMemFlag,verboseFlag)
#---
# std
if verboseFlag: APy3_GENfuns.printcol('std','blue')
std_e= numpy.nanstd(data_e[Img2proc[0]:(Img2proc[-1]+1),:,:],axis=0) # all Gn
#
std_e_xGn= APy3_GENfuns.numpy_NaNs((3,NRow,NCol))
NvalidImg_e_xGn= numpy.zeros((3,NRow,NCol))
for jGn in range(3):
    aux_data_thisGn= APy3_GENfuns.numpy_NaNs_like(data_e)
    aux_map_thisGnp= data_Gn==jGn
    aux_data_thisGn[aux_map_thisGnp]= data_e[aux_map_thisGnp]
    std_e_xGn[jGn]= numpy.nanstd(aux_data_thisGn[Img2proc[0]:(Img2proc[-1]+1),:,:],axis=0)
    NvalidImg_e_xGn[jGn]= numpy.sum(~numpy.isnan(aux_data_thisGn[Img2proc[0]:(Img2proc[-1]+1),:,:]),axis=0)
    del aux_data_thisGn; del aux_map_thisGnp
#
std_e_Original=numpy.copy(std_e)
badPixelMap= numpy.zeros_like(std_e).astype(bool) # originally badPixelMap=False
# ---
#%% interactive show
APy3_GENfuns.printcol("interactive plotting", 'blue')
thisRow=280;thisCol=320;this_histobins=15; ROIrows_str=":"; ROIcols_str=":"; atleastNImg=len(Img2proc)/2;
#
APy3_GENfuns.printcol("plot [N]oise maps / [F]ingerplot / [M]ost noisy pixel / mark [B]ad/re[L]oad all pixels/ [E]nd", 'green')
nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['n','N']:
        APy3_GENfuns.printcol("plotting noise maps", 'blue')
        this_histobins=100 #default
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'green'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'green'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("will estimate noise using ROI {0}".format(ROIstring), 'green')
        #
        data2histo= prep_hist(std_e[fromRow:(toRow+1),fromCol:(toCol+1)])
        #
        APy3_GENfuns.printcol("noise, avg in ROI{0}= {1}e +/- {2}e".format(ROIstring, numpy.nanmean(data2histo), numpy.nanstd(data2histo)), 'green')
        #
        if pngFlag: 
            auxTitle="{0}, noise [e]".format(imageLabel)
            APy3_GENfuns.png_2D_all(std_e, False, 'col','row',auxTitle, True, pngFolder+auxTitle+'_2D'+'.png')
            APy3_GENfuns.printcol("saved file: {0}".format(pngFolder+auxTitle+'_2D'+'.png'), 'green')
            #
            auxTitle="{0}, {1}, noise".format(imageLabel,ROIstring)
            APy3_GENfuns.png_histo1D(data2histo, this_histobins, False, auxTitle,"pixels","noise  [e]", pngFolder+auxTitle+'_1Dhisto'+'.png')
            APy3_GENfuns.printcol("saved file: {0}".format(pngFolder+auxTitle+'_2D'+'.png'), 'green')
            #
        else:
            auxTitle="{0}, noise [e]".format(imageLabel)
            APy3_GENfuns.plot_2D_all(std_e, False, 'col','row',auxTitle, True)
            #
            auxTitle="{0}, {1}, noise".format(imageLabel,ROIstring)
            APy3_GENfuns.plot_histo1D(data2histo, this_histobins, False, auxTitle,"pixels","noise  [e]")
            APy3_GENfuns.showit()
        del data2histo
    #
    if nextstep in ['f','F']:
        APy3_GENfuns.printcol("fingerplot spectrum:", 'black')
        this_histobins=15 #default

        APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'green'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'green'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'green'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("plotting fingerplot spectrum of pix ({0},{1}), {2} bins".format(thisRow,thisCol,this_histobins), 'green')
        #
        if ( numpy.isnan(std_e[thisRow,thisCol]) ) : 
            APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            APy3_GENfuns.printcol("noise for pix({0},{1})= {2}e".format(thisRow,thisCol,std_e[thisRow,thisCol]), 'green')
            data2histo= prep_hist(data_e[Img2proc[0]:(Img2proc[-1]+1), thisRow,thisCol])
            if pngFlag:
                APy3_GENfuns.png_histo1d(data2histo, this_histobins, False, "pixel output [e]","occurrences","{0} pix({1},{2})".format(imageLabel,thisRow,thisCol), pngFolder+auxTitle+"{0} pix({1},{2})".format(imageLabel,thisRow,thisCol)+'_1Dhisto'+'.png')
                APy3_GENfuns.printcol("saved png file to {0}".format(pngFolder), 'green')
            else:
                APy3_GENfuns.plot_histo1d(data2histo, this_histobins, False, "pixel output [e]","occurrences","{0} pix({1},{2})".format(imageLabel,thisRow,thisCol))
                APy3_GENfuns.showIt()

    #
    elif nextstep in ['G','g']:
        APy3_GENfuns.printcol("Easter Egg! plotting noise maps per gain", 'blue')
        this_histobins=100 #default
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        ROIrows= APy3_P2Mfuns.matlabRow(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        ROIcols= APy3_P2Mfuns.matlabCol(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will estimate per-Gn noise using ROI {0}, using pixels having at least {1} valid images".format(ROIstring,atleastNImg), 'green')
        #
        std_e_xGn_2show = numpy.copy(std_e_xGn)
        #std_e_xGn_2show[NvalidImg_e_xGn<atleastNImg]= numpy.NaN
        for jGn in range(3):
            aux2_map= NvalidImg_e_xGn[jGn,:,:]<atleastNImg
            std_e_xGn_2show[jGn,:,:][aux2_map]=numpy.NaN
        #
        auxTitle="{0}, noise per Gn [e]".format(imageLabel)
        if pngFlag: 
            matplotlib.pyplot.ioff()
            filenamepath_out= pngFolder+auxTitle+'_3x1Dhisto'+'.png'
        #
        fig = matplotlib.pyplot.figure()
        for jGn in range(3):
            std_e_thisGn= prep_hist(std_e_xGn_2show[jGn, fromRow:(toRow+1),fromCol:(toCol+1)])
            if len(std_e_thisGn)>0:
                auxNPix= numpy.sum(~numpy.isnan(std_e_thisGn).flatten()) 
                APy3_GENfuns.printcol("noise (Gn={3}), avg in ROI{0}= {1}e +/- {2}e for {4}pixels".format(ROIstring, numpy.nanmean(std_e_thisGn), numpy.nanstd(std_e_thisGn),jGn,auxNPix), 'green')
                matplotlib.pyplot.hist(std_e_thisGn, 100, alpha=0.5, label='Gn{0}'.format(jGn));
            del std_e_thisGn
        matplotlib.pyplot.legend(loc='upper right'); 
        matplotlib.pyplot.xlabel("noise [e]"); 
        matplotlib.pyplot.ylabel("pixels"); 
        matplotlib.pyplot.title(auxTitle)
        #
        if pngFlag: 
            matplotlib.pyplot.savefig(filenamepath_out)
            matplotlib.pyplot.close(fig)
            matplotlib.pyplot.ioff()
        else: APy3_GENfuns.showIt()
    #
    elif nextstep in ['M','m']:
        APy3_GENfuns.printcol("Find most noisy pixel", 'blue')
        auxmax= numpy.nanmax(std_e)
        auxargmax= numpy.unravel_index(numpy.nanargmax(std_e), std_e.shape)
        APy3_GENfuns.printcol("max noise= {0} e in {1}".format(auxmax,auxargmax), 'blue')
    #
    elif nextstep in ['L','l']:
        APy3_GENfuns.printcol("Reload all pixels (resets any bad pixel mask)", 'blue')
        std_e=numpy.copy(std_e_Original)
        badPixelMap[:,:]=False
        for jGn in range(3):
            aux_data_thisGn= APy3_GENfuns.numpy_NaNs_like(data_e)
            aux_map_thisGnp= data_Gn==jGn
            aux_data_thisGn[aux_map_thisGnp]= data_e[aux_map_thisGnp]
            std_e_xGn[jGn]= numpy.nanstd(aux_data_thisGn[Img2proc[0]:(Img2proc[-1]+1),:,:],axis=0)
            NvalidImg_e_xGn[jGn]= numpy.sum(~numpy.isnan(aux_data_thisGn[Img2proc[0]:(Img2proc[-1]+1),:,:]),axis=0)
            del aux_data_thisGn; del aux_map_thisGnp
    #
    elif nextstep in ['B','b']:
        APy3_GENfuns.printcol("will mark as Bad (nan) pixels in a ROI", 'blue')
        Rows2rmv= numpy.array([])
        Cols2rmv= numpy.array([])
        #
        APy3_GENfuns.printcol("Bad ROI map: Rows [first:last] [default is {0}]".format(Rows2rmv), 'blue')
        Rows2rmv_in= input()
        if len(Rows2rmv_in)<1: APy3_GENfuns.printcol("will keep default ROI Rows to remove {0}".format(Rows2rmv), 'blue')
        elif Rows2rmv_in in APy3_GENfuns.NOlist: Rows2rmv=[]
        elif Rows2rmv_in.isdigit(): Rows2rmv= APy3_GENfuns.matlabLike_range(Rows2rmv_in+':'+Rows2rmv_in)
        else: Rows2rmv= APy3_P2Mfuns.matlabRow(Rows2rmv_in)
        #
        APy3_GENfuns.printcol("Bad ROI map: Cols [first:last] [default is {0}]".format(Cols2rmv), 'blue')
        Cols2rmv_in= input()
        if len(Cols2rmv_in)<1: APy3_GENfuns.printcol("will keep default ROI Rows to remove {0}".format(Cols2rmv), 'blue')
        elif Cols2rmv_in in APy3_GENfuns.NOlist: Cols2rmv=[]
        elif Cols2rmv_in.isdigit(): Cols2rmv= APy3_GENfuns.matlabLike_range(Cols2rmv_in+':'+Cols2rmv_in)
        else: Cols2rmv= APy3_P2Mfuns.matlabCol(Cols2rmv_in)
        #
        if (len(Rows2rmv)<1)|(len(Cols2rmv)<1): APy3_GENfuns.printcol("will not remove any pixels", 'blue')
        else:
            APy3_GENfuns.printcol("Bad ROI map defined ({0}:{1},{2}:{3})".format(Rows2rmv[0],Rows2rmv[-1],Cols2rmv[0],Cols2rmv[-1]), 'blue')
            #
            std_e[Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]= numpy.NaN
            badPixelMap[Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]= True
            for jGn in range(3):
                std_e_xGn[jGn, Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]= numpy.NaN
                NvalidImg_e_xGn[jGn, Rows2rmv[0]:(Rows2rmv[-1]+1),Cols2rmv[0]:(Cols2rmv[-1]+1)]=0
        #
        if pngFlag:
            auxTitle="{0}, bad pixel map".format(imageLabel)
            APy3_GENfuns.png_2D_all(badPixelMap.astype(float), False, 'col','row',auxTitle, True, pngFolder+auxTitle+'_2D'+'.png')
            APy3_GENfuns.printcol("saved file: {0}".format(pngFolder+auxTitle+'_2D'+'.png'), 'green')
            #
        else:
            auxTitle="{0}, bad pixel map".format(imageLabel)
            APy3_GENfuns.plot_2D_all(badPixelMap.astype(float), False, 'col','row',auxTitle, True)
            APy3_GENfuns.showit()

    #
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:", 'green')
        APy3_GENfuns.printcol("G: noise per each Gn", 'green')
    #
    APy3_GENfuns.printcol("plot [N]oise maps / [E]nd plotting", 'black')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')


'''

#

#---
#%% interactive show
APy3_GENfuns.printcol("interactive plotting", 'blue')
thisRow=280;thisCol=320;this_histobins=15; ROIrows_str=":"; ROIcols_str=":"; atleastNImg=len(Img2proc)/2; badPixNoiseThres=350.0 # init

APy3_GENfuns.printcol("plot [N]oise maps / marking [B]ad pixels / plot [F]ingerplot / [E]nd plotting", 'black')


nextstep= APy3_GENfuns.press_any_key()
while nextstep not in ['e','E','q','Q']:
    if nextstep in ['n','N']:
        this_histobins=100 #default
        APy3_GENfuns.printcol("plotting noise maps", 'blue')
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having atr least {1} valid images".format(ROIstring,atleastNImg), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #

        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnParamToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        if showFlag:
            if saveFlag:
                auxTitle="std {0} (Gn{1}) [e]".format(mode_str,GnToUse)
                png_2D_all(stdThatGn_e_2show, False, 'col','row',"std {0} (Gn{1}) [e]".format(mode_str,GnToUse), True, saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
                auxTitle="number of Gn{0}-images for noise estimation".format(GnToUse)
                png_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True, saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
                #
                stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
                stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
                auxTitle="noise {0} {1}".format(mode_str,ROIstring)
                png_histo1D(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring), saveFolder+auxTitle)
                APy3_GENfuns.printcol("saved file: {0}".format(saveFolder+auxTitle+'.png'), 'green')
            else:
                APy3_GENfuns.plot_2D_all(stdThatGn_e_2show, False, 'col','row',"std {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
                APy3_GENfuns.plot_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True)
                #
                stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
                stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
                APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring))
                matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
    if nextstep in ['b','B']:
        this_histobins=100 #default
        APy3_GENfuns.printcol("plotting noise maps, marking bad pixels", 'blue')
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("marking as bad pixels the ones having a noise above [default is {0}]".format(badPixNoiseThres), 'black'); badPixNoiseThres_in= input(); 
        if (len(badPixNoiseThres_in)>0): badPixNoiseThres= float(badPixNoiseThres_in) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having at least {1} valid images, flagging as bad pixels the ones with noise above {0}e".format(ROIstring,atleastNImg,badPixNoiseThres), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #
        # show bad pixels
        badPixMap= stdThatGn_e_2show>badPixNoiseThres
        APy3_GENfuns.printcol("{0} pixels have a noise exceeding {1}e".format(numpy.sum(badPixMap),badPixNoiseThres), 'green')
        badPixNoiseMap_2show= numpy.copy(stdThatGn_e_2show)
        badPixNoiseMap_2show[~badPixMap]= numpy.NaN
        APy3_GENfuns.plot_2D_all(badPixNoiseMap_2show, False, 'col','row',"noise of bad pixels in {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
        #
        badPix_RowList,badPix_ColList=numpy.where(badPixMap)
        for iPix,thisRow in enumerate(badPix_RowList):
            thisRow= badPix_RowList[iPix]; thisCol= badPix_ColList[iPix]
            APy3_GENfuns.printcol("bad pix ({0},{1}): noise {2}e".format(thisRow,thisCol,stdThatGn_e_2show[thisRow,thisCol]), 'green')
        #
        # remove bad pixels
        stdThatGn_e_2show[badPixMap]= numpy.NaN
        #
        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnParamToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        #
        APy3_GENfuns.plot_2D_all(stdThatGn_e_2show, False, 'col','row',"noise {0} (Gn{1}) [e]".format(mode_str,GnToUse), True)
        APy3_GENfuns.plot_2D_all(vals2avg.astype(float), False, 'col','row',"number of Gn{0}-images for noise estimation".format(GnToUse), True)
        #
        stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
        APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} (Gn{1}) {2}".format(mode_str,GnToUse,ROIstring))
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
    #
    elif nextstep in ['f','F',]:
        this_histobins=15 #default
        APy3_GENfuns.printcol("fingerplot spectrum:", 'black')
        APy3_GENfuns.printcol("which pixel? (Row) [default is {0}]".format(thisRow), 'black'); thisRow_str= input(); 
        if thisRow_str.isdigit(): thisRow= int(thisRow_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("which pixel? (Col) [default is {0}]".format(thisCol), 'black'); thisCol_str= input(); 
        if thisCol_str.isdigit(): thisCol= int(thisCol_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        APy3_GENfuns.printcol("plotting fingerplot spectrum of pix ({0},{1}), {2} bins".format(thisRow,thisCol,this_histobins), 'blue')
        #
        if ( numpy.isnan(stdThatGn_e[thisRow,thisCol]) ) : 
            APy3_GENfuns.printcol("no valid data", 'orange')
        else:
            APy3_GENfuns.printcol("noise {0} for pix({1},{2})= {3}e, evaluated on {4} samples".format(mode_str,thisRow,thisCol,stdThatGn_e[thisRow,thisCol],vals2avg[thisRow,thisCol]), 'green')
            #
            drkThatGnThatPix_2histo= numpy.copy(drkThatGn_e[:,thisRow,thisCol])
            drkThatGnThatPix_2histo= drkThatGnThatPix_2histo[~numpy.isnan(drkThatGnThatPix_2histo)]
            APy3_GENfuns.plot_histo1d(drkThatGnThatPix_2histo, this_histobins, False, "pixel output [e]","occurrences","pix({0},{1}), {2}".format(thisRow,thisCol,mode_str))
            matplotlib.pyplot.show(block=True)    
    #
    elif nextstep in ['a','A']:
        APy3_GENfuns.printcol("Easter egg: A to check Noise by ADC", 'black')
        this_histobins=100 #default
        APy3_GENfuns.printcol("which Row ROI? [firstRow:lastRow] [default is {0}]".format(ROIrows_str), 'black'); ROIrows_in= input(); 
        if (len(ROIrows_in)>0): ROIrows_str= ROIrows_in # otherwise keeps the old value
        APy3_GENfuns.printcol("which Col ROI? [firstCol:lastCol] [default is {0}]".format(ROIcols_str), 'black'); ROIcols_in= input(); 
        if (len(ROIcols_in)>0): ROIcols_str= ROIcols_in # otherwise keeps the old value
        if ROIrows_str in ['all','All','ALL',':','*','-1']: fromRow= 0; toRow= NRow-1
        else: ROIrows= APy3_GENfuns.matlabLike_range(ROIrows_str); fromRow= ROIrows[0]; toRow= ROIrows[-1]
        if fromRow%7!=0: fromRow= (fromRow//7)*7
        if toRow%7!=6:   toRow=   ( (fromRow//7)*7 )+6
        ROIrows= numpy.arange(fromRow,toRow+1)
        #
        if ROIcols_str in ['all','All','ALL',':','*','-1']: fromCol= 32; toCol= NCol-1
        else: ROIcols= APy3_GENfuns.matlabLike_range(ROIcols_str); fromCol= ROIcols[0]; toCol= ROIcols[-1]
        ROIstring="({0}:{1},{2}:{3})".format(fromRow,toRow,fromCol,toCol)
        APy3_GENfuns.printcol("how many bins? [default is {0}]".format(this_histobins), 'black'); this_histobins_str= input()
        if this_histobins_str.isdigit(): this_histobins= int(this_histobins_str) # otherwise keeps the old value
        #
        APy3_GENfuns.printcol("using pixels having at least these many images valid  [default is {0}]".format(atleastNImg), 'black'); atleastNImg_in= input(); 
        if (len(atleastNImg_in)>0): atleastNImg= int(atleastNImg_in) # otherwise keeps the old value
        APy3_GENfuns.printcol("will estimate noise using ROI {0}, using pixels having atr least {1} valid images".format(ROIstring,atleastNImg), 'green')
        #
        stdThatGn_e_2show = numpy.copy(stdThatGn_e)
        stdThatGn_e_2show[vals2avg<atleastNImg]= numpy.NaN
        #
        APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}= {3}e +/- {4}e".format(mode_str, ROIstring, GnToUse, numpy.nanmean(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)]), numpy.nanstd(stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)])), 'green')
        stdThatGn_e_2histo= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].flatten()
        stdThatGn_e_2histo= stdThatGn_e_2histo[~numpy.isnan(stdThatGn_e_2histo)]
        APy3_GENfuns.plot_histo1d(stdThatGn_e_2histo, this_histobins, False, "noise {0} [e]".format(mode_str),"pixels","noise {0} {1}".format(mode_str,ROIstring))
        #
        stdThatGn_e_2show_xADC= stdThatGn_e_2show[fromRow:(toRow+1),fromCol:(toCol+1)].reshape((len(ROIrows)//7,7,len(ROIcols)))
        fig = matplotlib.pyplot.figure()
        for iADC in range(7):
            thisADCvals= stdThatGn_e_2show_xADC[:,iADC,:].flatten()
            thisADCvals= thisADCvals[~numpy.isnan(thisADCvals)]
            if len(thisADCvals)>0: 
                matplotlib.pyplot.hist(thisADCvals, 100, alpha=0.5, label='rows 7i + {0}'.format(iADC));
                APy3_GENfuns.printcol("noise {0}, avg in ROI{1} with Gn{2}, rows 7i+{3} = {4}e +/- {5}e".format(mode_str, ROIstring, GnParamToUse, iADC, numpy.nanmean(thisADCvals), numpy.nanstd(thisADCvals)), 'green')
            del thisADCvals
        matplotlib.pyplot.legend(loc='upper right'); 
        matplotlib.pyplot.xlabel("noise {0} [e]".format(mode_str)); 
        matplotlib.pyplot.ylabel("pixels"); 
        matplotlib.pyplot.title("noise {0} {1}".format(mode_str,ROIstring))
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter Egg list:", 'black')
        APy3_GENfuns.printcol("A to check Noise by ADC", 'black')
    #
    APy3_GENfuns.printcol("plot [N]oise maps / marking [B]ad pixels / plot [F]ingerplot / [E]nd plotting", 'black')
    nextstep= APy3_GENfuns.press_any_key()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end plotting", 'blue')
#---
'''
#%% that's all folks
endTime=time.time()
if verboseFlag: 
    APy3_GENfuns.printcol("done",'blue')
    APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
    for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')



