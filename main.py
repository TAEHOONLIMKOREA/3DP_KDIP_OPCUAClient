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
    uaclient.SubscribeBuildInfoNode()
    uaclient.SubscribeRobotServer()

    uaclient.StartBuildInfoStream()


    while True:
        if not OPCUAHelper.IsBuilding and OPCUAHelper.event.is_set():
            uaclient.StartRobotServerStream()
        elif OPCUAHelper.IsBuilding and not OPCUAHelper.event.is_set():
            uaclient.FinishRobotServerStream()

        # a = input()
        # if (a == 'exit'):
        #     uaclient.UnSubscribeBuildInfoNode()
        #     break
        # elif(a == 'Start'):
        #     event.set()
        time.sleep(1)




    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...
    t = Thread(target=MongoHelper.DisplayDBList())
    # OPCUAHelper.event.set()
    t.start()
    uaclient.DisconnectServer()


    # time.sleep(10)
    # OPCUAHelper.event.clear()




    # print('Script Start!')
    # for i in range(1, 6):
    #     time.sleep(3)
    #     print('for loop #{}'.format(i))
    #     if i == 4:
    #         event.clear()
    # print('Script End!')


