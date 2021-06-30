import matplotlib.pyplot as plt





def fac(n):
	'Факториал'
	p = 1
	for i in range(2, n+1):
		p *= i
	return p


def P(k, n):
	'Число размещений k элементов из n'
	p = 1
	for i in range(k):
		p *= n - i
	return p


def C(k, n):
	'Число сочетаний k элементов из n'
	return P(k, n) // fac(k)


def plot(charts):
	fig, ax = plt.subplots()

	for x, y, label in charts:
		ax.plot(x, y, label=label)

	ax.set_xlabel('n')
	ax.set_ylabel('p')
	ax.set_title('Distributions')
	ax.legend()

	plt.figure(figsize=(3, 3))
	plt.show()





# END
