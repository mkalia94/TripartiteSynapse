# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:11:05 2020

@author: toalu
"""

from appJar import gui
import model_functions as mf
import random
import tps
import matplotlib.pyplot as plt
import matplotlib

# setup, do not copy
paramdict = mf.getDefaultModelParameters()
myModel = tps.fmclass(paramdict)
timeArr,outputData = tps.exec_solve(myModel)

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


# function definitions
def pickAColor():
	oldColour = app.getButtonBg("colorPickerBtn")
	newColour = app.colourBox(colour=oldColour,parent=None)
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
		print(y1Min)
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
	if nPlots <= 2:
		nRows = 1
	else:
		nRows = 2
	# find number of columns for subplots
	if nPlots == 1:
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
		# create right y axis
		rightAxis = leftAxis.twinx()
		myAxes.append([leftAxis,rightAxis])
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

		# plot lines
		for lineIdx,lineObj in enumerate(graphData.subplots[subplotIdx].lines):
			dataLine = myModel.model(graphData.timeData,graphData.dataset,lineObj.name)
			if lineObj.isLeftAxis:
				axPosIdx = 0
			else:
				axPosIdx = 1

			if lineObj.color == None:
				cmap = plt.get_cmap("tab10")
				lineObj.color = cmap(lineIdx%10)
				# set color for future edits
				graphData.subplots[subplotIdx].lines[lineIdx].color = matplotlib.colors.rgb2hex(cmap(lineIdx%10)[:3])

			myAxes[axIdx][axPosIdx].plot(graphData.timeData, lineObj.offset+lineObj.weight*dataLine, label=lineObj.name, color=lineObj.color)

		# plot areas
		if graphData.subplots[subplotIdx].y1Lim == None:
			yMin = myAxes[axIdx][0].get_ylim()[0]
			yMax = myAxes[axIdx][0].get_ylim()[1]
		else:
			yMin = graphData.subplots[subplotIdx].y1Lim[0]
			yMax = graphData.subplots[subplotIdx].y1Lim[1]
		for areaLims in  graphData.areas:
			myAxes[axIdx][0].fill_between(areaLims, yMin, yMax, alpha=0.2)

		# add frame if current subplot
		if subplotIdx == graphData.currentIdx:
			xMin = graphData.timeData[0]
			xMax = graphData.timeData[-1]
			rectX = [xMin, xMax, xMax, xMin, xMin]
			rectY = [yMin, yMin, yMax, yMax, yMin]
			myAxes[axIdx][0].plot(rectX,rectY,color="red",linewidth=4)

		# set subplot info
		mySubplot = graphData.subplots[subplotIdx]
		myAxes[axIdx][0].set_title(mySubplot.title)
		myAxes[axIdx][0].set_xlabel(mySubplot.xLabel)
		myAxes[axIdx][0].set_ylabel(mySubplot.y1Label)
		myAxes[axIdx][1].set_ylabel(mySubplot.y2Label)
		myAxes[axIdx][0].set_xlim([graphData.timeData[0], graphData.timeData[-1]])
		if mySubplot.y1Lim == None:
			myAxes[axIdx][0].set_ylim([yMin, yMax])
		else:
			myAxes[axIdx][0].set_ylim(mySubplot.y1Lim)
		if not mySubplot.y2Lim == None:
			myAxes[axIdx][1].set_ylim(mySubplot.y2Lim)

	app.refreshPlot("plottingSpace")




app = gui() # do not copy

# data init, this should be created when the plot is available
graphData = cGraphs(timeArr,outputData,areas=[[1, 15], [20, 30]])

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
app.addNamedButton("Custom","customLineBtn",func=None,row=1,column=0)
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

# right column: plot settings
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

app.stopFrame()
app.setFrameSticky("settingsColumn","ens") # wens to stick to the plot

app.stopFrame()

initPlotWidow()

# run app
app.go()

