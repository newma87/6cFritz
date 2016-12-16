#-*- encoding:utf-8 -*-
"""
	Create by newma<newma@live.cn>
"""

class Event(object):
	"""
		Event that send by handler and deal within the looper
	"""
	def __init__(self, id = -1, message = "", object = None):
		self.__id = id
		self.__message = message
		self.__object = object

	def getId(self):
		return self.__id

	def setId(self, value):
		self.__id = value

	def getMessage(self):
		return self.__message

	def setMessage(self, value):
		self.__message = value

	def getObject(self):
		return self.__object

	def setObject(self, obj):
		self.__object = obj
