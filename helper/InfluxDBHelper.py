from influxdb import InfluxDBClient



class InfluxClient(object):
    def __init__(self, _kdip):
        self.KDIP = _kdip

    def ConnectInfluxServer(self, _host, _port):
        self.client = InfluxDBClient(host=_host, port=_port, timeout=500)
        self.health = False
        try:
            self.client.ping()
            self.health = True
            return True
        except:
            return False

    def CheckConnection(self):
        self.health = False
        try:
            self.client.ping()
            self.health = True
            return True
        except:
            return False

    def CreateDB(self, dbname):
        self.DBName = dbname
        # check database list
        try:
            if self.client is None:
                return False
            list_db = self.client.get_list_database()
            ret = next((item for item in list_db if item['name'] == dbname), None)
            if ret is None:
                self.client.create_database(dbname)
            return True
        except:
            try:
                self.client.create_database(dbname)
            except Exception as e:
                print("exception message : " + str(e))



    def CreateMeasurement(self, _measurement):
        self.Measurement = _measurement

    def InsertPoint(self, paramName, value, layerIdx, tag, timestamp):

        point = [
            {
                'measurement': self.Measurement,
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
        self.client.write_points(point, database=self.DBName)