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
import scipy.io as sio
import json


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
arg.add_argument('--block',type=json.loads)
arg.add_argument('--excite',nargs=2,type=float)
arg.add_argument('--astblock',nargs=2,type=float)
args = arg.parse_args()

# Model class
class smclass:
   def __init__(self,initvals,testparams):
      paramfile.parameters(self,testparams,initvals)
   def model(self,t,y,**args):
      if args:
        return(modelfile.model(t,y,self,**args))
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
GluCg0 = 2 # Empirical assumption
Wi0 = 2
Wg0 = 1.7
VolPreSyn = 1*1e-3
VolPAP = 1*1e-3 # Empirical
Volc = 1*1e-3 # Empirical

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

t0 = 0
tfinal = 170

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
initvals_temp = [NaCi0,KCi0,ClCi0,CaCi0,GluCi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,NaCg0,KCg0,\
ClCg0,CaCg0,GluCg0,Wi0,Wg0,VolPreSyn,VolPAP,Volc]
testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale,gltScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,alphae0,choicee,astroblock]
sm = smclass(initvals_temp,testparams)
testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
'pumpScaleAst', 'pumpScaleNeuron', \
'nkccScale', 'kirScale','gltScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
initvallist =['NNai0','NKi0','NCli0','NNag0','NKg0','NClg0','Wi0','Wg0']



## SOLVE ODE
initvals = [sm.NNai0,sm.NKi0,sm.NCli0,sm.m0,sm.h0,sm.n0,sm.NCai0,sm.NN0,sm.NR0,\
sm.NR10,sm.NR20,sm.NR30,sm.NF0,sm.NI0,sm.ND0,sm.NNag0,sm.NKg0,sm.NClg0,sm.NCag0,sm.Vpost0,sm.mAMPA0,sm.Wi0,sm.Wg0]
    
def modelfunc(t,y,*retvar):
    if retvar:
        return sm.model(t,y,block = args.block, excite = args.excite, astblock = args.astblock, ret = retvar[0])
    else:
        return sm.model(t,y,block = args.block, excite = args.excite, astblock = args.astblock, ret = None)
        
    

def solver(t0,tfinal,initvals):
    mod = Explicit_Problem(modelfunc, initvals, t0)
    sim = CVode(mod)
    sim.atol = 1e-11
    sim.rtol = 1e-11
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
    plt.axvspan(sm.tstart, sm.tend, color='0.7', alpha=0.5, lw=0,label=r"ED: {d}%".format(d=int(modelfunc(array(t),y,'1-min(blockerExp)')*100)))
    if args.excite:
        val = args.excite
        plt.axvspan(val[0], val[1], color='red', alpha=0.5, lw=0,label='Neuron excited')
    if args.astblock:
        val = args.astblock
        plt.axvspan(val[0], val[1], color='orange', alpha=0.5, lw=0,label='Ast. blocked')    
    if args.block:
        dict = args.block
        for key in dict:
                val = dict[key]
                if key in plotnamedict:
                    plt.axvspan(val[0], val[1], color='forestgreen', alpha=0.5, lw=0,label=r"{a}".format(a=plotnamedict[key]))
                else:
                     plt.axvspan(val[0], val[1], color='forestgreen', alpha=0.5, lw=0,label=r"{a}".format(a=key))   
    for plotname in str[0]:
        t1 = array(t)
        ploty = modelfunc(t1,y,plotname)
        if plotname in plotnamedict:
            plt.ylabel(r'{d}'.format(d=plotnamedict[plotname]))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotnamedict[plotname]))
        else:
            plt.ylabel(r'{d}'.format(d=plotname))
            plt.plot(t1,ploty,label = r"{d}".format(d=plotname))
        plt.xlabel("t (min.)")
    plt.xlim(t0,tfinal)
    
    fig.tight_layout()
    plotfilename = 'Images/{a}_{b}.pdf'.format(a=expname[0],b=plotname)
    plt.legend()
    plt.savefig(plotfilename,format='pdf',bbox_inches='tight')

    
    
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
    V = modelfunc(array(t),y,'V')
    
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

## SAVE DICTIONARY

dict = {'C':sm.C,
        'F' : sm.F,     # Faraday's constant
        'R' : sm.R,        # Gas constant
        'T' : sm.T,            # Temperature
        'PNaG' : sm.PNaG,        # permeability of gated Na current
        'PKG' : sm.PKG,      # permbeability of gated K current
        'PClG' : sm.PClG,      # permeability of gated Cl current
        'UKCl' : sm.UKCl,       # flux rate of KCl cotransporter
        'LH20i' : sm.LH20i,       # Osmotic permeability in the neuron
        'Qpump' : sm.Qpump,
        'Cg' : sm.Cg,               # Astrocyte membrane capacitance
        'Vg0' : sm.Vg0,            # Fix initial glial membrane potential
        'Vi0' : sm.Vi0,           # Fix initial neuronal membrane potential
        'KCe_thres' : sm.KCe_thres,        # Kir: Threshold for Kir gate
        'kup2' : sm.kup2,     # Kir: Rate of transition from low uptake to high uptake
        'PCaG' : sm.PCaG, # (from Naomi)
        'kNCXi' : sm.kNCXi, # 1/10th of NKA strength, from Oschmann (2017), spatial separation..
        'alphaNaNCX' : sm.alphaNaNCX, # in mM
        'alphaCaNCX' : sm.alphaCaNCX, # in mM, from Oschmann 2017
        'eNCX' : sm.eNCX, # in mM, from Oschmann 2017
        'ksatNCX' : sm.ksatNCX, # in mM, from Oschmann 2017
        'kGLT' : sm.kGLT, # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        'HeOHa' : sm.HeOHa, # from Breslin, Wade sodium microdomains..
        'Nv' : sm.Nv,# Naomi
        'Gv' : sm.Gv, # Naomi
        'k1max' : sm.k1max,# Naomi
        'KM' : sm.KM, # Naomi
        'KDV' : sm.KDV, # Naomi
        'k20' : sm.k20,  # Naomi
        'k2cat' : sm.k2cat, # Naomi
        'kmin20' : sm.kmin20, # Naomi
        'kmin1' : sm.kmin1, # Naomi
        'k3' : sm.k3, # Naomi
        'kmin3' : sm.kmin3, # Naomi
        'k4' : sm.k4, # Naomi
        'tinact' : sm.tinact, # Naomi
        'trec' : sm.trec, # Naomi
        'tpost' : sm.tpost, # Naomi
        'Vpost0' : sm.Vpost0, # Emperical
        'kNCXg' : sm.kNCXg,
        'gAMPA' : sm.gAMPA, # Tewari Majumdar
        'VAMPA' : sm.VAMPA, # Tewari Majumdar
        'Rm' : sm.Rm, # Tewari Majumdar
        'alphaAMPA' : sm.alphaAMPA,  # Segev and Koch chap 1p.NI0+p.NF0+p.ND0+p.NR0+p.NR10+p.NR20+p.NR30+p.NN0+p.NGlug0
        'betaAMPA' : sm.betaAMPA, # Segev and Koch chap 1
        'blockerScaleAst' : sm.blockerScaleAst,       # How much more should you block astrocyte pump?
        'blockerScaleNeuron' : sm.blockerScaleNeuron,     # How much more should you block neuronal pump?
        'pumpScaleAst' : sm.pumpScaleAst,           # baseline astrocyte pump strength factor
        'pumpScaleNeuron' : sm.pumpScaleNeuron,        # baseline neuron pump strength factor
        'nkccScale' : sm.nkccScale,              # factor NKCC1 flux rate
        'kirScale' : sm.kirScale,               # factor Kir conductance
        'gltScale' : sm.gltScale,
        'nka_na' : sm.nka_na,
        'nka_k' : sm.nka_k,
        'beta1' : sm.beta1,                  # sigmoidal rate NKA blockade onset
        'beta2' : sm.beta2,                  # sigmoidal rate NKA blockade offset
        'perc' : sm.perc,                   # Perc of baseline blocked NKA
        'tstart' : sm.tstart,                # Start blockade
        'tend' : sm.tend,                  # End blockade
        'nkccblock_after' : sm.nkccblock_after,
        'kirblock_after' : sm.kirblock_after,
        'alphae0' : sm.alphae0,
        'choice' : sm.choice,
        'astroblock' : sm.astroblock,
        'kGLT' : sm.kGLT,           # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        # Initial concentrations and volumes (baseline rest)
        'NaCi0' : sm.NaCi0,
        'KCi0' : sm.KCi0,
        'ClCi0' : sm.ClCi0,
        'CaCi0' : sm.CaCi0,
        'GluCi0' : sm.GluCi0,
        'NaCe0' : sm.NaCe0,
        'KCe0' : sm.KCe0,
        'ClCe0' : sm.ClCe0,
        'CaCc0' : sm.CaCc0,
        'GluCc0' : sm.GluCc0,
        'NaCg0' : sm.NaCg0,
        'KCg0' : sm.KCg0,
        'ClCg0' : sm.ClCg0,
        'CaCg0' : sm.CaCg0,
        'GluCg0' : sm.GluCg0,
        'Wi0' : sm.Wi0,
        'Wg0' : sm.Wg0,
        'VolPreSyn' : sm.VolPreSyn,
        'VolPAP' : sm.VolPAP,
        'Volc' : sm.Volc,
        'NF0' : sm.NF0,
        'NGlui0' : sm.NGlui0,
        'NGluc0' : sm.NGluc0,
        'We0' : sm.We0,
        'NNai0' : sm.NNai0,
        'NKi0' : sm.NKi0,
        'NCli0' : sm.NCli0,
        'NCai0' : sm.NCai0,
        'NNae0' : sm.NNae0,
        'NKe0' : sm.NKe0,
        'NCle0' : sm.NCle0,
        'NCac0' : sm.NCac0,
        'NNag0' : sm.NNag0,
        'NKg0' : sm.NKg0,
        'NClg0' : sm.NClg0,
        'NCag0' : sm.NCag0,
        'NGlug0' : sm.NGlug0,
        'CNa' : sm.CNa,
        'CK' : sm.CK,
        'CCl' : sm.CCl,
        'CCa' : sm.CCa,
        'Wtot' : sm.Wtot,
        'NAi' : sm.NAi,
        'NAe' : sm.NAe,
        'NBe' : sm.NBe,
        'NAg' : sm.NAg,
        'NBg' : sm.NBg,
        # Gates
        'alpham0' : sm.alpham0,
        'betam0' : sm.betam0,
        'alphah0' : sm.alphah0,
        'betah0' : sm.betah0,
        'alphan0' : sm.alphan0,
        'betan0' : sm.betan0,
        'm0' : sm.m0,
        'h0' : sm.h0,
        'n0' : sm.n0,
        # Neuronal leaks
        'INaG0' : sm.INaG0,
        'IKG0' : sm.IKG0,
        'IClG0' : sm.IClG0,
        'INaL0' : sm.INaL0,
        'IKL0' : sm.IKL0,
        'IClL0' : sm.IClL0,
        'JKCl0' : sm.JKCl0,
        'sigmapump' : sm.sigmapump,
        'fpump' : sm.fpump,
        'neurPump' : sm.neurPump,
        'INCXi0' : sm.INCXi0,
        'fGLTi0' : sm.fGLTi0,
        'ICaG0' : sm.ICaG0,
        'ICaL0' : sm.ICaL0,
        'fRelGlui0' : sm.fRelGlui0,
        'PNaL' : sm.PNaL,            # Estimated sodium leak conductance in neuron
        'PKL' : sm.PKL,   # Estimated K leak conductance in neuron
        'PClL' : sm.PClL,              # Estimated Cl leak conducatance in neuron
        'PCaL' : sm.PCaL,
        # Glial uptake parameters
        'kActive' : sm.kActive,
        'LH20g' : sm.LH20g,
        'gNKCC1' : sm.gNKCC1,
        'GKir' : sm.GKir,
        #-----------------------------------------------------------------------------------------------
        # Astrocyte leaks
        'fRelK0' : sm.fRelK0,
        'fRelCl0' : sm.fRelCl0,
        'fRelNa0' : sm.fRelNa0,
        'fNKCC10' : sm.fNKCC10,
        'sigmapumpA' : sm.sigmapumpA,
        'fpumpA' : sm.fpumpA,
        'fActive0': sm.fActive0,
        'IKir0' : sm.IKir0,
        'fRelGlu0' : sm.fRelGlu0,
        'fRelCa0' : sm.fRelCa0,
        'fGLTg0' : sm.fGLTg0,
        'INCXg0' : sm.INCXg0,
        'fRelGlu0' : sm.fRelGlu0,
        'k1init' : sm.k1init,
        'gCainit' : sm.gCainit,
        'k2init' : sm.k2init,
        'kmin2catinit' : sm.kmin2catinit,
        'kmin2init' : sm.kmin2init,
        'kRelNa' : sm.kRelNa,
        'kRelK' : sm.kRelK,
        'kRelCl' : sm.kRelCl,
        'kRelCa' : sm.kRelCa,
        #---------------------------------------------------------------------------------------------------------
        #Glutamate recycling initial conditions
        'NI0' : sm.NI0,
        'ND0' : sm.ND0,
        'NN0' : sm.NN0,
        'NR0' : sm.NR0,
        'NR10' : sm.NR10,
        'NR20' : sm.NR20,
        'NR30' : sm.NR30,
        'kRelGlui' : sm.kRelGlui,
        'kRelGlu' : sm.kRelGlu,
        'CGlu' : sm.CGlu}

paramName = 'Images/{a}_params.mat'.format(a=args.name[0])
sio.savemat(paramName,dict)
