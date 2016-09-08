#-*- encoding:utf-8 -*-
"""
	Create by newma<newma@live.cn>
"""

class Event(object):
	def __init__(self, id = -1, message = None, obj = None):
		self.__id = id
		self.__message = message
		self.__object = obj

	def getId(self):
		return self.__id

	def setId(self, value):
		self.__id = value

	def getMessage(self):
		return self.__message

	def setMessage(self, value):
		self.__message = value

	def setObject(self):
		return self.__object

	def getObject(self, obj):
		self.__object = obj
