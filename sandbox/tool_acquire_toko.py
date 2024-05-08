#!/usr/bin/env python3

""" This script was originally written by Toko Hirono, Desy.
    It is a complex acquisition script that also gathers settings from the detector
    and saves them in an h5 file. It supports doing several acquisitions to scan
    over a range of values.
"""
from __future__ import print_function

import sys
import os
import time
import argparse
from datetime import datetime
import numpy as np
import h5py
import json
import requests
import socket 

from percival_detector.carrier import const
from percival_detector.scripts.util import DAQClient
from percival_detector.scripts.util import PercivalClient

SCRIPT_NAME = os.path.basename(__file__)


####################### Option ########################
def options():
    desc = """Tool for Percival Data Acquisition
      <Example>
      N images: {0} -n <N>
      PTC scan, save to 'raw'(Hidra): {0} -n 500 -d /ramdisk/current/raw -p TRIGGERING_Repetition_rate -s 12:3:300ms -f Gh
      VRST ramp with PwBv2, save to 'processed' directly:  {0} -n 10 -d /gpfs/current/processed -p VS_Vref_spare -s 10000:10:40000
      N images X times: {0} -n <N> -s <X>
    """.format(SCRIPT_NAME)
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--address", action="store", default="127.0.0.1:8888",
                        help="Odin server address (default 127.0.0.1:8888)")
    parser.add_argument("-f", "--fname", default="", help="additional prefix for the file name. File name=<time stamp>_[this arg]_<scan index>_<000000|000001>.h5 default=''")
    parser.add_argument("-n", "--nimages", default=10, help="images for each acquisition: default=10")
    parser.add_argument("-t", "--integration", default="1199999", 
                        help="integration time. if 'ms' after float value, then the value will be calculated into 100MHzclk and subtracted by 1. min is 12ms and max is 300ms : e.g. 12ms, 29999999, default=1199999")
    parser.add_argument("-p", "--param", default="",
                        help="Scan Parameter: e.g. TRIGGERING_Repetition_rate, VS_Vref_spare")
    parser.add_argument("-s", "--scan", default="", 
                        help="Scan Range (start:step:stop) or int n(just repeat n times): e.g. 12:3:300ms (PTC), 10000:10:40000 (Vspare)")
    parser.add_argument("-d", "--directory", default="/home/prcvlusr/PercAuxiliaryTools/temp_data", 
                        help="outfile directory: e.g. /ramdisk/current/raw (<100GB) /gpfs/current/processed (>100GB) default=/home/prcvlusr/PercAuxiliaryTools/temp_data")
    parser.add_argument("--timeout", default=0, help="timeout in sec: default=60s for Untrig, for Triggered mode, inf")
    parser.add_argument("--nblocks", default=100, help="blocks_per_file: default=100, 0=no file splitting)")
 # try to delete this.   parser.add_argument("--savemeta", default='every', help="dont know all=settings&monitors, every=all+settings@each step")
    parser.add_argument("--debug", default=0, help="debug flg")
    parser.add_argument("--plsgen", default=False, help="is plsgen there? default=False")
    parser.add_argument("--p04sock", default=None, help="Address:Port e.g. 'haspp04g01:48123' default=None")
    args = parser.parse_args()

    # integration time in ms/clk
    if args.integration[-2:] =="ms":
        args.integration = int(float(args.integration[:-2])*100000.)-1
    # scan range
    if args.scan=="" and args.param=="":
        args.scan = np.arange(1)
    elif args.param=="": ## and args.scan!=""
        args.scan = np.arange(int(args.scan))
    else:                 ## args.param !=""
        start,step,stop = args.scan.split(":")
        if stop[-2:] =="ms":
            # convert acquisition time to 100mhz clock
            start = int(float(start)*100000.)-1
            step = int(float(step)*100000.)
            stop =int(float(stop[:-2])*100000.)-1
        else:
            start = int(start)
            step = int(step)
            stop = int(stop)
        args.scan = np.arange(start, stop, step)
        if args.scan[-1] != stop:
            args.scan = np.append(args.scan, stop)
    args.timeout = float(args.timeout)
    # file and directory
    if args.fname!='':
        args.fname='_'+args.fname
    #args.fname = datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")[:-3]+ args.fname
    args.fname = time.strftime("%Y%m%d_%H%M%S") + args.fname
    args.directory = os.path.join(args.directory, args.fname)
    os.system('mkdir -p {0:s}'.format(args.directory))
    os.system('ssh prcvlusr@cfeld-percival02 "mkdir -p {0:s}"'.format(args.directory)) 

    return args

############## This convenience function gets several status items from the adapter
### and amalgamates them into a dictionary. Monitors come with get_status().
def get_all_settings(pc):
    pc.send_command("cmd_update_monitors", wait=False)
    pc.wait_for_command_completion(0.1)  # this takes about 3s

    all_settings = {};
    res = pc.get_status("system_settings");
    all_settings.update(res);
    res = pc.get_status("clock_settings");
    all_settings.update(res);
    res = pc.get_status("chip_readout_settings");
    all_settings.update(res);
    res = pc.get_status("sensor_debug");
    all_settings.update(res);
    res = pc.get_status("channel_values");
    all_settings.update(res);
    res = pc.get_status("status");
    all_settings.update(res);
    return all_settings;


################ h5 meta file
def create_metafile(fname, t0, status, scan_param, scan_len, everystep=False):
    with h5py.File(fname, "w") as f:
        meta = f.create_group("meta_data")
        moni = meta.create_group("monitor")
        if everystep==True:
            meta_len=scan_len+1
        else:
            meta_len=1
        for kk, vv in status.items():
            if vv is None:
                continue
            dt = [('time','f8'),('id','i')]
            tname = kk
            #fix dtype
            #print(kk, type(vv), vv)
            for k, v in vv.items():
                if k == u'error' or isinstance(v, dict):
                    vv[k] = json.dumps(v)
                    dt.append((k.encode('ascii'), 'S{}'.format(len(vv[k])*2)))
                elif k == u'Train_number':
                    dt.append((k.encode('ascii'), 'u8'))
                elif isinstance(v, list):
                    vv[k] = np.array(v)
                    dt.append((k.encode('ascii'), vv[k].dtype, vv[k].shape))
                elif isinstance(v, type(u'')):
                    vv[k] = v.encode('ascii')
                    dt.append((k.encode('ascii'), 'S{}'.format(len(vv[k])*2)))
                else:  # isinstance(v, int) or isinstance(v, float):
                    dt.append((k.encode('ascii'), np.dtype(type(v))))
            # create talbe
            v_array = np.empty(1, dtype=dt)
            if tname in ['clock_settings','detector','system_settings','chip_readout_settings','sensor_debug','channel_settings']:
                tbl = meta.create_dataset(tname, (meta_len,), dtype=v_array.dtype, compression='gzip')
            elif tname in ['fr0', 'fr1','fp0', 'fp1',]:
                tbl = meta.create_dataset(tname, (meta_len,), dtype=v_array.dtype, compression='gzip')
            elif tname in ['frfp1_config', 'frfp0_config','plsgen']:
                tbl = meta.create_dataset(tname, (1,), dtype=v_array.dtype, compression='gzip')
            else:
                tbl = moni.create_dataset(tname, (1,), dtype=v_array.dtype, compression='gzip')
            # fill the first values
            v_array[0]['time'] = t0
            v_array[0]['id'] = -1
            for k, v in vv.items():
                v_array[0][k] = v
            tbl[0]= v_array[0]
        meta.create_dataset('scan', (scan_len,), 
                          dtype=np.dtype([('time', 'f8'),(scan_param,'i'),('fname','S128')]),
                          compression='gzip')

def append_metafile(fname, idx, tme, scan_value, outFileName, status=None):
    with h5py.File(fname, "a") as f:
      # meta_data/scan is indexed triples (time, fieldname, filename).
      f['/meta_data/scan'][idx,'time'] = tme
      f['/meta_data/scan'][idx, f['/meta_data/scan'].dtype.names[1]] = scan_value
      f['/meta_data/scan'][idx, 'fname'] = outFileName
      if status is not None:
          # this stores under metadata/status_class, a row for each idx, containing
          # (time, fieldname)
          # effectively dumping the status dict to a depth of TWO.
          for kk, vv in status.items():
            tname = '/meta_data/{0:s}'.format(kk)
            if tname in f:
                v_array = np.zeros(1,dtype=f[tname].dtype)
                v_array[0]['time'] = tme
                v_array[0]['id'] = idx
                for k, v in vv.items():
                    if isinstance(v, type(u'')):
                        v = v.encode('ascii')
                    elif k == u'error' or isinstance(v, dict):
                        v = json.dumps(v)
                    elif isinstance(v, list):
                        v = np.array(v) 
                    v_array[0][k] = v
                # I don't know why they're using idx+1 here.
                f[tname][idx+1]= v_array[0]
            else:
                print("no", tname, "in meta file")

################ ODIN utils
def parse_response(response):
    if 'error' in response and response['error']!='':
        print("Error Message:", response['error'])
        sys.exit(-1)

def wait_for_writing(dc, waiting_status, timeout=60., interval=0.2):
        read_count = 0
        while read_count<(timeout/interval) or timeout<0: 
            response = dc.get_status()
            fps = response['value']
            writing = [waiting_status]
            for fp in fps:
                writing.append(fp['hdf']['writing'])
            if all(writing) or not any(writing):
                return response
            #print("DAQ ready ?", "wait for", waiting_status, "read_count", read_count, writing, "<", timeout/interval)
            time.sleep(interval)
            read_count = read_count + 1
        ## stop writting
        response['error']="timeout, waiting for busy"+str(waiting_status)
        return response

def get_fr_status(addr="127.0.0.1:8888"):
    url="http://"+addr+"/api/0.1/fr/status"
    res = requests.get(url,
          headers={ 'Content-Type': 'application/json',
                    'Accept': 'application/json'
          }).json()
    return res

def get_frfp_config(addr="127.0.0.1:8888"):
    url="http://"+addr+"/api/0.1/fr/config"
    res = requests.get(url,
          headers={ 'Content-Type': 'application/json',
                    'Accept': 'application/json'
          }).json()
    url="http://"+addr+"/api/0.1/fp/config"
    tmp = requests.get(url,
          headers={ 'Content-Type': 'application/json',
                    'Accept': 'application/json'
          }).json()
    res["value"][0].update(tmp["value"][0])
    res["value"][1].update(tmp["value"][1])
    return res

################ P04sock-server
def send_p04sock(data, host, port):
    data_b = data.encode('ascii') + b'\r\n'
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(data_b)
        res=b""
        while True:
            res_tmp=s.recv(1)
            res = res + res_tmp
            if res_tmp == b'\n':
                break
    except:
        return "ERROR p04sock"
    finally:
        s.close()
    if res != b'OK\n':
        print("ERROR p04sock", res.decode('ascii'))
        sys.exit()
    return res.decode('ascii')

################ PlsGen
def send_plsgen(cmd_list):
    try:
        s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.37.230", 5025))
        res_list = []
        for cmd in cmd_list:
            s.sendall(cmd+b'\n')
            if b'?' in cmd:  # 0x3f = '?' # get reply if ? in command
                res=b""
                while True:
                    res_tmp=s.recv(1)
                    res = res + res_tmp
                    if res_tmp==b'\n':
                        break
                res_list.append(res)
            else:
                res_list.append(None)
    except:
        res_list.append(b'ERROR pulse gen.')
    finally:
        s.close()
    return res_list


################ Main
def main():

    start_tme = time.time()

    args = options()
    dc = DAQClient(args.address)
    pc = PercivalClient(args.address)
    BIG_status_lookup = {}

    # Reset DAQ
    parse_response(dc.send_command('hdf/write', '0'))
    dc.send_reset_stats()
    res = wait_for_writing(dc, waiting_status=False)

    # set blocks_per_file
    parse_response(dc.send_command('hdf/process/blocks_per_file', 
                                   '{}'.format(int(args.nblocks))))
    # set output folder
    parse_response(dc.set_file_path(args.directory))

    # get config/status
    BIG_status_lookup['fp0'] = res['value'][0]
    BIG_status_lookup['fp1'] = res['value'][1]
    res = get_frfp_config(args.address)
    BIG_status_lookup['frfp0_config'] = res['value'][0]
    BIG_status_lookup['frfp1_config'] = res['value'][1]
    res = get_fr_status(args.address)
    BIG_status_lookup['fr0'] = res['value'][0]
    BIG_status_lookup['fr1'] = res['value'][1]
    pc.wait_for_command_completion(0.01)
    res = get_all_settings(pc);
    BIG_status_lookup.update(res)

    ############# get config from plsgen
    npls = 0
    if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_source']:
      if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_mode']==1:
          npls = BIG_status_lookup['system_settings']['TRIGGERING_number_of_frames_per_trigger']
      else:
          npls = 1
      if args.plsgen:
        res_plsgen = send_plsgen([b'C1:BTWV?'])[0].decode('ascii')
        try:
            npls = int(res_plsgen.split(',')[5]) * npls
        except:
            print('!!!!!!!!!!!!ERROR pulse gen!!!!!!!!!!!!!!')
            print(res_plsgen)
            print('!!!!!!!!!!!!ERROR pulse gen!!!!!!!!!!!!!!')
            sys.exit()
        BIG_status_lookup['plsgen'] = {}
        BIG_status_lookup['plsgen']['C1'] = res_plsgen
    #############

    # set nimages
    if not BIG_status_lookup['system_settings']['ACQUISITION_Continuous_acquisition']:
        parse_response(pc.send_command(
          'cmd_system_setting',
          SCRIPT_NAME,
          arguments={'setting': 'ACQUISITION_Number_of_frames', 'value': int(args.nimages)},
          wait=False))
    parse_response(dc.set_frames(int(args.nimages))) # in DAQ

    # set exposure time
    if args.param == 'TRIGGERING_Repetition_rate':
       pass
    elif BIG_status_lookup['system_settings']['TRIGGERING_Trigger_mode']:
        if BIG_status_lookup['system_settings']['TRIGGERING_Burst_period'] != int(args.integration):
            pc.wait_for_command_completion(0.01)
            parse_response(pc.send_command(
               'cmd_system_setting',
               SCRIPT_NAME,
               arguments={'setting': 'TRIGGERING_Burst_period', 'value':int(args.integration)},
               wait=False))
    elif BIG_status_lookup['system_settings']['TRIGGERING_Repetition_rate'] != int(args.integration):
        pc.wait_for_command_completion(0.01)
        parse_response(pc.send_command(
           'cmd_system_setting',
           SCRIPT_NAME,
           arguments={'setting': 'TRIGGERING_Repetition_rate', 'value':int(args.integration)},
           wait=False))
    ## set timeout
    if args.timeout==0:
        if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_mode']:
            timeout = -1
        else:
            timeout = 60
    else:
        timeout = args.timeout

    # save to meta file
    meta_filename = os.path.join(args.directory, args.fname+"_meta.h5")
    if args.param=='':
       scan_param = 'scan'
    else:
       scan_param = args.param
    create_metafile(meta_filename, start_tme, BIG_status_lookup, scan_param, len(args.scan), everystep=True)
    if int(args.nimages) > 100:
        os.system('scp {0:s} prcvlusr@cfeld-percival02:{1:s}tmp.h5'.format(meta_filename,meta_filename[:-3]))

    print("-----------------------------------")
    print("Output directory:", args.directory)
    print("File name: ", args.fname+"_<idx>_<daq-idx>.h5")
    print("# of images:", args.nimages)
    print("Exposure time:", "---" if args.param=='TRIGGERING_Repetition_rate' else args.integration)
    print("Timeout:", "Acq time + {0:.2f}s".format(timeout) if args.param=='TRIGGERING_Repetition_rate' else "{0:.2f}s".format(int(args.integration)*int(args.nimages)/100000000.-1+timeout))
    print("Descramble:", dcr)
    print("Scan parameter:", args.param)
    print("Scan range: #=",len(args.scan),"range=",args.scan)
    print("Tigger mode:", "Triggered ({0:d}frame/trig)".format(npls) if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_source'] else "Untirggered")
    print("-----------------------------------{0:.2f}s".format(time.time()-start_tme))
    
    # start scan
    for (scanidx, scanvalue) in enumerate(args.scan):
        # set output filename
        outFileName= args.fname +"_{0:06d}".format(scanidx)
        parse_response(dc.set_file_name(outFileName))
        parse_response(dc.send_command('hdf/write', '1'))
        # set scanvalue
        if args.param!="":
          parse_response(pc.send_command(
             'cmd_system_setting' if args.param=='TRIGGERING_Repetition_rate' else 'cmd_set_channel',
             SCRIPT_NAME,
             arguments={'setting' if args.param=='TRIGGERING_Repetition_rate' else 'channel': args.param, 'value': scanvalue},
             wait=False));

          pc.wait_for_command_completion(0.01)

          parse_response(wait_for_writing(dc, waiting_status=True, timeout=timeout))
        
        # send to P04socket-server
        if not args.p04sock is None:
            tmp = args.directory.split(os.sep)
            if len(tmp) > 3:
                rel_path = os.sep.join(tmp[3:])
            else:
                rel_path = args.directory
            cmd_p04sock = "{0:s}, {1:d}".format(os.path.join(rel_path, outFileName), npls)
            p04host, p04port = args.p04sock.split(":") 
            send_p04sock(cmd_p04sock, p04host, p04port)

        # acquire
        tme = time.time()
        if not BIG_status_lookup['system_settings']['ACQUISITION_Continuous_acquisition']:
            result = pc.send_system_command(const.SystemCmd['start_acquisition'], SCRIPT_NAME, wait=False)
            pc.wait_for_command_completion(0.01)
        if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_source']:
            result = pc.send_system_command(const.SystemCmd['assert_MARKER_OUT_0'], SCRIPT_NAME, wait=False)
            pc.wait_for_command_completion(0.01)
            print("DAQ is ready, inject trigger. {}....h5: {} {}s".format(outFileName, scanidx, tme-start_tme))
        else:
            print("Acq started. {}....h5: {} {}s".format(outFileName, scanidx, tme-start_tme))

        # wait DAQ
        if args.param == 'TRIGGERING_Repetition_rate':
             args.integration = scanvalue
        wait = max(float(args.integration)*int(args.nimages)/100000000.-1+tme-time.time(), 0)
        time.sleep(wait)
        res_fp = wait_for_writing(dc, waiting_status=False, timeout=timeout)
        
        # deassert marker if DAQ is triggered
        if BIG_status_lookup['system_settings']['TRIGGERING_Trigger_source']:
            pc.send_system_command(const.SystemCmd['deassert_MARKER_OUT_0'], SCRIPT_NAME, wait=True)

        # write to meta

        BIG_status_lookup=get_all_settings(pc);
        BIG_status_lookup['fp0']=res_fp['value'][0]
        BIG_status_lookup['fp1']=res_fp['value'][1]
        res_fr = get_fr_status(args.address)
        BIG_status_lookup['fr0'] = res_fr['value'][0]
        BIG_status_lookup['fr1'] = res_fr['value'][1]

        append_metafile(meta_filename, scanidx, tme, scanvalue, outFileName, BIG_status_lookup)

        # check error & reset
        parse_response(res_fp)
        dc.send_reset_stats()
    print("DONE: {}s".format(time.time()-start_tme))
    os.system('scp {0:s} prcvlusr@cfeld-percival02:{0:s}'.format(meta_filename))
    #if int(args.nimages) > 100:
    #    os.system('ssh prcvlusr@cfeld-percival02 rm {0:s}tmp.h5'.format(meta_filename[:-3]))

    if args.debug=='hironoto':
        print('CMD: scp prcvlusr@cfeld-percival02:{0:s}* hironoto@max-fsg:/home/hironoto/11013723/processed/temp_data/'.format(meta_filename[:-7]))
        os.system('scp prcvlusr@cfeld-percival02:{0:s}* hironoto@max-fsg:/home/hironoto/11013723/processed/temp_data/'.format(meta_filename[:-7]))


if __name__ == '__main__':
    main()

