#Note that all parameters (except the free ones) set with value 0 will be update in fm_params
dict_ = {#
        #----------------------------------------------
        #--------FREE PARAMETERS-----------------------
        #----------------------------------------------
        #
        'blockerScaleAst' : 1.0,       # How much more should you block astrocyte pump?
        'blockerScaleNeuron' : 1.0,     # How much more should you block neuronal pump?
        'pumpScaleAst' : 1.6,           # baseline astrocyte pump strength factor
        'pumpScaleNeuron' : 1.6,        # baseline neuron pump strength factor
        'nkccScale' : 10,              # factor NKCC1 flux rate
        'kirScale' : 1.0,               # factor Kir conductance
        'gltScale' : 0.1,
        'gltScaleAst':2,
        'ncxScale' : 0.1,
        'nka_na' : 13.0,
        'nka_k' : 0.2,
        'beta1' : 4,                  # sigmoidal rate NKA blockade onset
        'beta2' : 4,                  # sigmoidal rate NKA blockade offset
        'perc' : 0.0,                   # Perc of baseline blocked NKA
        'tstart' : 20.0,                # Start blockade
        'tend' : 80.0,                  # End blockade
        't0':0.0,
        'tfinal': 150,
        'alphae0' : 0.0,
        #-----------------------------------------------
        #---------FIXED PARAMETERS----------------------
        #-----------------------------------------------
        #
        'C': 20.0,                # Neuron membrane capacitance
        'F' : 96485.333,     # Faraday's constant
        'R' : 8314.4598,        # Gas constant
        'T' : 310.0,            # Temperature
        'PNaG' : 80*1e-5,        # permeability of gated Na current
        'PKG' : 40*1e-5,      # permbeability of gated K current
        'PClG' : 1.95*1e-5,      # permeability of gated Cl current
        'PNaL_base': 0.2*1e-5,
        'PKL_base': 2*1e-5,
        'PClL_base': 0.25*1e-5,
        'UKCl' : 13*1e-7,       # flux rate of KCl cotransporter
        'LH20i' : 2*1e-14 ,       # Osmotic permeability in the neuron
        'Qpump' : 54.5,
        'Cg' : 20.0,               # Astrocyte membrane capacitance
        'Vg0' : -80.0,            # Fix initial glial membrane potential
        'Vi0' : -65.5,           # Fix initial neuronal membrane potential
        'KCe_thres' : 13.0,        # Kir: Threshold for Kir gate
        'kup2' : 0.1,     # Kir: Rate of transition from low uptake to high uptake
        'PCaG' : 0.75*1e-5, # (from Naomi)
        'kNCXi' : 0, # 1/10th of NKA strength, from Oschmann (2017), spatial separation..
        'alphaNaNCX' : 87.5, # in mM
        'alphaCaNCX' : 1.38, # in mM, from Oschmann 2017
        'eNCX' : 0.35, # in mM, from Oschmann 2017
        'ksatNCX' : 0.1, # in mM, from Oschmann 2017
        'kGLTi' : 0, # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        'kGLTg' : 0, # Take max current of 0.67pA/microm^2 from Oschmann, compute avg : (.)/6
        'HeOHa' : 0.66, # from Breslin, Wade sodium microdomains..
        'HeOHai':0.66,
        'Nv' : 1.5*1e4,# Naomi
        'Gv' : 2, # Naomi
        'k1max' : 1,# Naomi
        'KM' : 0.0023, # Naomi
        'KDV' : 0.1, # Naomi
        'k20' : 0.021*1e-3,  # Naomi
        'k2cat' : 20*1e-3, # Naomi
        'kmin20' : 0.017*1e-3, # Naomi
        'kmin1' : 0.05*1e-3, # Naomi
        'k3' : 4.4, # Naomi
        'kmin3' : 56*1e-3, # Naomi
        'k4' : 1.45, # Naomi
        'tinact' : 3, # Naomi
        'trec' : 30, # (instead of 800, as per Naomi) the change was made due to the new NI*ND term
        'tpost' : 50, # Naomi
        'Vpost0' : -65.5, # Emperical
        'kNCXg' : 0,
        'gAMPA' : 0.035, # Tewari Majumdar
        'VAMPA' : 0, # Tewari Majumdar
        'Rm' : 0.79, # Tewari Majumdar
        'alphaAMPA' : 1.1,  # Segev and Koch chap 1
        'betaAMPA' : 0.19, # Segev and Koch chap 1
        'perc_gray':0.95,

        # Initial concentrations and volumes (baseline rest)
        'NaCi0' : 13,
        'KCi0' : 145,
        'ClCi0' : 7,
        'CaCi0' : 0.1*1e-3, # Assumption based on Oschmann model
        'GluCi0' : 3 , # (instead of 3, which is in 'maintaining the presynaptic glutamate...Marx, Billups...2015)' note that this indicates total Glu, which includes all non-free states as well
        'NaCe0' : 152,
        'KCe0' : 3,
        'ClCe0' : 135,
        'CaCc0' : 1.8, # Oschmann
        'GluCc0' : 1*1e-4,
        'NaCg0' : 13,
        'KCg0' : 80,
        'ClCg0' : 35,
        'CaCg0' : 0.11*1e-3,
        'GluCg0' : 2,
        'Wi0' : 2,
        'Wg0' : 1.7,
        'VolPreSyn' : 1*1e-3,
        'VolPAP' : 1*1e-3,
        'Volc' : 1*1e-3,
        'NF0' : 0,
        'NGlui0' : 0,
        'NGluc0' : 0,
        'We0' : 0,
        'NNai0' : 0,
        'NKi0' : 0,
        'NCli0' : 0,
        'NCai0' : 0,
        'NNae0' : 0,
        'NKe0' : 0,
        'NCle0' : 0,
        'NCac0' : 0,
        'NNag0' : 0,
        'NKg0' : 0,
        'NClg0' : 0,
        'NCag0' : 0,
        'NGlug0' : 0,
        'CNa' : 0,
        'CK' : 0,
        'CCl' : 0,
        'CCa' : 0,
        'Wtot' : 0,
        'NAi' : 0,
        'NAe' : 0,
        'NBe' : 0,
        'NAg' : 0,
        'NBg' : 0,
        # Gates
        'alpham0' : 0,
        'betam0' : 0,
        'alphah0' : 0,
        'betah0' : 0,
        'alphan0' : 0,
        'betan0' : 0,
        'm0' : 0,
        'h0' : 0,
        'n0' : 0,
        # Neuronal leaks
        'INaG0' : 0,
        'IKG0' : 0,
        'IClG0' : 0,
        'INaL0' : 0,
        'IKL0' : 0,
        'IClL0' : 0,
        'JKCl0' : 0,
        'sigmapump' : 0,
        'fpump' : 0,
        'neurPump' : 0,
        'INCXi0' : 0,
        'fGLTi0' : 0,
        'ICaG0' : 0,
        'ICaL0' : 0,
        'fRelGlui0' : 0,
        'PNaL' : 0,            # Estimated sodium leak conductance in neuron
        'PKL' : 0,   # Estimated K leak conductance in neuron
        'PClL' : 0,              # Estimated Cl leak conducatance in neuron
        'PCaL' : 0,
        # Glial uptake parameters
        'kActive' : 0,
        'LH20g' : 0,
        'gNKCC1' : 0,
        'GKir' : 0,
        #-----------------------------------------------------------------------------------------------
        # Astrocyte leaks
        'fRelK0' : 0,
        'fRelCl0' : 0,
        'fRelNa0' : 0,
        'fNKCC10' : 0,
        'sigmapumpA' : 0,
        'fpumpA' : 0,
        'fActive0': 0,
        'IKir0' : 0,
        'fRelGlu0' : 0,
        'fRelCa0' : 0,
        'fGLTg0' : 0,
        'INCXg0' : 0,
        'fRelGlu0' : 0,
        'k1init' : 0,
        'gCainit' : 0,
        'k2init' : 0,
        'kmin2catinit' : 0,
        'kmin2init' : 0,
        'kRelNa' : 0,
        'kRelK' : 0,
        'kRelCl' : 0,
        'kRelCa' : 0,
        #---------------------------------------------------------------------------------------------------------
        #Glutamate recycling initial conditions
        'NI0' : 0,
        'ND0' : 0,
        'NN0' : 0,
        'NR0' : 0,
        'NR10' : 0,
        'NR20' : 0,
        'NR30' : 0,
        'kRelGlui' : 0,
        'kRelGlu' : 0,
        'CGlu' : 0}

