# -*- coding: utf-8 -*-
"""
LatOvflw_param incomplete array (NaN= missing data) => interpolate using valid 1st-neighbours/averages

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_03_filler.py
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
# ---
#
#%% defaults for GUI window
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal.h5_extractedOnly.h5"
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/"+"BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn012_2020.05.14b_MultiGnCal_gapsAvg.h5"
#dflt_GnToProc='2'
#
#
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD3.0_prelim.h5_avoidExtremes.h5"
#
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_test.h5"
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_test.h5_Gnyy2.h5"
#
#dflt_file2interpolate= "/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12c_Gn012_MultiGnCal_excludeBadPix.h5"
#dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200406_001_CalibParam_scripts_tempdata/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_fixGnCal/BSI04_Tm20_7of7ADC_biasBSI04.05_fixGn0_PGAB_2020.03.12_fixGnCal_from3of7gapsAvg_approx.h5"

dflt_file2interpolate= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn012_2020.06.10_MultiGnCal_ADU2eAvg.h5_usingOD0.5_OD3.0_R2_0.85.h5"

dflt_GnToProc='1'
#
dflt_Rows2proc='0:1483'  
dflt_Cols2proc='32:1439'

# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['use data from LatOvflw_param file'] 
GUIwin_arguments+= [dflt_file2interpolate] 
#
GUIwin_arguments+= ['Gn to process [0/1/2]'] 
GUIwin_arguments+= [dflt_GnToProc] 
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Rows2proc] 
GUIwin_arguments+= ['process data: in columns [from:to]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
#
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
file2interpolate= dataFromUser[i_param]; i_param+=1
#
GnToProc = int(dataFromUser[i_param]); i_param+=1
#
Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Rows2proc_mtlb in ['all','All','ALL',':','*','-1']: Rows2proc= numpy.arange(NRow)
else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 

Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Cols2proc_mtlb in ['all','All','ALL',':','*','-1']: Cols2proc= numpy.arange(NCol)
else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will process data from '+file2interpolate,'blue')
APy3_GENfuns.printcol('will elaborate Gn{0}, Cols {1}, Rows {2}'.format(GnToProc, Cols2proc_mtlb,Rows2proc_mtlb),'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#% read data files
if APy3_GENfuns.notFound(file2interpolate): APy3_GENfuns.printErr('not found: '+file2interpolate)
(indata_ADU0,indata_ADU2e)= APy3_GENfuns.read_2xh5(file2interpolate, '/Pedestal_ADU/', '/e_per_ADU/')
interpData_ADU0=  APy3_GENfuns.numpy_NaNs_like(indata_ADU0)
interpData_ADU2e= APy3_GENfuns.numpy_NaNs_like(indata_ADU2e)

def aux_copyvals(indata_ADU0, indata_ADU2e, GnToProc,Rows2proc,Cols2proc):
    ''' from indata to interpData:
        cp all data for Gn!=GnToProc
        cp only ROI for Gn==GnToProc '''
    interpData_ADU0=  APy3_GENfuns.numpy_NaNs_like(indata_ADU0)
    interpData_ADU2e= APy3_GENfuns.numpy_NaNs_like(indata_ADU2e)
    for iGn in range(3):
        if iGn!= GnToProc: 
            interpData_ADU0[iGn,:,:]=  numpy.copy(indata_ADU0[iGn,:,:])
            interpData_ADU2e[iGn,:,:]= numpy.copy(indata_ADU2e[iGn,:,:])
        else: 
            for iRow in Rows2proc:
                for iCol in Cols2proc:
                    interpData_ADU0[iGn,iRow,iCol]=  indata_ADU0[iGn,iRow,iCol]
                    interpData_ADU2e[iGn,iRow,iCol]= indata_ADU2e[iGn,iRow,iCol]   
    return (interpData_ADU0,interpData_ADU2e)

(interpData_ADU0,interpData_ADU2e)= aux_copyvals(indata_ADU0, indata_ADU2e, GnToProc,Rows2proc,Cols2proc)

#---
orig_GnToProc= GnToProc
orig_Rows2proc= numpy.copy(Rows2proc)
orig_Cols2proc= numpy.copy(Cols2proc)
#
totInterpCounter=0
#
APy3_GENfuns.printcol("Show [O]riginal/[I]nterpolated data / change source [R]OI or Gn / report [M]in-max-avg in source ROI,Gn / [D]elete values in a ROI/values [T]oo high or low / interpolate [number] cycles / fill with [A]verage/o[V]erwrite all with average in a destination ROI / upload a different [P]edestal/[S]lope / save to [F]ile / re[L]oad original source ROI / [E]nd", 'black')

nextstep = input()
#
while nextstep not in ['e','E','q','Q']:
    matplotlib.pyplot.close()
    #
    if nextstep in ['o','O']: 
        for iGn in range(3):
            APy3_GENfuns.plot_2D_all(indata_ADU2e[iGn], False, 'col','row',"Gn{0}: e/ADU (original)".format(iGn), True)
            APy3_GENfuns.plot_2D_all(indata_ADU0[iGn], False, 'col','row',"Gn{0}: pedestal [ADU] (original)".format(iGn), True)
        APy3_GENfuns.show_it()
    #
    elif nextstep in ['i','I']: 
        for iGn in range(3):
            APy3_GENfuns.plot_2D_all(interpData_ADU2e[iGn], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
            APy3_GENfuns.plot_2D_all(interpData_ADU0[iGn], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        APy3_GENfuns.show_it()
    # 
    elif nextstep in ['r','R']: 
        APy3_GENfuns.printcol("changing source ROI: rows? [first:last]", 'black')
        Rows2proc_in= input() 
        if (len(Rows2proc_in)<1): APy3_GENfuns.printcol("will keep ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        elif Rows2proc_in in ['all','All','ALL',':','*','-1']: 
            Rows2proc= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        else: 
            Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_in)
            APy3_GENfuns.printcol("will change ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing ROI: cols? [first:last]", 'black')
        Cols2proc_in= input() 
        if (len(Cols2proc_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        elif Cols2proc_in in ['all','All','ALL',':','*','-1']: 
            Cols2proc= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change ROI: cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        else: 
            Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_in)
            APy3_GENfuns.printcol("will change ROI: cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing source Gn: [0/1/2]", 'black')
        GnToProc_in= input() 
        if (len(GnToProc_in)<1): APy3_GENfuns.printcol("will keep Gn: {0}".format(GnToProc), 'green')
        else: 
            GnToProc= int(GnToProc_in)
            APy3_GENfuns.printcol("will change Gn: {0}".format(GnToProc), 'green')
        # 
        old_interpData_ADU0= numpy.copy(interpData_ADU0)
        old_interpData_ADU2e= numpy.copy(interpData_ADU2e)
        (interpData_ADU0,interpData_ADU2e)= aux_copyvals(old_interpData_ADU0, old_interpData_ADU2e, GnToProc,Rows2proc,Cols2proc)
        del old_interpData_ADU0; del old_interpData_ADU2e
        APy3_GENfuns.printcol("showing interpolated array, close image to move on", 'black')
        for iGn in range(3):
            APy3_GENfuns.plot_2D_all(interpData_ADU2e[iGn], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
            APy3_GENfuns.plot_2D_all(interpData_ADU0[iGn], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        APy3_GENfuns.show_it()
    #     
    elif nextstep in ['m','M']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("current source ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("current sub-ROI to evaluate is ({0}:{1},{2}:{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        #
        APy3_GENfuns.printcol("ADU0:", 'green')
        #
        ADU0_minval= numpy.nanmin(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        ADU0_minvaladdr= numpy.unravel_index(numpy.nanargmin(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]),
                                                             interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("    min val in sub-ROI,Gn is {0} in ({1},{2})".format(ADU0_minval,ADU0_minvaladdr[0]+Rows2avg[0],ADU0_minvaladdr[1]+Cols2avg[0]), 'green')
        #
        ADU0_maxval= numpy.nanmax(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        ADU0_maxvaladdr= numpy.unravel_index(numpy.nanargmax(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]),
                                                             interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("    max val in sub-ROI,Gn is {0} in ({1},{2})".format(ADU0_maxval,ADU0_maxvaladdr[0]+Rows2avg[0],ADU0_maxvaladdr[1]+Cols2avg[0]), 'green')
        #
        ADU0_avgval= numpy.nanmean(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(ADU0_avgval), 'green')
        #
        APy3_GENfuns.printcol("e/ADU:", 'green')
        #
        ADU2e_minval= numpy.nanmin(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        ADU2e_minvaladdr= numpy.unravel_index(numpy.nanargmin(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]),
                                                              interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("    min val in sub-ROI,Gn is {0} in ({1},{2})".format(ADU2e_minval,ADU2e_minvaladdr[0]+Rows2avg[0],ADU2e_minvaladdr[1]+Cols2avg[0]), 'green')
        #
        ADU2e_maxval= numpy.nanmax(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        ADU2e_maxvaladdr= numpy.unravel_index(numpy.nanargmax(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]),
                                                              interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("    max val in sub-ROI,Gn is {0} in ({1},{2})".format(ADU2e_maxval,ADU2e_maxvaladdr[0]+Rows2avg[0],ADU2e_maxvaladdr[1]+Cols2avg[0]), 'green')
        #
        ADU2e_avgval= numpy.nanmean(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(ADU2e_avgval), 'green')
        #
    elif nextstep in ['t','T']:
        APy3_GENfuns.printcol("will delete values too high/low in Gn{0}".format(GnToProc), 'black')
        #
        ADU0_avgval= numpy.nanmean(interpData_ADU0[GnToProc,:,:].flatten())
        ADU0_minval= numpy.nanmin(interpData_ADU0[GnToProc,:,:].flatten())
        ADU0_maxval= numpy.nanmax(interpData_ADU0[GnToProc,:,:].flatten())
        APy3_GENfuns.printcol("ADU0: min={0}, avg={1}, max={2}".format(ADU0_minval,ADU0_avgval,ADU0_maxval), 'green')
        #
        ADU2e_minval= numpy.nanmin(interpData_ADU2e[GnToProc,:,:].flatten())
        ADU2e_maxval= numpy.nanmax(interpData_ADU2e[GnToProc,:,:].flatten())
        ADU2e_avgval= numpy.nanmean(interpData_ADU2e[GnToProc,:,:].flatten())
        APy3_GENfuns.printcol("e/ADU: min={0}, avg={1}, max={2}".format(ADU2e_minval,ADU2e_avgval,ADU2e_maxval), 'green')
        #
        ADU0_notabove= ADU0_maxval+1.0
        ADU0_notbelow= ADU0_minval-1.0
        ADU2e_notabove= ADU2e_maxval+1.0
        ADU2e_notbelow= ADU2e_minval-1.0
        #
        APy3_GENfuns.printcol("will delete pixels having ADU0 (in Gn{0}) higher than: [default is {1}] ".format(GnToProc,ADU0_notabove), 'black')
        ADU0_notabove_in= input()
        if (len(ADU0_notabove_in)<1): APy3_GENfuns.printcol("will delete pixels having ADU0 (in Gn{0}) higher than {1}".format(GnToProc,ADU0_notabove), 'black')
        else: ADU0_notabove= float(ADU0_notabove_in)
        #
        APy3_GENfuns.printcol("will delete pixels having ADU0 (in Gn{0}) lower than: [default is {1}] ".format(GnToProc,ADU0_notbelow), 'black')
        ADU0_notbelow_in= input()
        if (len(ADU0_notbelow_in)<1): APy3_GENfuns.printcol("will delete pixels having ADU0 (in Gn{0}) lower than {1}".format(GnToProc,ADU0_notbelow), 'black')
        else: ADU0_notbelow= float(ADU0_notbelow_in)
        #
        APy3_GENfuns.printcol("will delete pixels having e/ADU (in Gn{0}) higher than: [default is {1}] ".format(GnToProc,ADU2e_notabove), 'black')
        ADU2e_notabove_in= input()
        if (len(ADU2e_notabove_in)<1): APy3_GENfuns.printcol("will delete pixels having ADU2e (in Gn{0}) higher than {1}".format(GnToProc,ADU2e_notabove), 'black')
        else: ADU2e_notabove= float(ADU2e_notabove_in)
        #
        APy3_GENfuns.printcol("will delete pixels having e/ADU (in Gn{0}) lower than: [default is {1}] ".format(GnToProc,ADU2e_notbelow), 'black')
        ADU2e_notbelow_in= input()
        if (len(ADU2e_notbelow_in)<1): APy3_GENfuns.printcol("will delete pixels having ADU2e (in Gn{0}) lower than {1}".format(GnToProc,ADU2e_notbelow), 'black')
        else: ADU2e_notbelow= float(ADU2e_notbelow_in)
        #
        aux_badmap2= numpy.zeros_like(interpData_ADU0[GnToProc,:,:]).astype('bool')
        #
        aux_badmap= interpData_ADU0[GnToProc,:,:]>ADU0_notabove
        aux_badmap2[aux_badmap]=True
        del aux_badmap
        #
        aux_badmap= interpData_ADU0[GnToProc,:,:]<ADU0_notbelow
        aux_badmap2[aux_badmap]=True
        del aux_badmap
        #
        aux_badmap= interpData_ADU2e[GnToProc,:,:]>ADU2e_notabove
        aux_badmap2[aux_badmap]=True
        del aux_badmap
        #
        aux_badmap= interpData_ADU2e[GnToProc,:,:]<ADU2e_notbelow
        aux_badmap2[aux_badmap]=True
        del aux_badmap
        #
        interpData_ADU0[GnToProc, :,:][aux_badmap2]= numpy.NaN
        interpData_ADU2e[GnToProc, :,:][aux_badmap2]= numpy.NaN
        #
        APy3_GENfuns.printcol("deleting {0} points".format(numpy.sum(aux_badmap2.flatten())), 'black')
        #
        APy3_GENfuns.printcol("showing after deleting, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(aux_badmap2.astype(float), False, 'col','row',"deleted pixels", True)
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
        matplotlib.pyplot.show(block=True)
        del aux_badmap2
    #
    elif nextstep in ['d','D']:
        APy3_GENfuns.printcol("will delete values in a ROI in Gn{0}".format(GnToProc), 'black')
        Rows2dest=numpy.copy(Rows2proc)
        Cols2dest=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("current deletion ROI is ({0}:{1},{2}:{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'black')
        APy3_GENfuns.printcol("changing deletion ROI: rows? [first:last]", 'black')
        Rows2dest_in= input() 
        if (len(Rows2dest_in)<1): APy3_GENfuns.printcol("will keep deletion ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        elif Rows2dest_in in ['all','All','ALL',':','*','-1']: 
            Rows2dest= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change deletion ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        elif Rows2dest_in.isdigit(): Rows2dest= APy3_GENfuns.matlabLike_range(Rows2dest_in+':'+Rows2dest_in)
        else: 
            Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
            APy3_GENfuns.printcol("will change deletion ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing ROI: deletion cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change deletion ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in.isdigit(): Cols2dest= APy3_GENfuns.matlabLike_range(Cols2dest_in+':'+Cols2dest_in)
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change deletion ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("deletion ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1],GnToProc), 'green')
        interpData_ADU0[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= numpy.NaN      
        interpData_ADU2e[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= numpy.NaN 
        # 
        APy3_GENfuns.printcol("showing after deleting, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
        matplotlib.pyplot.show(block=True) 
    #
    elif nextstep in ['a','A']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("current source ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("current sub-ROI to evaluate is ({0}:{1},{2}:{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        #
        APy3_GENfuns.printcol("ADU0:", 'green')
        avgval_ADU0= numpy.nanmean(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(avgval_ADU0), 'green')
        #
        APy3_GENfuns.printcol("e/ADU:", 'green')
        avgval_ADU2e= numpy.nanmean(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(avgval_ADU2e), 'green')
        #
        APy3_GENfuns.printcol("will fill destination ROI in Gn{0} with said averages".format(GnToProc), 'black')
        Rows2dest=numpy.copy(Rows2proc)
        Cols2dest=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("current destination ROI is ({0}:{1},{2}:{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'black')
        APy3_GENfuns.printcol("changing destination ROI: rows? [first:last]", 'black')
        Rows2dest_in= input() 
        if (len(Rows2dest_in)<1): APy3_GENfuns.printcol("will keep destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')

        elif Rows2dest_in in ['all','All','ALL',':','*','-1']: 
            Rows2dest= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        else: 
            Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
            APy3_GENfuns.printcol("will change ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing destination ROI: cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep destination ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("destination destination ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1],GnToProc), 'green')
        #
        interpData_ADU0[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)][numpy.isnan(interpData_ADU0[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1) ])]= avgval_ADU0      
        interpData_ADU2e[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)][numpy.isnan(interpData_ADU2e[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1) ])]= avgval_ADU2e
        #
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
        matplotlib.pyplot.show(block=True) 
    #
    elif nextstep in ['v','V']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("current source ROI is ({0}:{1},{2}:{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to evaluate: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to evaluate: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to evaluate: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("current sub-ROI to evaluate is ({0}:{1},{2}:{3}), current Gn is: {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],GnToProc), 'green')
        #
        APy3_GENfuns.printcol("ADU0:", 'green')
        avgval_ADU0= numpy.nanmean(interpData_ADU0[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(avgval_ADU0), 'green')
        #
        APy3_GENfuns.printcol("e/ADU:", 'green')
        avgval_ADU2e= numpy.nanmean(interpData_ADU2e[GnToProc,:,:][Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("    avg val in sub-ROI,Gn is {0}".format(avgval_ADU2e), 'green')
        APy3_GENfuns.printcol("will overwrite destination ROI in Gn{0} with said averages".format(GnToProc), 'black')
        Rows2dest=numpy.copy(Rows2proc)
        Cols2dest=numpy.copy(Cols2proc)
        #
        APy3_GENfuns.printcol("changing destination ROI: rows? [first:last]", 'black')
        Rows2dest_in= input() 
        if (len(Rows2dest_in)<1): APy3_GENfuns.printcol("will keep destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        elif Rows2dest_in in ['all','All','ALL',':','*','-1']: 
            Rows2dest= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        else: 
            Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
            APy3_GENfuns.printcol("will change ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing ROI: cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("destination ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1],GnToProc), 'green')
        #
        interpData_ADU0[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= avgval_ADU0      
        interpData_ADU2e[GnToProc, Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= avgval_ADU2e
        #
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
        matplotlib.pyplot.show(block=True)  
    #
    elif nextstep in ['p','P']: 
        APy3_GENfuns.printcol("will upload a different pedestal for Gn{0}".format(GnToProc), 'black')
        APy3_GENfuns.printcol("which file?", 'black')
        file2load= input()
        if APy3_GENfuns.notFound(file2load): APy3_GENfuns.printcol("not found: {0}".format(file2load), 'green')
        else:
            interpData_ADU0[GnToProc,:,:]= APy3_GENfuns.read_1xh5(file2load,'/data/data')
            APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
            APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
            APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
            APy3_GENfuns.showIt()
    elif nextstep in ['s','S']: 
        APy3_GENfuns.printcol("will upload a different slope for Gn{0}".format(GnToProc), 'black')
        APy3_GENfuns.printcol("which file?", 'black')
        file2load= input()
        if APy3_GENfuns.notFound(file2load): APy3_GENfuns.printcol("not found: {0}".format(file2load), 'green')
        else:
            interpData_ADU2e[GnToProc,:,:]= APy3_GENfuns.read_1xh5(file2load,'/data/data')
            APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
            APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(GnToProc), True)
            APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(GnToProc), True)
            APy3_GENfuns.showIt()
    #
    elif nextstep in ['f','F']: 
        outFileNamePath=file2interpolate+'_{0}interpol.h5'.format(totInterpCounter)
        APy3_GENfuns.write_2xh5(outFileNamePath, 
               interpData_ADU0, '/Pedestal_ADU/', 
               interpData_ADU2e, '/e_per_ADU/')
        APy3_GENfuns.printcol("interp file saved: {0}".format(outFileNamePath), 'black')
    #
    elif nextstep in ['l','L']:
        APy3_GENfuns.printcol("reloading original values, resetting the ROI and Gn to original values", 'black')
        GnToProc= orig_GnToProc
        Rows2proc= numpy.copy(orig_Rows2proc)
        Cols2proc= numpy.copy(orig_Cols2proc)
        (interpData_ADU0,interpData_ADU2e)= aux_copyvals(indata_ADU0, indata_ADU2e, GnToProc,Rows2proc,Cols2proc)
        totInterpCounter=0
        #
        for iGn in range(3):
            APy3_GENfuns.plot_2D_all(interpData_ADU2e[iGn,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
            APy3_GENfuns.plot_2D_all(interpData_ADU0[iGn,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['$']:
        APy3_GENfuns.printcol("Easter Egg: on e/ADU only: overwrite all non-nans n Gn {0} with the average".format(GnToProc),'green')
        aux_avg= numpy.nanmean(interpData_ADU2e[GnToProc,:,:].flatten())
        auxmap= ~numpy.isnan(interpData_ADU2e[GnToProc,:,:])
        interpData_ADU2e[GnToProc,:,:][auxmap]=aux_avg
        del aux_avg; del auxmap
        APy3_GENfuns.printcol("done",'green')        
    #
    elif nextstep in ['-']:
        APy3_GENfuns.printcol("Easter Egg: for each row: fill with the average for row, for Gn {0}".format(GnToProc),'green')
        aux_avg_ADU2e_xrow= numpy.nanmean(interpData_ADU2e[GnToProc,:,:], axis=1)
        aux_avg_ADU0_xrow= numpy.nanmean(interpData_ADU0[GnToProc,:,:], axis=1)
        #
        APy3_GENfuns.printcol("changing destination ROI: rows? [first:last]", 'black')
        Rows2dest_in= input() 
        if (len(Rows2dest_in)<1): APy3_GENfuns.printcol("will keep destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        elif Rows2dest_in in ['all','All','ALL',':','*','-1']: Rows2dest= numpy.arange(NRow); 
        else: Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
        #
        APy3_GENfuns.printcol("changing ROI: cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in in ['all','All','ALL',':','*','-1']: Cols2dest= numpy.arange(32,NCol); 
        else: Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
        #
        APy3_GENfuns.printcol("destination ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1],GnToProc), 'green')
        #
        APy3_GENfuns.printcol("ADU0: fill with the average for row?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            for thisRow in range(Rows2dest[0],Rows2dest[-1]+1):
                auxmap= numpy.isnan(interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][auxmap]=aux_avg_ADU0_xrow[thisRow]
                del auxmap
        del fillFlag_str
        #
        APy3_GENfuns.printcol("e/ADU: fill with the average for row?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            for thisRow in range(Rows2dest[0],Rows2dest[-1]+1):
                auxmap= numpy.isnan(interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][auxmap]=aux_avg_ADU2e_xrow[thisRow]
                del auxmap
        del fillFlag_str
        #
        del aux_avg_ADU2e_xrow; del aux_avg_ADU0_xrow

        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')

        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)

        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)

        APy3_GENfuns.showIt()
    #
    elif nextstep in ['@']:
        APy3_GENfuns.printcol("Easter Egg: for each row: fill with overall average, for Gn {0}".format(GnToProc),'green')
        aux_avg_ADU2e= numpy.nanmean(interpData_ADU2e[GnToProc,:,:].flatten())
        aux_avg_ADU0= numpy.nanmean(interpData_ADU0[GnToProc,:,:].flatten())
        #
        APy3_GENfuns.printcol("ADU0: fill with the average?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            auxmap= numpy.isnan(interpData_ADU0[GnToProc,:,32:])
            interpData_ADU0[GnToProc,:,32:][auxmap]=aux_avg_ADU0
            del auxmap; 
        del fillFlag_str
        #
        APy3_GENfuns.printcol("e/ADU: fill with the average?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            auxmap= numpy.isnan(interpData_ADU2e[GnToProc,:,32:])
            interpData_ADU2e[GnToProc,:,32:][auxmap]=aux_avg_ADU2e
            del auxmap; 
        del fillFlag_str
        #
        del aux_avg_ADU2e; del aux_avg_ADU0
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        APy3_GENfuns.showIt()
    #
    elif nextstep in ['^']:
        APy3_GENfuns.printcol("Easter Egg: for each row: overwrite with overall average, for Gn {0}".format(GnToProc),'green')
        aux_avg_ADU2e= numpy.nanmean(interpData_ADU2e[GnToProc,:,:].flatten())
        aux_avg_ADU0= numpy.nanmean(interpData_ADU0[GnToProc,:,:].flatten())
        #
        APy3_GENfuns.printcol("ADU0: overwrite with the average?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            interpData_ADU0[GnToProc,:,32:]=aux_avg_ADU0
        del fillFlag_str
        #
        APy3_GENfuns.printcol("e/ADU: overwrite with the average?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            interpData_ADU2e[GnToProc,:,32:]=aux_avg_ADU2e
        del fillFlag_str
        #
        del aux_avg_ADU2e; del aux_avg_ADU0
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        APy3_GENfuns.showIt()
    #
    elif nextstep in ['/']:
        APy3_GENfuns.printcol("Easter Egg: for each row: fill with linear regression values along row, for Gn {0}".format(GnToProc),'green')
        #
        APy3_GENfuns.printcol("changing destination ROI: rows? [first:last]", 'black')
        Rows2dest_in= input() 
        if (len(Rows2dest_in)<1): APy3_GENfuns.printcol("will keep destination ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        elif Rows2dest_in in ['all','All','ALL',':','*','-1']: Rows2dest= numpy.arange(NRow); 
        else: Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
        #
        APy3_GENfuns.printcol("changing ROI: cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest_in in ['all','All','ALL',':','*','-1']: Cols2dest= numpy.arange(32,NCol); 
        else: Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
        #
        APy3_GENfuns.printcol("destination ROI is ({0}:{1},{2},{3}), current Gn is: {4}".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1],GnToProc), 'green')
        #
        APy3_GENfuns.printcol("ADU0: fill with linear regression values along rows?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            for thisRow in range(Rows2dest[0],Rows2dest[-1]+1):
                map2fit= ~numpy.isnan(interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                map2fill= numpy.isnan(interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                if numpy.sum(map2fit)>1:
                    x2fit= numpy.arange(Cols2dest[0],(Cols2dest[-1]+1))[map2fit]
                    y2fit= interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][map2fit]
                    (slope_fitted, offset_fitted)= APy3_FITfuns.linear_fit(x2fit,y2fit)
                    y_fitted= APy3_FITfuns.linear_fun(numpy.arange(Cols2dest[0],(Cols2dest[-1]+1)), slope_fitted, offset_fitted)
                    interpData_ADU0[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][map2fill]= y_fitted[map2fill]
                    del x2fit; del y2fit; del slope_fitted; del offset_fitted; del y_fitted
                del map2fit; del map2fill; 
        del fillFlag_str
        #
        APy3_GENfuns.printcol("e/ADU: fill with linear regression values along rows?", 'black')
        fillFlag_str=input()
        if APy3_GENfuns.isitYes(fillFlag_str):
            for thisRow in range(Rows2dest[0],Rows2dest[-1]+1):
                map2fit= ~numpy.isnan(interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                map2fill= numpy.isnan(interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)])
                if numpy.sum(map2fit)>1:
                    x2fit= numpy.arange(Cols2dest[0],(Cols2dest[-1]+1))[map2fit]
                    y2fit= interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][map2fit]
                    (slope_fitted, offset_fitted)= APy3_FITfuns.linear_fit(x2fit,y2fit)
                    y_fitted= APy3_FITfuns.linear_fun(numpy.arange(Cols2dest[0],(Cols2dest[-1]+1)), slope_fitted, offset_fitted)
                    interpData_ADU2e[GnToProc,thisRow,Cols2dest[0]:(Cols2dest[-1]+1)][map2fill]= y_fitted[map2fill]
                    del x2fit; del y2fit; del slope_fitted; del offset_fitted; del y_fitted
                del map2fit; del map2fill; 
        del fillFlag_str
        #
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData_ADU2e[GnToProc,:,:], False, 'col','row',"Gn{0}: e/ADU (elaborated)".format(iGn), True)
        APy3_GENfuns.plot_2D_all(interpData_ADU0[GnToProc,:,:], False, 'col','row',"Gn{0}: pedestal [ADU] (elaborated)".format(iGn), True)
        APy3_GENfuns.showIt()
    #
    elif nextstep in ['#']:
        APy3_GENfuns.printcol("Easter eggs:",'green')
        APy3_GENfuns.printcol("$: on e/ADU only: overwrite all non-nans with the average",'green')
        APy3_GENfuns.printcol("@: fill with overall average",'green')
        APy3_GENfuns.printcol("-: fill with average per row",'green')
        APy3_GENfuns.printcol("/: fill with an linear regression along row",'green')
        APy3_GENfuns.printcol("^: overwrite with overall average",'green')

    #
    APy3_GENfuns.printcol("Show [O]riginal/[I]nterpolated data / change source [R]OI or Gn / report [M]in-max-avg in source ROI,Gn / [D]elete values in a ROI/values [T]oo high or low / interpolate [number] cycles / fill with [A]verage/o[V]erwrite all with average in a destination ROI / upload a different [P]edestal/[S]lope / save to [F]ile / re[L]oad original source ROI / [E]nd", 'black')
    nextstep = input()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end", 'blue')
# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




