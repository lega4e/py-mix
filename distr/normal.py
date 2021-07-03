############################################################
# imports 
import matplotlib.pyplot as plt
import math
import numpy as np

from funs import *





############################################################
# data
def norm(x, u, o):
	return math.e ** (-(x - u)**2 / (2*o)) / math.sqrt(2 * math.pi * o)

l = 6
n = 1001

charts = [
	#  (0.0, 1.0), (0.0, 0.5), (0.0, 0.2),
	(1.0, 1.0),
	(3.0, 1.0),
]

for i in range(len(charts)):
	x = np.linspace(charts[i][0] - l/2, charts[i][0] + l/2, n)
	y = norm(x, charts[i][0], charts[i][1])

	charts[i] = (x, y, 'u = %.1f, o^2 = %.1f' % (charts[i][0], charts[i][1]))





############################################################
# plot
plot(charts)





############################################################
# END
