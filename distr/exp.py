############################################################
# imports 
import matplotlib.pyplot as plt
import math
import numpy as np

from funs import *





############################################################
# data
def exp(t, l):
	return 1 - math.exp(-l * t)

n = 1001
maxt = 2

charts = [ 0.5, 1, 1.5 ]

for i in range(len(charts)):
	x = np.linspace(0, 5, n)
	y = np.array([ exp(t, charts[i]) for t in x ])

	print(charts[i], flush=True)
	charts[i] = (x, y, 'lambda = %.1f' % charts[i])





############################################################
# plot
plot(charts)





############################################################
# END
