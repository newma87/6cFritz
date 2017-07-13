# -*- encoding:utf-8 -*-

"""
	Created by newma<newma@live.cn>

	singleton design pattern decorator
"""

import __builtin__
import threading

__builtin__.SmarttoySingleInstances = {}
__builtin__.SmarttoyLock = threading.Lock()

def singletonclass(cls, *args, **kw):  
	def _singleton(*args, **kw):
		name = cls.__name__
		if name not in __builtin__.SmarttoySingleInstances:
			__builtin__.SmarttoyLock.acquire()
			if cls not in __builtin__.SmarttoySingleInstances:
				__builtin__.SmarttoySingleInstances[name] = object.__new__(cls)#cls(*args, **kw)
				__builtin__.SmarttoySingleInstances[name].__init__(*args, **kw)
			__builtin__.SmarttoyLock.release()
		return __builtin__.SmarttoySingleInstances[name]  
	return _singleton

def destorySingleton(instance):
	name = instance.__class__.__name__
	if name in __builtin__.SmarttoySingleInstances:
		__builtin__.SmarttoyLock.acquire()
		if name in __builtin__.SmarttoySingleInstances:
			__builtin__.SmarttoySingleInstances[name] = None
		__builtin__.SmarttoyLock.release()
