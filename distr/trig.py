############################################################
# imports 
import matplotlib.pyplot as plt
import math
import numpy as np

from funs import *





############################################################
# data
def trig(x, a, b, c):
	return (
		    (x - a)**2 / ((b - a) * (c - a)) if a <= x <= c else
		1 - (b - x)**2 / ((b - a) * (b - c)) if c <= x <= b else
		0 if x < a else 1
	)

n    = 1001
maxx = 5.0

charts = [
	(0.0, 5.0, 2.5), (0.0, 5.0, 4.5), (0.0, 5.0, 0.5)
]

for i in range(len(charts)):
	x = np.linspace(0, maxx, n)
	y = np.array([ trig(float(t), *charts[i]) for t in x ])

	print(charts[i], flush=True)
	charts[i] = (x, y, 'a = %.1f, b = %.1f, c = %.1f' % charts[i])





############################################################
# plot
plot(charts, name="Triangular")





############################################################
# END
