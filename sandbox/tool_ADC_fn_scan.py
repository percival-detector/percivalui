'''
Created by Alan Greer
modified by me

example:
from sandbox: 

python tool_ADC_crs_scan.py -w 7 --nimages=10
loop on many bias values: set filename, set new bias, wait 7sec, acquire 10 img, wait 3sec
'''




import sys
import argparse
import time
import logging
import numpy

from percival.log import log
from percival.carrier import const
from percival.scripts.util import DAQClient
from percival.scripts.util import PercivalClient

system_commands = "\n\t".join([name for name, tmp in list(const.SystemCmd.__members__.items())])

SCRIPT_NAME = "tool_ADC_fn_scan.py"

############################################################################################################################
### parameters ###

#tint=12ms
integr_time_to_use= 1200000 

# set output folder and prefix, set DAQ nimages
out_folder= '/home/prcvlusr/PercAuxiliaryTools/temp_data/'   # temp_data on cfeld-perc02
#out_folder= '/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/'  # ramdisk on cfeld-perc02

out_prefix= '2019.11.20_BSI04_Tm20_dmuxSELHi_BSI04_02_VRST_PGABBB_VRSTfromVin'

paramChannel= "VS_Vin"

# test ramp: VRSTfromVin= 10000,20000,30000 ADU
#paramValAr=numpy.arange(0,2+1,1).astype(int)
#paramValAr=numpy.arange(10000,12000+1,1000).astype(int)
#paramValAr=numpy.arange(10000,30000+1,10000).astype(int); out_suffix= '_10adc_testramp'

# crs ramp: VRSTfromVin= 10000->33920ADU (300 steps of 80 ADU each) 
#paramValAr=numpy.arange(10000,33920+1,80).astype(int); out_suffix= '_10adc_crsramp'

# fn ramp: VRSTfromVin= 18300->21290ADU (300 steps of 10 ADU each) 
paramValAr=numpy.arange(18300,21290+1,10).astype(int); out_suffix= '_10adc_fnramp'
###########################################################################################################################

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

def update_monitors(folder_percivalui, folder_sandbox):
    """ update-monitors """
    # cd to folder_percivalui
    aux_cmd= "cd "+folder_percivalui
    os.system(aux_cmd)
    # cd to folder_percivalui
    aux_cmd= "percival-hl-update-monitors"
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

    print("starting scan sequence: VRSTfromVin from {0} to {1}ADU, {2}Img each".format(paramValAr[0],paramValAr[-1],int(args.nimages)))

    parse_response(dc.set_frames(int(args.nimages)))
    parse_response(dc.set_file_path(out_folder))

    # set command nimages
    change_NImg(int(args.nimages), folder_percivalui, folder_sandbox)
    
    # set integration time
    change_tint(integr_time_to_use, folder_percivalui, folder_sandbox)
    print("new integration time {0}clk".format(integr_time_to_use))

    #time.sleep(float(args.wait))
    time.sleep(float(1.0))

    for ipar,this_paramVal in enumerate(paramValAr):
        # set out filename
        out_midfix= str(this_paramVal).zfill(4)
        outFileName=out_prefix+out_midfix+out_suffix
        parse_response(dc.set_file_name(outFileName))
        # --- 
        # open file
        parse_response(dc.start_writing())
        parse_response(dc.get_status())
        # ---
        # change Vin
        data = {
               'channel': paramChannel,
               'value': this_paramVal
        }
        print("Writing Control Channel \'{}\' value = {}".format(paramChannel, this_paramVal))
        result = pc.send_command('cmd_set_channel',
                                 'hl_set_channel.py',
                                 arguments=data,
                                 wait=(args.wait.lower() == "true"))
        print("Channel set response: {}".format(result))
        time.sleep(float(args.wait))
        # ---
        # update monitors
        #update_monitors(folder_percivalui, folder_sandbox)
        # ---
        time.sleep(float(1.0))
        #
        system_command = const.SystemCmd['start_acquisition']
        result = pc.send_system_command(system_command, 'hl_system_command.py', wait=(args.wait.lower() == "true"))
        print("Acquisition set response: {}".format(result))
        print("saved as files {}....h5".format(outFileName))
        time.sleep(float(2.0))

    print("The scan has completed :)")

if __name__ == '__main__':
    main()
