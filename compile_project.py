# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 19:48:45 2022

@author: krist
"""
from parsefile import *


startFile = openFile('/home/kristian/byggern-nicer_code/main.c')
topDir = '/home/kristian/byggern-nicer_code/'
homeDir = re.split('/', topDir)[-2]+'/'
excludeddirs = ['.vs', 'sam', 'build']
excludedsyms = ['if', 'else', 'for', 'while', 'printf']

includePaths = findAllIncludePaths(startFile, topDir, excludeddirs)
sourceDirs = returnSubdirs(topDir, excludeddirs)

allfiles = []
for item in sourceDirs:
    allfiles.extend(findSourceFiles(item))
graphNodes = [] #list of File objects which will be fed to graphing tool
missingout = [] #Files for which a full include path could not be found

for file in allfiles:    
    
    results = findAllIncludePaths_v2(file, allfiles)
    includes = results[0]
    missingout.extend(results[1])

    functioncalls = findFuncsAndArgs(file, excludedsyms)    
    
    #populate list of objects
    graphNodes.append(File(file, topDir))    

for fileObject in graphNodes:
    fileObject.setIncludes(findAllIncludePaths_v2(fileObject.absPath, allfiles)[0])
    fileObject.setFunctioncalls(findFuncsAndArgs(fileObject.absPath, excludedsyms))
    fileObject.setShortPath()
    fileObject.setShortenedIncludes(shortenIncludes(fileObject.includes, topDir, homeDir))

with open('fileobjects.txt', 'w') as outfile:
    for obj in graphNodes:
        writeFiletotxt(outfile, obj)