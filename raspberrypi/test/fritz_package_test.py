#-*- encoding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from smarttoy.fritz import FritzRobot
from time import sleep
 
if __name__ == "__main__":
	robot = FritzRobot()

	port = robot.findBoard()
	if port != None :
		print "found board on port %s" % (port)

	if robot.isConnected():
		print "load config..."
		robot.loadConfig()
		old = robot.state
		print "change config..."
		robot.jawConfig(pin = 1, min = -100, max = 300)
		print "save config..."
		robot.saveConfig()
		print "current robot state:"
		robot.dumpRobotState()
		sleep(0.5)
		robot.moveJaw(100)
		sleep(0.5)
		print "restore config..."
		robot.state = old
		robot.saveConfig()
		sleep(0.5)

	robot.close()
