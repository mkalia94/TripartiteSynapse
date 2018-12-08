from numpy import *

def model(t,y,p,*args):
   if args:
      NNa=y[:,0]
      NK=y[:,1]
      NCl=y[:,2]
      m=y[:,3]
      h=y[:,4]
      n=y[:,5]      
      Wi=y[:,6]
   else:
      NNa=y[0]
      NK=y[1]
      NCl=y[2]
      m=y[3]
      h=y[4]
      n=y[5]      
      Wi=y[6]

   NaCe = p.NaCe0
   KCe = p.KCe0
   ClCe = p.ClCe0
   
   # Concentrations
   NaCi =NNa/Wi
   KCi = NK/Wi
   ClCi = NCl/Wi

   
   # Voltages
   V=p.F/p.C*(NNa+NK-NCl-p.NAi)
   
   # Gates
   alpham = 0.32*(V+52)/(1-exp(-(V+52)/4))
   betam = 0.28*(V+25)/(exp((V+25)/5)-1)
   alphah = 0.128*exp(-(V+53)/18)
   betah = 4/(1+exp(-(V+30)/5))
   alphan = 0.016*(V+35)/(1-exp(-(V+35)/5))
   betan = 0.25*exp(-(V+50)/40)
   
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
   
   # Neuron: Na-K pump
   Ipump = blockerExp*p.Qpump*(0.62/(1+(6.7/NaCi)**3)+0.38/(1+(67.6/NaCi)**3));
   # Ipump = (p.blockerScaleNeuron*blockerExp-(p.blockerScaleNeuron-1))*p.pumpScaleNeuron*p.Qpump*(NaCi**(1.5)/(NaCi**(1.5)+p.nka_nra**1.5))*(KCe/(KCe+p.nka_k))
   
   # Neuron: KCl cotransport
   JKCl = p.UKCl*p.R*p.T/p.F*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe))
    
   # Water flux: neuron + astrocyte
   SCi = NaCi+KCi+ClCi+p.NAi/Wi
   SCe = NaCe+KCe+ClCe+p.ACe
   delpii = p.R*p.T*(SCi-SCe)
   fluxi = p.LH20i*(delpii)


   
   # blockerExp = 1/(1+exp(p.beta1*(t-70))) + 1/(1+exp(-p.beta2*(t-80)))
   # INaG = INaG*blockerExp
   
   # Final model
   ODEs=[  (-1/p.F*(INaG+INaL+3*Ipump) ), \
   (-1/p.F*(IKG+IKL-2*Ipump) - JKCl), \
   (1/p.F*(IClG+IClL)-JKCl), \
   alpham*(1-m)-betam*m,\
   alphah*(1-h)-betah*h,\
   alphan*(1-n)-betan*n,
   fluxi]    
   ODEs = array(ODEs)*60*1e3
      
   if args:
      return eval(args[0])
   else:
      return ODEs
      

