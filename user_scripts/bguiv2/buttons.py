#!/usr/bin/env python3

import json;
import socket;
import sys;
from tkinter import *;
import socketfns;

# we could have exit-server instead
if len(sys.argv)==2 and sys.argv[1]=="--shutdown-server":
    print("sending shutdown message to server");
    socketfns.sendMsg("exit", None);
    exit(0);

master = Tk();
master.geometry("800x400+100+100");
master.title("Percival Operation");

desc2but = {};
count = 0;

def btnCallback(td):
    global desc2but, laststatus;

    if td in desc2but.keys():
      # be careful with td here: it may not be concurrent.
      # this button callback should also disable the button so it doesn't
      # get pressed twice; we may as well disable all the buttons then.
      for but in list(desc2but.values()):
          but.configure(state=DISABLED);

   #   desc2but[td].configure(bg="orange");

      socketfns.togTask(td);
      laststatus = {};


def createCanvas(status):
    desc2but.clear();
    for wd in f.grid_slaves():
      wd.grid_forget();

    row = 0;
    # we go down the rows adding things; firstly lets add the stages done.
    if "done" in status:
      done = status["done"];
      while row < len(done):
        dn = done[row];
        if row+1 < len(done):
          dn += " - \u2705"; # this is a tick
        t0 = Label(f, height=2, width=30, text=dn);
        t0.grid(row=row, column=0, sticky=W);
        row += 1;

    # create an undo button for the last one in most cases
    if row:
      td = done[-1];
      b0 = Button(f, text="Undo", state=DISABLED, command=lambda bac=td: btnCallback(bac));
      b0.grid(row=row-1, column=1);
      desc2but[td] = b0;


    # add buttons for stages we can do at this stage
    if "todo" in status:
      buts = status["todo"];
      t0 = Label(f, height=1, width=30, text="Do next:");
      t0.grid(row=row, column=0);

      idx = 0;
      for td in buts:
        b0 = Button(f, text=td, state=DISABLED, command=lambda bac=td: btnCallback(bac));
        desc2but[td] = b0;
        maxperrow = 3;
        b0.grid(row=row+idx//maxperrow, column=idx%maxperrow+1);
        idx += 1;

    if "working" in status:
      working = status["working"];
      if working == []:
        for but in desc2but.values():
          but.configure(state=NORMAL);
      else:
        running = working[0];
        for but in list(desc2but.values()):
            but.configure(state=DISABLED);
        if running in desc2but.keys():
            desc2but[running].configure(bg="orange");


# status is a hash of three lists: working, done, todo and maybe shutdownPerc.
laststatus = {};
def updateStatus():
    global count, laststatus;
    # updateStatus and button callbacks won't be called simultaneously;
    # master seems to be single-threaded, but it will queue functions to call
   # print(("update status", count));
    count += 1;
    status = socketfns.getStatus();
    if status and status.get("shutdownPerc"):
        print("AUTOSHUTDOWN RUNNING");
        exit(0);

    if status != laststatus:
      print("status changed to:", status);
      createCanvas(status);
      laststatus = status;
    master.after(1000, updateStatus);

# borderwidth is internal border
f = Frame(master, height=600, width=500, borderwidth=10, highlightbackground="red", highlightthickness=0);
f.pack_propagate(0); # don't shrink
f.pack();

status = socketfns.getStatus();

master.after(1000, updateStatus);
mainloop();


