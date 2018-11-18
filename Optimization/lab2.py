import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


mr =1
mc = 10
l =0.5
b= 0.5
a_ref = 3.14
o_ref = 0
I = (1/3)*mr*(l**2)+mc*(l**2)

params = [b, I, a_ref, o_ref]

tStop = 10
tStart = 0.05
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


def target_function(x):
	k1,k2 = x
	solution = odeint(robot, h0, t, args=(params,k1,k2))
	Q = 0
	for alfa, omega in solution:
		M = k1*(a_ref-alfa)+k2*(o_ref- omega)
		Q = Q + (10*(a_ref-alfa)**2)+(o_ref - omega)**2 + M**2
	Q = Q * 0.05
	print(Q)
	return Q



def hook_jeeves(x, s, alfa, epsilon):
	"""Hooks Jeeves"""
	while s > epsilon:
		base_x = x
		x = try_hook_jeeves(base_x, s, epsilon, len(base_x))
		if target_function(x) < target_function(base_x):
			while target_function(x) <= target_function(base_x):
				previous_base_x = base_x
				base_x = x
				x = [i-j for i,j in [[[2*i for i in base_x][0],previous_base_x[0]],[[2*i for i in base_x][1],previous_base_x[1]]]]
				x = try_hook_jeeves(x,s, epsilon,1)
			x = base_x
		else:
			s = alfa * s
	return base_x


def try_hook_jeeves(x,s, e, n):
	"""Hooks Jeeves"""
	for j in range(n):
		if target_function([i+s*e**j for i in x]) < target_function(x):
			x = [k + s*e**j for k in x]
		else:
			if target_function([i-s*e**j for i in x]) < target_function(x):
				x = [k - s*e**j for k in x]
	return x


#
# Test Case:
#


print(hook_jeeves([2.7,3.18],1,1e-3,0.5))