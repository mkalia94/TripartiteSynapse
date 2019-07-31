from numpy import *
def parameters(p,testparams,initvals):
    p.C = 20                # Neuron membrane capacitance
    p.F = 96485.333         # Faraday's constant 
    p.R = 8314.4598         # Gas constant
    p.T = 310               # Temperature
    p.PNaG = 80*1e-5        # permeability of gated Na current
    p.PNaL = 0.2*1e-5  
    p.PKG = 40*1e-5         # permbeability of gated K current
    p.PKL = 2*1e-5 
    p.PClG = 1.95*1e-5      # permeability of gated Cl current
    p.PClL = 0.25*1e-5
    p.UKCl = 13*1e-7        # flux rate of KCl cotransporter
    p.LH20i = 2*1e-14       # Osmotic permeability in the neuron
    p.Qpump = 54.5          # Baseline neuronal pump strength
    p.Cg = 20               # Astrocyte membrane capacitance 
    
    
    p.Vi0 = -65.5           # Fix initial neuronal membrane potential 
    p.NaCe0 = 152           # Fix initial ECS Na Conc.
    p.KCe0 = 3              # Fix initial ECS K Conc.
    p.ClCe0 = 135           # Fix initial ECS Cl Conc.

    
    p.beta1 = testparams[0]                  # sigmoidal rate NKA blockade onset
    p.beta2 = testparams[1]                  # sigmoidal rate NKA blockade offset
    p.perc = testparams[2]                   # Perc of baseline blocked NKA
    p.tstart = testparams[3]                 # Start blockade
    p.tend = testparams[4]                  # End blockade

    
    # Initial concentrations and volumes (baseline rest)
    p.NNai0 = initvals[0]            
    p.NKi0 = initvals[1]
    p.NCli0 = initvals[2]
    p.Wi0 = initvals[3]
    p.NaCi0 = p.NNai0/p.Wi0
    p.KCi0 = p.NKi0/p.Wi0
    p.ClCi0 = p.NCli0/p.Wi0

    # Impermeants and conserved quantities
    p.NAi = p.NNai0 + p.NKi0 - p.NCli0 - p.C/p.F*p.Vi0
    p.ACe = (p.NNai0 + p.NKi0 + p.NCli0 + p.NAi)/p.Wi0 - (p.NaCe0 + p.KCe0 + p.ClCe0) 

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
    
    p.INaG0 = p.PNaG*(p.m0**3)*(p.h0)*(p.F**2)*(p.Vi0)/(p.R*p.T)*((p.NaCi0-p.NaCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(1-exp(-(p.F*p.Vi0)/(p.R*p.T))))
    p.IKG0 = (p.PKG*(p.n0**4))*(p.F**2)*(p.Vi0)/(p.R*p.T)*((p.KCi0-p.KCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(1-exp(-p.F*p.Vi0/(p.R*p.T))))
    p.IClG0 = p.PClG*1/(1+exp(-(p.Vi0+10)/10))*(p.F**2)*p.Vi0/(p.R*p.T)*((p.ClCi0-p.ClCe0*exp(p.F*p.Vi0/(p.R*p.T)))/(1-exp(p.F*p.Vi0/(p.R*p.T))))
    p.INaL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((p.NaCi0-p.NaCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IKL0 = p.F**2/(p.R*p.T)*p.Vi0*((p.KCi0-p.KCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IClL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((p.ClCi0-p.ClCe0*exp((p.F*p.Vi0)/(p.R*p.T)))/(1-exp((p.F*p.Vi0)/(p.R*p.T))))
    p.JKCl0 = p.UKCl*p.R*p.T/p.F*(log(p.KCi0)+log(p.ClCi0)-log(p.KCe0)-log(p.ClCe0))
    # p.neurPump = p.pumpScaleNeuron*p.Qpump*(p.NaCi0**(1.5)/(p.NaCi0**(1.5)+p.nka_na**1.5))*(p.KCe0/(p.KCe0+p.nka_k))
    p.neurPump = p.Qpump*(0.62/(1+(6.7/p.NaCi0)**3)+0.38/(1+(67.6/p.NaCi0)**3))
    
    p.PNaL = -((p.INaG0 + 3*p.neurPump))/p.INaL0             # Estimated sodium leak conductance in neuron
    p.PKL = -((p.IKG0 - 2*p.neurPump)+p.F*p.JKCl0)/p.IKL0    # Estimated K leak conductance in neuron 
    p.PClL = (p.F*p.JKCl0 - p.IClG0)/p.IClL0                 # Estimated Cl leak conducatance in neuron
