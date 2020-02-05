from tps import *
def negcheck_init(fm):
    negctr = 0
    for val in fm.initvals:
        if abs(val-fm.Vi0)<1e-2:
            negctr = negctr + 0
        elif val <0:
            negctr = negctr + 1
        else:
            negctr = negctr + 0

    if negctr == 0:
        disp('Initial conditions OK...')
    else:
        disp('ERROR: {a} Initial conditions have bad sign'.format(a=negctr))
