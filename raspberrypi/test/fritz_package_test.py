#-*- encoding: utf-8 -*-
from context import smarttoy

from smarttoy.fritz import FritzRobot
from time import sleep
 
if __name__ == "__main__":
	robot = FritzRobot()

	port = robot.findBoard()
	if port != None :
		print "found board on port %s" % (port)

	if robot.isConnected():
		if not robot.loadConfig():
			print 'load config failed'
			exit()
		robot.jawConfig(pin =9, min=-500, max = 500)
		if not robot.saveConfig():
			print 'save config failed'
			exit()
		sleep(0.5)
		robot.moveJaw(300)
		sleep(0.5)

	robot.close()
