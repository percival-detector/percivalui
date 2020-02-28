#!/bin/bash

echo "PERCIVAL POWERUP STARTED / DESY"
echo -e "Applies to detector head with sensor Wafer 3,Chip 3 \n"

echo "- Downloading device settings..."
percival-hl-download-channel-settings
percival-hl-system-command -c enable_global_monitoring

echo "- Loading initial safe status..."
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N00_SAFE_START.ini
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N00_SAFEstart.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N00_SAFE_START.ini

echo "- Preparing powerboard..."
percival-hl-system-command -c disable_LVDS_IOs
percival-hl-system-command -c stop_acquisition
percival-hl-system-command -c exit_acquisition_armed_status
percival-hl-system-command -c fast_disable_control_standby
percival-hl-system-command -c disable_startup_mode
percival-hl-initialise-channels
percival-hl-system-command -c fast_sensor_powerdown

echo "- Initializing..."
percival-hl-system-command -c disable_safety_actions
percival-hl-system-command -c enable_device_level_safety_controls
percival-hl-system-command -c enable_system_level_safety_controls
percival-hl-system-command -c enable_experimental_level_safety_controls
percival-hl-configure-control-groups -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Group_Definitions.xls
percival-hl-configure-monitor-groups -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Group_Definitions.xls
percival-hl-configure-setpoints -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Setpoint_Definitions.xls

echo "- Ramp UP Voltage Supplies and LVDS IOs..."
i=1
percival-hl-scan-setpoints -i 00_0_0V0A -f 01_0_VDD_ON_step_${i} -n 1 -d 2000

while [ $i -le 3 ]; do
	percival-hl-update-monitors
	read -p "Continue Ramp UP? [y, n]:" input
	if [[ $input == "n" || $input == "N" ]]; then
		echo "Ramp DOWN Voltage supplies to 0 V, 0 A..."
		percival-hl-scan-setpoints -i 01_0_VDD_ON_step_${i} -f 00_0_0V0A -n ${i} -d 2000
	
		exit 1
	elif [[ $input == "y" || $input == "Y" ]]; then
		echo "Continuing ramp UP voltage supplies"
		j=${i}
		i=$(( $i + 1 ))
		percival-hl-scan-setpoints -i 01_0_VDD_ON_step_${j}  -f 01_0_VDD_ON_step_${i} -n 1 -d 2000
	else
		echo "Wrong input, please enter [y, n]"
	fi
done

percival-hl-update-monitors
percival-hl-scan-setpoints -i 01_0_VDD_ON_step_4 -f 02_0_LVDS_ON -n 4 -d 2000
percival-hl-system-command -c enable_LVDS_IOs

echo "- Reset sensor"
percival-hl-system-command -c assert_sensor_Master_Reset
percival-hl-system-command -c deassert_sensor_Master_Reset

echo "- Ramp UP PixelVoltages..."
percival-hl-scan-setpoints -i 02_0_LVDS_ON -f 03_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 03_0_PixelVoltages_ON -f 04_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 04_0_PixelVoltages_ON -f 05_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 05_0_PixelVoltages_ON -f 06_0_PixelVoltages_ON -n 4 -d 2000

echo "- Ramp UP Voltage references..."
percival-hl-scan-setpoints -i 06_0_PixelVoltages_ON -f 07_0_VoltageReferences_ON -n 4 -d 2000

echo "- Ramp UP Current Biases..."
percival-hl-scan-setpoints -i 07_0_VoltageReferences_ON -f 08_0_CurrentBiases_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 08_0_CurrentBiases_ON -f 08_1_CurrentBiases_ON_ready3T -n 4 -d 2000
echo PERCIVAL POWERUP COMPLETED

echo "Additional operations:"
echo "- Load default operating status"
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N05_120MHz.ini
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N05_3T_120MHz.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N05_pixel_Test.ini

echo "- Enter armed status"
percival-hl-apply-sensor-roi
percival-hl-system-command -c enter_acquisition_armed_status
