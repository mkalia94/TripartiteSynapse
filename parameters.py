from numpy import *
class params:
   def __init__(self,initvals,testparams):
      self.C = 20
      self.F = 96485.333
      self.R = 8314.4598
      self.T = 310
      self.PNaG = 80*1e-5
      self.PNaL_base = 0.2*1e-5
      self.PKG = 40*1e-5
      self.PKL_base = 2*1e-5
      self.PClG = 1.95*1e-5
      self.PClL_base = 0.25*1e-5
      self.UKCl = 13*1e-7
      self.LH20i = 2*1e-14
      self.Qpump = 54.5
      self.Cg = 20
      self.alphae0 = 0.5        # Volume fraction: ECS
      self.Vg0 = -80            # Fix initial glial membrane potential
      self.Vi0 = -65.5
      self.NaCe0 = 152          # ECS Na Conc.
      self.KCe0 = 3             # ECS K Conc.
      self.ClCe0 = 135          # ECS Cl Conc.
      self.KCe_thres = 5
      self.kup2 = 0.1
      
      self.blockerScaleAst = testparams[0]
      self.blockerScaleNeuron = testparams[1]
      self.pumpScaleAst = testparams[2]
      self.pumpScaleNeuron = testparams[3]
      self.nkccScale = testparams[4]
      self.kirScale = testparams[5]
      self.beta1 = testparams[6]
      self.beta2 = testparams[7]
      self.perc = testparams[8]
      self.tstart = testparams[9]
      self.tend = testparams[10]
      
      # Initial concentrations and volumes (baseline rest)
      self.NNai0 = initvals[0]
      self.NKi0 = initvals[1]
      self.NCli0 = initvals[2]
      self.NNag0 = initvals[3]
      self.NKg0 = initvals[4]
      self.NClg0 = initvals[5]
      self.Wi0 = initvals[6]
      self.Wg0 = initvals[7]
      self.NaCg0 = self.NNag0/self.Wg0        # Glial Na Conc.
      self.KCg0 = self.NKg0/self.Wg0          # Glial K Conc.
      self.ClCg0 = self.NClg0/self.Wg0        # Glial Cl Conc.
      self.We0 = self.alphae0*self.Wi0
      self.Wtot = self.Wi0+self.We0+self.Wg0
      self.NaCi0 = self.NNai0/self.Wi0        # ICS Na Conc.
      self.KCi0 = self.NKi0/self.Wi0          # ICS K Conc.
      self.ClCi0 = self.NCli0/self.Wi0       # ICS Cl Conc.
      
      # Impermeants and conserved quantities
      self.NAi = self.NNai0 + self.NKi0 - self.NCli0 - self.C/self.F*self.Vi0
      self.NAe = ((self.NaCi0+self.KCi0+self.ClCi0+self.NAi/self.Wi0)-(self.NaCe0+self.KCe0+self.ClCe0))*self.We0
      self.NBg = (1/2*(self.NaCe0 + self.KCe0 + self.ClCe0 + self.NAe/self.We0) - (self.KCg0 + self.NaCg0) + self.Cg/2/self.F*self.Vg0/self.Wg0)*self.Wg0
      self.NAg = (1/2*(self.NaCe0 + self.KCe0 + self.ClCe0 + self.NAe/self.We0) - self.Cg/2/self.F*self.Vg0/self.Wg0 -self.ClCg0)*self.Wg0
      self.CNa = self.NaCi0*self.Wi0 + self.NaCe0*self.We0 + self.NaCg0*self.Wg0
      self.CK = self.KCi0*self.Wi0 + self.KCe0*self.We0 + self.KCg0*self.Wg0
      self.CCl = self.ClCi0*self.Wi0 + self.ClCe0*self.We0 + self.ClCg0*self.Wg0
      
      # Gates
      self.alpham0 = 0.32*(self.Vi0+52)/(1-exp(-(self.Vi0+52)/4))
      self.betam0 = 0.28*(self.Vi0+25)/(exp((self.Vi0+25)/5)-1)
      self.alphah0 = 0.128*exp(-(self.Vi0+53)/18)
      self.betah0 = 4/(1+exp(-(self.Vi0+30)/5))
      self.alphan0 = 0.016*(self.Vi0+35)/(1-exp(-(self.Vi0+35)/5))
      self.betan0 = 0.25*exp(-(self.Vi0+50)/40)
      self.m0 = self.alpham0/(self.alpham0+self.betam0)
      self.h0 = self.alphah0/(self.alphah0+self.betah0)
      self.n0 = self.alphan0/(self.alphan0+self.betan0)
      
      # Neuronal leaks
      self.INaG0 = self.PNaG*(self.m0**3)*(self.h0)*(self.F**2)*(self.Vi0)/(self.R*self.T)*((self.NaCi0-self.NaCe0*exp(-(self.F*self.Vi0)/(self.R*self.T)))/(1-exp(-(self.F*self.Vi0)/(self.R*self.T))))
      self.IKG0 = (self.PKG*(self.n0**4))*(self.F**2)*(self.Vi0)/(self.R*self.T)*((self.KCi0-self.KCe0*exp(-(self.F*self.Vi0)/(self.R*self.T)))/(1-exp(-self.F*self.Vi0/(self.R*self.T))))
      self.IClG0 = self.PClG*1/(1+exp(-(self.Vi0+10)/10))*(self.F**2)*self.Vi0/(self.R*self.T)*((self.ClCi0-self.ClCe0*exp(self.F*self.Vi0/(self.R*self.T)))/(1-exp(self.F*self.Vi0/(self.R*self.T))))
      self.INaL0 = (self.F**2)/(self.R*self.T)*self.Vi0*((self.NaCi0-self.NaCe0*exp((-self.F*self.Vi0)/(self.R*self.T)))/(1-exp((-self.F*self.Vi0)/(self.R*self.T))))
      self.IKL0 = self.F**2/(self.R*self.T)*self.Vi0*((self.KCi0-self.KCe0*exp((-self.F*self.Vi0)/(self.R*self.T)))/(1-exp((-self.F*self.Vi0)/(self.R*self.T))))
      self.IClL0 = (self.F**2)/(self.R*self.T)*self.Vi0*((self.ClCi0-self.ClCe0*exp((self.F*self.Vi0)/(self.R*self.T)))/(1-exp((self.F*self.Vi0)/(self.R*self.T))))
      self.JKCl0 = self.UKCl*self.R*self.T/self.F*(log(self.KCi0)+log(self.ClCi0)-log(self.KCe0)-log(self.ClCe0))
      self.neurPump = self.pumpScaleNeuron*self.Qpump*(self.NaCi0**(1.5)/(self.NaCi0**(1.5)+10**1.5))*(self.KCe0/(self.KCe0+3))
      
      self.PNaL = -((self.INaG0 + 3*self.neurPump)-self.F*self.JKCl0)/self.INaL0
      self.PKL = -((self.IKG0 - 2*self.neurPump)-self.F*self.JKCl0)/self.IKL0
      self.PClL = (-self.F*2*self.JKCl0 - self.IClG0)/self.IClL0
      
      # Glial uptake parameters
      self.kActive = self.Qpump*self.pumpScaleAst/self.F
      self.LH20g = self.LH20i
      self.gNKCC1 = self.nkccScale*6e-5
      self.GKir = self.kirScale*60*1e-3;
      
      # Astrocyte leaks
      self.fRelK0 = 1/self.F*self.F**2/(self.R*self.T)*self.Vg0*((self.KCg0-self.KCe0*exp((-self.F*self.Vg0)/(self.R*self.T)))/(1-exp((-self.F*self.Vg0)/(self.R*self.T))))
      self.fRelCl0 = 1/self.F*self.F**2/(self.R*self.T)*self.Vg0*((self.ClCg0-self.ClCe0*exp((self.F*self.Vg0)/(self.R*self.T)))/(1-exp((self.F*self.Vg0)/(self.R*self.T))))
      self.fRelNa0 = 1/self.F*self.F**2/(self.R*self.T)*self.Vg0*((self.NaCg0-self.NaCe0*exp((-self.F*self.Vg0)/(self.R*self.T)))/(1-exp((-self.F*self.Vg0)/(self.R*self.T))))
      self.fNKCC10 = self.gNKCC1*self.R*self.T/self.F*(log(self.KCe0) + log(self.NaCe0) + 2*log(self.ClCe0) - log(self.KCg0) - log(self.NaCg0) - 2*log(self.ClCg0))
      self.fActive0 = self.kActive*(self.NaCg0**(1.5)/(self.NaCg0**(1.5)+10**1.5))*(self.KCe0/(self.KCe0+3))
      self.IKir0 = self.GKir*1/self.F*self.F**2/(self.R*self.T)*self.Vg0*((self.KCg0-self.KCe0*exp((-self.F*self.Vg0)/(self.R*self.T)))/(1-exp((-self.F*self.Vg0)/(self.R*self.T))))*1/(1+exp((self.KCe_thres-self.KCe0)/self.kup2)) #(sqrt(KCe)/(1+exp((Vg - Vkg - 34)/19.23)))
      
      #(self.KCe0/(3+self.KCe0))**2*(self.NaCg0/(10+self.NaCg0))**3
      
      self.kRelNa = (3*self.fActive0 - self.fNKCC10)/self.fRelNa0
      self.kRelK = (self.IKir0-2*self.fActive0-self.fNKCC10)/self.fRelK0
      self.kRelCl = -2*self.fNKCC10/self.fRelCl0
      