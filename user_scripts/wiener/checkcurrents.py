#!/usr/bin/python

import sys
import time;
import os;
import subprocess;
import argparse;

# this script was written to query the wiener over snmp and read the currents, and
# check they are within acceptable limits. It has some command-line options:
# -pwbon checks currents appropriate for powerboard on
# -headon checks currents appropriate for chip powered
# its exit-code is 0 for ok, and 1 for fail.
# The checks were defined by Alessandro Marras, Desy

# could pull this from the environment?
WIENER_IP="172.23.16.179";

def qx(cmd):
   listy = cmd.split();
   output=subprocess.Popen(listy, stdout=subprocess.PIPE).communicate()[0];
   return output;

def fetch(key):
    str = "snmpget -v 2c -OqvU -m +WIENER-CRATE-MIB -c public {} {}".format(WIENER_IP, key);
    # if qx returns garbage, float() will throw and the script will exit(1).
    return float(qx(str));

parser = argparse.ArgumentParser(description="check voltages / currents on wiener");

parser.add_argument("-voltages", action="store_true", help="check terminal voltage levels u0-u101 are ok");
parser.add_argument("-pwbon", action="store_true", help="check currents ok for powerboard on");
parser.add_argument("-headon", action="store_true", help="check currents ok for head on");
parser.add_argument("-waddr", action="store", help="set wiener ip, defaults to 172.23.16.179");

args = parser.parse_args();

if args.waddr:
    WIENER_IP = args.waddr;
    print "wiener addr set to", WIENER_IP;

rc = 0;

if args.voltages:
    print "checking terminal voltages ok";
    volt = fetch("outputMeasurementTerminalVoltage.u0");
    if volt<3.6 or volt>4.2:
        print "Error v0 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u1");
    if volt<1.4 or volt>1.6:
        print "Error v1 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u2");
    if volt<2.6 or volt>3.0:
        print "Error v2 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u3");
    if volt<3.2 or volt>3.8:
        print "Error v3 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u4");
    if volt<5.7 or volt>6.3:
        print "Error v4 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u5");
    if volt<4.7 or volt>5.3:
        print "Error v5 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u6");
    if volt<3.1 or volt>3.5:
        print "Error v6 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u7");
    if volt<4.7 or volt>5.3:
        print "Error v7 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u100");
    if volt<7.5 or volt>8.5:
        print "Error v100 out of range", volt;
        rc += 1;
    volt = fetch("outputMeasurementTerminalVoltage.u101");
    if volt<7.5 or volt>8.5:
        print "Error v101 out of range", volt;
        rc += 1;


if args.pwbon:
    print "checking currents ok pwbon";
    cur = fetch("outputMeasurementCurrent.u0");
    if cur>0.010:
        print "Error current u0 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u1");
    if cur>0.010:
        print "Error current u1 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u2");
    if cur>0.010:
        print "Error current u2 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u3");
    if cur>0.010:
        print "Error current u3 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u4");
    if cur>0.020:
        print "Error current u4 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u5");
    if cur>0.080:
        print "Error current u5 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u6");
    if cur>0.020:
        print "Error current u6 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u7");
    if cur>0.020:
        print "Error current u7 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u100");
    if cur<0.125 or cur>0.175:
        print "Error current u100 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u101");
    if cur<0.125 or cur>0.175:
        print "Error current u101 out of range", cur;
        rc += 1;

if args.headon:
    print "checking currents ok headon";
    cur = fetch("outputMeasurementCurrent.u0");
    # upper bound is 2.6 for POWERUP and 2.8 for OPERATIONAL
    if cur<2.2 or cur>2.8:
        print "Error current u0 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u2");
    # lower bound is 500 for POWERUP and 450 for OPERATIONAL
    if cur<0.45 or cur>0.6:
        print "Error current u2 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u100");
    if cur>0.200:
        print "Error current u100 out of range", cur;
        rc += 1;
    cur = fetch("outputMeasurementCurrent.u101");
    if cur>0.200:
        print "Error current u101 out of range", cur;
        rc += 1;

if args.headon==False and args.pwbon==False and args.voltages==False:
    print "warning: script run but no action specified";
    
exit(rc);
