# tag.py





class Tag:
	'''
	name:    str     # название тега, собственно, сам тег
	parents: { Tag } # родительские теги теги
	childs:  { Tag } # дочерние теги
	'''

	def __init__(
		self,
		name:    str, *,
		parents  = set(),
		childs   = set()
	):
		self.name    = name
		self.parents = parents
		self.childs  = childs

	def ancestors(self):
		stack  = [ self ]
		result = set()

		while len(stack) != 0:
			cur = stack.pop()
			for parent in cur.parents:
				if result.add(parent):
					stack.append(parent)

		return result

	def tree(self, tab=''):
		result = tab + self.name + (':\n' if len(self.childs) != 0 else '')
		for child in self.childs:
			result += child.tree() + '\n'
		return result

	def __str__(self):
		return self.name

	def __repr__(self):
		return '<Tag: %s>' % self




def bind_tags(*, child: Tag, parent: Tag):
	child.parents.add(parent)
	parent.childs.add(child)





# END
