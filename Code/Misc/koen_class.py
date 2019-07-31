from numpy import *
import koen_model as modelfile
import koen_params as paramfile
class smclass:
   def __init__(self,initvals,testparams):
      paramfile.parameters(self,testparams,initvals)
   def model(self,t,y,*args):
      if args:
         return(modelfile.model(t,y,self,*args))
      else:
         return(modelfile.model(t,y,self))

#Initial values
NaCi0 = 10
KCi0 = 145
ClCi0 = 7
Wi0 = 2
Wg0 = 1.7
NNai0 = NaCi0*Wi0
NKi0 = KCi0*Wi0
NCli0 = ClCi0*Wi0
initvals = [NNai0,NKi0,NCli0,Wi0]

# Free parameters
tstart = 30
tend = 1000
beta1 = 0.5;
beta2 = 0.5;
perc = 0.0


testparams = [beta1, beta2, perc, tstart, tend]

# Generate class instance
sm = smclass(initvals,testparams)
testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
'pumpScaleAst', 'pumpScaleNeuron', \
'nkccScale', 'kirScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
initvallist =['NNai0','NKi0','NCli0','NNag0','NKg0','NClg0','Wi0','Wg0']

initvals = [NNai0,NKi0,NCli0,sm.m0,sm.h0,sm.n0,Wi0]
