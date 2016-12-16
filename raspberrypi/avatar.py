#-*- encoding:utf-8 -*-
from smarttoy.fritz import FritzRobot
from smarttoy.thread import *
import threading
import time

class Avatar(looper.Looper):
	CHECK_CONNECT_STATE_TIME = 1000 # every 1s check for connect
	class AvatarHandler(handler.Handler):
		def getAvatar(self):
			return self.getLooper()
		def getRobot(self):
			return self.getAvatar().getRobot()

	def __init__(self):	
		looper.Looper.__init__(self)

		self.__robot = FritzRobot()
		self.__lastClock = 0
		self.__onConnectStateCallback = None

		#start work thread
		self.__workThread = threading.Thread(target = self.__run)
		self.__workThread.start()

	def __invoke(self, cbState, *args):
		if cbState and len(cbState) > 0:
			cb = cbState[0]
			cbArgs = list(cbState[1])
			for arg in args:
				cbArgs.append(arg)
			apply(cb, cbArgs)

	def __run(self):
		print "[Debug]Avatar: work thread start"
		self.prepare()
		self.loop()
		print "[Debug]Avatar: work thread end"

	#override
	def  idle(self, force = False):
		now = int((time.time() + 0.5) * 1000)
		if force or now - self.__lastClock > Avatar.CHECK_CONNECT_STATE_TIME:
			self.__lastClock = now
			robot = self.__robot
			if not robot.isConnected():
				self.__invoke(self.__onConnectStateCallback, False, None)
				#print "[Debug]Avatar: searching for board..."
				port = robot.findBoard()
				if port:
					self.__invoke(self.__onConnectStateCallback, True, port)

	def registConnectStateCallback(self, callback, *args):
		self.__onConnectStateCallback = [callback, args]

	def isConnected(self):
		return self.__robot.isConnected

	def getRobot(self):
		return self.__robot

	def release(self):
		self.exit()
		self.__workThread.join()
		self.__workThread = None
		self.__robot.close()
		self.__robot = None

if __name__ == '__main__':
	ROBOT_CONNECT = 1
	ROBOT_DISCONNECT = 2
	class AvatarHandler(Avatar.AvatarHandler):
		def connect(self):
			return self.sendEvent(event.Event(id = ROBOT_CONNECT))

		def disconnect(self):
			return self.sendEvent(event.Event(id = ROBOT_DISCONNECT))

		def handle_message(self, event):
			eId = event.getId()
			looper = self.getLooper()
			robot = looper.getRobot()

			# handler message
			if eId == ROBOT_CONNECT:
				looper.idle(True)
			elif eId == ROBOT_DISCONNECT:
				if robot.isConnected():
					robot.close()
			else:
				print "[Error]Avatar: unknown event id of %d" % (eId)

	ava = Avatar()
	handler = AvatarHandler(ava)

	def onConnect(result, port):
		if result:
			print "connect to port \"%s\" successfully!" % (port)
		else:
			print "fritz is disconnected!"

	ava.registConnectStateCallback(onConnect)
	handler.connect()
	time.sleep(5)
	handler.disconnect()
	time.sleep(5)
	ava.release()
