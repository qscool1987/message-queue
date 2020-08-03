import web

urls = ('/index', 'index')

class index:
	def GET(self):
		print (web.input())
		return 'hello, world'

	def POST(self):
		print (web.input())
		print (web.data())
		return 'post req'


if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()
