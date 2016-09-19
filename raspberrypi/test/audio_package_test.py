#-*- encoding:utf-8 -*-

"""
	Created by newma<newma@live.cn>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from smarttoy import audio
from smarttoy.audio import util
from time import sleep
from array import array

import wave

CHANNELS = 1
WIDTH = 2
RATE = 44100

class MyRecordTest(audio.AudioRecordCallback):
	def __init__(self):
		self.record = None
		self.wf = None
		self.data = b''		# self.data is a string

	def onRecordData(self, in_data, bytesCount, frame_count, obj):
		#data = array('h', [1648 for i in xrange(int(bytesCount))]).tostring()
		self.wf.writeframes(in_data)

	def test(self, filePath):
		self.wf = wave.open(filePath, "wb")
		self.wf.setnchannels(CHANNELS)
		self.wf.setsampwidth(WIDTH)
		self.wf.setframerate(RATE)

		config = util.AudioConfig(sampleRate = RATE, channel = CHANNELS, bytes = WIDTH)
		self.record = audio.AudioRecorder(config, self)
		self.record.prepare()
		self.record.start()

		sleep(4)

		#while self.record.isRecording():
		#	sleep(0.1)

		self.record.stop()
		self.record.terminate()		

		self.wf.close()

class MyPlayTest(audio.AudioPlayCallback):

	def __init__(self, filePath):
		wf = wave.open(filePath, "rb")
		self.play_data = wf.readframes(wf.getnframes())
		config = util.AudioConfig(sampleRate = wf.getframerate(), channel = wf.getnchannels(), bytes = wf.getsampwidth())
		wf.close()

		self.play = audio.AudioPlayer(config, self)
		self.count = 0

	def onPlayEndCallback(self, obj):
		if self.count >= 1:
			os.remove(temp_audio_file) # delete audio file
			return True     # import: if this is not return True, then the play wan't be stopped
		else:
			print "play end, replay once more!"
			self.play.play(self.play_data)
			self.count += 1
		return False

	def testAsync(self):
		self.count = 0

		self.play.prepare()
		self.play.start()
		self.play.play(self.play_data)

		while self.play.isPlaying():
			sleep(0.1)
		
		self.play.stop()
		self.play.terminate()

	def testSync(self):
		self.play.syncPlay(self.play_data)

temp_audio_file = 'abc.wav'

if __name__ == '__main__':
	#print "record to file abc.wav"
	test = MyRecordTest()
	test.test(temp_audio_file)

	test1 = MyPlayTest(temp_audio_file)
	print "async play %s file" % (temp_audio_file)
	#test1.testAsync()
	test1.testSync()
	os.remove(temp_audio_file)
