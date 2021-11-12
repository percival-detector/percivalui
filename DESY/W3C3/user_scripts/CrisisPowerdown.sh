
if [[ $1 = '-u0' ]] && [[ $2 -gt 5 ]]; then

#####################################################################################################
# always the commands in this block need to be executed
echo "EMERGENCY PERCIVAL POWERDOWN STARTED" 

echo "Exit armed status"
percival-hl-system-command -c stop_acquisition
percival-hl-system-command -c forced_stop_acquisition
percival-hl-system-command -c exit_acquisition_armed_status

echo "Loading settings (ini)..."
percival-hl-configure-clock-settings -i ./DESY/W3C3/config/01_Clock_Settings/ClockSettings_N00_SAFE_START.ini
percival-hl-configure-chip-readout-settings -i ./DESY/W3C3/config/02_Chip_Readout_Settings/ChipReadoutSettings_N00_SAFEstart.ini
percival-hl-configure-system-settings -i ./DESY/W3C3/config/03_System_Settings/SystemSettings_N00_SAFE_START.ini
echo "Loading settings (xls)..."
percival-hl-configure-control-groups -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Group_Definitions.xls
percival-hl-configure-monitor-groups -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Group_Definitions.xls
percival-hl-configure-setpoints -i ./DESY/W3C3/config/05_Spreadsheets/DESY_W3C3_Setpoint_Definitions.xls

#####################################################################################################

if [[ $2 -gt 1300 ]]; then
echo "1300mA actions:"
echo " Ramp down Current Biases..."
percival-hl-scan-setpoints -i 08_0_CurrentBiases_ON -f 07_0_VoltageReferences_ON -n 4 -d 2000
fi

if [[ $2 -gt 850 ]]; then
echo "850mA actions:"
echo " Ramp down Voltage references..."
percival-hl-scan-setpoints -i 07_0_VoltageReferences_ON -f 06_0_PixelVoltages_ON -n 4 -d 2000
echo " Ramp down PixelVoltages..."
percival-hl-scan-setpoints -i 06_0_PixelVoltages_ON -f 05_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 05_0_PixelVoltages_ON -f 04_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 04_0_PixelVoltages_ON -f 03_0_PixelVoltages_ON -n 4 -d 2000
percival-hl-scan-setpoints -i 03_0_PixelVoltages_ON -f 02_0_LVDS_ON -n 4 -d 2000
echo " disabling IOs"
percival-hl-system-command -c disable_LVDS_IOs
fi


if [[ $2 -gt 550 ]]; then
echo "550mA actions:"
echo " Ramp down Voltage Supplies and LVDS IOs..."
percival-hl-scan-setpoints -i 02_0_LVDS_ON -f 01_0_VDD_ON -n 4 -d 2000
fi


if [[ $2 -gt 100 ]]; then
echo "100mA actions:"
echo " setpoint 01 to 00"
percival-hl-scan-setpoints -i 01_0_VDD_ON -f 00_0_0V0A -n 4 -d 2000
fi


echo "EMERGENCY PERCIVAL POWERDOWN COMPLETED"
echo "now please power off Wiener"

else
    echo "help: this script powers down percival based on a u0 current in mA. Specify eg -u0 1000"
    echo " run it in the percivalui directory of the pc running odin_server"
fi

