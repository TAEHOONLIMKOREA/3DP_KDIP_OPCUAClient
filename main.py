from helper import OPCUAHelper
from helper import InfluxDBHelper




if __name__ == '__main__':
    InfluxDBHelper.CreateDB()
    OPCUAHelper.ConnectServer()