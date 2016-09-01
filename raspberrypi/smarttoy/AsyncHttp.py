#-*- code:utf-8 -*-
import urllib2
import threading.Thread
import Queue

class HttpRequest(Thread):
	def __init__(self, name = None):
		self.name = name
		Thread.__init__(self)
