echo -n "RESET DATA SYNCH for digital test 1 ..."
# you must have Percival in a Sequencing mode like 3ghml before running this script!
# If you dont, you may need to restart Percival as it gets confused about frame numbers.

# EXIT ARMED STATUS
percival-hl-system-command -c exit_acquisition_armed_status

# ASSERT debug_CPNI = 1 & debug_sr7SC = 1 FLAGS IN DEBUG REGISTERS
percival-hl-configure-sensor-debug -i ./DESY/W3C3/config/04_Sensor_Settings/SensorDebug_003_DigitalTest1.ini

# TOGGLE CPNI_EXT
percival-hl-set-system-setting -s ADVANCED_Enable_CPNI_EXT -v 1
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 2
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_Enable_CPNI_EXT -v 0

# as per digTest1
percival-hl-set-system-setting -s ADVANCED_CPNI_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_sr7SC_EXT_options -v 1
percival-hl-set-system-setting -s ADVANCED_Enable_sr7SC_EXT -v 1
percival-hl-set-system-setting -s ADVANCED_Enable_CPNI_EXT -v 1

# remain in that state 
# percival-hl-configure-sensor-debug -i ./DESY/W3C3/config/04_Sensor_Settings/SensorDebug_003_DigitalTest1.ini

# ENTER ARMED STATUS
percival-hl-system-command -c enter_acquisition_armed_status

# sr7DIn as per digital test 1
percival-hl-system-command -c deassert_sr7DIn_1
percival-hl-system-command -c assert_sr7DIn_0
echo  DONE



