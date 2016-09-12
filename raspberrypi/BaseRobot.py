#-*- encoding:utf-8 -*-

"""
    The primary one has 5 parts which contains 2eyebrows, 2 lips and 1 jaw.
    He has two expression to express superise, sleepy, fury, speaking.
    Every expression has its name and its duration to express.
    A import tip: the maximum for jaw means closuse.
"""

__author__ = "yzihushan@gmail.com"

#module
from smarttoy.fritz import FritzRobot
import time 
import random 

class BaseRobot(object):
    #when init
    #1.findBoard()
    #2.complete the definate part`s config 
    #3.saveconfig()
    def __init__(self, config):
        self.robot = FritzRobot()
        port = self.robot.findBoard()
        self.robot.loadConfig()
        if port == None:
            print "not found board"
            exit()
        if not self.robot.state.get("leftLidPosition").get("pin")== config.get("leftLidPosition").get("pin"):
            self.robot.leftLidPositionConfig(config.get("leftLidPosition").get("trim"),
                                             config.get("leftLidPosition").get("min"),
                                             config.get("leftLidPosition").get("max"),
                                             config.get("leftLidPosition").get("pin"),
                                             config.get("leftLidPosition").get("enable"))
        if not self.robot.state.get("rightLidPosition").get("pin")== config.get("rightLidPosition").get("pin"):
            self.robot.rightLidPositionConfig(config.get("rightLidPosition").get("trim"),
                                              config.get("rightLidPosition").get("min"),
                                              config.get("rightLidPosition").get("max"),
                                              config.get("rightLidPosition").get("pin"),
                                              config.get("rightLidPosition").get("enable"))
        if not self.robot.state.get("leftEyebrow").get("pin")== config.get("leftEyebrow").get("pin"):
            self.robot.leftEyeBrowConfig(config.get("leftEyebrow").get("trim"),
                                         config.get("leftEyebrow").get("min"),
                                         config.get("leftEyebrow").get("max"),
                                         config.get("leftEyebrow").get("pin"),
                                         config.get("leftEyebrow").get("enable")) 
        if not self.robot.state.get("rightEyebrow").get("pin")== config.get("rightEyebrow").get("pin"):
            self.robot.rightEyeBrowConfig(config.get("rightEyebrow").get("trim"),
                                          config.get("rightEyebrow").get("min"),
                                          config.get("rightEyebrow").get("max"),
                                          config.get("rightEyebrow").get("pin"),
                                          config.get("rightEyebrow").get("enable"))     
        if not self.robot.state.get("jaw").get("pin")== config.get("jaw").get("pin"):
            self.robot.jawConfig(config.get("jaw").get("trim"),
                                 config.get("jaw").get("min"),
                                 config.get("jaw").get("max"),
                                 config.get("jaw").get("pin"),
                                 config.get("jaw").get("enable"))    
        self.robot.saveConfig()

    #this function can use lamda and dict
    

    #move all parts to normal suitation
    def normal(self,duration):
        self.robot.moveLeftLidPosition(0)
        self.robot.moveRightLidPosition(0)
        self.robot.moveRightEyeBrow(0)
        self.robot.moveLeftEyeBrow(0)
        self.robot.moveJaw(config.get("jaw").get("max"))
        time.sleep(duration)

    #2.5s is the minimum period
    def blink(self,duration):
        i= 0
        while i< duration:
            self.robot.moveLeftLidPosition(config.get("leftLidPosition").get("min"))
            self.robot.moveRightLidPosition(config.get("rightLidPosition").get("min"))
            time.sleep(0.5)
            self.robot.moveLeftLidPosition(0)
            self.robot.moveRightLidPosition(0)
            time.sleep(2)
            i+= 2.5


    #move brows only
    def fury(self,duration):
        self.robot.moveLeftLidPosition(config.get("leftLidPosition").get("trim") - 20)
        self.robot.moveRightLidPosition(config.get("rightLidPosition").get("trim") - 20)
        i = 0
        while(i < duration):
            if i % 2:
                self.robot.moveLeftEyeBrow(config.get("leftEyebrow").get("max"))
                self.robot.moveRightEyeBrow(config.get("rightEyebrow").get("max"))
                time.sleep(0.2)
            else:
                self.robot.moveLeftEyeBrow(config.get("leftEyebrow").get("min"))
                self.robot.moveRightEyeBrow(config.get("rightEyebrow").get("min"))
                time.sleep(0.2)
            i +=1
        self.normal(1)
    
    def superising(self,duration):
        print "superising now"
        i = 0
        while i<duration:
            i +=3
            self.robot.moveLeftLidPosition(config.get("leftLidPosition").get("max"))
            self.robot.moveRightLidPosition(config.get("rightLidPosition").get("max"))
            self.robot.moveJaw(config.get("jaw").get("min"))
            time.sleep(0.5)
            self.normal(1)

    #Every 5 seconds, he will yawn.
    def sleepy(self, duration):
        i= 1
        angle= config.get("leftLidPosition").get("trim")
        while (i < duration and angle> min):
            angle+=i*(-10) 
            self.robot.moveLeftLidPosition(angle)
            self.robot.moveRightLidPosition(angle)
            time.sleep(1)
            if not i % 5:
                angle= max
                self.robot.moveLeftLidPosition(angle)
                self.robot.moveRightLidPosition(angle)
                # self.robot.moveJaw(min)
                #learn: servo and time 
                time.sleep(0.5)
                angle= min
                self.robot.moveLeftLidPosition(angle)
                self.robot.moveRightLidPosition(angle)
                # self.robot.moveJaw(max)
                angle= trim
                time.sleep(0.3) 
            i +=1
        self.normal(1)
        

    #To simulate opening and closing mouth randomly.
    def speaking(self,duration):
        print "speaking now"
        i =1
        while i< duration:
            j = random.randint(1,3)
            if j%3:
                self.robot.moveJaw(config.get("jaw").get("min"))
            elif j%2:
                self.robot.moveJaw(0)
            else:
                self.robot.moveJaw(config.get("jaw").get("max"))
            time.sleep(0.5)
            i +=1
        self.normal(1)
    # print 1
    # self.robot.moveLeftLidPosition(0)
    # print 1
    # self.robot.moveRightLidPosition(0)
    def liveon(self, expression, duration):
        self.normal(1)
        self.blink(1)
        self.blink(1)
        self.blink(1)
        self.blink(1)
        expressions = {
            'superising': self.superising,
            'fury':self.fury,
            'sleepy':self.sleepy,
            'speaking':self.speaking
                    }.get(expression)(duration)
        self.normal(1)
#test
config = { 
	"leftHorizontalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftVerticalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"leftEyebrow" :  { "trim": 0, "min": -300, "max": 100, "pin": 8, "enable": True },
			"leftLidPosition" :  { "trim": -50, "min": -150, "max": 100, "pin": 2, "enable": True },
			"leftLip" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightHorizontalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightVerticalEye" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"rightEyebrow" :  { "trim": 0, "min": -100, "max": 100, "pin": 6, "enable": True },
			"rightLidPosition" :  { "trim": -50, "min": -100, "max": 100, "pin": 3, "enable": True },
			"rightLip" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"neckTilt" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"neckTwist" :  { "trim": 0, "min": -1000, "max": 1000, "pin": -1, "enable": False },
			"jaw" :  { "trim": -200, "min": -500, "max": 50, "pin": 4, "enable": True },
			"sonar" :  { "triggerPin": -1, "echoPin": -1, "enable": False},
			"ir" :  { "pin": -1, "enable": False }
		}
    

if __name__== '__main__':
    a= BaseRobot(config)
    print "Robot is comming."
    # a.liveon("superising",10)
    # print "superising"

    # print "superising"
    # a.superising(10)
    
    # print "speaking"
    # a.speaking(10)
    
    # print "fury"
    # a.fury(10)

    print "liveon"
    a.liveon("superising",5)
    #q: because all of this partion is not absolutely symmetry,this is quite narrow

    #httplib from urllib2
    #json
    #pyaudio

        

        
        
        
    


    


