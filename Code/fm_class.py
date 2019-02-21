from numpy import *
import fm_model as modelfile
import fm_params as paramfile
class smclass:
   def __init__(self,initvals,testparams):
      paramfile.parameters(self,testparams,initvals)
   def model(self,t,y,*args):
      if args:
         return(modelfile.model(t,y,self,*args))
      else:
         return(modelfile.model(t,y,self))

#Initial values
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
CaCi0 = 0.073*1e-3 # Assumption based on Oschmann model
GluCi0 = 2 # From 'Maintaining the presynaptic glutamate...Marx, Billups...2015'
NaCe0 = 152
KCe0 = 3
ClCe0 = 135
CaCc0 = 1.8 # Oschmann
GluCc0 = 1*1e-4 # Attwell Barbour Szatkowski... Non vesicular release...'93 (Neuron) 
NaCg0 = 13
KCg0 = 80
ClCg0 = 35
CaCg0 = 0.073*1e-3 # From 'Plasmalemmal so/ca exchanger...Reyes et al...2012'
GluCg0 = 2 # Emperical assumption
Wi0 = 2
Wg0 = 1.7
VolPreSyn = 1*1e-4
VolPAP = 1*1e-4 # Emperical
Volc = 1*1e-4 # Emperical

# Molar amounts

initvals = [NaCi0,KCi0,ClCi0,CaCi0,GluCi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,NaCg0,KCg0,\
ClCg0,CaCg0,GluCg0,Wi0,Wg0,VolPreSyn,VolPAP,Volc]

# Free parameters
tstart = 10
tend = 20
blockerScaleAst =1;
blockerScaleNeuron  =1;
pumpScaleAst = 1;
pumpScaleNeuron = 1;
nkccScale = 10;
kirScale = 1
nka_na = 13
nka_k = 0.2
nkccblock_after = 0
kirblock_after = 0
alphae0 = 0.2
choicee = 3

#Fixed params
beta1 = 0.9;
beta2 = 0.9;
perc = 0.6


testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,alphae0,choicee]

# Generate class instance
sm = smclass(initvals,testparams)
testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
'pumpScaleAst', 'pumpScaleNeuron', \
'nkccScale', 'kirScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
initvallist =['NNai0','NKi0','NCli0','NNag0','NKg0','NClg0','Wi0','Wg0']

initvals = [sm.NNai0,sm.NKi0,sm.NCli0,sm.m0,sm.h0,sm.n0,sm.NCai0,sm.NN0,sm.NR0,\
sm.NR10,sm.NR20,sm.NR30,sm.NF0,sm.NI0,sm.ND0,sm.NNag0,sm.NKg0,sm.NClg0,sm.NCag0,sm.Vpost0,sm.mAMPA0,sm.Wi0,sm.Wg0]