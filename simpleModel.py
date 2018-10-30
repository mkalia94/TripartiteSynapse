from numpy import *
from scipy.optimize import fsolve
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from parameters import *

##       PARAMETERS
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
NaCg0 = 13
KCg0 = 90
ClCg0 = 35
Wi0 = 2
Wg0 = 2




blockerScaleAst = 1;
blockerScaleNeuron = 1;
pumpScaleAst = 1;
pumpScaleNeuron = 1;
nkccScale = 0.4;
kirScale = 2;
beta1 = 0.8;
beta2 = 0.5;
perc = 0.1;

testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale, beta1, beta2, perc]








t0=0
t00b=30*60*1e3
t01b=31*60*1e3
t01c=31*60*1e3
t10b=46*60*1e3
t11b=47*60*1e3
t10c=30.5*60*1e3
t11c=30.5*60*1e3


t0b=t00b
t1b=t10b


t0na=0
t1na=0
tfinal=120*60*1e3
current=30

#-------------------------------------------------------
#         PARAMETERS AND INITIAL VALUE CALCULATION
#-------------------------------------------------------

#Conservation parameters

# Wtot=4.282092091428572
# CNa=216.85195418887753
# CK=297.16762407405264
# CCl=212.31185223435875

beta0=0.07
Wi0=1.9970095290373091
Wg0=1.9983122136358114
We0=Wi0/beta0

#Model parameters
C=20
F=96485.333 
R=8314.4598      
T=310    
PNaG=80*1e-5        
PNaL=0.2*1e-5       
PKG=40*1e-5         
PKL=2*1e-5          
PClG=1.95*1e-5      
PClL=0.25*1e-5
UKCl=13*1e-7       
LH20i=2*1e-14
LH20g=2*1e-14     
chi=0.8
Qpump=52.5
NAi=296
Nbuffertot = 300


#Initial conditions
NNa0=13.384917705158726
NK0=296.27615755617273
NCl0=13.674760584604426
delK0=0.0004733745768728212

m0=0.01194816930666775
h0=0.98886515241801343
n0=0.0026859395587689695



# OPTIONAL WAY TO GET NNag0 and NClg0 (you can set it yourself too)
# Step 1: Getting NNae0,NCle0,NKe0
NaCe0=152
KCe0=3
ACe=20
NAe=ACe*We0
NNae0=NaCe0*We0
NKe0=KCe0*We0
Vg0=-90

Wtot = Wi0 + We0+ Wg0

k1=0.0008
k21=15
k22=-1.15
k20=k1/(1+exp((KCe0-k21)/(k22)))


def func(x):
    NKbuffer0 = x[0]
    NNag0 = x[1]
    NCle0 = x[2]
    NClg0 = x[3]
    CNa = NNa0+NNae0+NNag0
    CK = NK0+NKe0 +NKbuffer0
    CCl = (CNa + CK) - (NAe+NAi)
    eqs=[k20*Nbuffertot*NKe0 - NKbuffer0*(k20*NKe0 + k1*We0),
         (NAe+NCle0+NKe0+NNae0)*Wtot - We0*(2*CK+2*CNa+Nbuffertot-NKbuffer0),
         NClg0 - CCl+(NCle0+NCl0),
         Vg0 - F/C*(NNag0+NKbuffer0-NClg0)
    ]
    return eqs

[NKbuffer0,NNag0,NCle0,NClg0]=fsolve(func,[100,100,100,100])

CNa = NNa0+NNae0+NNag0
CK = NK0+NKe0+NKbuffer0
CCl=(CNa + CK) - (NAe+NAi)
#===================================================================

#Initial conditions
y0=[NNa0,NK0,NCl0,delK0,m0,h0,n0,Wi0,Wg0]

#====================================================================







#-----------------------------------------------------------------------------
#                   SOLVING THE SYSTEM
#-----------------------------------------------------------------------------


def model(t,y,*args):
 

   Qpump=52.5
   
   if args:
      NNa=y[:,0]
      NK=y[:,1]
      NCl=y[:,2]
      delK=y[:,3]
      m=y[:,4]
      h=y[:,5]
      n=y[:,6]
      Wi=y[:,7]
      Wg=y[:,8]
   else:
      NNa=y[0]
      NK=y[1]
      NCl=y[2]
      delK=y[3]
      m=y[4]
      h=y[5]
      n=y[6]
      Wi=y[7]
      Wg=y[8]
      
   def smoothstep(t,a,b):
          if t<a:
             y=0
          elif t>=a and t<b:
            s=(t-a)/(b-a)
            y = (126+(-420+(540+(-315+70*s)*s)*s)*s)*s**5
          else:
            y=1
          return y  
    


   def veratridine(h,t):
      if t<=t00b:
         hchange=1
         h_ver=h
         curr=0
      elif t>t00b and t<=t01c:
         hchange=1-smoothstep(t,t00b,t01b)
         h_ver=h+(1-h)*smoothstep(t,t00b,t01b)
         curr=current*smoothstep(t,t00b,t01c)
      elif t>t01c and t<=t01b:
         hchange=1-smoothstep(t,t00b,t01b)
         h_ver=1
         curr=current
      elif t>t01b and t<=t10c:
         hchange=0
         h_ver=1
         curr=current
      elif t>t10c and t<=t11c:
         hchange=0
         h_ver=1
         curr=current*(1-smoothstep(t,t10c,t11c))
      elif t>t11c and t<=t10b:
         hchange=0
         h_ver=1
         curr=0
      elif t>t10b and t<=t11b:
         hchange=smoothstep(t,t10b,t11b)
         h_ver=1-smoothstep(t,t10b,t11b)
         curr=0
      else:
         hchange=1
         h_ver=0
         curr=0
      return hchange,h_ver,curr  
   
   if args:
      hchange=0
      curr=0
      t1=array(t)
      h_ver=ones(len(t1))
      for i in range(0,len(t1)):
        hchange,h_ver1,curr=veratridine(h[i],t1[i])
        h_ver[i]=h_ver1
   else:
      hchange,h_ver,curr=veratridine(h,t)
   
#   h=h_ver
   
         
   #Derived quantities
   NCle=CK+CNa-chi*delK-NAe-NAi-NClg0-NCl
   NClg=chi*delK+NClg0
   NKbuffer=delK+NKbuffer0
   NKe=CK-delK-NKbuffer0-NK
   NNae=CNa+(1-chi)*delK-NNag0-NNa
   NNag=(chi-1)*delK+NNag0
   We=Wtot-(Wi+Wg)
   Nbuffer=Nbuffertot-NKbuffer
   
   #Intracellular concentrations
   NaCi=NNa/Wi
   KCi=NK/Wi
   ClCi=NCl/Wi
   
   #Extracellular concentrations
   NaCe=NNae/We
   KCe=NKe/We
   ClCe=NCle/We
   
   #Glial concentrations
   NaCg=NNag/Wg
   ClCg=NClg/Wg
   
   #Voltage definition
   V=F/C*(NNa+NK-NCl-NAi)   
 
   #Gated currents
   INaG=PNaG*(m**3)*(h)*(F**2)*(V)/(R*T)*((NaCi-NaCe*exp(-(F*V)/(R*T)))/(1-exp(-(F*V)/(R*T))))
   IKG=(PKG*(n**2))*(F**2)*(V)/(R*T)*((KCi-KCe*exp(-(F*V)/(R*T)))/(1-exp(-F*V/(R*T))))
   IClG=PClG*1/(1+exp(-(V+10)/10))*(F**2)*V/(R*T)*((ClCi-ClCe*exp(F*V/(R*T)))/(1-exp(F*V/(R*T))))
   
   #Leak currents
   INaL=PNaL*(F**2)/(R*T)*V*((NaCi-NaCe*exp((-F*V)/(R*T)))/(1-exp((-F*V)/(R*T))))
   IKL=PKL*F**2/(R*T)*V*((KCi-KCe*exp((-F*V)/(R*T)))/(1-exp((-F*V)/(R*T))))
   IClL=PClL*(F**2)/(R*T)*V*((ClCi-ClCe*exp((F*V)/(R*T)))/(1-exp((F*V)/(R*T))))
   
   #Na-K pump
   Ipump=Qpump*(0.68/(1+(6.7/NaCi)**3)+0.32/(1+(67.6/NaCi)**3)) 
   
   #KCl cotransport
   JKCl=UKCl*R*T/F*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe))
   
   #Water flux
   SCi=NaCi+KCi+ClCi+NAi/Wi
   SCe=NaCe+KCe+ClCe+NAe/We
   SCg=NaCg+NKbuffer/Wg+ClCg
   delpii=R*T*(SCi-SCe)
   delpig=R*T*(SCg-SCe)
   fluxi=LH20i*(delpii)
   fluxg=LH20g*(delpig)
   
   #Gate coefficients
   alpham=0.32*(V+52)/(1-exp(-(V+52)/4))
   betam=0.28*(V+25)/(exp((V+25)/5)-1)
   alphah=0.128*exp(-(V+53)/18)
   betah=4/(1+exp(-(V+30)/5))
   alphan=0.016*(V+35)/(1-exp(-(V+35)/5))
   betan=0.25*exp(-(V+50)/40)
   
   #Buffer
   
   k1=0.0008
   k2=k1*(1-exp(-KCe/15))
   k2=k1/(1+exp((KCe-15)/(-1.15)))
   buffchange=(-k2*Nbuffer/Wg*KCe+k1*NKbuffer/Wg)
   
   #Nernst potentials
   NaNernst=R*T/F*log(NaCe/NaCi)
   KNernst=R*T/F*log(KCe/KCi)
   ClNernst=-R*T/F*log(ClCe/ClCi)   
   
   #Final model 
   ODEs=[-1/F*(INaG+INaL+3*Ipump-curr),
          -1/F*(IKG+IKL-2*Ipump)-JKCl,
          1/F*(IClG+IClL)-JKCl,
          # -(We*(buffchange)-KCe*(fluxi+fluxg)),
          (-We*buffchange+NKbuffer/Wg*fluxg),
          alpham*(1-m)-m*betam,
          hchange*(alphah*(1-h)-h*betah),
          alphan*(1-n)-n*betan,
          fluxi,
          fluxg]
    
  
   
   if args:
    plotlist=['INaG','IKG','IClG','INaL','IKL','IClL','NNa','NK','NCl','NNae','NKe','NCle','Ipump','NKbuffer','Wi','Wg','We','h','m','n','NaCi','KCi','ClCi','NaCe','ClCe','KCe','k1','KCg','NNag','NClg','Vg']
    plotdict={'INaG':INaG,'IKG':IKG,'IClG':IClG,'INaL':INaL,'IKL':IKL,'IClL':IClL,'NNa':NNa,'NK':NK,'NCl':NCl,'NNae':NNae,'NKe':NKe,'NCle':NCle,'Ipump':Ipump,'NKbuffer':NKbuffer,'Wi':(Wi/Wi0)**(2/3)*100,'Wg':(Wg/Wg0)**(2/3)*100,'We':(We/We0)**(2/3)*100,'h':h,'m':m,'n':n,'NaCi':NaCi,'KCi':KCi,'ClCi':ClCi,'NaCe':NaCe,'KCe':KCe,'ClCe':ClCe,'k1':k1*ones(len(t)),'KCg':NKbuffer/Wg,'NNag':NNag,'NClg':NClg,'Vg':(F/C*(NNag+NKbuffer-NClg))}
    plotnamedict={'INaG':r'$I_{Na^+}^g$ (pA)','IKG':r'$I_{K^+}^g$ (pA)','IClG':r'$I_{Cl^-}^g$ (pA)','INaL':r'$I_{Na^+}^l$ (pA)','IKL':r'$I_{K^+}^l$ (pA)','IClL':r'$I_{Cl^-}^l$ (pA)','NNa':r'$N_{Na^+}^i$ (fmol)','NK':r'$N_{K^+}^i$ (fmol)','NCl':r'$N_{Cl^-}^i$ (fmol)','NNae':r'$N_{Na^+}^e$ (fmol)','NKe':r'$N_{K^+}^e$ (fmol)','NCle':r'$N_{Cl^-}^e$ (fmol)','Ipump':r'$I_{pump}$ (pA)','NKbuffer':r'$N_{K^+buffer}^g$','Wi':r'$\%$ increase of $W_i$','Wg':r'$\%$ increase of $W_g$','We':r'$W_e$','h':r'h','m':r'm','n':r'n','NaCi':r'$[Na^+]_i$','KCi':r'$[K^+]_i$','ClCi':r'$[Cl^-]_i$','NaCe':r'$[Na^+]_e$','KCe':r'$[K^+]_e$','ClCe':r'$[Cl^-]_e$','k1':'buffering rate $k_1$','KCg':r'bbb $[K^+_{buffer}]_g$','NNag':r'$N_{Na^+}^g$','NClg':r'$N_{Cl^-}^g$','Vg':r'$V_g$'}   
    t1=array(t)/60*1e-3 
    for i in range(0,len(plotlist)):
     to_plot=plotdict.get(plotlist[i])
     plot_name=plotnamedict.get(plotlist[i])
     plt.plot(t1,to_plot,label=plot_name,zorder=2)
     if t0b!=0:
      p=plt.axvspan(t0b/60*1e-3, t1b/60*1e-3, color='0.7', alpha=0.5, lw=0,label="Veratridine")
     # p=plt.axvspan(t0na/60*1e-3, t1na/60*1e-3, color='0.4', alpha=0.5, lw=0,label="Na blockade")
     plt.legend()
     plt.ylabel(r'{d}'.format(d=plot_name))
     plt.xlabel("t (min.)")
     plt.savefig(r'Images_beta_0_07/{d}.eps'.format(d=plotlist[i]),format='eps')
     plt.clf()
    
    if t0b!=0:
     plt.axvspan(t0b/60*1e-3, t1b/60*1e-3, color='0.7', alpha=0.5, lw=0,label="OGD")
     plt.axvspan(t0na/60*1e-3, t1na/60*1e-3, color='0.4', alpha=0.5, lw=0,label="Na blockade")
    plt.plot(array(t)/60*1e-3,NaNernst,label=r"$Na^+$")
    plt.plot(array(t)/60*1e-3,KNernst,label=r"$K^+$")
    plt.plot(array(t)/60*1e-3,ClNernst,label=r"$Cl^-$")
    plt.plot(array(t)/60*1e-3,V,label=r"$V$")
    plt.legend()
    plt.ylabel("Nernst potentials/Membrane potential (mV)")
    plt.xlabel("t (min.)")
    plt.savefig('Images_beta_0_07/VNernst.eps',format='eps')
    plt.clf()
    
    Vg=F/C*(NNag+NKbuffer-NClg)
    plt.plot(array(t)/60*1e-3, Vg)
    plt.savefig('Images_beta_0_07/Vg.eps',format='eps')
    
     
   else:
    return array(ODEs)

mod = Explicit_Problem(model, y0, t0)
sim = CVode(mod)


def solver():
    sim.atol = 1e-9
    sim.rtol = 1e-9
    sim.iter = 'Newton'

    t, y = sim.simulate(tfinal)
    return t,y

def plotter():
   model(t,y,1)
      
# tt=arange(0,120*60*1e3,100)
# aa=zeros(len(tt))
# for i in range(0,len(tt)):
#    bb=model(tt[i],y0)
#    cc=model(tt[0],y0)
#    aa[i]=bb[0]/cc[0]
# 
# 
# plt.plot(array(tt),aa)11