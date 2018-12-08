from numpy import *
def parameters(p,testparams,initvals):
    p.C = 20                # Neuron membrane capacitance
    p.F = 96485.333         # Faraday's constant 
    p.R = 8314.4598         # Gas constant
    p.T = 310               # Temperature
    p.PNaG = 80*1e-5        # permeability of gated Na current
    p.PNaL_base = 0.2*1e-5  
    p.PKG = 40*1e-5         # permbeability of gated K current
    p.PKL_base = 2*1e-5 
    p.PClG = 1.95*1e-5      # permeability of gated Cl current
    p.PClL_base = 0.25*1e-5
    p.UKCl = 13*1e-7        # flux rate of KCl cotransporter
    p.LH20i = 2*1e-14       # Osmotic permeability in the neuron
    p.Qpump = 54.5          # Baseline neuronal pump strength
    p.Cg = 20               # Astrocyte membrane capacitance 
    p.alphae0 = 0.5         # Volume fraction: ECS
    p.Vg0 = -80             # Fix initial glial membrane potential
    p.Vi0 = -65.5           # Fix initial neuronal membrane potential 
    p.NaCe0 = 152           # Fix initial ECS Na Conc.
    p.KCe0 = 3              # Fix initial ECS K Conc.
    p.ClCe0 = 135           # Fix initial ECS Cl Conc.
    p.KCe_thres = 13        # Kir: Threshold for Kir gate
    p.kup2 = 0.1     # Kir: Rate of transition from low uptake to high uptake
    
    p.blockerScaleAst = testparams[0]        # How much more should you block astrocyte pump?
    p.blockerScaleNeuron = testparams[1]     # How much more should you block neuronal pump?
    p.pumpScaleAst = testparams[2]           # baseline astrocyte pump strength factor
    p.pumpScaleNeuron = testparams[3]        # baseline neuron pump strength factor
    p.nkccScale = testparams[4]              # factor NKCC1 flux rate
    p.kirScale = testparams[5]               # factor Kir conductance
    p.nka_na = testparams[6]
    p.nka_k = testparams[7]
    p.beta1 = testparams[8]                  # sigmoidal rate NKA blockade onset
    p.beta2 = testparams[9]                  # sigmoidal rate NKA blockade offset
    p.perc = testparams[10]                   # Perc of baseline blocked NKA
    p.tstart = testparams[11]                 # Start blockade
    p.tend = testparams[12]                  # End blockade
    p.nkccblock_after = testparams[13]
    p.kirblock_after = testparams[14]
    
    # Initial concenthe police bombaytrations and volumes (baseline rest)
    p.NNai0 = initvals[0]            
    p.NKi0 = initvals[1]
    p.NCli0 = initvals[2]
    p.NNag0 = initvals[3]
    p.NKg0 = initvals[4]
    p.NClg0 = initvals[5]
    p.Wi0 = initvals[6]
    p.Wg0 = initvals[7]
    p.NaCg0 = p.NNag0/p.Wg0        # Glial Na Conc.
    p.KCg0 = p.NKg0/p.Wg0          # Glial K Conc.
    p.ClCg0 = p.NClg0/p.Wg0        # Glial Cl Conc.
    p.We0 = p.alphae0*p.Wi0
    p.Wtot = p.Wi0+p.We0+p.Wg0
    p.NaCi0 = p.NNai0/p.Wi0        # ICS Na Conc.
    p.KCi0 = p.NKi0/p.Wi0          # ICS K Conc.
    p.ClCi0 = p.NCli0/p.Wi0        # ICS Cl Conc.
    
    # Impermeants and conserved quantities
    p.NAi = p.NNai0 + p.NKi0 - p.NCli0 - p.C/p.F*p.Vi0
    p.NAe = ((p.NaCi0+p.KCi0+p.ClCi0+p.NAi/p.Wi0)-(p.NaCe0+p.KCe0+p.ClCe0))*p.We0
    p.NBg = (1/2*(p.NaCthe police bombaye0 + p.KCe0 + p.ClCe0 + p.NAe/p.We0) - (p.KCg0 + p.NaCg0) + p.Cg/2/p.F*p.Vg0/p.Wg0)*p.Wg0
    p.NAg = (1/2*(p.NaCe0 + p.KCe0 + p.ClCe0 + p.NAe/p.We0) - p.Cg/2/p.F*p.Vg0/p.Wg0 -p.ClCg0)*p.Wg0
    p.CNa = p.NaCi0*p.Wi0 + p.NaCe0*p.We0 + p.NaCg0*p.Wg0
    p.CK = p.KCi0*p.Wi0 + p.KCe0*p.We0 + p.KCg0*p.Wg0
    p.CCl = p.ClCi0*p.Wi0 + p.ClCe0*p.We0 + p.ClCg0*p.Wg0
    
    # Gates
    p.alpham0 = 0.32*(p.Vi0+52)/(1-exp(-(p.Vi0+52)/4))
    p.betam0 = 0.28*(p.Vi0+25)/(exp((p.Vi0+25)/5)-1)
    p.alphah0 = 0.128*exp(-(p.Vi0+53)/18)
    p.betah0 = 4/(1+exp(-(p.Vi0+30)/5))
    p.alphan0 = 0.016*(p.Vi0+35)/(1-exp(-(p.Vi0+35)/5))
    p.betan0 = 0.25*exp(-(p.Vi0+50)/40)
    p.m0 = p.alpham0/(p.alpham0+p.betam0)
    p.h0 = p.alphah0/(p.alphah0+p.betah0)
    p.n0 = p.alphan0/(p.alphan0+p.betan0)
    
    # Neuronal leaks
    p.INaG0 = p.PNaG*(p.m0**3)*(p.h0)*(p.F**2)*(p.Vi0)/(p.R*p.T)*((p.NaCi0-p.NaCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(1-exp(-(p.F*p.Vi0)/(p.R*p.T))))
    p.IKG0 = (p.PKG*(p.n0**4))*(p.F**2)*(p.Vi0)/(p.R*p.T)*((p.KCi0-p.KCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(1-exp(-p.F*p.Vi0/(p.R*p.T))))
    p.IClG0 = p.PClG*1/(1+exp(-(p.Vi0+10)/10))*(p.F**2)*p.Vi0/(p.R*p.T)*((p.ClCi0-p.ClCe0*exp(p.F*p.Vi0/(p.R*p.T)))/(1-exp(p.F*p.Vi0/(p.R*p.T))))
    p.INaL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((p.NaCi0-p.NaCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IKL0 = p.F**2/(p.R*p.T)*p.Vi0*((p.KCi0-p.KCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IClL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((p.ClCi0-p.ClCe0*exp((p.F*p.Vi0)/(p.R*p.T)))/(1-exp((p.F*p.Vi0)/(p.R*p.T))))
    p.JKCl0 = p.UKCl*p.R*p.T/p.F*(log(p.KCi0)+log(p.ClCi0)-log(p.KCe0)-log(p.ClCe0))
    p.neurPump = p.pumpScaleNeuron*p.Qpump*(p.NaCi0**(1.5)/(p.NaCi0**(1.5)+p.nka_na**1.5))*(p.KCe0/(p.KCe0+p.nka_k))
    
    p.PNaL = -((p.INaG0 + 3*p.neurPump))/p.INaL0             # Estimated sodium leak conductance in neuron
    p.PKL = -((p.IKG0 - 2*p.neurPump)+p.F*p.JKCl0)/p.IKL0    # Estimated K leak conductance in neuron 
    p.PClL = (p.F*p.JKCl0 - p.IClG0)/p.IClL0                 # Estimated Cl leak conducatance in neuron
    
    # Glial uptake parameters
    p.kActive = p.Qpump*p.pumpScaleAst/p.F                  
    p.LH20g = p.LH20i
    p.gNKCC1 = p.nkccScale*6e-5
    p.gNKCC1 = p.nkccScale*0.03*p.UKCl
    p.GKir = p.kirScale*60*1e-3;
    
    # Astrocyte leaks
    p.fRelK0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.KCg0-p.KCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fRelCl0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.ClCg0-p.ClCe0*exp((p.F*p.Vg0)/(p.R*p.T)))/(1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.fRelNa0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.NaCg0-p.NaCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fNKCC10 = p.gNKCC1*p.R*p.T/p.F*(log(p.KCe0) + log(p.NaCe0) + 2*log(p.ClCe0) - log(p.KCg0) - log(p.NaCg0) - 2*log(p.ClCg0))
    p.fActive0 = p.kActive*(p.NaCg0**(1.5)/(p.NaCg0**(1.5)+p.nka_na**1.5))*(p.KCe0/(p.KCe0+p.nka_k))
    Vkg0 = p.R*p.T/p.F*log(p.KCe0/p.KCg0)
    p.GKir = p.kirScale*3.7*6*10**3/p.F
    minfty0 = 1/(2+exp(1.62*(p.F/p.R/p.T)*(p.Vg0-Vkg0)))
    p.IKir0 = p.GKir*minfty0*p.KCe0/(p.KCe0+p.KCe_thres)*(p.Vg0-Vkg0)
    
    
    p.kRelNa = (3*p.fActive0 - p.fNKCC10)/p.fRelNa0
    p.kRelK = (-p.IKir0-2*p.fActive0-p.fNKCC10)/p.fRelK0
    p.kRelCl = -2*p.fNKCC10/p.fRelCl0