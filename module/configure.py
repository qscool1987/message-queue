import os
import configparser

/*
** global configure class
**
*/

class ConfigParser():

	def __init__(self, confPath):
		self.configDict = self.initConf(confPath)

	def initConf(self, confPath):
		cf = configparser.ConfigParser()
		cf.read(confPath, encoding='utf8')
		return cf

	def getSector(self, sector):
		sectors = self.configDict.sections()
		if sector in sectors:
			return self.configDict.items(sector)
		return None

	def getConfigDict(self):
		return slef.configDict



if __name__ == '__main__':
	obj = ConfigParser('../conf/global')
	print (obj.getSector('system'))
	print (obj.getSector('log'))
	print (obj.getSector('user'))
	print (obj.getSector('subscription'))	
		

