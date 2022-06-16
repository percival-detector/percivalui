#!/usr/bin/env python3

# Percival acquisition script which creates output files with timestamps.

import sys
import argparse
import time

import percival.log;
from percival.carrier import const
from percival.scripts.util import DAQClient
from percival.scripts.util import PercivalClient

# system_commands = "\n".join([name for name, tmp in list(percival.carrier.const.SystemCmd.__members__.items())])
# use the root logger because it goes to console.
logger = percival.log.logger("");
verbose = True;


def whatTimeIsIt():
    aux_timeId=  time.strftime("%Y.%m.%d.%H.%M.%S")
    return(aux_timeId)

def options():
    desc = "Script to perform an acquisition";
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    wait_time_help = "How long to pause gratuitously (default 1.0s)"
    parser.add_argument("-w", "--wait", action="store", default=1.0, help=wait_time_help)
    parser.add_argument("-l", "--label", default="XYZ", help="filename label (default XYZ)")
    parser.add_argument("-n", "--nimages", default="10", help="number of images to acquire (default 10)")
    parser.add_argument("-t", "--tint", default="1200000", help="integration time in 100MHz clk (default 1200000)")
    parser.add_argument("-o", "--outdir", default="/dls/detectors/Percival/captures", help="folder for h5 files output (default captures)")

    args = parser.parse_args()
    return args

def parse_response(response):
    if verbose:
        logger.info("Response: %s", response)
    if response.get("error"):
        logger.info("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    args = options();

    dc = DAQClient(args.address)
    pc = PercivalClient(args.address)

    if verbose:
      logger.info(args)

    result = pc.send_system_command(const.SystemCmd.stop_acquisition, 'aqu_script')

    if verbose:
        logger.info("setting DAQ nimages");
    # we need to set num frames in detector and daq.
    parse_response(dc.set_frames(int(args.nimages))) # in DAQ
    pc.set_system_setting("ACQUISITION_Continuous_acquisition", 0);
    pc.set_system_setting("ACQUISITION_Number_of_frames", args.nimages); # in detector

    if verbose:
        logger.info("setting file path");
    # set output folder
    parse_response(dc.set_file_path(args.outdir))

    # set output filename
    outFileName= whatTimeIsIt() +"_"+ args.label
    parse_response(dc.set_file_name(outFileName))

    # set integration time
    # we shd parse the response as it could be waiting for some other command to finish.
    pc.set_system_setting("TRIGGERING_Repetition_rate", int(args.tint));

    # ready to acquire; gratuitous pause
    time.sleep(float(args.wait))

    # open file
    parse_response(dc.start_writing())
    parse_response(dc.get_status())

    # acquire
    if verbose:
        logger.info("starting acq.");

    result = pc.send_system_command(const.SystemCmd.start_acquisition, 'aqu_script')
    time.sleep(float(args.wait))
    
    #print("Acquisition set response: {}".format(result))
    print("hopefully saving as files {}....h5".format(outFileName))
   # dc.stop_writing();

if __name__ == '__main__':
    main()
