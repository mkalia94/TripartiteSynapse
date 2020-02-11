from tps import *
def exec_solve(fm,*args):
    if fm.solve:
        if 'readdata' in fm.__dict__.keys():
            loc_ = fm.readdata
            if loc_ == '':
                loc_ = fm.saveloc
            t = load('SimDataImages/{a}/tfile.npy'.format(a=loc_))
            y = load('SimDataImages/{a}/yfile.npy'.format(a=loc_))
        elif args:
            t = args[0]
            y = args[1]            
        else:
            t, y = solver(fm, fm.t0, fm.tfinal, fm.initvals)

        negcheck(fm,t,y)    

        if 'excite' in fm.__dict__.keys():
            duration_ = 1.2*(fm.excite[3]/60)/(1-fm.excite[4])
            tmax = argmin(abs(array(t)-duration_))
            Vi = fm.model(array(t),y,'Vi')
            ctr = 0
            sgn = 1
            for i in range(tmax):
                sgn_old = sgn
                if abs(Vi[i])<1:
                    if i!=0:
                        sgn = sign(Vi[i]-Vi[i-1])
                        if sgn != sgn_old:
                            ctr = ctr + 1
            ctr = ctr/2+0.5
            disp('Excitation: Number of action potentials: {a}'.format(a=ctr))
                
        exec_plot(fm,t,y)
        exec_savedata(fm,t,y)
        exec_geteigs(fm,y[-1,:])

    else:
        t = 0
        y = 0
    return t,y    
