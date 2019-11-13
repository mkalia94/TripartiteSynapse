from tps import *
import argparse

arg = argparse.ArgumentParser()
for key in paramdict:
    arg.add_argument('--{a}'.format(a=key), type=float)
    
arg.add_argument('-s', action='store_true')
arg.add_argument('-b', action='store_true')
arg.add_argument('-m', action='store_true')
arg.add_argument('--solve', action='store_true')
arg.add_argument('--datsave', action='store_true')
arg.add_argument('--plotall', action='store_true')
arg.add_argument('--plot', type=json.loads)
arg.add_argument('--block', type=json.loads)
arg.add_argument('--excite', nargs=2, type=float)
arg.add_argument('--astblock', nargs=2, type=float)
arg.add_argument('--nogates', action='store_true')
arg.add_argument('--nochargecons', action='store_true')
arg.add_argument('--saveloc', type=str)
arg.add_argument('--case1', type=json.loads)
arg.add_argument('--case2', type=json.loads)
arg.add_argument('--casename',type=str)

# arg.add_argument('--save',type=json.loads)
# arg.add_argument('--write', action='store_true')
# arg.add_argument('--titles', type=json.loads)

args = arg.parse_args()

for key in args.__dict__:
    if args.__dict__[key] is not None:
        paramdict[key] = args.__dict__[key]

if 'saveloc' in paramdict.keys():
    disp('------{a}------'.format(a=paramdict['saveloc']))
else:
    disp('------Test------')

fm = fmclass(paramdict)    

fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
               fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
            fm.Wi0, fm.Wg0]  

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
    
# ---------------------------------------------------------------------------
#                  Solve ODE
# ---------------------------------------------------------------------------

if 'saveloc' in fm.__dict__.keys():
    directory = 'Images/{a}'.format(a=fm.saveloc)
    if not os.path.exists(directory):
        os.makedirs(directory)        
else:
    directory = 'Images/{a}'.format(a='Test')
    if not os.path.exists(directory):
        os.makedirs(directory)

if 'casename' in fm.__dict__.keys():
    case1_ = fm.case1
    case2_ = fm.case2
    twocases(fmclass,paramdict,case1_,case2_,'TestCase')
    filename_ = "{a}/{b}.pdf".format(a=directory,b=fm.casename)
    plt.savefig(filename_,dpi=400,bbox_inches='tight',pad_inches=0)        

elif fm.solve:
    t, y = solver(fm, fm.t0, fm.tfinal, fm.initvals)

    # Negative check
    negcheck(fm,t,y)

    # Save numpy files and parameters, ready for Matlab (to be used in Matcont)
    if fm.datsave:
        if 'saveloc' in fm.__dict__.keys():
            directory = 'Images/{a}'.format(a=fm.saveloc)
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            directory = 'Images/{a}'.format(a='Test')
            if not os.path.exists(directory):
                os.makedirs(directory)
        save('{a}/tfile.npy'.format(a=directory),t)
        save('{a}/yfile.npy'.format(a=directory),y)
        pdict_= {}
        for key in fm.__dict__:
            if type(fm.__dict__[key]).__name__ in ['int','int64','float','float64']:
                pdict_[key]= float(fm.__dict__[key])
                sio.savemat('{a}/params.mat'.format(a=directory),pdict_)        
                sio.savemat('{a}/finalval.mat'.format(a=directory),mdict={'initvals':fm.initvals})
        
    # For making individual plots
    if 'plot' in fm.__dict__.keys():
        dict_ = fm.plot
        ctr = 0
        # Comment all lines till for loop to remove single file plotting
        len_ = fm.plot.__len__()
        if len_>1:
            widths = [1,1]
        else:
            widths = [1]
        heights= list(ones(int(len_/2)+1))
        wspace_ = 0.8
        hspace_ = 0.6
        figsizex_ = sum(widths)+(len(widths)+1)*wspace_
        figsizey_ = sum(heights)+(len(heights)+1)*hspace_
        fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
        spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                                  height_ratios=heights)
        fig.subplots_adjust(wspace=wspace_)
        fig.subplots_adjust(hspace=hspace_)
        for keys in dict_:
            # Switch comments for all commands except plottwoaxes(..) and ctr = ctr +1
            # to remove single file plotting
            #fig,ax = plt.subplots(num=ctr,figsize=(2,2))
            specx = int(ctr/2)
            if (int(ctr/2)-ctr/2) != 0:
                specy = 1
            else:
                specy = 0
            ax = fig.add_subplot(spec[specx,specy])
            plottwoaxes(fm,t,y,dict_[keys],[],keys,fig,ax)
            if ctr == (len_-1) or ctr == (len_-2):
                 ax.set_xlabel('time (min.)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
            #fig.tight_layout()
            #plotfilename = '{a}/{b}.pdf'.format(a=directory,b=keys)
            #plt.savefig(plotfilename, format='pdf', bbox_inches='tight')
            ctr = ctr + 1
        #fig.tight_layout()
        plt.savefig('{a}/Plots.pdf'.format(a=directory), format='pdf',bbox_inches='tight',pad_inches=0)
        disp('Plotting Done...')

    ## -----THIS DOES NOT HAVE TO GO INTO THE FINAL VERSION-----    
    # For plotting all relvant characteristics, as per tps.fm_plotall    
    if fm.plotall:
        widths = [1,1]
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
        plotall(fm,t,y,fig,spec,1)
        plt.savefig('{a}/PlotAll.pdf'.format(a=directory), format='pdf',bbox_inches='tight',pad_inches=0)
        

    # if 'save' in fm.__dict__.keys():
    #     dict_ = fm.save
    #     for key_ in dict_:
    #         y_ = fm.model(array(t),y,key_)
    #         fname_  = 'Images/{a}/{b}.dat'.format(a=fm.saveloc,b=key_)
    #         directory = 'Images/{a}'.format(a=fm.saveloc)
    #         if not os.path.exists(directory):
    #             os.makedirs(directory)
    #         if dict_[key_] == 'full':
    #             savetxt(fname_, array([array(t),y_]).T, fmt=['%.10f','%.10f'])
    #         elif dict_[key_] == 'short':
    #             factor_ = 100
    #             tnew_ = t[0::factor_]
    #             ynew_ = y_[0::factor_]
    #             savetxt(fname_, array([array(tnew_),ynew_]).T, fmt=['%.10f','%.10f'])
    # 
    # if fm.write:
    #     file_ = open('ExperimentResults.txt', 'r+')
    #     file_.seek(0, 2)
    #     if 'name' in fm.__dict__.keys():
    #         file_.write('Experiment: %s, V[0] = %2.3f, V[end] = %2.3f \n' % (
    #             fm.saveloc, V[0], V[-1]))
    #         file_.close()
    #     else:
    #         file_.write('Experiment: %s, V[0] = %2.3f, V[end] = %2.3f \n' % (
    #             'test', V[0], V[-1]))
    #         file_.close()


