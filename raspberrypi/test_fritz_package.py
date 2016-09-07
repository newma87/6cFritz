from smarttoy.fritz import FritzRobot
from time import sleep

if __name__ == "__main__":
	robot = FritzRobot()

	port = robot.findBoard()
	if port != None :
		print "found board on port %s" % (port)

	if robot.isConnected():
		robot.loadConfig()
		robot.jawConfig(pin = 1, min = -100, max = 300)
		robot.moveJaw(100)
		robot.saveConfig()

	robot.close()