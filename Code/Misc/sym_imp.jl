using SymPy
NAi = symbols("NAi",positive=true)
NAe = symbols("NAe",positive=true)
NBe = symbols("NBe",positive=true)
NAg = symbols("NAg",positive=true)
NBg = symbols("NBg",positive=true)
NAp = symbols("NAp",positive=true)
NBp = symbols("NBp",positive=true)
NaCi0,KCi0,ClCi0,CaCi0,GluCi0,Wi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,We0,NaCg0,KCg0,ClCg0,CaCg0,GluCg0,Wg0,NaCp0,KCp0,ClCp0,CaCp0,GluCp0,Wp0,CNa,CK,CCl,CCa,CGlu,Vi0,Vg0,Vp0,F,C,VolPAP, VolPreSyn, Volc, VolPostSyn= symbols("NaCi0,KCi0,ClCi0,CaCi0,GluCi0,Wi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,We0,NaCg0,KCg0,ClCg0,CaCg0,GluCg0,Wg0,NaCp0,KCp0,ClCp0,CaCp0,GluCp0,Wp0,CNa,CK,CCl,CCa,CGlu,Vi0,Vg0,Vp0,F,C,VolPAP, VolPreSyn, Volc, VolPostSyn")

ex1 = -NaCi0 - KCi0 - ClCi0 - CaCi0 - GluCi0 - NAi/Wi0 + NaCe0 + KCe0 + ClCe0 + CaCc0 + GluCc0 + NAe/We0
ex2 =-NaCg0 - KCg0 - ClCg0 - CaCg0 - GluCg0 - NAg/Wg0 - NBg/Wg0 + NaCe0 + KCe0 + ClCe0 + CaCc0 + GluCc0 + NAe/We0
ex3 = -NaCp0 - KCp0 - ClCp0 - CaCp0 - NAp/Wp0 -NBp/Wp0 + NaCe0 + KCe0 + ClCe0 + CaCc0 + GluCc0 + NAe/We0
#ex4 = CNa + CK - CCl + 2*CCa - CGlu - NAi - NAe + NBe - NAg + NBg - NAp + NBp
ex5 = (F/ C) * ((NaCi0 + KCi0 - ClCi0)*Wi0 + 2*CaCi0*VolPreSyn - GluCi0*VolPreSyn-NAi) - Vi0
ex6 = (F / C) * ((NaCg0 + KCg0 - ClCg0)*Wg0 + (2*CaCg0 - GluCg0)*VolPAP - NAg + NBg) - Vg0
ex7 = (F / C) * ((NaCp0 + KCp0 - ClCp0)*Wp0 + 2*CaCp0*VolPostSyn - NAp + NBp) - Vp0

sol = solve([ex1,ex2,ex3,ex5,ex6,ex7],NAi,NAe,NBg,NAg,NAp,NBp)
