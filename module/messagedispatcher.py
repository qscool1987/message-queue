import time
from common.linktable import LinkTable
from message import Message
import messagequeue
import threading
from usermanager import UserManager

class MessageDispatcher(threading.Thread):
	def __init__(self, msgQueue, userManager):
		super().__init__()
		self.msgQueue = msgQueue
		self.userManager = userManager
		self.interval = 0.5

	def run(self):
		while True:
			if not self.dispatcher():
				time.sleep(self.interval)		

	def dispatcher(self):
		obj = self.msgQueue.pop()
		if obj is not None:
			self.userManager.dispatcher(obj)
			print('finish dispatch ' + str(obj.data.msgNo) + 'msg')
			return True
		return False


if __name__ == '__main__':
	obj = messagequeue.MessageQueue()
	print (obj.capacity,obj.size(),obj.mutex)	
	for i in range(0,10):
		msg = Message('cool', i)
		msg.setMsgNo(1000 + i)
		obj.push(msg)
	obj.toString()
	userManager = UserManager()
	dispatcher = MessageDispatcher(obj, userManager)
	dispatcher.start()
	while obj.size() > 0:
		node = obj.pop()
		dispatcher.dispatcher(node)
		
	time.sleep(1000)
		

