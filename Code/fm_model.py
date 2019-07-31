from numpy import *
from scipy import signal

def model(t,y,p,**kwargs):
   casevec = [0,0,0,0]
   if size(shape(y))==2:
      NNa=y[:,0]
      NK=y[:,1]
      NCl=y[:,2]
      m=y[:,3]
      h=y[:,4]
      n=y[:,5]
      NCai = y[:,6]
      NN = y[:,7]
      NR = y[:,8]
      NR1 = y[:,9]
      NR2 = y[:,10]
      NR3 = y[:,11]
      NF = y[:,12]
      NI = y[:,13]
      ND = y[:,14]
      NNag = y[:,15]
      NKg = y[:,16]
      NClg = y[:,17]
      NCag = y[:,18]
      Vpost = y[:,19]
      mAMPA =  y[:,20]
      Wi = y[:,21]
      Wg = y[:,22] 
   else:
      NNa=y[0]
      NK=y[1]
      NCl=y[2]
      m=y[3]
      h=y[4]
      n=y[5]
      NCai = y[6]
      NN = y[7]
      NR = y[8]
      NR1 = y[9]
      NR2 = y[10]
      NR3 = y[11]
      NF = y[12]
      NI = y[13]
      ND = y[14]
      NNag = y[15]
      NKg = y[16]
      NClg = y[17]
      NCag = y[18]
      Vpost = y[19]
      mAMPA =  y[20]
      Wi = y[21]
      Wg = y[22]
   
   for key in kwargs:
      if kwargs['ret']:
         casevec[0] = 1
      if kwargs['block']:
         casevec[1] = 1
      if kwargs['excite']:
         casevec[2] = 1
      if kwargs['astblock']:
         casevec[3] = 1    
          
   # Ionic amounts and concentrations
   #ECS
   We = p.Wtot - Wi - Wg
   NNae = p.CNa - NNag - NNa
   NKe = p.CK - NKg - NK
   NCle = p.CCl - NClg - NCl
   NaCe = NNae/We
   KCe = NKe/We
   ClCe = NCle/We
   #Cleft
   NCac = p.CCa - NCai - NCag
   NGluc = NF
   CaCc = NCac/p.Volc
   GluCc = NGluc/p.Volc
   #Neuron
   NGlui = NI + NN + NR + NR1 + NR2 + NR3 + ND
   NaCi =NNa/Wi
   KCi = NK/Wi
   ClCi = NCl/Wi
   CaCi = NCai/p.VolPreSyn
   GluCi = NGlui/p.VolPreSyn
   #Astrocyte
   NGlug = p.CGlu - NGlui - NGluc
   NaCg = NNag/Wg
   KCg = NKg/Wg
   ClCg = NClg/Wg
   GluCg = NGlug/p.VolPAP
   CaCg = NCag/p.VolPAP
   
   
   # Voltages
   V=p.F/p.C*(NNa+NK+2*NCai-NGlui-NCl-p.NAi)
   Vg = p.F/p.Cg*(NNag + NKg + p.NBg - p.NAg -NClg + 2*NCag - NGlug )
   
   #============================================================================================================
   #--------------------NEURON------------------------------------------------------
   #============================================================================================================
   
   # Gates
   alpham = 0.32*(V+52)/(1-exp(-(V+52)/4))
   betam = 0.28*(V+25)/(exp((V+25)/5)-1)
   alphah = 0.128*exp(-(V+53)/18)
   betah = 4/(1+exp(-(V+30)/5))
   alphan = 0.016*(V+35)/(1-exp(-(V+35)/5))
   betan = 0.25*exp(-(V+50)/40)

   # Gated currents
   INaG = p.PNaG*(m**3)*(h)*(p.F**2)*(V)/(p.R*p.T)*((NaCi-NaCe*exp(-(p.F*V)/(p.R*p.T)))/(1-exp(-(p.F*V)/(p.R*p.T))))
   IKG = (p.PKG*(n**2))*(p.F**2)*(V)/(p.R*p.T)*((KCi-KCe*exp(-(p.F*V)/(p.R*p.T)))/(1-exp(-p.F*V/(p.R*p.T))))
   IClG = p.PClG*1/(1+exp(-(V+10)/10))*(p.F**2)*V/(p.R*p.T)*((ClCi-ClCe*exp(p.F*V/(p.R*p.T)))/(1-exp(p.F*V/(p.R*p.T))))
   ICaG = p.PCaG*m**2*h*4*p.F/(p.R*p.T)*V*((CaCi-CaCc*exp(-2*(p.F*V)/(p.R*p.T)))/(1-exp(-2*(p.F*V)/(p.R*p.T))))
   
   # Leak currents
   INaL = p.PNaL*(p.F**2)/(p.R*p.T)*V*((NaCi-NaCe*exp((-p.F*V)/(p.R*p.T)))/(1-exp((-p.F*V)/(p.R*p.T))))
   IKL = p.PKL*p.F**2/(p.R*p.T)*V*((KCi-KCe*exp((-p.F*V)/(p.R*p.T)))/(1-exp((-p.F*V)/(p.R*p.T))))
   IClL = p.PClL*(p.F**2)/(p.R*p.T)*V*((ClCi-ClCe*exp((p.F*V)/(p.R*p.T)))/(1-exp((p.F*V)/(p.R*p.T))))
   ICaL = 4*p.PCaL*(p.F**2)/(p.R*p.T)*V*((CaCi-CaCc*exp((-2*p.F*V)/(p.R*p.T)))/(1-exp((-2*p.F*V)/(p.R*p.T))))
   fRelGlui = p.kRelGlui*1/p.F*p.F**2/(p.R*p.T)*V*((GluCi-GluCc*exp((p.F*V)/(p.R*p.T)))/(1-exp((p.F*V)/(p.R*p.T))))
   
   # Blockade
   blockerExp = 1/(1+exp(p.beta1*(t-p.tstart))) + 1/(1+exp(-p.beta2*(t-p.tend)))
   blockerExp = p.perc + (1-p.perc)*blockerExp
   
   # Na-K pump
   sigmapump = 1/7*(exp(NaCe/67.3)-1)
   fpump = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*V)+0.0365*sigmapump*exp(-p.F/p.R/p.T*V))
   Ipump = (p.blockerScaleNeuron*blockerExp-(p.blockerScaleNeuron-1))*p.pumpScaleNeuron*fpump*p.Qpump*(NaCi**(1.5)/(NaCi**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))
   
   # KCl cotransport
   JKCl = p.UKCl*p.R*p.T/p.F*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe))
   
   # NCX
   INCXi = p.kNCXi*(NaCe**3)/(p.alphaNaNCX**3+NaCe**3)*(CaCc/(p.alphaCaNCX+CaCc))* \
   (NaCi**3/NaCe**3*exp(p.eNCX*p.F*V/p.R/p.T)-CaCi/CaCc*exp((p.eNCX-1)*p.F*V/p.R/p.T))/\
   (1+p.ksatNCX*exp((p.eNCX-1)*p.F*V/p.R/p.T))
   
   # EAAT
   fGLTi = p.kGLT*p.R*p.T/p.F*log(NaCe**3/NaCi**3*KCi/KCe*p.HeOHa*GluCc/GluCi)
   
   #============================================================================================================
   #----------------------------------CLEFT---------------------------------------------------------------------
   #============================================================================================================
   
   k1 = p.k1max*CaCi/(CaCi+p.KM)
   gCa = CaCi/(CaCi+p.KDV)
   k2 = p.k20+gCa*p.k2cat
   kmin2cat = p.k2cat*p.kmin20/p.k20   
   kmin2 = p.kmin20+gCa*kmin2cat


   #============================================================================================================
   #--------------------------ASTROCYTE-----------------------------------------
   #============================================================================================================
      
   # Na-K pump
   sigmapumpA = 1/7*(exp(NaCe/67.3)-1)
   fpumpA = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*Vg)+0.0365*sigmapumpA*exp(-p.F/p.R/p.T*Vg))
   fActive = (p.blockerScaleAst*blockerExp-(p.blockerScaleAst-1))*p.kActive*fpumpA*(NaCg**(1.5)/(NaCg**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))
   
   # Leak
   fRelK = p.kRelK*1/p.F*p.F**2/(p.R*p.T)*Vg*((KCg-KCe*exp((-p.F*Vg)/(p.R*p.T)))/(1-exp((-p.F*Vg)/(p.R*p.T))))
   fRelCl = p.kRelCl*1/p.F*p.F**2/(p.R*p.T)*Vg*((ClCg-ClCe*exp((p.F*Vg)/(p.R*p.T)))/(1-exp((p.F*Vg)/(p.R*p.T))))
   fRelNa = p.kRelNa*1/p.F*p.F**2/(p.R*p.T)*Vg*((NaCg-NaCe*exp((-p.F*Vg)/(p.R*p.T)))/(1-exp((-p.F*Vg)/(p.R*p.T))))
   fRelGlu = p.kRelGlu*1/p.F*p.F**2/(p.R*p.T)*Vg*((GluCg-GluCc*exp((p.F*Vg)/(p.R*p.T)))/(1-exp((p.F*Vg)/(p.R*p.T)))) 
   fRelCa = 4*p.kRelCa*1/p.F*p.F**2/(p.R*p.T)*Vg*((CaCg-CaCc*exp((-2*p.F*Vg)/(p.R*p.T)))/(1-exp((-2*p.F*Vg)/(p.R*p.T))))
   
   # NKCC1
   blockerExp_NKCC1 = 1/(1+exp(p.beta1*(t-p.tend))) + 1/(1+exp(-p.beta2*(t-p.tend - 5)))
   blockerExp_NKCC1 = 0.3 + (1-0.3)*blockerExp_NKCC1
   fNKCC1 = p.gNKCC1*p.R*p.T/p.F*(log(KCe) + log(NaCe) + 2*log(ClCe) - log(KCg) - log(NaCg) - 2*log(ClCg))
   if p.nkccblock_after == 1:
      fNKCC1 = blockerExp_NKCC1*fNKCC1
      
   # Kir4.1
   Vkg = p.R*p.T/p.F*log(KCe/KCg) 
   minfty = 1/(2+exp(1.62*(p.F/p.R/p.T)*(Vg-Vkg)))
   IKir = p.GKir*minfty*KCe/(KCe+p.KCe_thres)*(Vg-Vkg)
   # IKir = p.GKir*(Vg-Vkg)*sqrt(KCe)/(1+exp((Vg - Vkg - 34)/19.23)))
   if p.kirblock_after == 1:
      IKir = blockerExp_NKCC1*IKir 
      
   # GLT-1
   fGLTg = p.kGLT*p.R*p.T/p.F*log(NaCe**3/NaCg**3*KCg/KCe*p.HeOHa*GluCc/GluCg)   
   
   # NCX
   INCXg = p.kNCXg*(NaCe**3)/(p.alphaNaNCX**3+NaCe**3)*(CaCc/(p.alphaCaNCX+CaCc))* \
   (NaCg**3/NaCe**3*exp(p.eNCX*p.F*Vg/p.R/p.T)-CaCg/CaCc*exp((p.eNCX-1)*p.F*Vg/p.R/p.T))/\
   (1+p.ksatNCX*exp((p.eNCX-1)*p.F*Vg/p.R/p.T)) 
    
   #================================================
   #==============================================================
   #----------------------------VOLUME DYNAMICS-------------------------------------------------------------------
   #==============================================================================================================
   SCi = NaCi+KCi+ClCi+p.NAi/Wi
   SCe = NaCe+KCe+ClCe+p.NAe/We + p.NBe/We
   SCg = NaCg + KCg + ClCg + p.NAg/Wg + p.NBg/Wg
   delpii = p.R*p.T*(SCi-SCe)
   fluxi = p.LH20i*(delpii)
   delpig = p.R*p.T*(SCg-SCe)
   fluxg = p.LH20g*(delpig)
   
   #==============================================================================================================
   #----------------------------POSTSYNAPTIC RESPONSE-------------------------------------------------------------
   #==============================================================================================================
   
   IAMPA = p.gAMPA*mAMPA*(Vpost-p.VAMPA)
   
   #==============================================================================================================
   #----------------------------INTERVENTIONS--------------------------------------------------------------
   #==============================================================================================================
   
   if casevec[1] == 1:
      dict = kwargs['block']
      for key in dict:
         value = dict[key]
         blockOther = 1/(1+exp(p.beta1*(t-value[0]))) + 1/(1+exp(-p.beta2*(t-value[1])))
         if key == 'INaG':
            INaG = INaG*blockOther
         elif key == 'Ipump':
            Ipump = Ipump*blockOther
         elif key == 'Ipump':
            fActive = fActive*blockOther
         elif key == 'IKG':
            IKG = IKG*blockOther
         elif key == 'IClG':
            IClG = IClG*blockOther
         elif key == 'JKCl':
            JKCl = JKCl*blockOther
         elif key == 'INCXi':
            INCXi = INCXi*blockOther
         elif key == 'fNKCC1':
            fNKCC1 = fNKCC1*blockOther
         elif key == 'IKir':
            IKir = IKir*blockOther
         elif key == 'fGLTg':
            fGLTg = fGLTg*blockOther
         elif key == 'INCXg':
            INCXg = INCXg*blockOther
         elif key == 'Wateri':
            fluxi = fluxi*blockOther
         elif key == 'Waterg':
            fluxg = fluxg*blockOther                   
            
   if casevec[2] == 1:
      arg_excite = kwargs['excite']
      if t > arg_excite[0] & t < arg_excite[1]:
         IExcite = 5/p.F*(1-signal.square(array(100*t)))
      else:
         IExcite = 0   
   else:
      IExcite = 0
      
   if casevec[3] == 1:
      arg_astblock = kwargs['astblock']
      astblock =  1/(1+exp(p.beta1*(t-arg_astblock[0]))) + 1/(1+exp(-p.beta2*(t-arg_astblock[1])))  
   else:
      astblock = 1
      
      
   #==============================================================================================================
   #----------------------------RECOVERY EXPERIMENTS--------------------------------------------------------------
   #==============================================================================================================      
   
   # Final model
   ODEs=[ #Neuron
   (-1/p.F*(INaG+INaL+3*Ipump))-3/p.F*INCXi + 3*fGLTi + IExcite,
   (-1/p.F*(IKG+IKL-2*Ipump)-JKCl-fGLTi), \
   (1/p.F*(IClG+IClL)-JKCl), \
   alpham*(1-m)-betam*m,\
   alphah*(1-h)-betah*h,\
   alphan*(1-n)-betan*n,\
   -1/p.F*(ICaG+ICaL) + 1/p.F*INCXi,\
   # GLUTAMATE RECYCLING
   k1*ND-(p.kmin1+k2)*NN+kmin2*NR,\
   k2*NN-(kmin2+3*p.k3*CaCi)*NR + p.kmin3*NR1,\
   3*p.k3*CaCi*NR-(p.kmin3+2*p.k3*CaCi)*NR1+2*p.kmin3*NR2,\
   2*p.k3*CaCi*NR1-(2*p.kmin3+p.k3*CaCi)*NR2+3*p.kmin3*NR3,\
   p.k3*CaCi*NR2-(3*p.kmin3+p.k4)*NR3,\
   p.k4*NR3 - fGLTi - astblock*fGLTg - astblock*fRelGlu - fRelGlui,\
   - NI/p.trec + fGLTi + fRelGlui,\
   NI/p.trec-k1*ND+p.kmin1*NN,\
   #ASTROCYTE
   astblock*(-3*fActive + fRelNa + fNKCC1-3/p.F*INCXg + 3*fGLTg),\
   astblock*(IKir + 2*fActive + fRelK + fNKCC1-fGLTg), \
   astblock*(2*fNKCC1 + fRelCl), \
   astblock*(1/(p.F)*INCXg - fRelCa),\
   #POSTSYN
   0,#1/(p.tpost)*(-(Vpost-p.Vpost0)-p.Rm*IAMPA),\
   0,#p.alphaAMPA*GluCc*(1-mAMPA)-p.betaAMPA*mAMPA,\
   #WATER
   fluxi, \
   astblock*fluxg]    
   ODEs = array(ODEs)*60*1e3
      
   if casevec[0]==1:
      return eval(kwargs['ret'])
   else:
      return ODEs
      
from numpy import *

