import scipy.io as sio
from fm_class import *

dict = {'C':sm.C,
        'F' : sm.F,     # Faraday's constant
        'R' : sm.R,        # Gas constant
        'T' : sm.T,            # Temperature
        'PNaG' : sm.PNaG,        # permeability of gated Na current
        'PKG' : sm.PKG,      # permbeability of gated K current
        'PClG' : sm.PClG,      # permeability of gated Cl current
        'UKCl' : sm.UKCl,       # flux rate of KCl cotransporter
        'LH20i' : sm.LH20i,       # Osmotic permeability in the neuron
        'Qpump' : sm.Qpump,
        'Cg' : sm.Cg,               # Astrocyte membrane capacitance
        'Vg0' : sm.Vg0,            # Fix initial glial membrane potential
        'Vi0' : sm.Vi0,           # Fix initial neuronal membrane potential
        'KCe_thres' : sm.KCe_thres,        # Kir: Threshold for Kir gate
        'kup2' : sm.kup2,     # Kir: Rate of transition from low uptake to high uptake
        'PCaG' : sm.PCaG, # (from Naomi)
        'kNCXi' : sm.kNCXi, # 1/10th of NKA strength, from Oschmann (2017), spatial separation..
        'alphaNaNCX' : sm.alphaNaNCX, # in mM
        'alphaCaNCX' : sm.alphaCaNCX, # in mM, from Oschmann 2017
        'eNCX' : sm.eNCX, # in mM, from Oschmann 2017
        'ksatNCX' : sm.ksatNCX, # in mM, from Oschmann 2017
        'kGLT' : sm.kGLT, # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        'HeOHa' : sm.HeOHa, # from Breslin, Wade sodium microdomains..
        'Nv' : sm.Nv,# Naomi
        'Gv' : sm.Gv, # Naomi
        'k1max' : sm.k1max,# Naomi
        'KM' : sm.KM, # Naomi
        'KDV' : sm.KDV, # Naomi
        'k20' : sm.k20,  # Naomi
        'k2cat' : sm.k2cat, # Naomi
        'kmin20' : sm.kmin20, # Naomi
        'kmin1' : sm.kmin1, # Naomi
        'k3' : sm.k3, # Naomi
        'kmin3' : sm.kmin3, # Naomi
        'k4' : sm.k4, # Naomi
        'tinact' : sm.tinact, # Naomi
        'trec' : sm.trec, # Naomi
        'tpost' : sm.tpost, # Naomi
        'Vpost0' : sm.Vpost0, # Emperical
        'kNCXg' : sm.kNCXg,
        'gAMPA' : sm.gAMPA, # Tewari Majumdar
        'VAMPA' : sm.VAMPA, # Tewari Majumdar
        'Rm' : sm.Rm, # Tewari Majumdar
        'alphaAMPA' : sm.alphaAMPA,  # Segev and Koch chap 1p.NI0+p.NF0+p.ND0+p.NR0+p.NR10+p.NR20+p.NR30+p.NN0+p.NGlug0
        'betaAMPA' : sm.betaAMPA, # Segev and Koch chap 1
        'blockerScaleAst' : sm.blockerScaleAst,       # How much more should you block astrocyte pump?
        'blockerScaleNeuron' : sm.blockerScaleNeuron,     # How much more should you block neuronal pump?
        'pumpScaleAst' : sm.pumpScaleAst,           # baseline astrocyte pump strength factor
        'pumpScaleNeuron' : sm.pumpScaleNeuron,        # baseline neuron pump strength factor
        'nkccScale' : sm.nkccScale,              # factor NKCC1 flux rate
        'kirScale' : sm.kirScale,               # factor Kir conductance
        'gltScale' : sm.gltScale,
        'nka_na' : sm.nka_na,
        'nka_k' : sm.nka_k,
        'beta1' : sm.beta1,                  # sigmoidal rate NKA blockade onset
        'beta2' : sm.beta2,                  # sigmoidal rate NKA blockade offset
        'perc' : sm.perc,                   # Perc of baseline blocked NKA
        'tstart' : sm.tstart,                # Start blockade
        'tend' : sm.tend,                  # End blockade
        'nkccblock_after' : sm.nkccblock_after,
        'kirblock_after' : sm.kirblock_after,
        'alphae0' : sm.alphae0,
        'choice' : sm.choice,
        'astroblock' : sm.astroblock,
        'kGLT' : sm.kGLT,           # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        # Initial concentrations and volumes (baseline rest)
        'NaCi0' : sm.NaCi0,
        'KCi0' : sm.KCi0,
        'ClCi0' : sm.ClCi0,
        'CaCi0' : sm.CaCi0,
        'GluCi0' : sm.GluCi0,
        'NaCe0' : sm.NaCe0,
        'KCe0' : sm.KCe0,
        'ClCe0' : sm.ClCe0,
        'CaCc0' : sm.CaCc0,
        'GluCc0' : sm.GluCc0,
        'NaCg0' : sm.NaCg0,
        'KCg0' : sm.KCg0,
        'ClCg0' : sm.ClCg0,
        'CaCg0' : sm.CaCg0,
        'GluCg0' : sm.GluCg0,
        'Wi0' : sm.Wi0,
        'Wg0' : sm.Wg0,
        'VolPreSyn' : sm.VolPreSyn,
        'VolPAP' : sm.VolPAP,
        'Volc' : sm.Volc,
        'NF0' : sm.NF0,
        'NGlui0' : sm.NGlui0,
        'NGluc0' : sm.NGluc0,
        'We0' : sm.We0,
        'NNai0' : sm.NNai0,
        'NKi0' : sm.NKi0,
        'NCli0' : sm.NCli0,
        'NCai0' : sm.NCai0,
        'NNae0' : sm.NNae0,
        'NKe0' : sm.NKe0,
        'NCle0' : sm.NCle0,
        'NCac0' : sm.NCac0,
        'NNag0' : sm.NNag0,
        'NKg0' : sm.NKg0,
        'NClg0' : sm.NClg0,
        'NCag0' : sm.NCag0,
        'NGlug0' : sm.NGlug0,
        'CNa' : sm.CNa,
        'CK' : sm.CK,
        'CCl' : sm.CCl,
        'CCa' : sm.CCa,
        'Wtot' : sm.Wtot,
        'NAi' : sm.NAi,
        'NAe' : sm.NAe,
        'NBe' : sm.NBe,
        'NAg' : sm.NAg,
        'NBg' : sm.NBg,
        # Gates
        'alpham0' : sm.alpham0,
        'betam0' : sm.betam0,
        'alphah0' : sm.alphah0,
        'betah0' : sm.betah0,
        'alphan0' : sm.alphan0,
        'betan0' : sm.betan0,
        'm0' : sm.m0,
        'h0' : sm.h0,
        'n0' : sm.n0,
        # Neuronal leaks
        'INaG0' : sm.INaG0,
        'IKG0' : sm.IKG0,
        'IClG0' : sm.IClG0,
        'INaL0' : sm.INaL0,
        'IKL0' : sm.IKL0,
        'IClL0' : sm.IClL0,
        'JKCl0' : sm.JKCl0,
        'sigmapump' : sm.sigmapump,
        'fpump' : sm.fpump,
        'neurPump' : sm.neurPump,
        'INCXi0' : sm.INCXi0,
        'fGLTi0' : sm.fGLTi0,
        'ICaG0' : sm.ICaG0,
        'ICaL0' : sm.ICaL0,
        'fRelGlui0' : sm.fRelGlui0,
        'PNaL' : sm.PNaL,            # Estimated sodium leak conductance in neuron
        'PKL' : sm.PKL,   # Estimated K leak conductance in neuron
        'PClL' : sm.PClL,              # Estimated Cl leak conducatance in neuron
        'PCaL' : sm.PCaL,
        # Glial uptake parameters
        'kActive' : sm.kActive,
        'LH20g' : sm.LH20g,
        'gNKCC1' : sm.gNKCC1,
        'GKir' : sm.GKir,
        #-----------------------------------------------------------------------------------------------
        # Astrocyte leaks
        'fRelK0' : sm.fRelK0,
        'fRelCl0' : sm.fRelCl0,
        'fRelNa0' : sm.fRelNa0,
        'fNKCC10' : sm.fNKCC10,
        'sigmapumpA' : sm.sigmapumpA,
        'fpumpA' : sm.fpumpA,
        'fActive0': sm.fActive0,
        'IKir0' : sm.IKir0,
        'fRelGlu0' : sm.fRelGlu0,
        'fRelCa0' : sm.fRelCa0,
        'fGLTg0' : sm.fGLTg0,
        'INCXg0' : sm.INCXg0,
        'fRelGlu0' : sm.fRelGlu0,
        'k1init' : sm.k1init,
        'gCainit' : sm.gCainit,
        'k2init' : sm.k2init,
        'kmin2catinit' : sm.kmin2catinit,
        'kmin2init' : sm.kmin2init,
        'kRelNa' : sm.kRelNa,
        'kRelK' : sm.kRelK,
        'kRelCl' : sm.kRelCl,
        'kRelCa' : sm.kRelCa,
        #---------------------------------------------------------------------------------------------------------
        #Glutamate recycling initial conditions
        'NI0' : sm.NI0,
        'ND0' : sm.ND0,
        'NN0' : sm.NN0,
        'NR0' : sm.NR0,
        'NR10' : sm.NR10,
        'NR20' : sm.NR20,
        'NR30' : sm.NR30,
        'kRelGlui' : sm.kRelGlui,
        'kRelGlu' : sm.kRelGlu,
        'CGlu' : sm.CGlu}

sio.savemat('params.mat',dict)


