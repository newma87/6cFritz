# -*- encoding:utf-8 -*-

"""
	Created by newma<newma@live.cn>

	singleton design pattern decorator
"""

def singletonclass(cls, *args, **kw):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

