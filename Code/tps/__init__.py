import warnings
from numpy import *
from sympy import *
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import os  # to create directory if it doesn't exist
import matplotlib as mpl
from scipy import signal
from matplotlib import rc
from autograd import jacobian
import autograd.numpy as np
import argparse

# Main files
from tps.main.fm_dict import dict_ as paramdict            # Dictionary of known parameters
import tps.main.fm_model as modelfile                      # Model file
import tps.main.fm_params as paramfile                     # Computes unknown parameters
from tps.main.fm_solver import solver                      # Solve  (contains tolerances and so on)

# Initialization
from tps.init.fm_matlabpar import savematlabpar            # Saves paramaters for MATLAB
from tps.init.fm_get_initvals import get_initvals          # Obtain initial values to start simulation
from tps.init.fm_adjust_time import adjust_time            # Adjust time for energy deprivation experiment
from tps.init.fm_negcheck_init import negcheck_init        # Checks for negative initial values
from tps.init.fm_presolve_display import presolve_display  # Displays short info about experiment being performed
from tps.init.fm_set_saveloc import set_saveloc            # Sets save location           
from tps.init.fm_saveparams import saveparams              # Saves parameters to npy file

# Execution
from tps.exec.fm_labeloffset import label_offset           # Important for plotting
from tps.exec.fm_plottwoaxes import plottwoaxes            # Plotting in one figure - two axes
from tps.exec.fm_plotall import plotall                    # Plot all relevant traces in one figure
from tps.exec.fm_negcheck import negcheck                  # Check for negative states
from tps.exec.fm_twocases import twocases                  # Pre-processing 'two cases'
from tps.exec.fm_model_autograd import model as jac_model  # Autograd model for eigenvalue computation (same as fm.model)
from tps.exec.fm_exec_cases import exec_cases              # Execute 'two cases' option (side-by-side simulation+plotting)
from tps.exec.fm_exec_plot import exec_plot                # Execute plotting
from tps.exec.fm_exec_savedata import exec_savedata        # Execute saving data (parameters, data)
from tps.exec.fm_exec_geteigs import exec_geteigs          # Execute eigenvalue computation
from tps.exec.fm_exec_solve import exec_solve              # Execute solving
# etting up

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
