#-*- coding:utf-8 -*-

"""
	Created by newma<newma@live.cn>
"""

from abc import ABCMeta, abstractmethod
from Event import Event
import Looper
import Queue

__SEND_MESSAGE_TIMEOUT__ = 30 # seconds 

class Handler(object):
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

	def sendEvent(self, event = None, eventId = -1, message = None):
		if event == None:
			if eventId == -1:
				print "[error]Handler.sendEvent: wrong arguments"
				return False
			event = Event(id = eventId, message = message)
		try:
			queue = self.__looper.getQueue()
			queue.put(event, True, __SEND_MESSAGE_TIMEOUT__)
			return True
		except Queue.Full:
			print "[error]Handler.sendEvent: send time out, please try again"
		return False
