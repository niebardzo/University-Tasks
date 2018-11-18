import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

np.set_printoptions(threshold=np.nan)

DB = 0.00365665

a = 0.98
b= 0.63
g = 9.81
P = 1
Fin = 0.01
params = [a,b,g,P,DB,Fin]

tStop = 1000
tStart = 0.01
t = np.arange(0.,tStop,tStart)


volumeA = 5
volumeB = 1
tempB = 10

h0 = [volumeA,volumeB,tempB]


def tank(h,t,params, DA):
	"""Function defining the model to be solved by ODE"""
	a, b, g, P, DB, Fin = params
	Va,Vb,T = h
	try:
		dVa = -a*b*DA*math.sqrt(2*g*Va/P)
	except ValueError:
		dVa = 0
		Va = 0
	dVb = -a*b*DB*math.sqrt(2*g*Vb/P) - dVa + Fin
	dT = ((Fin)/Vb)*(10-T)-((dVa/Vb)*(90-T))
	delta = [dVa,dVb,dT]
	return delta


class Target:
	"""Class that has a coutner of target_function calls. And one method which is target function to be optimized."""
	def __init__(self):
		self.counter = 0

	def target_function(self,DA):
		solution = odeint(tank, h0, t, args=(params,DA))
		self.counter = self.counter + 1
		return abs(50-np.amax(solution))


def expansion(start, stop, expansion_factor, max_n):
	"""Implementation of Expantion method"""
	soln = Target()
	i = 0
	tab = [0 for i in range(max_n)]
	tab[0] = start
	tab[1] = stop
	if soln.target_function(tab[0]) == soln.target_function(tab[1]):
		return [tab[0],tab[1]], soln.counter
	if soln.target_function(tab[1]) > soln.target_function(tab[0]):
		tab[1] = - tab[1]
		if soln.target_function(tab[1]) >= soln.target_function(tab[0]):
			return [tab[1], - tab[1]], soln.counter
	while(True):
		if i >= max_n:
			raise ValueError
		i = i + 1
		tab[i+1] = expansion_factor**i * tab[1]
		if soln.target_function(tab[i]) <= soln.target_function(tab[i+1]):
			break
	if tab[i-1] < tab[i+1]:
		return [tab[i-1],tab[i+1]], soln.counter
	return [tab[i+1],tab[i-1]], soln.counter



def fib_rek(n):
	"""Return nth value of fibonaci"""
	if n < 1:
		return 0
	if n < 2:
		return 1
	return fib_rek(n - 1) + fib_rek(n - 2)


def fibonaci(x, epsilon):
	"""Implementation of Fibonaci method"""
	print("Fibonaci:")
	soln = Target()
	a, b = x
	k = 1
	while fib_rek(k) <= (b-a)/epsilon:
		k = k+1
	tab_a = [0 for j in range(k-2)]
	tab_b = [0 for j in range(k-2)]
	tab_c = [0 for j in range(k-2)]
	tab_d = [0 for j in range(k-2)]
	tab_a[0] = a
	tab_b[0] = b
	tab_c[0] = tab_b[0] - (fib_rek(k-1)*(tab_b[0]-tab_a[0])/fib_rek(k))
	tab_d[0] = tab_a[0] + tab_b[0] - tab_c[0]
	for i in range(k-3):
		print(i,",",tab_b[i]-tab_a[i])
		if soln.target_function(tab_c[i]) < soln.target_function(tab_d[i]):
			tab_a[i+1] = tab_a[i]
			tab_b[i+1] = tab_d[i]
		else:
			tab_b[i+1] = tab_b[i]
			tab_a[i+1] = tab_c[i]
		tab_c[i+1] = tab_b[i+1] - (fib_rek(k-i-2)*(tab_b[i+1]-tab_a[i+1])/fib_rek(k-i-1))
		tab_d[i+1] = tab_a[i+1] + tab_b[i+1] - tab_c[i+1]
	return tab_c[k-3], soln.counter



def lagrande(x, epsilon, max_n):
	"""Implementation of Lagrande method."""
	print("Lagrande :")
	soln = Target()
	a,b = x
	c = (a+b)/2
	gamma = epsilon/100
	i = 0
	tab_a = [0 for j in range(max_n)]
	tab_a[0] = a
	tab_b = [0 for j in range(max_n)]
	tab_b[0] = b
	tab_c = [0 for j in range(max_n)]
	tab_c[0] = c
	tab_d = [0 for j in range(max_n)]
	while(True):
		tab_d[i] = (1/2) * (
				(soln.target_function(tab_a[i])*(tab_c[i]**2-tab_b[i]**2)
				+soln.target_function(tab_c[i])*(tab_b[i]**2-tab_a[i]**2)
				+soln.target_function(tab_b[i])*(tab_a[i]**2-tab_c[i]**2)
				)
				/
				(soln.target_function(tab_a[i])*(tab_c[i]-tab_b[i])
				+soln.target_function(tab_c[i])*(tab_b[i]-tab_a[i])
				+soln.target_function(tab_b[i])*(tab_a[i]-tab_c[i]))
				)
		if tab_a[i] < tab_d[i] < tab_c[i]:
			if soln.target_function(tab_d[i]) < soln.target_function(tab_c[i]):
				tab_a[i+1] = tab_a[i]
				tab_c[i+1] = tab_d[i]
				tab_b[i+1] = tab_c[i]
			else:
				tab_a[i+1] = tab_d[i]
				tab_c[i+1] = tab_c[i]
				tab_b[i+1] = tab_b[i]
		else:
			if tab_c[i] < tab_d[i] < tab_b[i]:
				if soln.target_function(tab_d[i]) < soln.target_function(tab_c[i]):
					tab_a[i+1] = tab_c[i]
					tab_c[i+1] = tab_d[i]
					tab_b[i+1] = tab_b[i]
				else:
					tab_a[i+1] = tab_a[i]
					tab_c[i+1] = tab_c[i]
					tab_b[i+1] = tab_d[i]
			else:
				# nie zbiezny
				return [0, soln.counter]
		print(i,",",tab_b[i]-tab_a[i])
		i = i + 1
		if i > max_n:
			# nie ma rozwiazania
			return [0, soln.counter]
		#print(tab_a[:i+1],tab_b[:i+1],tab_c[:i+1],tab_d[:i+1])
		if tab_b[i] - tab_a[i] < epsilon or abs(tab_d[i] - tab_d[i-1]) <= gamma:
			break
	return [tab_d[i-1] , soln.counter]



N_max = 100
exp1 = random.random() * 10
exp2 = random.random() * 10
exp3 = random.random() * 10

exp = [exp1,exp2,exp3]

soln = Target()

with open('results.csv', 'w') as csvfile:
	fieldnames = ['e','x0', 'n_e', 'a', 'b', 'x_f','y_f','n_f', 'x_l','y_l','n_l']
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
	for e in exp:
		for i in range(100):
			x0 = random.random()/1000
			x = expansion(0, x0,e, N_max)
			#print("Expansion: " ,x)
			f = fibonaci(x[0], 0.001)
			f_val = soln.target_function(f[0])
			#print("Fib: ",f)
			l = lagrande(x[0],0.001,N_max)
			if l[0] == 0:
				l_val = 0
			else:
				l_val = soln.target_function(l[0])
			#print("lagrande: ",l)
			writer.writerow({'e':e,
							'x0': x0,
							'n_e': x[1],
							'a': x[0][0],
							'b': x[0][1],
							'x_f': f[0],
							'y_f': f_val,
							'n_f': f[1],
							'x_l': l[0],
							'y_l': l_val,
							'n_l': l[1]
							})
	
	print("!!!!!!!!!!!!!!Start!!!!!!!!!!!!!!!")
	f = fibonaci([0.0001,0.01], 0.001)
	f_val = soln.target_function(f[0])
	#print("Fib: ",f)
	l = lagrande([0.0001,0.01],0.001,N_max)
	if l[0] == 0:
		l_val = 0
	else:
		l_val = soln.target_function(l[0])
	writer.writerow({'e':0,
					'x0': 0,
					'n_e': 0,
					'a': 0,
					'b': 0,
					'x_f': f[0],
					'y_f': f_val,
					'n_f': f[1],
					'x_l': l[0],
					'y_l': l_val,
					'n_l': l[1]
					})




soln = odeint(tank, h0, t, args=(params,0.01))


# Plot results
fig = plt.figure(1, figsize=(8,8))

# Plot volume as a function of time
ax2 = fig.add_subplot(311)
ax2.plot(t, soln[:,0])
ax2.set_xlabel('time')
ax2.set_ylabel('VolumeA')


# Plot volume as a function of time
ax2 = fig.add_subplot(312)
ax2.plot(t, soln[:,1])
ax2.set_xlabel('time')
ax2.set_ylabel('VolumeB')

# Plot temp as a function of time
ax1 = fig.add_subplot(313)
ax1.plot(t, soln[:,2])
ax1.set_xlabel('time')
ax1.set_ylabel('Temp')


plt.tight_layout()
plt.show()