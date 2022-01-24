#!/usr/bin/env python

import threading;
import socket;
import time;
import json;
import os;
import os.path;
import requests;
import subprocess;

AtDesy = False;
HOST = ''  # all nics
PORT = 8889;      # Port to listen on (non-privileged ports are > 1023)

# Thread;
# The Protocol:
# the sender transmits a json dictionary which has
# "cmd:" ->
# gettasks
# querystatus
# start
# stop
#
# The server sends back the same json dictionary with some things appended:
# "tasks:" - an array of tasks available
# "taskstatus:" - a dictionary of tasks to status
# you can add your own task: add a unique name in the list of tasks, and specify the
# getOnScript, getOffScript. The script should return an exit-code: 0 means success.
tasks = ["turn on wiener", "power to PwB", "check voltages1", "power to head", "check voltages2", "head operational", "check voltages3", "digtest1", "check voltages4"];
# task states can be not done, done, doing and undoing.
if AtDesy:
    tasks[0] = "check voltages0";

def getOnScript(task):
    if task == "turn on wiener":
        return "./user_scripts/wiener/mainswitchON.sh";
    if task == "power to PwB":
        return "./user_scripts/wiener/pwb_UP.sh";
    if task == "power to head":
        return "./DESY/W3C3/user_scripts/POWERUP_000_unix.sh";
    if task == "head operational":
        return "./DESY/W3C3/user_scripts/DLS_FSI07_FromSysPowON_ToSeq_3T_PGAB_10Img_12ms_0802g_PLL120MHz_ADC25MHz.sh";
    if task == "digtest1":
        return "./DESY/W3C3/user_scripts/digTest1_RESET_DATA_SYNCH_STATUS_unix.sh";
    if task == "check voltages0":
        return "./user_scripts/wiener/checkcurrents.py -voltageszero";
    if task == "check voltages1":
        return "./user_scripts/wiener/checkcurrents.py -voltages -pwbon";
    if task == "check voltages2" or task == "check voltages3" or task == "check voltages4":
        return "./user_scripts/wiener/checkcurrents.py -voltages -headon";
    return "errorunknowntask";

def getOffScript(task):
    if task == "turn on wiener":
        return "./user_scripts/wiener/mainswitchOFF.sh";
    if task == "power to PwB":
        return "./user_scripts/wiener/pwb_DOWN.sh";
    if task == "power to head":
        return "./DESY/W3C3/user_scripts/POWERDOWN_000_unix.sh";
    if task == "head operational":
        return "./DESY/W3C3/user_scripts/DLS_FSI07_FromSeq0802g_ToSysPowON_unix.sh";
    if task == "digtest1":
        return "pwd";
    if task == "check voltages0":
        return "./user_scripts/wiener/checkcurrents.py -voltageszero";
    if task == "check voltages1":
        return "./user_scripts/wiener/checkcurrents.py -voltages -pwbon";
    if task == "check voltages2" or task == "check voltages3" or task == "check voltages4":
        return "./user_scripts/wiener/checkcurrents.py -voltages -headon";
    return "errorUnknownTask";

Go = True;

class myServer:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self._sock.bind((HOST, PORT));
        self._sock.listen(1);
        self._sock.settimeout(0.2);
        # nb the socket prevents two servers running on the same system
        self._taskstates = {};
        self._mythread = threading.Thread();
        for task in tasks:
            self._taskstates[task] = "not done";

    def __del__(self):
        print("closing server");
        if self._mythread and self._mythread.isAlive():
            self._mythread.join();
        self._sock.close();

    def doTask(self, task):
        print("DOING TASK ", task);
        script = getOnScript(task);
        if 0<=len(script):
            print("running ", script);
            rc = os.system(script);
            if rc:
                print("task failed", task);
                self._taskstates[task] = "not done";
            else:
                print("done task: ", task);
                self._taskstates[task] = "done";

    def undoTask(self, task):
        print("UNDOING TASK ", task);
        script = getOffScript(task);
        if 0<=len(script):
            print("running ", script);
            rc = os.system(script);
            if rc:
                print("script failed", task);
                self._taskstates[task] = "done";
            else:
                print("undone task: ", task);
                self._taskstates[task] = "not done";

    def doOnce(self):
        global Go;
        # what is crucial is that only one client can connect at any time, and that client
        # can not alter the state in an unsafe manner. Safe movements are moving from one
        # state to the next/previous only.
        try:
            conn, addr = self._sock.accept();
        except:
            return;

        try:
          #  print('Connected by', addr);
            data = conn.recv(1024).decode();
          #  print "got data from " , conn;
          #  print data;

            di = json.loads(data);
            if "cmd:" in di:
                cmd = di["cmd:"];
                if cmd=="gettasks":
                 #   print "GETTING TASKS";
                    di["tasklist:"] = tasks;
                elif cmd=="querystatus":
                    di["status:"] = self._taskstates;
                elif cmd=="start" or cmd=="stop" or cmd=="toggle":    
                    if "task:" in di and di["task:"] in tasks:
                        task = di["task:"];
                        tidx = tasks.index(task);
                        tstatus = self._taskstates[task];

                        if(cmd=="toggle" and self._taskstates[task]=="done"):
                            cmd = "stop";
                        if(cmd=="toggle" and self._taskstates[task]=="not done"):
                            cmd = "start";

                        print("TASK ", tidx, task, cmd);
                        # to do a task, two checks are made:
                        # firstly that the task itself is in state done/notdone
                        # secondly that the prev task is done, and the next task is not done.
                        # The tasks form a chain and you can only alter the one at the end of the done chain.
                        canDoTask = (tstatus == "not done");
                        canUndoTask = (tstatus == "done");

                        if 0 < tidx:
                            prevtask = tasks[tidx-1];
                            canUndoTask &= (self._taskstates[prevtask] == "done");
                            canDoTask &= (self._taskstates[prevtask] == "done");
                        if tidx+1 < len(tasks):
                            nexttask = tasks[tidx+1];
                            canUndoTask &= (self._taskstates[nexttask] == "not done");
                            canDoTask &= (self._taskstates[nexttask] == "not done");

                        if cmd=="start" and canDoTask:
                            self._taskstates[task] = "doing";
                            self._mythread = threading.Thread(target=self.doTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();
                        if cmd=="stop" and canUndoTask:
                            self._taskstates[task] = "undoing";
                            self._mythread = threading.Thread(target=self.undoTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();
                elif cmd=="shutdown":
                    Go = False;
                        
            ji = json.dumps(di).encode();
            conn.send(ji);
        except:
            pass;

        conn.close();

print("hello.\nchecking odin_server is started");
# need to check that odin_server is available. This is usually on localhost:8888
response = requests.get("http://localhost:8888");
if response.status_code != 200:
    exit(1);

print("check cur dir is percivalui");
if os.path.basename(os.getcwd())!="percivalui":
    print("fail");
    exit(2);

wnr = subprocess.check_output("user_scripts/wiener/querymainswitch.sh").decode();
if AtDesy:
   print("check wiener is ON");
   if "on" not in wnr:
        print("error: wiener is off; you need to load the carrier board firmware");
        exit(4);
else:
    print("check wiener is OFF");
    if "off" not in wnr:
        print("error: wiener is on");
        exit(3);

print("check venv contains percivalui");
rc = os.system("pip show percivalui");
if rc!=0:
    print("error can't find percivalui in python venv");
    exit(4);

print("checks passed");
serv = myServer();
while Go:
    serv.doOnce();

print("SHUTTING DOWN");


