from helper import OPCUAHelper
from helper import InfluxDBHelper
from helper import MongoHelper
from threading import Thread, Event
import time

#  ---------- InfluxDB Connection Resource --------------
_host = 'keties.iptime.org'
_port = 55592
_protocol = 'line'

#  ---------- OPC-UA Connection Resource --------------
opc_url = "opc.tcp://localhost:26543"


#  ---------- MongoDB Connection Resource --------------
mongodb_url = "mongodb://localhost:27017/"


class KDIP(object):
    def __init__(self):
        self.UaClient = OPCUAHelper.UaClient(self)
        self.MongoClient = MongoHelper.MyMongoClient(self)
        self.InfluxClient = InfluxDBHelper.InfluxClient(self)
        self.IsBuilding = False
        self.TestEvent = Event()
        self.BuildingEvent = Event()
        self.CurrentLayer = 0
        self.TotalLayer = 0

if __name__ == '__main__':
    kdip = KDIP()
    kdip.MongoClient.ConnectMongoServer(mongodb_url)
    kdip.InfluxClient.ConnectInfluxServer(_host, _port)
    kdip.InfluxClient.CreateDB("HBNU_PBF_M160")

    kdip.UaClient.ConnectServer(opc_url)
    kdip.UaClient.SetUaNodes()

    # ---------------------------- 3DP Edge code ----------------------------
    # Build Info Node 구독
    kdip.UaClient.CreateSubscribe()

    kdip.UaClient.StartBuildInfoStream()

    while True:
        if not kdip.IsBuilding and kdip.BuildingEvent.is_set():
            kdip.UaClient.StartEnvLogStream()
        elif kdip.IsBuilding and not kdip.BuildingEvent.is_set():
            kdip.UaClient.FinishEnvLogStream()
        time.sleep(1)

    # --------------------------------------------------------------------------------


    # ---------------------------- Test Robot Server code ----------------------------
    # kdip.UaClient.CreateSubscribe()
    # kdip.UaClient.StartTestBuildInfoStream()
    #
    # while True:
    #     if not kdip.IsBuilding and kdip.TestEvent.is_set():
    #         kdip.UaClient.StartRobotServerStream()
    #     elif kdip.IsBuilding and not kdip.TestEvent.is_set():
    #         kdip.UaClient.FinishRobotServerStream()
    #
    #     time.sleep(1)
    # --------------------------------------------------------------------------------



    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...
    t = Thread(target=MongoHelper.DisplayDBList())
    # OPCUAHelper.event.set()
    t.start()
    kdip.UaClient.DisconnectServer()


