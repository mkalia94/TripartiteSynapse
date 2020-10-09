import tps
import model_functions as mf
from appJar import gui
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from math import ceil
from scipy.interpolate import interp1d


# class definitions
class cLine:
	def __init__(self, name, color=None, isLeftAxis=True, weight=1, offset=0):
		self.name = name # name is also the formula for the line
		self.color = color
		self.isLeftAxis = isLeftAxis
		self.weight = weight
		self.offset = offset

class cSubplot:
	def __init__(self, title="", xLabel="", y1Label="", y2Label="", y1Lim=None, y2Lim=None):
		self.title = title
		self.xLabel = xLabel
		self.y1Label = y1Label
		self.y2Label = y2Label
		self.y1Lim = y1Lim
		self.y2Lim = y2Lim
		self.lines = []
	def addLine(self,formula):
		if isinstance(formula,str):
			# formula must be unique
			okToAdd = True
			for existingLines in self.lines:
				if formula == existingLines.name:
					okToAdd = False
					break
			if okToAdd:
				self.lines.append(cLine(formula))
	def removeLine(self,lineIdx):
		if lineIdx >= 0 and lineIdx < len(self.lines):
			self.lines.pop(lineIdx)

class cGraphs:
	def __init__(self,timeData, dataset, areas=[]):
		self.subplots = []
		self.timeData = timeData
		self.dataset = dataset
		self.areas = areas
		self.currentIdx = None
	def addSubplot(self,newSubplot=cSubplot()):
		if isinstance(newSubplot, cSubplot):
			self.subplots.append(newSubplot)
			self.currentIdx = len(self.subplots)-1
	def removeSubplot(self,subplotIdx):
		if subplotIdx == None:
			return
		if subplotIdx >= 0 and subplotIdx < len(self.subplots):
			self.subplots.pop(subplotIdx)
			# deinit index when last subplot is removed
			if len(self.subplots) == 0:
				self.currentIdx = None
				return
			# reposition index
			if self.currentIdx == subplotIdx:
				self.currentIdx -= 1
			if self.currentIdx == -1:
				self.currentIdx = len(self.subplots)-1
	def nextSubplot(self):
		if self.currentIdx == None:
			# no subplots
			return
		self.currentIdx = self.currentIdx+1
		if self.currentIdx == len(self.subplots):
			self.currentIdx = 0
	def prevSubplot(self):
		if self.currentIdx == None:
			# no subplots
			return
		self.currentIdx = self.currentIdx-1
		if self.currentIdx == -1:
			self.currentIdx = len(self.subplots)-1


# application's functions

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
		elif isinstance(par[2],dict):
			checkedOptions = app.getOptionBox(par[0]+" Option List")
			for optionIdx, optionItem in enumerate(checkedOptions.keys()):
				try:
					app.getLabel(par[0]+"_"+optionItem+"Label")
				except Exception:
					pass
				else:
					tInit = app.getEntry(par[0]+"_"+optionItem+"_tStart")
					tFinish = app.getEntry(par[0]+"_"+optionItem+"_tEnd")
					paramdict[par[0]][optionItem] = [tInit, tFinish]

	fm = tps.fmclass(paramdict) # create a model (__init__.py of tps)
	tps.negcheck_init(fm) # execute function negcheck (tps/exec)
	tps.exec_cases(fm,tps.fmclass) # execute function exec_cases (tps/exec)

	global currentModel
	currentModel = fm
	#print(fm.__dict__.keys())
	updateModelInfo()


def getParamOptionHandler(paramName):
	return lambda: paramOptionHandler(paramName)


def paramOptionHandler(paramName):
	# collect already set items
	paramDefaultDict = mf.getDefaultModelParameters()[paramName]
	checkedOptions = app.getOptionBox(paramName+" Option List")
	for optionIdx, optionItem in enumerate(checkedOptions.keys()):
		try:
			app.getLabel(paramName+"_"+optionItem+"Label")
		except Exception:
			pass
		else:
			tInit = app.getEntry(paramName+"_"+optionItem+"_tStart")
			tFinish = app.getEntry(paramName+"_"+optionItem+"_tEnd")
			paramDefaultDict[optionItem] = [tInit, tFinish]

	# clear frame
	app.emptyFrame(paramName+"ItemsFrame")

	# repopulate
	app.openFrame(paramName+"ItemsFrame")
	myRow = 1
	anyItem = False
	for optionIdx, optionItem in enumerate(checkedOptions.keys()):
		if checkedOptions[optionItem]:
			anyItem = True
			app.addLabel(paramName+"_"+optionItem+"Label",optionItem, row=myRow, column=0)
			app.addNumericEntry(paramName+"_"+optionItem+"_tStart", row=myRow, column=1)
			app.addNumericEntry(paramName+"_"+optionItem+"_tEnd", row=myRow, column=2)
			myRow += 1
			app.setEntry(paramName+"_"+optionItem+"_tStart",float(paramDefaultDict[optionItem][0]),callFunction=False)
			app.setEntry(paramName+"_"+optionItem+"_tEnd",float(paramDefaultDict[optionItem][1]),callFunction=False)
			app.setEntryWidth(paramName+"_"+optionItem+"_tStart",5)
			app.setEntryWidth(paramName+"_"+optionItem+"_tEnd",5)
			app.setEntryChangeFunction(paramName+"_"+optionItem+"_tStart",updateModel)
			app.setEntryChangeFunction(paramName+"_"+optionItem+"_tEnd",updateModel)

	if anyItem:
		app.addLabel(paramName+"_tStartLabel","t start", row=0, column=1)
		app.addLabel(paramName+"_tEndLabel","t end", row=0, column=2)

	app.stopFrame()


def solveModel():
	global lastSolvedModel, timeArr, outputData
	fm = currentModel
	timeArr,outputData = tps.exec_solve(fm) # execute function exec_solve (tps/exec)
	lastSolvedModel = fm

	# resampling if needed
	dt = 1/(60*10)# a reasonable dt (0.1 s)
	if np.min(np.diff(timeArr)) < dt:
		print("Data might be resampled...")
		tStart = timeArr[0]
		tFinal = timeArr[-1]
		nData = ceil((tFinal-tStart)/dt)
		if nData >= np.size(timeArr):
			# upsampling is useless
			return
		interpolatingFunc = interp1d(timeArr, outputData, axis=0, assume_sorted=True)

		print("Resampling...")
		# new downsampled data
		timeArr = np.linspace(tStart,tFinal,nData)
		outputData = interpolatingFunc(timeArr)

		# clear memory, probably not needed
		del interpolatingFunc


def solvedModelCallback(varIn=None):
	updateStatusLabel("Simulation complete")
	updateModelInfo()
	#stopWaitingWidget()
	showGraphOptions()
	initPlotWidow()
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
	#print(CurrentSolvedExperiment)
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


def showGraphOptions():
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

	# data init, this should be created when the plot is available
	for expIdx,expVal in enumerate(experimentAreas):
		if CurrentSolvedExperiment == expVal[0]:
			areasToPlot = expVal[1]
			break
	areasList = []
	for areaIdx,areaVal in enumerate(areasToPlot):
		tstart = lastSolvedModel.__dict__[areaVal[0]]
		tend = lastSolvedModel.__dict__[areaVal[1]]
		areasList.append([tstart, tend])
	global graphData
	graphData = cGraphs(timeArr,outputData,areas=areasList)


def printParamInfo(eventData,parLabel):
	#print(parLabel)
	#print(eventData.widget._name)

	if parLabel == "root":
		app.setMessage("infoText","")
	else:
		app.setMessage("infoText",mf.getParamInfo(parLabel))

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
	updateLineInfo()

def initPlotWidow():
	plotSpaceFig.clear()
	app.refreshPlot("plottingSpace")

def addSubplot():
	graphData.addSubplot(newSubplot=cSubplot(title="Subplot "+str(len(graphData.subplots)+1), xLabel="Time"))
	executePlot()
	displaySubplotInfo()

def removeCurrentSubplot():
	graphData.removeSubplot(graphData.currentIdx)
	executePlot()
	displaySubplotInfo()

def focusNextSubplot():
	graphData.nextSubplot()
	executePlot()
	displaySubplotInfo()

def focusPreviousSubplot():
	graphData.prevSubplot()
	executePlot()
	displaySubplotInfo()

def addLine():
	if graphData.currentIdx == None:
		return
	lineList = app.getListBox("linesBox")
	if lineList[0][0] == "-" and lineList[0][-1] == "-":
		# header line, skip
		return

	graphData.subplots[graphData.currentIdx].addLine(lineList[0])

	# update plot and info
	executePlot()
	displaySubplotInfo()

def removeLine():
	# get current line
	selectedLine = app.getOptionBox("lineSelector")
	mySubplot = graphData.subplots[graphData.currentIdx]
	myLineIdx = None
	for lineIdx,lineObj in enumerate(mySubplot.lines):
		if lineObj.name == selectedLine:
			myLineIdx = lineIdx
			break
	if myLineIdx == None:
		return
	graphData.subplots[graphData.currentIdx].removeLine(myLineIdx)

	# update plot and info
	executePlot()
	displaySubplotInfo()

def displaySubplotInfo():
	# get current subplot
	mySubplot = graphData.subplots[graphData.currentIdx]
	# update title
	app.setEntry("plotTitleVal",mySubplot.title,callFunction=False)
	# update xLabel
	app.setEntry("plotXlabelVal",mySubplot.xLabel,callFunction=False)
	# update y1Label
	app.setEntry("plotY1labelVal",mySubplot.y1Label,callFunction=False)
	# update y2Label
	app.setEntry("plotY2labelVal",mySubplot.y2Label,callFunction=False)
	# update y1Lim
	if not mySubplot.y1Lim == None:
		app.setEntry("plotY1minVal",mySubplot.y1Lim[0],callFunction=False)
		app.setEntry("plotY1maxVal",mySubplot.y1Lim[1],callFunction=False)
	# update y2Lim
	if not mySubplot.y2Lim == None:
		app.setEntry("plotY2minVal",mySubplot.y2Lim[0],callFunction=False)
		app.setEntry("plotY2maxVal",mySubplot.y2Lim[1],callFunction=False)
	# update lines list
	app.setButtonBg("colorPickerBtn",defaultBtnColor)
	lineList = ["- Lines -"]
	lineIdx = 0
	for lineObj in mySubplot.lines:
		lineList.append(lineObj.name)
		lineIdx = 1
	app.changeOptionBox("lineSelector", lineList, 0, callFunction=False)
	if lineIdx == 1:
		app.setOptionBox("lineSelector",lineIdx, callFunction = True)

def displayLineInfo():
	# get current line
	selectedLine = app.getOptionBox("lineSelector")
	mySubplot = graphData.subplots[graphData.currentIdx]
	myLine = None
	for lineObj in mySubplot.lines:
		if lineObj.name == selectedLine:
			myLine = lineObj
			break
	if myLine == None:
		return
	# update color
	app.setButtonBg("colorPickerBtn",lineObj.color)
	# update axis
	if lineObj.isLeftAxis:
		app.setRadioButton("axisRadio","Left",callFunction=False)
	else:
		app.setRadioButton("axisRadio","Right",callFunction=False)
	# update weight
	app.setEntry("weightVal",lineObj.weight,callFunction=False)
	# update offset
	app.setEntry("offsetVal",lineObj.offset,callFunction=False)

def updateSubplotInfo():
	# update title
	graphData.subplots[graphData.currentIdx].title = app.getEntry("plotTitleVal")
	# update xLabel
	graphData.subplots[graphData.currentIdx].xLabel = app.getEntry("plotXlabelVal")
	# update y1Label
	graphData.subplots[graphData.currentIdx].y1Label = app.getEntry("plotY1labelVal")
	# update y2Label
	graphData.subplots[graphData.currentIdx].y2Label = app.getEntry("plotY2labelVal")
	# update y1Lim
	y1Min = app.getEntry("plotY1minVal")
	y1Max = app.getEntry("plotY1maxVal")
	if isinstance(y1Min,float) and isinstance(y1Max,float):
		graphData.subplots[graphData.currentIdx].y1Lim = [y1Min, y1Max]
	else:
		graphData.subplots[graphData.currentIdx].y1Lim = None
	# update y2Lim
	y2Min = app.getEntry("plotY2minVal")
	y2Max = app.getEntry("plotY2maxVal")
	if isinstance(y2Min,float) and isinstance(y2Max,float):
		graphData.subplots[graphData.currentIdx].y2Lim = [y2Min, y2Max]
	else:
		graphData.subplots[graphData.currentIdx].y2Lim = None
	# update plot
	executePlot()
	displaySubplotInfo()

def updateLineInfo():
	# get current line
	selectedLine = app.getOptionBox("lineSelector")
	mySubplot = graphData.subplots[graphData.currentIdx]
	myLineIdx = None
	for lineIdx,lineObj in enumerate(mySubplot.lines):
		if lineObj.name == selectedLine:
			myLineIdx = lineIdx
			break
	if myLineIdx == None:
		return
	# update color
	graphData.subplots[graphData.currentIdx].lines[myLineIdx].color = app.getButtonBg("colorPickerBtn")
	# update axis
	graphData.subplots[graphData.currentIdx].lines[myLineIdx].isLeftAxis = app.getRadioButton("axisRadio") == "Left"
	# update weight
	graphData.subplots[graphData.currentIdx].lines[myLineIdx].weight = app.getEntry("weightVal")
	# update offset
	graphData.subplots[graphData.currentIdx].lines[myLineIdx].offset = app.getEntry("offsetVal")
	# update plot
	executePlot()
	displayLineInfo()

def executePlot():
	plotSpaceFig.clear()
	nPlots = len(graphData.subplots)
	if nPlots == 0:
		app.refreshPlot("plottingSpace")
		return
	# find number of rows for subplots
	if nPlots == 1:
		nRows = 1
	else:
		nRows = 2
	# find number of columns for subplots
	if nPlots <= 2:
		nCols = 1
	elif nPlots <= 4:
		nCols = 2
	else:
		nCols = 3
	# create axes
	myAxes = []
	for axIdx in range(1,min(6,nPlots)+1):
		# create left y axis
		leftAxis = plotSpaceFig.add_subplot(nRows,nCols,axIdx)
		myAxes.append(leftAxis)
	# find subplot range to use, the selected one should be last, unless the previous ones are less than six
	# it might be better if it worked like pages
	if graphData.currentIdx < 5:
		plotIdxStart = 0
		plotIdxEnd = min(6, nPlots)-1
	else:
		plotIdxStart = max(0, graphData.currentIdx-5)
		plotIdxEnd = graphData.currentIdx
	# plot
	for subplotIdx in range(plotIdxStart,plotIdxEnd+1):
		axIdx = subplotIdx-plotIdxStart
		plotSingleSubplot(myAxes[axIdx], subplotIdx, highlightCurrent=True)

	app.refreshPlot("plottingSpace")


def plotSingleSubplot(leftAxis, subplotIdx, highlightCurrent=False):
	# plot lines
	rightAxis = None
	for lineIdx,lineObj in enumerate(graphData.subplots[subplotIdx].lines):
		dataLine = lastSolvedModel.model(graphData.timeData,graphData.dataset,lineObj.name)
		if lineObj.isLeftAxis:
			axToUse = leftAxis
		else:
			if rightAxis == None:
				rightAxis = leftAxis.twinx()
			axToUse = rightAxis

		if lineObj.color == None:
			cmap = plt.get_cmap("tab10")
			lineObj.color = cmap(lineIdx%10)
			# set color for future edits
			graphData.subplots[subplotIdx].lines[lineIdx].color = matplotlib.colors.rgb2hex(cmap(lineIdx%10)[:3])

		axToUse.plot(graphData.timeData, lineObj.offset+lineObj.weight*dataLine, label=lineObj.name, color=lineObj.color)

	# plot areas
	if graphData.subplots[subplotIdx].y1Lim == None:
		yMin = leftAxis.get_ylim()[0]
		yMax = leftAxis.get_ylim()[1]
	else:
		yMin = graphData.subplots[subplotIdx].y1Lim[0]
		yMax = graphData.subplots[subplotIdx].y1Lim[1]
	for areaLims in  graphData.areas:
		leftAxis.fill_between(areaLims, yMin, yMax, alpha=0.2)

	# add frame if current subplot
	if subplotIdx == graphData.currentIdx and highlightCurrent:
		xMin = graphData.timeData[0]
		xMax = graphData.timeData[-1]
		rectX = [xMin, xMax, xMax, xMin, xMin]
		rectY = [yMin, yMin, yMax, yMax, yMin]
		leftAxis.plot(rectX,rectY,color="red",linewidth=4)

	# set subplot info
	mySubplot = graphData.subplots[subplotIdx]
	leftAxis.set_title(mySubplot.title)
	leftAxis.set_xlabel(mySubplot.xLabel)
	leftAxis.set_ylabel(mySubplot.y1Label)
	if not rightAxis == None:
		rightAxis.set_ylabel(mySubplot.y2Label)
	leftAxis.set_xlim([graphData.timeData[0], graphData.timeData[-1]])
	if mySubplot.y1Lim == None:
		leftAxis.set_ylim([yMin, yMax])
	else:
		leftAxis.set_ylim(mySubplot.y1Lim)
	if (not mySubplot.y2Lim == None) and (not rightAxis == None):
		rightAxis.set_ylim(mySubplot.y2Lim)
	leftAxis.legend(loc="center left")
	if not rightAxis == None:
		rightAxis.legend(loc = "center right")


def exportSubplots():
	nPlots = len(graphData.subplots)
	if nPlots == 0:
		return;

	files = [('PDF', '*.pdf'),
		  ('PNG', '*.png')]
	myFile = app.saveBox(fileTypes = files, fileName = "TriSynPlots.pdf", parent="plottingWin")
	if myFile=="":
		return

	# determine number of rows and columns
	if nPlots == 1:
		nRows = 1
	elif nPlots <= 6:
		nRows = 2
	else:
		nRows = ceil(nPlots/3)
	if nPlots <= 2:
		nCols = 1
	elif nPlots <= 4:
		nCols = 2
	else:
		nCols = 3

	# create temporary figure to plot all the output
	tempFig = plt.figure(figsize = (nCols*6.4, nRows*4.8))

	for subIdx,subpplotObj in enumerate(graphData.subplots):
		myLeftAx = tempFig.add_subplot(nRows, nCols, subIdx+1)
		plotSingleSubplot(myLeftAx, subIdx, highlightCurrent=False)

	tempFig.savefig(myFile, bbox_inches="tight", pad_inches=0.4)


def addCustomLine():
	if len(graphData.subplots) == 0:
		return
	newLine = app.textBox("Custom Line", "Type your custom line:", parent="plottingWin")
	if newLine == None:
		# Cancel was pressed
		return
	try:
		lastSolvedModel.model(graphData.timeData,graphData.dataset,newLine)
	except:
		# line not defined
		print("Custom line not defined.")
		return
	graphData.subplots[graphData.currentIdx].addLine(newLine)

	# update plot and info
	executePlot()
	displaySubplotInfo()



### end of defined functions
### main run

# create a new gui
app = gui(geom="1100x850")

# set window's title
app.setTitle("TriSyn GUI")

# initialization of global variables
currentModel = None
lastSolvedModel = None
outputData = None
timeArr = None
firstPlot = True;
CurrentSolvedExperiment = None
graphData = None

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
		elif tutorialLine[0]=="img":
			app.addImage(lineLabel, tutorialLine[1])
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

	app.startScrollPane("paramScroll"+expVal[0])
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
		elif isinstance(parVal[2], dict):
			app.startFrame(parVal[0]+"Container",row=parIdx,column=1)
			# add list item
			defaultParameters = mf.getDefaultModelParameters()
			app.addTickOptionBox(parVal[0]+" Option List",defaultParameters[parVal[0]].keys(),row=0,column=0)
			app.setOptionBoxChangeFunction(parVal[0]+" Option List", getParamOptionHandler(parVal[0]))
			app.startFrame(parVal[0]+"ItemsFrame",row=1,column=0)
				# empty at creation
			app.stopFrame()
			app.stopFrame()
			continue

	# close single tab
	app.stopScrollPane()
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

# window init
app.setSticky("nswe")
app.setStretch("both")
app.startFrame("rootPlotWindow")

# left column: line lists, subplot controls
app.setExpand("row")
app.startFrame("controlsColumn",row=0,column=0)

app.setStretch("both")
app.addListBox("linesBox",mf.getModelOutputNames(),row=0,column=0,colspan=2)
app.selectListItemAtPos("linesBox",0,callFunction=False)

app.setStretch("column")
app.addNamedButton("Custom","customLineBtn",func=addCustomLine,row=1,column=0)
app.setButtonSticky("customLineBtn","ws")
app.addNamedButton("Add line","addLineBtn",func=addLine,row=1,column=1)
app.setButtonSticky("addLineBtn","es")

app.startFrame("subplotControllers",row=2,column=0,colspan=2)
app.addNamedButton("<","previousPlotBtn",func=focusPreviousSubplot,row=0,column=0)
app.addNamedButton("+","addPlotBtn",func=addSubplot,row=0,column=1)
app.addNamedButton(">","nextPlotBtn",func=focusNextSubplot,row=0,column=2)
app.setButtonSticky("previousPlotBtn","ews")
app.setButtonSticky("addPlotBtn","ews")
app.setButtonSticky("nextPlotBtn","ews")
app.stopFrame()

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

# right column: plot settings, export
app.setExpand("row")
app.startFrame("settingsColumn",row=0,column=2)

app.setStretch("column")
app.startLabelFrame("lineControls", hideTitle=False, label="Line Editor")
# line selector
app.addOptionBox("lineSelector",["- Lines -"],row=0,column=0,colspan=2)
app.setOptionBoxChangeFunction("lineSelector",displayLineInfo)
# color selector
app.setStretch("none")
app.addLabel("colorLabel", "Colour:",row=1,column=0)
app.setLabelSticky("colorLabel","w")
app.setStretch("column")
app.addNamedButton("", "colorPickerBtn", func=pickAColor, row=1, column=1)
app.setButtonSticky("colorPickerBtn","we")
defaultBtnColor = app.getButtonBg("colorPickerBtn")
# axis selector
app.startLabelFrame("axisControl", hideTitle=False, label="Axis", row=2, column=0, colspan=2)
app.addRadioButton("axisRadio","Left")
app.addRadioButton("axisRadio","Right")
app.setRadioButtonChangeFunction("axisRadio",updateLineInfo)
app.stopLabelFrame()
# size selector
app.addLabel("weightLabel","Weight:", row=3, column=0)
app.addNumericEntry("weightVal", row=3, column=1)
app.setEntry("weightVal",1)
app.setEntryWidth("weightVal",7)
app.setEntryChangeFunction("weightVal",updateLineInfo)
app.addLabel("offsetLabel","Offset:", row=4, column=0)
app.addNumericEntry("offsetVal", row=4, column=1)
app.setEntry("offsetVal",0)
app.setEntryWidth("offsetVal",7)
app.setEntryChangeFunction("offsetVal",updateLineInfo)
# delete curve
app.addNamedButton("Delete Line","deleteLineBtn",func=removeLine,row=5,column=1)
app.stopLabelFrame()

app.startLabelFrame("plotControls", hideTitle=False, label="Plot Editor")
# title entry
app.addLabel("plotTitleLabel","Title:",row=0,column=0)
app.addEntry("plotTitleVal",row=0,column=1,colspan=2)
app.setEntryChangeFunction("plotTitleVal",updateSubplotInfo)
# xLabel entry
app.addLabel("plotXlabelLabel","X label:",row=1,column=0)
app.addEntry("plotXlabelVal",row=1,column=1,colspan=2)
app.setEntryChangeFunction("plotXlabelVal",updateSubplotInfo)
# y1Label entry
app.addLabel("plotY1labelLabel","Y1 label:",row=2,column=0)
app.addEntry("plotY1labelVal",row=2,column=1,colspan=2)
app.setEntryChangeFunction("plotY1labelVal",updateSubplotInfo)
# y2Label entry
app.addLabel("plotY2labelLabel","Y2 label:",row=3,column=0)
app.addEntry("plotY2labelVal",row=3,column=1,colspan=2)
app.setEntryChangeFunction("plotY2labelVal",updateSubplotInfo)
# yLimits entry
app.addLabel("minAxisLabel","Min",row=4,column=1)
app.addLabel("maxAxisLabel","Max",row=4,column=2)
app.addLabel("plotY1limitsLabel","Y1 lim:",row=5,column=0)
app.addNumericEntry("plotY1minVal",row=5,column=1)
app.setEntryWidth("plotY1minVal",7)
app.setEntryChangeFunction("plotY1minVal",updateSubplotInfo)
app.addNumericEntry("plotY1maxVal",row=5,column=2)
app.setEntryWidth("plotY1maxVal",7)
app.setEntryChangeFunction("plotY1maxVal",updateSubplotInfo)
app.addLabel("plotY2limitsLabel","Y2 lim:",row=6,column=0)
app.addNumericEntry("plotY2minVal",row=6,column=1)
app.setEntryWidth("plotY2minVal",7)
app.setEntryChangeFunction("plotY2minVal",updateSubplotInfo)
app.addNumericEntry("plotY2maxVal",row=6,column=2)
app.setEntryWidth("plotY2maxVal",7)
app.setEntryChangeFunction("plotY2maxVal",updateSubplotInfo)
# delete subplot
app.addNamedButton("Delete Subplot","deleteSubplotBtn",func=removeCurrentSubplot, row=7,column=2)
app.stopLabelFrame()

# export button
app.addNamedButton("Export", "exportBtn", func=exportSubplots)
app.setButtonSticky("exportBtn","ne")

app.stopFrame()
app.setFrameSticky("settingsColumn","ens") # wens to stick to the plot


app.stopFrame()

initPlotWidow()
app.stopSubWindow()


# run the gui
app.go()