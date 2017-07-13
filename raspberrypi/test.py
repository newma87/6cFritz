
from smarttoy.singleton import singletonclass
from threading import Thread
from time import sleep

INSTANCE_COUNT = 0

@singletonclass
class App(object):
	def __init__(self):
		global INSTANCE_COUNT
		INSTANCE_COUNT = INSTANCE_COUNT + 1
		print "instance count: %d" % INSTANCE_COUNT

def run():
	App()
	print "end thread..."

if __name__ == '__main__':
	for i in xrange(0, 4):
		th = Thread(target = run)
		th.start()
	sleep(2)
	print INSTANCE_COUNT

"""
from Tkinter import *

root = Tk()

var = IntVar()
def onChange(*arg):
	print arg
	print 'value change', var.get()

var.trace_variable('w', onChange)

def validateNum(old, new):
	print "old:", old, " new:", new 
	return True

#c = Checkbutton(root, text = "text", variable = var)
#c.pack()

vldt_ifnum_cmd = (root.register(validateNum),'%s', '%S')
w = Spinbox(root, from_ = -1000, to = 1000, textvariable = var, validate='all', validatecommand = (validateNum, '%s', '%S'))
w.var = var
w.pack()

def onClick():
	print var.get()
b = Button(root, text = "get", command = onClick)
b.pack()

def onSet():
	i = var.get()
	if i == 0:
		var.set(1)
	else:
		var.set(0)
t = Button(root, text = 'set', command = onSet)
t.pack()
#w = Spinbox(values=(1, 2, 4, 8))
#w.pack()

#w2 = Spinbox(root, from_=0, to=10)
#w2.pack()

root.mainloop()
"""
	