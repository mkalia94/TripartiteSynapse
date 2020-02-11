from tps import *

def twocases(fmclass,pdict,dict1,dict2,name):
    pdict_ = pdict
    
    for key in dict1:
        if type(pdict_).__name__ == 'str':
            pdict_[key] = eval(dict1[key])
        else:
            pdict_[key] = dict1[key]

    pdict_['tstart_old'] = pdict_['tstart']
    pdict_['tend_old'] = pdict_['tend']
    pdict_['tstart'] = pdict_['tstart_old'] - 1/pdict_['beta1']*log(1/pdict_['perc_gray'] -1)
    pdict_['tend'] = pdict_['tend_old'] + 1/pdict_['beta2']*log(1/pdict_['perc_gray'] -1)       
    fm = fmclass(pdict_)
    get_initvals(fm)
    t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)
    if fm.savenumpy:
        save('{a}/tfile1.npy'.format(a=fm.directory),t1)
        save('{a}/yfile1.npy'.format(a=fm.directory),y1)

    if fm.savematlab:
        sio.savemat('{a}/sim1.mat'.format(a=fm.directory),{'t':t1,'y':y1})
        
    negcheck(fm,t1,y1)
    pdict_ = pdict
    #pdict_['s'] = False
    #pdict_['m'] = False
    #pdict_['b'] = False
    #pdict_['nochargecons'] = False
    #pdict_['nogates'] = False
    for key in dict1:
        if type(pdict_).__name__ == 'str':
            pdict_[key] = eval(dict2[key])
        else:
            pdict_[key] = dict2[key]
    pdict_['tstart_old'] = pdict_['tstart']
    pdict_['tend_old'] = pdict_['tend']
    pdict_['tstart'] = pdict_['tstart_old'] - 1/pdict_['beta1']*log(1/pdict_['perc_gray'] -1)
    pdict_['tend'] = pdict_['tend_old'] + 1/pdict_['beta2']*log(1/pdict_['perc_gray'] -1)
    fm2 = fmclass(pdict_)
    get_initvals(fm2)
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
    
    
