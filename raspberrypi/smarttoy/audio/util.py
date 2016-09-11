#-*- encoding:utf-8 -*-
"""
	Created by newma<newma@live.cn>
"""

import pyaudio

class AudioConfig(object):

	CHANNEL_MONO = 1
	CHANNEL_STEREO = 2

	ENCODE_8BITS = 1
	ENCODE_16BITS = 2
	ENCODE_24BITS = 3
	ENCODE_32BITS = 4

	"""docstring for AudioConfig"""
	def __init__(self, sampleRate = 8000, channel = 1, bytes = 1):
		self.sampleRate = sampleRate
		self.channel = channel
		self.bytes = bytes

	def get_pa_format(self):
		if self.bytes == AudioConfig.ENCODE_8BITS:
			return pyaudio.paInt8
		elif self.bytes == AudioConfig.ENCODE_16BITS:
			return pyaudio.paInt16
		elif self.bytes == AudioConfig.ENCODE_24BITS:
			return pyaudio.paInt24
		elif self.bytes == AudioConfig.ENCODE_32BITS:
			return pyaudio.paInt32

	def get_pa_channel(self):
		if self.channel == AudioConfig.CHANNEL_MONO:
			return 1
		elif self.channel == AudioConfig.CHANNEL_STEREO:
			return 2

	def get_pa_rate(self):
		return self.sampleRate
