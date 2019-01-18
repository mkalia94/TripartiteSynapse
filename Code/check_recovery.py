from numpy import *
ii = range(6)
jj = range(2)
for i in ii:
    for j in jj:
        y = load('y{d}{e}.npy'.format(d=i,e=j))
        print('{a},{b}: {c}'.format(a=i,b=j,c=sum((y[0,:]-y[-1,:])**2)))
        