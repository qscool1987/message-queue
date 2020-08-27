import os
import configparser
import setting
import time
import threading
import json


class ConfigParser(threading.Thread):
    _instance = None

    def __init__(self):
        super().__init__()
        self.interval = 10

    def __initConf(self, confPath):
        cf = configparser.ConfigParser()
        cf.read(confPath, encoding='utf8')
        self.configDict = cf

    def run(self):
        while True:
            self.__initConf(setting.confDir + setting.confFile)
            print("init conf")
            port = self.getInt('system', 'port')
            print(port)
            time.sleep(self.interval)

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

    def getGlobalInfo(self):
        info = {}
        info['max_concurrency_thread'] = self.getInt('system', 'max_concurrency_thread')
        info['memory_data_load_limit'] = self.getFloat('system', 'memory_data_load_limit')
        info['memory_persist_limit'] = self.getFloat('system', 'memory_persist_limit')
        info['max_queue_len'] = self.getInt('system', 'max_queue_len')
        info['port'] = self.getInt('system', 'port')
        info['record_limit'] = self.getInt('persist', 'record_limit')
        return info

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = ConfigParser()
            cls._instance.__initConf(setting.confDir + setting.confFile)
        return cls._instance
		
		


if __name__ == '__main__':
    obj = ConfigParser.getInstance()
    obj.start()
		

