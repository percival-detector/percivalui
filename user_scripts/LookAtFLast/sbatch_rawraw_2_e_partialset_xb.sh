#!/bin/bash
#SBATCH --partition=cfel
#SBATCH --nodes=1                                 # Number of nodes
#SBATCH --job-name  rawraw_2_e_partialset
#SBATCH --chdir   /home/marras/PercAuxiliaryTools/LookAtFLast/sbatch_slurmWaste    # directory must already exist!

cd ..
source /usr/share/Modules/init/sh
module load anaconda/3
python3 ./sbatch_rawraw_2_e_partialset_xb.py $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11}
#
# this file: descramble, ADUcorr, CDS/CMA Gn0 if needed, LatOvflw to electron, save to file
#1 input folder
#2 prefix file
#3,4 scrmbld suffix
#5 output folder
#6 Img to process
#7 ADCcor file
#8 MultiGn file
#9 Gn0 alternate pedestal
#10 Gn0 CMA?
#11 Gn0 CDS?
# could be used as:
# sbatch ./sbatch_rawraw_2_e_partialset_xb.sh "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/shared/timingTest/1kImg/scrmbld/" "2019.12.11.23.54.58_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kpin_" "000000.h5"  "000001.h5" "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/shared/timingTest/1kImg/data_e/" "0:249" "/gpfs/cfel/fsds/labs/percival/2019/calibration/20190612_000_CalibrationParametersToUse/processed/BSI04/BSI04_Tm20/BSI04_Tm20_dmuxSELsw_H0,H1_ADCcor/BSI04_Tminus20_dmuxSELsw_2019.11.20_ADCcor.h5" "/gpfs/cfel/fsds/labs/percival/2020/calibration/20200312_000_BSI04_dynamicRange/processed/fullWell_ramp_LatOvflow3G_PGABBB_dmuxSELHi_v2/LatOvflw_Param/BSI04_Tm20_dmuxSELHi_biasBSI04_02_PGABBB_2020.03.12b_Gn012_MultiGnCal.h5" "/gpfs/cfel/fsds/labs/percival/2019/experiment/20191210_000_Petra3_P04_JPLBSI04/shared/timingTest/1kImg/Ped/2019.12.11.23.57.21_BSI04_7of7_3GPGABBB_120ms_0250eV_5um_1kdrk_Gn0_CDS_avg.h5" "NONE" "Y"
