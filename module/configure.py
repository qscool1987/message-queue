import os
import configparser
import setting


class ConfigParser():
	_instance = None

	def __init__(self):
		pass

	def __initConf(self, confPath):
		cf = configparser.ConfigParser()
		cf.read(confPath, encoding='utf8')
		self.configDict = cf

	def getSector(self, sector):
		sectors = self.configDict.sections()
		if sector in sectors:
			return self.configDict.items(sector)
		return None

	def getConfigDict(self):
		return self.configDict

	def getInt(self, sector, name):
		return self.configDict.getint(sector, name)

	def getFloat(self, sector, name):
		return self.configDict.getfloat(sector, name)

	def getString(self, sector, name):
		return self.configDict.get(sector, name)

	@classmethod
	def getInstance(cls):
		if not cls._instance:
			cls._instance = ConfigParser()
			cls._instance.__initConf(setting.confDir + setting.confFile)
		return cls._instance
		
		


if __name__ == '__main__':
	obj = ConfigParser.getInstance()
	print (obj.getSector('system'))
	print (obj.getSector('log'))
	print (obj.getSector('user'))
	print (obj.getSector('subscription'))	
	print (obj.getFloat('system', 'memory_limit'))
	print (obj.getInt('system', 'max_queue_len'))
	print (obj.getString('subscription', 'name'))
		

