from numpy import *
import fm_model as modelfile
import fm_params as paramfile
import argparse
import timeit
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from plotdict import *
from scipy.integrate import odeint

# ARGUMENT PARSING AND MODEL CLASS
arg = argparse.ArgumentParser()
arg.add_argument('--freeparams',nargs='*') 
arg.add_argument('-s', action='store_true')
arg.add_argument('-b', action='store_true')
arg.add_argument('-m', action='store_true')
arg.add_argument('--name',nargs=1)
arg.add_argument('--solve',action='store_true')
arg.add_argument('--write',action='store_true')
arg.add_argument('--plot',nargs='*') 
args = arg.parse_args()

# Model class
class smclass:
   def __init__(self,initvals,testparams):
      paramfile.parameters(self,testparams,initvals)
   def model(self,t,y,*args):
      if args:
         return(modelfile.model(t,y,self,*args))
      else:
         return(modelfile.model(t,y,self))
         
         
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# SET PARAMETERS MANUALLY
#Initial values
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
CaCi0 = 0.1*1e-3 # Assumption based on Oschmann model
GluCi0 = 3 # From 'Maintaining the presynaptic glutamate...Marx, Billups...2015'
NaCe0 = 152
KCe0 = 3
ClCe0 = 135
CaCc0 = 1.8 # Oschmann
GluCc0 = 1*1e-4 # Attwell Barbour Szatkowski... Non vesicular release...'93 (Neuron) 
NaCg0 = 13
KCg0 = 80
ClCg0 = 35
CaCg0 = 0.05*1e-3 # From 'Plasmalemmal so/ca exchanger...Reyes et al...2012'
GluCg0 = 2 # Emperical assumption
Wi0 = 2
Wg0 = 1.7
VolPreSyn = 1*1e-3
VolPAP = 1*1e-3 # Emperical
Volc = 1*1e-3 # Emperical

# Free parameters
tstart = 20
tend = 80
blockerScaleAst =1;
blockerScaleNeuron  =1;
pumpScaleAst = 1;
pumpScaleNeuron = 1;
nkccScale = 10;
kirScale = 1
gltScale = 1
nka_na = 13
nka_k = 0.2
nkccblock_after = 0
kirblock_after = 0
alphae0 = 0.98
choicee = 0
astroblock = 0


#Fixed params
beta1 = 1.1;
beta2 = 1.1;
perc = 0.0

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Change parameters as per args
if args.freeparams:
    argdict = args.freeparams    
    for i in argdict:
        exec(i)
if args.s:
    alphae0 = 0.2
elif args.m:
    alphae0 = 0.5
elif args.b:
    alphae0 = 0.98

# Generate class instance
initvals = [NaCi0,KCi0,ClCi0,CaCi0,GluCi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,NaCg0,KCg0,\
ClCg0,CaCg0,GluCg0,Wi0,Wg0,VolPreSyn,VolPAP,Volc]
testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale,gltScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,alphae0,choicee,astroblock]
sm = smclass(initvals,testparams)
testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
'pumpScaleAst', 'pumpScaleNeuron', \
'nkccScale', 'kirScale','gltScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
initvallist =['NNai0','NKi0','NCli0','NNag0','NKg0','NClg0','Wi0','Wg0']

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# SOLVE ODE
initvals = [sm.NNai0,sm.NKi0,sm.NCli0,sm.m0,sm.h0,sm.n0,sm.NCai0,sm.NN0,sm.NR0,\
sm.NR10,sm.NR20,sm.NR30,sm.NF0,sm.NI0,sm.ND0,sm.NNag0,sm.NKg0,sm.NClg0,sm.NCag0,sm.Vpost0,sm.mAMPA0,sm.Wi0,sm.Wg0]

t0 = 0
tfinal = 170

def solver(t0,tfinal,initvals):
    mod = Explicit_Problem(sm.model, initvals, t0)
    sim = CVode(mod)
    sim.atol = 1e-9
    sim.rtol = 1e-9
    # sim.iter = 'Newton'
    # sim.discr = 'BDF'
    # sim.linear_solver = 'SPGMR'
    # sim.report_continuously = True
    # sim.verbosity = 10
    t, y = sim.simulate(tfinal)
    return t,y
    
def plotter(expname,fignum,t,y,*str):  
    plt.rc('font',size=20)
    plt.rc('axes',titlesize=20)
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=3)
    fig = plt.figure(fignum)
    ax = fig.add_subplot(111)
    plt.axvspan(sm.tstart, sm.tend, color='0.7', alpha=0.5, lw=0,label=r"OGD".format(d=(sm.perc*100)))
    for plotname in str[0]:
        t1 = array(t)
        ploty = sm.model(t1,y,plotname)
        if plotname in plotnamedict:
            plt.ylabel(r'{d}'.format(d=plotnamedict[plotname]))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotnamedict[plotname]))
        else:
            plt.ylabel(r'{d}'.format(d=plotname))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotname))
        plt.xlabel("t (min.)")
    plt.xlim(t0,tfinal)
    plt.title(r"Max pump strength $=$ {d}$\%$ of baseline".format(d=int(sm.model(array(t),y,'min(blockerExp)')*100)))
    plt.savefig(r'Images/%s_%s.png'%(expname,plotname),format='png')
    plt.legend()
    fig.tight_layout()
    
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


if args.solve:
    t,y = solver(t0,tfinal,initvals)
    V = sm.model(array(t),y,'V')
    
    if args.write:
        f = open('ExperimentResults.txt','r+')
        f.seek(0,2)
        f.write('Experiment: %s, V[0] = %2.3f, V[end] = %2.3f \n'%(args.name,V[0],V[-1]))
        f.close()
 
    if args.plot:
        ctr=1
        for i in args.plot:
            plotter(args.name,ctr,t,y,[i])
            ctr = ctr + 1
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
