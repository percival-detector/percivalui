#!/bin/bash

# this file: descramble, ADUcorr, CDS/CMA Gn0 if needed, LatOvflw to electron, save to 4 files
# use:
# ./<thisfile>.sh
# do NOT add spaces between = and variables!
# DO NOT use "xxx"+"yyy"

#using /asap3 files
inFolder="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/processed/example_of_data_processing/input_scrmbld/"
prefix_fl="2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_"
suffix_fl0="000000.h5"
suffix_fl1="000001.h5"
#
# note that 1st img is discarded so 248:499 will produce 249:499. 
# MUST use EVEN PAIRS (always start from even, always have an even image number). DO NOT start from an odd number!. 
# e.g. "248:499" is OK
# "249:499" is NOT OK (not start from even)
# "248:498" is NOT OK (not have an even image number)
# "249:498" is NOT OK (not start from even)
# 
Img000to249="000:249"
# will give 1:249
# note 249 is repeated as last of 1st and 1st of 2nd, same with  others
#
Img250to499="248:499"
# 249:499
#
Img500to749="498:749"
# 499:749
#
Img750to999="748:999"
# 749: 999
#
#using /asap3 files
ADCcor="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5"
#
#using /asap3 files
#MultiGnCal="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5"
MultiGnCal="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/CalibParamToUse/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELHi_biasBSI04_04_PGABBB_2020.03.12c_Gn012_MultiGnCal_excludeBadPix.h5"
#
#using /asap3 files
altPed="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/shared/Pedestals/2019.12.11.23.57.21_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5"
#
CMAcols="NONE"
CDSFlag="Y"
#
#using /asap3 folder
outFolder="/asap3/fs-ds-percival/gpfs/percival.sys.1/2020/data/11010234/processed/example_of_data_processing/output_electrons/"
#
#echo $inFolder  
#
sbatch ./sbatch_rawraw_2_e_partialset_xb.sh $inFolder $prefix_fl $suffix_fl0 $suffix_fl1 $outFolder $Img000to249 $ADCcor $MultiGnCal $altPed $CMAcols $CDSFlag
sbatch ./sbatch_rawraw_2_e_partialset_xb.sh $inFolder $prefix_fl $suffix_fl0 $suffix_fl1 $outFolder $Img250to499 $ADCcor $MultiGnCal $altPed $CMAcols $CDSFlag
sbatch ./sbatch_rawraw_2_e_partialset_xb.sh $inFolder $prefix_fl $suffix_fl0 $suffix_fl1 $outFolder $Img500to749 $ADCcor $MultiGnCal $altPed $CMAcols $CDSFlag
sbatch ./sbatch_rawraw_2_e_partialset_xb.sh $inFolder $prefix_fl $suffix_fl0 $suffix_fl1 $outFolder $Img750to999 $ADCcor $MultiGnCal $altPed $CMAcols $CDSFlag
#
# to check:
# squeue -u marras
# or: 
# ~/Utili/sbatch_showJobs.sh
#
# logfiles in .../sbatch_slurmWaste
#
# to abort:
# scancel -t PENDING -u marras

