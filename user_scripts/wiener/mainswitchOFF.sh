#!/bin/bash

# Switch the WIENER OFF

WIENER_IP=172.23.16.179

echo Switching the WIENER Power Supply OFF

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP sysMainSwitch.0 i 0

FAIL=$?
if [ $FAIL -eq 0 ]; then
echo Wiener Power-supply switched OFF
fi

exit $FAIL
