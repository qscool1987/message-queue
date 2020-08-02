import configure
from message import Message
from common.linktable import LinkTable
from multiprocessing import Process, Lock


class MessageQueue():
	def __init__(self):
		gConfig = configure.ConfigParser.getInstance()
		self.capacity = gConfig.getInt('system', 'max_queue_len') 
		self.queue = LinkTable()
		self.mutex = Lock()
		self.current = self.queue.begin()
		self.msgTable = {}
		
	
	def push(self, msg):
		self.mutex.acquire()
		# push message to queue
		# write here 
		# this queue is double link
		node = self.queue.pushBack(msg)
		self.msgTable[msg.msgNo] = node
		self.mutex.release()

	def pop(self):
		self.mutex.acquire()
		self.queue.popFront()
		self.mutex.release()
	
	def popNode(self, node):
		self.mutex.acquire()
		self.queue.removeNode(node)
		self.msgTable.pop(node.data.msgNo)
		self.mutex.release()

	def currentMessage(self):
		return self.current.data

	def nextMessage(self):
		self.current = self.current.next.data
		return self.current.data

	def size(self):
		return self.queue.size()

	
	def toString(self):
		self.queue.toString()
		print (self.msgTable)


if __name__ == '__main__':
	obj = MessageQueue()
	print (obj.capacity,obj.size(),obj.mutex)	
	for i in range(0,10):
		msg = Message('cool', i)
		msg.setMsgNo(i)
		obj.push(msg)
	obj.toString()
	
