from smarttoy.fritz import FritzRobot

if __name__ == "__main__":
	robot = FritzRobot()

	port = robot.findBoard()
	if port != None :
		print "found board on port %s" % (port)

	if robot.isConnected():
		robot.loadConfig()
		robot.moveJaw(100)
	robot.close()