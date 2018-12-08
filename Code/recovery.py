from sim import *
ecsratio = arange(0.1,0.9,0.05)
perclist = arange(0.1,0.9,0.1)

# ecsratio = [0.2]
# perclist = [0.7]
swellratio = zeros((size(ecsratio),size(perclist)))

for i in range(size(ecsratio)):
    for j in range(size(perclist)):
        alphae0 = ecsratio[i]
        perc = perclist[j]
        testparams = [blockerScaleAst, blockerScaleNeuron, \
        pumpScaleAst, pumpScaleNeuron, \
        nkccScale, kirScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,alphae0]
        sm = smclass(initvals,testparams)
        mod = Explicit_Problem(sm.model, initvals, t0)
        sim = CVode(mod)
        sim.atol = 1e-13
        sim.rtol = 1e-13
        sim.iter = 'Newton'
        sim.discr='BDF'
        sim.report_continuously = True
        sim.verbosity = 10
        t, y = sim.simulate(tfinal+100)
        Wi = sm.model(array(t),y,'Wi')
        swellratio[i,j] = Wi[-1]/Wi[0]
        
from matplotlib import pyplot as plt
plt.imshow(swellratio)
        
        