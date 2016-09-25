#-*- encoding:utf-8 -*-
"""
	Created by newma<newma@live.cn>
"""

import util
import os
from json import *
import types

class UserDefault(object):
	"""
		Used to storage some permanent user data
	"""

	def __init__(self, storage_file = 'app_data_storage.json', storage_dir = '.smarttoy'):
		self.json_file = storage_file
		self.directory = storage_dir
		self.valueMap = {} 

	def getBool(self, name, defVal = False):
		val = self.valueMap.get(name)
		if (val == None):
			return defVal
		if not (type(val) is types.BooleanType):
			print "[warning]UserDefault.getBool: get the wrong type, return default value"
			return defVal
		return val
	def setBool(self, name, value):
		if (not type(value) is types.BooleanType):
			print "[error]UserDefault.setBool: value argument type is wrong"
			return
		self.valueMap[name] = value

	def getString(self, name, defVal = None):
		val = self.valueMap.get(name)
		if (val == None):
			return defVal
		if not (type(val) is types.StringType):
			print "[warning]UserDefault.getString: get the wrong type, return default value"
			return defVal
		return val
	def setString(self, name, value):
		if (not type(value) is types.StringType):
			print "[error]UserDefault.setString: value argument type is wrong"
			return
		self.valueMap[name] = value

	def getInt(self, name, defVal = 0):
		val = self.valueMap.get(name)
		if (val == None):
			return defVal
		if not (type(val) is types.IntType):
			print "[warning]UserDefault.getInt: get the wrong type, return default value"
			return defVal
		return val
	def setInt(self, name, value):
		if (not type(value) is types.IntType):
			print "[error]UserDefault.setInt: value argument type is wrong"
			return
		self.valueMap[name] = value

	def getFloat(self, name, defVal = "0.0"):
		val = self.valueMap.get(name)
		if (val == None):
			return defVal
		if not (type(val) is types.FloatType):
			print "[warning]UserDefault.getFloat: get the wrong type, return default value"
			return defVal
		return val
	def setFloat(self, name, value):
		if (not type(value) is types.FloatType):
			print "[error]UserDefault.setFloat: value argument type is wrong"
			return
		self.valueMap[name] = value

	def getLong(self, name, defVal = 0):
		val = self.valueMap.get(name)
		if (val == None):
			return defVal
		if not (type(val) is types.LongType):
			print "[warning]UserDefault.getLong: get the wrong type, return default value"
			return defVal
		return val
	def setLong(self, name, value):
		if (not type(value) is types.LongType):
			print "[error]UserDefault.setLong: value argument type is wrong"
			return
		self.valueMap[name] = value

	def save(self):
		path = os.path.join(util.getUserDataFold(), self.directory)
		file = os.path.join(path, self.json_file)
		if (not os.path.exists(path)):
			os.makedirs(path)

		fp = None
		if (os.path.exists(file)):
			fp = open(file, 'w')
		else:
			fp = open(file, 'a')
		data = JSONEncoder().encode(self.valueMap)
		fp.write(data)
		fp.flush()
		fp.close()

	def load(self):
		path = os.path.join(util.getUserDataFold(), self.directory)
		file = os.path.join(path, self.json_file)
		if (not os.path.exists(file)):
			print "[warning]UserDefault.load: not storage file exits!"
			return
		fp = open(file, 'r')
		data = fp.read()
		fp.close()
		self.valueMap = JSONDecoder().decode(data)

	def dump(self):
		keys = self.valueMap.keys()
		print "{"
		for k in keys:
			print "\t", k, "=", self.valueMap[k]
		print "}"

if __name__ == '__main__':
	ud = UserDefault("testfile.json", ".smarttoy")
	ud.load()
	ud.dump()

	ud.setString("user_name", "newma")
	ud.setString("user_descript", "nothing")
	ud.setInt("user_goal", 200)

	ud.save()
