# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:44:57 2020

@author: toalu
"""
from pylatexenc.latex2text import LatexNodes2Text
from tps.main.fm_dict import dict_
def ltx(latexString):
        return LatexNodes2Text().latex_to_text(latexString)


# model specific functions, these should be part of the model library
def getDefaultModelParameters():
        extradict = {
                 'solve': True,
                 'nogates': True,
                 'savenumpy': False,
                 'Plot': True,
                 'plotall': True,
                 'savematlab': False,
                 'nochargecons': False,
                 'geteigs': False,
                 'savematlabpar': False,
                 'nosynapse': False,
                 's':False,
                 'b':False,
                 'm':False
        }
        for key in extradict:
                dict_[key] = extradict[key]
                
        return dict_

def getModelOutputNames():
        # entries contained by - are considered as headers
        modelOutputNames = [
                "- Membrane potential -",
                "E"+"\u2098"+" neuron",
                "E"+"\u2098"+" astrocyte",
                "- Neuron -",
                "[Na"+"\u207a"+"]"+"\u2099",
                "[K"+"\u207a"+"]"+"\u2099",
                "[Cl"+"\u207b"+"]"+"\u2099",
                "[Ca"+"\u00b2"+"\u207a"+"]"+"\u2099",
                "[Glu"+"]"+"\u2099",
                "- Astrocyte -",
                "[Na"+"\u207a"+"]"+"\u2090",
                "[K"+"\u207a"+"]"+"\u2090",
                "[Cl"+"\u207b"+"]"+"\u2090",
                "[Ca"+"\u00b2"+"\u207a"+"]"+"\u2090",
                "[Glu"+"]"+"\u2090",
                "- Volumes -",
                "Vol. neuron",
                "Vol. astrocyte"]
        
        return modelOutputNames

def getModelOutputExp():
        # entries contained by - are considered as headers
        modelOutputNames = {
                "- Membrane potential -":{"exp":"","pl":""},
                "E"+"\u2098"+" neuron":{"exp":"Vi","pl":r"$E_m^n$"},
                "E"+"\u2098"+" astrocyte":{"exp":"Vg","pl":r"$E_m^a$"},
                "- Neuron -":{"exp":"","pl":""},
                "[Na"+"\u207a"+"]"+"\u2099":{"exp":"NaCi","pl":r"[Na$^+$]$_n$"},
                "[K"+"\u207a"+"]"+"\u2099":{"exp":"KCi","pl":r"[K$^+$]$_n$",},
                "[Cl"+"\u207b"+"]"+"\u2099":{"exp":"ClCi","pl":r"[Cl$^-$]$_n$",},
                "[Ca"+"\u00b2"+"\u207a"+"]"+"\u2099":{"exp":"CaCi","pl":r"[Ca$^{2+}$]$_n$",},
                "[Glu"+"]"+"\u2099":{"exp":"GluCi","pl":r"[Glu]$_n$",},
                "- Astrocyte -":{"exp":"","pl":""},
                "[Na"+"\u207a"+"]"+"\u2090":{"exp":"NaCg","pl":r"[Na$^+$]$_a$"},
                "[K"+"\u207a"+"]"+"\u2090":{"exp":"KCg","pl":r"[K$^+$]$_a$"},
                "[Cl"+"\u207b"+"]"+"\u2090":{"exp":"ClCg","pl":r"[Cl$^-$]$_a$"},
                "[Ca"+"\u00b2"+"\u207a"+"]"+"\u2090":{"exp":"CaCg","pl":r"[Ca$^{2+}$]$_a$"},
                "[Glu"+"]"+"\u2090":{"exp":"GluCg","pl":r"[Glu]$_n$"},
                "- Volumes -":{"exp":"","pl":""},
                "Vol. neuron":{"exp":"Wi/p.Wi0*100","pl":r"Rel. change $W_n$"},
                "Vol. astrocyte":{"exp":"Wg/p.Wg0*100","pl":r"Rel. change $W_a$"}}    
        return modelOutputNames

def getExperimentParameters():
        # definition of experiments: name and associated parameters
        # experiment = [name | label | parameters]
        # parameters = [name | label | default]
        experimentList = [
                ["EnergyDeprivation","Energy Deprivation",[
                        ["ECS","Intial ECS (%)",20],
                        ["tfinal","Simulation length [min]",100.0],
                        ["tstart","Start energy deprivation [min]",20.0],
                        ["tend","End energy deprivation [min]",30.0],
                        ["EnergyAvailable","NKA activity left during ED",50],
                        ["nogates","Steady-state gates?",True]]],
                ["Excitation","Excitation",[
                        ["ECS","Intial ECS (%)",20],
                        ["tfinal","Simulation length [min]",100.0],
                        ["StartExcitation","Start excitation [min]",1.0],
                        ["EndExcitation","End excitation [min]",15.0],
                        ["Current","Current [pA]",20],
                        ["Wavelength","Wavelength of pulse [s]",20.0],
                        ["Duty","Duty [fraction]",0.95],
                        ["BlockAstrocyte","Block astrocyte?",True],
                        ["nogates","Asymptotic Gates",True]]]]
        return experimentList

def getExperimentAreas():
        # info for plotting
        # experimentArea = [name | areas]
        # areas = [startParam | endParam]
        experimentAreas = [
                ["EnergyDeprivation",[
                        ["tstart","tend"]
                        ]],
                ["Excitation",[
                        ["StartExcitation","EndExcitation"]
                        ]],
                ["Test",[
                        ["StartExcitation","EndExcitation"],
                        ["tstart","tend"]
                        ]]]
        return experimentAreas

def getTutorialPages():
        # tutorialText = [label | title | lines]
        # lines = [style | text]
        # style = {"h1","h2","p","a","img"}
        # images are loaded faster if gif format
        tutorialText = [
                ["tutorialTab1","Introduction",[
                  ["h1","Welcome!"],
                  #["h2","Sub title"],
                  ["p", "Welcome to the TriSyn GUI, based on the biophysical model for the tripartite synapse, which can be found here" ],      
                  ["a","Link to paper","https://www.overleaf.com/read/phckbggmmjyv"],
                  ["p","The model describes dynamics of ion concentrations at a tripartite synapse, along with respective volume changes. This is done by incorporating biophysical models for the most important ion channels in neuronal and astrocyte compartments, in an electroneutral framework. Here is an overview of the model:"],
                  ["img","Images/MainFig.gif"]
                  ]],
                ["tutorialTab2","GUI options",[
                  ["p","In the GUI currently there are two options for doing experiments. We go over both these options shortly. "]
                  ]]
                ]
        return tutorialText

def getModelInfo():
        # modelInfo = [name | label]
        modelInfo = [
                ["status","Status"],
                ["experiment","Summary"]
                ]
        return modelInfo

def getParamInfo(paramName):
        paramInfo = {"ECS":"Initial extracellular volume fraction (in %)",
                     "tstart":"Start time (in min.) for  energy deprivation",
                     "tend":"End time (in min.) for energy deprivation",
                     "tfinal":"End time (in min.) of the simulation",
                     "EnergyAvailable":"Maximum capacity of NKA activity (% of baseline) during energy deprivation",
                     "nogates":"Use steady-state Hodgkin-Huxley gates to speed up simulation, note that the transition to pathological equilibrium can be unrealistic",
                     "StartExcitation":"Start time (in min.) of neuronal stimulation",
                     "EndExcitation":"End time (in min.) of neuronal stimulation",
                     "Current":"Current (in pA) injected into the neuron",
                     "Wavelength":"Duration of stimulation (in s)",
                     "Duty":"Pulse frequency fraction: 0 (high) and 1 (low)",
                     "BlockAstrocyte":"Select to block astrocyte activity during neuronal stimulation"}
        return paramInfo[paramName]
