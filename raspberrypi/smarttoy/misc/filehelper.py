#-*- encoding: utf-8 -*-
"""
	Created by newma<newma@live.cn>
"""

import shutil
import platform

os_type = platform.system()

try:
	if (os_type == "Windows"):
		from win32com.shell import shell  
		from win32com.shell import shellcon  
	elif (os_type == "Linux"):
		import os
except ImportError as e:
	print e.toString()
	exit()

def getUserHomeFold():
	"""
		get current user folder path
		On windows is some kind of lik "C:\\Document and Settings\\USER_NAME\\AppData"
		On linux is "$HOME" path
	"""
	if (os_type == "Linux"):
		return os.environ['HOME']
	elif (os_type == "Windows"):
		return shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_APPDATA))

def removeNoemptyFold(fold):
	shutil.rmtree(fold)
