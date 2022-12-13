'''
Created by Alan Greer
modified by me

example:
from sandbox: 

# save temp_data on cfeld-perc02:
python tool_PTC_acquisitions_v2.py -w 90 -n 500 -t "12:3:120" -p "BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_OD3.5_" -s "_500lgh" -d "/home/prcvlusr/PercAuxiliaryTools/temp_data/"
python tool_PTC_acquisitions_v2.py -w 90 -n 500 -t "12:3:120" -p "BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_ODx.x_" -s "_500drk" -d "/home/prcvlusr/PercAuxiliaryTools/temp_data/"

# save ramdisk for hidra:
python tool_PTC_acquisitions_v2.py -w 90 -n 500 -t "12:3:120" -p "BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_OD3.5_" -s "_500lgh" -d "/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/"
python tool_PTC_acquisitions_v2.py -w 90 -n 500 -t "12:3:120" -p "BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_ODx.x_" -s "_500drk" -d "/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/"

# loop on many tint (12ms, 15ms, 18, 21, ..., 120ms): 
# set filename as folder + prefix + int time in ms+ suffix 
# wait 1sec, acquire Nimg, 
# wait (inttime x2 x1000 + 120)sec [hidra]

Latovlfw example:
python tool_PTC_acquisitions_v2.py -w 10 -n 50 -t "12:1:200" -p "BSI04_Tm20_dmuxSELHi_biasBSI04_04_3G_PGABBB_OD2.0_" -s "_50lgh" -d "/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/"

'''


import sys
import argparse
import time
import logging
import numpy

from percival_detector.log import log
from percival_detector.carrier import const
from percival_detector.scripts.util import DAQClient
from percival_detector.scripts.util import PercivalClient

system_commands = "\n\t".join([name for name, tmp in list(const.SystemCmd.__members__.items())])

SCRIPT_NAME = "tool_PTC_aquisitions_v2.py"

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

def matlabLike_inttime_range2(matlabstring):
    '''
    uses the sensible matlab syntax instead of the python nonsense
    '4:2:16' means: [4,6,8,10,12,14,16]
    '12:2:20'[ms] => [1200000,1400000,1600000,1800000,1200000] [tint clk]
    '''
    clk_per_ms= 100000
    range_start= int(matlabstring.partition(':')[0])
    aux_next= matlabstring.partition(':')[-1]
    range_step= int(aux_next.partition(':')[0])
    range_end= int(aux_next.partition(':')[-1])
    #
    out_range= numpy.arange(range_start*clk_per_ms, (range_end*clk_per_ms)+1, range_step*clk_per_ms)
    return out_range
    
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
    parser.add_argument("-t", "--tintarray", default="12:2:20", help="images for each acquisition")
    parser.add_argument("-p", "--prefix", default="xxx", help="out file prefix")
    parser.add_argument("-s", "--suffix", default="xxx", help="out file suffix")
    parser.add_argument("-d", "--directory", default="xxx", help="outfile directory")

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
    #out_folder= '/ramdisk/cfel/fsds/labs/percival/2019/calibration/20190826_000_temp_data/scratch/'   # ramdisk for hidra
    out_folder= args.directory
    #
    #out_prefix= 'BSI04_Tm20_dmuxSELHi_biasBSI04_03_3T_PGA666_OD4.0_'
    out_prefix= args.prefix
    #
    #out_suffix= '_500lgh'
    #out_suffix= '_500drk'
    out_suffix= args.suffix
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
    #tintValAr=numpy.arange(1200000,12000000+1,300000).astype(int)
    #tint_ms= "12:130:3"
    tint_ms= args.tintarray
    tintValAr= matlabLike_inttime_range2(tint_ms)
    #
    #tintNameAr=numpy.arange(12,120+1,3).astype(int)
    tintNameAr= tintValAr/100000 
    #twait=(tintNameAr.astype(float)) + float(args.wait)  
    twait=(tintNameAr.astype(float)*(int(args.nimages))*2.0/1000.0) + float(args.wait)  


    # twait= ( tintValAr.astype(float) *2 *float(args.nimages) ) + float(args.wait)
    # e.g. for -w 90:
    # 500Imgx12ms (6 sec to acquire): wait 12sec + 90sec
    # 500Imgx120ms (60 sec to acquire): wait 120sec + 90sec
    ###########################################################################################################################

    print("starting scan sequence: tint from {0} to {1}clk, {2}Img each".format(tintValAr[0],tintValAr[-1],int(args.nimages)))
    print("int time in clk: "+ str(tintValAr))
    print("waiting times in sec: "+ str(twait))
    print("{0}Img each".format(int(args.nimages)))
    print("will save as: {0}{1}XXXms{2}".format(out_folder,out_prefix,out_suffix))
    print("will take approx {0}minutes to end".format(numpy.sum(twait)/60))
    input('Press enter to continue: ')
    print("-- -- -- --")

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
        print("saving as files {}....h5".format(outFileName))
        print("-")
        #time.sleep(float(args.wait))
        time.sleep(twait[itint])
    #
    print("The scan has completed :)")
    for iaux in range(3): print("-------------")

if __name__ == '__main__':
    main()
