import tps
from numpy import sin, pi, arange
from appJar import gui
import random
import matplotlib.pyplot as plt
import numpy as np


def showLabels():
	axesList = fig.get_axes()
	axes = axesList[0]

	axes.legend()
	axes.set_xlabel("time")
	axes.set_ylabel("Y Axes")
	app.refreshPlot("plotFig")

def plotSomething():
	x = [1, 2, 3]
	y = [0, 1, 0]
	axes.clear()
	axes.plot(x,y)
	app.refreshPlot("plotFig")
	showLabels()

def solveModel():
	tStart = app.getEntry("tStartVal")
	tEnd = app.getEntry("tEndVal")
	if tStart is None:
		tStart = 20
	if tEnd is None:
		tEnd = 30
	if tEnd < tStart:
		tEnd = tStart

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
                 'tstart': tStart,
                 'tend': tEnd,
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
                 'nosynapse': False}
	fm = tps.fmclass(paramdict) # create a model (__init__.py of tps)
	tps.negcheck_init(fm) # execute function negcheck (tps/exec)
	tps.exec_cases(fm,tps.fmclass) # execute function exec_cases (tps/exec)
	global timeArr, myData, tstart, tend, firstPlot
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)
	#transpose data
	myData = np.zeros((len(outputData[0]),len(outputData)))
	for rowIdx in range(len(outputData)):
		for colIdx in range(len(outputData[0])):
			myData[colIdx][rowIdx] = outputData[rowIdx][colIdx]
	#fm.model(t,y,string) #string = 'NNa' -> creates a plot of description in string, using t as sampling time

	tstart = paramdict["tstart"]
	tend = paramdict["tend"]
	showOptions()
	firstPlot = False
	plotModel()

def plotModel():

	axes.clear()
	if not firstPlot:
		graphsToPlot = app.getOptionBox("Graphs")
		for itemIdx, itemLabel in enumerate(graphsToPlot):
			if graphsToPlot[itemLabel]:
				axes.plot(timeArr, myData[itemIdx], label=itemLabel)

		# area of oxygen deprivation
		limits = axes.get_ylim()
		ymin = limits[0]
		ymax = limits[1]
		areaX = np.array([tstart, tend])
		axes.fill_between(areaX, ymin, ymax, alpha=0.2)
		axes.set_ylim(limits)
		axes.set_xlim([timeArr[0], timeArr[-1]])
		app.refreshPlot("plotFig")
		showLabels()

def showOptions():
	app.addTickOptionBox("Graphs",[
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
		"Wg"
		], 0,10)
	app.setOptionBoxChangeFunction("Graphs", plotModel)


# main run
app = gui()

fig = app.addPlotFig("plotFig",0,0,10,10)
axes = fig.add_subplot(111)
app.addButton("SolveBtn", solveModel, 10,9)
#app.addButton("PlotBtn", plotSomething,11,9)
app.addLabel("tStartLabel","T start",10,0)
app.addNumericEntry("tStartVal",10,1)
app.setEntryDefault("tStartVal",20)
app.addLabel("tEndLabel","T end",11,0)
app.addNumericEntry("tEndVal",11,1)
app.setEntryDefault("tEndVal",30)
myData = []
timeArr = []
tstart = 0
tend = 0
firstPlot = True;


app.go()
#no code after this line