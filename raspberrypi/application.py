#-*- encoding:utf-8 -*-
import Tkinter as tk
import tkMessageBox
import threading
import os

from smarttoy.thread import *
from smarttoy.misc import storage as stg
from smarttoy.singleton import *

from avatar import Avatar
from avatarhandler import *
from uihandler import *
from ui import *
import mainwidget as mw

@singletonclass
class Application(object):
	"""
		Global singleton application, use Application() to create and get the application instance 
	"""
	UPDATE_RATE = int(1000 / 64) # update at 64fps

	CONFIG_FILE = '6cFritz-config.json'
	WIN_POS_X = 'win_x'
	WIN_POS_Y = 'win_y'

	def __init__(self):
		# create windows
		self.master = tk.Tk()
		self.master.geometry("720x640")
		self.master.title('6cFritz')
		curDir = os.path.dirname(os.path.abspath(__file__))
		img = tk.Image("photo", file=curDir + "/favor.png")
		self.master.tk.call('wm','iconphoto', self.master._w, img)
		self.master.resizable(width=False, height=False)
		self.master.protocol("WM_DELETE_WINDOW", self.onDestory)
		self.storage = stg.UserDefault(storage_file = self.CONFIG_FILE, storage_dir = '.')
		if self.storage.load():
			x = self.storage.getInt(self.WIN_POS_X, default = -1)
			y = self.storage.getInt(self.WIN_POS_Y, default = -1)
			if x == -1 or y == -1:
				center(self.master)
			else:
				moveWinPosition(self.master, x, y)
		else:
			center(self.master)

		# handler
		self.uiLooper = looper.Looper()
		self.uiHandler = UIHandler(self.uiLooper)
		#data
		self.avatar = Avatar()
		self.avatar.registConnectStateCallback(self.onAvatarConnectStateChange)
		self.avaHandler = AvatarHanlder(self.avatar)

		# create widget within windows
		self.mainWidget = mw.MainWidget(self.master)
		self.mainWidget.pack()

		self.avaHandler.connect()

	def getUserData(self):
		return self.storage

	def getUIHandler(self):
		return self.uiHandler

	def getAvatar(self):
		return self.avatar

	def getAvatarHandler(self):
		return self.avaHandler

	def mainloop(self):
		self.uiLooper.prepare()
		self.master.after(self.UPDATE_RATE, self.update)
		self.master.mainloop()

	def update(self):
		self.uiLooper.dispatchOneMessage()
		self.master.after(self.UPDATE_RATE, self.update)

	def timer(self, delay, callback):
		self.master.after(delay, callback)

	def getMainWidget(self):
		return self.mainWidget

	def getMaster(self):
		return self.master

	def runInUIThread(self, func, *args):
		if not callable(func):
			print "[Error]Application.runInUIThread: func argument must be callable"
		obj = (func, ) + args
		self.uiHandler.sendEvent(id = A2U_RUN_IN_UI_THREAD, object = obj)

	def runInAvatarThread(self, func, *args):
		if not callable(func):
			print "[Error]Application.runInUIThread: func argument must be callable"
		obj = (func, ) + args
		self.avaHandler.sendEvent(id = U2A_RUN_IN_AVATAR_THREAD, object = obj)

#event call back functions
	def onAvatarConnectStateChange(self, result, port):
		# jump to main thread
		eve = event.Event(id = A2U_CONNECT_STATE)
		if result:
			eve.setObject(port)
		self.uiHandler.sendEvent(eve)

		# load config from device
		if result:
			robot = self.avatar.getRobot()
			eve = event.Event(id = A2U_LOAD_CONFIG_RESULT)
			if not robot.loadConfig():
				print "[Error] load motor configure from device failed, using default value"
				eve.setObject(False)
			else:
				eve.setObject(True)
			self.uiHandler.sendEvent(eve)

	def onDestory(self):
		self.storage.setInt(self.WIN_POS_X, self.master.winfo_x())
		self.storage.setInt(self.WIN_POS_Y, self.master.winfo_y())
		self.storage.save()

		self.master.destroy()
		if self.avatar:
			self.avatar.release()
		destorySingleton(self)

def main(*args):
	app = Application()
	app.mainloop()

if __name__ == '__main__':
	main()
