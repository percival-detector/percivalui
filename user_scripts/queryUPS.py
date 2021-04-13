#!/usr/bin/env python

import threading;
import socket;
import time;
import json;
import os;
import os.path;
import requests;
import subprocess;
import serial;

def checkUPS():

    try:
    # this will raise if it cant open the device
        ser = serial.Serial("/dev/ttyUSB0", baudrate=2400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1);
        ser.write(b"Q1\r");
        reply = ser.read(47);
       # print reply;
        # we need a space before the zeros to make sure we match the first bit
        if(0 < reply.index(b" 0000000")):
            return True;            

    except Exception as e:
       # print e;
        pass;
        
    return False; 


if __name__ == "__main__":
    if checkUPS():
        print "UPS is ok";
    else:
        print "UPS IS UNPOWERED OR DISCONNECTED";  
    










