'''
Created by Alan Greer
modified by me

example
python tool_acquire_wdate.py -w 0.1 -p test -n 100 -t 1200000

set filename, wait 1sec, acquire 100 img, wait 1sec

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

def whatTimeIsIt():
    aux_timeId=  time.strftime("%Y.%m.%d.%H.%M.%S")
    return(aux_timeId)
### ## ### ######## ###

def options():
    desc = """Test script to demonstrate starting an acquisition
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    wait_time_help = "How long (seconds) to pause between each scan point (default 5.0)"
    parser.add_argument("-w", "--wait", action="store", default=0.1, help=wait_time_help)
    parser.add_argument("-p", "--prefix", default="XXX", help="file prefix")
    parser.add_argument("-n", "--nimages", default="10", help="number of images to acquire")
    parser.add_argument("-t", "--tint", default="1200000", help="integration time in 100MHz clk")

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

    # set output folder and prefix, set DAQ nimages
    parse_response(dc.set_frames(int(args.nimages))) # in DAQ
    change_NImg(int(args.nimages), folder_percivalui, folder_sandbox) # in cntrl

    # set output folder
    out_folder= '/home/prcvlusr/PercAuxiliaryTools/temp_data/'
    parse_response(dc.set_file_path(out_folder))

    # set output filename
    outFileName= whatTimeIsIt() +"_"+ args.prefix
    parse_response(dc.set_file_name(outFileName))

    # set tint
    change_tint(int(args.tint), folder_percivalui, folder_sandbox)

    # ready to acquire
    time.sleep(float(args.wait))

    # open file
    parse_response(dc.start_writing())
    parse_response(dc.get_status())

    # acquire
    system_command = const.SystemCmd['start_acquisition']
    result = pc.send_system_command(system_command, 'hl_system_command.py', wait=(args.wait.lower() == "true"))
    time.sleep(float(args.wait))
    
    #print("Acquisition set response: {}".format(result))
    print("saved as files {}....h5".format(outFileName))
    # that's all folks

if __name__ == '__main__':
    main()
