import os
import time
import threading
import configure
import message
import sysmonitor
import messagequeue


class DataPersistence(threading.Thread):

    def __init__(self):
        super().__init__()
        self.interval = 30
        self.dataDir = configure.ConfigParser.getInstance().getString("persist","data_dir")
        self.recordLimit = configure.ConfigParser.getInstance().getInt("persist","record_limit")
        self.currentRecordNo = 0
        self.needPersist = False
        self.needLoad = False
        self.messageQueue = messagequeue.MessageQueue.getInstance()
        self.fPersist = None
        self.fileLoadNo = 0
    
    def run(self):

        while True:
            memFree = sysmonitor.SysMonitor.getInstance().memFreeRate
            print (memFree)
            if self.needPersist:
                self.persistData()
            if self.needLoad:
                self.loadData()
            self.needPersist = sysmonitor.SysMonitor.getInstance().checkNeedPersistData()
            self.needLoad = sysmonitor.SysMonitor.getInstance().checkNeedLoadData()


    def persistData(self):
        print("persist data")
        msg = self.messageQueue.popFront()
        if msg:
            msgStr = msg.dumpMessage() + "\n"
            print(msgStr)
            fileNo = self.currentRecordNo / self.recordLimit
            print('fileNo is %d' % fileNo)
            if self.fPersist is None:
                fileName = self.dataDir + "/" + str(fileNo) + ".data"
                print(fileName)
                self.fPersist = open(fileName, 'a+')
            elif self.currentRecordNo % self.recordLimit == 0:
                self.fPersist.close()
                fileName = self.dataDir + "/" + str(fileNo) + ".data"
                print(fileName)
                self.fPersist = open(fileName, 'a+')
            self.fPersist.write(msgStr)
            self.fPersist.flush()
        else:
            time.sleep(self.interval)

    def loadData(self):
        print("load data")
        fileName = self.dataDir + "/" + str(self.fileLoadNo) + ".data"
        if os.path.exists(fileName):
            with open(fileName) as fLoad:
                for line in fLoad:
                    msgStr = line.strip()
                    msg = message.Message()
                    msg.buildMessage(msgStr)
                    self.messageQueue.pushBack(msg)

        else:
            time.sleep(self.interval)


if __name__ == '__main__':
    sysmonitor.SysMonitor.getInstance().start()
    obj = DataPersistence()
    obj.start()
