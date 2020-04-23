#Note that all parameters (except the free ones) set with value 0 will be updated in fm_params.py
dict_ = {#
        #----------------------------------------------
        #--------FREE PARAMETERS-----------------------
        #----------------------------------------------
        #
        'pumpScaleAst' : 1.0,           # baseline astrocyte pump strength factor (Pscale)
        'pumpScaleNeuron' : 1.0,        # baseline neuron pump strength factor (Pscale)
        'nkccScale' : 1.0,              # factor NKCC1 flux rate
        'kirScale' : 1.0,               # factor Kir conductance
        'eaatScaleNeuron' : 1.0,        # factor EAAT conductance (neuron)
        'eaatScaleAst':1.0,             # factor EAAT conductance (astrocyte)
        'ncxScale' : 1.0,
        'nka_na' : 13.0,
        'nka_k' : 0.2,
        'beta1' : 4,                    # sigmoidal rate NKA blockade onset
        'beta2' : 4,                    # sigmoidal rate NKA blockade offset
        'perc' : 0.0,                   # Available energy during NKA blockade (in fraction, between 0 and 1)
        'tstart' : 20.0,                # Time of NKA blockade onset (in min.)
        'tend' : 80.0,                  # Time of NKA blockade offset (in min.)
        't0': 0.0,                   
        'tfinal': 150,                  # End time of simulation (in min.)
        'alphae0' : 0.0,                # Initial extracellular volume ratio (in fraction, between 0 and 1)
        #-----------------------------------------------
        #---------FIXED PARAMETERS----------------------
        #-----------------------------------------------
        #
        'C': 20.0,                # Neuron membrane capacitance
        'F' : 96485.333,          # Faraday's constant
        'R' : 8314.4598,          # Gas constant
        'T' : 310.0,              # Temperature
        'PNaG' : 80*1e-5,         # permeability of gated Na current
        'PKG' : 40*1e-5,          # permbeability of gated K current
        'PClG' : 1.95*1e-5,       # permeability of gated Cl current
        'PNaL_base': 0.2*1e-5,
        'PKL_base': 2*1e-5,
        'PClL_base': 0.25*1e-5,
        'UKCl' : 13*1e-7,         # flux rate of KCl cotransporter
        'LH20i' : 2*1e-14 ,       # Osmotic permeability in the neuron
        'LH20p' : 2*1e-14 ,       # Osmotic permeability in the PS neuron
        'PNKAi' : 54.5*1.6,       # Baseline NKA pump strength
        'Cg' : 20.0,              # Astrocyte membrane capacitance
        'Vg0' : -80.0,            # Fix initial glial membrane potential
        'Vi0' : -65.5,            # Fix initial neuronal membrane potential
        'Vp0' : -65.5,
        'KCe_thres' : 13.0,       # Kir: Threshold for Kir gate
        'kup2' : 0.1,             # Kir: Rate of transition from low uptake to high uptake
        'PCaG' : 2*0.75*1e-5,       # permeability of voltage-gated Ca channel
        'PNCXi' : 0,              # NCX conductance (defined in tps/fm_params.py)
        'alphaNaNCX' : 87.5,      # NCX: Na half saturation concentration
        'alphaCaNCX' : 1.38,      # NCX: Ca  half saturation concentration
        'eNCX' : 0.35,            # NCX: position of energy barrier
        'ksatNCX' : 0.1,          # NCX: saturation factor
        'PEAATi' : 0,              # EAAT: Neuronal EAAT strength (defined in tps/fm_params.py)
        'PEAATg' : 0,             # EAAT: Astrocyte EAAT strength (defined in tps/fm_params.py)
        'HeOHa' : 0.66,           # Proton ratio (ex:in) in astrocytes (fixed)
        'HeOHai':0.66,            # Proton ratio (ex:in) in neurons (fixed)
        'k1max' : 1,              # Glut recycling: Max forward reaction rate
        'KM' : 0.0023,            # Glu recycling: Ca half-saturation concentration
        'KDV' : 0.1,              # Glu recycling: Half saturation for forward reaction rate
        'k20' : 0.021*1e-3,       # Glu recycling: Uncatalysed forward reaction rate
        'k2cat' : 20*1e-3,        # Glu recycling: Catalysed forward reaction rate
        'kmin20' : 0.017*1e-3,    # Glu recycling: Uncatalysed backward reaction rate
        'kmin1' : 0.05*1e-3,      # Glu recycling: Backward reaction rate
        'k3' : 4.4,               # Glu recycling: Forward reaction rate
        'kmin3' : 56*1e-3,        # Glu recycling: Backward reaction rate
        'k4' : 1.45,              # Glu recycling: Fusion rate
        'trec' : 30,              # Glu recycling: Vesicle fusion factor
        'PNCXg' : 0,              # Astrocyte NCX conductance (defined in tps/fm_params.py)
        'perc_gray':0.95,         # Gray area in plotting starts when avaliable energy is below perc_gray

        # Initial concentrations and volumes (baseline rest)
        'NaCi0' : 13,             # Neuronal sodium concentration
        'KCi0' : 145,             # Neuronal potassium concentration               
        'ClCi0' : 7,              # Neuronal chloride concentration
        'CaCi0' : 0.1*1e-3,       # Neuronal calcium concentration
        'GluCi0' : 3 ,            # Neuronal glutamate concentration
        'NaCp0' : 13,             # PS Neuronal sodium concentration
        'KCp0' : 145,             # PS Neuronal potassium concentration
        'ClCp0' : 7,              # PS Neuronal chloride concentration
        'CaCp0' : 0.1*1e-3,       # PS Neuronal calcium concentration
        'GluCp0' : 3 ,            # PS Neuronal glutamate concentration
        'NaCe0' : 152,            # Extracellular sodium concentration
        'KCe0' : 3,               # Extracellular potassium concentration
        'ClCe0' : 135,            # Extracellular chloride concentration
        'CaCc0' : 1.8,            # Cleft calcium concentration
        'GluCc0' : 1*1e-4,        # Cleft glutamate concentration
        'NaCg0' : 13,             # Astrocyte sodium concentration
        'KCg0' : 80,              # Astrocyte potassium concentration
        'ClCg0' : 35,             # Astrocyte chloride concentration
        'CaCg0' : 0.11*1e-3,      # Astrocyte calcium concentration
        'GluCg0' : 2,             # Astrocyte glutamate concentration
        'Wi0' : 2,                # Neuronal volume
        'Wg0' : 1.7,              # Astrocyte volume
        'Wp0' : 2,                # PS Neuronal volume
        'VolPreSyn' : 1*1e-3,     # Presynaptic terminal volume (fixed)
        'VolPostSyn' : 1*1e-3,    # Postsynaptic terminal volume (fixed)
        'VolPAP' : 1*1e-3,        # Perisynaptic astrocyte process volume (fixed)
        'Volc' : 1*1e-3,          # Cleft volume (fixed)
        # RECEPTOR initials
        'AMPA2A0' : 0,
        'AMPA2D0' : 0,
        'NMDAA0': 0,
        'PAMPA2' : 0,             # AMPA2 permeability (defined in tps/fm_params.py)
        'PAMPA1' :0,              # AMPA1 permeability (defined in tps/fm_params.py)
        'PNMDA' : 0,              # NMDA permeability (defined in tps/fm_params.py)

        # All parameters below are computed/defined in tps/fm_params.py 
        'NF0' : 0,                # Fused glutamate = Cleft glutamate molar amount
        'NGlui0' : 0,             # Neuronal glutamate molar amount
        'NGluc0' : 0,             # Cleft glutamate molar amount
        'We0' : 0,                # Extracellular volume
        'NNai0' : 0,              # Neuronal sodium molar amount
        'NKi0' : 0,               # Neuronal potassium molar amount
        'NCli0' : 0,              # Neuronal chloride molar amount
        'NCai0' : 0,              # Neuronal calcium molar amount
        'NNap0' : 0,              # Neuronal sodium molar amount
        'NKp0' : 0,               # Neuronal potassium molar amount
        'NClp0' : 0,              # Neuronal chloride molar amount
        'NCap0' : 0,              # Neuronal calcium molar amount
        'NNae0' : 0,              # Extracellular sodium molar amount  
        'NKe0' : 0,               # Extracellular potassium molar amount
        'NCle0' : 0,              # Extracellular chloride molar amount
        'NCac0' : 0,              # Cleft calcium molar amount
        'NNag0' : 0,              # Astrocyte sodium molar amount
        'NKg0' : 0,               # Astrocyte potassium molar amount
        'NClg0' : 0,              # Astrocyte chloride molar amount
        'NCag0' : 0,              # Astrocyte calcium molar amount
        'NGlug0' : 0,             # Astrocyte sodium molar amount
        'CNa' : 0,                # Total molar amount of sodium in the system
        'CK' : 0,                 # Total molar amount of potassium in the system
        'CCl' : 0,                # Total molar amount of chloride in the system
        'CCa' : 0,                # Total molar amount of calcium in the system
        'Wtot' : 0,               # Total volume in the system
        'NAi' : 0,                # Molar amount of neuronal impermeant anions
        'NAp' : 0,                # PS Molar amount of neuronal impermeant anions
        'NAe' : 0,                # Molar amount of extracellular impermeant anions
        'NBe' : 0,                # Molar amount of extracellular impermeant cations
        'NAg' : 0,                # Molar amount of astrocyte impermeant anions
        'NBg' : 0,                # Molar amount of astrocyte impermeant cations
        # Gates
        'alpham0' : 0,            # Gating: alpha function for m for Vi=Vi0
        'betam0' : 0,             # Gating: beta function for m for Vi=Vi0
        'alphah0' : 0,            # Gating: alpha function for h for Vi=Vi0
        'betah0' : 0,             # Gating: beta function for h for Vi=Vi0
        'alphan0' : 0,            # Gating: alpha function for n for Vi=Vi0
        'betan0' : 0,             # Gating: beta function for n for Vi=Vi0
        'm0' : 0,                 # Gating: baseline sodium activation
        'h0' : 0,                 # Gating: baseline sodium inactivation
        'n0' : 0,                 # Gating: baseline potassium activation
        # Gates
        'alphamp0' : 0,            # Gating: alpha function for m for Vi=Vi0
        'betamp0' : 0,             # Gating: beta function for m for Vi=Vi0
        'alphahp0' : 0,            # Gating: alpha function for h for Vi=Vi0
        'betahp0' : 0,             # Gating: beta function for h for Vi=Vi0
        'alphanp0' : 0,            # Gating: alpha function for n for Vi=Vi0
        'betanp0' : 0,             # Gating: beta function for n for Vi=Vi0
        'mp0' : 0,                 # Gating: baseline sodium activation
        'hp0' : 0,                 # Gating: baseline sodium inactivation
        'np0' : 0,                 # Gating: baseline potassium activation
        # Neuronal leaks
        'INaGi0' : 0,              # Baseline neuronal sodium voltage gated channel current
        'IKGi0' : 0,               # Baseline neuronal potassium voltage gated channel current
        'IClGi0' : 0,              # Baseline neuronal chloride voltage gated channel current
        'INaLi0' : 0,              # Leak: baseline neuronal sodium leak
        'IKLi0' : 0,               # Leak: baseline neuronal potassium leak
        'IClLi0' : 0,              # Leak: baseline neuronal chloride leak
        'JKCl0' : 0,               # Baseline KCC-cotrasnporter flux
        'INaGp0' : 0,              # Baseline neuronal sodium voltage gated channel current
        'IKGp0' : 0,               # Baseline neuronal potassium voltage gated channel current
        'IClGp0' : 0,              # Baseline neuronal chloride voltage gated channel current
        'INaLp0' : 0,              # Leak: baseline neuronal sodium leak
        'IKLp0' : 0,               # Leak: baseline neuronal potassium leak
        'IClLp0' : 0,              # Leak: baseline neuronal chloride leak
        'JKClp0' : 0,               # Baseline KCC-cotrasnporter flux
        'sigmapump' : 0,           # NKA: sigma expression at baseline in neuron
        'fpump' : 0,               # NKA: g expression at baseline in neuron
        'neurPump' : 0,            # NKA: total pump current at baseline in neuron
        'INCXi0' : 0,              # NCX: baseline neuronal current
        'JEAATi0' : 0,             # EAAT: baseline neuronal current
        'ICaG0' : 0,               # Voltage-gated calcium channel: baseline neuronal current
        'ICaLi0' : 0,              # Leak: baseline neuronal calcium leak
        'IGluLi0' : 0,             # Leak: baseline neuronal glutamate leak
        'PNaLi' : 0,               # sodium leak conductance in neuron
        'PKLi' : 0,                # potassium leak conductance in neuron
        'PClLi' : 0,               # chloride leak conducatance in neuron
        'PCaLi' : 0,               # caclium leak conductance in neuron
        'ICaGp0' : 0,               # Voltage-gated calcium channel: baseline neuronal current
        'ICaLp0' : 0,              # Leak: baseline neuronal calcium leak
        'IGluLp0' : 0,             # Leak: baseline neuronal glutamate leak

        # Glial uptake parameters
        'PNKAg' : 0,             # NKA: astrocyte conductance
        'LH20g' : 0,              # Astrocyte water permeability
        'PNKCC1' : 0,             # NKCC1: astrocyte conductance
        'PKir' : 0,               # Kir4.1: astrocyte conductance
        #-----------------------------------------------------------------------------------------------
        # Astrocyte leaks
        'IKLg0' : 0,             # Baseline astrocyte potassium leak
        'IClLg0' : 0,            # Baseline astrocyte chloride leak
        'INaLg0' : 0,            # Baseline astrocyte sodium leak
        'JNKCC10' : 0,            # NKCC1: Baseline astrocyte flux
        'sigmapumpA' : 0,         # NKA: sigma expression at baseline for astrocyte
        'fpumpA' : 0,             # NKA: g expression at baseline for astrocyte
        'astpump': 0,            # NKA: total pump current at baseline for astrocyte
        'IKir0' : 0,              # Baseline Kir channel current for astrocyte
        'IGluLg0' : 0,           # Baseline astrocyte glutamate leak
        'ICaLg0' : 0,            # Baseline astrocyte calcium leak
        'JEAATg0' : 0,             # Baseline astrocyte EAAT current
        'INCXg0' : 0,             # Baseline astrocyte NCX current
        'k1init' : 0,             # Glu recycling: k1 at baseline
        'gCainit' : 0,            # Glu recycling: gCa at baseline
        'k2init' : 0,             # Glu recycling: k2 at baseline
        'kmin2catinit' : 0,       # Glu recycling: kmin2cat at baseline
        'kmin2init' : 0,          # Glu recycling: kmin2 at baseline
        'PNaLg' : 0,             # Astrocyte sodium leak conductance
        'PKLg' : 0,              # Astrocyte potassium leak conductance
        'PClLg' : 0,             # Astrocyte chloride leak conductance
        'PCaLg' : 0,             # Astrocyte calcium leak conductance
        #---------------------------------------------------------------------------------------------------------
        #Glutamate recycling initial conditions
        'NI0' : 0,                # Molar amount of inactive=presynaptic glutamate
        'ND0' : 0,                # Molar amount of depot (D)
        'NN0' : 0,                # Molar amount of non releasable pool (N)
        'NR0' : 0,                # Molar amount of readily releasable pool (R)
        'NR10' : 0,               # Molar amount of readily releasable pool 1 (R1)
        'NR20' : 0,               # Molar amount of readily releasable pool 2 (R2)
        'NR30' : 0,               # Molar amount of readily releasable pool 3 (R3)
        'PGluLi' : 0,           # Astrocyte glutamate leak conductance
        'PGluLg' : 0,            # Neuron glutamate leak conductance
        'CGlu' : 0}               # Molar amount of total glutamate in the system

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