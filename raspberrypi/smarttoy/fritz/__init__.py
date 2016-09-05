#-*- encoding:utf-8 -*-

"""
	Create by newma<newma@live.cn>
	Fritz robot
"""

__all__ = ["protocol"]

__author__ = "newma<newma@live.cn>"

from protocol import Protocol
from serial import Serial
import serial.tools.list_ports
from time import sleep


class FritzRobot(object):

	__SAVE_ORDER__ = ('leftEyebrow', 'rightEyebrow', 'leftLidPosition', 'rightLidPosition', 'leftHorizontalEye', 'rightHorizontalEye', 'leftVerticalEye', 
	'rightVerticalEye', 'neckTwist', 'neckTilt', 'leftLip', 'rightLip', 'jaw', 'sonar', 'ir')

	def __init__(self):
		self.state = { 
			"leftHorizontalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftVerticalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftEyebrow" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftLidPosition" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftLip" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightHorizontalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightVerticalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightEyebrow" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightLidPosition" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightLip" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"neckTilt" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"neckTwist" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"jaw" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"sonar" :  { "triggerPin": -1, "echoPin": -1, "enable": False},
			"ir" :  { "pin": -1, "enable": False }
		}
		self.serial = None
		self.protocol = Protocol()
		
	def close(self):
		if self.serial != None:
			self.serial.close()
			self.serial = None

	def isConnected(self):
		return self.serial != None

	def saveConfig(self):
		if not self.isConnected():
			print "Device is disconnection, please use findBoard to connect to device on serial port"
			return False

		shortArray = self.__serialConfig()
		try:
			self.serial.write(self.protocol.packShortArrayCommand(Protocol.ARDUINO_SAVE_CONFIG, shortArray))
			self.serial.flush()
			# read response
			byteArray = self.serial.read(3)
			command, _ = self.protocol.unpackResponseHead(byteArray)
			if command != Protocol.ARDUINO_SAVE_CONFIG :
				print "print save config response is not correct"
			return True
		except Exception as e:
			print "saveConfig raise Exception:" + str(e)
		return False

	def loadConfig(self):
		if not self.isConnected():
			print "Device is disconnection, please use findBoard to connect to device on serial port"
			return False

		try:
			byte2Read = self.serial.inWaiting()
			if byte2Read > 0:
				print "clear up pre dirty serial data"
				self.serial.read(byte2Read)
			self.serial.write(self.protocol.packCommand(Protocol.ARDUINO_LOAD_CONFIG, [85]))
			self.serial.flush()
			#read config
			sleep(0.5)		# wait for serial prepare
			byteArray = self.serial.read(3)
			command, count = self.protocol.unpackResponseHead(byteArray)
			print command, count
			if command != Protocol.ARDUINO_LOAD_CONFIG:
				print 'load config return an error command'
				byte2Read = self.serial.inWaiting()
				self.serial.read()
				return False

			byteArray = self.__readSerial(count)
			#self.__dumpRobotState()
			self.__unserialConfig(self.protocol.unpackByteArray2ShortArray(byteArray))
			print "after load config...................."
			#self.__dumpRobotState()
			return True
		except Exception as e:
			print "LoadConfig raise Exception:" + str(e)
		return False

	def reset(self):
		if not self.isConnected():
			print "Device is disconnection, please use findBoard to connect to device on serial port"
			return False

		try:
			self.serial.write(self.protocol.packCommand(Protocol.ARDUINO_RESET))
			self.serial.flush()
			return True
		except Exception as e:
			print "reset raise Exception:" + str(e)
		return False

	def findBoard(self):
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			s = None
			try:
				s = Serial(port = p.device, baudrate = 57600, timeout = 5, write_timeout = 1)
				#print "waiting read"
				byte2Read = s.inWaiting()
				if byte2Read > 0:
					print "clear input buffer when we need to response"
					s.read(byte2Read)
				print "checking port %s ..." % p.device
				s.write(self.protocol.packCommand(Protocol.ARDUINO_GET_ID))
				s.flush()
				sleep(0.5)
				buf = s.read(size = 7)
				if (buf != None) and (len(buf) == 7):
					pre, version = self.protocol.unpackVersion(buf)
					if pre == 'ARDU':
						if version < 4:
							print "The fritz firmwork is too old, we need at least version 4 and above"
						self.serial = s
						return p.device

				s.close()
			except Exception as e:
				print "findBoard raise Exception:" + str(e)
				if s != None and s.isOpen() :
					s.close()
				continue

		return None

	def __readSerial(self, byteLen):
		byteArray = []
		while (byteLen > 0):
			data = self.serial.read(byteLen)
			byteLen -= len(data)
			byteArray += data
		return byteArray

	def __setConfig(self, confName, trim, min, max, pin, enable):
		conf = self.state[confName]
		if trim != None:
			conf['trim'] = trim
		if min != None:
			conf['min'] = min
		if max != None:
			conf['max'] = max
		if pin != None:
			conf['pin'] = pin
		conf['enable'] = enable

	# return a short array in 85 length
	def __serialConfig(self):
		shortArray = [0] * 85
		i = 0
		for item in FritzRobot.__SAVE_ORDER__:
			conf = self.state[item]
			if item == "sonar":
				shortArray[77] = conf['triggerPin']
				shortArray[78] = conf['echoPin']
				if conf['enable']:
					shortArray[79] = 1
				else:
					shortArray[79] = 0
			else:
				if item == "ir":
					shortArray[83] = conf['pin']
					if conf['enable']:
						shortArray[84] = 1
					else:
						shortArray[84] = 0
				else:
					shortArray[i * 5] = conf['trim']
					shortArray[i * 5 + 1] = conf['max']
					shortArray[i * 5 + 2] = conf['min']
					shortArray[i * 5 + 3] = conf['pin']
					if conf['enable']:
						shortArray[i * 5 + 4] = 1	
					else:
						shortArray[i * 5 + 4] = 0
			i += 1
		return shortArray

	def __unserialConfig(self, shortArray):
		#print shortArray
		i = 0
		while (i < len(shortArray)):
			print shortArray[i], shortArray[i + 1], shortArray[i + 2], shortArray[i + 3], shortArray[i + 4]
			i += 5
		
		i = 0
		for item in FritzRobot.__SAVE_ORDER__:
			conf = self.state[item]
			if item == "sonar":
				conf['triggerPin'] = shortArray[77]
				conf['echoPin'] = shortArray[78]
				conf['enable'] = (shortArray[79] != 0)
			else:
				if item == "ir":
					conf['pin'] = shortArray[83]
					conf['enable'] = (shortArray[84] != 0)
				else:
					conf['trim'] = shortArray[i * 5]
					conf['max'] = shortArray[i * 5 + 1]
					conf['min'] = shortArray[i * 5 + 2]
					conf['pin'] = shortArray[i * 5 + 3]
					conf['enable'] = (shortArray[i * 5 + 4] != 0)
			i += 1

	def __dumpRobotState(self):
		print self.state

	def __pinDigitalWrite(self, pin, value):
		if not self.isConnected():
			print "Device is disconnection, please use findBoard to connect to device on serial port"
			return False

		buf = self.protocol.packShortPinValue(Protocol.ARDUINO_SET_SERVO, pin, value + 1500)
		try:
			print "write servo pin {%d} = value {%d}" % (pin, value)
			print buf
			self.serial.write(buf)
			self.serial.flush()
		except Exception as e:
			print "__pinDigitalWrite raise Exception:" + str(e)
			return False
		return True;

	def __moveServo(self, name, value):
		if not self.__isEnable(name) :
			print "%s is disable, move it failed!" % (name)
			return False
		value = value + self.__getTrim(name)
		if self.__getMax(name) < value:
			value = self.__getMax(name)
		if self.__getMin(name) > value:
			value = self.__getMin(name)

		return self.__pinDigitalWrite(self.__getPin(name), value)

	def __isEnable(self, name):
		return self.state[name]['enable']

	def __getPin(self, name):
		return self.state[name]['pin']

	def __getTrim(self, name):
		return self.state[name]['trim']

	def __getMin(self, name):
		return self.state[name]['min']

	def __getMax(self, name):
		return self.state[name]['max']

	def leftHorizontalEyeConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveLeftHorizontalEye(self, value):
		return self.__moveServo('leftHorizontalEye', value)

	def leftVerticalEyeConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveLeftVerticalEyeConfig(self, value):
		return self.__moveServo('leftVerticalEye', value)

	def leftEyeBrowConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveLeftEyeBrow(self, value):
		return self.__moveServo('leftEyebrow', value)

	def leftLidPositionConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveLeftLidPosition(self, value):
		return self.__moveServo('leftLidPosition', value)

	def leftLipConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveLeftLip(self, value):
		return self.__moveServo('leftLip', value)

	def rightHorizontalEyeConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveRightHorizontalEye(self, value):
		return self.__moveServo('rightHorizontalEye', value)

	def rightVerticalEyeConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveRightVerticalEye(self, value):
		return self.__moveServo('rightVerticalEye', value)

	def rightEyeBrowConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('leftHorizontalEye', trim, min, max, pin, enable)

	def moveRightEyeBow(self, value):
		return self.__moveServo('rightEyebrow', value)

	def rightLidPositionConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('rightLidPosition', trim, min, max, pin, enable)
	
	def moveRightLidPosition(self, value):
		return self.__moveServo('rightLidPosition', value)

	def rightLipConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('rightLip', trim, min, max, pin, enable)

	def moveRightLip(self, value):
		return self.__moveServo('rightLip', value)

	def neckTiltConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('neckTilt', trim, min, max, pin, enable)

	def moveNeckTilt(self, value):
		return self.__moveServo('neckTilt', value)

	def neckTwistConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('neckTwist', trim, min, max, pin, enable)

	def moveNeckTwist(self, value):
		return self.__moveServo('neckTwist', value)

	def jawConfig(self, trim = None, min = None, max = None, pin = None, enable = True):
		self.__setConfig('jaw', trim, min, max, pin, enable)

	def moveJaw(self, value):
		return self.__moveServo('jaw', value)

	def sonarConfig(self, triggerPin = None, echoPin = None, enable = False):
		if triggerPin != None:
			self.state['sonar']['triggerPin'] = triggerPin
		if echoPin != None:
			self.state['sonar']['echoPin'] = echoPin
		self.state['sonar']['enable'] = enable

	def getSonar(self):
		#TODO: newma
		pass

	def IRConfig(self, pin = None, enable = False):
		if pin != None:
			self.state['ir']['pin'] = pin
		self.state['ir']['enable'] = enable

	def getIR(self):
		#TODO: newma
		pass

if __name__ == "__main__":

	robot = FritzRobot()

	port = robot.findBoard()
	if port != None :
		print "found board on port %s" % (port)

	if robot.isConnected():
		robot.loadConfig()
		#robot.moveJaw(100)
	robot.close()

