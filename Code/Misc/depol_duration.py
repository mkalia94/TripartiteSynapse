from tps import *
perclist = arange(0.1,0.55,0.05)
ecs = 0.2
depol_time = zeros(shape(perclist))

for j in range(size(perclist)):
    paramdict['s'] = True
    paramdict['m'] = False
    paramdict['b'] = False
    paramdict['nochargecons'] = False
    paramdict['nogates'] = False
    paramdict['pumpScaleNeuron'] = 1.8
    paramdict['pumpScaleAst'] = 1.8
    paramdict['gltScale'] = 2
    paramdict['perc'] = perclist[j]
    paramdict['tstart'] = 20
    paramdict['tend'] = 140
    paramdict['tfinal'] = 80
    fm = fmclass(paramdict)
    fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
        fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NF0, fm.NI0,
        fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0,
        fm.Vpost0, fm.Wi0, fm.Wg0]  
    t, y = solver(fm,fm.t0,fm.tfinal,fm.initvals)
    Vi = fm.model(array(t),y,'Vi')
    index_ = 0
    for i in range(size(Vi)-5):
        Vtemp = Vi[i]
        if (sum(fm.model(t[i],y[i,:])**2))<1e-1 and (t[i]>fm.tstart):
            index_ = i
            break
    if index_ == 0:
        Tdepol = -1
    else:
        Tdepol = t[index_]-fm.tstart
    depol_time[j] = Tdepol

plt.plot(array(t),Vi)
plt.show()

save('depol_time.npy',depol_time)          
        
