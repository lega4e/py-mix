#!/usr/bin/python3

from threading import Thread

import datetime as dt
import math
import time





# functions
def thread_function(time):
	btime = dt.datetime.now()

	while dt.datetime.now() < btime + dt.timedelta(seconds=time):
		value = math.sin(dt.datetime.now().second)

	return





# main
print('Start thread function alone (time=3.0)', flush=True)
thread_function(3.0)

print('Sleep 3.0 seconds', flush=True)
time.sleep(3.0)


n = 4
print('Start %i threads' % n, flush=True)
ths = [ Thread(target=thread_function, args=[10.0]) for i in range(n) ]
for th in ths:
	th.start()

print('Join threads...', flush=True)
for th in ths:
	th.join()

print('END', flush=True)





# END
