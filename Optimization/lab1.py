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


def target_function(DA):
	solution = odeint(tank, h0, t, args=(params,DA))
	return abs(50-np.amax(solution))


def expansion(start, stop, expansion_factor, max_n):
	i = 0
	tab = [0 for i in range(max_n)]
	tab[0] = start
	tab[1] = stop
	if target_function(tab[0]) == target_function(tab[1]):
		return [tab[0],tab[1]]
	if target_function(tab[1]) > target_function(tab[0]):
		tab[1] = - tab[1]
		if target_function(tab[1]) >= target_function(tab[0]):
			return [tab[1], - tab[1]]
	while(True):
		if i >= max_n:
			raise ValueError
		i = i + 1
		tab[i+1] = expansion_factor**i * tab[1]
		if target_function(tab[i]) <= target_function(tab[i+1]):
			break
	if tab[i-1] < tab[i+1]:
		return [tab[i-1],tab[i+1]]
	return [tab[i+1],tab[i-1]]



def fib_rek(n):
	"""Return nth value of fibonaci"""
	if n < 1:
		return 0
	if n < 2:
		return 1
	return fib_rek(n - 1) + fib_rek(n - 2)


def fibonaci(x, epsilon):
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
		if target_function(tab_c[i]) < target_function(tab_d[i]):
			tab_a[i+1] = tab_a[i]
			tab_b[i+1] = tab_d[i]
		else:
			tab_b[i+1] = tab_b[i]
			tab_a[i+1] = tab_c[i]
		tab_c[i+1] = tab_b[i+1] - (fib_rek(k-i-2)*(tab_b[i+1]-tab_a[i+1])/fib_rek(k-i-1))
		tab_d[i+1] = tab_a[i+1] + tab_b[i+1] - tab_c[i+1]
	return tab_c[k-3]



def lagrande(x, epsilon, max_n):
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
				(target_function(tab_a[i])*(tab_c[i]**2-tab_b[i]**2)
				+target_function(tab_c[i])*(tab_b[i]**2-tab_a[i]**2)
				+target_function(tab_b[i])*(tab_a[i]**2-tab_c[i]**2)
				)
				/
				(target_function(tab_a[i])*(tab_c[i]-tab_b[i])
				+target_function(tab_c[i])*(tab_b[i]-tab_a[i])
				+target_function(tab_b[i])*(tab_a[i]-tab_c[i]))
				)
		if tab_a[i] < tab_d[i] < tab_c[i]:
			if target_function(tab_d[i]) < target_function(tab_c[i]):
				tab_a[i+1] = tab_a[i]
				tab_c[i+1] = tab_d[i]
				tab_b[i+1] = tab_c[i]
			else:
				tab_a[i+1] = tab_d[i]
				tab_c[i+1] = tab_c[i]
				tab_b[i+1] = tab_b[i]
		else:
			if tab_c[i] < tab_d[i] < tab_b[i]:
				if target_function(tab_d[i]) < target_function(tab_c[i]):
					tab_a[i+1] = tab_c[i]
					tab_c[i+1] = tab_d[i]
					tab_b[i+1] = tab_b[i]
				else:
					tab_a[i+1] = tab_a[i]
					tab_c[i+1] = tab_c[i]
					tab_b[i+1] = tab_d[i]
			else:
				print("Algorytm nie jest zbiezny.")
				raise ValueError
		i = i + 1
		if i > max_n:
			print("Nie udało się osiągnąć dokładności epsilon.")
			raise ValueError
		#print(tab_a[:i+1],tab_b[:i+1],tab_c[:i+1],tab_d[:i+1])
		if tab_b[i] - tab_a[i] < epsilon or abs(tab_d[i] - tab_d[i-1]) <= gamma:
			break
	return tab_d[i-1]



N_max = 100
eps1 = random.random() / 100
eps2 = random.random() / 100
eps3 = random.random() / 100


print(expansion(0,0.001,1.1,100))
print(fibonaci([0.0000001,0.01],0.001))
print(lagrande([0.0000001,0.01],0.001,100))


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