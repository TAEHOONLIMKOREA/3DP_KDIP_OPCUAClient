
from influxdb import InfluxDBClient
from datetime import datetime

_host = 'keties.iptime.org'
_port = 55592
_protocol = 'line'
_dbname = 'TestDB'
_measurement = '20230223_1749'

client = InfluxDBClient(host=_host, port=_port)

def CreateDB(dbname=_dbname, measurement=_measurement):
    # check database list
    list_db = client.get_list_database()
    ret = next((item for item in list_db if item['name'] == dbname), None)
    if ret is None:
        client.create_database(dbname)

        # check measurement list
    list_measurements = client.get_list_measurements()
    rtn = next((item for item in list_measurements if item['name'] == measurement), None)
    if rtn is measurement:
        client.drop_measurement(measurement)

    mesurementName=measurement
    global mesurementName


def InsertPoint(paramName, value, layerIdx, tag):

    timestamp = datetime.now()
    point = [
        {
            'measurement': mesurementName,
            'tags': {
                'LayerIdx': layerIdx,
                'tag': tag
            },
            'fields': {
                paramName: value,
            },
            'time': timestamp
        }
    ]

    print("Write point: {0}".format(point))
    client.write_points(point, database=_dbname)