import sys
import time
import json
from loghandle import glog

class Message():
    def __init__(self, owner="", msgBody=""):
        self.msgNo = -1 
        self.msgBody = msgBody
        self.expireTime = -1
        self.owner = owner
        self.publishTime = -1
        self.subscriptionTime = 0

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

    def buildMessage(self, data):
        data = json.loads(data)
        if 'owner' in data:
            self.setOwner(data['owner'])
        if 'msgBody' in data:
            self.setMsgBody(data['msgBody'])
        if 'publishTime' in data:
            self.setPublishTime(data['publishTime'])
        if 'msgNo' in data:
            self.setMsgNo(data['msgNo'])
        if 'expireTime' in data:
            self.setExpireTime(data['expireTime'])
        else:
            self.setExpireTime(int(time.time()) + 86400)
        if 'subscriptionTime' in data:
            self.setSubscriptionTime(data['subscriptionTime'])

    def dumpMessage(self):
        obj = {
            'msgNo': self.msgNo,
            'msgBody': self.msgBody,
            'expireTime': self.expireTime,
            'owner': self.owner,
            'publishTime': self.publishTime,
            'subscriptionTime': self.subscriptionTime
        }
        return json.dumps(obj)

    def droupout(self):
        if self.subscriptionTime <= 0:
            return True
        currTime = int(time.time())
        if currTime >= self.expireTime:
            return True
        return False

if __name__ == '__main__':
    '''msg = Message()
    obj = {
        "msgNo": 100,
        "msgBody": "xxxxyyysdfdf",
        "expireTime": 123434345,
        "owner": "qinshuai",
        "publishTime": 12434555,
        "subscriptionTime": 3
    }
    msgStr = json.dumps(obj)
    msg.buildMessage(msgStr)
    print(msg.msgNo,msg.msgBody,msg.expireTime,msg.owner,msg.publishTime,msg.subscriptionTime)
    res = msg.dumpMessage()
    print (res)
    '''
    glog.warning("message py")
