echo PERCIVAL POWERDOWN STARTED / DESY
echo Applies to detector head with sensor Wafer 3,Chip 3
echo

echo - Exit armed status
percival-hl-system-command -c stop_acquisition
percival-hl-system-command -c forced_stop_acquisition
percival-hl-system-command -c exit_acquisition_armed_status

echo - Loading initial safe status...
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N00_SAFE_START.ini
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N00_SAFEstart.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N00_SAFE_START.ini

echo - Ramp DOWN Current Biases...
percival-hl-scan-setpoints -i 08_0_CurrentBiases_ON -f 07_0_VoltageReferences_ON -n 4 -d 2000

echo - Ramp DOWN Voltage references...
percival-hl-scan-setpoints -i 07_0_VoltageReferences_ON -f 06_0_PixelVoltages_ON -n 4 -d 2000

echo - Ramp DOWN PixelVoltages...
percival-hl-scan-setpoints -i 06_0_PixelVoltages_ON -f 05_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 05_0_PixelVoltages_ON -f 04_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 04_0_PixelVoltages_ON -f 03_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 03_0_PixelVoltages_ON -f 02_0_LVDS_ON -n 4 -d 2000

echo - Ramp DOWN Voltage Supplies and LVDS IOs...
percival-hl-system-command -c disable_LVDS_IOs
percival-hl-scan-setpoints -i 02_0_LVDS_ON -f 01_0_VDD_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 01_0_VDD_ON -f 00_0_0V0A -n 4 -d 2000

echo PERCIVAL POWERDOWN COMPLETED
