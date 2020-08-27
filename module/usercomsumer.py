import time
import queue
import threading
import sysmonitor
from message import Message
from common.linktable import LinkTable

class UserComsumer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.msgQueue = queue.Queue()
        self.currentMsgNo = -1
        self.currentRecordNo = 0
        self.interval = 3 
        self.user = ""

    def run(self):
        while True:
            if not self.msgQueue.empty():
                print('user comsumer ' + str(self.pop().msgNo) + ' msg')
            else:
                time.sleep(self.interval)
                print("usercomsumer sleep !!!")
            self.setConsumerInfo()
				
	
    def push(self, msg):
        self.msgQueue.put(msg)

    def pop(self):
        msg = self.msgQueue.get()
        self.currentMsgNo = msg.msgNo
        self.currentRecordNo += 1
        return msg

    def size(self):
        return self.msgQueue.qsize()

    def setUser(self, user):
        self.user = user

    def setConsumerInfo(self):
        info = {
            "user" : self.user,
            "qsize" : self.size(),
            "msgNo" : self.currentMsgNo,
            "recordNo" : self.currentRecordNo
            }
        sysmonitor.SysMonitor.getInstance().setConsumerInfo(info)
	
if __name__ == '__main__':
    obj = UserComsumer()
    obj.start()
	

