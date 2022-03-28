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


class Defcon:

  def __init__(self):
    # list of stages that have been done and finished
    self.done_ = [];
    # list of stages that are being done / undone; can include elements of done_.
    self.doing_ = [];
    self.undoing_ = [];
    self.allstages_ = {};

  def loadConfig(self, filepath):

#    if(os.path.dirname(filepath)==""):
#      dir_path = os.path.dirname(os.path.realpath(__file__));
#      filepath = os.path.join(dir_path, filepath);

    f = open(filepath);
    # if there is invalid json, this will raise
    self.config_ = json.load(f);

    f.close();

  def loadConfigAndValidate(self, filepath):
    self.loadConfig(filepath);
    return self.validateConfig();

  def validateConfig(self):
    rc = 0;
    self.allstages_ = {};

    for sn,acts in self.config_.items():
      print("reading snake",sn);
      for act in acts:
        if "description" in act:
          desc = act["description"];
          if desc in self.allstages_:
            if(act != self.allstages_[desc]):
              print ("Fatal Error: you have an action called -", desc, "- which is different in different places in your json file");
              exit (1);
              rc = 1;
          else:
            self.allstages_[desc] = act;

    for stage in self.allstages_.values():
      bok = False;
      if "onscript" in stage:
        if "offscript" in stage or "action" in stage:
          bok = True;

      if(bok == False):
        print("error:", stage["description"], "is incomplete: needs on/offscript/action");
        exit(1);
        rc = 1;

      # get returns None instead of throwing
      if not os.path.isfile(stage.get("onscript").split(" ")[0]):
        print("error onscript:", stage["onscript"], " does not exist");
        rc = 1;

      if "offscript" in stage:
        if not os.path.isfile(stage.get("offscript").split(" ")[0]):
          print("error offscript:", stage["offscript"], " does not exist");
          rc = 1;

    return rc;

  def getDoneList(self, considerDoingAsDone=False):
    if considerDoingAsDone:
      return self.done_ + self.doing_;
    else:
      return self.done_;

  def getNextStages(self, considerDoingAsDone=False):
    ret = [];
    optimisticDone = self.getDoneList(considerDoingAsDone);

    for sn,acts in self.config_.items():
      snOk = True;
      idx = 0;
      while idx < len(optimisticDone) and idx<len(acts) and snOk:
        if optimisticDone[idx] != acts[idx]["description"]:
          snOk = False;
        idx += 1;

      if(snOk and idx < len(acts)):
        nextAct = acts[idx]["description"];
        if not nextAct in ret:
          ret.append(nextAct);

    return ret;

  def getLastAction(self):
    if self.done_ == []:
      return None;
    else:
      return self.done_[-1];

  def doTask(self, name):
    # need to check nothing is running
    if(name in self.getNextStages()):
      act = self.allstages_[name];
      print("DOING TASK ", name);
      # this returns None in the case of key unknown
      script = act.get("onscript");
      if script and 0<=len(script):
          self.doing_.append(name);
          print("running ", script);
          rc = os.system(script);
          if rc:
              print("task failed");
          elif "action" in act and act["action"]:
              print("done action ok");
             # self.done_.append(name);
          else:
              print("done task ok");
              self.done_.append(name);
      else:
        print ("error: no onscript specified");
    else:
      print ("error trying to do an action that you cant");
    self.doing_ = [];

  def undoTask(self, name):
    if(len(self.done_) and name==self.done_[-1]):
      act = self.allstages_[name];
      print("UNDOING TASK ", name);
      script = act.get("offscript");
      if script and 0<=len(script):
          self.undoing_.append(name);
          print("running ", script);
          rc = os.system(script);
          if rc:
              print("script failed");
          else:
              print("undone task ok");
              self.done_.pop();
      else:
        print ("error: no onscript specified");
    else:
      print ("error trying to undo an action that you cant");
    self.undoing_ = [];

  def getStatus(self):
    ret = {};
    ret["done"] = self.getDoneList(True);
    # only add doing here.
    ret["working"] = self.doing_ + self.undoing_;
    ret["todo"] = self.getNextStages(True);
    return ret;

if __name__ == "__main__":
  h = Defcon();

  h.loadConfig();
  h.validateConfig();
  h.doTask("stage0");

  print (h.getNextStages());
    



