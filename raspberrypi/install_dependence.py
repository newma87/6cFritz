#-*- encoding: utf-8 -*-

import httplib
import re
import tarfile
import subprocess
import os
import sys
import shutil
import networkspeed as ns

from time import sleep

TMP_DIR = '/tmp'

#====================utils==================================
def getPythonModulePath():
	paths = []
	for path in sys.path:
		if re.search("site-packages$", path):
			paths.append(path)
	return paths

def checkPythonModuleInstalled(moduleName):
	module_path = getPythonModulePath()
	for p in module_path:
		if os.path.exists(p + '/' + moduleName):
			return True
	return False

def getLinuxDistro():
	data = subprocess.Popen("cat /etc/*release", shell = True, stdout = subprocess.PIPE).communicate()[0]
	return re.search('NAME=[\"]*([^\n^\"]+)[\"]*', data).group(1).lower()

def request(url):
	isHttps = re.match("https://", url) != None
	if isHttps:
		webSite = url[8:].split('/')[0]
		routePath = url[8 + len(webSite):]
	else:
		webSite = url[7:].split('/')[0]
		routePath = url[7 + len(webSite):]

	if not routePath:
		routePath = '/'

	data = None
	conn = None
	try:
		if isHttps:
			conn = httplib.HTTPSConnection(webSite)
		else:
			conn = httplib.HTTPConnection(webSite)
		conn.request('GET', routePath)
		resp = conn.getresponse()
		data = resp.read()
	except httplib.HTTPException as ex:
		print ex.toString()
	finally:
		if conn:
			conn.close()
	return data

def download(url):
	package = TMP_DIR + '/' + url[url.rfind('/') + 1:]
	file = None
	try:
		print "Downloading '%s' ..." % (url)
		file = open(package, 'wb')
		ns.startNetworkTrace()
		file.write(request(url))
		ns.stopNetworkTrace()
		file.flush()
	except IOError as err:
		print err
		print "Download '%s' failed!" % (url)
		return None
	finally:
		if file:
			file.close()
	return package

def untarFile(package):
	tar = tarfile.open(package)
	tar.extractall(package[0 : package.rfind('/')])
	tar.close()
	return package[:package.rfind('.tar')]

#==========================mpg123 install=========================================
def checkMpg123Installed():
	return os.path.exists('/usr/local/lib/libmpg123.so') or os.path.exists('/usr/lib/libmpg123.so')

def getMpg123LastVersion():
	url = "https://sourceforge.net/projects/mpg123/files/"
	data = request(url)
	return re.search("Download mpg123-([\.\d]+)\.tar", data).group(1)

def downloadMpg123():
	version = getMpg123LastVersion()
	download_url = "http://heanet.dl.sourceforge.net/project/mpg123/mpg123/%s/mpg123-%s.tar.bz2" % (version, version)
	return download(download_url)

def installMpg123():
	if sys.platform.find("win") > 0:
		print "Sorry, you have to manually install mpg123 package on windows"
		return

	print "Start to download mpg123 package"
	gzFile = downloadMpg123()
	package = gzFile.split('/')[-1]
	print "Download done!"

	print "Untar package '%s'" % (package)
	install_dir = untarFile(gzFile)

	print "Installing mpg123..."
	try:
		subprocess.Popen('./configure', shell = True, cwd = install_dir).wait()
		subprocess.Popen('make', shell = True, cwd = install_dir).wait()
		subprocess.Popen('sudo make install', shell = True, cwd = install_dir).wait()
		print "Install mpg123 done!"
	except OSError as er:
		print er.child_traceback
		print "[error] Installing mpg123 failed!"

	#remove tmp file
	os.remove(gzFile)
	shutil.rmtree(install_dir)

#==========================audiotools install=========================================
def getAudioToolsLastesVersion():
	data = request("http://audiotools.sourceforge.net")
	return re.search("Latest version: ([\d\.]*)", data).group(1)

def downloadAudioTools():
	version = getAudioToolsLastesVersion()
	download_url = "http://heanet.dl.sourceforge.net/project/audiotools/audiotools/%s/audiotools-%s.tar.gz" % (version, version)
	return download(download_url)

def installAudioTools():
	if sys.platform.find("win") > 0:
		print "Sorry, you have to manually install audiotools package on windows"
		return

	print "Start to download audiotools package"
	gzFile = downloadAudioTools()
	package = gzFile.split('/')[-1]
	print "Download done!"

	print "Untar package '%s'" % (package)
	install_dir = untarFile(gzFile)

	print "Installing audiotools..."
	try:
		subprocess.Popen('make install', shell = True, cwd = install_dir).wait()
		print "Install audiotools done!"
	except OSError as er:
		print er.child_traceback
		print "[error] Installing audiotools failed!"

	#remove tmp file
	os.remove(gzFile)
	shutil.rmtree(install_dir)

#==========================pyaudio install=========================================
def installPyAudio():
	if sys.platform.find("win") > 0:
		print "Sorry, you have to manually install pyaudio package on windows"
		return

	dist = getLinuxDistro()
	cmd = None
	if dist == 'fedora' or dist == 'centos' or dist == 'redhat':
		cmd = "sudo yum install -y pyaudio"
	else:
		cmd = "sudo apt-get install -y python-pyaudio"
	try:
		subprocess.Popen(cmd, shell = True).wait()
		print "Install pyaudio done!"
	except OSError as er:
		print er.child_traceback
		print "[error] Installing pyaudio failed!"	

#====================================================================================
def main():
	try:
		subprocess.Popen("pip install -r requirements.txt", shell = True).wait()
	except OSError as er:
		print er.child_traceback

	# install mpg123 for audiotools
	if not checkMpg123Installed():
		installMpg123()
	else:
		print "mpg123 installed" 

	#install audiotools
	if checkPythonModuleInstalled("audiotools"):
		print "audiotools installed"
	else:
		installAudioTools()

	#install pyAudio
	if checkPythonModuleInstalled("pyaudio.py"):
		print "pyaudio installed"
	else:
		installPyAudio()

if __name__ == '__main__':
	main()
