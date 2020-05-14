from tps import *
def get_initvals(fm):
    fm.initvals = array([fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0, fm.NN0, fm.NR0, fm.NR10, fm.NR20,
                         fm.NR30, fm.NI0, fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
                         fm.Wi0, fm.Wg0, fm.Wp0, fm.NNap0, fm.NKp0, fm.NClp0, fm.NCap0, fm.mp0, fm.hp0, fm.np0, fm.AMPA2A0, fm.AMPA2D0])
    # , fm.AMPA1A
    # fm.NMDAA0])
    # added 12 DE´s
    if fm.nogates:
        fm.initvals = fm.initvals + 1e-7*array([1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,])*fm.initvals
    else:    
        fm.initvals  = fm.initvals + 1e-5*fm.initvals
