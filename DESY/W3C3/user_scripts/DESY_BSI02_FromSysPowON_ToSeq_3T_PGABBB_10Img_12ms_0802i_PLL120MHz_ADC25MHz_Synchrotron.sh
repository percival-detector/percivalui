percival-hl-system-command -c stop_acquisition
percival-hl-system-command -c exit_acquisition_armed_status

echo change biases from standard-after-PowON-status to 08_2i-status , BSI02 3T  
percival-hl-scan-setpoints -i 08_1_CurrentBiases_ON_ready3T -f 08_2i_BSI02_3T -n 4 -d 2000

echo Load ADC25MHz, PLL120MHz, 3T,PGAB SequentialMode, 10 Images, 12ms integration
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N06_120MHz_ACD25MHz.ini
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N15_3T_ADC25MHz_PLL120MHz_SEQUENTIAL.ini
#percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N15_pixel_10Img_12ms_SEQUENTIAL.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N18_pixel_10Img_12ms_SeqMod_Synchrotron.ini

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
echo  "PLL120MHz,ADC25MHz PLL120MHz,ADC25MHz PLL120MHz,ADC25MHz"
echo  "SeqMod,dmuxSELswitching SeqMode,dmuxSELswitching"
echo  "10img,12ms 10img,12ms 10img,12ms 10img,12ms 10img,12ms 10img,12ms"
echo  "3T,PGAB,0802i(BSI2) 3T,PGAB,0802i(BSI2) 3T,PGAB,0802i(BSI2)"
