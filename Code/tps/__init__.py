import warnings
from numpy import *
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
from tps.plotdict import plotnamedict
import scipy.io as sio
import json
import os  # to create directory if it doesn't exist
import matplotlib as mpl
from scipy import signal
import tps.fm_model as modelfile
import tps.fm_params as paramfile
from tps.fm_dict import dict_ as paramdict
from tps.fm_solver import solver
#from tps.fm_plotter import plotter
from tps.fm_plottwoaxes import plottwoaxes
from tps.fm_plotall import plotall
from matplotlib import rc
from tps.fm_labeloffset import label_offset
from tps.fm_negcheck import negcheck
from tps.fm_twocases import twocases
import autograd.numpy as np
from tps.fm_model_autograd import model as jac_model
from autograd import jacobian
from tps.fm_matlabpar import savematlabpar
# Initialization
from tps.fm_get_initvals import get_initvals
from tps.fm_adjust_time import adjust_time
from tps.fm_negcheck_init import negcheck_init
from tps.fm_presolve_display import presolve_display
from tps.fm_set_saveloc import set_saveloc
from tps.fm_adjust_time import adjust_time
from tps.fm_saveparams import saveparams
# Execution
from tps.fm_exec_cases import exec_cases
from tps.fm_exec_plot import exec_plot
from tps.fm_exec_savedata import exec_savedata
from tps.fm_exec_geteigs import exec_geteigs
from tps.fm_exec_solve import exec_solve
# etting up
import argparse
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
mpl.use('Qt4Agg')

warnings.filterwarnings("ignore")

class fmclass:
    def __init__(self, dict_):
        paramfile.parameters(self, dict_)
        get_initvals(self)
        adjust_time(self)
        presolve_display(self)
        set_saveloc(self)
        saveparams(self)
        
    def model(self, t, y, *args):
        return(modelfile.model(t, y, self, *args))

    def labeloffset(self,ax,axis_):
        return(label_offset(ax,axis_))

    def num_model(self,y,p):
        return(jac_model(0,y,self,p))

print("Model imported..")    
