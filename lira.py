# 
# author:   lis
# created: 2021.03.01 01:04:18
# 
import pickle



class Lira:
	def __init__(self, _data, _head):
		self.__dict__['_fpls'] = { (0, 2**40) }
		self.__dict__['_objs'] = dict()
		self.__dict__['_objv'] = dict()
		self.__dict__['_cats'] = dict()
		self.__dict__['_mnid'] = -1
		try:
			self.__dict__['_data'] = open(_data, 'rb+')
		except:
			self.__dict__['_data'] = open(_data, 'wb+')
		self.__dict__['_head'] = _head
		self.read_head()
		return

	def __del__(self):
		self._data.close()
		self.write_head()
		return

	def read_head(self, _head=None):
		if _head is None:
			_head = self._head;
		try:
			with open(_head, 'rb') as file: # if can't open ?
				self.__dict__['_fpls'] = pickle.load(file)
				self.__dict__['_objs'] = pickle.load(file)
				self.__dict__['_cats'] = pickle.load(file)
			self.__dict__['_mnid'] = min(
				filter(lambda x: isinstance(x, int), self._objs.keys())
			) - 1
		except:
			pass
		return

	def write_head(self, head=None):
		if head is None:
			head = self._head;
		with open(head, 'wb') as file:
			pickle.dump(self._fpls, file)
			pickle.dump(self._objs, file)
			pickle.dump(self._cats, file)
		return

	def get(self, id):
		obj = self._objv.get(id, None)
		if obj is not None:
			return obj

		pl = self._objs.get(id, None)
		if pl is None:
			return None
		pl = pl[0]

		self._data.seek(pl[0], 0)
		dump = self._data.read(pl[1])
		obj = pickle.loads(dump)

		self._objv[id] = obj;
		return obj

	def put(self, obj, id=None, cat=None, meta=None):
		if id is None:
			id = self._nextid()
		elif isinstance(id, int) and id < 0:
			raise Exception("Error: id can't be less then 0")
		else:
			self.out(id)

		return self._put(obj, id, cat, meta)

	def out(self, id):
		obj = self._objs.pop(id, None)
		if obj is None:
			return None;

		self._free(obj[0])

		val = self._objv.pop(id)
		self._cats[obj[1]].remove(id)
		return val

	def _put(self, obj, id, cat, meta):
		dump = pickle.dumps(obj)
		pl = self._malloc(len(dump))

		self._data.seek(pl[0], 0)
		self._data.write(dump)

		self._objs[id] = (pl, cat, meta);
		self._objv[id] = obj
		self._cats.setdefault(cat, set()).add(id)
		return



	def _free(self, pl):
		self._fpls.add(pl)

		l = r = None
		for fpl in self._fpls:
			if fpl[0] + fpl[1] == pl[0]:
				l = fpl
			elif pl[0] + pl[1] == fpl[0]:
				r = fpl

		if l is not None:
			self._fpls.remove(l)
			self._fpls.remove(pl)
			pl = (l[0], l[1] + pl[1])
			self._fpls.add(pl)

		if r is not None:
			self._fpls.remove(r)
			self._fpls.remove(pl)
			pl = (pl[0], pl[1] + r[1])
			self._fpls.add(pl)

		return

	def _malloc(self, s):
		best = None
		for el in self._fpls:
			if el[1] >= s and (best is None or el[1] < best[1]):
				best = el

		if best is None:
			raise Exception("memory out")

		self._fpls.remove(best)
		if s != best[1]:
			self._fpls.add( (best[0] + s, best[1] - s) )

		return (best[0], s)

	def _nextid(self):
		self.__dict__['_mnid'] = self._mnid - 1;
		return self._mnid + 1


	def __getattr__(self, attr):
		return self.get(attr)

	def __setattr__(self, attr, value):
		return self.put(value, id=attr)

	def __delattr__(self, attr):
		return self.out(attr)

	def __getitem__(self, item):
		return self._cats[item]





# END
