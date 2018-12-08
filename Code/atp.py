from numpy import *
from scipy import io
import matplotlib.pyplot as plt
mat = io.loadmat('Data/atp.mat')
tatp = mat['tatp']
atp = mat['atp']
plt.figure()
plt.plot(tatp.T,atp)
t = linspace(0,30,500)
perc = 0.65
tstart = 5.7
tend = 7.4
beta1 = 0.9
beta2 = 0.6
blockerExp = 1/(1+exp(beta1*(t-tstart))) + 1/(1+exp(-beta2*(t-tend)))
blockerExp = perc + (1-perc)*blockerExp
plt.plot(t,blockerExp)
plt.show()