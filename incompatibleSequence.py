import ps
from ps import model
from optparse import OptionParser
from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
import sys, os
import logging
import csv
from psPythonUtil import *
import gviz_api
import threading
import webbrowser
import time
import ast
from collections import deque
from collections import Counter

def initalizeMe():
	solveModes = ('solve', 'repair')
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-m", "--mode", dest="solveMode", help="solve or repair")
	options, args = parser.parse_args()
	
	return solveModes, options, args

def psIncompatible(model, outputDir, incompatibleList, resInGroup):
	log.info('\tExporting Resource Schedule:')
	resSeq = {}
	incompatibleAttr = model.getAttributes()['INCOMPATIBLE']
	incompatibleYes = incompatibleAttr.findValue('YES')
	res = model.getResources()
	
	for resource in resInGroup:	
		r = res[resource]
		resSched = model.solution.findResourceSchedule( r )
		if resSched:
			sequence=deque([])
			for ai in resSched:
				w = ai.getWorkOrderOperation()
				if w:
					itemCode = w.getWorkOrder().item.code
					if len(sequence) < 2:
						sequence.append(itemCode)
					else:
						sequence.popleft()
						sequence.append(itemCode)
		
				if list(sequence) in incompatibleList:
					ai.changeAttributeValue(incompatibleYes)

def getResFromGroup(model, resGroupName):
	'''
		Get resources for a given resource group
	'''
	resGroup = model.getResourceGroups()
	r = resGroup[resGroupName].getElements()
	resources = []
	for res in r:
		resources.append(res.code)
	
	return resources

if __name__ == "__main__":	
	configFile = os.path.join( os.getcwd(), 'psPythonConfig.xml')
	variables = setVariables(configFile)
	for key,val in variables.items():
		exec(key + '=val')
	log = setLog(logname, psOutputDirectory)
	outDir = variables['psOutputDirectory']
	myModel = getModel()	
	sequenceList = ast.literal_eval(incompatibleSequence)
	resInGroup = getResFromGroup(myModel, resourceGroup)
		
	solveModes, options, args = initalizeMe()
	if options.solveMode is not None and not options.solveMode in solveModes:
		parser.error("Invalid solve mode '" + options.solveMode + " '")
	
	if options.solveMode == 'solve' or 'repair':
		psIncompatible(myModel, outDir, sequenceList, resInGroup)

