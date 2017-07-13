#-*- encoding:utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
import types

from smarttoy.fritz import CONFIG_SAVE_ORDER

from ui import *
import application as app
import avatarhandler as av

MIN_MOTOR_RANGE = -1000
MAX_MOTOR_RANGE = 1000

LIST_PIN = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5')

def findPin(strPin):
	index = -1
	for key in LIST_PIN:
		index = index + 1
		if key == strPin:
			break
	return index

class ComponentWidget(Frame):
	"""
		Component for single motor test
	"""
	SPINBOX_WIDTH = 5
	def __init__(self, master, name, kwData, onChangeCallback, onClickCallback):
		Frame.__init__(self, master)
		if type(kwData) is types.DictType :
			self.data = self.__translate(kwData)
		else:
			self.data = kwData
		self.name = name
		self.onChangeCallback = onChangeCallback
		self.onClickCallback = onClickCallback

		self.create_widgets()

	def getName(self):
		return self.name

	def getValue(self, key):
		var = self.data[key]
		if key == 'enable':
			return not (var.get() == 0)
		return var.get()

	def onValidateValueChange(self, *args):
		try:
			trim = self.data['trim'].get()
			if trim != '':
				if trim > MAX_MOTOR_RANGE:
					self.data['trim'].set(MAX_MOTOR_RANGE)
					return
				elif trim < MIN_MOTOR_RANGE:
					self.data['trim'].set(MIN_MOTOR_RANGE)
					return

			min_ = self.data['min'].get()
			if min_ != '':
				if min_ > MAX_MOTOR_RANGE:
					self.data['min'].set(MAX_MOTOR_RANGE)
					return
				elif min_ < MIN_MOTOR_RANGE:
					self.data['min'].set(MIN_MOTOR_RANGE)
					return

			max_ = self.data['max'].get()
			if max_ != '':
				if max_ > MAX_MOTOR_RANGE:
					self.data['max'].set(MAX_MOTOR_RANGE)
					return
				elif max_ < MIN_MOTOR_RANGE:
					self.data['max'].set(MIN_MOTOR_RANGE)
					return
		except ValueError:
			return
		#self.onValueChange(*args)

	def onValueChange(self, *args):
		if self.data['enable'].get() == 0:
			self.__enable(False)
		else:
			self.__enable()

		if self.onChangeCallback and callable(self.onChangeCallback):
			self.onChangeCallback(self)

	def __enable(self, enable = True):
		if enable:
			self.combo.config(state = 'normal')
			self.trim.config(state = 'normal')
			self.min.config(state = 'normal')
			self.max.config(state = 'normal')
			self.btn.config(state = 'normal')
		else:
			self.combo.config(state = 'disabled')
			self.trim.config(state = 'disabled')
			self.min.config(state = 'disabled')
			self.max.config(state = 'disabled')
			self.btn.config(state = 'disabled')

	def __registVarListen(self):
		for key, var in self.data.iteritems():
			if key == 'trim' or key == 'min' or key == 'max':
				var.trace("w", self.onValidateValueChange)
			else:
				var.trace("w", self.onValueChange)

	def create_label(self, label, min, max, var):
		f = Frame(self)
		lab = Label(f, text = label)
		lab.pack(side = LEFT)
		validate_func = (app.Application().getMaster().register(self.validateInput), label[:-1], '%V', '%P', '%S', '%i') # arguments order: Widget, validate type, text after validate accept, insert or delete key, beginning index of insert or delete text
		val = Spinbox(f, width = ComponentWidget.SPINBOX_WIDTH, from_ = min, to = max, textvariable = var, validate='all', validatecommand = validate_func)
		val.pack(side = LEFT)
		return f, lab, val

	def create_widgets(self):
		self.grid_columnconfigure(0, minsize = 140)
		chk = Checkbutton(self, text = self.name, variable = self.data["enable"])
		chk.grid(row = 0, column = 0, sticky = W)

		f = Frame(self)
		lab = Label(f, text = "pin:")
		lab.pack(side = LEFT)
		self.combo = ttk.Combobox(f, width = 3, textvariable = self.data["pin"])
		self.combo['values'] = LIST_PIN
		self.combo.pack(side = LEFT)
		f.grid(row = 0, column = 1, sticky = E)

		f, _, self.trim = self.create_label("trim:", MIN_MOTOR_RANGE, MAX_MOTOR_RANGE, self.data["trim"])
		f.grid(row = 0, column = 2, sticky = E)
		f, _, self.min = self.create_label("min:", MIN_MOTOR_RANGE, MAX_MOTOR_RANGE, self.data["min"])
		f.grid(row = 0, column = 3, sticky = E)
		f, _, self.max = self.create_label("max:", MIN_MOTOR_RANGE, MAX_MOTOR_RANGE, self.data["max"])
		f.grid(row = 0, column = 4, sticky = E)

		self.btn = Button(self, text = "check", command = self.onButtonClick)
		self.btn.grid(row = 0, column = 5, sticky = E)
		if self.data["enable"].get() == 0:
			self.__enable(False)
		else:
			self.__enable()

		self.__registVarListen()

	def onButtonClick(self):
		if self.onClickCallback and callable(self.onClickCallback):
			self.onClickCallback(self)

	def __translate(self, kwVal):
		kwVar = {}
		for key, val in kwVal.iteritems():
			var = None
			if type(val) is types.StringType:
				var = StringVar(value = val)
			elif key == "pin":
				if (val == -1):
					var = StringVar(value = LIST_PIN[0])
				else:
					var = StringVar(value = LIST_PIN[val])
			elif type(val) is types.IntType:
				var = IntVar(value = val)
			elif type(val) is types.BooleanType:
				if val:
					var = IntVar(value = 1)
				else:
					var = IntVar(value = 0)
			kwVar[key] = var
		return kwVar

	def copyRawData(self, kwTarget = {}):
		for key, var in self.data.iteritems():
			try:
				if key == "enable":		# for bool value 
					if var.get() == 0:
						kwTarget[key] = False
					else:
						kwTarget[key] = True
				elif key == "pin":
					kwTarget[key] = findPin(var.get())
				else:
					kwTarget[key] = var.get()
			except ValueError:
				continue
		return kwTarget

	def validateInput(self, widget, type_, text, key, index):
		#print widget, " type:", type_, " text:", text, " key:", key, " index:", index
		if type_ == "key":
			if key != '' and not key.isdigit() and not(key == '-' and index == '0'):
				app.Application().getMaster().bell()
				return False
		elif type_ == "focusout":
			if self.onChangeCallback and callable(self.onChangeCallback):
				self.onChangeCallback(self, widget)
		return True

class SetupDialog(Dialog):
	def __init__(self):
		self.robot = app.Application().getAvatar().getRobot()
		self.handler = app.Application().getAvatarHandler()
		Dialog.__init__(self, app.Application().getMaster(), title = "setup motor")
		app.Application().timer(1000, self.onTimer)

	def body(self, master):
		state = self.robot.getState()
		row = 0
		col = 0
		init_comp = None
		for key in CONFIG_SAVE_ORDER:
			if key is None or key == "ir" or key == "sonar":
				continue
			comp = ComponentWidget(master, key, state[key], self.onComponentValueChange, self.onComponentTest)
			comp.grid(row = row, column = col, sticky = W)
			if row == 0 and col == 0:
				init_comp = comp
			col += 1
			if col > 1:
				row += 1
				col = 0
		return init_comp
	
	def onTimer(self):
		#TODO: it is time to save and move
		app.Application().timer(1000, self.onTimer)
		pass	

	def apply(self):
		#save config
		if not self.robot.isSync():
			self.handler.saveConfig()

	#override cancel
	def cancel(self, event=None):
		Dialog.cancel(self, event)

	def onComponentValueChange(self, component = None, widget = None):
		#refresh robot state
		name = component.getName()
		self.robot.setConfig(name, config = component.copyRawData())
		#save config'
		if widget == 'trim'or widget == 'min' or widget == 'max':
			self.handler.saveConfig(callback = (self.onSaveConfig, component, widget))

	def onSaveConfig(self, component, key, result):
		if result:
			if (key == 'trim'):
				self.robot.moveServo(component.getName(), component.getValue(key) + component.getValue('min'))
			else:
				self.robot.moveServo(component.getName(), component.getValue(key))

	def onComponentTest(self, component):
		pass

