import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
from numpy import linalg as LA
from scipy.optimize import minimize, differential_evolution
from mpl_toolkits.mplot3d import Axes3D

np.set_printoptions(threshold=np.nan)


class Solution:
	"""Class that has a coutner of target_function calls. And one method which is target function to be optimized."""
	def __init__(self):
		self.counter = 0

	def target_function(self,x):
		self.counter = self.counter + 1
		x1, x2 = x
		return (x1**2+x2**2-math.cos(2.5*math.pi*x1)-math.cos(2.5*math.pi*x2) + 2)


	def evolution(self, mutation):
		"""Steps optimization"""
		return differential_evolution(self.target_function, [(-1,1), (-1,1)], mutation=mutation, init='random')
		
#
# Saving to file
#
omegs = [0.01,0.1,1,10,100]

with open('results.csv', 'w') as csvfile:
	fieldnames = ['omega','x1', 'x2', 'y', 'f', 'minimum']
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
	writer.writeheader()
	for omega in omegs:
		for i in range(100):

			soln = Solution()
			genetics = soln.evolution(omega/100)
			print(genetics)
			if abs(genetics.fun) < 0.001:
				minimum = 'yes'
			else:
				minimum = 'no'

			writer.writerow({'omega': omega,
							'x1': genetics.x[0],
							'x2': genetics.x[1],
							'y': genetics.fun, 
							'f': genetics.nfev, 
							'minimum': minimum
							})