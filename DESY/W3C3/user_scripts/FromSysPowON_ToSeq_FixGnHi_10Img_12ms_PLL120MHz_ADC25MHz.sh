if [[ $1 = '--setpoint' ]] && [[ ${#2} -gt 4 ]]; then

percival-hl-configure-setpoints -i ./DESY/W3C3/config/05_Spreadsheets/DLS_Setpoint_Definitions.xls
percival-hl-system-command -c stop_acquisition
percival-hl-system-command -c exit_acquisition_armed_status

echo "change biases from standard-after-PowON-status to $2 Fixed Gain Hi no PGA"
percival-hl-scan-setpoints -i 08_1_CurrentBiases_ON_ready3T -f $2 -n 2 -d 500
percival-hl-set-channel -c VS_Vref_DB -v 0

echo "Load ADC25MHz, PLL120MHz, 3T,PGAB SequentialMode, 10 Images, 12ms integration"
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N06_120MHz_ACD25MHz.ini
# there is a questionmark about whether this should be N15 or N18
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N15_3T_ADC25MHz_PLL120MHz_SEQUENTIAL.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N15_pixel_10Img_12ms_SEQUENTIAL.ini

echo RESET DATA SYNCH STATUS...
# EXIT ARMED STATUS
percival-hl-system-command -c exit_acquisition_armed_status
# ASSERT CPNI FLAGS IN DEBUG REGISTERS
percival-hl-configure-sensor-debug -i ./DESY/W3C3/config/04_Sensor_Settings/SensorDebug_002_SET_CPNI.ini
# TOGGLE CPNI_EXT
percival-hl-set-system-setting -s ADVANCED_Enable_CPNI_EXT -v 1
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 2
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_Enable_CPNI_EXT -v 0
# DEASSERT ALL FLAGS IN DEBUG REGISTERS
percival-hl-configure-sensor-debug -i ./DESY/W3C3/config/04_Sensor_Settings/SensorDebug_000_SAFE_START.ini
# ENTER ARMED STATUS
percival-hl-system-command -c enter_acquisition_armed_status

echo  "DONE"
echo  "PLL120MHz,ADC25MHz, 10img, 12ms, 3T, PGAB"
echo  "SeqMod,dmuxSELswitching SeqMode,dmuxSELswitching"

else

  echo "you must specify the setpoint to be set with --setpoint NAME";
  exit 1;
fi
