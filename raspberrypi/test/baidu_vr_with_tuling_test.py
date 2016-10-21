# -*- coding: utf-8 -*- 
"""
    Created by newma<newma@live.cn>

    pydub depend on ffmpeg, so to run this test you need to install ffmpeg and pip install pydub

    fedora install ffmpeg: sudo yum install ffmpeg
    ubuntu install ffmpeg: sudo apt-get install ffmpeg
"""

from context import smarttoy

import os
from smarttoy.misc import tulingrobot as tr
from smarttoy.voicerecognize import baiduEngine as baidu
from smarttoy import audio
from smarttoy.audio import util

from array import array
from time import sleep
from pydub import AudioSegment

RATE = 8000
TTS_TEMPL_FILE = "baidu_tts.temp"

class MyRobot(audio.AudioRecordCallback):
    def __init__(self, name = "fritz"):
        audio.AudioRecordCallback.__init__(self)
        self.name = "fritz"
        self.__record_data = array('b')

    def onRecordData(self, in_data, bytesCount, frame_count, obj):
        self.__record_data = self.__record_data + array('b', in_data)

    def startOnce(self):
        config = util.AudioConfig(sampleRate = RATE, channel = 1, bytes = 2)
        record = audio.AudioRecorder(config, self)
        record.prepare()
        record.start()

        sleep(4)

        record.stop()
        record.terminate()

        engine = baidu.BaiduEngine()
        errNo, result = engine.recognizeRawVoice(self.__record_data.tostring(), 'pcm', RATE)
        if errNo != 0:
            print "Recognization Error: %s" % (result)
            return

        print "recognize result: ", result
        tlResult = tr.TulingRobot.getResponseForQuestion(result.decode('utf-8'))
        if tlResult == None or tlResult.getDescriptType() == "error":
            print "Tuling response error"
            return

        text = tlResult.getText()
        print "TTS result: ", text
        errNo, result = engine.getTTSMp3FromText(text.encode('utf-8'))
        if errNo != 0:
            print "TTS Error: %s" % (result)
            return

        #create mp3 file
        f = open(TTS_TEMPL_FILE, 'wb')
        f.write(result)
        f.flush()
        f.close()
        # covert to wave
        sound = AudioSegment.from_file(TTS_TEMPL_FILE, format = 'mp3')
        sound.export(TTS_TEMPL_FILE, format = 'wav')
        
        player = audio.AudioPlayer()
        player.syncPlayWave(TTS_TEMPL_FILE)

        os.remove(TTS_TEMPL_FILE)


def main():
    robot = MyRobot()
    robot.startOnce()

if __name__ == '__main__':
    main()
