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

#Initial values
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
NaCg0 = 13
KCg0 = 80
ClCg0 = 35
Wi0 = 2
Wg0 = 1.5
NNai0 = NaCi0*Wi0
NKi0 = KCi0*Wi0
NCli0 = ClCi0*Wi0
NNag0 = NaCg0*Wg0
NKg0 = KCg0*Wg0
NClg0 = ClCg0*Wg0
initvals = [NNai0,NKi0,NCli0,NNag0,NKg0,NClg0,Wi0,Wg0]

# Free parameters
tstart = 40
tend = 42
blockerScaleAst =3.1;
blockerScaleNeuron  =3.1;
#blockerScaleNeuron = 1.07
pumpScaleAst = 1;
pumpScaleNeuron = 1;
nkccScale = 10;
kirScale = 1
nka_na = 13
nka_k = 0.2
beta1 = 1.1;
beta2 = 1.1;
perc = 0.85;
#perc = 0.3
testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend]

# Generate class instance
sm = smclass(initvals,testparams)
testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
'pumpScaleAst', 'pumpScaleNeuron', \
'nkccScale', 'kirScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
initvallist =['NNai0','NKi0','NCli0','NNag0','NKg0','NClg0','Wi0','Wg0']


# sm = smclass(initvals,testparams)
# initvals = [NNai0,NKi0,NCli0,sm.m0,sm.h0,sm.n0,NNag0,NKg0,NClg0,Wi0,Wg0]
# testparamlist = ['blockerScaleAst', 'blockerScaleNeuron', \
# 'pumpScaleAst', 'pumpScaleNeuron', \
# 'nkccScale', 'kirScale', 'beta1', 'beta2', 'perc', 'tstart', 'tend']
# initvallist =['NNai0','NKi0','NCli0','m0','h0','n0','NNag0','NKg0','NClg0','Wi0','Wg0']
