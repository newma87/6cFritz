#-*- encoding:utf-8 -*-

"""
	Create by newma<newma@live.cn>

	The fritz original protocol

	When command ^ 128 < 32, the struct of protocol command package:
	___________________________________________
   | command(>=128 & < 160) | data length | data | crc |
	___________________________________________

	When command ^ 128 >= 32, the struct of protocol command package:
	_____________________________________________________________________________________________________
   | command(>= 160) | data length low bits (0 - 7 bit) | data length high bits (0 - 7 bit) | data | crc |
    _____________________________________________________________________________________________________
"""

class Protocol (object):
	#short command
	ARDUINO_GET_ID = 0
	ARDUINO_RESET = 1
	ARDUINO_SET_OBJECT = 2
	ARDUINO_SET_SERVO = 3
	ARDUINO_HEARTBEAT = 4
	ARDUINO_RELEASE_SERVO = 5
	ARDUINO_GET_IR = 6
	ARDUINO_GET_SONAR = 7

	#long command
	ARDUINO_LOAD_CONFIG = 32
	ARDUINO_SAVE_CONFIG = 33
	ARDUINO_SAVE_SEQUENCE = 34

	def __init__(self):
		pass

	# byteArray must an  byte array, in this function, each item will be treated as a char
	def packCommand(self, command, byteArray = []):
		if command >= 128:
			print "[error]Protocol packCommand: command must less than 128"
			return None
		buf = [chr(command | 128)]
		dLen = len(byteArray)
		# add length
		if command >= 32:
			buf.append(chr(dLen  & 127))
			buf.append(chr((dLen >> 7) & 127))
		else:
			buf.append(chr(dLen & 127)) # 0 - 7 validate bit
		#add data
		if dLen > 0:
			for byte in byteArray:
				buf.append(chr(byte))
			#add crc
			crc = 0
			for i in buf:
				crc ^= ord(i)
			buf.append(chr(crc))
		return buf

	def packShortPinValue(self, command, pin, val):
		return self.packCommand(command, [(pin & 127), (val & 127), ((val >> 7) & 127)])

	def packIntPinValue(self, command, pin, val):
		return self.packCommand(command, [(pin & 127), (val & 127), ((val >> 7) & 127), ((val >> 14) & 127), ((val >> 21) & 127), ((val >> 28) & 127)])

	def packBytePinValue(self, command, pin, val):
		return self.packCommand(command, [(pin & 127), (val & 127)])

	def packShortArrayCommand(self, command, shortArray = []):
		byteArray = []
		for s in shortArray:
			byteArray.append(s & 127)
			byteArray.append((s >> 7) & 127)

		return self.packCommand(command, byteArray)

	# return version_prefix, version_code
	def unpackVersion(self, byteArray):
		return str(byteArray[ : -3]), int(byteArray[-3 : ])

	def unpackByteArray2ShortArray(self, byteArray):
		length = len(byteArray)
		shortArray = []
		i = 0
		while (i < length):
			# If byte array is odd, then abandon the last element
			if length - i == 1:
				print "[warn]Protocol unpackByteArray2ShortArray: argument byteArray is odd, ignore last element 0x%x" % (ord(byteArray[-1]))
				break;
			num = (ord(byteArray[i]) & 127) | ((ord(byteArray[i + 1]) & 127) << 7)
			# Because we lost two highest bits when saving it to arduino, so we assume number that larger than 8192 is a negative number! So we need to correct it by substracting 16384
			if num > 8192:
				num -= 16384
			shortArray.append(num)
			i += 2
		return shortArray

	def unpackResponseHead(self, byteArray):
		command = ord(byteArray[0]) & 127
		if command >= 32:
			count = ((ord(byteArray[1]) & 127) | ((ord(byteArray[2]) & 127) << 7))
		else:
			count = ord(byteArray[1]) & 127
		return command, count