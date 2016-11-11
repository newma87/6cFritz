# -*- encoding: utf-8 -*-

import threading
from collections import deque
import time
import psutil
import sys

trace_flag = False
trace_thread = None

def calcNetwork(rate, dt=1, interface='wlp3s0'):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)
    global trace_flag
    while trace_flag:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [(now - last) / (t1 - t0) / 1000.0
                  for now, last in zip(tot, last_tot)]
        rate.append((ul, dl))
        printRate(rate)
        t0 = time.time()
    print '\n'

def printRate(rate):
	"""
    try:
        print 'UL: {0:.0f} kB/s / DL: {1:.0f} kB/s'.format(*rate[-1])
    except IndexError:
        'UL: - kB/s/ DL: - kB/s'
    """
	try:
		sys.stdout.write("\rDownload at speed: {1:.0f} kB/s".format(*rate[-1]))
	except IndexError:
		sys.stdout.write("\rDownload at speed: - kB/s")
	sys.stdout.flush()

def startNetworkTrace():
	stopNetworkTrace()

	global trace_thread, trace_flag
	trace_flag = True
	transfer_rate = deque(maxlen=1)
	trace_thread = threading.Thread(target=calcNetwork, args=(transfer_rate,))

	# The program will exit if there are only daemonic threads left.
	trace_thread.daemon = True
	trace_thread.start()

def stopNetworkTrace():
	global trace_thread, trace_flag
	if trace_thread:
		trace_flag = False
		trace_thread.join()
		trace_thread = None
