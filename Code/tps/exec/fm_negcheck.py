from tps import *
def negcheck(fm,t,y):
    negcheck_ = 0
    for i in range(len(t)):
        for j in range(len(fm.initvals)):
            if j != 19:
                if y[i,j]<-1e-8:
                    negcheck_ = 1
    if negcheck_ == 0:
        disp('Positivity check ...OK')
    else:
        fm.status = fm.status + 'ERROR: Negative states obtained after solve. '
        disp('ERROR: Negative states!')
    return    
