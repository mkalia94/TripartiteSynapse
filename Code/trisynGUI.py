import tps
import model_functions as mf
from appJar import gui
import matplotlib.pyplot as plt
import numpy as np

import gc
import sys
import random

# application's functions

def plotSomething():
	x = [1, 2, 3]
	y = [0, 1, 0]
	axes.clear()
	axes.plot(x,y)
	app.refreshPlot("plotFig")


def updateModel():
	paramdict = mf.getDefaultModelParameters()
	tabId = app.getTabbedFrameSelectedTab("experimentsFrame")
	paramList = None
	for expIdx,expVal in enumerate(experimentList):
		if tabId == expVal[0]+"Tab":
			experimentId = expVal[0]
			paramList = expVal[2]
			break
	if paramList == None:
		return

	for idx,par in enumerate(paramList):
		if isinstance(par[2],bool):
			paramdict[par[0]] = app.getCheckBox(par[0]+"Val_"+experimentId)
		elif isinstance(par[2],float) or isinstance(par[2],int):
			paramdict[par[0]] = app.getEntry(par[0]+"Val_"+experimentId)
# 		print(par[0])
# 		print(paramdict[par[0]])

	fm = tps.fmclass(paramdict) # create a model (__init__.py of tps)
	tps.negcheck_init(fm) # execute function negcheck (tps/exec)
	tps.exec_cases(fm,tps.fmclass) # execute function exec_cases (tps/exec)

	global currentModel
	currentModel = fm
	#print(fm.__dict__.keys())
	updateModelInfo()


def solveModel():
	global lastSolvedModel, timeArr, outputData
	fm = currentModel
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)
	lastSolvedModel = fm

	#fm.model(t,y,string) #string = 'NNa' -> creates a plot of description in string, using t as sampling time


def solvedModelCallback(varIn=None):
	print(varIn)
	updateStatusLabel("Simulation complete")
	updateModelInfo()
	#stopWaitingWidget()
	showOptions()
	global firstPlot
	firstPlot = False
	plotModel()


def solveBtnFunction():
	if currentModel == None:
		updateModel()

	global CurrentSolvedExperiment
	tabId = app.getTabbedFrameSelectedTab("experimentsFrame")
	for expIdx,expVal in enumerate(experimentList):
		if tabId == expVal[0]+"Tab":
			CurrentSolvedExperiment = expVal[0]
			break
	print(CurrentSolvedExperiment)
	updateStatusLabel("Simulating")

	#startWaitingWidget()
	app.threadCallback(solveModel, solvedModelCallback)


def updateModelInfo():
	modelInfo = mf.getModelInfo()
	for modelInfoIdx,modelInfoVal in enumerate(modelInfo):
		if isinstance(currentModel.__dict__[modelInfoVal[0]],bool):
			if currentModel.__dict__[modelInfoVal[0]]:
				newLabel = "True"
			else:
				newLabel = "False"
		elif isinstance(currentModel.__dict__[modelInfoVal[0]],float):
			newLabel = str(round(currentModel.__dict__[modelInfoVal[0]],4))
		else:
			newLabel = str(currentModel.__dict__[modelInfoVal[0]])
		app.queueFunction(app.setLabel,modelInfoVal[0]+"_expInfoVal",newLabel)


def updateStatusLabel(newStatus):
	app.queueFunction(app.setLabel,"statusLabel","Status: "+newStatus)


# def startWaitingWidget():
# 	print("Start waiting...")


# def stopWaitingWidget():
# 	print("Done waiting!")


def plotModel():
	axes.clear()
	if not firstPlot:
		graphsToPlot = app.getOptionBox("Graphs")
		for itemIdx, itemLabel in enumerate(graphsToPlot):
			if graphsToPlot[itemLabel]:
				dataLine = currentModel.model(timeArr,outputData,itemLabel)
				axes.plot(timeArr, dataLine, label=itemLabel)


		# plot areas
		limits = axes.get_ylim()
		ymin = limits[0]
		ymax = limits[1]

		for expIdx,expVal in enumerate(experimentAreas):
			if CurrentSolvedExperiment == expVal[0]:
				areasToPlot = expVal[1]
				break
		for areaIdx,areaVal in enumerate(areasToPlot):
			tstart = lastSolvedModel.__dict__[areaVal[0]]
			tend = lastSolvedModel.__dict__[areaVal[1]]
			areaX = np.array([tstart, tend])
			axes.fill_between(areaX, ymin, ymax, alpha=0.2)

		axes.set_ylim(limits)
		axes.set_xlim([timeArr[0], timeArr[-1]])
		app.refreshPlot("plotFig")
		showLabels()


def showLabels():
	axesList = fig.get_axes()
	axes = axesList[0]

	anyPlot = False
	plotList = app.getOptionBox("Graphs")
	for plotIdx,plotLabel in enumerate(plotList):
		if plotList[plotLabel]:
			anyPlot = True
			break
	if anyPlot:
		axes.legend()
	axes.set_xlabel("time")
	axes.set_ylabel("Y Axes")
	app.refreshPlot("plotFig")


def showOptions():
	# reset option box
	try:
		app.getOptionBox("Graphs")
	except Exception:
		pass
	else:
		app.removeOptionBox("Graphs")

	# reset plotting button
	try:
		app.getButton("plotWinBtn")
	except Exception:
		pass
	else:
		app.removeButton("plotWinBtn")

	app.openFrame("rootFrame")
	app.addTickOptionBox("Graphs", mf.getModelOutputNames(), row=0,column=3,rowspan=1,colspan=2)
	app.setOptionBoxChangeFunction("Graphs", plotModel)
	app.setOptionBoxSticky("Graphs","ne")
	app.addButton("plotWinBtn", openPlotWindow, row=2,column=2)
	app.setButton("plotWinBtn","Advanced Plots")
	app.setButtonSticky("plotWinBtn","se")
	app.stopFrame()


def printParamInfo(eventData,parLabel):
	#print(parLabel)
	#print(eventData.widget._name)

	if parLabel == "root":
		app.setMessage("infoText","")
	else:
		app.setMessage("infoText","Instructions for "+parLabel+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer."+"\nAnd this might be a very long text that might even require a scroll. Is it scrolling yet? Who knows, but we can try to make it longer.")

def getClickFunction(widgetLabel):
	return lambda eventData: printParamInfo(eventData,widgetLabel)


def fixPaneWidth():
	#print(app.getScrollPaneWidget(tutorialTab[0]+"Panel").winfo_width())
	global tutorialText
	for tutorialTabsIdx,tutorialTab in enumerate(tutorialText):
		# should use scroll's width instrad of fixed number
		widgetWidth = app.getScrollPaneWidget(tutorialTab[0]+"Panel").winfo_width()-20
		for tutorialLineIdx,tutorialLine in enumerate(tutorialTab[2]):
			if tutorialLine[0]=="p":
				lineLabel = tutorialTab[0]+"_line"+str(tutorialLineIdx)
				app.setMessageWidth(lineLabel, widgetWidth)


def openPlotWindow():
	app.showSubWindow("plottingWin")


def pickAColor():
	oldColour = app.getButtonBg("colorPickerBtn")
	newColour = app.colourBox(colour=oldColour,parent="plottingWin")
	app.setButtonBg("colorPickerBtn",newColour)


def initPlotWidow():
	plotSpaceFig.clear()
	axes1_1 = plotSpaceFig.add_subplot(2,3,random.randint(1,6))
	axes1_2 = plotSpaceFig.add_subplot(2,3,random.randint(1,6))
	app.refreshPlot("plottingSpace")



### end of defined functions
### main run

# create a new gui
app = gui() #geom="1000x850" it should resize later on...

# set window's title
app.setTitle("TriSyn GUI")

# initialization of global variables
currentModel = None
lastSolvedModel = None
outputData = None
timeArr = None
firstPlot = True;
CurrentSolvedExperiment = None

app.setStretch("both")
rootFrame = app.startFrame("rootFrame")

# tutorialText = [label | title | lines]
# lines = [style | text]
# style = {"h1","h2","p","a"}
tutorialText = mf.getTutorialPages()
tutorialFont = "Helvetica"
titleStyle = "20 underline"
subtitleStyle = "16 bold"
parStyle = "14"

# create tutorial tabs
app.startTabbedFrame("tutorialFrame",row=0,column=0,rowspan=2,colspan=1)

#app.setStretch("none")
for tutorialTabsIdx,tutorialTab in enumerate(tutorialText):
	app.startTab(tutorialTab[0]+"Tab")
	app.setTabText("tutorialFrame",tutorialTab[0]+"Tab",tutorialTab[1])
	app.startScrollPane(tutorialTab[0]+"Panel", disabled="horizontal")

	for tutorialLineIdx,tutorialLine in enumerate(tutorialTab[2]):
		lineLabel = tutorialTab[0]+"_line"+str(tutorialLineIdx)
		if tutorialLine[0]=="p":
 			app.addMessage(lineLabel, tutorialLine[1])
 			app.setMessageSticky(lineLabel,"news")
 			app.getMessageWidget(lineLabel).config(font=tutorialFont+" "+parStyle)
 			app.setMessageAlign(lineLabel,"left")
 			#app.setMessageRelief(lineLabel,"sunken")
		elif tutorialLine[0]=="a":
			app.addWebLink(tutorialLine[1],tutorialLine[2])
		else:
			app.addLabel(lineLabel, tutorialLine[1])
			app.setLabelSticky(lineLabel,"news")
			if tutorialLine[0] == "h1":
				app.getLabelWidget(lineLabel).config(font=tutorialFont+" "+titleStyle)
			elif tutorialLine[0] == "h2":
				app.getLabelWidget(lineLabel).config(font=tutorialFont+" "+subtitleStyle)
			else:
				app.removeLabel(lineLabel)
			#app.setLabelRelief(lineLabel,"sunken")

	app.stopScrollPane()
	app.getScrollPaneWidget(tutorialTab[0]+"Panel").bind("<Configure>",lambda e: fixPaneWidth(),add="+")
	app.stopTab()
app.stopTabbedFrame()

app.setStretch("both")
# create text for instructions
app.startScrollPane("infoScroll", disabled="horizontal",row=2,column=0,rowspan=1,colspan=1)
app.addMessage("infoText","")
app.setMessageSticky("infoText","news")
app.setMessageAspect("infoText",300)
app.setMessageRelief("infoText","sunken")
app.stopScrollPane()

# create figure for plots
fig = app.addPlotFig("plotFig",row=0,column=1,colspan=2,rowspan=1)
axes = fig.add_subplot(111)

# definition of experiments: name and associated parameters
# experiment = [name | label | parameters]
# parameters = [name | label | default]
experimentList = mf.getExperimentParameters()
experimentAreas = mf.getExperimentAreas()

# open a tabbed frame for the experiments
app.startTabbedFrame("experimentsFrame",row=1,column=1,colspan=1,rowspan=1)

# create single tabs
for expIdx,expVal in enumerate(experimentList):
	# open tab and set correct text
	app.startTab(expVal[0]+"Tab")
	app.setTabText("experimentsFrame",expVal[0]+"Tab",expVal[1])

	# create parameters (label+control)
	for parIdx,parVal in enumerate(experimentList[expIdx][2]):
		# label creation and handling of click event
		labelWidget = app.addLabel(parVal[0]+"Label_"+expVal[0],parVal[1],row=parIdx,column=0)
		myCallback = getClickFunction(parVal[0])
		labelWidget.bind("<Button-1>",myCallback,add="+")

		# control creation, according to its type
		if isinstance(parVal[2],bool):
			app.addCheckBox(parVal[0]+"Val_"+expVal[0],row=parIdx,column=1)
			app.setCheckBox(parVal[0]+"Val_"+expVal[0],ticked=parVal[2], callFunction=False)
			app.setCheckBoxText(parVal[0]+"Val_"+expVal[0],"")
			app.setCheckBoxSticky(parVal[0]+"Val_"+expVal[0],"w")
			app.setCheckBoxChangeFunction(parVal[0]+"Val_"+expVal[0],updateModel)
		elif isinstance(parVal[2], float) or isinstance(parVal[2], int):
			app.addNumericEntry(parVal[0]+"Val_"+expVal[0],row=parIdx,column=1)
			app.setEntry(parVal[0]+"Val_"+expVal[0],parVal[2])
			app.setEntryChangeFunction(parVal[0]+"Val_"+expVal[0],updateModel)
	# close single tab
	app.stopTab()

# close tabbed frame
app.stopTabbedFrame()
app.setTabbedFrameChangeFunction("experimentsFrame",updateModel)


# experiment info panel
# modelInfo = [name | label]
modelInfo = mf.getModelInfo()
app.startLabelFrame("experimentInfo", label="Experiment Info", row=2,column=1)
app.setSticky("we")
for modelInfoIdx,modelInfoVal in enumerate(modelInfo):
	app.addLabel(modelInfoVal[0]+"_expInfoLabel",modelInfoVal[1]+":",row=modelInfoIdx,column=0)
	app.setLabelAlign(modelInfoVal[0]+"_expInfoLabel","right")
	app.addLabel(modelInfoVal[0]+"_expInfoVal","",row=modelInfoIdx,column=1)
	app.setLabelAlign(modelInfoVal[0]+"_expInfoVal","left")

app.stopLabelFrame()
updateModel()

# create status label
app.setSticky("we")
app.addLabel("statusLabel","",row=3,column=1)
updateStatusLabel("Ready")

# create solve button
app.addButton("SolveBtn", solveBtnFunction, row=1,column=2,rowspan=1,colspan=1)
app.setButton("SolveBtn","Solve")
app.setButtonSticky("SolveBtn","nwe")

# close root frame
app.stopFrame()

# handle click function for whole window (not working)
rootFrame.bind("<Button-1>",getClickFunction("root"),add="+")

# create second window
app.startSubWindow("plottingWin",title="Plot Editor", modal=True, blocking=False, transient=False)
app.setSticky("nswe")
app.setStretch("both")
# app.addLabel("tempLabel","Work in Progress")
# will be added from the template
app.startFrame("rootPlotWindow")

# left column: line lists, subplot controls
app.setExpand("none")
app.startFrame("controlsColumn",row=0,column=0)

app.setStretch("both")
app.addListBox("linesBox",mf.getModelOutputNames(),row=0,column=0,colspan=3)
app.selectListItemAtPos("linesBox",0,callFunction=False)

app.setStretch("column")
app.addNamedButton("Add line","addLineBtn",func=initPlotWidow,row=1,column=0,colspan=3)
app.setButtonSticky("addLineBtn","es")

app.addNamedButton("<","previousPlotBtn",func=None,row=2,column=0)
app.addNamedButton("+","addPlotBtn",func=None,row=2,column=1)
app.addNamedButton(">","nextPlotBtn",func=None,row=2,column=2)
app.setButtonSticky("previousPlotBtn","ews")
app.setButtonSticky("addPlotBtn","ews")
app.setButtonSticky("nextPlotBtn","ews")

app.stopFrame()
app.setFrameSticky("controlsColumn","wns") # wens to stick to the plot

# central column: plotting area
app.setExpand("both")
app.setStretch("both")
app.startFrame("plottingSpaceFrame",row=0,column=1)
plotSpaceFig = app.addPlotFig("plottingSpace")
plotSpaceFig.add_subplot(111)
app.stopFrame()
app.setFrameSticky("plottingSpaceFrame","nsew")

# right column: plot settings
app.setExpand("none")
app.startFrame("settingsColumn",row=0,column=2)

app.setStretch("column")
app.startLabelFrame("lineControls", hideTitle=False, label="Line Editor")
# line selector
app.addOptionBox("lineSelector",["- Lines -"],row=0,column=0,colspan=2)

# color selector
app.setStretch("none")
app.addLabel("colorLabel", "Colour:",row=1,column=0)
app.setLabelSticky("colorLabel","w")
app.setStretch("column")
app.addNamedButton("", "colorPickerBtn", func=pickAColor, row=1, column=1)
app.setButtonSticky("colorPickerBtn","we")

# axis selector
app.startLabelFrame("axisControl", hideTitle=False, label="Axis", row=2, column=0, colspan=2)
app.addRadioButton("axisRadio","Left")
app.addRadioButton("axisRadio","Right")
app.stopLabelFrame()

# size selector
app.addLabel("weightLabel","Weight:", row=3, column=0)
app.addNumericEntry("weightVal", row=3, column=1)
app.setEntry("weightVal",1)
app.setEntryWidth("weightVal",7)
app.addLabel("offsetLabel","Offset:", row=4, column=0)
app.addNumericEntry("offsetVal", row=4, column=1)
app.setEntry("offsetVal",0)
app.setEntryWidth("offsetVal",7)

# delete curve
app.addNamedButton("Delete Line","deleteLineBtn",func=None,row=5,column=1)

app.stopLabelFrame()

app.startLabelFrame("plotControls", hideTitle=False, label="Plot Editor")
app.addLabel("plotTitleLabel","Title:",row=0,column=0)
app.addEntry("plotTitleVal",row=0,column=1,colspan=2)
app.addLabel("plotXlabelLabel","X label:",row=1,column=0)
app.addEntry("plotXlabelVal",row=1,column=1,colspan=2)
app.addLabel("plotY1labelLabel","Y1 label:",row=2,column=0)
app.addEntry("plotY1labelVal",row=2,column=1,colspan=2)
app.addLabel("plotY2labelLabel","Y2 label:",row=3,column=0)
app.addEntry("plotY2labelVal",row=3,column=1,colspan=2)

app.addLabel("minAxisLabel","Min",row=4,column=1)
app.addLabel("maxAxisLabel","Max",row=4,column=2)
app.addLabel("plotY1limitsLabel","Y1 lim:",row=5,column=0)
app.addNumericEntry("plotY1minVal",row=5,column=1)
app.setEntryWidth("plotY1minVal",7)
app.addNumericEntry("plotY1maxVal",row=5,column=2)
app.setEntryWidth("plotY1maxVal",7)
app.addLabel("plotY2limitsLabel","Y2 lim:",row=6,column=0)
app.addNumericEntry("plotY2minVal",row=6,column=1)
app.setEntryWidth("plotY2minVal",7)
app.addNumericEntry("plotY2maxVal",row=6,column=2)
app.setEntryWidth("plotY2maxVal",7)

app.addNamedButton("Delete Subplot","deleteSubplotBtn",func=None, row=7,column=2)
app.stopLabelFrame()

app.stopFrame()
app.setFrameSticky("settingsColumn","ens") # wens to stick to the plot

app.stopFrame()

initPlotWidow()
app.stopSubWindow()


# run the gui
app.go()

#code after this line is executed when the gui is closed
gc.collect()
sys.exit()
exit()
