############################################################
# imports 
import matplotlib.pyplot as plt
import numpy as np

from funs import *





############################################################
# data
n = 100

charts = [ (i/10, 1 - i/10) for i in range(1, 10) ]

for i in range(len(charts)):
	x = np.arange(0, n+1)
	y = np.zeros((n+1,))

	for j in range(n+1):
		y[j] = C(j, n) * charts[i][0]**j * charts[i][1]**(n-j)

	charts[i] = (x, y, 'p = %.1f, q = %.1f' % (charts[i][0], charts[i][1]))





############################################################
# plot
plot(charts)





############################################################
# END
