# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:38:44 2020

@author: toalu
"""

from appJar import gui
import tps
import model_functions as mf
from numpy import sin, pi, arange
import random


def solve():
	paramdict = mf.getDefaultModelParameters()
	fm = tps.fmclass(paramdict)
	app.setLabel("myLabel","Beginning")
	tps.negcheck_init(fm) # execute function negcheck (tps/exec)
	tps.exec_cases(fm,tps.fmclass) # execute function exec_cases (tps/exec)
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)
	app.setLabel("myLabel","Solved")
	print("Solved")

	if usePlots:
		fig.clear()
		axes = fig.add_subplot(1,1,1)
		dataLine = fm.model(timeArr,outputData,"NNa/Wi")
		axes.plot(timeArr, dataLine, label="NNa/Wi")
		app.refreshPlot("plotFig")



usePlots = True
app = gui()
app.addLabel("myLabel","Hello World")
app.addButton("Go",solve)

if usePlots:
	fig = app.addPlotFig("plotFig",row=0,column=1,colspan=2,rowspan=1)

app.go()
