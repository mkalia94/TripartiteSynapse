using SymPy
NN = symbols("NN",positive=true)
NR = symbols("NR",positive=true)
NR1 = symbols("NR1",positive=true)
NR2 = symbols("NR2",positive=true)
NR3 = symbols("NR3",positive=true)
NI = symbols("NI",positive=true)
ND = symbols("ND",positive=true)
k1, kmin1, k2, kmin2, k3, CaCi0, kmin3, k4, trec, fGLTi, fRelGlui = symbols("k1,kmin1,k2,kmin2,k3,CaCi0,kmin3,k4, trec, fGLTi,fRelGlui")

ex1 = k1*ND-(kmin1+k2)*NN+kmin2*NR
ex2 = k2*NN-(kmin2+3*k3*CaCi0)*NR+kmin3*NR1
ex3 = 3*k3*CaCi0*NR-(kmin3+2*k3*CaCi0)*NR1+2*kmin3*NR2
ex4 = 2*k3*CaCi0*NR1-(2*kmin3+k3*CaCi0)*NR2+3*kmin3*NR3
ex5 = k3*CaCi0*NR2-(3*kmin3+k4)*NR3
ex6 = -NI*ND/trec + fGLTi+fRelGlui
ex7 = NI*ND/trec - k1*ND + kmin1*NN

NI_ = k4*NR3*trec/ND
ex7_ = ex7.subs(NI,NI_)
NN_ = solve(ex7_,NN)
ex1_ = ex1.subs(NN,NN_[1])
NR_ = solve(ex1_,NR)
ex2_ = ex2.subs(NR,NR_[1]).subs(NN,NN_[1])
NR1_ = solve(ex2_,NR1)
ex3_ = ex3.subs(NR1,NR1_[1]).subs(NR,NR_[1])
NR2_ = solve(ex3_,NR2)
ex4_ = ex4.subs(NR2,NR2_[1]).subs(NR1,NR1_[1])
NR3_ = solve(ex4_,NR3)
ex5_ = simplify(ex5.subs(NR2,NR2_[1]).subs(NR3,NR3_[1]))
NI_ = NI_.subs(NR3,NR3_[1])

CGlu = symbols("CGlu")
NR3_=NI_*ND/k4/trec
NR2_ = NR2_[1].subs(NI,NI_).subs(NR3,NR3_)
NR1_ = NR1_[1].subs(NI,NI_).subs(NR3,NR3_)
NR_ = NR_[1].subs(NI,NI_).subs(NR3,NR3_)
NN_ = NN_[1].subs(NI,NI_).subs(NR3,NR3_)

NGluc, NGlug = symbols("NGluc, NGlug")
ex_ = NN_ + ND + NI_ + NR_ + NR1_ + NR2_ + NR3_ + NGluc + NGlug - CGlu
ND_ = solve(ex_,ND)
