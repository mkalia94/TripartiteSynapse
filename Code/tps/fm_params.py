from tps import *
def parameters(p, dict_):
    p.__dict__.update(dict_)

    if p.nosynapse == 1:
        block_synapse = 0
    if p.nosynapse == 0:
        block_synapse = 1
    if p.s:
        p.alphae0 = 0.2
    if p.m:
        p.alphae0 = 0.5
    if p.b:
        p.alphae0 = 0.98

    p.kGLTi = p.gltScale*1e-5   # Take max current
    #                             0.67pA/microm^2 from Oschmann,
    #                             compute avg = (.)/6
    p.kGLTg = p.kGLTi*1
    p.kNCXi = p.ncxScale*54  # 1/10th of NKA strength,
    #                          from Oschmann (2017),
    #                          spatial separation..
    p.kNCXg = p.kNCXi
    p.NF0 = p.GluCc0*p.Volc
    p.NGlui0 = p.GluCi0*p.VolPreSyn
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
    p.INaL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((
        p.NaCi0 -
        p.NaCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IKL0 = p.F**2/(p.R*p.T)*p.Vi0*((
        p.KCi0-p.KCe0*exp((-p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vi0)/(p.R*p.T))))
    p.IClL0 = (p.F**2)/(p.R*p.T)*p.Vi0*((
        p.ClCi0-p.ClCe0*exp((p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vi0)/(p.R*p.T))))
    p.JKCl0 = p.UKCl*p.R*p.T/p.F*(log(p.KCi0) +
                                  log(p.ClCi0)-log(p.KCe0)-log(p.ClCe0))
    p.sigmapump = 1/7*(exp(p.NaCe0/67.3)-1)
    p.fpump = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*p.Vi0) +
                 0.0365*p.sigmapump*exp(-p.F/p.R/p.T*p.Vi0))
    p.neurPump = p.pumpScaleNeuron*p.Qpump*p.fpump*(p.NaCi0**(1.5)/(
        p.NaCi0**(1.5)+p.nka_na**1.5))*(p.KCe0/(p.KCe0+p.nka_k))
    p.INCXi0 = p.kNCXi*(p.NaCe0**3)/(
        p.alphaNaNCX**3+p.NaCe0**3)*(
            p.CaCc0/(p.alphaCaNCX+p.CaCc0))*(
                p.NaCi0**3/p.NaCe0**3*exp(p.eNCX*p.F*p.Vi0/p.R/p.T) -
                p.CaCi0/p.CaCc0*exp((p.eNCX-1)*p.F*p.Vi0/p.R/p.T))/(
                    1+p.ksatNCX*exp((p.eNCX-1)*p.F*p.Vi0/p.R/p.T))
    p.fGLTi0 = p.kGLTi*p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCi0**3*p.KCi0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCi0)
    p.ICaG0 = p.PCaG*p.m0**2*p.h0*4*p.F/(p.R*p.T)*p.Vi0*((
        p.CaCi0-p.CaCc0*exp(-2*(p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp(-2*(p.F*p.Vi0)/(p.R*p.T))))
    p.ICaL0 = 4*(p.F**2)/(p.R*p.T)*p.Vi0*((
        p.CaCi0-p.CaCc0*exp((-2*p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((-2*p.F*p.Vi0)/(p.R*p.T))))
    p.fRelGlui0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vi0*((
        p.GluCi0-p.GluCc0*exp((p.F*p.Vi0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vi0)/(p.R*p.T)))) 

    p.PNaL = (-p.INaG0 - 3*p.neurPump - block_synapse*3*p.INCXi0
              + block_synapse*3*p.F*p.fGLTi0)/p.INaL0  # Estimated sodium leak
    #                                                    conductance in neuron
    p.PKL = (-p.IKG0 + 2*p.neurPump - p.F*p.JKCl0 -
             block_synapse*p.F*p.fGLTi0)/p.IKL0    # Estimated K leak conductance in neuron 
    p.PClL = (p.F*p.JKCl0 - p.IClG0)/p.IClL0                 # Estimated Cl leak conducatance in neuron
    p.PCaL = (-p.ICaG0+p.INCXi0)/p.ICaL0

    # Glial uptake parameters
    p.kActive = p.Qpump*p.pumpScaleAst/p.F
    p.LH20g = p.LH20i
    p.gNKCC1 = p.nkccScale*0.03*p.UKCl
    p.GKir = p.kirScale*6*1e-2

    # ---------------------------------------------------------------------------------
    # Astrocyte leaks
    p.fRelK0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.KCg0-p.KCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fRelCl0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.ClCg0-p.ClCe0*exp((p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.fRelNa0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.NaCg0-p.NaCe0*exp((-p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-p.F*p.Vg0)/(p.R*p.T))))
    p.fNKCC10 = p.gNKCC1*p.R*p.T/p.F*(log(p.KCe0) +
                                      log(p.NaCe0) +
                                      2*log(p.ClCe0) -
                                      log(p.KCg0) -
                                      log(p.NaCg0) - 2*log(p.ClCg0))
    p.sigmapumpA = 1/7*(exp(p.NaCe0/67.3)-1)
    p.fpumpA = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*p.Vg0) +
                  0.0365*p.sigmapumpA*exp(-p.F/p.R/p.T*p.Vg0))
    p.fActive0 = p.kActive*p.fpumpA*(p.NaCg0**(1.5)/(
        p.NaCg0**(1.5)+p.nka_na**1.5))*(
            p.KCe0/(p.KCe0+p.nka_k))
    Vkg0 = p.R*p.T/p.F*log(p.KCe0/p.KCg0)
    p.GKir = p.kirScale*3.7*6*10**3/p.F/p.F
    minfty0 = 1/(2+exp(1.62*(p.F/p.R/p.T)*(p.Vg0-Vkg0)))
    p.IKir0 = p.GKir*minfty0*p.KCe0/(p.KCe0+p.KCe_thres)*(p.Vg0-Vkg0)
    p.fRelGlu0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.GluCg0-p.GluCc0*exp((p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.fRelCa0 = 4/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.CaCg0-p.CaCc0*exp((-2*p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-2*p.F*p.Vg0)/(p.R*p.T))))
    p.fGLTg0 = p.kGLTg*p.R*p.T/p.F*log(
        p.NaCe0**3/p.NaCg0**3*p.KCg0/p.KCe0*p.HeOHa*p.GluCc0/p.GluCg0)
    p.INCXg0 = p.kNCXg*(p.NaCe0**3)/(p.alphaNaNCX**3+p.NaCe0**3)*(
        p.CaCc0/(p.alphaCaNCX+p.CaCc0))*(
            p.NaCg0**3/p.NaCe0**3*exp(p.eNCX*p.F*p.Vg0/p.R/p.T) -
            p.CaCg0/p.CaCc0*exp((p.eNCX-1)*p.F*p.Vg0/p.R/p.T))/(
                1+p.ksatNCX*exp((p.eNCX-1)*p.F*p.Vg0/p.R/p.T))
    p.fRelGlu0 = 1/p.F*p.F**2/(p.R*p.T)*p.Vg0*((
        p.GluCg0-p.GluCc0*exp((p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((p.F*p.Vg0)/(p.R*p.T))))
    p.k1init = p.k1max*p.CaCi0/(p.CaCi0+p.KM)
    p.gCainit = p.CaCi0/(p.CaCi0+p.KDV)
    p.k2init = p.k20+p.gCainit*p.k2cat
    p.kmin2catinit = p.k2cat*p.kmin20/p.k20
    p.kmin2init = p.kmin20+p.gCainit*p.kmin2catinit

    p.kRelNa = (3*p.fActive0 - p.fNKCC10 +
                block_synapse*3/p.F*p.INCXg0 -
                block_synapse*3*p.fGLTg0)/p.fRelNa0
    p.kRelK = (-p.IKir0 - 2*p.fActive0 -
               p.fNKCC10+block_synapse*p.fGLTg0)/p.fRelK0
    p.kRelCl = -2*p.fNKCC10/p.fRelCl0
    p.kRelCa = -1/p.F*p.INCXg0/p.fRelCa0
    # -------------------------------------------------------------------------------
    
    # Glutamate recycling initial conditions
    p.NI0inv = (6*p.CaCi0**4*p.k1max*p.k20*p.k3**3*(
        p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV) +
              6*p.CaCi0**3*p.k1max*p.k20*p.k3**2*(
                  p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*(
                      p.k4 + 3*p.kmin3) +
              p.CaCi0*p.k1max*(2*p.CaCi0**2*p.k3**2*p.k4*(
                  3*p.CaCi0*p.k20*p.k3*(p.CaCi0 + p.KDV) +
                  p.CaCi0*(p.k20 + p.k2cat)*p.kmin20 +
                  p.k20*p.KDV*p.kmin20) + p.CaCi0*p.k3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3 + 2*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3**2 + 6*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3**3) + (p.CaCi0 + p.KM)*(2*p.CaCi0**2*p.k3**2*p.k4*(3*p.CaCi0*p.k20*p.k3*(p.KDV*(p.k20 + p.kmin1) + p.CaCi0*(p.k20 + p.k2cat + p.kmin1)) + (p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20) + p.CaCi0*p.k3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3 + 2*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3**2 + 6*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3**3) + 3*p.CaCi0**2*p.k1max*p.k20*p.k3*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*(p.CaCi0*p.k3*p.k4 + 2*p.kmin3*(p.k4 + 3*p.kmin3)) + p.CaCi0*p.k1max*p.k20*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*(2*p.CaCi0**2*p.k3**2*p.k4 + p.CaCi0*p.k3*p.k4*p.kmin3 + 2*p.kmin3**2*(p.k4 + 3*p.kmin3)) + 6*p.CaCi0**4*p.k1max*p.k20*p.k3**3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.trec)/(6*p.CaCi0**4*p.k1max*p.k20*p.k3**3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.trec)
    p.NI0 = p.NGlui0/p.NI0inv
    p.ND0 = ((p.CaCi0 + p.KM)*(2*p.CaCi0**2*p.k3**2*p.k4*(3*p.CaCi0*p.k20*p.k3*(p.KDV*(p.k20 + p.kmin1) + p.CaCi0*(p.k20 + p.k2cat + p.kmin1)) + (p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20) + p.CaCi0*p.k3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3 + 2*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3**2 + 6*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin1*p.kmin20*p.kmin3**3)*p.NI0)/(6*p.CaCi0**4*p.k1max*p.k20*p.k3**3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.trec)
    p.NN0 = (1/(6*p.CaCi0**3*p.k20*p.k3**3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.trec))*(2*p.CaCi0**2*p.k3**2*p.k4*(3*p.CaCi0*p.k20*p.k3*(p.CaCi0 + p.KDV) + p.CaCi0*(p.k20 + p.k2cat)*p.kmin20 + p.k20*p.KDV*p.kmin20) + p.CaCi0*p.k3*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3 + 2*p.k4*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3**2 + 6*(p.CaCi0*(p.k20 + p.k2cat) + p.k20*p.KDV)*p.kmin20*p.kmin3**3)*p.NI0
    p.NR0 = ((2*p.CaCi0**2*p.k3**2*p.k4 + p.CaCi0*p.k3*p.k4*p.kmin3 + 2*p.kmin3**2*(p.k4 + 3*p.kmin3))*p.NI0)/(6*p.CaCi0**3*p.k3**3*p.k4*p.trec)
    p.NR10 = ((p.CaCi0*p.k3*p.k4 + 2*p.kmin3*(p.k4 + 3*p.kmin3))*p.NI0)/(2*p.CaCi0**2*p.k3**2*p.k4*p.trec)
    p.NR20 = ((p.k4 + 3*p.kmin3)*p.NI0)/(p.CaCi0*p.k3*p.k4*p.trec)
    p.NR30 = p.NI0/(p.k4*p.trec)
    p.kRelGlui = (p.NI0/(p.trec)-p.fGLTi0)/p.fRelGlui0
    p.kRelGlu = (-p.fGLTg0 - p.fGLTi0 - p.kRelGlui*p.fRelGlui0 + p.k4*p.NR30)/p.fRelGlu0
    
    p.CGlu = p.NI0+p.NF0+p.ND0+p.NR0+p.NR10+p.NR20+p.NR30+p.NN0+p.NGlug0
    
    # Postsynaptic parameters
    p.mAMPA0 = p.alphaAMPA*p.GluCc0/(p.betaAMPA+p.alphaAMPA*p.GluCc0)
    
    
    #================================================================================
    #    CHECKS CHECKS CHECKS CHECKS CHECKS
    #=============================================================================
    
    ctr = 0
    
    if (p.NAi>0) & (p.NAe>0) & (p.NAg>0) & (p.NBe>=0) & (p.NBg>0):
        disp('Quantity of impermeants....OK')
    else:
        disp('ERROR: Quantity of an impermeant is nonpositive')
        
    if (p.kRelGlu>0) & (p.kRelNa<0) & (p.kRelK<0) & (p.kRelCl>0) & (p.kRelCa>0):
        disp('Leak cond. in astrocytes....OK')
    else:
        disp('ERROR: Sign error in astrocyte leak conductance')
        disp('kRelGlu (>0): {}'.format(p.kRelGlu))
        disp('kRelNa (<0): {}'.format(p.kRelNa))
        disp('kRelK (<0): {}'.format(p.kRelK))
        disp('kRelCl (>0): {}'.format(p.kRelCl))
        disp('kRelCa (>0): {}'.format(p.kRelCa))
        disp('----------------------------------')
    
    if (p.kRelGlui>0) & (p.PNaL>0) & (p.PKL>0) & (p.PClL>0) & (p.PCaL>0):
        disp('Leak cond. in neurons....OK')
    else:
        disp('ERROR: Sign error in neuron leak conductance')
        disp('kRelGlui (>0): {}'.format(p.kRelGlui))
        disp('PNaL (>0): {}'.format(p.PNaL))
        disp('PKL (>0): {}'.format(p.PKL))
        disp('PClL (>0): {}'.format(p.PClL))
        disp('PCaL (>0): {}'.format(p.PCaL))
        disp('----------------------------------')
