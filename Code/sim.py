from numpy import *
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from sm_class import *

t0 = 0
tfinal = 50

mod = Explicit_Problem(sm.model, initvals, t0)
sim = CVode(mod)

def solver():
    sim.atol = 1e-12
    sim.rtol = 1e-12
    sim.iter = 'Newton'
    sim.linear_solver = 'SPGMR'

    t, y = sim.simulate(tfinal)
    return t,y
    
def plotter(t,y,*str):   
    for plotname in str:
        t1 = array(t)
        ploty = sm.model(t1,y,plotname)
        p=plt.axvspan(sm.tstart, sm.tend, color='0.7', alpha=0.5, lw=0,label="{d} of baseline NKA".format(d=sm.perc))
        plt.legend()
        plt.ylabel(r'{d}'.format(d=plotname))
        plt.xlabel("t (min.)")
        plt.plot(t1,ploty)
        plt.savefig(r'Images/{d}.eps'.format(d=plotname),format='eps')
        plt.show()
    
def plotall(t,y):
    plotter(t,y,'KCe')
    plotter(t,y,'NaCe')
    plotter(t,y,'NaCg')
    
