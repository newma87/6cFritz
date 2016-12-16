#-*- encoding:utf-8 -*-
from smarttoy.thread import *
import application as app

A2U_CONNECT_STATE = 1
A2U_LOAD_CONFIG_RESULT = 2
A2U_SAVE_CONFIG_RESULT = 3

A2U_OPEN_SETUP_MOTOR = 4

A2U_RUN_IN_UI_THREAD = 0xff

class UIHandler(handler.Handler):
	"""
		Handler that communicate with ui thread
	"""
	def getWinManager(self):
		return app.Application().getMaster()

	def getWindow(self):
		return app.Application().getMainWidget()

	def handle_message(self, event):
		eId = event.getId()
		if eId == A2U_CONNECT_STATE:
			port = event.getObject()
			wm = self.getWinManager()
			win = self.getWindow()
			if port:
				wm.title("6cFirtz - connected to \"%s\"" % (port))
				win.onMotorConnected(port)
			else:
				wm.title("6cFirtz - disconnected")
				win.onMotorDisconnected()
		elif eId == A2U_LOAD_CONFIG_RESULT:
			result = event.getObject()
			win = self.getWindow()
			win.onConfigLoad(result)
		elif eId == A2U_SAVE_CONFIG_RESULT:
			self.getWindow().writeStatusBar("save fritz config succefully!")
		elif eId == A2U_OPEN_SETUP_MOTOR:
			self.getWindow().openSetupMotorWidget()
		elif eId == A2U_RUN_IN_UI_THREAD:
			callback = event.getObject()
			if type(callback) is tuple and callable(callback[0]):
				args = list(callback[:-1])
				apply(callback[0], args)
			elif callable(callback):
				callback()
			else:
				print "[Error]runInUIThread: callback function is None or not callable"

