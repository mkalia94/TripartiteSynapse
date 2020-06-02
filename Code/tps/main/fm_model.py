from tps import *
def model(t, y, p, *args):
    #only PS
    if size(shape(y)) == 2:
        NNa = y[:, 0]
        NK = y[:, 1]
        NCl = y[:, 2]
        m = y[:, 3]
        h = y[:, 4]
        n = y[:, 5]
        NCai = y[:, 6]
        NN = y[:, 7]
        NR = y[:, 8]
        NR1 = y[:, 9]
        NR2 = y[:, 10]
        NR3 = y[:, 11]
        NI = y[:, 12]
        ND = y[:, 13]
        NNag = y[:, 14]
        NKg = y[:, 15]
        NClg = y[:, 16]
        NCag = y[:, 17]
        NGlug = y[:,18]
        Vtemp = y[:, 19]
        Wi = y[:, 20]
        Wg = y[:, 21]
        Wp = y[:, 22]
        NNap = y[:, 23]
        NKp = y[:, 24]
        NClp = y[:, 25]
        NCap = y[:, 26]
        mp = y[:, 27]
        hp = y[:, 28]
        np = y[:, 29]
        AMPA2A = y[:, 30]
        AMPA2D = y[:, 31]
        #AMPA1A = y[:,32]
        #NMDAA = y[:, 33]

    else:
        NNa = y[0]
        NK = y[1]
        NCl = y[2]
        m = y[3]
        h = y[4]
        n = y[5]
        NCai = y[6]
        NN = y[7]
        NR = y[8]
        NR1 = y[9]
        NR2 = y[10]
        NR3 = y[11]
        NI = y[12]
        ND = y[13]
        NNag = y[14]
        NKg = y[15]
        NClg = y[16]
        NCag = y[17]
        NGlug = y[18]
        Vtemp = y[19]
        Wi = y[20]
        Wg = y[21]
        Wp = y[22]
        NNap = y[23]
        NKp = y[24]
        NClp = y[25]
        NCap = y[26]
        mp = y[27]
        hp = y[28]
        np = y[29]
        AMPA2A = y[30]
        AMPA2D = y[31]
        #AMPA1A = y[32]
        #NMDAA = y[33]

    if p.nosynapse:
        synapse_block = 0
    else:
        synapse_block = 1

    # Ionic amounts and concentrations
    # ECS
    We = p.Wtot - Wi - Wg - Wp
    NNae = p.CNa - NNag - NNa - NNap
    NKe = p.CK - NKg - NK - NKp
    NCle = p.CCl - NClg - NCl - NClp
    NaCe = NNae/We
    KCe = NKe/We
    ClCe = NCle/We
    # Presynaptic Neuron
    NGlui = NI
    NaCi = NNa/Wi
    KCi = NK/Wi
    ClCi = NCl/Wi
    CaCi = NCai/p.VolPreSyn
    GluCi = NGlui/p.VolPreSyn
    # Postsynaptic Neuron

    NaCp = NNap / Wp
    KCp = NKp / Wp
    ClCp = NClp / Wp
    CaCp = NCap / Wp

    # Astrocyte
    NaCg = NNag/Wg
    KCg = NKg/Wg
    ClCg = NClg/Wg
    GluCg = NGlug/p.VolPAP
    CaCg = NCag/p.VolPAP
    # Cleft
    NCac = p.CCa - NCai - NCag
    NGluc = p.CGlu - NGlui - NGlug - ND - NN - NR - NR1- NR2 - NR3
    CaCc = NCac/p.Volc
    GluCc = NGluc/p.Volc
    #print(GluCc)
    #tprint(GluCc)
    #Joel Glutamat: adds 150mM = 0.15M
    # Voltages
    if 'excite' in p.__dict__.keys():
        V = Vtemp
    else:
        V = p.F/p.C*(NNa+NK+synapse_block*2*NCai-synapse_block*(NGlui+NN+NR+NR1+NR2+NR3+ND)-NCl-p.NAi)
    Vi = V # Needed for plotting
    Vg = p.F/p.Cg*(NNag + NKg + p.NBg - p.NAg - NClg +
                   synapse_block*2*NCag - synapse_block*NGlug)
    Vp = p.F / p.C * (NNap + NKp + synapse_block * 2 * NCap - NClp - p.NAp + p.NBp)


    # ==========================================================================
    # --------------------NEURON-------------------------------------------------
    # ===========================================================================

    alpham = 0.32*(V+52)/(1-exp(-(V+52)/4))
    betam = 0.28*(V+25)/(exp((V+25)/5)-1)
    alphah = 0.128*exp(-(V+53)/18)
    betah = 4/(1+exp(-(V+30)/5))
    alphan = 0.016*(V+35)/(1-exp(-(V+35)/5))
    betan = 0.25*exp(-(V+50)/40)

    if p.nogates:
        gates_block = 0
        m = alpham/(alpham + betam)
        h = alphah/(alphah + betah)
        n = alphan/(alphan + betan)
    else:
        gates_block = 1   

    # Gated currents
    INaG = p.PNaG*(m**3)*(h)*(p.F**2)*(V)/(
       p.R*p.T)*((NaCi -
                  NaCe*exp(-(p.F*V)/(p.R*p.T)))/(
                     1-exp(-(p.F*V)/(p.R*p.T))))
    IKG = (p.PKG*(n**2))*(p.F**2)*(V)/(
       p.R*p.T)*((KCi -
                  KCe*exp(-(p.F*V)/(p.R*p.T)))/(
                     1-exp(-p.F*V/(p.R*p.T))))
    IClG = p.PClG*1/(1+exp(-(V+10)/10))*(
       p.F**2)*V/(p.R*p.T)*((ClCi -
                             ClCe*exp(p.F*V/(p.R*p.T)))/(
                                1-exp(p.F*V/(p.R*p.T))))
    ICaG = p.PCaG*m**2*h*4*p.F/(
       p.R*p.T)*V*((CaCi-
                    CaCc*exp(-2*(p.F*V)/(p.R*p.T)))/(
                       1-exp(-2*(p.F*V)/(p.R*p.T))))

    # Leak currents
    INaLi = p.PNaLi*(p.F**2)/(
       p.R*p.T)*V*((NaCi -
                    NaCe*exp((-p.F*V)/(p.R*p.T)))/(
                       1-exp((-p.F*V)/(p.R*p.T))))
    IKLi = p.PKLi*p.F**2/(p.R*p.T)*V*((
       KCi -
       KCe*exp((-p.F*V)/(p.R*p.T)))/(
          1-exp((-p.F*V)/(p.R*p.T))))
    IClLi = p.PClLi*(p.F**2)/(
       p.R*p.T)*V*((ClCi -
                    ClCe*exp((p.F*V)/(p.R*p.T)))/(
                       1-exp((p.F*V)/(p.R*p.T))))
    ICaLi = 4*p.PCaLi*(p.F**2)/(
       p.R*p.T)*V*((CaCi -
                    CaCc*exp((-2*p.F*V)/(p.R*p.T)))/(
                       1-exp((-2*p.F*V)/(p.R*p.T))))
    IGluLi = p.PGluLi*p.F**2/(
       p.R*p.T)*V*((GluCi -
                    GluCc*exp((p.F*V)/(p.R*p.T)))/(
                       1-exp((p.F*V)/(p.R*p.T))))

    # Blockade
    blockerExp = 1/(1+exp(p.beta1*(t-p.tstart))) + 1/(
       1+exp(-p.beta2*(t-p.tend)))
    blockerExpAlt = 1/(1+exp(p.beta1*(t-p.tstart))) + p.perc/(
       1+exp(-p.beta2*(t-p.tend)))
    blockerExp = p.perc + (1-p.perc)*blockerExp
    #blockerExp = blockerExpAlt

    # Na-K pump
    sigmapump = 1/7*(exp(NaCe/67.3)-1)
    fpump = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*V) +
               0.0365*sigmapump*exp(-p.F/p.R/p.T*V))
    Ipumpi = blockerExp*p.pumpScaleNeuron*fpump*p.PNKAi*(
                NaCi**(1.5)/(NaCi**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))

    # KCl cotransport
    JKCl = p.UKCl*p.R*p.T/p.F*(log(KCi)+log(ClCi)-log(KCe)-log(ClCe))

    # NCX
    INCXi = p.PNCXi*(NaCe**3)/(p.alphaNaNCX**3+NaCe**3)*(
       CaCc/(p.alphaCaNCX+CaCc))*(
          NaCi**3/NaCe**3*exp(p.eNCX*p.F*V/p.R/p.T) -
          CaCi/CaCc*exp((p.eNCX-1)*p.F*V/p.R/p.T))/(
             1+p.ksatNCX*exp((p.eNCX-1)*p.F*V/p.R/p.T))

    # EAAT
    JEAATi = p.PEAATi*p.R*p.T/p.F*log(NaCe**3/NaCi**3 *
                                    KCi/KCe*p.HeOHai*GluCc/GluCi)

    # =========================================================================
    # ---------------------------------------------------------------------
    # ========================================================================

    # ===========================================================================
    # --------------------------hier postsynapse-----------------------------------------
    # ============================================================================
    alphamp = 0.32 * (Vp + 52) / (1 - exp(-(Vp + 52) / 4))
    betamp = 0.28 * (Vp + 25) / (exp((Vp + 25) / 5) - 1)
    alphahp = 0.128 * exp(-(Vp + 53) / 18)
    betahp = 4 / (1 + exp(-(Vp + 30) / 5))
    alphanp = 0.016 * (Vp + 35) / (1 - exp(-(Vp + 35) / 5))
    betanp = 0.25 * exp(-(Vp + 50) / 40)

    if p.nogates:
        gates_block = 0
        mp = alphamp / (alphamp + betamp)
        hp = alphahp / (alphahp + betahp)
        np = alphanp / (alphanp + betanp)
    else:
        gates_block = 1

        # Gated currents
    INaGp = p.PNaGp * (mp ** 3) * (hp) * (p.F ** 2) * (Vp) / (
            p.R * p.T) * ((NaCp -
                           NaCe * exp(-(p.F * Vp) / (p.R * p.T))) / (
                                  1 - exp(-(p.F * Vp) / (p.R * p.T))))
    IKGp = (p.PKG * (np ** 2)) * (p.F ** 2) * (Vp) / (
            p.R * p.T) * ((KCp -
                           KCe * exp(-(p.F * Vp) / (p.R * p.T))) / (
                                  1 - exp(-p.F * Vp / (p.R * p.T))))
    IClGp = p.PClG * 1 / (1 + exp(-(Vp + 10) / 10)) * (
            p.F ** 2) * Vp / (p.R * p.T) * ((ClCp -
                                            ClCe * exp(p.F * Vp / (p.R * p.T))) / (
                                                   1 - exp(p.F * Vp / (p.R * p.T))))
    ICaGp = p.PCaG * mp ** 2 * hp * 4 * p.F / (
            p.R * p.T) * Vp * ((CaCp -
                               CaCc * exp(-2 * (p.F * V) / (p.R * p.T))) / (
                                      1 - exp(-2 * (p.F * V) / (p.R * p.T))))

    # Leak currents
    INaLp = p.PNaLi * (p.F ** 2) / (
            p.R * p.T) * Vp * ((NaCp -
                               NaCe * exp((-p.F * Vp) / (p.R * p.T))) / (
                                      1 - exp((-p.F * Vp) / (p.R * p.T))))
    IKLp = p.PKLi * p.F ** 2 / (p.R * p.T) * Vp * ((
                                KCp - KCe * exp((-p.F * Vp) / (p.R * p.T))) / (
                                    1 - exp((-p.F * Vp) / (p.R * p.T))))
    IClLp = p.PClLi * (p.F ** 2) / (
            p.R * p.T) * Vp * ((ClCp -
                               ClCe * exp((p.F * Vp) / (p.R * p.T))) / (
                                      1 - exp((p.F * Vp) / (p.R * p.T))))
    ICaLp = 4 * p.PCaLi * (p.F ** 2) / (
            p.R * p.T) * Vp * ((CaCp -
                               CaCc * exp((-2 * p.F * Vp) / (p.R * p.T))) / (
                                      1 - exp((-2 * p.F * Vp) / (p.R * p.T))))
    #IGluLp = p.PGluLi * p.F ** 2 / (
            #p.R * p.T) * V * ((GluCp -
                               #GluCc * exp((p.F * Vp) / (p.R * p.T))) / (
                                      #1 - exp((p.F * Vp) / (p.R * p.T))))

    # Blockade
    blockerExp = 1 / (1 + exp(p.beta1 * (t - p.tstart))) + 1 / (
            1 + exp(-p.beta2 * (t - p.tend)))
    blockerExpAlt = 1 / (1 + exp(p.beta1 * (t - p.tstart))) + p.perc / (
            1 + exp(-p.beta2 * (t - p.tend)))
    blockerExp = p.perc + (1 - p.perc) * blockerExp
    # blockerExp = blockerExpAlt

    # Na-K pump
    sigmapumpP = 1 / 7 * (exp(NaCe / 67.3) - 1)
    fpumpP = 1 / (1 + 0.1245 * exp(-0.1 * p.F / p.R / p.T * Vp) +
                 0.0365 * sigmapumpP * exp(-p.F / p.R / p.T * Vp))
    IpumpP = blockerExp * p.pumpScaleNeuron * fpumpP * p.PNKAp * (
            NaCp ** (1.5) / (NaCp ** (1.5) + p.nka_na ** 1.5)) * (KCe / (KCe + p.nka_k))

    # KCl cotransport
    JKClp = p.UKCl * p.R * p.T / p.F * (log(KCi) + log(ClCi) - log(KCe) - log(ClCe))

    # NCX
    INCXp = p.PNCXi * (NaCe ** 3) / (p.alphaNaNCX ** 3 + NaCe ** 3) * (
            CaCc / (p.alphaCaNCX + CaCc)) * (
                    NaCp ** 3 / NaCe ** 3 * exp(p.eNCX * p.F * Vp / p.R / p.T) -
                    CaCp / CaCc * exp((p.eNCX - 1) * p.F * Vp / p.R / p.T)) / (
                    1 + p.ksatNCX * exp((p.eNCX - 1) * p.F * Vp / p.R / p.T))

    IAMPA2 = p.PAMPA2 * AMPA2A * (p.F ** 2) * (Vp) / (
            p.R * p.T) * ((NaCp -
                           NaCe * exp(-(p.F * Vp) / (p.R * p.T))) / (
                                  1 - exp(-(p.F * Vp) / (p.R * p.T))))
    # JAMPA1 = p.PAMPA1 * p.R*p.T/p.F*log(NaCe/NaCp)

    # JNMDA = p.PNMDA * p.R*p.T/p.F*log(NaCe/NaCp * KCp/KCe * CaCc/CaCp)

    CAMPA2 = 1
    AMPA2R = CAMPA2 - AMPA2D - AMPA2A
    print("AMPA2R:")
    print(AMPA2R)
    print("AMPA2A:")
    print(AMPA2A)
    print("AMPA2D:")
    print(AMPA2D)

    #print(AMPA2A)
    #print(AMPA2R)
    #CAMPA1 = 1
    #AMPA1R = CAMPA1 - AMPA1A
    #CNMDA = 1
    #NMDAR = CNMDA - NMDAA
    #initial AMPA2A0 : 0.3

    # EAAT
    #JEAATi = p.PEAATi * p.R * p.T / p.F * log(NaCe ** 3 / NaCp ** 3 *
                                              #KCp / KCe * p.HeOHai * GluCc / GluCp)
    # ===========================================================================
    # --------------------------hier postsynapse ende-----------------------------
    # ============================================================================

    k1 = p.k1max*CaCi/(CaCi+p.KM)
    gCa = CaCi/(CaCi+p.KDV)
    k2 = p.k20+gCa*p.k2cat
    kmin2cat = p.k2cat*p.kmin20/p.k20
    kmin2 = p.kmin20+gCa*kmin2cat

    # ===========================================================================
    # --------------------------ASTROCYTE-----------------------------------------
    # ============================================================================

    # Na-K pump
    sigmapumpA = 1/7*(exp(NaCe/67.3)-1)
    fpumpA = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*Vg) +
                0.0365*sigmapumpA*exp(-p.F/p.R/p.T*Vg))
    Ipumpg = p.pumpScaleAst*blockerExp*p.PNKAg*fpumpA*(
          NaCg**(1.5)/(NaCg**(1.5)+p.nka_na**1.5))*(KCe/(KCe+p.nka_k))

    # Leak
    IKLg = p.PKLg*p.F**2/(
       p.R*p.T)*Vg*((KCg -
                     KCe*exp((-p.F*Vg)/(p.R*p.T)))/(
                        1-exp((-p.F*Vg)/(p.R*p.T))))
    IClLg = p.PClLg*p.F**2/(
       p.R*p.T)*Vg*((ClCg -
                     ClCe*exp((p.F*Vg)/(p.R*p.T)))/(
                        1-exp((p.F*Vg)/(p.R*p.T))))
    INaLg = p.PNaLg*p.F**2/(
       p.R*p.T)*Vg*((NaCg -
                     NaCe*exp((-p.F*Vg)/(p.R*p.T)))/(
                        1-exp((-p.F*Vg)/(p.R*p.T))))
    IGluLg = p.PGluLg*p.F**2/(
       p.R*p.T)*Vg*((GluCg -
                     GluCc*exp((p.F*Vg)/(p.R*p.T)))/(
                        1-exp((p.F*Vg)/(p.R*p.T))))
    ICaLg = 4*p.PCaLg*p.F**2/(
       p.R*p.T)*Vg*((CaCg -
                     CaCc*exp((-2*p.F*Vg)/(p.R*p.T)))/(
                        1-exp((-2*p.F*Vg)/(p.R*p.T))))

    # NKCC1
    JNKCC1 = p.PNKCC1*p.R*p.T/p.F*(log(KCe) + log(NaCe)
                                   + 2*log(ClCe) - log(KCg)
                                   - log(NaCg) - 2*log(ClCg))

    # Kir4.1
    Vkg = p.R*p.T/p.F*log(KCe/KCg)
    minfty = 1/(2+exp(1.62*(p.F/p.R/p.T)*(Vg-Vkg)))
    IKir = p.PKir*minfty*KCe/(KCe+p.KCe_thres)*(Vg-Vkg)
    # IKir = p.GKir*(Vg-Vkg)*sqrt(KCe)/(1+exp((Vg - Vkg - 34)/19.23)))

    # GLT-1
    JEAATg = p.PEAATg*p.R*p.T/p.F*log(NaCe**3/NaCg**3*KCg/KCe *
                                    p.HeOHa*GluCc/GluCg)

    # NCX
    INCXg = p.PNCXg*(NaCe**3)/(p.alphaNaNCX**3 +
                               NaCe**3)*(CaCc/(p.alphaCaNCX+CaCc))*(
                                  NaCg**3/NaCe**3*exp(p.eNCX*p.F*Vg/p.R/p.T) -
                                  CaCg/CaCc*exp((p.eNCX-1)*p.F*Vg/p.R/p.T))/(
                                     1+p.ksatNCX*exp(
                                        (p.eNCX-1)*p.F*Vg/p.R/p.T))

    # =========================================================================
    # ----------------------------VOLUME DYNAMICS------------------------------
    # =========================================================================
    SCi = NaCi+KCi+ClCi+p.NAi/Wi
    SCp = NaCp+KCp+ClCp+p.NAp/Wp+p.NBp/Wp
    SCe = NaCe+KCe+ClCe+p.NAe/We
    SCg = NaCg + KCg + ClCg + p.NAg/Wg + p.NBg/Wg
    delpii = p.R*p.T*(SCi-SCe)
    fluxi = p.LH20i*(delpii)
    delpig = p.R*p.T*(SCg-SCe)
    fluxg = p.LH20g*(delpig)
    delpip = p.R * p.T * (SCp - SCe)
    fluxp = p.LH20p * (delpip)

    Voli = Wi/p.Wi0*100
    Volg = Wg/p.Wg0*100
    Volp = Wp/p.Wp0*100
    # =========================================================================
    # ----------------------------POSTSYNAPTIC RESPONSE------------------------
    # =========================================================================

   # IAMPA = p.gAMPA*mAMPA*(Vpost-p.VAMPA)

    # ==========================================================================
    # ----------------------------INTERVENTIONS---------------------------------
    # ==========================================================================

    if 'block' in p.__dict__.keys():
        dict_ = p.block
        for key in dict_:
            val_ = dict_[key]
            blockOther = (1/(1+exp(100*(t-val_[0]))) +
                          1/(1+exp(-100*(t-val_[1]))))
            if key == 'INaG':
                INaG = INaG*blockOther
            elif key == 'IKG':
                IKG = IKG*blockOther
            elif key == 'IClG':
                IClG = IClG*blockOther
            elif key == 'JKCl':
                JKCl = JKCl*blockOther
            elif key == 'ICaG':
                ICaG = ICaG*blockOther
            elif key == 'INCXi':
                INCXi = INCXi*blockOther
            elif key == 'JEAATi':
                JEAATi = JEAATi*blockOther
            elif key == 'IKir':
                IKir = IKir*blockOther
            elif key == 'JNKCC1':
                JNKCC1 = JNKCC1*blockOther
            elif key == 'JEAATg':
                JEAATg = JEAATg*blockOther
            elif key == 'INCXg':
                INCXg = INCXg*blockOther
            elif key == 'WaterN':
                fluxi = fluxi*blockOther
            elif key == 'WaterA':
                fluxg = fluxg*blockOther
    if 'excite' in p.__dict__.keys():
        arg_excite = p.excite
        blocker_Excite = 1 - (1/(1+exp(100*(t-arg_excite[0]))) +
                              1/(1+exp(-100*(t-arg_excite[1]))))
        IExcite = blocker_Excite*arg_excite[2]/2/p.F*(1-signal.square(array(5*t),duty=arg_excite[3]))
        dur_ = arg_excite[3]
        duty_ = arg_excite[4]
        IExcite = blocker_Excite*arg_excite[2]/2/p.F*(1-signal.square(2*pi*array(t)*(1-duty_)/(dur_/60),duty=duty_))
        #IExcite = blocker_Excite*4.5/p.F
    else:
        IExcite = 0

    if 'astblock' in p.__dict__.keys():
        arg_astblock = p.astblock
        astblock = (1/(1+exp(500*(t-arg_astblock[0]))) +
                    1/(1+exp(-500*(t-arg_astblock[1]))))
    else:
        astblock = 1
    #timeconstants
    AMPAtaoAD = 4 #4
    AMPAtaoRA = 0.1   #0.1
    AMPAtaoAR = 10    #10
    AMPAtaoDR = 10    #100
    #NMDAtaoAD
    #NMDAtaoDR
    GluT = 5e-5

    # ==========================================================================
    # ----------------------------FINAL MODEL-----------------------------------
    # ==========================================================================
    
    ODEs = [  # Neuron
       ((-1/p.F*(INaG+INaLi+3*Ipumpi))-synapse_block*3/p.F*INCXi +
        synapse_block*3*JEAATi),
       (-1/p.F*(IKG+IKLi-2*Ipumpi)-JKCl-synapse_block*JEAATi),
       (1/p.F*(IClG+IClLi)-JKCl),
       gates_block*(alpham*(1-m)-betam*m),
       gates_block*(alphah*(1-h)-betah*h),
       gates_block*(alphan*(1-n)-betan*n),
       synapse_block*(-1/2/p.F)*(ICaG+ICaLi -INCXi),
       # GLUTAMATE RECYCLING
       (k1*ND-(p.kmin1+k2)*NN+kmin2*NR),        #N_D
       (k2*NN-(kmin2+3*p.k3*CaCi)*NR + p.kmin3*NR1),        #N_R
       (3*p.k3*CaCi*NR-(p.kmin3+2*p.k3*CaCi)*NR1+2*p.kmin3*NR2),        #N_R1
       (2*p.k3*CaCi*NR1-(2*p.kmin3+p.k3*CaCi)*NR2+3*p.kmin3*NR3),       #N_R2
       (p.k3*CaCi*NR2-(3*p.kmin3+p.k4)*NR3),                #N_R3
       synapse_block*(- NI*ND/p.trec + JEAATi + 1/p.F*IGluLi), #N_I
       (NI*ND/p.trec-k1*ND+p.kmin1*NN),                        #N_D
       # ASTROCYTE
       astblock*((-1/p.F)*(3*Ipumpg + INaLg +
                  synapse_block*3*INCXg)+JNKCC1+synapse_block*3*JEAATg),
       astblock*((-1/p.F)*(-IKir - 2*Ipumpg + IKLg)+
                 + JNKCC1-synapse_block*JEAATg),
       astblock*(2*JNKCC1 + 1/p.F*IClLg),
       synapse_block*astblock*(-1/2/p.F)*(-INCXg + ICaLg),
       synapse_block*astblock*(JEAATg + 1/p.F*IGluLg),
       0,
       # WATER
       fluxi, \
       astblock*fluxg,
        #postsyn
       fluxp,
        ((-1 / p.F * (INaGp + INaLp + 3 * IpumpP + IAMPA2)) - p.F * INCXp), #+ JAMPA #works: - p.F * INCXp
       (-1 / p.F * (IKGp + IKLp - 2 * IpumpP) - JKClp),
       (1 / p.F * (IClGp + IClLp) - JKClp),
       (-1 / 2 / p.F) * (ICaGp + ICaLp - INCXp),
       (alphamp * (1 - mp) - betamp * mp),
       (alphahp * (1 - hp) - betahp * hp),
       (alphanp * (1 - np) - betanp * np),
       (1/1+exp(GluT - GluCc)) * -AMPA2A/AMPAtaoAD + (GluCc*AMPA2R)/AMPAtaoRA - AMPA2A/AMPAtaoAR, # add (1/1+exp(GluCc - GluT))
       (1/1+exp(GluT - GluCc)) * AMPA2A/AMPAtaoAD - AMPA2D/AMPAtaoDR]
       #AMPA1A/AMPAtaoAD - AMPA2D/AMPAtaoDR]
       #NMDAA / NMDAtaoAD - AMPA2D / NMDAtaoDR]


    if 'excite' in p.__dict__.keys():
        ODEs[19] =  p.F/p.C*(ODEs[0]+ODEs[1]+synapse_block*2*(ODEs[6])-synapse_block*(ODEs[7]+ODEs[8]+ODEs[9]+ODEs[10]+ODEs[11]+ODEs[12]+ODEs[13])-ODEs[2] + IExcite)
    
    ODEs = array(ODEs)*60*1e3

    if args:
        if 'ax1' in args[0] or 'ax2' in args[0]:
            temp_ = args[0]
            return eval(temp_[3:])
        else:     
            return eval(args[0])
    else:
        return ODEs
