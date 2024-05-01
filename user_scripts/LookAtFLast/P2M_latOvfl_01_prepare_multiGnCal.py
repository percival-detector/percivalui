# -*- coding: utf-8 -*-
"""
group Pedestal_ADU, e/ADU (Gn0) in std MultiGnCal.h5 file (NaN for Gn1,2)

# load environment python3 environment on cfeld-percival02
source /home/prcvlusr/PercAuxiliaryTools/Anaconda3/Anaconda3/bin/activate root
# or load environment on maxwell
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./P2M_latOvfl_01_prepare_multiGnCal.py
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
NGn=3
#
ERRint16=APy3_P2Mfuns.ERRint16 #-256 # negative value usable to track Gn/Crs/Fn from missing pack 
ERRBlw=APy3_P2Mfuns.ERRBlw #-0.1
ERRDLSraw=APy3_P2Mfuns.ERRDLSraw #65535 # forbidden uint16, usable to track "pixel" from missing pack
# ---
#
def read_warn_1xh5(filenamepath, path_2read):
    if APy3_GENfuns.notFound(filenamepath): APy3_GENfuns.printErr("not found: "+filenamepath)
    dataout= APy3_GENfuns.read_1xh5(filenamepath, path_2read)
    return dataout
# ---
#
#%% defaults for GUI window
#
#
#
'''
# BSI04, PGA04_2, 3TGn0, PGABBB
dflt_PedestalADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/avg_xGn/2020.03.16.18.07.51_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_012ms_1kdrk_Gn0_ADU_CDS_avg.h5'

dflt_e_per_ADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_fixGn0_PGABBB/PTCParam/2020.03.12_BSI04_Tm20_dmuxSELHi_biasBSI04_04_3T_PGABBB_(:,:)_x4pix_ADU2e.h5_0interpol.h5'

dflt_outFile= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi/LatOvflw_Param/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12_Gn0xx_MultiGnCal.h5'
'''
#
'''
# BSI04, PGA04_5, 3G(Gn0), PGA6BB
dflt_PedestalADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/avg_std/BSI04_PTC_Tm20_3of7ADC_biasBSI04_05_Gn0_PGA6_ODx.x_t012ms_500drk_CDS_avg.h5'
dflt_e_per_ADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/PTCParam/2020.05.14_BSI04_Tm20_dmuxSELHi_biasBSI04_05_3T_PGA666_(:,:)_xpix_ADU2e.h5'
dflt_outFile= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/PTCParam/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn0xx_2020.05.14_MultiGnCal.h5'
#'''
#
'''
# BSI04, PGA04_5, 3G(Gn0), PGA6BB
# alternate, bo interpol
dflt_PedestalADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/avg_std/BSI04_PTC_Tm20_3of7ADC_biasBSI04_05_Gn0_PGA6_ODx.x_t012ms_500drk_CDS_avg.h5'
dflt_e_per_ADU_Gn0_file= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/PTCParam/2020.05.14_BSI04_Tm20_dmuxSELHi_biasBSI04_05_3T_PGA666_(:,:)_xpix_ADU2e.h5_prelim.h5'
dflt_outFile= '/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_3of7ADC_biasBSI04_05_PGA6/PTCParam/'+'BSI04_Tm20_dmuxSELHi_biasBSI04_05_PGA6BB_Gn0xx_2020.05.14b_MultiGnCal.h5'
#'''
#
#'''
# BSI04, 7/7ADC, biasBSI04.5, PGA6BB 3G(Gn0)
# alternate, bo interpol
dflt_PedestalADU_Gn0_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/avg_xGn/"+"BSI04_Tm20_7of7_biasBSI04_05_3G_PGA6BB_ODx.x_t012ms_30drk_Gn0_ADU_CDS_avg.h5"
dflt_e_per_ADU_Gn0_file= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/PTC_BSI04_7of7ADC_biasBSI04_05_PGA6/PTCParam/"+"2020.06.10_BSI04_Tm20_7of7_biasBSI04.05_3T.PGA6_(:,:)_xpix_ADU2e.h5_asItComesFromScript.h5"
dflt_outFile= "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200505_000_BSI04_LatOvflw_PGA4or6BB/processed/LatOvflw_BSI04_7of7ADC_biasBSI04_05_PGA6BB/LatOvflw_Param/"+"BSI04_Tm20_7of7_biasBSI04.05_3G.PGA6BB_Gn0xx_2020.06.10_MultiGnCal.h5_prelim.h5"
#'''

#


#
dflt_showFlag='Y'
dflt_verboseFlag='Y'
# ---
#
#%% pack arguments for GUI window
GUIwin_arguments= []
GUIwin_arguments+= ['pedestal [ADU] Gn0 filepath'] 
GUIwin_arguments+= [dflt_PedestalADU_Gn0_file] 
GUIwin_arguments+= ['e/ADU Gn0 filepath'] 
GUIwin_arguments+= [dflt_e_per_ADU_Gn0_file] 
GUIwin_arguments+= ['output filepath'] 
GUIwin_arguments+= [dflt_outFile] 
GUIwin_arguments+= ['show? [Y/N]'] 
GUIwin_arguments+= [dflt_showFlag] 
GUIwin_arguments+= ['verbose? [Y/N]'] 
GUIwin_arguments+= [dflt_verboseFlag] 
#
# ---
#%% GUI window
GUIwin_arguments=tuple(GUIwin_arguments)
dataFromUser= APy3_GENfuns.my_GUIwin_text(GUIwin_arguments)
#
i_param=0
PedestalADU_Gn0_file= dataFromUser[i_param]; i_param+=1
e_per_ADU_Gn0_file= dataFromUser[i_param]; i_param+=1
outFile= dataFromUser[i_param]; i_param+=1
showFlag=     APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
verboseFlag= APy3_GENfuns.isitYes(dataFromUser[i_param]); i_param+=1
# ---
#
#%% what's up doc
if verboseFlag:
    APy3_GENfuns.printcol('will process Pedestal [ADU] Gn0 data from {0}'.format(PedestalADU_Gn0_file),'blue')
    APy3_GENfuns.printcol('will process e/ADU Gn0 data from {0}'.format(e_per_ADU_Gn0_file),'blue')
    APy3_GENfuns.printcol('will save to {0}'.format(outFile),'blue')
    if showFlag: APy3_GENfuns.printcol('will show maps','blue')
    APy3_GENfuns.printcol('verbose','blue')
    APy3_GENfuns.printcol("--  --  --  --",'blue')
# ---
#ls
#%% start
startTime = time.time()
if verboseFlag: APy3_GENfuns.printcol("script operations beginning for real at {0}".format(APy3_GENfuns.whatTimeIsIt()),'green')
#---
#% read data files
PedestalADU_multiGn= APy3_GENfuns.numpy_NaNs((NGn,NRow,NCol))
e_per_ADU_multiGn= APy3_GENfuns.numpy_NaNs((NGn,NRow,NCol))

PedestalADU_multiGn[0,:,:]= read_warn_1xh5(PedestalADU_Gn0_file, '/data/data')
e_per_ADU_multiGn[0,:,:]= read_warn_1xh5(e_per_ADU_Gn0_file, '/data/data')

if showFlag:
    for iGn in range(NGn):
        APy3_GENfuns.plot_2D_all(PedestalADU_multiGn[iGn,:,:],False, "col","row","Pedestal [ADU] Gn{0}".format(iGn), True)
        APy3_GENfuns.plot_2D_all(e_per_ADU_multiGn[iGn,:,:],  False, "col","row","e/ADU Gn{0}".format(iGn), True)
    APy3_GENfuns.showIt()

APy3_GENfuns.write_2xh5(outFile, 
           PedestalADU_multiGn, '/Pedestal_ADU/', 
           e_per_ADU_multiGn, '/e_per_ADU/')
if verboseFlag: APy3_GENfuns.printcol("data saved in {0} under /Pedestal_ADU/ , /e_per_ADU/".format(outFile),'green')



# ---
#%% that's all folks
APy3_GENfuns.printcol("done",'blue')
endTime=time.time()
APy3_GENfuns.printcol("script ended at {0}".format(APy3_GENfuns.whatTimeIsIt()),'blue')
for iaux in range(3): APy3_GENfuns.printcol("----------------",'blue')




