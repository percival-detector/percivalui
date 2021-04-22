#!/bin/bash

# Switch the WIENER On

WIENER_IP=172.23.16.179
# note that you need to have WIENER-CRATE-MIB.txt installed in /usr/share/snmp/mibs
# and that the first time you plug it in, you cant use this script to turn it on,
# you must use the physical switch.

echo Switching the WIENER Power Supply ON

# read -n1 -rsp $'Press any key to continue or Ctrl+C to exit...\n'

snmpset -v 2c -m +WIENER-CRATE-MIB -c guru $WIENER_IP sysMainSwitch.0 i 1

echo WIENER Power Supply switched ON
