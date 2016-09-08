#-*- encoding:utf-8 -*-

from smarttoy.thread import Event, Looper, Handler
import threading
from time import sleep

EVENT_EXIT = 1
EVENT_SAY_HELLO = 2

class MyHanlder(Handler.Handler):
	def handle_message(self, event):
		eid = event.getId()
		if eid == EVENT_EXIT:
			print "I got an exit, I must go die"
			self.getLooper().exit()
		elif eid == EVENT_SAY_HELLO:
			print event.getMessage()

class MyThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.looper = Looper.Looper()
		self.handler = MyHanlder(self.looper)

	def getHandler(self):
		return self.handler

	def run(self):
		print "thread start..."
		self.looper.prepare()
		self.looper.loop()
		print "thread end..."

if __name__ == "__main__":
	thread = MyThread()
	thread.start()

	sleep(1)
	print "send thread say hello"
	thread.getHandler().sendEvent(eventId = EVENT_SAY_HELLO, message = "Hello, this is come from main and say in thread")
	sleep(3)
	print "send exit to looper"
	thread.getHandler().sendEvent(eventId = EVENT_EXIT)
	thread.join()
