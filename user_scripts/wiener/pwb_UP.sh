
# for each channel, we need to set several things.
# our policy is to disable the supervisor functions cos they can switch the channel off.
# we care about the ramp speed, the final voltage and the current limit
# we don't know what state the channels are in when we start; we don't reset them in case
# this is dangerous.

export WIENER_IP=172.23.16.179

echo ramping UP voltages and switching ON channels

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u0 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u0 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u0 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u0  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u0  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u0 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u0 F 3.9	 
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u0 F 3
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u0 i 1
		
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u1 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u1 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u1 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u1  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u1  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u1 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u1 F 1.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u1 F 0.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u1 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u2 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u2 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u2 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u2  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u2  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u2 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u2 F 2.8
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u2 F 1.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u2 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u3 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u3 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u3 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u3  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u3  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u3 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u3 F 3.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u3 F 1
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u3 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u4 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u4 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u4 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u4  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u4  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u4 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u4 F 6
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u4 F 0.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u4 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u5 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u5 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u5 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u5  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u5  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u5 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u5 F 5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u5 F 0.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u5 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u6 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u6 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u6 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u6  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u6  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u6 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u6 F 3.3
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u6 F 0.1
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u6 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u7 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u7 F 1.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u7 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u7  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u7  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u7 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u7 F 5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u7 F 0.5
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u7 i 1

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u100 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u100 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u100 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u100  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u100  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u100 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u100 F 8		 
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u100 F 0.3
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u100 i 1
		
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageRiseRate.u101 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltageFallRate.u101 F 2.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxTerminalVoltage.u101 F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMinSenseVoltage.u101  F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxSenseVoltage.u101  F 15.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSupervisionMaxCurrent.u101 F 5.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u101 F 8
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputCurrent.u101 F 0.4
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u101 i 1

sleep 6s

echo finished
