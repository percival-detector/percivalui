#!/usr/bin/env python

import json;
import socket;
import sys;
from Tkinter import *;
import socketfns;

if len(sys.argv)==2 and sys.argv[1]=="--shutdown-server":
    print "sending shutdown message to server";
    socketfns.sendMsg("shutdown", None);
    exit(0);

master = Tk();
master.geometry("600x300+200+200");
master.title("Percival Operation");

desc2but = {};
count = 0;

def btnCallback(tk):
    global desc2but;
    # be careful with tk here: it may not be concurrent.
    # this button callback should also disable the button so it doesn't
    # get pressed twice; we may as well disable all the buttons then.
    for but in desc2but.values():
        but.configure(state=DISABLED);

    if(tk.get("type")=="level"):
        socketfns.togTask(tk.get("description"));
    elif(tk.get("type")=="action"):
        socketfns.doTask(tk.get("description"));
        but = desc2but.get(tk.get("description"));
        but.configure(bg="orange");

def updateCanvas(levels):
    for i in range(0,len(levels)):
        cv = f.grid_slaves(column=2, row=i)[0];
        state = levels[i].get("state");
        if state=="done":
            cv.configure(bg="green");
        elif state=="not done":
            cv.configure(bg="red");
        elif state and "doing" in state:
            cv.configure(bg="orange");
        else:
            cv.configure(bg="black");

def updateButtons(levels):
    for lv in levels:
        but = desc2but[lv.get("description")];

        if lv.get("enable"):
            but.configure(state=NORMAL);
        else:
            but.configure(state=DISABLED);

        for ac in lv.get("actions") or []:
            but = desc2but[ac.get("description")];
            if(ac.get("enable")):
                but.configure(state=NORMAL, bg="#d9d9d9");
            else:
                but.configure(state=DISABLED);
        

def updateStatus():
    global count;
    # updateStatus and button callbacks won't be called simultaneously;
    # master seems to be single-threaded, but it will queue functions to call
    print "update status", count;
    count += 1;
    levels = socketfns.getStatus();
    updateCanvas(levels);
    updateButtons(levels);
    master.after(1000, updateStatus);

# borderwidth is internal border
f = Frame(master, height=320, width=400, borderwidth=10, highlightbackground="red", highlightthickness=0);
f.pack_propagate(0); # don't shrink
f.pack();

levels = socketfns.getStatus();

for lv in levels:
    row = lv.get("level");
    t0 = Label(f, height=1, width=30, text=lv.get("description"));
    t0.grid(row=row, column=0);
#  t0.insert(END, "task1");

    c0 = Canvas(f,
           width=20,
           height=10,
           bg="grey");
    c0.grid(row=row, column=2);

    b0 = Button(f, text="on/off", state=DISABLED, command=lambda bac=lv: btnCallback(bac));
    b0.grid(row=row, column=1);
    desc2but[lv.get("description")]=b0;

    for ac in lv.get("actions") or []:
        b1 = Button(f, text=ac.get("description"), state=DISABLED, command=lambda bac=ac: btnCallback(bac));
        desc2but[ac.get("description")]=b1;
        aidx = ac.get("aidx");
        b1.grid(row=row, column=3+aidx, padx=5, sticky=E);

master.after(1000, updateStatus);
mainloop();


