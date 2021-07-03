############################################################
# imports 
import matplotlib.pyplot as plt
import math
import numpy as np

from funs import *





############################################################
# data
def erlang(x, n, l):
	return l**n * x**(n-1) * math.exp(-l*x) / fac(n-1)

n    = 1001
maxx = 12.0

charts = [
	#  (2, 0.5), (3, 0.5), (7, 0.5)
	(3, 0.5),
	(3, 1.0),
	(3, 2.0),
]

for i in range(len(charts)):
	x = np.linspace(0, maxx, n)
	y = np.array([ erlang(float(t), charts[i][0], charts[i][1]) for t in x ])

	print(charts[i], flush=True)
	charts[i] = (x, y, 'n = %i, l = %.1f' % (charts[i][0], charts[i][1]))





############################################################
# plot
plot(charts, name="Erlang")





############################################################
# END
