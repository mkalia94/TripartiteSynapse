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
from tps.fm_plotter import plotter
from tps.fm_plottwoaxes import plottwoaxes
mpl.use('Qt4Agg')


mpl.rcParams['text.usetex'] = True

warnings.filterwarnings("ignore")

class fmclass:
    def __init__(self, dict_):
        paramfile.parameters(self, dict_)

    def model(self, t, y, *args):
        return(modelfile.model(t, y, self, *args))  

print("Model imported..")    
