import tps
import model_functions as mf
from appJar import gui
import matplotlib.pyplot as plt
import numpy as np

# application's functions

def plotSomething():
	x = [1, 2, 3]
	y = [0, 1, 0]
	axes.clear()
	axes.plot(x,y)
	app.refreshPlot("plotFig")
	showLabels()


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

	global currentModel, tstart, tend
	currentModel = fm
	tstart = currentModel.__dict__["tstart"]
	tend = currentModel.__dict__["tend"]
	#print(fm.__dict__.keys())
	updateModelInfo()


def solveModel():
	if currentModel == None:
		updateModel()

	print("ready to simulate")

	global timeArr, outputData

	fm = currentModel
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)

	#fm.model(t,y,string) #string = 'NNa' -> creates a plot of description in string, using t as sampling time


def solvedModelCallback(varIn=None):
	print(varIn)
	updateModelInfo()
	stopWaitingWidget()
	showOptions()
	global firstPlot
	firstPlot = False
	plotModel()


def solveBtnFunction():
	startWaitingWidget()
	useThreads = False
	if useThreads:
		app.threadCallback(solveModel, solvedModelCallback)
	else:
		solveModel()
		solvedModelCallback()


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
		app.setLabel(modelInfoVal[0]+"_expInfoVal",newLabel)


def startWaitingWidget():
	print("Start waiting...")


def stopWaitingWidget():
	print("Done!")


def plotModel():
	axes.clear()
	if not firstPlot:
		graphsToPlot = app.getOptionBox("Graphs")
		for itemIdx, itemLabel in enumerate(graphsToPlot):
			if graphsToPlot[itemLabel]:
				dataLine = currentModel.model(timeArr,outputData,itemLabel)
				axes.plot(timeArr, dataLine, label=itemLabel)


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
	try:
		app.getOptionBox("Graphs")
	except Exception:
		pass
	else:
		print("try to remove the box")
		app.removeOptionBox("Graphs")

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
		app.setMessage("infoText","Instructions for "+parLabel)

def getClickFunction(widgetLabel):
	return lambda eventData: printParamInfo(eventData,widgetLabel)


def fixPaneWidth():
	#print(app.getScrollPaneWidget(tutorialTab[0]+"Panel").winfo_width())
	global tutorialText
	for tutorialTabsIdx,tutorialTab in enumerate(tutorialText):
		for tutorialLineIdx,tutorialLine in enumerate(tutorialTab[2]):
			if tutorialLine[0]=="p":
				lineLabel = tutorialTab[0]+"_line"+str(tutorialLineIdx)
				# should use scroll's width instrad of fixed number
				app.setMessageWidth(lineLabel, app.getScrollPaneWidget(tutorialTab[0]+"Panel").winfo_width()-20)


def openPlotWindow():
	app.showSubWindow("plottingWin")


### end of defined functions
### main run

# create a new gui
app = gui()
app.setStretch("both")
rootFrame = app.startFrame("rootFrame")

# initialization of global variables
currentModel = None
outputData = None
timeArr = None
tstart = 0
tend = 0
firstPlot = True;

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
# 	myAttrFile = open("C:/Users/toalu/Google Drive/UTwente/Work/TriSyn GUI/prova gui/scrollPane_size.txt","w")
# 	for att in dir(app.getScrollPaneWidget(tutorialTab[0]+"Panel").size):
# 	 	myAttrFile.write(att+"\n")
# 	 	print(getattr(app,att))#, getattr(app,att)
# 	myAttrFile.close()

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
app.addMessage("infoText","",row=2,column=0,rowspan=1,colspan=1)
app.setMessageRelief("infoText","sunken")

# create figure for plots
fig = app.addPlotFig("plotFig",row=0,column=1,colspan=2,rowspan=1)
axes = fig.add_subplot(111)

# definition of experiments: name and associated parameters
# experiment = [name | label | parameters]
# parameters = [name | label | default]
experimentList = mf.getExperimentParameters()

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

# create solve button
app.addButton("SolveBtn", solveBtnFunction, row=1,column=2,rowspan=1,colspan=1)
app.setButton("SolveBtn","Solve")
app.setButtonSticky("SolveBtn","nwe")

# set window's title
app.setTitle("TriSyn GUI")

app.stopFrame()

# handle click function for whole window (not working)
rootFrame.bind("<Button-1>",getClickFunction("root"),add="+")

# create second window
app.startSubWindow("plottingWin",title="Plot Editor", modal=True, blocking=False, transient=False)
app.addLabel("Plotting Window")
app.stopSubWindow()

# myAttrFile = open("C:/Users/toalu/Google Drive/UTwente/Work/TriSyn GUI/prova gui/gui_attributes.txt","w")
# for att in dir(app):
# 	myAttrFile.write(att+"\n")
# 	#print(att)#, getattr(app,att)
# myAttrFile.close()


# run the gui
app.go()
#no code after this line
