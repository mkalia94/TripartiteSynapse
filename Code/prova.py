import tps
from numpy import sin, pi, arange
from appJar import gui
import random
import matplotlib.pyplot as plt
import numpy as np

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
                 'nosynapse': False}
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
		"Wg"]
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
			["nogates","No Gates",True],
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
			["nogates","No Gates",True],
			["solve","Solve",True],
			["savenumpy","Save numpy",False],
			["savematlab","Save matlab",False],
			["Plot","Plot",True]]]]
	return experimentList

def getTutorialPages():
	# tutorialText = [label | title | lines]
	# lines = [style | text]
	# style = {"h1","h2","p"}
	tutorialText = [
		["tutorialTab1","Introduction",[
		  ["h1","Title"],
		  ["h2","Sub title"],
		  ["p","Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."],
		  ["h2","Another sub title"],
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


# application's functions
def plotSomething():
	x = [1, 2, 3]
	y = [0, 1, 0]
	axes.clear()
	axes.plot(x,y)
	app.refreshPlot("plotFig")
	showLabels()


def updateModel():
	paramdict = getDefaultModelParameters()
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
	modelInfo = getModelInfo()
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
				axes.plot(timeArr, outputData[:,itemIdx], label=itemLabel)

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
	app.addTickOptionBox("Graphs", getModelOutputNames(), row=0,column=3,rowspan=1,colspan=2)
	app.setOptionBoxChangeFunction("Graphs", plotModel)
	app.setOptionBoxSticky("Graphs","ne")
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
# style = {"h1","h2","p"}
tutorialText = getTutorialPages()
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
experimentList = getExperimentParameters()

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
modelInfo = getModelInfo()
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

# myAttrFile = open("C:/Users/toalu/Google Drive/UTwente/Work/TriSyn GUI/prova gui/gui_attributes.txt","w")
# for att in dir(app):
# 	myAttrFile.write(att+"\n")
# 	#print(att)#, getattr(app,att)
# myAttrFile.close()


# run the gui
app.go()
#no code after this line
