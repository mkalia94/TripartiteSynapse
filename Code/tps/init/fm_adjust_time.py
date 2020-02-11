from tps import *
def adjust_time(fm):
    fm.tstart_old = fm.tstart
    fm.tend_old = fm.tend
    #paramdict['tstart_old'] = fm.tstart_old
    #paramdict['tend_old'] = fm.tend_old
    fm.tstart = fm.tstart_old - 1/fm.beta1*log(1/fm.perc_gray -1)
    fm.tend = fm.tend_old + 1/fm.beta2*log(1/fm.perc_gray - 1)
