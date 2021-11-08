#!/usr/bin/env python

import socket;
import sys;
import json;

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

    ji["task:"] = task;
    ji["cmd:"] = command;

    jis = json.dumps(ji);
    s.send(jis);
    ji = {};
    back = s.recv(512);
    s.close();

    if back:
        ji = json.loads(back);

    return ji;

def getActions():
    dd = sendMsg("gettasks", None);
    if "tasklist:" in dd:
        return dd["tasklist:"];
    else:
        return [];

def doTask(task):
    dd = sendMsg("start", task);

def undoTask(task):
    dd = sendMsg("stop", task);

def togTask(task):
    dd = sendMsg("toggle", task);

def getStatus():
    dd = sendMsg("querystatus", None);
    if "status:" in dd:
        return dd["status:"];
    else:
        return {};

