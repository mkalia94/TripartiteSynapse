from tps import *
def plotter(fm,expname, filename_, title_, fignum, t, y, *str):
    plt.rc('text', usetex=True)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=20)
    plt.locator_params(axis='y', nbins=4)
    plt.locator_params(axis='x', nbins=4)
    fig = plt.figure(fignum,figsize=(6.4,2.4))
    ax = fig.add_subplot(111)
    tnew = arange(fm.t0, fm.tfinal, 1e-2)
    tnew = tile(tnew, (2, 1))
    blockerExp = 1/(1+exp(fm.beta1*(tnew-fm.tstart))) \
        + 1/(1+exp(-fm.beta2*(tnew-fm.tend)))
    blockerExp = fm.perc + (1-fm.perc)*blockerExp
    plt.imshow(1-blockerExp, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
               cmap='Greys', alpha=0.5, aspect = "auto")
    plt.axvspan(0, 0, color='0.7', alpha=0.5, lw=0,
                label=r"Energy avail.: {d}\%".format(d=int(
                    fm.model(array(t), y, 'min(blockerExp)')*100)))
    if 'excite' in fm.__dict__.keys():
        val = fm.excite
        plt.axvspan(val[0], val[1], color='red',
                    alpha=0.5, lw=0, label='Neuron excited')
    if 'astblock' in fm.__dict__.keys():
        val = fm.astblock
        blockOther = 1/(1+exp(500*(tnew-val[0]))) \
            + 1/(1+exp(-500*(tnew-val[1])))
        plt.imshow(1-blockOther, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
                   cmap='Oranges', alpha=0.5, aspect = "auto")
        plt.axvspan(0, 0, color='orange', alpha=0.5, lw=0,
                    label='Ast. blocked')
    if 'block' in fm.__dict__.keys():
        dict_ = fm.block
        for key in dict_:
            val = dict_[key]
            if key in plotnamedict:
                blockOther = (1/(1+exp(fm.beta1*(tnew-val[0]))) +
                              1/(1+exp(-fm.beta2*(tnew-val[1]))))
                plt.imshow(1-blockOther, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
                           cmap='Greens', alpha=0.5, aspect = "auto")
                plt.axvspan(0, 0, color='forestgreen', alpha=0.5, lw=0,
                            label=r"{a} blocked".format(a=plotnamedict[key]))
            else:
                blockOther = (1/(1+exp(fm.beta1*(tnew-val[0]))) +
                              1/(1+exp(-fm.beta2*(tnew-val[1]))))
                plt.imshow(1-blockOther, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
                           cmap='Greens', alpha=0.5, aspect = "auto")
                plt.axvspan(0, 0, color='forestgreen', alpha=0.5, lw=0,
                            label=r"{a} blocked".format(a=key))
    ylim_max = -1e8
    ylim_min = 1e8
    for plotname in str[0]:
        t1 = array(t)
        ploty = fm.model(t1, y, plotname)
        if plotname[-1] == 'i':
            plt.plot(t1, ploty, label="Neuron")
        elif plotname[-1] == 'e':
            plt.plot(t1, ploty, color='forestgreen', label="ECS")
        elif plotname[-1] == 'g':
            plt.plot(t1, ploty, color='orange', label="Ast.")
        elif plotname[-1] == 'c':
            plt.plot(t1, ploty, color='forestgreen', label="Cleft")
        elif plotname in plotnamedict:
            plt.plot(t1, ploty, label=r"{d}".format(d=plotnamedict[plotname]))
        else:
            plt.plot(t1, ploty)
        if max(ploty) > ylim_max:
            ylim_max = max(ploty)
        if min(ploty) < ylim_min:
            ylim_min = min(ploty)
    plt.ylabel(r"{a}".format(a=title_))
    #plt.xlabel("t (min.)")
    plt.xlim(fm.t0, fm.tfinal)
    diff_ = ylim_max - ylim_min
    plt.ylim(ylim_min - 0.15*diff_, ylim_max + 0.15*diff_)
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ratio = 0.25
    #plt.axes().set_aspect(aspect=abs((xright-xleft)/(ybottom-ytop))*ratio)
    fig.tight_layout()
    # plt.axes().set_aspect(aspect=0.5)
    if 'saveloc' in fm.__dict__.keys():
        directory = 'Images/{a}'.format(a=fm.saveloc)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plotfilename = 'Images/{c}/{a}_{b}.pdf'.format(a=expname,
                                                       b=filename_,
                                                       c=fm.saveloc)
        save('Images/{a}/tfile.npy'.format(a=fm.saveloc),t)
        save('Images/{a}/yfile.npy'.format(a=fm.saveloc),y)
    else:
        plotfilename = 'Images/{a}_{b}.pdf'.format(a=expname, b=filename_)
        # paramfilename = 'Images/{a}_params.mat'.format(a=expname)
    #plt.legend(loc='upper right')
    #plt.savefig(plotfilename, format='pdf', bbox_inches='tight')
    # paramdict.update(fm.__dict__)
    # sio.savemat(paramfilename,paramdict)
