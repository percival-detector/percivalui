#!/usr/bin/env python3

# Percival scan that does several acquisitions at different values

import sys
import argparse
import time
import numpy;
import math;

# do we use print or logger?
import percival_detector.log;
import percival_detector.carrier.const;
from percival_detector.scripts.util import DAQClient
from percival_detector.scripts.util import PercivalClient

# system_commands = "\n".join([name for name, tmp in list(percival_detector.carrier.const.SystemCmd.__members__.items())])
# use the root logger because it goes to console.
logger = percival_detector.log.logger("");
# make this a command line option?
verbose = False;

minScanTimeUs = 12000;

def start_acquisition(pc):
    # shall we move this to a method of pc?
    if verbose:
      print("starting acq.");
    # system commands go under the command 'cmd_system_command'
    system_command = percival_detector.carrier.const.SystemCmd['start_acquisition']
    result = pc.send_system_command(system_command, 'calib_scan')
    time.sleep(1.0)
   # print("Acquisition start response: {}".format(result));
    parse_responsePER(result);


def options():
    desc = "Script to perform an acquisition";
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    parser.add_argument("-l", "--label", default="PTCSCAN", help="filename labels (default PTCSCAN)")
    parser.add_argument("-n", "--nimages", default="1000", help="number of images per acquisition (default 1000)")
    parser.add_argument("--nacq", default="5", help="number of acquisitions in scan (default 5)")
    parser.add_argument("-o", "--outdir", default="/mnt/gpfs02/detectors/new/Percival/captures", help="folder for h5 files output (default /mnt/gpfs02/detectors/new/Percival/captures)")
    parser.add_argument("--no-capture", dest="capture", help="do not capture frames at DAQ", action="store_false", default=True);


    args = parser.parse_args()
    return args

def check_fp_status(dc):
    valid_check = True
    file_name = "";
    frames_writ = 0;
    writing = False;
    # We should have a valid connection to the FR adapter
    if dc:
        status_dict = dc.get_status();
        if 'value' in status_dict:
            fps = status_dict['value']
            for fp in fps:
                try:
                    frames_writ += fp['hdf']['frames_written'];
                    if(file_name==""):
                      file_name = fp['hdf']['file_name'][0:-10];
                    # due to a bug in the FR, I am not convinced this writing variable is valid.
                    writing |= fp['hdf']["writing"];
                except Exception as ex:
                    valid_check = False;
                    reason = "uh oh something wrong with your FP: {}".format(str(ex));
        else:
            valid_check = False;
            reason = "No status returned from the FP adapter";
    else:
        valid_check = False
                
    return valid_check, file_name, frames_writ, writing;

# these parse_response functions are pretty pointless and are legacy
def parse_responseDAQ(response):
    if verbose:
        print("DAQ Response: %s", response)
    # I think the daq responds with "value: [list of dictionaries]", so this does nothing.
    if response.get("error"):
        logger.error("Error Message: %s", response['error'])
        sys.exit(-1)

def parse_responsePER(response):
    if verbose:
        print("PER Response: %s", response)
    # response => Failed goes with the error, but this only checks that the command
    # has been queued.
    if response.get("error"):
        logger.error("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    global verbose;
    args = options();

    dc = DAQClient(args.address)
    pc = PercivalClient(args.address)

    if "combined" in args.label or "_" in args.label or args.label=="" or args.label[0].isdigit():
      print("error invalid label",args.label);
      exit(1);

    paramValues = []; out_suffix="sfx";
 
   # print("setting time values with geometric scaling");
    numsteps = int(args.nacq);
    tot = 1.0;
    r = 1 if numsteps==1 else math.exp(math.log(10)/(numsteps-1));
    for i in range(numsteps):
      paramValues.append(tot);
      tot *= r;
    out_suffix= 'ptcramp'

    pc.send_system_command(percival_detector.carrier.const.SystemCmd.stop_acquisition, 'ptc_script')
    pc.set_system_setting("ACQUISITION_Continuous_acquisition", 0);

    print("Starting scan sequence: exposure time {0:.0f} to {1:.0f} us, {2} steps".format(minScanTimeUs * paramValues[0], minScanTimeUs * paramValues[-1], len(paramValues)))

    print("setting DAQ nimages %s" % args.nimages);
    parse_responseDAQ(dc.set_frames(int(args.nimages))) # in DAQ

    # we should chase the type of this - int or string?
    parse_responsePER(pc.set_system_setting("ACQUISITION_Number_of_frames", args.nimages));

    print("setting file path %s" % args.outdir);
    # set output folder
    parse_responseDAQ(dc.set_file_path(args.outdir));

    for scanIdx, scanVal in enumerate(paramValues):
        tus = int(minScanTimeUs * scanVal);
        tint = tus * 100;

        out_midfix = str(tus).zfill(6);
        outFileName= "{}_{}us_{}".format(args.label,out_midfix,out_suffix);

        parse_responseDAQ(dc.set_file_name(outFileName));
        if args.capture:
          parse_responseDAQ(dc.start_writing())

        print("setting exposure time %06d us" % (tint // 100));
        # set integration time
        parse_responsePER(pc.set_system_setting("TRIGGERING_Repetition_rate", tint));
        start_acquisition(pc);

        time_to_run = 1.1 * tus * int(args.nimages) / 1e6;
        print("please wait {:.2f} secs to clear exposure time {}us".format(time_to_run, tus));
        time.sleep(time_to_run);
        
        need_to_wait = True;
        while(need_to_wait):
          vc, fn, fw, wting = check_fp_status(dc);
          if(vc and fn==outFileName and fw==int(args.nimages) and wting==False):
            need_to_wait = False;
          else:
            print("waiting...",fw," frames saved");
          time.sleep(1);

        print("saved as files {}....h5".format(outFileName));
        parse_responseDAQ(dc.stop_writing());

    print("The scan has completed.")

if __name__ == '__main__':
    main()
