import time
import threading
from message import Message
from common.linktable import LinkTable, LinkNode

class MessageTable():
	def __init__(self):
		self.msgTable = dict()
		self.mutex = threading.Lock()

	def insert(self, node):
		self.mutex.acquire()
		self.msgTable[node.data.msgNo] = node
		print('insert ' + str(node.data.msgNo) + ' msg')
		self.mutex.release()

	def pop(self, node):
		self.mutex.acquire()
		self.msgTable.pop(node.data.msgNo)
		self.mutex.release()

	def size(self):
		return len(self.msgTable)

	def fetch(self, msgNo):
		self.mutex.acquire()
		node = self.msgTable[msgNo]
		self.mutex.release()
		return node

	def comsume(self, node):
		self.mutex.acquire()
		self.msgTable[node.data.msgNo].subscriptionTime -= 1
		self.mutex.release()
		
	

if __name__ == '__main__':
	obj = MessageTable()
	for i in range(0,10):
		msg = Message('cool',i);
		msg.setMsgNo(100 + i);
		node = LinkNode(msg)
		obj.insert(node)
	print (obj.size())
	node = obj.fetch(102)
	print (node.data.msgNo,node.data.owner,node.data.msgBody)
	obj.pop(node)
	print (obj.size())
