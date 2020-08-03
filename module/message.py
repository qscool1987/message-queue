import sys
import time

class Message():
	def __init__(self, owner, msgBody):
		self.msgNo = 0
		self.msgBody = msgBody
		self.expireTime = -1
		self.owner = owner
		self.publishTime = -1
		self.subscriptionTime = 1

	def setMsgNo(self, msgNo):
		self.msgNo = msgNo
	
	def setMsgBody(self, msgBody):
		self.msgBody = msgBody

	def setExpireTime(self, expireTime):
		self.expireTime = expireTime
	
	def setOwner(self, owner):
		self.owner = owner

	def setPublishTime(self, publishTime):
		self.publishTime = publishTime

	def setSubscriptionTime(self, subscriptionTime):
		self.subscriptionTime = subscriptionTime

	def droupout(self):
		if self.subscriptionTime <= 0:
			return True
		currTime = int(time.time())
		if currTime >= self.expireTime:
			return True
		return False

if __name__ == '__main__':
	obj = Message('qscool', 'helloworld')
	obj.setMsgNo(123324334)
	obj.setMsgBody('welcome to my github')
	obj.setExpireTime(int(time.time()))
	obj.setPublishTime(int(time.time()) - 100)
	obj.setSubscriptionTime(5)
	print (obj.owner,obj.msgNo,obj.msgBody,obj.expireTime,obj.publishTime,obj.subscriptionTime,obj.droupout())	
		