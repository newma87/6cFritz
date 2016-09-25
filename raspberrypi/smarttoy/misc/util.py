#-*- encoding: utf-8 -*-

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

def getUserDataFold():
	if (os_type == "Linux"):
		return os.environ['HOME']
	elif (os_type == "Windows"):
		return shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_APPDATA))
