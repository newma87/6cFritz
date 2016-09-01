#-*-coding:utf-8-*-

import Handler
import Queue.Queue as Queue
import Queue.Empty as Empty
from time import sleep

__SLEEP_SECOND =  1  # delay time when event queue is empty

__all__ = ['Looper']

class Looper(object):
	mainLooper = None

	def __init__(self):
		self.handlers = None
		self.queue = None

	def prepare(self):		
		self.handlers = []
		self.queue = Queue()

	def run(self):
		while (True):
			if not self.queue.empty():
				try :
					itme = self.queue.get(True, __SLEEP_SECOND * 1000) # block get
				except Empty:
					continue
			else:
				sleep(__SLEEP_SECOND)		# wait for 1 second

	def getQueue(self):
		return self.queue

	def addHandler(self, handler):
		pass

	def removeHandler(self, handler):
		pass
