# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:11:05 2020

@author: toalu
"""

from appJar import gui
import model_functions as mf
import random



def pickAColor():
	oldColour = app.getButtonBg("colorPickerBtn")
	newColour = app.colourBox(colour=oldColour,parent=None)
	app.setButtonBg("colorPickerBtn",newColour)

def initPlotWidow():
	plotSpaceFig.clear()
	axes1_1 = plotSpaceFig.add_subplot(2,3,random.randint(1,6))
	axes1_2 = plotSpaceFig.add_subplot(2,3,random.randint(1,6))
	app.refreshPlot("plottingSpace")

app = gui()
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

controlsColumnWidth = app.getFrameWidget("controlsColumn").winfo_width()
settingsColumnWidth = app.getFrameWidget("settingsColumn").winfo_width()
# app.getFrameWidget("rootPlotWindow").bind("<Configure>",lambda e: resizeCallback(),add="+")

# run app
app.go()

