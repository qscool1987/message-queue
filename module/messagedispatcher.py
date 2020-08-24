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

    def run(self):
        while True:
            if not self.dispatcher():
                time.sleep(self.interval)	
                print('dispatcher: no msg to dispatcher')	

    def dispatcher(self):
        self.dispatchClose = sysmonitor.SysMonitor.getInstance().checkNeedLoadData()
        if self.dispatchClose:
            return False
        obj = self.msgQueue.popFront()
        if obj is not None:
            self.userManager.dispatcher(obj)
            print('dispatch ' + str(obj.data.msgNo) + 'msg')
            return True
        return False


if __name__ == '__main__':
    sysmonitor.SysMonitor.getInstance().start()
    dispatcher = MessageDispatcher()
    dispatcher.start()
    time.sleep(1000)
		

