from tps import *
ecsratio = arange(0.1,0.9,0.1)
perclist = arange(0.1,0.9,0.1)

# ecsratio = [0.2]
# perclist = [0.7]
swellratio = zeros((size(ecsratio),size(perclist),4))

for i in range(size(ecsratio)):
    for j in range(size(perclist)):
        paramdict['s'] = False
        paramdict['m'] = False
        paramdict['b'] = False
        paramdict['nochargecons'] = False
        paramdict['nogates'] = False
        paramdict['alphae0'] = ecsratio[i]
        paramdict['perc'] = perclist[j]
        paramdict['pumpScaleNeuron'] = 1.8
        paramdict['pumpScaleAst'] = 1.8
        paramdict['gltScale'] = 2
        paramdict['tstart'] = 20
        paramdict['tend'] = 45
        paramdict['tfinal'] = 120
        fm = fmclass(paramdict)
        fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NF0, fm.NI0,
            fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0,
            fm.Vpost0, fm.Wi0, fm.Wg0]  
        t, y = solver(fm,fm.t0,fm.tfinal,fm.initvals)
        Wi = fm.model(array(t),y,'Wi')
        Vi = fm.model(array(t),y,'Vi')
        swellratio[i,j,:] = (ecsratio[i],perclist[j],Wi[-1]/Wi[0]*100,Vi[-1])

plt.figure()
plt.rc('text',usetex=True)
plt.rc('font',size=20)
swellratio_temp = flip(swellratio[:,:,2],0)
plt.imshow(swellratio_temp,cmap='hot',extent=(0.1,0.8,0.1,0.8))
plt.colorbar()
plt.savefig('swellratio_short.pdf', format='pdf', bbox_inches='tight')
        
save('swellratio_short.npy',swellratio)        
        
