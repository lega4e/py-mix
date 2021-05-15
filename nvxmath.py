# 
# author:  lis
# created: 2021.03.01 13:38:47
# 
# Разные математически функции
# 

import math





def gcd(a, b=None):
	'Нахождение НОД'
	if b is None:
		return gcd(a[0], a[1])
	while a != 0:
		b %= a
		a, b = b, a
	return b

def fac(n):
	'Факториал'
	p = 1
	for i in range(2, n+1):
		p *= i
	return p

def У(k, n):
	'Число размещений k элементов из n'
	p = 1
	for i in range(k):
		p *= n - i

def C(k, n):
	'Число сочетаний k элементов из n'
	return P(k, n) // fac(k)

def reduce(a, b=None):
	'Сокращение дроби'
	g = gcd(a, b)
	if b is None:
		return a[0] // g, a[1] // g
	return a // g, b // g

def striling(n):
	'Приближенное вычисление факториала по формуле Стирлинга'
	return math.sqrt(2*math.pi*n) * (n/math.e) ** n





# classes
class Vec2:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		return

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def scalar(lhs, rhs):
		return lhs.x * rhs.x + lhs.y * rhs.y

	def cos(lhs, rhs):
		return lhs.scalar(rhs) / lhs.length() / rhs.length()

	def angle(lhs, rhs):
		return math.acos(lhs.cos(rhs))

	def __str__(self):
		return '(%.3f, %.3f)' % (self.x, self.y)





# END
