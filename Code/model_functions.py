# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:44:57 2020

@author: toalu
"""
from pylatexenc.latex2text import LatexNodes2Text
def ltx(latexString):
	return LatexNodes2Text().latex_to_text(latexString)


# model specific functions, these should be part of the model library
def getDefaultModelParameters():
	paramdict = {'pumpScaleAst': 1.0,
                 'pumpScaleNeuron': 1.0,
                 'nkccScale': 1.0,
                 'kirScale': 1.0,
                 'eaatScaleNeuron': 1.0,
                 'eaatScaleAst': 1.0,
                 'ncxScale': 1.0,
                 'nka_na': 13.0,
                 'nka_k': 0.2,
                 'beta1': 4,
                 'beta2': 4,
                 'perc': 0.5,
                 'tstart': 20,
                 'tend': 30,
                 't0': 0.0,
                 'tfinal': 100.0,
                 'alphae0': 0.2,
                 'C': 20.0,
                 'F': 96485.333,
                 'R': 8314.4598,
                 'T': 310.0,
                 'PNaG': 0.0008,
                 'PKG': 0.0004,
                 'PClG': 1.95e-05,
                 'PNaL_base': 2.0000000000000003e-06,
                 'PKL_base': 2e-05,
                 'PClL_base': 2.5e-06,
                 'UKCl': 1.2999999999999998e-06,
                 'LH20i': 2e-14,
                 'PNKAi': 87.2,
                 'Cg': 20.0,
                 'Vg0': -80.0,
                 'Vi0': -65.5,
                 'KCe_thres': 13.0,
                 'kup2': 0.1,
                 'PCaG': 1.5000000000000002e-05,
                 'PNCXi': 0,
                 'alphaNaNCX': 87.5,
                 'alphaCaNCX': 1.38,
                 'eNCX': 0.35,
                 'ksatNCX': 0.1,
                 'PEAATi': 0,
                 'PEAATg': 0,
                 'HeOHa': 0.66,
                 'HeOHai': 0.66,
                 'k1max': 1,
                 'KM': 0.0023,
                 'KDV': 0.1,
                 'k20': 2.1000000000000002e-05,
                 'k2cat': 0.02,
                 'kmin20': 1.7000000000000003e-05,
                 'kmin1': 5e-05,
                 'k3': 4.4,
                 'kmin3': 0.056,
                 'k4': 1.45,
                 'trec': 30,
                 'PNCXg': 0,
                 'perc_gray': 0.95,
                 'NaCi0': 13,
                 'KCi0': 145,
                 'ClCi0': 7,
                 'CaCi0': 0.0001,
                 'GluCi0': 3,
                 'NaCe0': 152,
                 'KCe0': 3,
                 'ClCe0': 135,
                 'CaCc0': 1.8,
                 'GluCc0': 0.0001,
                 'NaCg0': 13,
                 'KCg0': 80,
                 'ClCg0': 35,
                 'CaCg0': 0.00011,
                 'GluCg0': 2,
                 'Wi0': 2,
                 'Wg0': 1.7,
                 'VolPreSyn': 0.001,
                 'VolPAP': 0.001,
                 'Volc': 0.001,
                 'NF0': 0,
                 'NGlui0': 0,
                 'NGluc0': 0,
                 'We0': 0,
                 'NNai0': 0,
                 'NKi0': 0,
                 'NCli0': 0,
                 'NCai0': 0,
                 'NNae0': 0,
                 'NKe0': 0,
                 'NCle0': 0,
                 'NCac0': 0,
                 'NNag0': 0,
                 'NKg0': 0,
                 'NClg0': 0,
                 'NCag0': 0,
                 'NGlug0': 0,
                 'CNa': 0,
                 'CK': 0,
                 'CCl': 0,
                 'CCa': 0,
                 'Wtot': 0,
                 'NAi': 0,
                 'NAe': 0,
                 'NBe': 0,
                 'NAg': 0,
                 'NBg': 0,
                 'alpham0': 0,
                 'betam0': 0,
                 'alphah0': 0,
                 'betah0': 0,
                 'alphan0': 0,
                 'betan0': 0,
                 'm0': 0,
                 'h0': 0,
                 'n0': 0,
                 'INaGi0': 0,
                 'IKGi0': 0,
                 'IClGi0': 0,
                 'INaLi0': 0,
                 'IKLi0': 0,
                 'IClLi0': 0,
                 'JKCl0': 0,
                 'sigmapump': 0,
                 'fpump': 0,
                 'neurPump': 0,
                 'INCXi0': 0,
                 'JEAATi0': 0,
                 'ICaG0': 0,
                 'ICaLi0': 0,
                 'IGluLi0': 0,
                 'PNaLi': 0,
                 'PKLi': 0,
                 'PClLi': 0,
                 'PCaLi': 0,
                 'PNKAg': 0,
                 'LH20g': 0,
                 'PNKCC1': 0,
                 'PKir': 0,
                 'IKLg0': 0,
                 'IClLg0': 0,
                 'INaLg0': 0,
                 'JNKCC10': 0,
                 'sigmapumpA': 0,
                 'fpumpA': 0,
                 'astpump': 0,
                 'IKir0': 0,
                 'IGluLg0': 0,
                 'ICaLg0': 0,
                 'JEAATg0': 0,
                 'INCXg0': 0,
                 'k1init': 0,
                 'gCainit': 0,
                 'k2init': 0,
                 'kmin2catinit': 0,
                 'kmin2init': 0,
                 'PNaLg': 0,
                 'PKLg': 0,
                 'PClLg': 0,
                 'PCaLg': 0,
                 'NI0': 0,
                 'ND0': 0,
                 'NN0': 0,
                 'NR0': 0,
                 'NR10': 0,
                 'NR20': 0,
                 'NR30': 0,
                 'PGluLi': 0,
                 'PGluLg': 0,
                 'CGlu': 0,
                 'command': 'EnergyDeprivation',
                 'ECS': 0.2,
                 'EnergyAvailable': 0.5,
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
				 'testDict':{
					 'ch1': [0, 1],
					 'ch2': [2, 3],
					 'ch3': [2, 3],
					 'ch4': [2, 3],
					 'ch5': [2, 3],
					 'ch6': [2, 3],
					 'ch7': [2, 3],
					 'ch8': [2, 3],
					 'ch9': [2, 3],
					 'ch10': [2, 3],
					 'ch11': [2, 3],
					 'ch12': [2, 3],
					 'ch13': [2, 3],
					 'ch14': [2, 3],
					 'ch15': [2, 3],
					 'ch16': [2, 3],
					 'ch17': [2, 3],
					 'ch18': [5, 6]}}
	return paramdict

def getModelOutputNames():
	modelOutputNames = [
		"NNa",
		"NK",
		"NCl",
		"m",
		"h",
		"n",
		"NCai",
		"NN",
		"NR",
		"NR1",
		"NR2",
		"NR3",
		"NI",
		"ND",
		"NNag",
		"NKg",
		"NClg",
		"NCag",
		"NGlug",
		"Vtemp",
		"Wi",
		"Wg",
		"NNa/Wi"]
	return modelOutputNames

def getExperimentParameters():
	# definition of experiments: name and associated parameters
	# experiment = [name | label | parameters]
	# parameters = [name | label | default]
	experimentList = [
		["EnergyDeprivation","Energy Deprivation",[
		 	["ECS","ECS",0.2],
		 	["tfinal","T total [min]",100.0],
			["tstart","T start [min]",20.0],
			["tend","T end [min]",30.0],
			["EnergyAvailable","Available Energy",0.5],
			["solve","Solve",True],
			["nogates","Asymptotic Gates",True],
			["savenumpy","Save numpy",False],
			["savematlab","Save matlab",False],
			["Plot","Plot",True]]],
	 	["Excitation","Excitation",[
			["ECS","ECS",0.2],
			["tfinal","T total [min]",100.0],
			["StartExcitation","T start excitation [min]",1.0],
			["EndExcitation","T end excitation [min]",15.0],
			["Current","Current [pA]",20],
			["Wavelength","Wavelength [min]",20.0],
			["Duty","Duty [fraction]",0.95],
			["BlockAstrocyte","Block Astrocyte gradients",0.5],
			["nogates","Asymptotic Gates",True],
			["solve","Solve",True],
			["savenumpy","Save numpy",False],
			["savematlab","Save matlab",False],
			["Plot","Plot",True]]],
	 	["Test","Test",[
			["StartExcitation","T start excitation [min]",1.0],
			["EndExcitation","T end excitation [min]",15.0],
			["testDict","a dictionary",{}],
			["tstart","T start [min]",20.0],
			["tend","T end [min]",30.0],
			["nogates","No Gates",True],
			["Plot","Plot",True]]]]
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
	# style = {"h1","h2","p","a"}
	tutorialText = [
		["tutorialTab1","Introduction",[
		  ["h1","Title"],
		  ["h2","Sub title"],
		  ["a","A link","http://www.google.com/"],
		  ["p",ltx(r"Lorem $\alpha$ ipsum dolor sit amet,\\consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")],
		  ["h2","Another sub title"],
		  ["p",ltx(r"\frac{dx}{dt} = 0")],
		  ["p","Arcu dictum varius duis at consectetur lorem. Pellentesque eu tincidunt tortor aliquam. Pellentesque adipiscing commodo elit at imperdiet dui. Ultricies lacus sed turpis tincidunt id aliquet risus feugiat in. Ullamcorper eget nulla facilisi etiam dignissim diam quis. Elementum nisi quis eleifend quam adipiscing vitae. Lacus suspendisse faucibus interdum posuere lorem ipsum. Faucibus in ornare quam viverra orci. Penatibus et magnis dis parturient montes nascetur ridiculus. Aliquam ultrices sagittis orci a scelerisque purus. Montes nascetur ridiculus mus mauris vitae ultricies leo integer malesuada."]
		  ]],
		["tutorialTab2","An explaination",[
		  ["h1","Explaination title"],
		  ["h2","First subtitle"],
		  ["p","lorem ipsum dolor sit amet"],
		  ["h2","Another sub title"],
		  ["p","second paragraph"],
		  ["p","Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]
		  ]]
		]
	return tutorialText

def getModelInfo():
	# modelInfo = [name | label]
	modelInfo = [
		["pumpScaleAst","Pump Scale Astrocyte"],
		["pumpScaleNeuron","Pump Scale Neuron"],
		["tstart","T Start"],
		["tend","T End"],
		["solve","Solve"]
		]
	return modelInfo

