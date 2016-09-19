# -*- encoding:utf-8 -*-

"""
	Created by newma
"""
from abc import ABCMeta, abstractmethod

class AudioRecordCallback(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def onRecordData(self, in_data, bytesCount, frame_count, obj):
		pass

class AudioPlayCallback(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def onPlayEndCallback(self, obj):
		pass
		