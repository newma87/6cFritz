#-*- coding:utf-8 -*-

"""
	Created by newma<newma@live.cn>
"""

from abc import ABCMeta, abstractmethod
from event import Event
import Queue

class Handler(object):
	"""
		Abstract class that communicate with looper, sending event to looper event message queue
		To do that, you have to implement the handle_message method of a subclass that inherit from this class
	"""
	__metaclass__ = ABCMeta

	def __init__(self, looper):
		self.attach(looper)

	def getLooper(self):
		return self.__looper

	def attach(self, looper):
		self.__looper = looper
		self.__looper.addHandler(self)

	def dettach(self):
		if self.__looper != None:
			self.__looper.removeHandler(handler = self)
			self.__looper = None

	@abstractmethod
	def handle_message(self, event):
		pass

	# Send event to be handled by current handler
	def sendEvent(self, event = None, id = -1, message = None, object = None):
		if event == None:
			if id == -1:
				print "[error]Handler.sendEvent: wrong arguments"
				return False
			event = Event(id = id, message = message, object = object)
		return self.__looper.pushEvent(event, self)

	# Send event to all handlers added to Looper
	def broadcastEvent(self, event = None, id = -1, message = None, object = None):
		if event == None:
			if id == -1:
				print "[error]Handler.sendEvent: wrong arguments"
				return False
			event = Event(id = id, message = message, object = object)
		return self.__looper.pushEvent(event)
