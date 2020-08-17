# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:38:44 2020

@author: toalu
"""

from appJar import gui
import tps
import model_functions as mf
#import matplotlib.pyplot as plt
import numpy as np



def solve():
	paramdict = mf.getDefaultModelParameters()
	fm = tps.fmclass(paramdict)
	app.setLabel("myLabel","Beginning")
	tps.negcheck_init(fm) # execute function negcheck (tps/exec)
	tps.exec_cases(fm,tps.fmclass) # execute function exec_cases (tps/exec)
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)
	app.setLabel("myLabel","Solved")
	print("Solved")

# 	axes.clear()
# 	dataLine = fm.model(timeArr,outputData,"NNa/Wi")
# 	axes.plot(timeArr, dataLine, label="NNa/Wi")


# 	# area of oxygen deprivation
# 	tstart = fm.__dict__["tstart"]
# 	tend = fm.__dict__["tend"]
# 	limits = axes.get_ylim()
# 	ymin = limits[0]
# 	ymax = limits[1]
# 	areaX = np.array([tstart, tend])
# 	axes.fill_between(areaX, ymin, ymax, alpha=0.2)
# 	axes.set_ylim(limits)
# 	axes.set_xlim([timeArr[0], timeArr[-1]])
# 	app.refreshPlot("plotFig")



app = gui()
app.addLabel("myLabel","Hello World")
app.addButton("Go",solve)
# create figure for plots
fig = app.addPlotFig("plotFig",row=0,column=1,colspan=2,rowspan=1)
axes = fig.add_subplot(111)

app.go()
