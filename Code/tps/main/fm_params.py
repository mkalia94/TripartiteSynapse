from tps import *


def parameters(p, dict_):
    p.__dict__.update(dict_)

    if p.nosynapse:
        block_synapse = 0
    if p.nosynapse == False:
        block_synapse = 1
    if p.alphae0 == 0:
        if p.s:
            p.alphae0 = 0.2
        elif p.m:
            p.alphae0 = 0.5
        elif p.b:
            p.alphae0 = 0.98
        else:
            p.alphae0 = 0.2

    p.PEAATg = p.eaatScaleAst*2*1e-5
    p.PEAATi = p.eaatScaleNeuron*1e-6
    p.PNCXi = 5.7 # 1/15 of NKA strength
    p.PNCXg = p.PNCXi    
    # Glial uptake parameters
    p.PNKAg = p.PNKAi
    p.LH20g = p.LH20i
    p.PNKCC1 = p.nkccScale*7.3215*1e-7 # From OSTBY
    p.PKir = p.kirScale*0.286102 # From Dronne
    p.gNMDA_Na = p.NMDAscale*p.gNMDA_Na
    p.gNMDA_K = p.NMDAscale*p.gNMDA_K
    p.gNMDA_Ca = p.NMDAscale*p.gNMDA_Ca
    p.UKClg = p.UKClg*p.KCCscale

    p.NF0 = p.GluCc0*p.Volc
    p.NGluc0 = p.NF0
    p.We0 = p.alphae0*(p.Wi0 + p.Wg0)/(1-p.alphae0)
    p.NNai0 = p.NaCi0*p.Wi0
    p.NKi0 = p.KCi0*p.Wi0
    p.NCli0 = p.ClCi0*p.Wi0
    p.NCai0 = p.CaCi0*p.VolPreSyn
    p.NNae0 = p.NaCe0*p.We0
    p.NKe0 = p.KCe0*p.We0
    p.NCle0 = p.ClCe0*p.We0
    p.NCac0 = p.CaCc0*p.Volc
    p.NGluc0 = p.NF0
    p.NNag0 = p.NaCg0*p.Wg0
    p.NKg0 = p.KCg0*p.Wg0
    p.NClg0 = p.ClCg0*p.Wg0
    p.NCag0 = p.CaCg0*p.VolPAP
    p.NGlug0 = p.GluCg0*p.VolPAP

    p.CNa = p.NNai0 + p.NNae0 + p.NNag0
    p.CK = p.NKi0 + p.NKe0 + p.NKg0
    p.CCl = p.NCli0 + p.NCle0 + p.NClg0
    p.CCa = p.NCai0 + p.NCac0 + p.NCag0
    p.Wtot = p.Wi0 + p.We0 + p.Wg0

    #-------------------------------------------------------------
    # Glutamate recycling initial conditions
    # -----------------------------------------------------------

    p.k1init = p.k1max*p.CaCi0/(p.CaCi0+p.KM)
    p.gCainit = p.CaCi0/(p.CaCi0+p.KDV)
    p.k2init = p.k20+p.gCainit*p.k2cat
    p.kmin2catinit = p.k2cat*p.kmin20/p.k20
    p.kmin2init = p.kmin20+p.gCainit*p.kmin2catinit    
        
    p.NGluitot = p.GluCi0*p.VolPreSyn
    p.CGlu = p.NGluitot + p.NGluc0 + p.NGlug0
    p.ND0 =  (p.CGlu*(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) - 6*p.CaCi0**3*p.k1init*p.k2init*p.k3**3*p.k4*p.trec - p.NGluc0*(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) - p.NGlug0*(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3))/(6*p.CaCi0**3*p.k1init*p.k2init*p.k3**3 + 6*p.CaCi0**3*p.k1init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 11*p.CaCi0**2*p.k1init*p.k2init*p.k3**2*p.k4 + 18*p.CaCi0**2*p.k1init*p.k2init*p.k3**2*p.kmin3 + 2*p.CaCi0**2*p.k1init*p.k3**2*p.k4*p.kmin2init + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + 7*p.CaCi0*p.k1init*p.k2init*p.k3*p.k4*p.kmin3 + 18*p.CaCi0*p.k1init*p.k2init*p.k3*p.kmin3**2 + p.CaCi0*p.k1init*p.k3*p.k4*p.kmin2init*p.kmin3 + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k1init*p.k2init*p.k4*p.kmin3**2 + 6*p.k1init*p.k2init*p.kmin3**3 + 2*p.k1init*p.k4*p.kmin2init*p.kmin3**2 + 6*p.k1init*p.kmin2init*p.kmin3**3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3)
    p.NI0 = 6*p.CaCi0**3*p.k1init*p.k2init*p.k3**3*p.k4*p.trec/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3)
    p.NN0 = (-6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + p.ND0*p.k1init)/p.kmin1
    p.NR0 = (-6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4*p.kmin1/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + p.k2init*(-6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + p.ND0*p.k1init))/(p.kmin1*p.kmin2init)
    p.NR10 = (-18*p.CaCi0**4*p.ND0*p.k1init*p.k2init*p.k3**4*p.k4*p.kmin1/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) - 6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4*p.kmin1*p.kmin2init/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + 3*p.CaCi0*p.k2init*p.k3*(-6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + p.ND0*p.k1init))/(p.kmin1*p.kmin2init*p.kmin3)
    p.NR20 = (-18*p.CaCi0**5*p.ND0*p.k1init*p.k2init*p.k3**5*p.k4*p.kmin1/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) - 6*p.CaCi0**4*p.ND0*p.k1init*p.k2init*p.k3**4*p.k4*p.kmin1*p.kmin2init/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) - 3*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4*p.kmin1*p.kmin2init*p.kmin3/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + 3*p.CaCi0**2*p.k2init*p.k3**2*(-6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3*p.k4/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3) + p.ND0*p.k1init))/(p.kmin1*p.kmin2init*p.kmin3**2)
    p.NR30 = 6*p.CaCi0**3*p.ND0*p.k1init*p.k2init*p.k3**3/(6*p.CaCi0**3*p.k2init*p.k3**3*p.k4 + 6*p.CaCi0**3*p.k3**3*p.k4*p.kmin1 + 2*p.CaCi0**2*p.k3**2*p.k4*p.kmin1*p.kmin2init + p.CaCi0*p.k3*p.k4*p.kmin1*p.kmin2init*p.kmin3 + 2*p.k4*p.kmin1*p.kmin2init*p.kmin3**2 + 6*p.kmin1*p.kmin2init*p.kmin3**3)
    p.NGlui0 = p.NGluitot

    p.NMDA_C0_0 = p.Rc*p.Rd*p.Rv**2/(p.GluCc0**2*p.R0*p.Rb**2*p.Rd + p.GluCc0**2*p.Rb**2*p.Rc*p.Rd
                                     + p.GluCc0**2*p.Rb**2*p.Rc*p.Rr + p.GluCc0*p.Rb*p.Rc*p.Rd*p.Rv
                                     + p.Rc*p.Rd*p.Rv**2)
    p.NMDA_C1_0 = p.NMDA_C0_0*p.GluCc0*p.Rb/p.Rv
    p.NMDA_C2_0 = p.NMDA_C0_0*p.GluCc0**2*p.Rb**2/p.Rv**2
    p.NMDA_D_0 = p.NMDA_C0_0*p.GluCc0**2*p.Rb**2*p.Rr/p.Rv**2/p.Rd
    p.NMDA_O_0 = p.NMDA_C0_0*p.GluCc0**2*p.R0*p.Rb**2/p.Rc/p.Rv**2
    
    
    
    # Impermeants and conserved quantities
    p.NAi = (block_synapse*2*p.NCai0 - p.NCli0 -
             block_synapse*p.NGlui0 + p.NKi0 + p.NNai0 - (p.C*p.Vi0)/p.F)
    p.NAe = (p.Cg*p.Vg0*p.Wi0 + p.C*p.Vi0*(-p.We0 + p.Wi0) +
             p.F*(block_synapse*2*p.NCai0*p.We0 -
                  block_synapse*p.NGlui0*p.We0 + 2*p.NKi0*p.We0 +
                  2*p.NNai0*p.We0 + block_synapse*2*p.NCac0*p.Wi0 -
                  2*p.NCle0*p.Wi0 -
                  block_synapse*p.NGluc0*p.Wi0))/(2*p.F*p.Wi0)
    p.NBe = -((p.Cg*p.Vg0*p.Wi0 +
               p.C*p.Vi0*(p.We0 + p.Wi0) +
               p.F*(-block_synapse*2*p.NCai0*p.We0 +
                    block_synapse*p.NGlui0*p.We0 -
                    2*p.NKi0*p.We0 - 2*p.NNai0*p.We0 +
                    block_synapse*2*p.NCac0*p.Wi0 -
                    block_synapse*p.NGluc0*p.Wi0 +
                    2*p.NKe0*p.Wi0 + 2*p.NNae0*p.Wi0))/(2*p.F*p.Wi0))
    p.NAg = -((p.C*p.Vi0*p.Wg0 +
               p.Cg*p.Vg0*p.Wi0 +
               p.F*(-block_synapse*2*p.NCai0*p.Wg0 +
                    block_synapse*p.NGlui0*p.Wg0 -
                    2*p.NKi0*p.Wg0 - 2*p.NNai0*p.Wg0 -
                    block_synapse*2*p.NCag0*p.Wi0 +
                    2*p.NClg0*p.Wi0 +
                    block_synapse*p.NGlug0*p.Wi0))/(2*p.F*p.Wi0))
    p.NBg = (-p.C*p.Vi0*p.Wg0 +
             p.Cg*p.Vg0*p.Wi0 +
             p.F*(block_synapse*2*p.NCai0*p.Wg0 -
                  block_synapse*p.NGlui0*p.Wg0 + 2*p.NKi0*p.Wg0 +
                  2*p.NNai0*p.Wg0 - block_synapse*2*p.NCag0*p.Wi0 +
                  block_synapse*p.NGlug0*p.Wi0 - 2*p.NKg0*p.Wi0 -
                  2*p.NNag0*p.Wi0))/(2*p.F*p.Wi0)

    # If we ignore charge conservation and thus remove NBe (this might be useful
    # to adjust baseline equilibria)
    if p.nochargecons:
        p.NAe = -((p.C*p.Vi0*p.We0 +
                   p.F*(-2*p.NCai0*p.We0 + p.NGlui0*p.We0 -
                        2*p.NKi0*p.We0 - 2*p.NNai0*p.We0 +
                        p.NCle0*p.Wi0 + p.NKe0*p.Wi0 +
                        p.NNae0*p.Wi0))/(p.F*p.Wi0))
        p.NBe = 0

    p.NGlui0 = p.NI0
    p.GluCi0 = p.NGlui0/p.VolPreSyn

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
    p.INaG0 = p.PNaG*(p.m0**3)*(p.h0)*(p.F**2)*(p.Vi0)/(
        p.R*p.T)*((p.NaCi0 -
                   p.NaCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(
                       1-exp(-(p.F*p.Vi0)/(p.R*p.T))))
    p.IKG0 = (p.PKG*(p.n0**2))*(p.F**2)*(p.Vi0)/(
        p.R*p.T)*((p.KCi0 -
                   p.KCe0*exp(-(p.F*p.Vi0)/(p.R*p.T)))/(
                       1-exp(-p.F*p.Vi0/(p.R*p.T))))
    
    p.IClG0 = p.PClG*1/(1+exp(-(p.Vi0+10)/10))*(p.F**2)*p.Vi0/(
        p.R*p.T)*((p.ClCi0 -
                   p.ClCe0*exp(p.F*p.Vi0/(p.R*p.T)))/(
                       1-exp(p.F*p.Vi0/(p.R*p.T))))
    p.INaLi0 = (p.F**2)/(p.R*p.T)*p.Vi0*((
        p.NaCi0 -
        p.NaCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IKLi0 = p.F**2/(p.R*p.T)*p.Vi0*((
        p.KCi0-p.KCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IClLi0 = (p.F**2)/(p.R*p.T)*p.Vi0*((
        p.ClCi0-p.ClCe0*exp((p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vi0)/(p.R*p.T))))
    p.JKCl0 = p.UKCl*p.R*p.T/p.F*(log(p.KCi0) +
                                  log(p.ClCi0)-log(p.KCe0)-log(p.ClCe0))
    p.sigmapump = 1/7*(exp(p.NaCe0/67.3)-1)
    p.fpump = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*p.Vi0) +
                 0.0365*p.sigmapump*exp(-p.F/p.R/p.T*p.Vi0))
    p.neurPump = p.pumpScaleNeuron*p.PNKAi*p.fpump*(p.NaCi0**(1.5)/(
        p.NaCi0**(1.5)+p.nka_na**1.5))*(p.KCe0/(p.KCe0+p.nka_k))
    p.INCXi0 = p.PNCXi*(p.NaCe0**3)/(
        p.alphaNaNCX**3+p.NaCe0**3)*(
            p.CaCc0/(p.alphaCaNCX+p.CaCc0))*(
                p.NaCi0**3/p.NaCe0**3*exp(p.eNCX*p.F*p.Vi0/p.R/p.T) -
                p.CaCi0/p.CaCc0*exp((p.eNCX-1)*p.F*p.Vi0/p.R/p.T))/(
                    1+p.ksatNCX*exp((p.eNCX-1)*p.F*p.Vi0/p.R/p.T))
    p.JEAATi0 = p.PEAATi*p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCi0**3*p.KCi0/p.KCe0*p.HeOHai*p.GluCc0/p.GluCi0) # Option 1: Cotransporter activation gate
    p.ICaG0 = p.PCaG*p.m0**2*p.h0*4*p.F/(p.R*p.T)*p.Vi0*((
        p.CaCi0-p.CaCc0*exp(-2*(p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp(-2*(p.F*p.Vi0)/(p.R*p.T))))
    p.ICaLi0 = 4*(p.F**2)/(p.R*p.T)*p.Vi0*((
        p.CaCi0-p.CaCc0*exp((-2*p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-2*p.F*p.Vi0)/(p.R*p.T))))
    p.IGluLi0 = p.F**2/(p.R*p.T)*p.Vi0*((
        p.GluCi0-p.GluCc0*exp((p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vi0)/(p.R*p.T))))
    

    p.PNaLi = (-p.INaG0 - 3*p.neurPump - block_synapse*3*p.INCXi0
               + block_synapse*3*p.JEAATi0*p.F)/p.INaLi0  # Estimated sodium leak
    #                                                    conductance in neuron
    p.PKLi = (-p.IKG0 + 2*p.neurPump - p.F*p.JKCl0 -
              block_synapse*p.JEAATi0*p.F)/p.IKLi0    # Estimated K leak conductance in neuron 
    p.PClLi = (p.F*p.JKCl0 - p.IClG0)/p.IClLi0                 # Estimated Cl leak conducatance in neuron
    p.PCaLi = (-p.ICaG0+p.INCXi0)/p.ICaLi0


    JEAAT_g =1/(1+exp(p.EAAT_beta*(p.EAAT_th-p.GluCc0)))*p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCg0**3*p.KCg0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCg0)
    JEAAT_g =p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCg0**3*p.KCg0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCg0)
    # p.PEAATg = 9*p.JEAATi0/JEAAT_g
    
    # ----------------------------------------------------------------------------------
    # Astrocyte leaks
    p.IKLg0 = p.F**2/(p.R*p.T)*p.Vg0*((
        p.KCg0-p.KCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.IClLg0 = p.F**2/(p.R*p.T)*p.Vg0*((
        p.ClCg0-p.ClCe0*exp((p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.INaLg0 = p.F**2/(p.R*p.T)*p.Vg0*((
        p.NaCg0-p.NaCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.Mg_block0 = 1/(1+exp(-0.062*p.Vg0))*p.Mg/3.57
    p.INMDA_Na0 = p.gNMDA_Na*p.Mg_block0*p.NMDA_O_0*(p.F**2)*(p.Vg0)/(
        p.R*p.T)*((p.NaCg0 -
                   p.NaCe0*exp(-(p.F*p.Vg0)/(p.R*p.T)))/(
                       1-exp(-(p.F*p.Vg0)/(p.R*p.T))))
    p.INMDA_K0 = p.gNMDA_K*p.Mg_block0*p.NMDA_O_0*(p.F**2)*(p.Vg0)/(
        p.R*p.T)*((p.KCg0 -
                   p.KCe0*exp(-(p.F*p.Vg0)/(p.R*p.T)))/(
                       1-exp(-(p.F*p.Vg0)/(p.R*p.T))))
    p.INMDA_Ca0 = p.gNMDA_Ca*p.Mg_block0*p.NMDA_O_0*(p.F**2)*(p.Vg0)/(
        p.R*p.T)*((p.CaCg0 -
                   p.CaCc0*exp(-(p.F*p.Vg0)/(p.R*p.T)))/(
                       1-exp(-(p.F*p.Vg0)/(p.R*p.T))))
    p.JNKCC10 = p.PNKCC1*p.R*p.T/p.F*(log(p.KCe0) +
                                      log(p.NaCe0) +
                                      2*log(p.ClCe0) -
                                      log(p.KCg0) -
                                      log(p.NaCg0) - 2*log(p.ClCg0))
    p.JKClg0 = p.UKClg*p.R*p.T/p.F*(log(p.KCg0) +
                                  log(p.ClCg0)-log(p.KCe0)-log(p.ClCe0))
    p.sigmapumpA = 1/7*(exp(p.NaCe0/67.3)-1)
    p.fpumpA = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*p.Vg0) +
                  0.0365*p.sigmapumpA*exp(-p.F/p.R/p.T*p.Vg0))
    p.astpump = p.pumpScaleAst*p.fpumpA*p.PNKAg*(p.NaCg0**(1.5)/(
        p.NaCg0**(1.5)+p.nka_na_g**1.5))*(
            p.KCe0/(p.KCe0+p.nka_k_g))
    Vkg0 = p.R*p.T/p.F*log(p.KCe0/p.KCg0)
    minfty0 = 1/(2+exp(1.62*(p.F/p.R/p.T)*(p.Vg0-Vkg0)))
    p.IKir0 = p.PKir*minfty0*p.KCe0/(p.KCe0+p.KCe_thres)*(p.Vg0-Vkg0)
    p.ICaLg0 = 4*p.F**2/(p.R*p.T)*p.Vg0*((
        p.CaCg0-p.CaCc0*exp((-2*p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-2*p.F*p.Vg0)/(p.R*p.T))))
    p.JEAATg0 = 1/(1+exp(p.EAAT_beta*(p.EAAT_th-p.GluCc0)))*p.PEAATg*p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCg0**3*p.KCg0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCg0)
    if p.origEAAT >0:
        p.JEAATg0 = p.PEAATg*p.R*p.T/p.F*log(
            p.NaCe0**3/p.NaCg0**3*p.KCg0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCg0)
    p.INCXg0 = p.PNCXg*(p.NaCe0**3)/(p.alphaNaNCX**3+p.NaCe0**3)*(
        p.CaCc0/(p.alphaCaNCX+p.CaCc0))*(
            p.NaCg0**3/p.NaCe0**3*exp(p.eNCX*p.F*p.Vg0/p.R/p.T) -
            p.CaCg0/p.CaCc0*exp((p.eNCX-1)*p.F*p.Vg0/p.R/p.T))/(
                1+p.ksatNCX*exp((p.eNCX-1)*p.F*p.Vg0/p.R/p.T))
    p.IGluLg0 = p.F**2/(p.R*p.T)*p.Vg0*((
        p.GluCg0-p.GluCc0*exp((p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vg0)/(p.R*p.T))))


    p.PNaLg = (-3*p.astpump + p.F*p.JNKCC10
                -block_synapse*3*p.INCXg0 + p.INMDA_Na0 +
                block_synapse*3*p.JEAATg0*p.F)/p.INaLg0
    p.PKLg = (p.IKir0 + 2*p.astpump +
               p.F*p.JNKCC10 - p.F*p.JKClg0 -block_synapse*p.JEAATg0*p.F - p.INMDA_K0)/p.IKLg0
    p.PClLg = (-2*p.F*p.JNKCC10 + p.F*p.JKClg0)/p.IClLg0
    p.PCaLg = (p.INCXg0-p.INMDA_Ca0)/p.ICaLg0
    #p.kRelCa = p.kRelCa*(1+1e-3)
    # -------------------------------------------------------------------------------
    
    # Glu parameters
    p.PGluLi = (p.F*p.NI0*p.ND0/p.trec - p.F*p.JEAATi0)/p.IGluLi0
    p.PGluLg   = -p.F*p.JEAATg0/p.IGluLg0

    ## MOST RECENT (our baseline is unstable for alphae0 = 80%)
    if p.alphae0 == 0.8:
        p.NNai0 = 2.62555481e+01
        p.NKi0 = 2.90164201e+02
        p.NCli0 = 1.44199062e+01
        p.m0 = 1.45863462e-02
        p.h0 = 9.85797304e-01
        p.n0 = 3.23309977e-03
        p.NCai0 = 1.04358462e-07
        p.NN0 = 1.53480926e-18
        p.NR0 = 1.89122476e-18
        p.NR10 = 4.65190283e-20
        p.NR20 = 3.80040802e-22
        p.NR30 = 1.07852956e-25
        p.NI0 = 2.75071805e-03
        p.ND0 = 1.77179868e-21
        p.NNag0 = 2.40386841e+01
        p.NKg0 = 1.34390376e+02
        p.NClg0 = 5.98284913e+01
        p.NCag0 = 1.30526963e-07
        p.NGlug0 = 2.24922516e-03
        p.Vi0 = -6.55000001e+01
        p.Wi0 = 2.00265709e+00
        p.Wg0 = 1.70208082e+00
        p.NMDA_C0_0 = 5.65973148e-01
        p.NMDA_C1_0 = 2.21859297e-01
        p.NMDA_D_0 = 7.04026592e-02
        p.NMDA_O_0 = 5.47969048e-02
    
    #================================================================================
    #    CHECKS CHECKS CHECKS CHECKS CHECKS
    #=============================================================================
    
    ctr = 0
    p.err = 0
    
    if (p.NAi>0) & (p.NAe>0) & (p.NAg>0) & (p.NBe>=0) & (p.NBg>0):
        disp('Quantity of impermeants....OK')
    else:
        disp('ERROR: Quantity of an impermeant is nonpositive')
        p.err = 10
        
    if (p.PGluLg>0) & (p.PNaLg>0) & (p.PKLg>0) & (p.PClLg>0) & (p.PCaLg>0):
        disp('Leak cond. in astrocytes....OK')
    else:
        disp('ERROR: Sign error in astrocyte leak conductance')
        disp('PGluLg (>0): {}'.format(p.PGluLg))
        disp('PNaLg (<0): {}'.format(p.PNaLg))
        disp('PKLg (<0): {}'.format(p.PKLg))
        disp('PClLg (>0): {}'.format(p.PClLg))
        disp('PCaLg (>0): {}'.format(p.PCaLg))
        disp('----------------------------------')
        p.err = 10
    
    if (p.PGluLi>0) & (p.PNaLi>0) & (p.PKLi>0) & (p.PClLi>0) & (p.PCaLi>0):
        disp('Leak cond. in neurons....OK')
    else:
        disp('ERROR: Sign error in neuron leak conductance')
        disp('PGluLi (>0): {}'.format(p.PGluLi))
        disp('PNaLi (>0): {}'.format(p.PNaLi))
        disp('PKLi (>0): {}'.format(p.PKLi))
        disp('PClLi (>0): {}'.format(p.PClLi))
        disp('PCaLi (>0): {}'.format(p.PCaLi))
        disp('----------------------------------')
        p.err = 10
