# -*- encoding:utf-8 -*-

"""
	Created by newma

	AudioRecorder usage:
	-----------------------------------------------------------------------------
		class RecordCallback(audio.AudioRecordCallback):
			def __init__(self):
				pass
			def onRecordData(self, in_data, bytesCount, frame_count, obj):
				# write record data to file
				wavFile.writeframes(in_data)

		config = audio.util.AudioConfig(sample_rate, chennel, smaple_width)
		recorder = audio.AudioRecorder(config, RecordCallback())
		recorder.prepare()
		recorder.start()
		time.sleep(RECORD_SECONDS)
		recorder.stop()
		recorder.terminate()
	------------------------------------------------------------------------------

	AudioPlayer usage:
	1, sync play
	------------------------------------------------------------------------------
		config = audio.util.AudioConfig(sample_rate, chennel, smaple_width)
		player = audio.AudioPlayer(config)
		player.syncPlay(wavFile.readframes(wavFile.getnframes())) # or player.syncPlay(sound_pcm_data)
	------------------------------------------------------------------------------
	
	2, async play (Importance: Note that this operation is not stable, the play quality is not guarantee !!!)
	------------------------------------------------------------------------------
		class PlayCallback(audio.AudioPlayCallback):
			def __init__(self):
				pass

			# Please keep it in your mind, this method is called in another thread !!!
			# So don't call the AudioPlayer.terminate or AudioPlayer.stop to stop it, or it will fire exception
			# If return False, the play will play again and also call this callback again when play end.
			def onRecordData(self, in_data, bytesCount, frame_count, obj):
				print "play end"
				return True			

		config = audio.util.AudioConfig(sample_rate, chennel, smaple_width)
		player = audio.AudioPlayer(config, PlayCallback())
		player.prepare()
		player.start()
		while player.isPlaying():
			# do something others
			time.sleep(0.1)
		player.stop()
		player.terminate()
	------------------------------------------------------------------------------
"""	

import util
from smarttoy.singleton import singletonclass
import pyaudio

from array import array
import wave

__all__ = ["callback", "util"]

__author__ = ["newma<newma@live.cn>"]

from callback import AudioRecordCallback, AudioPlayCallback
from util import checkInputAudioConfigIsSupported

class BaseAudio(object):
	"""docstring for BaseAudio"""
	def __init__(self, audioConfig = None):
		if audioConfig != None:
			checkInputAudioConfigIsSupported(audioConfig)
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
		if self.config != None:
			checkInputAudioConfigIsSupported(self.config)
			if self.config.get_pa_format() == pyaudio.paInt8:
				print "[warn]Current is not stable in recording 8bits per sample. Recommand using 16bits per sample instead!"

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
	__WRITE_FRAMES__  = 1024

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

	def syncPlayWave(self, waveFile):
		wf = wave.open(waveFile, "rb")
		data = wf.readframes(wf.getnframes())
		config = util.AudioConfig(sampleRate = wf.getframerate(), channel = wf.getnchannels(), bytes = wf.getsampwidth())
		self.setAudioConfig(config)
		wf.close()
		self.syncPlay(data)

	def syncPlay(self, dnf_data):
		if self.audio != None:
			if self.isPlaying():
				print "[error]AudioPlayer.syncPlay: async play is starting, please stop it first and try again!"
				return False
			else:
				print "[warin]AudioPlayer.syncPlay: async play is prepared but not play, it will be terminate!"
				self.terminate()

		# calculate read bytes size each time
		bytesSize = self.__WRITE_FRAMES__ * self.config.channel * self.config.bytes

		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(format = self.config.get_pa_format(),
                channels = self.config.get_pa_channel(),
                rate = self.config.get_pa_rate(),
                output = True,
                frames_per_buffer = bytesSize)
		while len(dnf_data) >= bytesSize :
			data = dnf_data[: bytesSize]
			dnf_data = dnf_data[bytesSize :]
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
				if self.__callback.onPlayEndCallback(self): # if callback return True then complete this playing
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
