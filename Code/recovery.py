from set_up import *
ecsratio = arange(0.1,0.91,0.1)
perclist = arange(0.1,0.91,0.1)

paramdict['tstart'] = 20
paramdict['tend'] = 25
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
        get_initvals(fm_)
        fm_.tfinal = 55
        fm_.solve = True
        t,y = exec_solve(fm_)        
        Voli = fm_.model(array(t),y,'Voli[-1]')
        swellratio[i,j,:] = array([fm_.alphae0,fm_.perc,Voli])
        
#from matplotlib import pyplot as plt
#plt.imshow(swellratio[:,:,3])
#plt.show()        
        
save('minNKA_VS_alphae.npy',swellratio)
