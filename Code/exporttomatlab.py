import scipy.io as sio
from smgates_class import *
C = float(sm.C)                # Neuron membrane capacitance
F = sm.F         # Faraday's constant 
R = sm.R         # Gas constant
T = sm.T              # Temperature
PNaG = sm.PNaG        # permeability of gated Na current  
PNaL = sm.PNaL
PKG = sm.PKG         # permbeability of gated K current 
PKL = sm.PKL
PClG = sm.PClG      # permeability of gated Cl current
PClL = sm.PClL
UKCl = sm.UKCl        # flux rate of KCl cotransporter
LH20i = sm.LH20i       # Osmotic permeability in the neuron
Qpump = sm.Qpump          # Baseline neuronal pump strength
Cg = sm.Cg               # Astrocyte membrane capacitance 

Vg0 = sm.Vg0             # Fix initial glial membrane potential
Vi0 = sm.Vi0           # Fix initial neuronal membrane potential 
NaCe0 = sm.NaCe0           # Fix initial ECS Na Conc.
KCe0 = sm.KCe0              # Fix initial ECS K Conc.
ClCe0 = sm.ClCe0           # Fix initial ECS Cl Conc.
KCe_thres = sm.KCe_thres        # Kir: Threshold for Kir gate
kup2 = sm.kup2     # Kir: Rate of transition from low uptake to high uptake

#testparams
blockerScaleAst = sm.blockerScaleAst       # How much more should you block astrocyte pump?
blockerScaleNeuron = sm.blockerScaleNeuron     # How much more should you block neuronal pump?
pumpScaleAst = sm.pumpScaleAst           # baseline astrocyte pump strength factor
pumpScaleNeuron = sm.pumpScaleNeuron        # baseline neuron pump strength factor
nkccScale = sm.nkccScale              # factor NKCC1 flux rate
kirScale = sm.kirScale              # factor Kir conductance
nka_na = sm.nka_na
nka_k = sm.nka_k
beta1 = sm.beta1                  # sigmoidal rate NKA blockade onset
beta2 = sm.beta2                  # sigmoidal rate NKA blockade offset
perc = sm.perc                   # Perc of baseline blocked NKA
tstart = sm.tstart                 # Start blockade
tend = sm.tend                  # End blockade
nkccblock_after = sm.nkccblock_after
kirblock_after = sm.kirblock_after
alphae0 = sm.alphae0

# Initial concentrations and volumes (baseline rest)
NNai0 = sm.NNai0            
NKi0 = sm.NKi0
NCli0 = sm.NCli0
NNag0 = sm.NNag0
NKg0 = sm.NKg0
NClg0 = sm.NClg0
Wi0 = sm.Wi0
Wg0 = sm.Wg0
NaCg0 = sm.NNag0/sm.Wg0        # Glial Na Conc.
KCg0 = sm.NKg0/sm.Wg0          # Glial K Conc.
ClCg0 = sm.NClg0/sm.Wg0        # Glial Cl Conc.
# Volume fraction: ECS

NaCi0 = sm.NNai0/sm.Wi0        # ICS Na Conc.
KCi0 = sm.NKi0/sm.Wi0          # ICS K Conc.
ClCi0 = sm.NCli0/sm.Wi0        # ICS Cl Conc.

# Glial uptake parameters
kActive = sm.Qpump*sm.pumpScaleAst/sm.F                  
LH20g = sm.LH20i
gNKCC1 = sm.nkccScale*0.03*sm.UKCl
GKir = sm.kirScale*3.7*6*10**3/sm.F/sm.F
kRelNa = (3*sm.fActive0 - sm.fNKCC10)/sm.fRelNa0
kRelK = (-sm.IKir0-2*sm.fActive0-sm.fNKCC10)/sm.fRelK0
kRelCl = -2*sm.fNKCC10/sm.fRelCl0

dict = {'C':C,'F':F,'R':R,'T':T,'PNaG':PNaG,'PNaL':PNaL,'PKG':PKG,'PKL':PKL,'PClG':PClG,'PClL':PClL,'UKCl':UKCl,'LH20i':LH20i,'Qpump':Qpump,'Cg':Cg,'Vg0':Vg0,'Vi0':Vi0,'NaCe0':NaCe0,'KCe0':KCe0,'ClCe0':ClCe0,'nkccScale':nkccScale,'kirScale':kirScale,'nka_na':nka_na,'nka_k':nka_k,'beta1':beta1,'beta2':beta2,'perc':perc,'tstart':tstart,'tend':tend,'alphae0':alphae0,'NNai0':NNai0,'NKi0':NKi0,'NCli0':NCli0,'NNag0':NNag0,'NKg0':NKg0,'NClg0':NClg0,'Wi0':Wi0,'Wg0':Wg0,'NaCg0':NaCg0,'KCg0':KCg0,'ClCg0':ClCg0,'NaCi0':NaCi0,'KCi0':KCi0,'ClCi0':ClCi0,'kActive':kActive,'LH20g':LH20g,'gNKCC1':gNKCC1,'GKir':GKir,'kRelNa':kRelNa,'kRelK':kRelK,'kRelCl':kRelCl}

sio.savemat('paramsUllahPump.mat',dict)
