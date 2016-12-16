#-*-coding:utf-8-*-

import Queue

__MAX_MESSAGE_QUEUE__ = 50  #max message queue
__PUSH_MESSAGE_TIMEOUT__ = 30 # seconds 

class Looper(object):
	"""
		Looper that deal with event queue run in thread
	"""
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
			self.dispatchOneMessage()
			self.idle()

	def dispatchOneMessage(self):
		if not self.__queue.empty():
			msg = self.__queue.get_nowait()
			if msg[1] is None:
				for h in self.__handlers:
					h.handle_message(msg[0])
			else:
				msg[1].handle_message(msg[0])

	def getQueue(self):
		return self.__queue

	def pushEvent(self, event, handler = None):
		try:
			self.__queue.put((event, handler), True, __PUSH_MESSAGE_TIMEOUT__)
			return True
		except Queue.Full:
			print "[error]Handler.sendEvent: send time out, please try again"
		return False

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
	def idle(self):
		pass
