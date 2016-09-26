#-*- encoding:utf-8 -*-
"""
	Created by newma<newma@live.cn>
"""

import urllib
import httplib
import json
from json import JSONEncoder
import base64
import wave

class BaiduEngine(object):

	ACCESS_TOKEN = None

	__APP_KEY__ = "mTTHl4KD98XZrerYoQqAwU1x"
	__SECRET_KEY__ = "41889b7a9c1b32e2b43786e031763f3c"

	__SERVER_ADDR__ = "openapi.baidu.com"

	def __init__(self):
		pass

	@staticmethod
	def getBaiduAccessToken():
		"""
			Get baidu voice recognization api access token
			Note: baidu access token can be requested by post only 
		"""
		if BaiduEngine.ACCESS_TOKEN == None:
			conn = None
			try:
				conn = httplib.HTTPSConnection(BaiduEngine.__SERVER_ADDR__)
				params= {
        			"grant_type" : "client_credentials",
        			"client_id" : BaiduEngine.__APP_KEY__,
        			"client_secret" : BaiduEngine.__SECRET_KEY__
    			}

				body = urllib.urlencode(params)
				header = {"Content-type": "application/x-www-form-urlencoded"}

				conn.request("POST", "/oauth/2.0/token", body, header)
				resp = conn.getresponse()
				if resp.status == 200:
					BaiduEngine.ACCESS_TOKEN = json.loads(resp.read()).get('access_token')
				else:
					print "[error]getBaiduAccessToken: request access token, get error response: ", resp.read()
			except Exception as e:
				print "[error]getBaiduAccessToken: ", e.toString()
			finally:
				if conn != None:
					conn.close()

		return BaiduEngine.ACCESS_TOKEN

	def recognizeWaveAudio(self, waveFile, cuid = "0001"):
		wf = wave.open(waveFile, "rb")
		return self.recognizeRawVoice(wf.readframes(wf.getnframes()), "wav", wf.getframerate(), cuid)

	def recognizeRawVoice(self, rawData, voiceType = "pcm", rate = 8000, cuid = "0001"):
		"""
			Using baidu voice recognization service

			Arguments:
				rawData - pcm data byte array
				voiceType - pcm、wav、opus、speex、amr、x-flac
				rate - only support 8000Hz or 16000Hz
				cuid - user identify string

			Return:
				(result_code, result_description)
				result_code - 0 is success, others is error
				result_description - recognize text string when success, others is the string for error descript
		"""
		encode_data = base64.b64encode(rawData)
		params = {
			"format": voiceType,
			"rate": rate,
			"channel": 1,
			"cuid": cuid,
			"token": BaiduEngine.getBaiduAccessToken(),
			"lan" : 'zh',
			"speech": encode_data,
			"len": len(rawData)
		}
		header = { "Content-Type": "application/json" }
		conn = None
		errCode = -1
		errData = None
		try:
			body = JSONEncoder().encode(params)
			conn = httplib.HTTPConnection("vop.baidu.com")
			conn.request("POST", "/server_api", body, header)
			resp = conn.getresponse()
			if resp.status != 200:
				errCode = -1
				errData = resp.reason
			elif (resp.getheader('Content-Type') == "application/json"):
				errs = json.loads(resp.read())
				errCode = errs.get("err_no")
				if errCode == 0 :
					errData = errs.get("result")[0].encode('utf-8')
				else:
					errData = errs.get("err_msg")
			else:
				errCode = -1
				errData = "not supported respon type(json type requested)"
		except Exception as e:
			print "[warning]BaiduEngine.recognizaPCMVioce: catch exception \"%s\"" % (e.toString())
			errCode = e.toString()
		finally:
			if conn != None:
				conn.close()
		return errCode, errData

	def getTTSMp3FromText(self, text, cuid = "0001", voiceConf = {
			"spd": 5,	# speed of speech 0-9
			"pit": 5,   # pitch of speech 0-9
			"vol": 9,	# volumn of speech 0-9
			"per": 1    # 0 is female, 1 is male
		}):
		"""
			use baidu tts service to obtain the voice data stream
			argument:
				text  -  used to tts, should be utf-8 encoding
				cuid  -  user identify
				voiceConf - configure the result sound

			return value:
				(result_code, result_description)
				result_code - 0 is success, others is error
				result_description - mp3 data when success, others is the string for error descript
		"""
		params = {
			"tex" : text,
			"lan" : "zh",
			"ctp" : 1,
			"tok" : BaiduEngine.getBaiduAccessToken(),
			"cuid" : cuid,
			"spd" : voiceConf["spd"],
			"pit" : voiceConf["pit"],
			"vol" : voiceConf["vol"],
			"per" : voiceConf["per"]
    	}
		header = {"Content-type": "application/x-www-form-urlencoded"}
		conn = None
		errCode = -1
		errData = None
		try:
			body = urllib.urlencode(params)
			conn = httplib.HTTPConnection("tsn.baidu.com")
			conn.request("POST", "/text2audio", body, header)
			resp = conn.getresponse()
			if resp.status != 200:
				errCode = -1
				errData = resp.reason
			elif (resp.getheader('Content-Type') == "application/json"):
				errs = json.loads(resp.read())
				errCode = errs.get("err_no")
				errData = errs.get("err_msg")
			elif (resp.getheader('Content-Type') == "audio/mp3"):
				errCode = 0
				errData = resp.read()
			else:
				errCode = -1
				errData = "not supported respon type(neither json nor mp3 type)"
		except Exception as e:
			print "[warning]BaiduEngine.getTTSMp3FromText: catch exception \"%s\"" % (e.toString())
			errCode = e.toString()
		finally:
			if conn != None:
				conn.close()
		return errCode, errData

if __name__ == '__main__':
	engine = BaiduEngine()
	print "TTS test..."
	errNo, result = engine.getTTSMp3FromText("百度合成语音引擎")
	if errNo == 0 :
		print "TTS correctlly!"
	else:
		print "TTS Error: %s" % result

	print "Recognization test..."
	f = open("test/test.pcm", 'rb')
	f.seek(0, 2)
	length = f.tell()
	f.seek(0, 0)
	data = f.read(length)
	errNo, result = engine.recognizeRawVoice(data, "pcm", 8000)
	if errNo == 0:
		print "Recognization result: \"%s\"" % (result)
	else:
		print "Recognization Error: %s" % (result)
		