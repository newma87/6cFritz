#-*-coding:utf-8-*-

import Handler
import Queue

__MAX_MESSAGE_QUEUE__ = 50  #max message queue

class Looper(object):
	mainLooper = None

	def __init__(self):
		self.__queue = Queue.Queue(__MAX_MESSAGE_QUEUE__)
		self.__isReady = False
		self.__isRunning = False
		self.__handlers = []

	def isReady(self):
		return self.__isReady

	def prepare(self):
		self.__isRunning = True
		self.__isReady = True

	def loop(self):
		if not self.isReady():
			print "[error]Looper.loop: Looper is not ready, did you forget to call prepare?"
			return
		while self.__isRunning:
			if not self.__queue.empty():
				event = self.__queue.get_nowait()
				for h in self.__handlers:
					h.handle_message(event)
			self.logic()

	def getQueue(self):
		return self.__queue

	def exit(self):
		self.__isRunning = False

	def addHandler(self, handler):
		self.__handlers.append(handler)
		return len(self.__handlers)

	def removeHandler(self, handlerId = -1, handler = None):
		if handlerId != -1:
			if handlerId > len(self.__handlers):
				print "[warn]Looper.removeHandler: handler id is not available!"
				return
			self.__handlers.pop(handlerId - 1)
		elif handler != None:
			self.__handlers.remove(handler)

	# for override
	def logic(self):
		pass
