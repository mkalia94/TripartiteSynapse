from numpy import *
def parameters(p,testparams,initvals):
    p.C = 20
    p.F = 96485.333
    p.R = 8314.4598
    p.T = 310
    p.PNaG = 80*1e-5
    p.PNaL_base = 0.2*1e-5
    p.PKG = 40*1e-5
    p.PKL_base = 2*1e-5
    p.PClG = 1.95*1e-5
    p.PClL_base = 0.25*1e-5
    p.UKCl = 13*1e-7
    p.LH20i = 2*1e-14
    p.Qpump = 54.5
    p.Cg = 20
    p.alphae0 = 0.01        # Volume fraction: ECS
    p.Vg0 = -80            # Fix initial glial membrane potential
    p.Vi0 = -65.5
    p.NaCe0 = 152          # ECS Na Conc.
    p.KCe0 = 3             # ECS K Conc.
    p.ClCe0 = 135          # ECS Cl Conc.
    p.KCe_thres = 7
    p.kup2 = 0.1
    
    p.blockerScaleAst = testparams[0]
    p.blockerScaleNeuron = testparams[1]
    p.pumpScaleAst = testparams[2]
    p.pumpScaleNeuron = testparams[3]
    p.nkccScale = testparams[4]
    p.kirScale = testparams[5]
    p.beta1 = testparams[6]
    p.beta2 = testparams[7]
    p.perc = testparams[8]
    p.tstart = testparams[9]
    p.tend = testparams[10]
    
    # Initial concentrations and volumes (baseline rest)
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
    p.NBg = (1/2*(p.NaCe0 + p.KCe0 + p.ClCe0 + p.NAe/p.We0) - (p.KCg0 + p.NaCg0) + p.Cg/2/p.F*p.Vg0/p.Wg0)*p.Wg0
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
    p.neurPump = p.pumpScaleNeuron*p.Qpump*(p.NaCi0**(1.5)/(p.NaCi0**(1.5)+10**1.5))*(p.KCe0/(p.KCe0+3))
    
    p.PNaL = -((p.INaG0 + 3*p.neurPump))/p.INaL0
    p.PKL = -((p.IKG0 - 2*p.neurPump)+p.F*p.JKCl0)/p.IKL0
    p.PClL = (p.F*p.JKCl0 - p.IClG0)/p.IClL0
    
    # Glial uptake parameters
    p.kActive = p.Qpump*p.pumpScaleAst/p.F
    p.LH20g = p.LH20i
    p.gNKCC1 = p.nkccScale*6e-5
    p.GKir = p.kirScale*60*1e-3;
    
    # Astrocyte leaks
    p.fRelK0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.KCg0-p.KCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fRelCl0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.ClCg0-p.ClCe0*exp((p.F*p.Vg0)/(p.R*p.T)))/(1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.fRelNa0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.NaCg0-p.NaCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fNKCC10 = p.gNKCC1*p.R*p.T/p.F*(log(p.KCe0) + log(p.NaCe0) + 2*log(p.ClCe0) - log(p.KCg0) - log(p.NaCg0) - 2*log(p.ClCg0))
    p.fActive0 = p.kActive*(p.NaCg0**(1.5)/(p.NaCg0**(1.5)+10**1.5))*(p.KCe0/(p.KCe0+3))
    p.IKir0 = p.GKir*1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((p.KCg0-p.KCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(1-exp((-p.F*p.Vg0)/(p.R*p.T))))*1/(1+exp((p.KCe_thres-p.KCe0)/p.kup2)) #(sqrt(KCe)/(1+exp((Vg - Vkg - 34)/19.23)))
    
    #(p.KCe0/(3+p.KCe0))**2*(p.NaCg0/(10+p.NaCg0))**3
    
    p.kRelNa = (3*p.fActive0 - p.fNKCC10)/p.fRelNa0
    p.kRelK = (p.IKir0-2*p.fActive0-p.fNKCC10)/p.fRelK0
    p.kRelCl = -2*p.fNKCC10/p.fRelCl0