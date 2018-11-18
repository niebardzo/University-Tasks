import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

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
			return [0,0]
		i = i + 1
		tab[i+1] = expansion_factor**i * tab[1]
		if target_function(tab[i]) <= target_function(tab[i+1]):
			break
	if tab[i-1] < tab[i+1]:
		return [tab[i-1],tab[i+1]]
	return [tab[i+1],tab[i-1]]



def fibonaci():
	pass


def lagrande():
	pass


print(expansion(0,0.001,1.1,1000))



soln = odeint(tank, h0, t, args=(params,0.05))


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