#!/usr/bin/env python

import threading;
import socket;
import time;
import json;
import os;
import os.path;
import requests;
import subprocess;
import queryUPS;


HOST = ''  # all nics
PORT = 8889;      # Port to listen on (non-privileged ports are > 1023)

g_AtDesy = False;
g_upsOk = True;
# Thread;
# The Protocol:
# the sender transmits a json dictionary which has
# "cmd" ->
# querystatus
# start
# stop
# toggle
#
# The server sends back the list of levels.
#

# task states can be not done, done, doing and undoing.

# firstly lets load our config:
g_levels = [
    {
      "description" : "turn on wiener",
      "onscript"  : "./user_scripts/wiener/mainswitchON.sh",
      "offscript" : "./user_scripts/wiener/mainswitchOFF.sh"
    },

    { 
      "description" : "power to PwB",
      "onscript"  : "./user_scripts/wiener/pwb_UP.sh",
      "offscript" : "./user_scripts/wiener/pwb_DOWN.sh"
    },

    { 
      "description" : "check voltages1",
      "onscript"  : "./user_scripts/wiener/checkcurrents.py -voltages -pwbon",
      "offscript" : "./user_scripts/wiener/checkcurrents.py -voltages -pwbon"
    },

    { 
      "description" : "power to head",
      "onscript"  : "./DESY/W3C3/user_scripts/POWERUP_000_unix.sh",
      "offscript" : "./DESY/W3C3/user_scripts/POWERDOWN_000_unix.sh"
    },

    { 
      "description" : "check voltages2",
      "onscript"  : "./user_scripts/wiener/checkcurrents.py -voltages -headon",
      "offscript" : "./user_scripts/wiener/checkcurrents.py -voltages -headon"
    },

    { 
      "description" : "head operational",
      "onscript"  : "./DESY/W3C3/user_scripts/DESY_FSI01_FromSysPowON_ToSeq_3G_PGAB_10Img_12ms_0802h3_PLL120MHz_ADC25MHz.sh",
      "offscript" : "./DESY/W3C3/user_scripts/DESY_FSI01_FromSeq0802h3_ToSysPowON_unix.sh"
    },

    { 
      "description" : "check voltages3",
      "onscript"  : "./user_scripts/wiener/checkcurrents.py -voltages -headon",
      "offscript" : "./user_scripts/wiener/checkcurrents.py -voltages -headon",
      "actions"   : [
            {
              "description" : "TestMode1",
              "onscript"  : "./DESY/W3C3/user_scripts/digTest1_RESET_DATA_SYNCH_STATUS_unix.sh"
            },
            {
              "description" : "TestMode3",
              "onscript"  : "./DESY/W3C3/user_scripts/digTest3_RESET_DATA_SYNCH_STATUS_unix.sh"
            }
      ]
    }
];

def validateDoc(levels):
    score = 0;
    # iterate thru levels
    lidx = 0;
    descs = [];
    for lv in levels:
        lv["type"] = "level";
        lv["level"] = lidx;
        if(lv.has_key("state")):
            print "uh oh this level has a state when it shouldnt";
        lv["state"] = "not done";
        score += 1;
        if("description" in lv.keys() and "onscript" in lv.keys() and "offscript" in lv.keys()):
            desc = lv.get("description");
            if(5<len(desc) and desc not in descs):
                descs.append(desc);
                score -= 1;
            actions = lv.get("actions");
            aidx = 0;
            for ac in actions or []:
                    score += 1;
                    ac["type"] = "action";
                    ac["level"] = lidx;
                    ac["aidx"] = aidx;
                    if("description" in ac.keys() and "onscript" in ac.keys()):
                        desc = ac.get("description");
                        if(5<len(desc) and desc not in descs):
                            descs.append(desc);
                            score -= 1;
                    aidx += 1;
                    
        lidx += 1;

    if(lidx < 2):
        score = 1;   

    return score;

def setEnableFlags(levels):
    somethingRunning = False;
    # warning alltasks needs to be a different list.
    alltasks = list(levels);
    for lv in levels:
        if(lv.has_key("actions")):
            alltasks.extend(lv.get("actions"));

    for tk in alltasks:
        # set all to disabled
        tk["enable"] = False;
        # python wont search a None string.
        if(tk.get("state") and "doing" in tk.get("state")):
            somethingRunning = True;

    if(somethingRunning == False):
        if(levels[0].get("state")=="not done"):
            levels[0]["enable"] = True;
        if(levels[-1].get("state")=="done"):
            levels[-1]["enable"] = True;
        # must have >=2 levels
        for lidx in range(0,len(levels)-1):
            if(levels[lidx].get("state") == "done" and levels[lidx+1].get("state") == "not done"):
                levels[lidx]["enable"] = True;
                levels[lidx+1]["enable"] = True;
        for lv in levels:
            if(lv.get("enable") == True and lv.get("state") == "done"):
                for ac in lv.get("actions") or []:
                    ac["enable"] = True;

# this returns a ref to the global levels object, with enableflags updated.
def getLevels():
    global g_levels;
    setEnableFlags(g_levels);
    return g_levels;

def getLevelsShort():
    levels = getLevels();
    levels2 = [];
    for lv in levels:
        lv2 = dict(lv);
        lv2.pop("onscript", None);
        lv2.pop("offscript", None);
        levels2.append(lv2);
    return levels2;
        

# looks thru actions and levels for the description.
def getTask(desc):
    levelsA = getLevels();
    for lv in levelsA:
        if(lv.get("description") == desc):
            return lv;
        for ac in lv.get("actions") or []:
            if(ac.get("description") == desc):
                return ac;
    return None;

# this is a function to test the UPS and returns true if it has mains power.
def upsOk():
    return g_AtDesy or queryUPS.checkUPS(); 

g_Go = True;

class myServer:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # this REUSEADDR means the socket is freed earlier
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((HOST, PORT));
        self._sock.listen(1);
        self._sock.settimeout(0.2);
        # nb the socket prevents two servers running on the same system
        self._mythread = threading.Thread();

    def __del__(self):
        print "closing server";
        if self._mythread and self._mythread.isAlive():
            self._mythread.join();
        self._sock.close();

    def doTask(self, task):
        print "DOING TASK ", task.get("description");
        script = task.get("onscript");
        if 0<=len(script):
            print "running ", script;
            rc = os.system(script);
            if rc:
                print "task failed";
                task["state"] = "not done";
            else:
                print "done task ok";
                task["state"] = "done";

    def undoTask(self, task):
        print "UNDOING TASK ", task.get("description");
        script = task.get("offscript");
        if 0<=len(script):
            print "running ", script;
            rc = os.system(script);
            if rc:
                print "script failed";
                task["state"] = "done";
            else:
                print "undone task ok";
                task["state"] = "not done";

    # this version of doMsg will move down the levels undoing the tasks,
    # and it will tell any connections that it is autoshutdown
    def doMsgShutdown(self):
        global g_Go;

        lvs = getLevels();

        if len(lvs) == 0 or lvs[0].get("state")=="not done":
            g_Go = False;
        for task in lvs:
            if(task.get("enable") and task.get("state")=="done"):
                   if self._mythread.is_alive():
                      print "assert failure thread is alive when it shouldnt";
                      exit(1);
                   print "autoshutdown undoing ", task.get("description");
                   if "check" in task["description"]:
                      # we skip the checks.
                      task["state"] = "not done";
                   else:
                       ## I do not like having this state change here.
                       # can we put it in the function too?
                       task["state"] = "undoing";
                       ## todo we should check _mythread is vacant; it should be.
                       self._mythread = threading.Thread(target=self.undoTask, args=(task,));
                       self._mythread.daemon = True; # thread dies when prog exits
                       self._mythread.start();

        # when this goes into autoShutdown all messages are returned to sender,
        # and commands are automatically executed until it reaches off.
        try:
            conn, addr = self._sock.accept();
        except:
            return;

      #  print('Connected by', addr);
        data = conn.recv(1024);

       # di = json.loads(data);

        ji_sh = [{"shutdownPerc" : True}];
        ji = json.dumps(ji_sh);
        conn.send(ji);
        conn.close();


    def doMsg(self):
        global g_Go;
        # what is crucial is that only one client can connect at any time, and that client
        # can not alter the state in an unsafe manner. Safe movements are moving from one
        # state to the next/previous only.
        try:
            conn, addr = self._sock.accept();
        except:
            return;

        try:
          #  print('Connected by', addr);
            data = conn.recv(1024);
           # print "got data from " , conn;
          #  print "incoming message:", data;

            di = json.loads(data);

            if di.has_key("cmd"):
                cmd = di["cmd"];

                if cmd=="toggle" or cmd=="start" or cmd=="stop":
                    if di.has_key("task") and getTask(di["task"]):
                        task = getTask(di["task"]);

                        if(cmd=="toggle" and task.get("state")=="done"):
                            cmd = "stop";
                        if(cmd=="toggle" and task.get("state")=="not done"):
                            cmd = "start";

                    #    print "TASK ", cmd, task;

                        enabled = task.get("enable");

                        if cmd=="start" and enabled:
                            task["state"] = "doing";
                            self._mythread = threading.Thread(target=self.doTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();
                        if cmd=="stop" and enabled:
                            task["state"] = "undoing";
                            self._mythread = threading.Thread(target=self.undoTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();

                elif cmd=="exit":
                    g_Go = False;
                        

            ji = json.dumps(getLevelsShort());
            conn.send(ji);
        except Exception as e:
            print "exception", e;
            pass;

        conn.close();

print "hello.\nchecking config is ok";

rc = validateDoc(g_levels);

if(rc):
    print("invalid config: you are missing fields or have duplicated a description");
    exit(rc);

print "checking odin_server is started";
# need to check that odin_server is available. This is usually on localhost:8888
response = requests.get("http://localhost:8888");
if response.status_code != 200:
    exit(1);

print "check cur dir is percivalui";
if False and os.path.basename(os.getcwd())!="percivalui":
    print "fail";
    exit(2);

wnr = subprocess.check_output("user_scripts/wiener/querymainswitch.sh");
if g_AtDesy:
   print "check wiener is ON";
   if "on" not in wnr:
        print "error: wiener is off; you need to load the carrier board firmware";
        exit(4);
else:
    print "check wiener is OFF";
    if "off" not in wnr:
        print "error: wiener is on";
        exit(3);

    print "check UPS is reachable and has mains power";
    if upsOk()==False:
        print "fail";
        exit(4);

print "check venv contains percivalui";
rc = os.system("pip show percivalui");
if rc!=0:
    print "error can't find percivalui in python venv";
    exit(4);

print "checks passed";

serv = myServer();
while g_Go:
    if g_upsOk and upsOk() == False:
        g_upsOk = False;
        print "UPS HAS NO POWER: automatic shutdown has begun; please wait.";

    if g_upsOk:
        serv.doMsg();
    else:
        serv.doMsgShutdown();
        

print "Exiting server.py";

