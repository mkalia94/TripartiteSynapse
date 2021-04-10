
using SymPy
C0 = symbols("C0",positive=true)
C1 = symbols("C1",positive=true)
C2 = symbols("C2",positive=true)
D = symbols("D",positive=true)
O = symbols("O",positive=true)
Rv, Rc, Rb, Rr, Rd, R0, Glu = symbols("Rv, Rc, Rb, Rr, Rd, R0, Glu")

ex1 = Rv*C1-Rb*Glu*C0
ex2 = Rb*Glu*C0-Rv*C1 + Rv*C2-Rb*Glu*C1
ex3 = Rr*C2 - Rd*D
ex4 = R0*C2-Rc*O
ex5 = simplify(-ex1- ex2-ex3-ex4)

C1_ = solve(ex1,C1)[1]
ex2_ = ex2.subs(C1,C1_)
C2_ = solve(ex2_,C2)[1]
D_ = solve(ex3.subs(C2,C2_),D)[1]
O_ = solve(ex4.subs(C2,C2_),O)[1]
ex5_ = 1-C1_-C2_-D_-O_-C0
C0_ = simplify(solve(ex5_,C0)[1])
# ex5_ = ex5.subs(C1,C1_).subs(D,D_).subs(O,O_)
# C2_ = solve(ex5_,C2)[1]
# D_ = D_.subs(C2,C2_)
# O_ = O_.subs(C2,C2_)
# ex_ = 1-C1_-C2_-D_-O_
# C0_ = simplify(solve(ex_,C0)[1])

# C1_ = simplify(C1_.subs(C0,C0_))
# C2_ = simplify(C2_.subs(C0,C0_))
# D_ = simplify(D_.subs(C0,C0_))
# O_ = simplify(O_.subs(C0,C0_))

# C1_ = Rb*Glu*C0/Rv
# ex2_ = ex7.subs(NI,NI_)
# NN_ = solve(ex7_,NN)
# ex1_ = ex1.subs(NN,NN_[1])
# NR_ = solve(ex1_,NR)
# ex2_ = ex2.subs(NR,NR_[1]).subs(NN,NN_[1])
# NR1_ = solve(ex2_,NR1)
# ex3_ = ex3.subs(NR1,NR1_[1]).subs(NR,NR_[1])
# NR2_ = solve(ex3_,NR2)
# ex4_ = ex4.subs(NR2,NR2_[1]).subs(NR1,NR1_[1])
# NR3_ = solve(ex4_,NR3)
# ex5_ = simplify(ex5.subs(NR2,NR2_[1]).subs(NR3,NR3_[1]))
# NI_ = NI_.subs(NR3,NR3_[1])

# CGlu = symbols("CGlu")
# NR3_=NI_*ND/k4/trec
# NR2_ = NR2_[1].subs(NI,NI_).subs(NR3,NR3_)
# NR1_ = NR1_[1].subs(NI,NI_).subs(NR3,NR3_)
# NR_ = NR_[1].subs(NI,NI_).subs(NR3,NR3_)
# NN_ = NN_[1].subs(NI,NI_).subs(NR3,NR3_)

# NGluc, NGlug = symbols("NGluc, NGlug")
# ex_ = NN_ + ND + NI_ + NR_ + NR1_ + NR2_ + NR3_ + NGluc + NGlug - CGlu
# ND_ = solve(ex_,ND)
