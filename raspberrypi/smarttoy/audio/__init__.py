# -*- encoding:utf-8 -*-

"""
	Created by newma
"""

import util
from abc import ABCMeta, abstractmethod
from smarttoy.singleton import singletonclass
import pyaudio

from array import array

__all__ = ["util"]

__author__ = ["newma<newma@live.cn>"]

class AudioRecordCallback(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def onRecordData(self, in_data, bytesCount, frame_count, obj):
		pass

class AudioPlayCallback(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def onPlayEndCallback(self, bytesCount, frame_count, obj):
		pass

class BaseAudio(object):
	"""docstring for BaseAudio"""
	def __init__(self, audioConfig = None):
		if audioConfig.get_pa_format() == pyaudio.paInt8:
			print "[warn]Current is not stable in recording 8bits per sample. Recommand using 16bits per sample instead!"
		self.config = audioConfig
		self.audio = None
		self.stream = None
		self.input = True
		self.output = True

	def prepare(self):
		self.audio = pyaudio.PyAudio()
		def pyaudio_callback(in_data, frame_count, time_info, status):
			return self.onDataCallback(in_data, frame_count)
		self.stream = self.audio.open(format = self.config.get_pa_format(),
                channels = self.config.get_pa_channel(),
                rate = self.config.get_pa_rate(),
                input = self.input,
                output = self.output,
                stream_callback = pyaudio_callback)
		#print "prepare: rate - %d, channels - %d, bits - %d" % (self.config.get_pa_rate(), self.config.get_pa_channel(), self.config.get_pa_format())

	def getAudioConfig(self):
		return self.config

	def setAudioConfig(self, audioConfig):
		self.config = audioConfig		

	def terminate(self):
		if self.stream != None :
			self.stream.stop_stream()
			self.stream.close()
		if self.audio != None:
			self.audio.terminate()
			self.audio = None

	"""callback when the pyAudio record data or need data to play"""
	def onDataCallback(self, snd_data, frame_count):
		return snd_data

@singletonclass
class AudioRecorder(BaseAudio):
	"""docstring for AudioRecorder"""
	def __init__(self, audioConfig = None, callback = None):
		BaseAudio.__init__(self, audioConfig)
		self.input = True
		self.output = False
		self.__callback = None
		if callback != None:
			self.setCallback(callback)

	def setCallback(self, callback):		
		if not isinstance(callback, AudioRecordCallback):
			print "[error]AudioRecorder: ctor argument callback must be a type of AudioRecordCallback"
		else:
			self.__callback = callback

	def getCallback(self):
		return self.__callback

	def start(self):
		if self.stream == None:
			print "[error]AudioRecorder.start: pyAudio object is None! Did you forget to call prepare before call this method?"
			return False
		self.stream.start_stream()

	def stop(self):
		self.stream.stop_stream()

	def isRecording(self):
		return self.stream.is_active()	

	def onDataCallback(self, snd_data, frame_count):
		bytesSize = self.audio.get_sample_size(self.config.get_pa_format())
		bytesSize =  bytesSize * frame_count * self.config.channel
		
		if self.__callback:
			self.__callback.onRecordData(snd_data, bytesSize, frame_count, self)
		return None, pyaudio.paContinue

@singletonclass
class AudioPlayer(BaseAudio):
	__WRITE_CHUNK__  = 1024

	"""docstring for AudioPlayer"""
	def __init__(self, audioConfig = None, callback = None):
		BaseAudio.__init__(self, audioConfig)
		self.input = False
		self.output = True
		self.__callback = None
		if callback != None:
			self.setCallback(callback)
		self.__data = None
		self.__playStarted = False

	def setCallback(self, callback):		
		if not isinstance(callback, AudioPlayCallback):
			print "[error]AudioPlayer: ctor argument callback must be a type of AudioPlayCallback"
		else:
			self.__callback = callback

	def getCallback(self):
		return self.__callback

	def syncPlay(self, dnf_data):
		if self.audio != None:
			if self.isPlaying():
				print "[error]AudioPlayer.syncPlay: async play is starting, please stop it first and try again!"
				return False
			else:
				print "[warin]AudioPlayer.syncPlay: async play is prepared but not play, it will be terminate!"
				self.terminate()

		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(format = self.config.get_pa_format(),
                channels = self.config.get_pa_channel(),
                rate = self.config.get_pa_rate(),
                output = True,
                frames_per_buffer = AudioPlayer.__WRITE_CHUNK__)
		while len(dnf_data) >= AudioPlayer.__WRITE_CHUNK__ :
			data = dnf_data[: AudioPlayer.__WRITE_CHUNK__]
			dnf_data = dnf_data[AudioPlayer.__WRITE_CHUNK__ :]
			self.stream.write(data)

		if len(dnf_data) > 0:
			self.stream.write(dnf_data)

		self.stream.stop_stream()
		self.stream.close()
		self.stream = None
		self.audio.terminate()
		self.audio = None
		return True

	def start(self):
		if self.stream == None:
			print "[error]AudioPlayer.play: pyAudio object is None! Did you forget to call prepare before call this method?"
			return False
		self.stream.start_stream()

	def play(self, dnf_data):
		self.__data = dnf_data
		self.__playStarted = True

	def stop(self):
		self.stream.stop_stream()

	def isPlaying(self):
		return self.stream.is_active()

	def onDataCallback(self, snd_data, frame_count):
		bytesSize = self.audio.get_sample_size(self.config.get_pa_format())
		bytesSize =  bytesSize * frame_count * self.config.channel

		status = pyaudio.paContinue

		# if play end then call callback
		if self.__data == None and self.__playStarted:
			self.__playStarted = False
			if self.__callback != None:
				if self.__callback.onPlayEndCallback(self, bytesSize, frame_count): # if callback return True then complete this playing
					return None, pyaudio.paComplete
		# if play is not complete, check self.__data, if it is empty then create mute data else play it's data
		retData = None
		if self.__data == None:
			print '[warn]Playing mute data ...'
			retData = array('b', [0 for i in xrange(int(bytesSize))]).tostring()
		else :
			length = len(self.__data)
			if length > 0:
				if length > bytesSize:
					retData = self.__data[: bytesSize]
					self.__data = self.__data[bytesSize :]
				else:
					retData = self.__data + array('b', [0 for i in xrange(int(bytesSize - length))]).tostring()
					self.__data = None
		return retData, status
