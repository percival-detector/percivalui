""" This is a thin wrapper for Influxdb access, originally written by
AGreer 2016 for influxDB version 1. Version 1 seems to have reached
end of life and is not supported any more, and is getting harder to find
and install. We can probably delete ver1 support.
    extended in 2024 for use with InfluxDB2 which is our standard.
"""

import influxdb; # for accessing influxdb1
import influxdb_client; # for accessing influxdb2
import requests;
import logging;


class InfluxDB(object):

    def __init__(self, db_host, db_port, db_name):
        self._log = logging.getLogger(".".join([__name__, self.__class__.__name__]))
        self._db_host = db_host
        self._db_port = db_port
        self._db_name = db_name
        self._influx_client = None
        self._connected = False

    def connect(self):
        self._log.info("Opening connection to influxDB at {:s}:{:d}".format(self._db_host, self._db_port))
        self._connected = False
        try:
            self._influx_client = influxdb.InfluxDBClient(host=self._db_host, port=self._db_port)

            existing_dbs = self._influx_client.get_list_database()
            db_exists = False
            for db in existing_dbs:
                if db['name'] == self._db_name:
                    db_exists = True
                    break

            if db_exists:
                self._log.info("{} database exists already".format(self._db_name))
            else:
                self._log.info("Creating {} database".format(self._db_name))
                self._influx_client.create_database(self._db_name)

            self._influx_client.switch_database(self._db_name)
            self._connected = True

        except requests.ConnectionError:
            self._log.info("Unable to connect to {} database".format(self._db_name))

    def get_status(self):
        status = {
            "address": self._db_host,
            "port": self._db_port,
            "name": self._db_name,
            "connected": self._connected
        }
        return status

    def connected(self):
      return self._connected;

    #  @param time of measurement as ?
    #  @param measurement dont know
    #  @param data a dict of (field, value) pairs
    def log_point(self, time, measurement, data):
        self._log.debug("influxdb point: %s %s %s", time, measurement, data)
        if self._connected:
            point = {
                "measurement": measurement,
                "time": time,
                "fields": {}
            }

            for item in data:
                point["fields"][item] = data[item]

            self._influx_client.write_points([point])



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

    def log_point(self, time, measurement, data):
      if self.connected():
        self._log.debug("influxdb point: %s? %s %s", time, measurement, data)
        try:
            write_api = self._influx_client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)
            assert(write_api);
            dp = influxdb_client.Point(measurement); 
            # dp.tag("location", "Prague");

            for item in data:
                dp.field(item, data[item]);

            write_api.write(bucket=self._bkt_name, record=dp)
        except Exception as err:
            self._log.error("influxdb write failed %s", repr(err));


