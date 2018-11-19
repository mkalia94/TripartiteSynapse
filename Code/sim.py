# Runs on Python 3.x or higher.
# Dependencies: assimulo, numpy, matplotlib
# There are 4 files: sm_params: Contains function that calculates parameters based on baseline values and free parameters
#                    sm_model: Contains function that defines the function
#                    sm_class: Generates class which includes model, parameters in one instance
#                    sim: t,y = solver(t0,tfinal,initvals) solves the ODE from t=t0 to t=tfinal
#                         plotter(t,y,'term') plots 'term', for example, plotter(t,y,'KCe') plots extracellular concentrations
#                         saveparams() saves the current parameters and initial values in one table, in one figure

from numpy import *
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from plotdict import *
from sm_class import *

t0 = 0
tfinal = 70


def solver(t0,tfinal,initvals):
    mod = Explicit_Problem(sm.model, initvals, t0)
    sim = CVode(mod)
    sim.atol = 1e-12
    sim.rtol = 1e-12
    sim.iter = 'Newton'
    sim.linear_solver = 'SPGMR'
    t, y = sim.simulate(tfinal)
    return t,y
    
def plotter(t,y,*str):  
    p=plt.axvspan(sm.tstart, sm.tend, color='0.7', alpha=0.5, lw=0,label=r"{d}$\%$ of baseline NKA".format(d=sm.perc))
    for plotname in str:
        t1 = array(t)
        ploty = sm.model(t1,y,plotname)
        
        if plotname in plotnamedict:
            plt.ylabel(r'{d}'.format(d=plotnamedict[plotname]))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotnamedict[plotname]))
        else:
            plt.ylabel(r'{d}'.format(d=plotname))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotname))
        plt.xlabel("t (min.)")
    plt.savefig(r'Images/{d}.eps'.format(d=plotname),format='eps')
    plt.legend()
    plt.show()
    
def plotall(t,y):
    ctr = 0
    for str in ['KCe','NaCi','NaCg']:
        plt.figure(ctr)
        plotter(t,y,str)
        ctr += 1
    
def saveparams():
    fig,ax = plt.subplots(1,2)
    fig.subplots_adjust(wspace=1.2)
    ax[0].table(cellText = reshape(array(initvals),(8,1)),
                rowLabels = initvallist,
                colLabels = ['Initial values'],
                loc = "center")
    ax[0].axis("off")      
    ax[1].table(cellText = reshape(array(testparams),(11,1)),
              rowLabels = testparamlist,
              colLabels = ['Test parameters'],
              loc = "center")
    ax[1].axis("off")
    plt.show()
    plt.savefig(r'Images/{d}.eps'.format(d='parameters'),format='eps')