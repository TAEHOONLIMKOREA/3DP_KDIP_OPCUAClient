from helper import OPCUAHelper
from helper import InfluxDBHelper
from threading import Thread
from helper import MongoHelper
import time


url = "opc.tcp://localhost:26543"


if __name__ == '__main__':
    # InfluxDBHelper.CreateDB()
    uaclient = OPCUAHelper.UaClient(url)
    uaclient.ConnectServer()
    uaclient.StartTestRobotServer()
    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...

    t = Thread(target=MongoHelper.DisplayDBList())
    # OPCUAHelper.event.set()
    t.start()


    # time.sleep(10)
    # OPCUAHelper.event.clear()




    # print('Script Start!')
    # for i in range(1, 6):
    #     time.sleep(3)
    #     print('for loop #{}'.format(i))
    #     if i == 4:
    #         event.clear()
    # print('Script End!')


