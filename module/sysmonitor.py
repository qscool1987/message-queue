import time
import configure
from collections import OrderedDict
import threading
import json
import copy
from loghandle import glog

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
        self.dispatchInfo = dict()
        self.sysInfo = dict()
        self.receiveInfo = dict()
        self.globalInfo = dict()
        self.publishInfo = dict()
        self.oldInfo = dict()
        

    def run(self):
        while True:
            self.__updateAll()
            time.sleep(self.interval)

    def __calUserQps(self):
        for user in self.publishInfo:
            old = 0
            if user in self.oldInfo:
                old = self.oldInfo[user]['msgRealNum']
            self.publishInfo[user]['qps'] = "%.1f" % (float(self.publishInfo[user]['msgRealNum'] - old) / self.interval)
        
        self.oldInfo = copy.deepcopy(self.publishInfo)

    def __updateAll(self):
        self.mutex.acquire()
        self.__calUserQps()
        self.__updateMemInfo()
        self.__updateGlobalConf()
        self.__updateDispatchInfo()
        ginfo = {
                "publishInfo" : self.publishInfo,
                "dispatchInfo" : self.dispatchInfo,
                "receiveInfo" : self.receiveInfo,
                "globalInfo": self.globalInfo,
                "memFreeRate": self.memFreeRate,
                "memPersistLimit" : self.memPersistLimit,
                "memDataLoadLimit" : self.memDataLoadLimit,
                "isPersist" : self.checkNeedPersistData(),
                "isLoaddata" : self.checkNeedLoadData(),
                }
        ginfo = json.dumps(ginfo)
        glog.info(ginfo)
        self.mutex.release()
            
    def __updateMemInfo(self):
        self.memPersistLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_persist_limit")
        self.memDataLoadLimit = configure.ConfigParser.getInstance().getFloat("system", "memory_data_load_limit")
        memoryInfo = self.__memInfo()
        memTotal = memoryInfo['MemTotal'].split(' ')[0].strip()
        memFree = memoryInfo['MemFree'].split(' ')[0].strip()
        self.memFreeRate = float("%.2f" % (float(memFree) / float(memTotal)))

    def __memInfo(self):
        meminfo = OrderedDict()    
        with open('/proc/meminfo') as f:
            for line in f:
                items = line.strip().split(':')
                meminfo[items[0].strip()] = items[1].strip()
        return meminfo

    def checkNeedPersistData(self):
        memOk = (self.memFreeRate < self.memPersistLimit)
        return memOk

    def checkNeedLoadData(self):
        memOk = (self.memFreeRate > self.memDataLoadLimit)
        return memOk
    
    def setMessageDispatcher(self, dispatcher):
        self.messageDispatcher = dispatcher

    def setConsumerInfo(self, info):
        self.mutex.acquire()
        self.receiveInfo[info['user']] = info
        self.mutex.release()

    def __updateGlobalConf(self):
        self.globalInfo = configure.ConfigParser.getInstance().getGlobalInfo()

    def __updateDispatchInfo(self):
        self.dispatchInfo = self.messageDispatcher.getPublishInfo()

    def addUserRealRequestNumber(self, user):
        self.mutex.acquire()
        if user not in self.publishInfo:
            self.publishInfo[user] = dict()
            self.publishInfo[user]['msgRealNum'] = 0
            self.publishInfo[user]['msgOkNum'] = 0
        self.publishInfo[user]['msgRealNum'] += 1
        self.mutex.release()

    def addUserMsgOkNumber(self, user):
        self.mutex.acquire()
        if user not in self.publishInfo:
            self.publishInfo[user] = dict()
            self.publishInfo[user]['msgRealNum'] = 0
            self.publishInfo[user]['msgOkNum'] = 0
        self.publishInfo[user]['msgOkNum'] += 1
        self.mutex.release()

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
