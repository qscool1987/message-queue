import time
import queue
import threading
from message import Message
from common.linktable import LinkTable

class UserComsumer(threading.Thread):
	def __init__(self):
		super().__init__()
		self.msgQueue = queue.Queue()
		self.interval = 3 

	def run(self):
		while True:
			if not self.msgQueue.empty():
				print('user comsumer ' + str(self.pop().data.msgNo) + ' msg')
			else:
				time.sleep(self.interval)
				print("usercomsumer sleep !!!")
			
			
	
	def push(self, node):
		self.msgQueue.put(node)

	def pop(self):
		return self.msgQueue.get()

	def size(self):
		return self.msgQueue.qsize()
	
if __name__ == '__main__':
	obj = LinkTable()
	end = obj.end()
	for i in range(0,10):
		msg = Message('cool', i)
		msg.setMsgNo(1000 + i)
		obj.pushBack(msg)
	obj.toString()
	ut = UserComsumer()
	ut.start()
	while obj.size() > 0:
		node = obj.popFront()
		ut.push(node)
	ut.join()
	print ('main thread quit')	
	

