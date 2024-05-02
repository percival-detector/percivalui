#!/bin/bash

# Switch the WIENER On

WIENER_IP=172.23.16.179
# note that you need to have WIENER-CRATE-MIB.txt installed in /usr/share/snmp/mibs
# and that the first time you plug it in, you can't use this script to turn it on,
# you must use the physical switch.

echo Switching the WIENER Power Supply ON

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP sysMainSwitch.0 i 1

FAIL=$?
if [ $FAIL -eq 0 ]; then
echo Wiener Power-supply switched ON
fi

exit $FAIL
