import configure
import message
from multiprocessing import Process, Lock


class MessageQueue():
	def __init__(self):
		gConfig = configure.ConfigParser.getInstance()
		self.capacity = gConfig.getInt('system', 'max_queue_len') 
		self.queue = [None] * self.capacity
		self.realSize = 0
		self.mutex = Lock()
		
	
	def push(self, msg):
		self.mutex.acquire()
		# push message to queue
		# write here 
		# this queue is a loop queue

		self.mutex.release()

	def pop(self):
		pass	


if __name__ == '__main__':
	obj = MessageQueue()
	print (obj.capacity,obj.realSize,obj.mutex)	
