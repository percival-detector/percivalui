


from percival.carrier.database import InfluxDB
from percival.log import log

def main():
    log.info("Connecting to influxdb...")
    db = InfluxDB('localhost', 8086, 'db_test')

    dp = {
        "value1": 24.5,
        "value2": 12.0
        }

    db.log_point("2017-05-17T13:00:00Z",'item1', dp)

if __name__ == '__main__':
    main()
