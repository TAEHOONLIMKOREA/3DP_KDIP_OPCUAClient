from helper import OPCUAHelper
from helper import InfluxDBHelper
from threading import Thread, Event
from helper import MongoHelper
import time

#  ---------- InfluxDB Connection Resource --------------
_host = 'keties.iptime.org'
_port = 55592
_protocol = 'line'
_dbname = 'TestDB'
_measurement = '20230302_1661'

#  ---------- OPC-UA Connection Resource --------------
opc_url = "opc.tcp://localhost:26543"


#  ---------- MongoDB Connection Resource --------------
mongodb_url = "mongodb://localhost:27017/"


class KDIP(object):
    def __init__(self):
        self.UaClient = OPCUAHelper.UaClient(self)
        self.MongoClient = MongoHelper.MyMongoClient(self)
        self.InfluxClient = InfluxDBHelper.InfluxClient(self)
        self.CurrentLayer = 0
        self.TotalLayer = 0

if __name__ == '__main__':
    kdip = KDIP()
    kdip.UaClient.ConnectServer(opc_url)
    kdip.UaClient.SetUaNodes()

    # ---------------------------- 3DP Edge code ----------------------------
    # Build Info Node 구독
    # kdip.UaClient.CreateBuildInfoSubscribe()
    # kdip.UaClient.CreateEnvLogSubscribe()
    #
    # kdip.UaClient.StartBuildInfoStream()
    #
    # while True:
    #     if not kdip.UaClient.IsBuilding and OPCUAHelper.BuildingEvent.is_set():
    #         kdip.UaClient.StartEnvLogStream()
    #     elif kdip.UaClient.IsBuilding and not OPCUAHelper.BuildingEvent.is_set():
    #         kdip.UaClient.FinishEnvLogStream()
    #     time.sleep(1)

    # --------------------------------------------------------------------------------


    # ---------------------------- Test Robot Server code ----------------------------
    kdip.UaClient.CreateTestBuildInfoSubscribe()
    kdip.UaClient.CreateRobotServerSubscribe()
    kdip.UaClient.StartTestBuildInfoStream()

    while True:
        if not kdip.UaClient.IsBuilding and kdip.UaClient.TestEvent.is_set():
            kdip.UaClient.StartRobotServerStream()
        elif kdip.UaClient.IsBuilding and not kdip.UaClient.TestEvent.is_set():
            kdip.UaClient.FinishRobotServerStream()

        time.sleep(1)
    # --------------------------------------------------------------------------------



    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...
    t = Thread(target=MongoHelper.DisplayDBList())
    # OPCUAHelper.event.set()
    t.start()
    kdip.UaClient.DisconnectServer()


