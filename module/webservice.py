import json
import configure
import message
import web
import messagequeue
import messagedispatcher

urls = (
	'/push', 'push',
	'/fetch', 'fetch'
)

class push:
	def GET(self):
		print (web.input())
		return 'hello, world'

	def POST(self):
		data = web.data()
		print (data)
		msg = message.Message()
		msg.buildMessage(data)
		messagequeue.MessageQueue.getInstance().pushBack(msg)
		return 'successful'

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
	port = gConfigure.getInt('system', 'port')
	msgDispatcher = messagedispatcher.MessageDispatcher() 
	msgDispatcher.start()
	app = WebService(urls, globals())
	app.run(port)
