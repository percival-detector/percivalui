from influxdb import InfluxDBClient
import requests
import logging


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

        try:
            self._influx_client = InfluxDBClient(host=self._db_host, port=self._db_port)

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

    def log_point(self, time, measurement, data):
        if self._connected:
            point = {
                "measurement": measurement,
                "time": time,
                "fields": {}
            }

            for item in data:
                point["fields"][item] = data[item]

            self._influx_client.write_points([point])
