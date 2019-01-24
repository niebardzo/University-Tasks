import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
from numpy import linalg as LA
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

np.set_printoptions(threshold=np.nan)


class Solution:
	"""Class that has a coutner of target_function calls. And one method which is target function to be optimized."""
	def __init__(self):
		self.counter = 0

	def target_function(self,x):
		self.counter = self.counter + 1
		x1, x2 = x
		return (x1**2+x2**2-math.cos(2.5*3.1415*x1)-math.cos(2.5*3.1415*x2)+2)


	def golden(self, x, epsilon, max_n):
		"""Golden Division"""
		self.counter = 0
		i = 0
		alpha = (math.sqrt(5) - 1 )/2
		a,b = x
		if a > b:
			return 0
		tab_a = [0 for j in range(max_n)]
		tab_a[0] = a
		tab_b = [0 for j in range(max_n)]
		tab_b[0] = b
		tab_c = [0 for j in range(max_n)]
		tab_c[0] = tab_b[0] - alpha * (tab_b[0] - tab_a[0])
		tab_d = [0 for j in range(max_n)]
		tab_d[0] = tab_a[0] + alpha * (tab_b[0] - tab_a[0])
		while True:
			if self.target_function(tab_c[i]) < self.target_function(tab_d[i]):
				tag_a[i+1] = tab_a[i]
				tab_b[i+1] = tab_d[i]
				tab_d[i+1] = tab_c[i]
				tab_c[i+1] = tab_b[i+1] - alpha * (tab_b[i+1] - tab_a[i+1])
			else:
				tag_a[i+1] = tab_c[i]
				tab_b[i+1] = tab_b[i]
				tab_d[i+1] = tab_a[i] + alpha * (tab_b[i+1] - tab_a[i+1])
				tab_c[i+1] = tab_d[i+1]
			i = i + 1
			if i > max_n:
				return 0
			if tab_b[i] - tab_a[i] < epsilon:
				break
		return (tab_a[i] + tab_b[i])/2 


	def methods(self, x0, epsilon, n_max):
		i =0
		x = [0 for j in range(max_n)]
		x[0] = x0
		while True:
			d = numpy.gradient(self.target_function, x0)
			h = get_h(self.target_function ,x0)
			x[i+1] = x[i] + h * d[i]
			i = i + 1
			if ortonalization(x[i]. x[i-1]) < epsilon:
				return x[i]

			if i > n_max:
				break
		return 0



	def steps(self, x0, step=0):
		"""Steps optimization"""
		if step == 0:
			return minimize(self.target_function, x0, method='BFGS')
		return minimize(self.target_function, x0, method='BFGS', options={'eps': step})


	def newton(self, x0, step=0):
		"""Steps optimization"""
		if step == 0:
			return minimize(self.target_function, x0, method='L-BFGS-B')
		return minimize(self.target_function, x0, method='L-BFGS-B', options={'eps': step})


	def cg(self, x0, step=0):
		"""Step CG method"""
		if step == 0:
			return minimize(self.target_function, x0, method='CG')
		return minimize(self.target_function, x0, method='CG', options={'eps': step})

#
# Saving to file
#


with open('results.csv', 'w') as csvfile:
	fieldnames = ['x1','x2', 'step', 'x1s', 'x2s', 'ys','fs','gs', 'x1cg', 'x2cg','ycg','fcg', 'gcg', 'x1n', 'x2n','yn','fn', 'gn']
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
	writer.writeheader()

	for i in range(100):
		x1 = random.random() * 10
		x2 = random.random() * 10
		x = [x1,x2]

		print("x0: ", x)
		soln = Solution()

		steps_1 = soln.steps(x, 0.05)
		cg_1 = soln.cg(x, 0.05)
		new_1 = soln.newton(x, 0.05)

		steps_2 = soln.steps(x, 0.12)
		cg_2 = soln.cg(x, 0.12)
		new_2 = soln.newton(x, 0.12)

		steps_3 = soln.steps(x)
		cg_3 = soln.cg(x)
		new_3 = soln.newton(x)
		print(new_3)

		writer.writerow({'x1':x1,
						'x2': x2,
						'step': 0.05,
						'x1s': steps_1.x[0], 
						'x2s': steps_1.x[1], 
						'ys': steps_1.fun,
						'fs': steps_1.nfev,
						'gs': steps_1.njev, 
						'x1cg': cg_1.x[0], 
						'x2cg': cg_1.x[1],
						'ycg': cg_1.fun,
						'fcg': cg_1.nfev, 
						'gcg': cg_1.njev,
						'x1n': new_1.x[0],
						'x2n': new_1.x[1],
						'yn': new_1.fun,
						'fn': new_1.nfev,
						'gn': cg_1.njev
						})

		writer.writerow({'x1':x1,
						'x2': x2,
						'step': 0.12,
						'x1s': steps_2.x[0], 
						'x2s': steps_2.x[1], 
						'ys': steps_2.fun,
						'fs': steps_2.nfev,
						'gs': steps_2.njev, 
						'x1cg': cg_2.x[0], 
						'x2cg': cg_2.x[1],
						'ycg': cg_2.fun,
						'fcg': cg_2.nfev, 
						'gcg': cg_2.njev,
						'x1n': new_2.x[0],
						'x2n': new_2.x[1],
						'yn': new_2.fun,
						'fn': new_2.nfev,
						'gn': cg_2.njev
						})

		writer.writerow({'x1':x1,
						'x2': x2,
						'step': 'Changing',
						'x1s': steps_3.x[0], 
						'x2s': steps_3.x[1], 
						'ys': steps_3.fun,
						'fs': steps_3.nfev,
						'gs': steps_3.njev, 
						'x1cg': cg_3.x[0], 
						'x2cg': cg_3.x[1],
						'ycg': cg_3.fun,
						'fcg': cg_3.nfev, 
						'gcg': cg_3.njev,
						'x1n': new_3.x[0],
						'x2n': new_3.x[1],
						'yn': new_3.fun,
						'fn': new_3.nfev,
						'gn': cg_3.njev
						})
