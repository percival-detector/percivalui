#!/usr/bin/env python3

# Percival acquisition script which puts the .

import sys
import argparse
import time

import percival.log;
import logging;
from percival.carrier import const
from percival.scripts.util import DAQClient
from percival.scripts.util import PercivalClient

# system_commands = "\n".join([name for name, tmp in list(percival.carrier.const.SystemCmd.__members__.items())])
# use the root logger because it goes to console.
logger = percival.log.logger("tool_ca");
logger.setLevel(logging.INFO);


def whatTimeIsIt():
    aux_timeId=  time.strftime("%Y.%m.%d.%H.%M.%S")
    return(aux_timeId)

def options():
    desc = "Script to put Percival into / outof continuous acquisition";
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")

    wait_time_help = "How long to pause gratuitously (default 1.0s)"
    parser.add_argument("-w", "--wait", action="store", default=1.0, help=wait_time_help)
    # todo add integration time here
    parser.add_argument("--start-continuous-acq", action="store_true", default=False, dest="start", help="put it into cont acq mode")
    parser.add_argument("--stop-continuous-acq", action="store_true", default=False, dest="stop", help="end cont. acquisition")
    parser.add_argument("-t", "--tint", default="1200000", help="integration time in 100MHz clk (default 1200000)")

    args = parser.parse_args()
    return args

def parse_response(response):

    logger.info("Response: %s", response)
    if response.get("error"):
        logger.info("Error Message: %s", response['error'])
        sys.exit(-1)


def main():
    args = options();

    pc = PercivalClient(args.address)

    logger.info(args)
    logger.info("stopping acquistion.");

    result = pc.send_system_command(const.SystemCmd.stop_acquisition, 'aqu_script')

    if(args.start and args.stop):
      logger.error("error, can not start and stop both");
      exit(1);

    if(args.start==False and args.stop==False):
      logger.error("error, specify start or stop");
      exit(1);

    logger.info("setting cont acqu to %d", 0 if args.stop else 1);
    pc.set_system_setting("ACQUISITION_Continuous_acquisition", 0 if args.stop else 1);

    # set integration time
    # we shd parse the response as it could be waiting for some other command to finish.
    pc.set_system_setting("TRIGGERING_Repetition_rate", int(args.tint));

    # ready to acquire; gratuitous pause
    time.sleep(float(args.wait))

    if args.start:
      # acquire
      logger.info("setting tint to %s and starting acquitision", args.tint);
      result = pc.set_system_setting("TRIGGERING_Repetition_rate", int(args.tint));
      result = pc.send_system_command(const.SystemCmd.start_acquisition, 'aqu_script')
    time.sleep(float(args.wait))
    
    #print("Acquisition set response: {}".format(result))
    print("Percival in cont acquisition state:", 0 if args.stop else 1)


if __name__ == '__main__':
    main()

