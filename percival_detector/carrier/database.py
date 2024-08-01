""" This is a thin wrapper for Influxdb access, originally written by
AGreer 2016 for influxDB version 1.
    changed in 2024 to use InfluxDB2.
"""

import influxdb_client; # for accessing influxdb2
import requests;
import logging;


class InfluxDB2(object):

    def __init__(self, db_host, db_port, bkt_name):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._db_host = db_host
        self._db_port = db_port
        self._bkt_name = bkt_name
        self._influx_client = None
        self._connected = False

    def connect(self):
        self._log.info("Opening connection to influxDB at {:s}:{:d}".format(self._db_host, self._db_port))
        self._connected = False
        # it seems you can use username and password without a token.
        token = "";

        # this only uses address, port, username and pw. The bucket and org are used later in log_point().

        self._influx_client = influxdb_client.InfluxDBClient(url="http://%s:%s"%(self._db_host, self._db_port),
              org="percival", token=token, username="percival", password="percival");

        health = self._influx_client.health();
        self._connected = health.status=="pass";
        if(self._connected==False):
            self._log.warn("Unable to connect to database: {}".format(health.message))

    def get_status(self):
        status = {
            "address": self._db_host,
            "port": self._db_port,
            "name": self._bkt_name,
            "connected": self._connected
        }
        return status

    def connected(self):
        return self._connected;

    """
    @param time0 a datetime.datetime instance is preferred.
          influxdb uses timestamps since 1970 utc natively, and has its own converter class
          for reading strings which it assumes are in utc unless a timezone is specified.
          The default precision is ns, we only need ms.
    @param measurement this is a parameter for the influxdb
    @param data a dict of key-value pairs.
    """
    def log_point(self, time0, measurement, data):
      if self.connected():
        self._log.debug("influxdb point: %s utc %s %s", time0, measurement, data);
        try:
            write_api = self._influx_client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS);
            dp = influxdb_client.Point(measurement);

            for item in data:
              dp.field(item, data[item]);

            dp.time(time0, write_precision=influxdb_client.domain.write_precision.WritePrecision.MS);

            write_api.write(bucket=self._bkt_name, record=dp);
        except Exception as err:
            self._log.error("influxdb write failed %s", repr(err));


