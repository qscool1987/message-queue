import time
import configure
from collections import OrderedDict
import threading

class SysMonitor(threading.Thread):
    _instance = None
    def __init__(self):
        super().__init__()

    def __initMonitor(self):
        self.memFreeRate = None
        self.memPersistLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_persist_limit")
        self.memDataLoadLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_data_load_limit")
        self.interval = 10
        self.mutex = threading.Lock()
        

    def run(self):
        while True:
            self.__update()
            print(self.memFreeRate)
            print(self.checkNeedPersistData())
            print(self.checkNeedLoadData())
            time.sleep(self.interval)
            
    def __update(self):
        memoryInfo = self.__memInfo()
        memTotal = memoryInfo['MemTotal'].split(' ')[0].strip()
        memFree = memoryInfo['MemFree'].split(' ')[0].strip()
        self.mutex.acquire()
        self.memFreeRate = float("%.2f" % (float(memFree) / float(memTotal)))
        self.mutex.release()
        

    def __memInfo(self):
        meminfo = OrderedDict()    
        with open('/proc/meminfo') as f:
            for line in f:
                items = line.strip().split(':')
                meminfo[items[0].strip()] = items[1].strip()
        return meminfo

    def checkNeedPersistData(self):
        self.mutex.acquire()
        memOk = (self.memFreeRate < self.memPersistLimit)
        self.mutex.release()
        return memOk

    def checkNeedLoadData(self):
        self.mutex.acquire()
        memOk = (self.memFreeRate > self.memDataLoadLimit)
        self.mutex.release()
        return memOk

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = SysMonitor()
            cls._instance.__initMonitor()
        return cls._instance




if __name__ == '__main__':
    SysMonitor.getInstance().start()
