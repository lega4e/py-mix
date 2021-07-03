############################################################
# imports 
import matplotlib.pyplot as plt
import math
import numpy as np

from funs import *





############################################################
# data
def poisson(k, l):
	return l ** k / fac(k) * math.exp(-l)

n = 40

charts = [ 1, 2, 5, 10, 20 ]

for i in range(len(charts)):
	x = list(range(0, n+1))
	y = [ poisson(k, charts[i]) for k in x ]

	charts[i] = (x, y, 'lambda = %i' % charts[i])





############################################################
# plot
plot(charts)





############################################################
# END
