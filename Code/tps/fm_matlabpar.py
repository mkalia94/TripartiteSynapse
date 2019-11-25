from tps import *
def savematlabpar(fm):
    pdict_= {}
    for key in fm.__dict__:
        if type(fm.__dict__[key]).__name__ in ['int','int64','float','float64']:
            pdict_[key]= float(fm.__dict__[key])
    sio.savemat('{a}/params.mat'.format(a=fm.directory),pdict_)
