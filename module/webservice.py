import json
import configure
import sysmonitor
import message
import web
import messagequeue
import datapersistence
import messagedispatcher
import messageerror
from loghandle import glog

urls = (
	'/push', 'push',
	'/fetch', 'fetch'
)

class push:
    def GET(self):
        #print (web.input())
        return 'hello, world'

    def POST(self):
        params = web.input()
        #check user auth
        user = params['user']
        sysmonitor.SysMonitor.getInstance().addUserRealRequestNumber(user)

        data = web.data()
        info = dict()
        info['userIp'] = web.ctx.ip
        msg = message.Message()
        errcode = msg.buildMessage(data)
        info['errcode'] = errcode
        info['errMsg'] = messageerror.errorDict[errcode]
        if errcode == messageerror.MSG_OK:
            node = messagequeue.MessageQueue.getInstance().pushBack(msg)
            info['msgNo'] = node.data.msgNo
            info['owner'] = node.data.owner
            sysmonitor.SysMonitor.getInstance().addUserMsgOkNumber(user)
        info = json.dumps(info)
        glog.info(info)
        return info

class fetch:
    def GET(self):
        print (web.input())
        return 'xxx'


class WebService(web.application):
    def run(self, port = 8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


if __name__ == '__main__':
    gConfigure = configure.ConfigParser.getInstance()
    gConfigure.start()
    port = gConfigure.getInt('system', 'port')
    msgDispatcher = messagedispatcher.MessageDispatcher() 
    msgDispatcher.start()
    sysmonitor.SysMonitor.getInstance().start()
    sysmonitor.SysMonitor.getInstance().setMessageDispatcher(msgDispatcher)
    dataPersistence = datapersistence.DataPersistence()
    dataPersistence.start()
    app = WebService(urls, globals())
    app.run(port)
