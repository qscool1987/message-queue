import time
from common.linktable import LinkTable
from message import Message
import messagequeue
import threading
from usercomsumer import UserComsumer
from messagetable import MessageTable

class UserManager():
	def __init__(self):
		self.userComsumers = dict()
		self.msgTable = MessageTable()

	def dispatcher(self, node):
		name = node.data.owner
		if name not in self.userComsumers:
			self.userComsumers[name] = UserComsumer()
			self.userComsumers[name].start()
		self.userComsumers[name].push(node)
		self.msgTable.insert(node)
	
	def fetchMessage(self, msgNo):
		return self.msgTable.fetch(msgNo)



if __name__ == '__main__':
	obj = LinkTable()
	end = obj.end()
	for i in range(0,10):
		msg = Message('cool',i)
		msg.setMsgNo(1000 + i)
		obj.pushBack(msg)
	obj.toString()

	userManager = UserManager()
	while obj.size() > 0:
		node = obj.popFront()
		userManager.dispatcher(node)
	while True:
		time.sleep(1000)
	
	
	
	
