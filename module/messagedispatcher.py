import time
from common.linktable import LinkTable
from message import Message
import messagequeue
import threading
from usermanager import UserManager
import sysmonitor

class MessageDispatcher(threading.Thread):
    def __init__(self):
        super().__init__()
        self.msgQueue = messagequeue.MessageQueue.getInstance()
        self.userManager = UserManager()
        self.interval = 3
        self.dispatchClose = False
        self.publishInfo = dict()

    def run(self):
        while True:
            if not self.dispatcher():
                time.sleep(self.interval)	

    def dispatcher(self):
        self.dispatchClose = sysmonitor.SysMonitor.getInstance().checkNeedPersistData()
        if self.dispatchClose:
            return False
        obj = self.msgQueue.popFront()
        if obj is not None:
            if obj.owner not in self.publishInfo:
                self.publishInfo[obj.owner] = dict()
                self.publishInfo[obj.owner]['dispatchTotal'] = 0
            self.publishInfo[obj.owner]['dispatchTotal'] += 1
            self.publishInfo[obj.owner]['maxMsgNo'] = obj.msgNo
            self.userManager.dispatcher(obj)
            return True
        return False

    def getPublishInfo(self):
        return self.publishInfo


if __name__ == '__main__':
    sysmonitor.SysMonitor.getInstance().start()
    dispatcher = MessageDispatcher()
    dispatcher.start()
    time.sleep(1000)
		

