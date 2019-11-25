from tps import *

def twocases(fmclass,pdict,dict1,dict2,name):
    pdict_ = pdict
    pdict_['s'] = False
    pdict_['m'] = False
    pdict_['b'] = False
    pdict_['nochargecons'] = False
    pdict_['nogates'] = False
    for key in dict1:
        if type(pdict_).__name__ == 'str':
            pdict_[key] = eval(dict1[key])
        else:
            pdict_[key] = dict1[key]
    fm = fmclass(pdict_)
    fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
               fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
            fm.Wi0, fm.Wg0]  
    t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)
    if fm.savenumpy:
        save('{a}/tfile1.npy'.format(a=fm.directory),t1)
        save('{a}/yfile1.npy'.format(a=fm.directory),y1)

    if fm.savematlab:
        sio.savemat('{a}/sim1.mat'.format(a=fm.directory),{'t':t1,'y':y1})
        
    negcheck(fm,t1,y1)
    pdict_ = pdict
    pdict_['s'] = False
    pdict_['m'] = False
    pdict_['b'] = False
    pdict_['nochargecons'] = False
    pdict_['nogates'] = False
    for key in dict2:
        pdict_[key] = dict2[key]
    fm2 = fmclass(paramdict)
    fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
                    fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
                    fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
                    fm2.Wi0, fm2.Wg0]
    t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)
    if fm.savenumpy:
        save('{a}/tfile2.npy'.format(a=fm.directory),t2)
        save('{a}/yfile2.npy'.format(a=fm.directory),y2)

    if fm.savematlab:
        sio.savemat('{a}/sim2.mat'.format(a=fm.directory),{'t':t2,'y':y2})
    negcheck(fm2,t2,y2)
    # Prepare figure
    widths = [1,1,1,1]
    heights= [0.25,1,1,1,1,1,1]
    wspace_ = 1.2
    hspace_ = 0.6
    figsizex_ = sum(widths)+(len(widths)+1)*wspace_
    figsizey_ = sum(heights)+(len(heights)+1)*hspace_
    fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
    spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                          height_ratios=heights)
    fig.subplots_adjust(wspace=wspace_)
    fig.subplots_adjust(hspace=hspace_)
    plotall(fm,t1,y1,fig,spec,1)
    plotall(fm2,t2,y2,fig,spec,2)
    plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
    
    
