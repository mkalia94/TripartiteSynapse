from tps import *
import argparse
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

if 'saveloc' in paramdict.keys():
    disp('------{a}------'.format(a=paramdict['saveloc']))
else:
    disp('------Test------')

fm = fmclass(paramdict)    

fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NF0, fm.NI0,
               fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vpost0,
            fm.Wi0, fm.Wg0]  

    
# ---------------------------------------------------------------------------
#                  Solve ODE
# ---------------------------------------------------------------------------

if fm.solve:
    t, y = solver(fm, fm.t0, fm.tfinal, fm.initvals)
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
            plotter(fm, expname, keys, titledic_[keys], ctr, t, y, dict_[keys])
            ctr = ctr + 1
        disp('Plotting Done...')
