def model(t,y,*args):
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

    NNae = p.CNa - NNag - NNa;
    NKe = p.CK - NKg - NK;
    NCle = p.CCl - NClg - NCl;
    We = p.Wtot - Wi - Wg;
    
    % Concentrations
    NaCi =NNa./Wi;
    KCi = NK./Wi;
    ClCi = NCl./Wi;
    NaCe = NNae./We;
    KCe = NKe./We;
    ClCe = NCle./We;
    NaCg = NNag./Wg;
    KCg = NKg./Wg;
    ClCg = NClg./Wg;
    
    % Voltage definition 
    V=p.F./p.C.*(NNa+NK-NCl-p.NAi);
    Vg = p.F/p.Cg.*(NNag + NKg + p.NBg - p.NAg -NClg);
    
    % Gates
    alpham = 0.32.*(V+52)./(1-exp(-(V+52)./4));
    betam = 0.28.*(V+25)./(exp((V+25)./5)-1);
    alphah = 0.128.*exp(-(V+53)./18);
    betah = 4./(1+exp(-(V+30)./5));
    alphan = 0.016.*(V+35)./(1-exp(-(V+35)./5));
    betan = 0.25.*exp(-(V+50)./40);
    m = alpham./(alpham+betam);
    h = alphah./(alphah+betah);
    n = alphan./(alphan+betan);
    
    % Neuron: Gated currents
    INaG = p.PNaG.*(m.^3).*(h).*(p.F.^2).*(V)./(p.R.*p.T).*((NaCi-NaCe.*exp(-(p.F.*V)./(p.R.*p.T)))./(1-exp(-(p.F.*V)./(p.R.*p.T))));
    IKG = (p.PKG.*(n.^4)).*(p.F.^2).*(V)./(p.R.*p.T).*((KCi-KCe.*exp(-(p.F.*V)./(p.R.*p.T)))./(1-exp(-p.F.*V./(p.R.*p.T))));
    IClG = p.PClG.*1./(1+exp(-(V+10)./10)).*(p.F.^2).*V./(p.R.*p.T).*((ClCi-ClCe.*exp(p.F.*V./(p.R.*p.T)))./(1-exp(p.F.*V./(p.R.*p.T))));
    
    
    % Neuron: Leak currents
    INaL = p.PNaL.*(p.F.^2)./(p.R.*p.T).*V.*((NaCi-NaCe.*exp((-p.F.*V)./(p.R.*p.T)))./(1-exp((-p.F.*V)./(p.R.*p.T))));
    IKL = p.PKL.*p.F.^2./(p.R.*p.T).*V.*((KCi-KCe.*exp((-p.F.*V)./(p.R.*p.T)))./(1-exp((-p.F.*V)./(p.R.*p.T))));
    IClL = p.PClL.*(p.F.^2)./(p.R.*p.T).*V.*((ClCi-ClCe.*exp((p.F.*V)./(p.R.*p.T)))./(1-exp((p.F.*V)./(p.R.*p.T))));
    
    blockerExp = blocker(t,p.tstart,p.tend,p.perc,p.beta1,p.beta2);
    
    % Neuron: Na-K pump
    Ipump = (p.blockerScaleNeuron*blockerExp-(p.blockerScaleNeuron-1)).*p.pumpScaleNeuron.*p.Qpump.*(NaCi.^(1.5)./(NaCi.^(1.5)+10.^1.5)).*(KCe./(KCe+3));
    
    % Neuron: KCl cotransport
    JKCl = p.UKCl.*p.R.*p.T./p.F.*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe));
    fNKCC1_n = p.gNKCC1*p.R*p.T/p.F.*(log(KCe) + log(NaCe) + 2*log(ClCe) - log(KCi) - log(NaCi) - 2*log(ClCi));
    
    % Astrocyte: pump
    fActive = (p.blockerScaleAst*blockerExp-(p.blockerScaleAst-1)).*p.kActive.*(NaCg.^(1.5)./(NaCg.^(1.5)+10.^1.5)).*(KCe./(KCe+3));
    
    % Astrocyte: Leak
    fRelK = p.kRelK.*1/p.F*p.F.^2./(p.R.*p.T).*Vg.*((KCg-KCe.*exp((-p.F.*Vg)./(p.R.*p.T)))./(1-exp((-p.F.*Vg)./(p.R.*p.T))));
    fRelCl = p.kRelCl.*1/p.F*p.F.^2./(p.R.*p.T).*Vg.*((ClCg-ClCe.*exp((p.F.*Vg)./(p.R.*p.T)))./(1-exp((p.F.*Vg)./(p.R.*p.T))));
    fRelNa = p.kRelNa.*1/p.F*p.F.^2./(p.R.*p.T).*Vg.*((NaCg-NaCe.*exp((-p.F.*Vg)./(p.R.*p.T)))./(1-exp((-p.F.*Vg)./(p.R.*p.T))));
    
    % Astrocyte: NKCC1
    fNKCC1 = p.gNKCC1*p.R*p.T/p.F.*(log(KCe) + log(NaCe) + 2*log(ClCe) - log(KCg) - log(NaCg) - 2*log(ClCg));
    
    % Astrocyte: Kir4.1
    Vkg = p.R.*p.T./p.F.*log(KCe./KCg); 
    IKir = p.GKir/p.F.*p.F.^2./(p.R.*p.T).*Vg.*((KCg-KCe.*exp((-p.F.*Vg)./(p.R.*p.T)))./(1-exp((-p.F.*Vg)./(p.R.*p.T)))).*1./(1+exp((p.KCe_thres-KCe)/p.kup2));%(sqrt(KCe)./(1+exp((Vg - Vkg - 34)./19.23)));
    
    % Water flux: neuron + astrocyte
    SCi = NaCi+KCi+ClCi+p.NAi./Wi;
    SCe = NaCe+KCe+ClCe+p.NAe./We;
    SCg = NaCg + KCg + ClCg + p.NAg./Wg + p.NBg./Wg;
    delpii = p.R.*p.T.*(SCi-SCe);
    fluxi = p.LH20i.*(delpii);
    delpig = p.R.*p.T.*(SCg-SCe);
    fluxg = p.LH20g.*(delpig);
    
    % Final model
    ODEs=[  (-1/p.F*(INaG+INaL+3*Ipump) + fNKCC1_n);
            (-1/p.F*(IKG+IKL-2*Ipump) + fNKCC1_n);
            (1/p.F*(IClG+IClL)+2*fNKCC1_n);
            -3*fActive + fRelNa + fNKCC1;
            -IKir + 2*fActive + fRelK + fNKCC1;
            2*fNKCC1 + fRelCl;
            fluxi;
            fluxg;
            ];    
    ODEs = ODEs.*60*1e3;
    
    if nargin > 3
        ODEs = eval(varargin{1});
    end
    
    end