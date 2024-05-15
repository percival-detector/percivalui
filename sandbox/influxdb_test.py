#!/usr/bin/env python3

""" Simple test-script to put some data into influxdb
"""


from percival_detector.carrier.database import InfluxDB, InfluxDB2;
from percival_detector.log import log
import random;
import time;

def main():
    log.info("Connecting to influxdb...")
    db = InfluxDB2('ws450', 8086, 'db_test');
    db.connect();

    for a in range(0,100):
      dp = {
          "value1": 24.5 + random.randint(-10,10),
          "value2": 12.0 + random.randint(0,100)
          }

      db.log_point("2017-05-17T13:00:00Z",'meas1', dp)
      time.sleep(1);

if __name__ == '__main__':
    main()
