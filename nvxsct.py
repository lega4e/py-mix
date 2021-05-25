# author:  nvx
# created: 2021.03.01 21:29:08
# 
# Простая структура данных; почти как
# словарь, только обращаться к полям
# через точку
#

class sct:
	def __init__(self, **kargs):
		for key, value in kargs.items():
			self.__dict__[key] = value
		return

	def __str__(self):
		return '{' + ', '.join( self._extract(val) for val in self.__dict__.values() ) + '}'

	def __repr__(self):
		return '<' + ', '.join(
			'%s=%s' % (str(key), self._extract(value))
			for key, value in self.__dict__.items()
		) + '>'

	def __getitem__(self, key):
		point = key.find('.')
		if point < 0: 
			return self.__dict__[key]
		pkey = key[:point]
		return self.__dict__[pkey][key[point+1:]]

	def __setitem__(self, key, value):
		point = key.find('.')
		if point < 0:
			self.__dict__[key] = value
			return
		pkey = key[:point]
		if pkey not in self.__dict__:
			self.__dict__[pkey] = sct()
		self.__dict__[pkey][key[point+1:]] = value
		return

	def __iter__(self):
		for item in self.__dict__.items():
			yield item

	def pretty(self, tab='', name='sct'):
		length = max(list(map(
			lambda s: len(s),
			filter(
				lambda key: not isinstance(self.__dict__[key], sct),
				self.__dict__.keys()
			)
		)) + [0])
		s = tab + name + ':\n'
		tab += '  '
		for key in self.__dict__.keys():
			obj = self.__dict__[key]
			if isinstance(obj, sct):
				s += obj.pretty(tab, name=key)
			else:
				s += (
					tab + (key + (length - len(key))*' ') + ' : ' +
					self._extract(self.__dict__[key]) + '\n'
				)
		return s


	@staticmethod
	def _extract(val):
		if isinstance(val, str):
			return "'" + val + "'"
		return str(val)





# END
