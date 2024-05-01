# -*- coding: utf-8 -*-
"""
incomplete array (NaN= missing data) => interpolate using valid 1st-neighbours 

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_PTC_02_filler.py
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
#
def read_warn_1xh5(filenamepath, path_2read):
    if APy3_GENfuns.notFound(filenamepath): printErr("not found: "+filenamepath)
    dataout= APy3_GENfuns.read_1xh5(filenamepath, path_2read)
    return dataout
# ---
#
#%% defaults for GUI window
#dflt_file2interpolate= '/gpfs/cfel/fsds/labs/percival/2019/calibration/20191122_000_BSI04_PTC/processed/BSI04_dmuxSELHi_biasBSI04_03_3T_PGA666_PTC/v1/PTCParam/'+'prelim_2019.11.27_BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_(:,:)_x1pix_ADU2e.h5'

dflt_file2interpolate= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/PTCParam/2020.05.14_BSI04_Tm20_dmuxSELHi_biasBSI04_05_3T_PGA666_(:,:)_xpix_ADU2e.h5'



#dflt_Rows2proc='400:1000'  
#dflt_Cols2proc='400:1000'
#dflt_Rows2proc='700:1100'  
#dflt_Cols2proc='500:735'
dflt_Rows2proc='0:1483'  
dflt_Cols2proc='32:1439'

# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['use data from file'] 
GUIwin_arguments+= [dflt_file2interpolate] 
#
GUIwin_arguments+= ['process data: in Rows [from:to]'] 
GUIwin_arguments+= [dflt_Rows2proc] 
GUIwin_arguments+= ['process data: in columns [from:to]'] 
GUIwin_arguments+= [dflt_Cols2proc] 
#
#GUIwin_arguments+= ['interpolation cycles'] 
#GUIwin_arguments+= [dflt_interpCycles] 
#
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
file2interpolate= dataFromUser[i_param]; i_param+=1
#
Rows2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Rows2proc_mtlb in ['all','All','ALL',':','*','-1']: Rows2proc= numpy.arange(NRow)
else: Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_mtlb) 

Cols2proc_mtlb= dataFromUser[i_param]; i_param+=1; 
if Cols2proc_mtlb in ['all','All','ALL',':','*','-1']: Cols2proc= numpy.arange(NCol)
else: Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_mtlb)

#interpCycles= int(dataFromUser[i_param]); i_param+=1;
# ---
#
#%% what's up doc
APy3_GENfuns.printcol('will process data from '+file2interpolate,'blue')
APy3_GENfuns.printcol('will elaborate Cols {0}, Rows {1}'.format(Cols2proc_mtlb,Rows2proc_mtlb),'blue')
#APy3_GENfuns.printcol('will interpolate {0} cycles at a time'.format(interpCycles),'blue')
APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#
#%% start
startTime = time.time()
APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#% read data files
indata= read_warn_1xh5(file2interpolate, '/data/data')

def aux_copyvals(indata, Rows2proc,Cols2proc):
    ''' from indata to interpData:
        cp only ROI, nan the rest '''
    interpData= APy3_GENfuns.numpy_NaNs_like(indata)
    for iRow in Rows2proc:
        for iCol in Cols2proc:
            interpData[iRow,iCol]= indata[iRow,iCol]  
    return interpData

interpData= aux_copyvals(indata, Rows2proc,Cols2proc)

#---
orig_Rows2proc= numpy.copy(Rows2proc)
orig_Cols2proc= numpy.copy(Cols2proc)
totInterpCounter=0

APy3_GENfuns.printcol("Show [O]riginal/[I]nterpolated data / change source [R]OI / report [M]in-max-avg in source ROI / [D]elete ROI/values [T]oo high or too low / interpolate [number] of cycles / fill with [A]verage/o[V]erwrite all with average in a destination ROI / save to [F]ile / re[L]oad original / [E]nd", 'black')
nextstep = input()
#
while nextstep not in ['e','E','q','Q']:
    matplotlib.pyplot.close()
    #
    if nextstep in ['o','O']: 
        APy3_GENfuns.printcol("showing original array, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(indata, False, 'col','row','original data', True) 
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['i','I']: 
        APy3_GENfuns.printcol("showing interpolated array, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    elif nextstep in ['r','R']: 
        APy3_GENfuns.printcol("current source ROI is ({0}:{1},{2},{3})".format(Rows2proc[0],Rows2proc[-1],Cols2proc[0],Cols2proc[-1]), 'green')
        APy3_GENfuns.printcol("changing source ROI: rows? [first:last]", 'black')
        Rows2proc_in= input() 
        if (len(Rows2proc_in)<1): APy3_GENfuns.printcol("will keep source ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        elif Rows2proc_in in ['all','All','ALL',':','*','-1']: 
            Rows2proc= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change source ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        else: 
            Rows2proc=APy3_GENfuns.matlabLike_range(Rows2proc_in)
            APy3_GENfuns.printcol("will change source ROI: rows [{0}:{1}]".format(Rows2proc[0],Rows2proc[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing source ROI: cols? [first:last]", 'black')
        Cols2proc_in= input() 
        if (len(Cols2proc_in)<1): APy3_GENfuns.printcol("will source keep ROI: Cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        elif Cols2proc_in in ['all','All','ALL',':','*','-1']: 
            Cols2proc= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change source ROI: cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        else: 
            Cols2proc=APy3_GENfuns.matlabLike_range(Cols2proc_in)
            APy3_GENfuns.printcol("will change ROI: cols [{0}:{1}]".format(Cols2proc[0],Cols2proc[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        old_interpData= numpy.copy(interpData)
        interpData= aux_copyvals(old_interpData, Rows2proc,Cols2proc)
        del old_interpData
        APy3_GENfuns.printcol("showing interpolated array, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after ROI resizing', True) 
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
        #
    elif nextstep in ['m','M']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        APy3_GENfuns.printcol("current ROI to evaluate is ({0}:{1},{2}:{3})".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1]), 'black')
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
        APy3_GENfuns.printcol("current sub-ROI to evaluate is ({0}:{1},{2}:{3})".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1]), 'green')
        #
        minval= numpy.nanmin(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        minvaladdr= numpy.unravel_index(numpy.nanargmin(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]), interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("min val in sub-ROI is {0} in ({1},{2})".format(minval,minvaladdr[0]+Rows2avg[0],minvaladdr[1]+Cols2avg[0]), 'green')
        #
        maxval= numpy.nanmax(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten())
        maxvaladdr= numpy.unravel_index(numpy.nanargmax(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)]), interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].shape)
        APy3_GENfuns.printcol("max val in sub-ROI is {0} in ({1},{2})".format(maxval,maxvaladdr[0]+Rows2avg[0],maxvaladdr[1]+Cols2avg[0]), 'green')
        #
        avgval= numpy.nanmean(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("avg val in sub-ROI is {0}".format(avgval), 'green')
        #
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    # 
    elif nextstep in ['d','D']:
        APy3_GENfuns.printcol("will delete values in a ROI", 'black')
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
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change deletion ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("deletion ROI is ({0}:{1},{2},{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'green')
        interpData[Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= numpy.NaN      
        # 
        APy3_GENfuns.printcol("showing after deleting, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData[:,:], False, 'col','row',"data after deletion", True)
        matplotlib.pyplot.show(block=True) 
    # 
    elif nextstep in ['t','T']:
        APy3_GENfuns.printcol("will delete values too high or too low", 'black')
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
        else: 
            Rows2dest=APy3_GENfuns.matlabLike_range(Rows2dest_in)
            APy3_GENfuns.printcol("will change deletion ROI: rows [{0}:{1}]".format(Rows2dest[0],Rows2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing ROI: deletion cols? [first:last]", 'black')
        Cols2dest_in= input() 
        if (len(Cols2dest_in)<1): APy3_GENfuns.printcol("will keep ROI: Cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        elif Cols2dest in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change deletion ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change deletion ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("deletion ROI is ({0}:{1},{2},{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'green')
        #
        minval= numpy.nanmin(interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)].flatten())
        minvaladdr= numpy.unravel_index(numpy.nanargmin(interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)]), interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)].shape)
        APy3_GENfuns.printcol("min val in sub-ROI is {0} in ({1},{2})".format(minval,minvaladdr[0]+Rows2dest[0],minvaladdr[1]+Cols2dest[0]), 'green')
        #
        maxval= numpy.nanmax(interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)].flatten())
        maxvaladdr= numpy.unravel_index(numpy.nanargmax(interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)]), interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)].shape)
        APy3_GENfuns.printcol("max val in sub-ROI is {0} in ({1},{2})".format(maxval,maxvaladdr[0]+Rows2dest[0],maxvaladdr[1]+Cols2dest[0]), 'green')
        #
        avgval= numpy.nanmean(interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("avg val in sub-ROI is {0}".format(avgval), 'green')
        #
        minOKval= minval*0.9
        maxOKval= maxval*1.1
        #
        APy3_GENfuns.printcol("-", 'green')
        APy3_GENfuns.printcol("min acceptable value?", 'black')
        minOKval_in= input()
        if (len(minOKval_in)<1): APy3_GENfuns.printcol("will min acceptable value: {0}".format(minOKval), 'green')
        else: 
            minOKval=float(minOKval_in)
            APy3_GENfuns.printcol("will delete all values in the sub-ROI <{0}".format(minOKval), 'green')
        #
        APy3_GENfuns.printcol("max acceptable value?", 'black')
        maxOKval_in= input()
        if (len(maxOKval_in)<1): APy3_GENfuns.printcol("will max acceptable value: {0}".format(maxOKval), 'green')
        else: 
            maxOKval=float(maxOKval_in)
            APy3_GENfuns.printcol("will delete all values in the sub-ROI >{0}".format(maxOKval), 'green')
        #
        tooLow_map= interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)]<minOKval
        interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)][tooLow_map]= numpy.NaN
        tooHigh_map= interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)]>maxOKval
        interpData[Rows2dest[0]:(Rows2dest[-1])+1,Cols2dest[0]:(Cols2dest[-1]+1)][tooHigh_map]= numpy.NaN
        APy3_GENfuns.printcol("{0} points below min, {1} points above max have been removed".format(numpy.sum(tooLow_map),numpy.sum(tooHigh_map)), 'green')   
        # 
        APy3_GENfuns.printcol("showing after deleting, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData[:,:], False, 'col','row',"data after deletion", True)
        matplotlib.pyplot.show(block=True) 
    # 
    elif nextstep.isdigit(): 
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        APy3_GENfuns.printcol("current ROI to interpolate is ({0}:{1},{2}:{3})".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1]), 'black')
        APy3_GENfuns.printcol("changing sub-ROI to average: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to average: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("interpolating the missing values within the sub-ROI:", 'black')
        NCycles= int(nextstep)
        for iCycle in range(NCycles):
            if numpy.sum( numpy.isnan(interpData[Rows2avg[0]:(Rows2avg[-1]+1),Cols2avg[0]:(Cols2avg[-1]+1)]) )!=0:
                totInterpCounter+=1
                for iRow in Rows2avg:
                    for iCol in Cols2avg:
                        if numpy.isnan(interpData[iRow,iCol]):
                            aux_fromCol= iCol-1; aux_toColp1= iCol+1+1; aux_fromRow= iRow-1; aux_toRowp1= iRow+1+1;
                            if iRow==Rows2avg[0]: aux_fromRow=iRow
                            if iCol==Cols2avg[0]: aux_fromCol=iCol
                            if iRow==Rows2avg[-1]: aux_toRowp1=iRow+1
                            if iCol==Cols2avg[-1]: aux_toColp1=iCol+1
                            aux_val= numpy.nanmean(interpData[aux_fromRow:aux_toRowp1,aux_fromCol:aux_toColp1].flatten())
                            interpData[iRow,iCol]=aux_val
                    APy3_GENfuns.dot_every10th(iRow,len(Rows2avg))
            else: APy3_GENfuns.printcol("nothing to interpolate in the sub-ROI", 'black')
        APy3_GENfuns.printcol("\nshowing after interpolation, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    # 
    elif nextstep in ['a','A']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        APy3_GENfuns.printcol("current ROI to avg is ({0}:{1},{2}:{3})".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1]), 'black')
        APy3_GENfuns.printcol("changing sub-ROI to average: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to average: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        avgval= numpy.nanmean(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("average within the defined subROI ({0}:{1},{2},{3}): {4}".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1],avgval), 'black')
        APy3_GENfuns.printcol("will fill empty pixels in destination ROI in Gn{0} with said average", 'black')
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
        elif Cols2dest in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("destination destination ROI is ({0}:{1},{2},{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'green')
        #
        interpData[Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)][numpy.isnan(interpData[Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1) ])]= avgval   
        APy3_GENfuns.printcol("showing after filling, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        matplotlib.pyplot.show(block=True) 
    # 
    elif nextstep in ['v','V']:
        Rows2avg=numpy.copy(Rows2proc)
        Cols2avg=numpy.copy(Cols2proc)
        APy3_GENfuns.printcol("current ROI to avg is ({0}:{1},{2}:{3})".format(Rows2avg[0],Rows2avg[-1],Cols2avg[0],Cols2avg[-1]), 'black')
        APy3_GENfuns.printcol("changing sub-ROI to average: rows? [first:last]", 'black')
        Rows2avg_in= input() 
        if (len(Rows2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')

        elif Rows2avg_in in ['all','All','ALL',':','*','-1']: 
            Rows2avg= numpy.arange(NRow); 
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        else: 
            Rows2avg=APy3_GENfuns.matlabLike_range(Rows2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: rows [{0}:{1}]".format(Rows2avg[0],Rows2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("changing sub-ROI to average: cols? [first:last]", 'black')
        Cols2avg_in= input() 
        if (len(Cols2avg_in)<1): APy3_GENfuns.printcol("will keep sub-ROI to average: Cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        elif Cols2avg_in in ['all','All','ALL',':','*','-1']: 
            Cols2avg= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        else: 
            Cols2avg=APy3_GENfuns.matlabLike_range(Cols2avg_in)
            APy3_GENfuns.printcol("will change sub-ROI to average: cols [{0}:{1}]".format(Cols2avg[0],Cols2avg[-1]), 'green')
        #
        APy3_GENfuns.printcol("-", 'green')
        avgval= numpy.nanmean(interpData[Rows2avg[0]:(Rows2avg[-1])+1,Cols2avg[0]:(Cols2avg[-1]+1)].flatten()) 
        APy3_GENfuns.printcol("average within the source sub-ROI ({0}:{1},{2},{3}): {4}".format(Rows2proc[0],Rows2proc[-1],Cols2proc[0],Cols2proc[-1],avgval), 'black')
        APy3_GENfuns.printcol("will overwrite destination ROI with said average", 'black')
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
        elif Cols2dest in ['all','All','ALL',':','*','-1']: 
            Cols2dest= numpy.arange(32,NCol); 
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        else: 
            Cols2dest=APy3_GENfuns.matlabLike_range(Cols2dest_in)
            APy3_GENfuns.printcol("will change destination ROI: cols [{0}:{1}]".format(Cols2dest[0],Cols2dest[-1]), 'green')
        #
        APy3_GENfuns.printcol("destination destination ROI is ({0}:{1},{2},{3})".format(Rows2dest[0],Rows2dest[-1],Cols2dest[0],Cols2dest[-1]), 'green')
        #
        interpData[Rows2dest[0]:(Rows2dest[-1]+1),Cols2dest[0]:(Cols2dest[-1]+1)]= avgval   

        APy3_GENfuns.printcol("showing after overwriting, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        matplotlib.pyplot.show(block=True) 
    #
    elif nextstep in ['f','F']: 
        outFileNamePath=file2interpolate+'_{0}interpol.h5'.format(totInterpCounter)
        APy3_GENfuns.write_1xh5(outFileNamePath, interpData, '/data/data')
        APy3_GENfuns.printcol("interp file saved: {0}".format(outFileNamePath), 'black')
    #
    elif nextstep in ['l','L']:
        APy3_GENfuns.printcol("reloading original values, resetting the ROI to original values", 'black')
        Rows2proc= numpy.copy(orig_Rows2proc)
        Cols2proc= numpy.copy(orig_Cols2proc)
        interpData= aux_copyvals(indata,Rows2proc,Cols2proc)
        totInterpCounter=0
        #
        APy3_GENfuns.printcol("showing after reloading, close image to move on", 'black')
        APy3_GENfuns.plot_2D_all(interpData, False, 'col','row','data after {0} interpolation'.format(totInterpCounter), True) 
        #APy3_GENfuns.maximize_plot()
        matplotlib.pyplot.show(block=True) # to allow for interactive zoom
    #
    APy3_GENfuns.printcol("Show [O]riginal/[I]nterpolated data / change source [R]OI / report [M]in-max-avg in source ROI / [D]elete ROI/values [T]oo high or too low / interpolate [number] of cycles / fill with [A]verage/o[V]erwrite all with average in a destination ROI / save to [F]ile / re[L]oad original / [E]nd", 'black')
    nextstep = input()
    if nextstep in ['e','E','q','Q']: APy3_GENfuns.printcol("end", 'blue')
# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




