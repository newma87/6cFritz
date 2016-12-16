from Tkinter import *
import tkMessageBox
from ui import *
#-*- encoding:utf-8 -*-
from setup import *
import application as app
import uihandler as uih
from paint import FritzPaint

class MainWidget(Frame):
	"""
		Main top window application widgets
	"""
	def __init__(self, master, **kargs):
		apply(Frame.__init__, (self, master), kargs) #init super class
		self.menu = self.create_menu()
		self.create_widgets()
		self.statusBar = StatusBar(self.master)
		self.statusBar.pack(side = BOTTOM, fill="x")

	def create_widgets(self):
		self.canv = Canvas(self, bg = "#220044", cursor = 'fleur', width = self.master.winfo_width(), height = self.master.winfo_height())
		self.canv.pack(side = TOP, fill = "both",  expand = 1)
		self.fritz = FritzPaint(self.canv)
		self.fritz.draw()

	def create_menu(self):
		menu = Menu(self)
		self.master.config(menu = menu)
		#file
		self.fileMenu = Menu(self, tearoff = 0)
		menu.add_cascade(label = "file", menu = self.fileMenu)
		self.fileMenu.add_command(label = "connect", command = self.connect)
		self.fileMenu.add_command(label = "disconnect", command = self.disconnect)
		self.__enable_menu(self.fileMenu, "connect")
		self.__enable_menu(self.fileMenu, "disconnect", False)
		#setup
		self.setupMenu = Menu(self, tearoff = 0)
		menu.add_cascade(label = "setup", menu = self.setupMenu)
		self.setupMenu.add_command(label = "setup motor", command = self.setupMotor)
		self.__enable_menu(self.setupMenu, "setup motor", False)
		#help
		self.helpMenu = Menu(self, tearoff = 0)
		menu.add_cascade(label = "help", menu = self.helpMenu)
		self.helpMenu.add_command(label = "about", command = self.about)
		return menu

	def writeStatusBar(self, format, *args):
		self.statusBar.set(format, *args)

	def clearStatusBar(self):
		self.statusBar.set('')

	def connect(self):
		app.Application().getAvatarHandler().connect()

	def disconnect(self):
		app.Application().getAvatarHandler().disconnect()

	def setupMotor(self):
		self.clearStatusBar()
		if app.Application().getAvatar().getRobot().isSync():
			self.openSetupMotorWidget()
		else:
			app.Application().getAvatarHandler().loadConfig(callback = 
				lambda result: result and app.Application().getUIHandler().sendEvent(id = uih.A2U_OPEN_SETUP_MOTOR))

	def openSetupMotorWidget(self):
		SetupDialog()

	def about(self):
		tkMessageBox.showinfo(
			"About",
			"fritz for 6cit"
        )

	def __enable_menu(self, menu, item, enable = True):
		if enable:
			menu.entryconfig(item, state = 'normal')
		else:
			menu.entryconfig(item, state = 'disabled')

	def onMotorConnected(self, port):
		if port is None:
			self.writeStatusBar("connect to fritz failed!")
		else:
			self.writeStatusBar("connect to fritz successfully!")
		self.__enable_menu(self.fileMenu, "connect", False)
		self.__enable_menu(self.fileMenu, "disconnect")

	def onMotorDisconnected(self):
		self.writeStatusBar("fritz disconnected!")
		self.__enable_menu(self.fileMenu, "connect")
		self.__enable_menu(self.fileMenu, "disconnect", False)

	def onConfigLoad(self, result):
		if result:
			self.writeStatusBar("load fritz configure successfully!")
			self.__enable_menu(self.setupMenu, "setup motor")
		else:
			self.writeStatusBar("load fritz configure failed!")
			