from set_up import *
ecsratio = arange(0.1,0.91,0.1)
perclist = arange(0.1,0.91,0.1)

paramdict['tstart'] = 20
paramdict['tend'] = 40
paramdict['keepbranch'] = True
# ecsratio = [0.2]
# perclist = [0.7]
swellratio = zeros((size(ecsratio),size(perclist),3))

for i in range(size(ecsratio)):
    for j in range(size(perclist)):
        alphae0 = ecsratio[i]
        perc = perclist[j]
        paramdict['perc']= perc
        paramdict['alphae0'] = alphae0
        fm_ = fmclass(paramdict)
        fm_.initvals = [fm_.NNai0, fm_.NKi0, fm_.NCli0, fm_.m0, fm_.h0, fm_.n0, fm_.NCai0,
            fm_.NN0, fm_.NR0, fm_.NR10, fm_.NR20, fm_.NR30, fm_.NI0,
               fm_.ND0, fm_.NNag0, fm_.NKg0, fm_.NClg0, fm_.NCag0, fm_.NGlug0, fm_.Vi0,
            fm_.Wi0, fm_.Wg0]
        fm_.tfinal = 300
        #fm_.nogates = True
        t,y = solver(fm_,fm_.t0,fm_.tfinal,fm_.initvals)
        
        Voli = fm_.model(array(t),y,'Voli[-1]')
        swellratio[i,j,:] = array([fm_.alphae0,fm_.perc,Voli])
        
#from matplotlib import pyplot as plt
#plt.imshow(swellratio[:,:,3])
#plt.show()        
        
save('minNKA_VS_alphae.npy',swellratio)
