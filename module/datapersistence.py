import os
import time
import threading
import setting
import configure
import message
import sysmonitor
import messagequeue


class DataPersistence(threading.Thread):

    def __init__(self):
        super().__init__()
        self.interval = 30
        self.dataDir = setting.DATA_PATH
        self.recordLimit = configure.ConfigParser.getInstance().getInt("persist","record_limit")
        self.currentRecordNo = 0
        self.needPersist = False
        self.needLoad = False
        self.messageQueue = messagequeue.MessageQueue.getInstance()
        self.fPersist = None
        self.fileLoadNo = 0
        self.filePersistNo = 0

    def run(self):

        while True:
            memFree = sysmonitor.SysMonitor.getInstance().memFreeRate
            if self.needPersist:
                self.persistData()
            if self.needLoad:
                self.loadData()
            self.needPersist = sysmonitor.SysMonitor.getInstance().checkNeedPersistData()
            self.needLoad = sysmonitor.SysMonitor.getInstance().checkNeedLoadData()



    def persistData(self):
        msg = self.messageQueue.popFront()
        if msg:
            msgStr = msg.dumpMessage() + "\n"
            if self.fPersist is None:
                fileName = self.dataDir + "/" + str(self.filePersistNo) + ".data"
                self.fPersist = open(fileName, 'a+')
            elif self.currentRecordNo % self.recordLimit == 0:
                self.fPersist.close()
                self.filePersistNo += 1
                fileName = self.dataDir + "/" + str(self.filePersistNo) + ".data"
                self.fPersist = open(fileName, 'a+')
            self.fPersist.write(msgStr)
            self.fPersist.flush()
            self.currentRecordNo += 1
        else:
            time.sleep(self.interval)

    def loadData(self):
        fileName = self.dataDir + "/" + str(self.fileLoadNo) + ".data"
        if os.path.exists(fileName):
            with open(fileName) as fLoad:
                for line in fLoad:
                    msgStr = line.strip()
                    msg = message.Message()
                    msg.buildMessage(msgStr)
                    self.messageQueue.pushBack(msg)
            self.fileLoadNo += 1

        else:
            time.sleep(self.interval)


if __name__ == '__main__':
    sysmonitor.SysMonitor.getInstance().start()
    obj = DataPersistence()
    obj.start()
