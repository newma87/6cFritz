# -*- coding: utf-8 -*- 

import urllib
import httplib
import json

class TulingResultFactory(object):
	@staticmethod
	def createResult(jsonText):
		obj = json.loads(jsonText)
		code = obj.get("code")
		if code == 100000:
			return TulingResult(obj)
		elif code == 200000:
			return TulingLinksResult(obj)
		elif code == 302000:
			return TulingNewsResult(obj)
		elif code == 308000:
			return TulingMenuResult(obj)
		elif code == 313000:
			return None      # not supported
		elif code == 314000:
			return None 	 # not supported
		else:
			return TulingErrorResult(obj)

class TulingResult(object):
	def __init__(self, dictObj):
		self.code = dictObj["code"]
		self.text = dictObj["text"]

	def getCode(self):
		return self.code
	def setCode(self, code):
		self.code = code

	def getText(self):
		return self.text
	def setText(self, text):
		self.text = text

	def getDescriptType(self):
		if self.code == 100000:
			return "text"
		elif self.code == 200000:
			return "link"
		elif self.code == 302000:
			return "new"
		elif self.code == 308000:
			return "menu"
		elif self.code == 313000:
			return "song"
		elif self.code == 314000:
			return "poem"
		else:
			return "error"

class TulingErrorResult(TulingResult):
	def __init__(self, dictObj):
		TulingResult.__init__(self, dictObj)

class TulingLinksResult(TulingResult):
	def __init__(self, dictObj):
		TulingResult.__init__(self, dictObj)
		self.url = dictObj.get["url"]

	def getUrl(self):
		return self.url
	def setUrl(self, url):
		self.url = url

class TulingNewsResult(TulingResult):
	def __init__(self, dictObj):
		TulingResult.__init__(self, dictObj)
		self.news = dictObj.get("list")

	def getNews(self):
		return self.news
	def setNews(self, lists = []):
		self.news = lists

	def getArticalLists(self):
		result = []
		for item in self.news:
			result.append(item["article"])
		return result

class TulingMenuResult(TulingResult):
	def __init__(self, dictObj):
		TulingResult.__init__(self, dictObj)
		self.menus = dictObj.get("list")

	def getMenus(self):
		return self.menus
	def setMenus(self, menus = []):
		self.menus = menus

	def getMenusInfos(self):
		result = []
		for item in self.menus:
			result.append(item["name"])
		return result

class TulingRobot(object):
	__APP_KEY__ = "176ac2eb42664f57941db41b9b79e9c0"
	__TULING_SERVER__ = "www.tuling123.com"

	@staticmethod
	def getResponseForQuestion(unicodeQuestion, cuid = "0001"):
		"""
			Request answear from tuling robot

			Arguments:
				question - an unicode string
				cuid - identify user

			return:

		"""
		if not isinstance(unicodeQuestion, unicode):
			print "[warning]TulingRobot.getResponseForQuestion: argument unicodeQuestion should be in unicode type"
			return None

		conn = None
		result = None

		params = {
			'key': TulingRobot.__APP_KEY__,
			'info': unicodeQuestion.encode('utf-8'),
			'userid': cuid
		}
		headers = { "Content-Type": 'application/x-www-form-urlencoded' }
		try:
			body = urllib.urlencode(params)
			conn = httplib.HTTPConnection(TulingRobot.__TULING_SERVER__)
			conn.request("POST", "/openapi/api", body, headers)
			resp = conn.getresponse().read()
			result = TulingResultFactory.createResult(resp)
		except Exception as e:
			print e
		finally:
			if conn != None:
				conn.close()
		return result

if __name__ == '__main__':
	result = TulingRobot.getResponseForQuestion(u"你好")
	if result == None:
		print "TulingRobot.getResponseForQuestion test failed!"
	elif result.getDescriptType() == "error":
		print "Error: ", result.getText()
	else:
		print result.getText()
