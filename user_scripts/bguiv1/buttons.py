#!/usr/bin/env python

import json;
import sys;
from tkinter import *
import socketfns;

if len(sys.argv)==2 and sys.argv[1]=="--shutdown-server":
    print("sending shutdown message to server");
    socketfns.sendMsg("shutdown", None);
    exit(0);

master = Tk();
master.geometry("400x300+200+200");
master.title("Percival Operation");

def btnCallback(buttxt):
    actions = socketfns.getActions();
    # this button callback should also disable the button so it doesn't
    # get pressed twice; we may as well disable all the buttons then.
    for i in range(0,len(actions)):
        but = f.grid_slaves(column=1,row=i)[0];
        but.configure(state=DISABLED);

    if buttxt in actions:
        print("toggling action ", actions.index(buttxt));
        socketfns.togTask(buttxt);


def updateCanvas(status):
    for i in range(0,len(actions)):
        cv = f.grid_slaves(column=2, row=i)[0];
        state = status[actions[i]];
        if state=="done":
            cv.configure(bg="green");
        elif state=="not done":
            cv.configure(bg="red");
        else:
            cv.configure(bg="orange");

def updateButtons(status):
    for i in range(0,len(actions)):
        but = f.grid_slaves(column=1,row=i)[0];
        canChange = True;
        if 0<i:
            canChange &= (status[actions[i-1]]=="done");
        if i+1<len(actions):
            canChange &= (status[actions[i+1]]=="not done");

        taskStatus = status[actions[i]];
            
        if canChange and (taskStatus=="done" or taskStatus=="not done"):
            but.configure(state=NORMAL);
        else:
            but.configure(state=DISABLED);

def updateStatus():
    # updateStatus and button callbacks won't be called simultaneously;
    # master seems to be single-threaded, but it will queue functions to call
    print("update status");
    status = socketfns.getStatus();
    updateCanvas(status);
    updateButtons(status);
    master.after(1000, updateStatus);

# borderwidth is internal border
f = Frame(master, height=320, width=400, borderwidth=10, highlightbackground="red", highlightthickness=0);
f.pack_propagate(0); # don't shrink
f.pack();

actions = socketfns.getActions();
row = 0;

for ac in actions:
    t0 = Label(f, height=1, width=30, text=ac);
    t0.grid(row=row, column=0);
#  t0.insert(END, "task1");

    c0 = Canvas(f,
           width=20,
           height=10,
           bg="grey");
    c0.grid(row=row, column=2);

    b0 = Button(f, text="on/off", state=DISABLED, command=lambda bac=ac: btnCallback(bac));
    b0.grid(row=row, column=1);
    row = row + 1;

master.after(1000, updateStatus);
mainloop();


