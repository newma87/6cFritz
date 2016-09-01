#! /usr/bin/python #pylint: disable=C0111
#-*- utf-8 -*-

import json
import httplib

class TTSpeech:
	def __init__(self, queue, text = ''):
		self._text = text

	def setText(self, text):
		self._text = text

	def speak(self):
		pass
		
