#!/usr/bin/env python3

# Percival scan that does several acquisitions at different values

import sys
import argparse
import time
import numpy;

# do we use print or logger?
import percival.log;
import percival.carrier.const;
from percival.scripts.util import DAQClient
from percival.scripts.util import PercivalClient

# system_commands = "\n".join([name for name, tmp in list(percival.carrier.const.SystemCmd.__members__.items())])
# use the root logger because it goes to console.
logger = percival.log.logger("");
# make this a command line option
verbose = False;


def whatTimeIsIt():
    aux_timeId=  time.strftime("%Y.%m.%d.%H.%M.%S")
    return(aux_timeId)

def update_monitors(pc):
    result = pc.send_command('cmd_update_monitors',
                         'calib_scan')
    parse_responsePER(result);

def start_acquisition(pc):
    if verbose:
        logger.info("starting acq.");
    # system commands go under the command 'cmd_system_command'
    system_command = percival.carrier.const.SystemCmd['start_acquisition']
    result = pc.send_system_command(system_command, 'calib_scan')
    time.sleep(1.0)
   # logger.info("Acquisition start response: {}".format(result));
    parse_responsePER(result);

def set_vin(pc, paramVal):
    paramChannel= "VS_Vin";
    data = {
           'channel': paramChannel,
           'value': paramVal
    };
    logger.info("Writing Control Channel \'{}\' value = {}".format(paramChannel, paramVal))
    result = pc.send_command('cmd_set_channel',
                             'calib_scan',
                             arguments=data)

    parse_responsePER(result);
    time.sleep(1.0);


def options():
    desc = "Script to perform an acquisition";
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    parser.add_argument("-l", "--label", default="VINSCAN", help="filename labels (default VINSCAN)")
    parser.add_argument("-p", "--pattern", help="the scan pattern: fine, coarse or test (default coarse)", default="coarse");
    parser.add_argument("-n", "--nimages", default="10", help="number of images per acquisition (default 10)")
    parser.add_argument("-t", "--tint", default="1200000", help="integration time in 100MHz clk (default 1200000)")
    parser.add_argument("-o", "--outdir", default="/dls/detectors/Percival/captures", help="folder for h5 files output (default /dls/detectors/Percival/captures)")
    parser.add_argument("-v", "--verbose", help="verbose logging (default F)", action="store_true", default=False);
    parser.add_argument("--no-capture", dest="capture", help="do not capture frames at DAQ", action="store_false", default=True);


    args = parser.parse_args()
    return args

# these parse_response functions are pretty pointless and are legacy
def parse_responseDAQ(response):
    if verbose:
        logger.info("DAQ Response: %s", response)
    # I think the daq responds with "value: [list of dictionaries]", so this does nothing.
    if response.get("error"):
        logger.error("Error Message: %s", response['error'])
        sys.exit(-1)

def parse_responsePER(response):
    if verbose:
        logger.info("PER Response: %s", response)
    # response => Failed goes with the error, but this only checks that the command
    # has been queued.
    if response.get("error"):
        logger.error("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    global verbose;
    args = options();
    if args.verbose:
      verbose = True;

    dc = DAQClient(args.address)
    pc = PercivalClient(args.address)

    if verbose:
      logger.info(args)

    if "combined" in args.label or "_" in args.label or any(c.isdigit() for c in args.label):
      print("error invalid label",label);
      exit(1);

    paramValues = []; out_suffix="sfx";
    if args.pattern == "fine":
      logger.info("doing fine scan");
      # The fine scan needs to encompass only one coarse-value, and we choose one in the middle
      # of the range. The coarse ADC outputs 31 to 0 as we set the DAC in [10k,34k].
      # The width of this scan should be 1500 because moving the DAC by 750 moves the coarse-ADC by
      # 1 unit, and we expect some overlap.
      paramValues=numpy.arange(18300,21290+1,10).astype(int);
      out_suffix= 'fnramp'
    elif args.pattern == "coarse":
      logger.info("doing coarse scan");
      paramValues=numpy.arange(10000,33920+1,80).astype(int);
      out_suffix= 'crsramp'
    elif args.pattern == "test":
      logger.info("doing test scan");
      paramValues=numpy.arange(10000,31001,10000).astype(int);
      out_suffix= 'testramp'
    else:
      logger.error("unknown pattern %s", args.pattern);
      exit(1);

    logger.info("Starting scan sequence: VRST=Vin from {0} to {1}ADU, steps of {2}".format(paramValues[0], paramValues[-1], paramValues[1] - paramValues[0]))

    if verbose:
        logger.info("setting DAQ nimages %s", args.nimages);
    parse_responseDAQ(dc.set_frames(int(args.nimages))) # in DAQ
    # we should chase the type of this - int or string?
    parse_responsePER(pc.set_system_setting("ACQUISITION_Number_of_frames", args.nimages));

    if verbose:
        logger.info("setting file path %s", args.outdir);
    # set output folder
    parse_responseDAQ(dc.set_file_path(args.outdir));

    if verbose:
        logger.info("setting exposure time %d", int(args.tint));
    # set integration time
    parse_responsePER(pc.set_system_setting("TRIGGERING_Repetition_rate", int(args.tint)));

    for scanIdx, scanVal in enumerate(paramValues):
        out_midfix= str(scanVal).zfill(5);
        outFileName= "{}_{}_{}".format(args.label,out_midfix,out_suffix);

        parse_responseDAQ(dc.set_file_name(outFileName));
        if args.capture:
          parse_responseDAQ(dc.start_writing())
        parse_responseDAQ(dc.get_status())

        set_vin(pc, scanVal);
        time.sleep(float(4.0))
        start_acquisition(pc);

        time.sleep(float(2.0));
        logger.info("saved as files {}....h5".format(outFileName));
        parse_responseDAQ(dc.stop_writing());



    logger.info("The scan has completed.")

if __name__ == '__main__':
    main()
