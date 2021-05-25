# 
# author:  nvx
# created: 2021.05.25 12:18:12
# 

from nvxmath import gcd, lcm







# types
class Frac:
	'''
	Frac class description
	'''
	a = 0
	b = 1

	def __init__(self, a = 0, b = 1):
		self.a = a
		self.b = b
		self.reduce()
		return

	def isNaN(self):
		'Проверяет, имеет ли дробь особое значение'
		return self.b == 0

	def clone(self):
		return Frac(self.a, self.b)

	def reduce(self):
		'''
		Сокращение дроби (производится автоматически
		при каждой арифметической операции)
		'''
		g = gcd(abs(self.a), self.b)
		self.a //= g
		self.b //= g
		if self.a < 0 and self.b < 0:
			self.a, self.b = -self.a, -self.b
		return self



	# Операторы приведения
	def __str__(self):
		return (
			'%i/%i' % (self.a, self.b)
			if not self.isNaN() else
			'NaN'
		)

	def __repr__(self):
		return "<class 'nvxfrac.Frac' : %s>" % str(self)

	def __float__(self):
		return self.a / self.b

	def __int__(self):
		return self.a // self.b



	# Операторы присваивающих арифметических операций
	def __iadd__(lhs, rhs):      # +=
		if lhs.isNaN():
			return lhs
		if isinstance(rhs, int):
			rhs = Frac(rhs)
		l = lcm(lhs.b, rhs.b)
		lhs.a = lhs.a * (l // lhs.b) + rhs.a * (l // rhs.b)
		lhs.b = l
		lhs.reduce()
		return lhs

	def __isub__(lhs, rhs):      # -=
		if lhs.isNaN():
			return lhs
		if isinstance(rhs, int):
			rhs = Frac(rhs)
		l = lcm(lhs.b, rhs.b)
		lhs.a = lhs.a * (l // lhs.b) - rhs.a * (l // rhs.b)
		lhs.b = l
		lhs.reduce()
		return lhs

	def __imul__(lhs, rhs):      # *=
		if lhs.isNaN():
			return lhs
		if isinstance(rhs, int):
			rhs = Frac(rhs)
		lhs.a *= rhs.a
		lhs.b *= rhs.b
		lhs.reduce()
		return lhs

	def __itruediv__(lhs, rhs):  # /=
		if lhs.isNaN():
			return lhs
		if isinstance(rhs, int):
			rhs = Frac(rhs)
		lhs.a *= rhs.b
		lhs.b *= rhs.a
		lhs.reduce()
		return lhs


	# Неприсваивающие арифметические операции
	def __add__(lhs, rhs):     # x + y
		res  = lhs.clone()
		res += rhs
		return res

	def __sub__(lhs, rhs):     # x - y
		res  = lhs.clone()
		res -= rhs
		return res

	def __mul__(lhs, rhs):     # x * y
		res  = lhs.clone()
		res *= rhs
		return res

	def __truediv__(lhs, rhs): # x / y
		res  = lhs.clone()
		res /= rhs
		return res


	def __radd__(rhs, lhs):     # x + y
		res  = rhs.clone()
		res += lhs
		return res

	def __rsub__(rhs, lhs):     # x - y
		if isinstance(lhs, int):
			res = Frac(lhs)
		else:
			res  = lhs.clone()
		res -= rhs
		return res

	def __rmul__(rhs, lhs):     # x * y
		res  = rhs.clone()
		res *= lhs
		return res

	def __rtruediv__(rhs, lhs): # x / y
		if isinstance(lhs, int):
			res = Frac(lhs)
		else:
			res  = lhs.clone()
		res /= rhs
		return res



	# Операции сравнения
	def __lt__(lhs, rhs): # x < y
		if not isinstance(rhs, Frac):
			return not lhs.isNaN() and float(lhs) < rhs
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b < rhs.a * lhs.b
		)

	def __gt__(lhs, rhs): # x > y
		if not isinstance(rhs, Frac):
			return not lhs.isNaN() and float(lhs) > rhs
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b > rhs.a * lhs.b
		)

	def __le__(lhs, rhs): # x ≤ y
		return lhs < rhs or lhs == rhs

	def __ge__(lhs, rhs): # x ≥ y
		return lhs > rhs or lhs == rhs

	def __eq__(lhs, rhs): # x == y
		if isinstance(rhs, int):
			return (
				not lhs.isNaN() and
				lhs.a % lhs.b == 0 and
				int(lhs) == rhs
			)
		elif not isinstance(rhs, Frac):
			return not lhs.isNaN() and float(lhs) == rhs
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b == rhs.a * lhs.b
		)

	def __ne__(lhs, rhs): # x != y
		return not lhs == rhs


	def __rlt__(rhs, lhs): # x < y
		if not isinstance(lhs, Frac):
			return not rhs.isNaN() and lhs < float(rhs)
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b < rhs.a * lhs.b
		)

	def __rgt__(rhs, lhs): # x > y
		if not isinstance(lhs, Frac):
			return not rhs.isNaN() and lhs > float(rhs)
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b > rhs.a * lhs.b
		)

	def __rle__(rhs, lhs): # x ≤ y
		return lhs < rhs or lhs == rhs

	def __rge__(rhs, lhs): # x ≥ y
		return lhs > rhs or lhs == rhs

	def __req__(rhs, lhs): # x == y
		if isinstance(lhs, int):
			return (
				not rhs.isNaN() and
				rhs.a % rhs.b == 0 and
				int(rhs) == lhs
			)
		elif not isinstance(lhs, Frac):
			return not rhs.isNaN() and float(rhs) == lhs
		return (
			not lhs.isNaN() and not rhs.isNaN() and
			lhs.a * rhs.b == rhs.a * lhs.b
		)

	def __rne__(rhs, lhs): # x != y
		return not lhs == rhs







# END
