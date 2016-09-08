from threading import Thread
import Queue
from time import sleep
import time

EVENT_PRINT_ID = 1
EVENT_STOP_ID = 2
EVENT_EXIT_ID = 3

EVENT_DONE = 4

class Event(object):
	def __init__(self, eventId=-1, message=None):
		self.eventId = eventId
		self.message = message

	def getEventId(self):
		return self.eventId

	def setEventId(self, eventId):
		self.eventId = eventId

	def getMessage(self):
		return self.message

	def setMessage(self, message):
		self.message = message

class MyThread(Thread):
	def __init__(self, inQueue, outQueue = None):
		Thread.__init__(self, name = "MyThread")
		self.isRunning = False
		self.queue = inQueue
		self.output = outQueue

	def setRunning(self, state):
		self.isRunning = state

	def run(self):
		if self.queue == None:
			print "event message queue is not initialized!"
			return
		self.isRunning = True
		print "[thread]start"
		while self.isRunning:
			event = self.queue.get(block = True)

			eId = event.getEventId()

			if eId == EVENT_PRINT_ID:
				if self.output != None:
					e = Event(EVENT_DONE, "We have started printing!")
					output.put(e, True)
			elif eId == EVENT_STOP_ID:
				if self.output != None:
					e = Event(EVENT_DONE, "We have stop printing!")
					output.put(e, True)
			elif eId == EVENT_EXIT_ID:
				self.isRunning = False
			self.queue.task_done()
		print "[thread]exit"

if __name__ == "__main__":
	q = Queue.Queue(10)
	output = Queue.Queue(10)
	thread = MyThread(q, output)
	thread.start()

	sleep(1)
	print "put a print event..."
	q.put(Event(EVENT_PRINT_ID), True)
	sleep(1)
	print "put a stop event"
	q.put(Event(EVENT_STOP_ID), True)
	sleep(1)

	start = time.clock()
	while True:
		if time.clock() - start > 5:
			print "time over!"
			break;
		try:
			e = output.get_nowait()
			eId = e.getEventId()
			if eId == EVENT_DONE:
				print "get message: ", e.getMessage()
		except Queue.Empty:
			continue

	print "put an exit event"
	q.put(Event(EVENT_EXIT_ID))
	thread.join()