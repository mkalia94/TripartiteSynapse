from tps import *
def solver(fm, t0, tfinal, initvals):
    mod = Explicit_Problem(fm.model, initvals, t0)
    sim = CVode(mod)
    sim.atol = 1e-11
    sim.rtol = 1e-11

    sim.verbosity = 50
    
    # sim.iter = 'Newton'
    # sim.discr = 'BDF'
    # sim.linear_solver = 'SPGMR'
    # sim.report_continuously = True
    # sim.verbosity = 10
    if fm.nogates:
        t, y = sim.simulate(tfinal)
    else:
        t, y = sim.simulate(tfinal)# ,fm.tfinal*5*1e3)
    disp('Simulation Done...')
    return t, y
