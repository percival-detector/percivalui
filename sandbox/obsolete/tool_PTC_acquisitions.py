'''
Created by Alan Greer
modified by me

example:
from sandbox: 

python tool_PTC_acquisitions.py -w 6 --nimages=10
loop on many tint: set filename, wait 1sec, acquire 10 img, wait 6sec

python tool_PTC_acquisitions.py -w 150 --nimages=500
loop on many tint: set filename, wait 1sec, acquire 500 img, wait 150sec

python tool_PTC_acquisitions.py -w 210 --nimages=500
loop on many tint: set filename, wait 1sec, acquire 500 img, wait 210sec [hidra]

python tool_PTC_acquisitions.py -w 120 --nimages=500
loop on many tint: set filename, wait 1sec, acquire 500 img, wait (inttime x2 x1000 + 120)sec [hidra]


'''
from __future__ import print_function

import sys
import argparse
import time
import logging
import numpy

from percival.log import log
from percival.carrier import const
from percival.scripts.util import DAQClient
from percival.scripts.util import PercivalClient

system_commands = "\n\t".join([name for name, tmp in const.SystemCmd.__members__.items()])

SCRIPT_NAME = "tool_PTC_aquisitions.py"

### my own commands ###
import os

folder_percivalui= "/home/prcvlusr/percival/percivalui/"
folder_sandbox=    "/home/prcvlusr/percival/percivalui/sandbox/"

def change_tint(tint, folder_percivalui, folder_sandbox):
    """ change integration time to tint [clk] """
    # cd to folder_percivalui
    aux_cmd= "cd "+folder_percivalui
    os.system(aux_cmd)
    # cd to folder_percivalui
    aux_cmd= "percival-hl-set-system-setting -s TRIGGERING_Repetition_rate -v " + str(tint)
    os.system(aux_cmd)
    # cd to folder_percivalui
    aux_cmd= "cd "+folder_sandbox
    os.system(aux_cmd)
    return

def change_NImg(NImg, folder_percivalui, folder_sandbox):
    """ change number-of-images-to-be acquired to NImg """
    # cd to folder_percivalui
    aux_cmd= "cd "+folder_percivalui
    os.system(aux_cmd)
    # cd to folder_percivalui
    aux_cmd= "percival-hl-set-system-setting -s ACQUISITION_Number_of_frames -v " + str(NImg)
    os.system(aux_cmd)
    # cd to folder_percivalui
    aux_cmd= "cd "+folder_sandbox
    os.system(aux_cmd)
    return
### ## ### ######## ###

def options():
    desc = """Test script to demonstrate starting an acquisition
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    wait_time_help = "How long (seconds) to pause between each scan point (default 5.0)"
    parser.add_argument("-w", "--wait", action="store", default=5.0, help=wait_time_help)
    parser.add_argument("-n", "--nimages", default="20", help="images for each acquisition")

    args = parser.parse_args()
    return args

def parse_response(response):
    log.info("Response: %s", response)
    if 'error' in response:
        log.info("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    args = options()

    log.setLevel(logging.DEBUG)
    dc = DAQClient(args.address)

    pc = PercivalClient(args.address)

    #log.info("Test FP")
    log.info(args)

    ############################################################################################################################
    # set output folder and prefix, set DAQ nimages
    #out_folder= '/home/prcvlusr/PercAuxiliaryTools/temp_data/'   # temp_data on cfeld-perc02
    out_folder= '/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/'   # ramdisk for hidra
    out_prefix= 'BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_OD4.0_'
    out_suffix= '_500lgh'
    #out_suffix= '_500drk'
    #out_suffix= '_10lgh'
    #
    # 12ms,13,14,...,300ms
    #tintNameAr=numpy.arange(12,300+1,1).astype(int)
    #tintValAr=numpy.arange(1200000,30000000+1,100000).astype(int)
    #
    # 15ms,20,25,...,100ms
    #tintNameAr=numpy.arange(15,100+1,5).astype(int)
    #tintValAr=numpy.arange(1500000,10000000+1,500000).astype(int)
    #
    # 12ms,14,16,18,20,...,120ms
    tintNameAr=numpy.arange(12,120+1,3).astype(int)
    tintValAr=numpy.arange(1200000,12000000+1,300000).astype(int)
    twait=tintNameAr.astype(float) + float(args.wait)  
    # twait= ( tintValAr.astype(float) *2.0 *float(args.nimages) ) + float(args.wait)
    # e.g. for -w 120:
    # 500Imgx12ms (6 sec to acquire): wait 12sec + 2 min
    # 500Imgx120ms (60 sec to acquire): wait 120sec + 2 min
    ###########################################################################################################################

    print("starting scan sequence: tint from {0} to {1}clk, {2}Img each".format(tintValAr[0],tintValAr[-1],int(args.nimages)))

    parse_response(dc.set_frames(int(args.nimages)))
    parse_response(dc.set_file_path(out_folder))

    # set command nimages
    change_NImg(int(args.nimages), folder_percivalui, folder_sandbox)
    # --- 
    #time.sleep(float(args.wait))
    time.sleep(float(1.0))

    for itint,this_tintName in enumerate(tintNameAr):
        # set out filename
        out_midfix= "t"+str(this_tintName).zfill(3)+"ms"
        outFileName=out_prefix+out_midfix+out_suffix
        parse_response(dc.set_file_name(outFileName))
        # --- 
        # open file
        parse_response(dc.start_writing())
        parse_response(dc.get_status())
        # ---
        # set integration time
        change_tint(tintValAr[itint], folder_percivalui, folder_sandbox)
        print("new integration time {0}clk, ={1}ms".format(tintValAr[itint],this_tintName))
        # ---
        #time.sleep(float(args.wait))
        time.sleep(float(1.0))
        # ---
        #
        system_command = const.SystemCmd['start_acquisition']
        result = pc.send_system_command(system_command, 'hl_system_command.py', wait=(args.wait.lower() == "true"))
        print("Acquisition set response: {}".format(result))
        print("saved as files {}....h5".format(outFileName))
        #time.sleep(float(args.wait))
        time.sleep(twait[itint])

    print("The scan has completed :)")

if __name__ == '__main__':
    main()
