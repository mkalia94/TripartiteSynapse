import warnings
from numpy import *
import fm_model as modelfile
import fm_params as paramfile
from fm_dict import dict_ as paramdict
import argparse
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from plotdict import plotnamedict
# import scipy.io as sio
import json
import os  # to create directory if it doesn't exist
import matplotlib as mpl
from scipy import signal

mpl.rcParams['text.usetex'] = True

warnings.filterwarnings("ignore")
# -------------------------------------------------------------------------
#                Argument Parsing
# -------------------------------------------------------------------------

arg = argparse.ArgumentParser()
for key in paramdict:
    arg.add_argument('--{a}'.format(a=key), type=float)
arg.add_argument('-s', action='store_true')
arg.add_argument('-b', action='store_true')
arg.add_argument('-m', action='store_true')
arg.add_argument('--solve', action='store_true')
arg.add_argument('--write', action='store_true')
arg.add_argument('--plot', type=json.loads)
arg.add_argument('--titles', type=json.loads)
arg.add_argument('--block', type=json.loads)
arg.add_argument('--excite', nargs=2, type=float)
arg.add_argument('--astblock', nargs=2, type=float)
arg.add_argument('--nogates', action='store_true')
arg.add_argument('--nochargecons', action='store_true')
arg.add_argument('--saveloc', type=str)
arg.add_argument('--name', type=str)
args = arg.parse_args()

for key in args.__dict__:
    if args.__dict__[key] is not None:
        paramdict[key] = args.__dict__[key]


class fmclass:
    def __init__(self, dict_):
        paramfile.parameters(self, dict_)

    def model(self, t, y, *args):
        return(modelfile.model(t, y, self, *args))


if 'saveloc' in paramdict.keys():
    disp('------{a}------'.format(a=paramdict['saveloc']))
else:
    disp('------Test------')

fm = fmclass(paramdict)
# ---------------------------------------------------------------------------
#                  Setup solver and plotter
# ---------------------------------------------------------------------------

initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NF0, fm.NI0,
            fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.Vpost0,
            fm.mAMPA0, fm.Wi0, fm.Wg0]


def solver(t0, tfinal, initvals):
    mod = Explicit_Problem(fm.model, initvals, t0)
    sim = CVode(mod)
    sim.atol = 1e-11
    sim.rtol = 1e-11
    sim.verbosity = 50
    # sim.iter = 'Newton'
    # sim.discr = 'BDF'
    # sim.linear_solver = 'SPGMR'
    # sim.report_continuously = True
    # sim.verbosity = 10
    t, y = sim.simulate(tfinal)
    disp('Simulation Done...')
    return t, y


def plotter(expname, filename_, title_, fignum, t, y, *str):
    plt.rc('text', usetex=True)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=20)
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=3)
    fig = plt.figure(fignum)
    ax = fig.add_subplot(111)
    tnew = arange(fm.t0, fm.tfinal, 1e-2)
    tnew = tile(tnew, (2, 1))
    blockerExp = 1/(1+exp(fm.beta1*(tnew-fm.tstart))) \
        + 1/(1+exp(-fm.beta2*(tnew-fm.tend)))
    blockerExp = fm.perc + (1-fm.perc)*blockerExp
    plt.imshow(1-blockerExp, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
               cmap='Greys', alpha=0.5)
    plt.axvspan(0, 0, color='0.7', alpha=0.5, lw=0,
                label=r"Energy avail.: {d}\%".format(d=int(
                    fm.model(array(t), y, 'min(blockerExp)')*100)))
    if 'excite' in fm.__dict__.keys():
        val = fm.excite
        plt.axvspan(val[0], val[1], color='red',
                    alpha=0.5, lw=0, label='Neuron excited')
    if 'astblock' in fm.__dict__.keys():
        val = fm.astblock
        blockOther = 1/(1+exp(fm.beta1*(tnew-val[0]))) \
            + 1/(1+exp(-fm.beta2*(tnew-val[1])))
        plt.imshow(1-blockOther, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
                   cmap='Oranges', alpha=0.5)
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
                           cmap='Greens', alpha=0.5)
                plt.axvspan(0, 0, color='forestgreen', alpha=0.5, lw=0,
                            label=r"{a} blocked".format(a=plotnamedict[key]))
            else:
                blockOther = (1/(1+exp(fm.beta1*(tnew-val[0]))) +
                              1/(1+exp(-fm.beta2*(tnew-val[1]))))
                plt.imshow(1-blockOther, extent=[fm.t0, fm.tfinal, -1e4, 1e4],
                           cmap='Greens', alpha=0.5)
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
    plt.xlabel("t (min.)")
    plt.xlim(fm.t0, fm.tfinal)
    diff_ = ylim_max - ylim_min
    plt.ylim(ylim_min - 0.15*diff_, ylim_max + 0.15*diff_)
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ratio = 0.5
    plt.axes().set_aspect(aspect=abs((xright-xleft)/(ybottom-ytop))*ratio)
    fig.tight_layout()
    # plt.axes().set_aspect(aspect=0.5)
    if 'saveloc' in fm.__dict__.keys():
        directory = 'Images/{a}'.format(a=fm.saveloc)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plotfilename = 'Images/{c}/{a}_{b}.pdf'.format(a=expname,
                                                       b=filename_,
                                                       c=fm.saveloc)
        # paramfilename = 'Images/{c}/{a}_params.mat'.format(a=expname,
        #                                                   c=fm.saveloc)
    else:
        plotfilename = 'Images/{a}_{b}.pdf'.format(a=expname, b=filename_)
        # paramfilename = 'Images/{a}_params.mat'.format(a=expname)
    plt.legend(loc='upper right')
    plt.savefig(plotfilename, format='pdf', bbox_inches='tight')
    # paramdict.update(fm.__dict__)
    # sio.savemat(paramfilename,paramdict)

# ---------------------------------------------------------------------------
#                  Solve ODE
# ---------------------------------------------------------------------------


if fm.solve:
    t, y = solver(fm.t0, fm.tfinal, initvals)
    V = fm.model(array(t), y, 'V')

    if fm.write:
        file_ = open('ExperimentResults.txt', 'r+')
        file_.seek(0, 2)
        if 'name' in fm.__dict__.keys():
            file_.write('Experiment: %s, V[0] = %2.3f, V[end] = %2.3f \n' % (
                fm.saveloc, V[0], V[-1]))
            file_.close()
        else:
            file_.write('Experiment: %s, V[0] = %2.3f, V[end] = %2.3f \n' % (
                'test', V[0], V[-1]))
            file_.close()

    if 'plot' in fm.__dict__.keys():
        dict_ = fm.plot
        titledic_ = fm.titles
        ctr = 1
        if 'name' in fm.__dict__.keys():
            expname = fm.name
        else:
            expname = 'Test'
        for keys in dict_:
            plotter(expname, keys, titledic_[keys], ctr, t, y, dict_[keys])
            ctr = ctr + 1
        disp('Plotting Done...')
