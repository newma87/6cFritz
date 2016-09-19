# -*- coding: utf-8 -*- 
"""
    Created by newma<newma@live.cn>

    pydub depend on ffmpeg, so to run this test you need to install ffmpeg and pip install pydub

    fedora install ffmpeg: sudo yum install ffmpeg
    ubuntu install ffmpeg: sudo apt-get install ffmpeg
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import requests
import time

from pydub import AudioSegment

from smarttoy import audio
from smarttoy.audio import util

class TTS_Player(audio.AudioPlayCallback):
    def __init__(self, sampelRate, channel, sampleWidth):
        self.player = audio.AudioPlayer(util.AudioConfig(sampelRate, channel, sampleWidth), self)

    def __del__(self):
        print "TTS_Player destory!"

    def onPlayEndCallback(self, obj):
        print "play music end"
        return True

    def playMusic(self, snd_data):
        self.player.prepare()
        self.player.start()
        self.player.play(snd_data)

    def stop(self):
        self.player.terminate()

#调用baidu语音api
def voice_baidu(file_name): 
    var = {
        "grant_type" : "client_credentials",
        "client_id" : "mTTHl4KD98XZrerYoQqAwU1x",
        "client_secret" : "41889b7a9c1b32e2b43786e031763f3c"
    }
    r = requests.post("https://openapi.baidu.com/oauth/2.0/token", data = var)
    access_token = json.loads(r.text).get("access_token")
    print "obain access token: ", access_token

    text = "本例程主要示范了如何使用百度的合成语音引擎，并且示范了如何使用语音库来播放合成后的mp3文件"

    body = {
        "tex" : text,
        "lan" : "zh",
        "ctp" : 1,
        "tok" : access_token,
        "cuid" : "f0:de:f1:b1:f6:3a",
        "vol" : 9,
        "per" : 0,
    }
    print "request audio file..."
    r = requests.post("http://tsn.baidu.com/text2audio", data = body)
    #打开WAV文档
    f = open(file_name, "wb")
    f.write(r.content)
    f.close()
    print "write to file done!"


TTS_NAME = "baidu_tts"

if __name__ == '__main__':
    voice_baidu(TTS_NAME)
    sound = AudioSegment.from_file(TTS_NAME, format = 'mp3')
    file = sound.export(TTS_NAME, format = 'wav')
    sound = AudioSegment.from_file(file, format = 'wav')
    print sound.sample_width, sound.frame_rate, sound.channels  

    # sync play
    config = util.AudioConfig(sound.frame_rate, sound.channels, sound.sample_width)
    player = audio.AudioPlayer(config)
    player.syncPlay(sound.raw_data)

    #async play (not stable)
    #player = TTS_Player(sound.frame_rate, sound.channels, sound.sample_width)
    #player.playMusic(sound.raw_data)
    #time.sleep(20)

    #remove temp file
    os.remove(TTS_NAME)
