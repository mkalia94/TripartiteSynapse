from numpy import *

def model(t,y,p,*args):
   if args:
      NNa=y[:,0]
      NK=y[:,1]
      NCl=y[:,2]
      NNag=y[:,3]
      NKg=y[:,4]
      NClg=y[:,5]
      Wi=y[:,6]
      Wg=y[:,7]
   else:
      NNa=y[0]
      NK=y[1]
      NCl=y[2]
      NNag=y[3]
      NKg=y[4]
      NClg=y[5]
      Wi=y[6]
      Wg=y[7]
   
   NNae = p.CNa - NNag - NNa
   NKe = p.CK - NKg - NK
   NCle = p.CCl - NClg - NCl
   We = p.Wtot - Wi - Wg
   
   # Concentrations
   NaCi =NNa/Wi
   KCi = NK/Wi
   ClCi = NCl/Wi
   NaCe = NNae/We
   KCe = NKe/We
   ClCe = NCle/We
   NaCg = NNag/Wg
   KCg = NKg/Wg
   ClCg = NClg/Wg
   
   # Voltages
   V=p.F/p.C*(NNa+NK-NCl-p.NAi)
   Vg = p.F/p.Cg*(NNag + NKg + p.NBg - p.NAg -NClg)
   
   # Gates
   alpham = 0.32*(V+52)/(1-exp(-(V+52)/4))
   betam = 0.28*(V+25)/(exp((V+25)/5)-1)
   alphah = 0.128*exp(-(V+53)/18)
   betah = 4/(1+exp(-(V+30)/5))
   alphan = 0.016*(V+35)/(1-exp(-(V+35)/5))
   betan = 0.25*exp(-(V+50)/40)
   m = alpham/(alpham+betam)
   h = alphah/(alphah+betah)
   n = alphan/(alphan+betan)
   
   # Neuron: Gated currents
   INaG = p.PNaG*(m**3)*(h)*(p.F**2)*(V)/(p.R*p.T)*((NaCi-NaCe*exp(-(p.F*V)/(p.R*p.T)))/(1-exp(-(p.F*V)/(p.R*p.T))))
   IKG = (p.PKG*(n**2))*(p.F**2)*(V)/(p.R*p.T)*((KCi-KCe*exp(-(p.F*V)/(p.R*p.T)))/(1-exp(-p.F*V/(p.R*p.T))))
   IClG = p.PClG*1/(1+exp(-(V+10)/10))*(p.F**2)*V/(p.R*p.T)*((ClCi-ClCe*exp(p.F*V/(p.R*p.T)))/(1-exp(p.F*V/(p.R*p.T))))
   
   
   # Neuron: Leak currents
   INaL = p.PNaL*(p.F**2)/(p.R*p.T)*V*((NaCi-NaCe*exp((-p.F*V)/(p.R*p.T)))/(1-exp((-p.F*V)/(p.R*p.T))))
   IKL = p.PKL*p.F**2/(p.R*p.T)*V*((KCi-KCe*exp((-p.F*V)/(p.R*p.T)))/(1-exp((-p.F*V)/(p.R*p.T))))
   IClL = p.PClL*(p.F**2)/(p.R*p.T)*V*((ClCi-ClCe*exp((p.F*V)/(p.R*p.T)))/(1-exp((p.F*V)/(p.R*p.T))))
   
   # Blockade
   blockerExp = 1/(1+exp(p.beta1*(t-p.tstart))) + 1/(1+exp(-p.beta2*(t-p.tend)))
   blockerExp = p.perc + (1-p.perc)*blockerExp
   
   fac = 3
   recover = 1/(1+exp(-p.beta1*(t-p.tend-100))) + 1/(1+exp(p.beta2*(t-p.tend - 200)))
   recover = (fac-1)*recover - (fac-2)
   # Neuron: Na-K pump
   Ipump = (p.blockerScaleNeuron*blockerExp-(p.blockerScaleNeuron-1))*p.pumpScaleNeuron*p.Qpump*(NaCi**(1.5)/(NaCi**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))
   
   # Neuron: KCl cotransport
   JKCl = p.UKCl*p.R*p.T/p.F*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe))
   
   # Astrocyte: pump
   fActive = (p.blockerScaleAst*blockerExp-(p.blockerScaleAst-1))*p.kActive*(NaCg**(1.5)/(NaCg**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))
   
   # Astrocyte: Leak
   fRelK = p.kRelK*1/p.F*p.F**2/(p.R*p.T)*Vg*((KCg-KCe*exp((-p.F*Vg)/(p.R*p.T)))/(1-exp((-p.F*Vg)/(p.R*p.T))))
   fRelCl = p.kRelCl*1/p.F*p.F**2/(p.R*p.T)*Vg*((ClCg-ClCe*exp((p.F*Vg)/(p.R*p.T)))/(1-exp((p.F*Vg)/(p.R*p.T))))
   fRelNa = p.kRelNa*1/p.F*p.F**2/(p.R*p.T)*Vg*((NaCg-NaCe*exp((-p.F*Vg)/(p.R*p.T)))/(1-exp((-p.F*Vg)/(p.R*p.T))))
   
   # Astrocyte: NKCC1
  
   blockerExp_NKCC1 = 1/(1+exp(p.beta1*(t-p.tend))) + 1/(1+exp(-p.beta2*(t-p.tend - 5)))
   blockerExp_NKCC1 = 0.3 + (1-0.3)*blockerExp_NKCC1
   fNKCC1 = p.gNKCC1*p.R*p.T/p.F*(log(KCe) + log(NaCe) + 2*log(ClCe) - log(KCg) - log(NaCg) - 2*log(ClCg))
   if p.nkccblock_after == 1:
      fNKCC1 = blockerExp_NKCC1*fNKCC1
      
   # Astrocyte: Kir4.1
   Vkg = p.R*p.T/p.F*log(KCe/KCg) 
   minfty = 1/(2+exp(1.62*(p.F/p.R/p.T)*(Vg-Vkg)))
   IKir = p.GKir*minfty*KCe/(KCe+p.KCe_thres)*(Vg-Vkg)
   # IKir = p.GKir*(Vg-Vkg)*sqrt(KCe)/(1+exp((Vg - Vkg - 34)/19.23)))
   if p.kirblock_after == 1:
      IKir = blockerExp_NKCC1*IKir 
    
   # Water flux: neuron + astrocyte
   SCi = NaCi+KCi+ClCi+p.NAi/Wi
   SCe = NaCe+KCe+ClCe+p.NAe/We + p.NBe/We
   SCg = NaCg + KCg + ClCg + p.NAg/Wg + p.NBg/Wg
   delpii = p.R*p.T*(SCi-SCe)
   fluxi = p.LH20i*(delpii)
   delpig = p.R*p.T*(SCg-SCe)
   fluxg = p.LH20g*(delpig)

   
   # blockerExp = 1/(1+exp(p.beta1*(t-70))) + 1/(1+exp(-p.beta2*(t-80)))
   # INaG = INaG*blockerExp
   
   # Final model
   ODEs=[  (-1/p.F*(INaG+INaL+3*Ipump) ), \
   (-1/p.F*(IKG+IKL-2*Ipump) - JKCl), \
   (1/p.F*(IClG+IClL)-JKCl), \
   -3*fActive + fRelNa + fNKCC1, \
   IKir + 2*fActive + fRelK + fNKCC1, \
   2*fNKCC1 + fRelCl, \
   fluxi, \
   fluxg]    
   ODEs = array(ODEs)*60*1e3
      
   if args:
      return eval(args[0])
   else:
      return ODEs
      
from numpy import *

