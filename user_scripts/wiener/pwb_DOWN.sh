

WIENER_IP=172.23.16.179

echo ramping DOWN voltages and switching OFF channels

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u0 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u1 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u2 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u3 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u4 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u5 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u6 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u7 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u100 F 0.0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputVoltage.u101 F 0.0

sleep 6s

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u0 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u1 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u2 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u3 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u4 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u5 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u6 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u7 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u100 i 0
snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP outputSwitch.u101 i 0

echo finished
