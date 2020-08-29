import configure
from message import Message
from common.linktable import LinkTable
from multiprocessing import Process, Lock


class MessageQueue():
    _instance = None
    def __init__(self):
        pass

    def __initQueue(self):
        gConfig = configure.ConfigParser.getInstance()
        self.capacity = gConfig.getInt('system', 'max_queue_len') 
        self.queue = LinkTable()
        self.mutex = Lock()
        self.currentMsgNo = 10000	
	
    def pushFront(self, msg):
        self.mutex.acquire()
        if msg.msgNo < 0:
            self.currentMsgNo += 1
            msg.msgNo = self.currentMsgNo
        node = self.queue.pushFront(msg)
        self.mutex.release()

    def popFront(self):
        self.mutex.acquire()
        msgObj = self.queue.popFront()
        self.mutex.release()
        if msgObj is None:
            return None
        return msgObj.data
	
    def pushBack(self, msg):
        self.mutex.acquire()
        if msg.msgNo < 0:
            self.currentMsgNo += 1
            msg.msgNo = self.currentMsgNo
        node = self.queue.pushBack(msg)
        self.mutex.release()
        return node
	
    def size(self):
        return self.queue.size()
	
    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = MessageQueue()
            cls._instance.__initQueue()
        return cls._instance
    
    def toString(self):
        self.queue.toString()


if __name__ == '__main__':
	obj = MessageQueue.getInstance()
	print (obj.capacity,obj.size(),obj.mutex)	
	for i in range(0,10):
		msg = Message('cool', i)
		msg.setMsgNo(i)
		obj.pushBack(msg)
	obj.toString()
	node = obj.popFront()
	while node is not None:
		print (node.data.owner,node.data.msgBody, node.data.msgNo, obj.size())
		node = obj.popFront()
	print (obj.size())

	
