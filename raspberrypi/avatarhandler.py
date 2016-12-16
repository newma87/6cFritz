#-*- encoding:utf-8 -*-
from smarttoy.thread import *
from avatar import Avatar
import application as app
import uihandler as ui

U2A_CONNECT = 1
U2A_DISCONNECT = 2
U2A_LOAD_CONFIG = 3
U2A_SAVE_CONFIG = 4

U2A_RUN_IN_AVATAR_THREAD = 0xff

class AvatarHanlder(Avatar.AvatarHandler):
	"""
		Handler that communicate with avatar thread
	"""
	def sendToUIThread(self, **kwArg):
		handler = app.Application().getUIHandler()
		handler.sendEvent(**kwArg)

	def connect(self):
		return self.sendEvent(event.Event(id = U2A_CONNECT))

	def disconnect(self):
		return self.sendEvent(event.Event(id = U2A_DISCONNECT))

	def saveConfig(self, callback = None):
		return self.sendEvent(id = U2A_SAVE_CONFIG, object = callback)

	def loadConfig(self, callback = None):
		return self.sendEvent(id = U2A_LOAD_CONFIG, object = callback)

	def handle_message(self, event):
		eId = event.getId()
		robot = self.getRobot()
		# handler message
		if eId == U2A_CONNECT:
			print "[Debug] try to connect"
			self.getLooper().idle(True)
		elif eId == U2A_DISCONNECT:
			print "[Debug] try to disconnect"
			if robot.isConnected():
				robot.close()
		elif eId == U2A_LOAD_CONFIG:
			callback = event.getObject()
			result = robot.loadConfig()
			if result: 
				print "[Debug]AvatarHandler: loaded configure"
			if type(callback) is tuple and callable(callback[0]):
				args = list(callback[1:])
				args.append(result)
				apply(callback[0], args)
			elif callable(callback):
				callback(result)
			else:
				self.sendToUIThread(id = ui.A2U_LOAD_CONFIG_RESULT, object = result)
		elif eId == U2A_SAVE_CONFIG:
			callback = event.getObject()
			result = robot.saveConfig()
			if result:
				print "[Debug]AvatarHandler: saved configure"
			if type(callback) is tuple and callable(callback[0]):
				args = list(callback[1:])
				args.append(result)
				apply(callback[0], args)
			elif callable(callback):
				callback(result)
			else:
				self.sendToUIThread(id = ui.A2U_SAVE_CONFIG_RESULT, object = result)
		elif eId == U2A_RUN_IN_AVATAR_THREAD:
			callback = event.getObject()
			if type(callback) is tuple and callable(callback[0]):
				args = list(callback[:-1])
				apply(callback[0], args)
			elif callable(callback):
				callback()
			else:
				print "[Error]runInAvatarThread: callback function is None or not callable"
		else:
			print "[Error]AvatarHandler: unknown event id of %d" % (eId)
