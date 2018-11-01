from numpy import *
import sm_model as modelfile
import sm_params as paramfile
class smclass:
   def __init__(self,initvals,testparams):
      paramfile.parameters(self,testparams,initvals)
   def model(self,t,y,*args):
      if args:
         return(modelfile.model(t,y,self,*args))
      else:
         return(modelfile.model(t,y,self))
      
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
NaCg0 = 13
KCg0 = 90
ClCg0 = 35
Wi0 = 2
Wg0 = 2
NNai0 = NaCi0*Wi0
NKi0 = KCi0*Wi0
NCli0 = ClCi0*Wi0
NNag0 = NaCg0*Wg0
NKg0 = KCg0*Wg0
NClg0 = ClCg0*Wg0
initvals = [NNai0,NKi0,NCli0,NNag0,NKg0,NClg0,Wi0,Wg0]

tstart = 30
tend = 32
blockerScaleAst = 1;
blockerScaleNeuron = 1;
pumpScaleAst = 1;
pumpScaleNeuron = 1;
nkccScale = 0.4;
kirScale = 2;
beta1 = 0.8;
beta2 = 0.5;
perc = 0.1;
testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale, beta1, beta2, perc, tstart, tend]

sm = smclass(initvals,testparams)