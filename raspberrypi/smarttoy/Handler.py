#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
from Looper import Looper

class Event(object):
	def __init__(self):
		self.event = 0
		self.message = ""
		self.object = None

	def getEvent(self):
		return self.event

	def setEvent(self, value):
		self.event = value

	def getMessage(self):
		return self.message

	def setMessage(self, value):
		self.message = value

	def setObject(self):
		return self.object

	def getObject(self, obj):
		self.object = obj


class Handler(object):
	__metaclass__ = ABCMeta

	def __init__(self, loop):
		self.queue = loop.getQueue()

	@abstractmethod
	def handle_message(self, event):
		pass
