from helper import OPCUAHelper
from helper import InfluxDBHelper
from helper import MongoHelper
from threading import Thread, Event
import socket
import time

#  ---------- InfluxDB Connection Resource --------------
_host = 'keties.iptime.org'
_port = 55594
_protocol = 'line'
influx_url = "https://ketis.iptime.org:55592"
#  ---------- OPC-UA Connection Resource --------------
opc_url = "opc.tcp://localhost:26543"


#  ---------- MongoDB Connection Resource --------------
mongodb_url = "mongodb://localhost:27013/"
mongo_host = "https://localhost"
mongo_port = 27017


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

def throw_if_mongodb_is_unavailable(host, port):
    sock = None
    try:
        sock = socket.create_connection((host, port), timeout=1) # one second
    except socket.error as err:
        raise EnvironmentError(
            "Can't connect to MongoDB at {host}:{port} because: {err}"
            .format(**locals()))
    finally:
        if sock is not None:
            sock.close()


if __name__ == '__main__':
    kdip = KDIP()
    kdip.MongoClient.ConnectMongoServer(mongodb_url)
    # throw_if_mongodb_is_unavailable(_host, _port)
    kdip.InfluxClient.ConnectInfluxServer(_host, _port)
    print("Result : ", kdip.InfluxClient.health)
    kdip.InfluxClient.CreateDB("HBNU_PBF_M160")


    if kdip.UaClient.client is None:
        kdip.UaClient.ConnectServer(opc_url)

    rtn = kdip.UaClient.CheckConnection()
    print(rtn)

    if kdip.UaClient.client is not None:
        kdip.UaClient.SetUaNodes()

    rtn = kdip.UaClient.CheckConnection()

    kdip.UaClient.DisconnectServer()
    if kdip.UaClient.client is None:
        x = 10
    else:
        x = 0

    print(x)


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


