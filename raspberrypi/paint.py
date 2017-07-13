#-*- encoding:utf-8 -*-
from Tkinter import *

class FritzPaint(Canvas):
	"""
		Paint fritz face, each component is range from -1 to 1 (0 is middle)
	"""
	RES_WIDTH = 356
	RES_HEIGHT = 378

	def __init__(self, master, **kwarg):
		Canvas.__init__(self, master, **kwarg)

		self.height = kwarg.get('height')
		self.width = kwarg.get('width')
		if self.width is None or self.height is None:
			self.width = FritzPaint.RES_WIDTH
			self.height = FritzPaint.RES_HEIGHT
			self.config(width = self.width, height = self.height)

		self.scaleX = float(self.width) / FritzPaint.RES_WIDTH
		self.scaleY = float(self.height) / FritzPaint.RES_HEIGHT

		self.state = {
			"leftLidPosition": {
				'value': 1,			# component current value(range from -1 to 1)
				'cord': [0,0,0,0],  # component aabb box
				'item': [],			# canvas item ids that make up component
				'normal': 20,		# this means value 1 is about 20p and -1 is -20p
				'selected': False	# whether this component been selected
			},
			"rightLidPosition": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},
			"leftEyebrow": {
				'value': 0,
				'cord': [0,0,0,0],
				'moveRage':20,
				'selected': False
			},
			"rightEyebrow": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},
			"leftVerticalEye": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},
			"leftHorizontalEye": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},
			"rightVerticalEye": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},
			"rightHorizontalEye": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			},	
			"jaw": {
				'value': 1,
				'cord': [0,0,0,0],
				'item': [],
				'normal': 20,
				'selected': False
			}
		}

	def draw(self):	
		self.drawBackground()
		self.scale('all', 0, 0, self.scaleX, self.scaleY)

	def drawBackground(self):
		#draw head outline
		headOutline = (31, 203, 36, 209, 44, 221, 47, 226, 53, 236, 55, 242, 59, 251, 69, 277, 71, 287, 73, 292, 75, 303, 75, 309, 76, 335, 81, 338, 88, 340, 104, 347, 104, 310, 250, 310, 250, 346, 260, 343, 269, 340, 280, 335, 280, 312, 282, 296, 283, 291, 285, 283, 287, 276, 294, 255, 306, 231, 310, 224, 312, 219, 325, 201, 325, 50, 321, 41, 316, 34, 309, 28, 301, 22, 293, 19, 63, 19, 56, 21, 49, 25, 44, 29, 34, 41, 31, 48, 31, 203)
		self.create_polygon(headOutline, outline = 'gray', fill = '#ffff96', tag = 'background')

		midX = FritzPaint.RES_WIDTH >> 1
		midY = FritzPaint.RES_HEIGHT >> 1
		#draw eyes
		eyeR = int(midX * 0.24)
		eyeX = int(midX - midX * 0.40)
		eyeY = int(midY - midY * 0.37)
		#draw left eye
		self.create_oval(eyeX - eyeR, eyeY - eyeR, eyeX + eyeR, eyeY + eyeR, fill = "white", outline = 'gray', tag = 'background')
		eyeX = int(midX + midX * 0.40)
		#draw right eye
		self.create_oval(eyeX - eyeR, eyeY - eyeR, eyeX + eyeR, eyeY + eyeR, fill = "white", outline = 'gray', tag = 'background')
		#draw noise
		noiseXPixel = int(midX * 0.02)
		noiseYPixel = int(midY * 0.25)
		self.create_rectangle(midX - noiseXPixel, midY - noiseYPixel, midX + noiseXPixel, midY + noiseYPixel, fill = '#B9A073', outline = 'gray', tag = 'background')

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

