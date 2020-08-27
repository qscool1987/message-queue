import time
import configure
from collections import OrderedDict
import threading
import json

class SysMonitor(threading.Thread):
    _instance = None
    def __init__(self):
        super().__init__()

    def __initMonitor(self):
        self.memFreeRate = 0.5
        self.memPersistLimit = 0.3
        self.memDataLoadLimit = 0.8
        self.interval = 10
        self.mutex = threading.Lock()
        self.publishInfo = dict()
        self.sysInfo = dict()
        self.receiveInfo = dict()
        self.globalInfo = dict()
        

    def run(self):
        while True:
            self.__updateAll()
            print(self.memFreeRate)
            print(json.dumps(self.publishInfo))
            print(json.dumps(self.receiveInfo))
            print(json.dumps(self.globalInfo))
            time.sleep(self.interval)

    def __updateAll(self):
        self.__updateMemInfo()
        self.__updateGlobalConf()
        self.__updatePublishInfo()
            
    def __updateMemInfo(self):
        self.memPersistLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_persist_limit")
        self.memDataLoadLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_data_load_limit")
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
    
    def setMessageDispatcher(self, dispatcher):
        self.messageDispatcher = dispatcher

    def setConsumerInfo(self, info):
        self.mutex.acquire()
        self.receiveInfo[info['user']] = info
        self.mutex.release()

    def __updateGlobalConf(self):
        self.globalInfo = configure.ConfigParser.getInstance().getGlobalInfo()

    def __updatePublishInfo(self):
        self.publishInfo = self.messageDispatcher.getPublishInfo()

    def getSysAllInfo(self):
        pass
    
    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = SysMonitor()
            cls._instance.__initMonitor()
        return cls._instance






if __name__ == '__main__':
    SysMonitor.getInstance().start()
