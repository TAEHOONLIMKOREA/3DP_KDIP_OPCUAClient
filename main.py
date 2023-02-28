from helper import OPCUAHelper
from helper import InfluxDBHelper

from threading import Thread, Event
import time

event = Event()

def infinite_loop():
    while event.is_set():
        time.sleep(1)
        print('Infinite Loop Thread!')

    print('Infinite Loop Stop!')
    return


if __name__ == '__main__':
    # damon을 True로 해주면 메인쓰레드가 종료될때 함께 종료됨...
    t = Thread(target=infinite_loop, daemon=True)
    event.set()
    t.start()

    print('Script Start!')
    for i in range(1, 6):
        time.sleep(3)
        print('for loop #{}'.format(i))
        if i == 4:
            event.clear()
    print('Script End!')



    # InfluxDBHelper.CreateDB()
    # OPCUAHelper.ConnectServer()