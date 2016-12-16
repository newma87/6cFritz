#-*- encoding:utf-8 -*-
from Tkinter import *

class FritzPaint(object):
	"""
		Paint fritz face, each component is range from -1 to 1 (0 is middle)
	"""
	def __init__(self, canvas):
		self.canv = canvas
		self.state = {
			"leftLidPosition": {
				'value': 1,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"rightLidPosition": {
				'value': 1,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"leftEyebrow": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"rightEyebrow": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"leftVerticalEye": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"leftHorizontalEye": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"rightVerticalEye": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"rightHorizontalEye": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},	
			"jaw": {
				'value': 1,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			}
		}

		self._drag_item = None
		self.canv.bind("<Button-1>", self.OnDragButtonPress)
		self.canv.bind("<B1-Motion>", self.OnDragMotion)
		self.canv.bind("<ButtonRelease-1>", self.OnDragButtonRelease)

 	def OnDragButtonPress(self, event):
		self._drag_item = self.canv.find_closest(event.x, event.y)[0]

	def OnDragButtonRelease(self, event):
		self._drag_item = None

	def OnDragMotion(self, event):
		pass


	def clear(self):
		w = self.canv.winfo_width()
		h = self.canv.winfo_height()
		self.canv.create_rectangle(0, 0, w, h, outline = self.canv["background"], fill = self.canv["background"])

	def draw(self):
		coord = 0, 0, 240, 210
		arc = self.canv.create_arc(coord, start= 0, extent= 150, fill="red")
		coord = 20, 20, 240, 210
		arc = self.canv.create_arc(coord, start= 0, extent= 150, fill="red")

	def drawLeftEyeBrow(self):
		pass

	def drawRightEyeBrow(self):
		pass

	def drawLeftEyeLid(self):
		pass

	def drawRightEyeLid(self):
		pass

	def drawJaw(self):
		pass

	def drawLeftEyes(self):
		pass

	def drawRightEyes(self):
		pass

