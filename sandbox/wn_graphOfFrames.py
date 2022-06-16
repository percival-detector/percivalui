#!/dls_sw/apps/python/anaconda/1.7.0/64/bin/python

# This script reads the logfiles and tcpdump files you give it and draws a graph showing
# how long the DAQ stages take to complete.
# nothing to do with calibration.

import time
import os
import re
import numpy
import re;
import sys;
import argparse;
from datetime import datetime;

from PIL import Image, ImageDraw, ImageFont;


class Block:

    def __init__(self, channel, frame, start, end):
        self.m_start = int(start);
        self.m_end = int(end);
        self.m_frame = int(frame);
        self.m_channel = channel;

    def getChannel(self):
        return self.m_channel;

    def getStart(self):
        return self.m_start;

    def getEnd(self):
        return self.m_end;

    def getFrame(self):
        return self.m_frame;


def getYForChannel(ch):
    ret = 0;
    allch = ["packets", "fr", "percival", "liveview", "calib", "hdf", "axis"];
    ret = 100 + allch.index(ch) * 50;

    return ret;

def getColForFrame(frame):
    num = frame % 4;
    col = "yellow";
    if num<2:
      col = "red";
    return col;

def blocks2Image(blockList, outfile):

    los = [b.getStart() for b in blockList];
    his = [b.getEnd() for b in blockList];

    lo = min(los);
    hi = max(his);
    rangeTS = hi - lo;

    width = max(1000, 10 * len(blockList));
    height = 500;
    lmargin = 120.0;
    rmargin = 50;
    scalef = (width - lmargin - rmargin) / rangeTS;

    im = Image.new('RGB', (width,height), (0,200,200));
    font0 = ImageFont.truetype("arial.ttf", size=20);
    font1 = ImageFont.truetype("arial.ttf", size=15);
    dctx = ImageDraw.Draw(im);
    dctx.text((100, 2), "Time graph of Percival DAQ during capture showing active stages", font=font0);

    # this is duplicating actions
    for bl in blockList:
        ch = bl.getChannel();
        dctx.text((10,getYForChannel(ch)), "{}".format(ch), font=font0);
        dctx.line([(lmargin, getYForChannel(ch)+10), (width - rmargin, getYForChannel(ch)+10)], fill="yellow" );

    for a in range(0, rangeTS, 5000):
        posX = lmargin + scalef * a;
        dctx.line([(posX, getYForChannel("axis")-10), (posX, getYForChannel("axis")+0)], fill="black" ); 

   # dctx.text((100, getYForChannel(8)), "(count of events)", fill="green");
    dctx.text((100, getYForChannel("axis")+30), "TIME---> (5ms intervals), total range {}ms".format((hi-lo)/1000), font=font0);

    for b in blockList:
        y = getYForChannel(b.getChannel());
        x1 = scalef * (b.getStart()-lo);
        x2 = scalef * (b.getEnd()-lo);
        x1 = x1 + lmargin;
        x2 = x2 + lmargin;

        bbox = [(x1, y), (x2,y+20)];
        if x1 <= x2:
          dctx.rectangle(bbox, fill=getColForFrame(b.getFrame()), outline="blue");
        else:
          print("warning time vals gone awol");

  #      dctx.text( (x1+2,y+2), "{}".format(b.getQty()), fill="green", font=font1);


    del dctx;

    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S");
    print("saving", outfile);
    im.save(outfile);

def parseFile(filename):
    ret = [];
    packetArrivalTimes = [];
    with open(filename) as fp:
       spans = [];
       for cnt, line in enumerate(fp):
     ##     print("Line {}: {}".format(cnt, line));

          # this is what we'd see in a FR log
          match = re.search("Frame (\\d+) arrived at (\\d+)us dispatched at (\\d+)us", line);
          if(match):
            frame = int(match.group(1))*2;
            t0 = int(match.group(2));
            t1 = int(match.group(3));
            spans.append(t1 - t0);
            bl = Block("fr", frame, t0, t1);
            ret.append(bl);

          match = re.search("plugin: (\\w+), frame (\\d+) started at (\\d+)us, ended at (\\d+)us", line);
          if(match):
            channel = match.group(1);
            frame = match.group(2);
            t0 = match.group(3);
            t1 = match.group(4);
            bl = Block(channel, frame, t0, t1);
            ret.append(bl);

          # use -tt on tcpdump
          match = re.search("^(\\d+)\\.(\\d+) IP .* length 4982", line);
          if(match):
         #   print("recognized ", match.group(0) );
            tm = int(match.group(1)) * 1000000 + int(match.group(2));
            tm &= 0xffffffff;
            packetArrivalTimes.append(tm);

    if spans:
      print("average fr span:", numpy.average(spans));
    if(packetArrivalTimes):
      packetArrivalTimes.sort();
      edgeTimes = [];
      edgeTimes.append(packetArrivalTimes[0]);
      for i in range(len(packetArrivalTimes)-1):
        if 4000 < (packetArrivalTimes[i+1] - packetArrivalTimes[i]):
          edgeTimes.append(packetArrivalTimes[i]);
          edgeTimes.append(packetArrivalTimes[i+1]);

      edgeTimes.append(packetArrivalTimes[-1]);
    #  print ("packet edgeTimes ", edgeTimes);
      spans = [];
      for i in range(0,len(edgeTimes)-1,2):
        channel = "packets";
        frame = i;
        t0 = edgeTimes[i];
        t1 = edgeTimes[i+1];
        spans.append(t1-t0);
        bl = Block(channel, frame, t0, t1);
        ret.append(bl);

      print("average packet arrival span:", numpy.average(spans));      

    return (ret);


def options():
    desc = "custom script to create a graph of active stages in daq.";
    parser = argparse.ArgumentParser(description=desc)

  #  parser.add_argument("-l", "--label", default="VINSCAN", help="filename label to search for")
    parser.add_argument("--indir", default="/dls/detectors/Percival/software", help="folder for log files input (default software)")
    parser.add_argument("-i", "--infiles", nargs="+", default=["fp1.log","fr1.log"], help="list of log files input")
    parser.add_argument("--framerange", default=None, nargs="+", help="--framerange st end (default None)")

    parser.add_argument("-o", "--outfile", default="output", help="output png file (default output)");
#    parser.add_argument("--graph", metavar="H5FILE", default="", help="show graphs of this file instead");

    args = parser.parse_args()
    return args;



def main():
  args = options();

  indir = "";
  if os.path.isdir(args.indir):
    indir = args.indir;
  else:
    print ("invalid in directory ", args.indir);
    exit(1);

  outfile = args.outfile;
  if not outfile.endswith(".png"):
    outfile += ".png";

  framerange = None;
  if args.framerange and len(args.framerange)==2:
    framerange = map(int,args.framerange);

  infiles = [os.path.join(indir, a) for a in args.infiles];

  blocks = [];
  for f in infiles:
    if os.path.isfile(f):
      blocks += parseFile(f);
    else:
      print("Invalid file:", f);
      exit(1);

  blocks2 = [];
  for b in blocks:
    if framerange==None or (framerange[0] <= b.getFrame() and b.getFrame() <= framerange[1]):
      blocks2.append(b);

  print("I have {} blocks".format(len(blocks2)));
##  print ("Processing these logfiles:", infiles);
  blocks2Image(blocks2, outfile);

if __name__ == '__main__':
    main()

