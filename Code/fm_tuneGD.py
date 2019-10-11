from tps import *
from scipy.optimize import root



def tuneGD(x):
    alphaN = x[0]
    alphaA = x[1]
    WN = x[2]
    WA = x[3]
    
    paramdict['s'] = True
    paramdict['b'] = False
    paramdict['m'] = False
    paramdict['nochargecons'] = False
    paramdict['nogates'] = False
    paramdict['HeOHa'] = 1/alphaA
    paramdict['HeOHai'] = 1/alphaN
    paramdict['ncxScale']= 0.8
    paramdict['pumpScaleNeuron'] = 1.2
    paramdict['pumpScaleAst'] = 1.2
    paramdict['gltScale'] = 0.01
    paramdict['GluCi0'] = 1e-4
    fm = fmclass(paramdict)
    alphaNaN = alphaN
    alphaKN = alphaN
    alphaClN = 1/alphaN
    alphaGluN = 1/alphaN
    alphaCaN = alphaN**2
    alphaNaA = alphaA
    alphaKA = alphaA
    alphaClA = 1/alphaA
    alphaGluA = 1/alphaA
    alphaCaA = alphaA**2
    NaCe = fm.CNa/(fm.Wtot+WN*(1-1/alphaNaN)+WA*(1-1/alphaNaA))
    KCe = fm.CK/(fm.Wtot+WN*(1-1/alphaKN)+WA*(1-1/alphaKA))
    ClCe = fm.CCl/(fm.Wtot+WN*(1-1/alphaClN)+WA*(1-1/alphaClA))
    GluCc = fm.CGlu/(fm.Volc+fm.VolPreSyn/alphaGluN+fm.VolPAP/alphaGluA)
    CaCc = fm.CCa/(fm.CGlu/(fm.Volc+fm.VolPreSyn/alphaCaN+fm.VolPAP/alphaCaA))
    NNaN = NaCe/alphaNaN*WN
    NKN = KCe/alphaKN*WN
    NClN = ClCe/alphaClN*WN
    NGluN = GluCc/alphaGluN*fm.VolPreSyn
    NCaN = CaCc/alphaCaN*fm.VolPreSyn
    NNaA = NaCe/alphaNaA*WA
    NKA = KCe/alphaKA*WA
    NClA = ClCe/alphaClA*WA
    NGluA = GluCc/alphaGluA*fm.VolPAP
    NCaA = CaCc/alphaCaA*fm.VolPAP   
    dy = array([fm.R*fm.T/fm.F*log(alphaN)-fm.F/fm.C*(NNaN+NKN-NClN-NGluN+2*NCaN-fm.NAi),\
          fm.R*fm.T/fm.F*log(alphaA)-fm.F/fm.C*(NNaA+NKA-NClA-NGluA+2*NCaA+fm.NBg-fm.NAg),\
          (NNaN+NKN+NClN+fm.NAi)/WN-(NaCe+KCe+ClCe+(fm.NAe+fm.NBg)/(fm.Wtot-WN-WA)),\
          (NNaA+NKA+NClA+fm.NAg+fm.NBg)/WA-(NaCe+KCe+ClCe+(fm.NAe+fm.NBg)/(fm.Wtot-WN-WA))])
    disp(GluCc)
    return dy


sol2 = root(tuneGD,array([0.77999142, 1.15059609, 2.16569886, 1.73335491]))

if sol2.success:
    alphaN = sol2.x[0]
    alphaA = sol2.x[1]
    paramdict['s'] = True
    paramdict['b'] = False
    paramdict['m'] = False
    paramdict['nochargecons'] = False
    paramdict['nogates'] = False
    paramdict['HeOHa'] = 1/alphaA
    paramdict['HeOHai'] = 1/alphaN
    paramdict['ncxScale']= 0.8
    paramdict['pumpScaleNeuron'] = 1.2
    paramdict['pumpScaleAst'] = 1.2
    paramdict['gltScale'] = 0.01
    paramdict['GluCi0'] = 1e-4
    fm = fmclass(paramdict)
    alphaGluN = 1/alphaN
    alphaGluA = 1/alphaA
    GluCc = fm.CGlu/(fm.Volc+fm.VolPreSyn/alphaGluN+fm.VolPAP/alphaGluA)
    GluCi =  GluCc/alphaGluN
    GluCg =  GluCc/alphaGluA
    disp([GluCi,GluCc,GluCg])
