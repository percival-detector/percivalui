#!/usr/bin/env python

import socket;
import sys;
import json;

# I am inclined to move all this into buttons.py and/or use zmq.

HOST = '172.23.17.54'  # ws450 at Diamond. This is the pc you run server.py on.
PORT = 8889;      # Port to listen on (non-privileged ports are > 1023)

"""
task - task id is one or two or three or stop to shutdown server
command - start, status
returns any response from server
"""
def sendMsg(command, task):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    # this timeout is bigger than the time it shd take to serve a request.
    s.settimeout(1.0);
    s.connect((HOST, PORT));

    ji = {};

    ji["cmd"] = command;
    ji["task"] = task;


    jis = json.dumps(ji);
    s.send(jis);
    ji = {};
    back = s.recv(2048);
    s.close();

    if back:
     #   print "returned", back;
        ji = json.loads(back);

    return ji;

def doTask(task):
    dd = sendMsg("start", task);

def undoTask(task):
    dd = sendMsg("stop", task);

def togTask(task):
    dd = sendMsg("toggle", task);

def getStatus():
    levels = sendMsg("getLevels", None);
    return levels;


