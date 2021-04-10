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


def openSub1():
	app.showSubWindow("subWin1")

def askAString():
	newString = app.textBox("New String","ciao, come stai?:", parent="subWin1")
	print(newString)


usePlots = True
app = gui()
app.addLabel("myLabel","Hello World")
app.addButton("Go",solve)
app.addButton("Win",openSub1)

app.startSubWindow("subWin1", title="Sub win 1", modal=True, blocking=False, transient=False)
app.addNamedButton("String","newWinBtn",func=askAString)

app.stopSubWindow()


app.go()
