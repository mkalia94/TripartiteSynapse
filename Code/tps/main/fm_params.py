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
    #EAAT??
    #p.PAMPA2 = 2*1e-5
    #p.PAMPA1 = ...
    #p.PNMDA = ...


    p.PNCXi = 2*p.ncxScale*0.1*54
    p.PNCXg = p.PNCXi
    p.PNCXp = p.PNCXi

    # Glial uptake parameters
    p.PNKAg = p.PNKAi
    p.PNKAp = p.PNKAi
    p.LH20g = p.LH20i
    p.PNKCC1 = p.nkccScale*0.3*p.UKCl
    p.PKir = p.kirScale*3.7*6*10**3/p.F


    p.NF0 = p.GluCc0*p.Volc
    # p.NGlui0 = p.GluCi0*p.VolPreSyn
    p.NGluc0 = p.NF0
    p.We0 = p.alphae0*(p.Wi0 + p.Wg0 + p.Wp0)/(1-p.alphae0)
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
    p.NNap0 = p.NaCp0*p.Wp0
    p.NKp0 = p.KCp0*p.Wp0
    p.NClp0 = p.ClCp0*p.Wp0
    p.NCap0 = p.CaCp0*p.VolPostSyn
    p.CNa = p.NNai0 + p.NNae0 + p.NNag0 + p.NNap0
    p.CK = p.NKi0 + p.NKe0 + p.NKg0 + p.NKp0
    p.CCl = p.NCli0 + p.NCle0 + p.NClg0 + p.NClp0
    p.CCa = p.NCai0 + p.NCac0 + p.NCag0 + p.NCap0
    p.Wtot = p.Wi0 + p.We0 + p.Wg0 + p.Wp0
    p.AMPA2A0 = 0
    p.AMPA2D0 = 0
    p.AMPA2R0 = 1
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
    # Impermeants and conserved quantitiesNEW
    p.NAi = -p.C * p.Vi0 / p.F + 2 * p.CaCi0 * p.Wi0 - p.ClCi0 * p.Wi0 - p.GluCi0 * p.Wi0 + p.KCi0 * p.Wi0 + p.NaCi0 * p.Wi0

    p.NAe = -p.C * p.Vi0 * p.We0 / (
                p.F * p.Wi0) - p.CaCc0 * p.We0 + 3 * p.CaCi0 * p.We0 - p.ClCe0 * p.We0 - p.GluCc0 * p.We0 - p.KCe0 * p.We0 + 2 * p.KCi0 * p.We0 - p.NaCe0 * p.We0 + 2 * p.NaCi0 * p.We0

    p.NBg = p.C * p.Vg0 / (2 * p.F) - p.C * p.Vi0 * p.Wg0 / (
                2 * p.F * p.Wi0) - 3 * p.CaCg0 * p.Wg0 / 2 + 3 * p.CaCi0 * p.Wg0 / 2 - p.KCg0 * p.Wg0 + p.KCi0 * p.Wg0 - p.NaCg0 * p.Wg0 + p.NaCi0 * p.Wg0

    p.NAg = -p.C * p.Vg0 / (2 * p.F) - p.C * p.Vi0 * p.Wg0 / (
                2 * p.F * p.Wi0) + p.CaCg0 * p.Wg0 / 2 + 3 * p.CaCi0 * p.Wg0 / 2 - p.ClCg0 * p.Wg0 - p.GluCg0 * p.Wg0 + p.KCi0 * p.Wg0 + p.NaCi0 * p.Wg0

    p.NAp = -p.C * p.Vi0 * p.Wp0 / (2 * p.F * p.Wi0) - p.C * p.Vp0 / (
                2 * p.F) + 3 * p.CaCi0 * p.Wp0 / 2 + p.CaCp0 * p.Wp0 / 2 - p.ClCp0 * p.Wp0 + p.KCi0 * p.Wp0 + p.NaCi0 * p.Wp0

    p.NBp = -p.C * p.Vi0 * p.Wp0 / (2 * p.F * p.Wi0) + p.C * p.Vp0 / (
                2 * p.F) + 3 * p.CaCi0 * p.Wp0 / 2 - 3 * p.CaCp0 * p.Wp0 / 2 + p.KCi0 * p.Wp0 - p.KCp0 * p.Wp0 + p.NaCi0 * p.Wp0 - p.NaCp0 * p.Wp0

    print(p.NAi, p.NAe, p.NBg, p.NAg, p.NAp, p.NBp)
    # Impermeants and conserved quantities
    '''p.NAi = (block_synapse*2*p.NCai0 - p.NCli0 -
             block_synapse*p.NGlui0 + p.NKi0 + p.NNai0 - (p.C*p.Vi0)/p.F)
    p.NAp = (block_synapse*2*p.NCap0 - p.NClp0 + p.NKp0 + p.NNap0 - (p.C*p.Vp0)/p.F)
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
                  2*p.NNag0*p.Wi0))/(2*p.F*p.Wi0)'''

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

    # Gates postsynapse

    p.alphamp0 = 0.32 * (p.Vp0 + 52) / (1 - exp(-(p.Vp0 + 52) / 4))
    p.betamp0 = 0.28 * (p.Vp0 + 25) / (exp((p.Vp0 + 25) / 5) - 1)
    p.alphahp0 = 0.128 * exp(-(p.Vp0 + 53) / 18)
    p.betahp0 = 4 / (1 + exp(-(p.Vp0 + 30) / 5))
    p.alphanp0 = 0.016 * (p.Vp0 + 35) / (1 - exp(-(p.Vp0 + 35) / 5))
    p.betanp0 = 0.25 * exp(-(p.Vp0 + 50) / 40)
    p.m0 = p.alphamp0 / (p.alphamp0 + p.betamp0)
    p.h0 = p.alphahp0 / (p.alphahp0 + p.betahp0)
    p.n0 = p.alphanp0 / (p.alphanp0 + p.betanp0)

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
        p.NaCe0**3/p.NaCi0**3*p.KCi0/p.KCe0*p.HeOHai*p.GluCc0/p.GluCi0)
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
    #---------------------------------------------------------------------------------
    # Postsynaptic Neuron leaks
    #test
    p.INaGp0 = p.PNaG * (p.mp0 ** 3) * (p.hp0) * (p.F ** 2) * (p.Vp0) / (
            p.R * p.T) * ((p.NaCp0 -
                           p.NaCe0 * exp(-(p.F * p.Vp0) / (p.R * p.T))) / (
                                  1 - exp(-(p.F * p.Vp0) / (p.R * p.T))))
    p.IKGp0 = (p.PKG * (p.np0 ** 2)) * (p.F ** 2) * (p.Vp0) / (
            p.R * p.T) * ((p.KCp0 -
                           p.KCe0 * exp(-(p.F * p.Vp0) / (p.R * p.T))) / (
                                  1 - exp(-p.F * p.Vp0 / (p.R * p.T))))

    p.IClGp0 = p.PClG * 1 / (1 + exp(-(p.Vp0 + 10) / 10)) * (p.F ** 2) * p.Vp0 / (
            p.R * p.T) * ((p.ClCp0 -
                           p.ClCe0 * exp(p.F * p.Vp0 / (p.R * p.T))) / (
                                  1 - exp(p.F * p.Vp0 / (p.R * p.T))))
    p.INaLp0 = (p.F ** 2) / (p.R * p.T) * p.Vp0 * ((
                                                           p.NaCp0 -
                                                           p.NaCe0 * exp((-p.F * p.Vp0) / (p.R * p.T))) / (
                                                           1 - exp((-p.F * p.Vp0) / (p.R * p.T))))
    p.IKLp0 = p.F ** 2 / (p.R * p.T) * p.Vp0 * ((
                                                        p.KCp0 - p.KCe0 * exp((-p.F * p.Vp0) / (p.R * p.T))) / (
                                                        1 - exp((-p.F * p.Vp0) / (p.R * p.T))))
    p.IClLp0 = (p.F ** 2) / (p.R * p.T) * p.Vp0 * ((
                                                           p.ClCp0 - p.ClCe0 * exp((p.F * p.Vp0) / (p.R * p.T))) / (
                                                           1 - exp((p.F * p.Vp0) / (p.R * p.T))))
    p.JKClp0 = p.UKCl * p.R * p.T / p.F * (log(p.KCp0) +
                                          log(p.ClCp0) - log(p.KCe0) - log(p.ClCe0))
    p.sigmapumpP = 1 / 7 * (exp(p.NaCe0 / 67.3) - 1)
    p.fpumpP = 1 / (1 + 0.1245 * exp(-0.1 * p.F / p.R / p.T * p.Vp0) +
                   0.0365 * p.sigmapumpP * exp(-p.F / p.R / p.T * p.Vp0))
    p.neurPumpP = p.pumpScaleNeuron * p.PNKAp * p.fpumpP * (p.NaCp0 ** (1.5) / (
            p.NaCp0 ** (1.5) + p.nka_na ** 1.5)) * (p.KCe0 / (p.KCe0 + p.nka_k))
    p.INCXp0 = p.PNCXi * (p.NaCe0 ** 3) / (
            p.alphaNaNCX ** 3 + p.NaCe0 ** 3) * (
                       p.CaCc0 / (p.alphaCaNCX + p.CaCc0)) * (
                       p.NaCp0 ** 3 / p.NaCe0 ** 3 * exp(p.eNCX * p.F * p.Vp0 / p.R / p.T) -
                       p.CaCp0 / p.CaCc0 * exp((p.eNCX - 1) * p.F * p.Vp0 / p.R / p.T)) / (
                       1 + p.ksatNCX * exp((p.eNCX - 1) * p.F * p.Vp0 / p.R / p.T))

    #p.JAMPA20 = p.PAMPA2 * p.AMPA2A0 * (p.F ** 2) * (p.Vp0) / (
            #p.R * p.T) * ((p.NaCp0 -
                           #p.NaCp0 * exp(-(p.F * p.Vp0) / (p.R * p.T))) / (
                                  #1 - exp(-(p.F * p.Vp0) / (p.R * p.T))))

    #p.JEAATi0 = p.PEAATi * p.R * p.T / p.F * log(
        #p.NaCe0 ** 3 / p.NaCp0 ** 3 * p.KCp0 / p.KCe0 * p.HeOHai * p.GluCc0 / p.GluCp0)
    p.ICaGp0 = p.PCaG * p.mp0 ** 2 * p.hp0 * 4 * p.F / (p.R * p.T) * p.Vp0 * ((
                                                                                   p.CaCp0 - p.CaCc0 * exp(
                                                                               -2 * (p.F * p.Vp0) / (p.R * p.T))) / (
                                                                                   1 - exp(
                                                                               -2 * (p.F * p.Vp0) / (p.R * p.T))))
    p.ICaLp0 = 4 * (p.F ** 2) / (p.R * p.T) * p.Vp0 * ((
                                                               p.CaCp0 - p.CaCc0 * exp(
                                                           (-2 * p.F * p.Vp0) / (p.R * p.T))) / (
                                                               1 - exp((-2 * p.F * p.Vp0) / (p.R * p.T))))
    #p.IGluLi0 = p.F ** 2 / (p.R * p.T) * p.Vp0 * ((
                                                          #p.GluCp0 - p.GluCc0 * exp((p.F * p.Vp0) / (p.R * p.T))) / (
                                                          #1 - exp((p.F * p.Vp0) / (p.R * p.T))))

    p.PNaLp = (-p.INaGp0 - 3 * p.neurPump - block_synapse * 3 * p.INCXp0
               + block_synapse) / p.INaLp0  # Estimated sodium leak
    #                                                    conductance in neuron
    p.PKLp = (-p.IKGp0 + 2 * p.neurPump - p.F * p.JKClp0 -
              block_synapse * p.F) / p.IKLi0  # Estimated K leak conductance in neuron
    p.PClLp = (p.F * p.JKClp0 - p.IClGp0) / p.IClLp0  # Estimated Cl leak conducatance in neuron
    p.PCaLp = (-p.ICaGp0 + p.INCXp0) / p.ICaLp0


    # ---------------------------------------------------------------------------------
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
    p.JNKCC10 = p.PNKCC1*p.R*p.T/p.F*(log(p.KCe0) +
                                      log(p.NaCe0) +
                                      2*log(p.ClCe0) -
                                      log(p.KCg0) -
                                      log(p.NaCg0) - 2*log(p.ClCg0))
    p.sigmapumpA = 1/7*(exp(p.NaCe0/67.3)-1)
    p.fpumpA = 1/(1+0.1245*exp(-0.1*p.F/p.R/p.T*p.Vg0) +
                  0.0365*p.sigmapumpA*exp(-p.F/p.R/p.T*p.Vg0))
    p.astpump = p.pumpScaleAst*p.PNKAg*p.fpumpA*(p.NaCg0**(1.5)/(
        p.NaCg0**(1.5)+p.nka_na**1.5))*(
            p.KCe0/(p.KCe0+p.nka_k))
    Vkg0 = p.R*p.T/p.F*log(p.KCe0/p.KCg0)
    minfty0 = 1/(2+exp(1.62*(p.F/p.R/p.T)*(p.Vg0-Vkg0)))
    p.IKir0 = p.PKir*minfty0*p.KCe0/(p.KCe0+p.KCe_thres)*(p.Vg0-Vkg0)
    p.ICaLg0 = 4*p.F**2/(p.R*p.T)*p.Vg0*((
        p.CaCg0-p.CaCc0*exp((-2*p.F*p.Vg0)/(p.R*p.T)))/(
            1-exp((-2*p.F*p.Vg0)/(p.R*p.T))))
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
                -block_synapse*3*p.INCXg0 +
                block_synapse*3*p.JEAATg0*p.F)/p.INaLg0
    p.PKLg = (p.IKir0 + 2*p.astpump +
               p.F*p.JNKCC10-block_synapse*p.JEAATg0*p.F)/p.IKLg0
    p.PClLg = -2*p.F*p.JNKCC10/p.IClLg0
    p.PCaLg = p.INCXg0/p.ICaLg0
    #p.kRelCa = p.kRelCa*(1+1e-3)
    # -------------------------------------------------------------------------------
    
    # Glu parameters
    p.PGluLi = (p.F*p.NI0*p.ND0/p.trec - p.F*p.JEAATi0)/p.IGluLi0
    p.PGluLg = -p.F*p.JEAATg0/p.IGluLg0
    
    

    #================================================================================
    #    CHECKS CHECKS CHECKS CHECKS CHECKS
    #=============================================================================
    
    ctr = 0
    p.err = 0
    
    if (p.NAi>0) & (p.NAe>0) & (p.NAg>0) & (p.NBe>=0) & (p.NBg>0) & (p.NAp>0) & (p.NBp>0):
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
