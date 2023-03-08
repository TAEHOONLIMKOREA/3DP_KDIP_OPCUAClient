from helper import OPCUAHelper
from helper import InfluxDBHelper
from threading import Thread, Event
from helper import MongoHelper
import time


url = "opc.tcp://localhost:26543"


if __name__ == '__main__':
    # InfluxDBHelper.CreateDB()
    OPCUAHelper.IsBuilding = False
    uaclient = OPCUAHelper.UaClient(url)
    uaclient.ConnectServer()
    uaclient.SetUaNodes()

    # Build Info Node 구독
    uaclient.CreateBuildInfoSubscribe()
    uaclient.CreateEnvLogSubscribe()

    uaclient.StartBuildInfoStream()

    while True:
        if not uaclient.IsBuilding and OPCUAHelper.BuildingEvent.is_set():
            uaclient.StartEnvLogStream()
        elif uaclient.IsBuilding and not OPCUAHelper.BuildingEvent.is_set():
            uaclient.FinishEnvLogStream()
        time.sleep(1)




    # ---------------------------- Test Robot Server code ----------------------------
    # uaclient.CreateTestBuildInfoSubscribe()
    # uaclient.CreateRobotServerSubscribe()
    # uaclient.StartTestBuildInfoStream()
    #
    # while True:
    #     if not OPCUAHelper.IsBuilding and OPCUAHelper.test_event.is_set():
    #         uaclient.StartRobotServerStream()
    #     elif OPCUAHelper.IsBuilding and not OPCUAHelper.test_event.is_set():
    #         uaclient.FinishRobotServerStream()
    #
    #     time.sleep(1)
    # --------------------------------------------------------------------------------



    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...
    t = Thread(target=MongoHelper.DisplayDBList())
    # OPCUAHelper.event.set()
    t.start()
    uaclient.DisconnectServer()


