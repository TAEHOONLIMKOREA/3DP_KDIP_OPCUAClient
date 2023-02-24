from influxdb import InfluxDBClient
from datetime import datetime

_host = 'keties.iptime.org'
_port = 55592
_protocol = 'line'
_dbname = 'TestDB'
_measurement = '20230223_1749'

client = InfluxDBClient(host=_host, port=_port)


def CreateDB(dbname=_dbname):
    # check database list
    list_db = client.get_list_database()
    ret = next((item for item in list_db if item['name'] == dbname), None)
    if ret is None:
        client.create_database(dbname)



def InsertPoint(paramName, value, layerIdx, tag):

    timestamp = datetime.now()
    point = [
        {
            'measurement': _measurement,
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
    client.write_points(point, database=_dbname)f