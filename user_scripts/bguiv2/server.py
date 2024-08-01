#!/usr/bin/env python3

# modules to install: requests, serial, mibs for wiener,
import threading;
import socket;
import time;
import json;
import os;
import os.path;
import requests;
import subprocess;
import defcon;
import argparse;


HOST = ''  # all nics
PORT = 8889;      # Port to listen on (non-privileged ports are > 1023)

g_AtDesy = False;
# Thread;
# The Protocol:
# the sender transmits a json dictionary which has
# "task" -> taskname
# "cmd" ->
# querystatus
# start
# stop
# toggle
#
# The server sends back a dictionary like
# { ? }
# OR (if powercut):
# {"shutdownPerc" : True}
#
#

# task states can be not done, done, doing and undoing.


# this is a function to test the UPS and returns true if it has mains power.
def upsOk():
    return True; 

class myServer:
    s_Go = True;
    s_upsOk = True;
    def __init__(self, configfile):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # this REUSEADDR means the socket is freed earlier
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((HOST, PORT));
        self._sock.listen(1);
        self._sock.settimeout(0.2);
        # nb the socket prevents two servers running on the same system
        self._mythread = threading.Thread();
        self.defcon_ = defcon.Defcon();
        self.defcon_.loadConfig(configfile);
        rc = self.defcon_.validateConfig();
        if rc:
          print("failed to initialize");
          exit(1);

    def __del__(self):
        print("closing server");
        if self._mythread and self._mythread.is_alive():
            self._mythread.join();
        self._sock.close();


    def doMsg(self):
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

            di = json.loads(data.decode());
          #  print ("incoming message:", di);

            if "cmd" in di:
                cmd = di["cmd"];
                if cmd=="toggle" or cmd=="start" or cmd=="stop":
                  if "task" in di:
                      task = di["task"];

                      if(cmd=="toggle"):
                        if(task == self.defcon_.getLastAction()):
                          cmd = "stop";
                        else:
                          cmd = "start";

                  #    print "TASK ", cmd, task;
                      if self._mythread.is_alive() == False:
                        if cmd=="start":
                            self._mythread = threading.Thread(target=self.defcon_.doTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();
                        if cmd=="stop":
                            self._mythread = threading.Thread(target=self.defcon_.undoTask, args=(task,));
                            self._mythread.daemon = True; # thread dies when prog exits
                            self._mythread.start();

                elif cmd=="exit":
                    myServer.s_Go = False;

            retdict = self.defcon_.getStatus();

            ji = json.dumps(retdict);
            conn.send(ji.encode());
        except Exception as e:
            print("exception", e);
            pass;

        conn.close();

    def runLoop(self):
      while myServer.s_Go:
          if myServer.s_upsOk and upsOk() == False:
              myServer.s_upsOk = False;
              print("UPS HAS NO POWER: automatic shutdown has begun; please wait.");

          if myServer.s_upsOk:
              self.doMsg();
          else:
              self.doMsgShutdown();

def initialChecks(): 
  print("hello.\n");

  print("checking odin_server is started");
  # need to check that odin_server is available. This is usually on localhost:8888
  response = requests.get("http://localhost:8888");
  if response.status_code != 200:
      exit(1);

  print("check cur dir is percivalui");
  if False and os.path.basename(os.getcwd())!="percivalui":
      print("fail");
      exit(2);

  wnr = subprocess.check_output("user_scripts/wiener/querymainswitch.sh");
  wnr = wnr.decode();
  if g_AtDesy:
     print("check wiener is ON");
     if "on" not in wnr:
          print("error: wiener is off; you need to load the carrier board firmware");
          exit(4);
  else:
      print("check wiener is OFF");
      if "off" not in wnr:
          print("error: wiener is on");
          exit(3);

      print("check UPS is reachable and has mains power");
      if upsOk()==False:
          print("fail");
          exit(4);

  print("check venv contains percivalui");
  rc = os.system("pip show percivalui");
  if rc!=0:
      print("error can't find percivalui in python venv");
      exit(4);

  print("checks passed");

def options():
    desc = "The serverside part of the buttongui v3 for percival powerup";
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--config", help="the json config file for your detector", required=True)

    # this will print help and exit if it sees -h
    args = parser.parse_args()
    return args

def main():
  args = options();
  if(not os.path.isfile(args.config)):
    print ("can not find config file");
    exit(1);

  initialChecks();
  serv = myServer(args.config);
  serv.runLoop();

  print("Exiting server.py");

if __name__ == '__main__':
    main()

