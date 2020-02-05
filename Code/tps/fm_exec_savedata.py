from tps import *
def exec_savedata(fm,t,y):
    if fm.savematlabpar:
        savematlabpar(fm)

    # Save numpy files
    if fm.savenumpy:
        save('{a}/tfile.npy'.format(a=fm.directory),t)
        save('{a}/yfile.npy'.format(a=fm.directory),y)

    if fm.savematlab:
        sio.savemat('{a}/sim.mat'.format(a=fm.directory),{'t':t,'y':y})
