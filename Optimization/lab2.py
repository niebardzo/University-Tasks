import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
from numpy import linalg as LA
from scipy.optimize import minimize

np.set_printoptions(threshold=np.nan)

mr =1
mc = 10
l =0.5
b= 0.5
a_ref = 3.14
o_ref = 0
I = (1/3)*mr*(l**2)+mc*(l**2)

params = [b, I, a_ref, o_ref]

tStop = 5
tStart = 0.01
t = np.arange(0.,tStop,tStart)

h0 = [0,0]


def robot(h,t,params,k1,k2):
	alfa, omega = h
	b, I, a_ref, o_ref = params
	M = k1*(a_ref-alfa)+k2*(o_ref- omega)
	dalfa = omega
	domega = (M-b*omega)/I
	derivs = [dalfa,domega]
	return derivs


def ortonormalization(vs, lamd):
	Q = np.matmul(vs, [[lamd[0],0],[lamd[1],lamd[1]]])
	d1 = np.divide(Q[0],LA.norm(Q[0],2))
	d2 = np.divide((Q[1] - np.multiply(np.dot(Q[0],d1),d1)),(LA.norm((Q[1] - np.multiply(np.dot(Q[0],d1),d1)),2)))
	versors = [d1,d2]
	return versors


class Solution:
	"""Class that has a coutner of target_function calls. And one method which is target function to be optimized."""
	def __init__(self):
		self.counter = 0

	def target_function(self,x):
		k1,k2 = x
		solution = odeint(robot, h0, t, args=(params,k1,k2))
		Q = 0
		for alfa, omega in solution:
			M = k1*(a_ref-alfa)+k2*(o_ref- omega)
			Q = Q + (10*(a_ref-alfa)**2)+(o_ref - omega)**2 + M**2
		self.counter = self.counter + 1
		return Q * 0.05


	def hook_jeeves(self, x, s, alfa, epsilon):
		self.counter = 0
		"""Hooks Jeeves"""
		while True:
			base_x = x
			x = self.try_hook_jeeves(base_x, s)
			if self.target_function(x) < self.target_function(base_x):
				while True:
					previous_base_x = base_x
					base_x = x
					x = [2*base_x[0]-previous_base_x[0], 2*base_x[1]-previous_base_x[1]]
					x = self.try_hook_jeeves(x,s)
					if self.target_function(x) >= self.target_function(base_x):
						break
				x = base_x
			else:
				s = alfa * s
			if s < epsilon:
				break
		return base_x


	def try_hook_jeeves(self, x,s):
		"""Hooks Jeeves try"""
		e = 0.1
		if self.target_function([x[0]+s*e,x[1]]) < self.target_function(x):
			x = [x[0]+s*e,x[1]]
		else:
			if self.target_function([x[0]-s*e,x[1]]) < self.target_function(x):
				x = [x[0]-s*e,x[1]]

		if self.target_function([x[0],x[1]+s*e]) < self.target_function(x):
			x = [x[0],x[1]+s*e]
		else:
			if self.target_function([x[0],x[1]-s*e]) < self.target_function(x):
				x = [x[0],x[1]-s*e]
		return x


	def rosenbrock(self, x, s, alpha, beta):
		self.counter = 0
		lambd = [0,0]
		next_lambd = [0,0]
		p = [0,0]
		next_p = [0,0]
		es = [s,s]
		next_es = [s,s]
		base_x = x
		versory = [[1.,0.],[0.,1.]]
		j = 0
		while j <= 200:
			for i in range(len(x)):
				if self.target_function([base_x[0] + es[i]*versory[i][0], base_x[1] + es[i]*versory[i][1]]) < self.target_function(base_x):
					base_x = [base_x[0] + es[i]*versory[i][0], base_x[1] + es[i]*versory[i][1]]
					next_lambd[i] = lambd[i] + es[i]
					next_es[i] = alpha* es[i]
				else:
					next_es[i] = - beta * es[i]
					next_p[i] = p[i] + 1

			j = j + 1
			x = base_x
			if (next_lambd[0] != 0 and next_p[0] != 0):
				versory[0] = ortonormalization(versory, next_lambd)[0]
				lambd[0] = 0
				next_lambd[0] = 0
				p[0] = 0
				next_p[0] = 0
				es[0] = s
				next_es[0] = s
			elif (next_lambd[1] != 0  and next_p[1] != 0):
				versory[1] = ortonormalization(versory, next_lambd)[1]
				lambd[1] = 0
				next_lambd[1] = 0
				p[1] = 0
				next_p[1] = 0
				es[1] = s
				next_es[1] = s
		return x


	def powell(self, x0):
		"""Powel optimization"""
		return minimize(self.target_function, x0, method='Powell')


	def nelmeda(self, x0):
		return minimize(self.target_function, x0, method='Nelder-Mead')




#
# Saving to file
#


exp1 = random.random() * 10
exp2 = random.random() * 10
exp3 = random.random() * 10
alpha = 1e-3
epsi = 0.01
exp = [exp1,exp2,exp3]

with open('results.csv', 'w') as csvfile:
	fieldnames = ['e','k10', 'k20', 'k1hj', 'k2hj', 'Qhj','nhj','k1r', 'k2r', 'Qr','nr','k1nm', 'k2nm', 'Qnm','nnm']
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
	writer.writeheader()
	for e in exp:
		for i in range(100):
			k10 = random.random() * 10
			k20 = random.random() * 10
			k0 = [k10,k20]

			print("k0: ", k0)
			soln = Solution()

			hok_jev = soln.hook_jeeves(k0, e, alpha, epsi)
			hok_jev_val = soln.target_function(hok_jev)
			hok_jev_n = soln.counter - 1
			rosen = soln.powell(k0)
			nel = soln.nelmeda(k0)

			writer.writerow({'e':e,
							'k10': k10,
							'k20': k20,
							'k1hj': hok_jev[0], 
							'k2hj': hok_jev[1], 
							'Qhj': hok_jev_val,
							'nhj': hok_jev_n,
							'k1r':rosen.x[0], 
							'k2r':rosen.x[1], 
							'Qr':rosen.fun,
							'nr':rosen.nfev,
							'k1nm':nel.x[0], 
							'k2nm':nel.x[1],
							'Qnm':nel.fun,
							'nnm':nel.nfev
							})
	


#
# Test Case:
#


tStop = 20
tStart = 0.0001
t = np.arange(0.,tStop,tStart)

def target_function(x):
	k1,k2 = x
	solution = odeint(robot, h0, t, args=(params,k1,k2))
	Q = 0
	Q_overtime = []
	for alfa, omega in solution:
		M = k1*(a_ref-alfa)+k2*(o_ref- omega)
		Q_overtime.append(Q)
		Q = Q + (10*(a_ref-alfa)**2)+(o_ref - omega)**2 + M**2
		#print(Q*0.05)
	Q = Q * 0.05
	return Q_overtime
	#return Q

self = odeint(robot, h0, t, args=(params,2.7,3.18))

# Plot results
fig = plt.figure(1, figsize=(8,8))

ax1 = fig.add_subplot(311)
ax1.plot(t, self[:,0])
ax1.set_xlabel('time')
ax1.set_ylabel('delta-Alfa')


ax2 = fig.add_subplot(312)
ax2.plot(t, self[:,1])
ax2.set_xlabel('time')
ax2.set_ylabel('delta-omega')


ax3 = fig.add_subplot(313)
ax3.plot(t, target_function([2.7,3.18]))
ax3.set_xlabel('time')
ax3.set_ylabel('Q')


plt.tight_layout()
plt.show()

#print(hook_jeeves([2.7,3.18],1,1e-3,0.5))
#print(hook_jeeves([3.2,3.68],1,1e-3,0.5))