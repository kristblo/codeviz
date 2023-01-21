# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 21:24:44 2022

@author: krist
"""

import re
import regex
import os
#import graphviz
import sys

#This script focuses on the dissection of a single file into its components.
#If necessary, design with width-first approach in mind.

# 1. Open file
def openFile(filename):
    try:
        file = open(filename,  'r')
        out = file.read()
    
    except Exception as e:
        out = 'File: ' + filename + ' could not be opened'
        print(out, e)
    
    return out

# 2. Find, store and count includes: full path

def findIncludes(filestring):
    includes = []
    
    pattern = re.compile('#include ([\'\"<](\w|[\.\/])*[\'\">])')
    matches = pattern.findall(filestring)
    
    for entry in matches:
        strippedName = entry[0].strip("<>\'\"")
        includes.append(strippedName)
    
    return includes


def hasExcludedName(filename, excludedNames):
    forbidden = False
    
    for name in excludedNames:
        pattern = re.compile(name)
        if pattern.search(filename):            
            forbidden = True    
    return forbidden


def findAllSubdirs(topDir, subdirs, excludedDirs):
    
    for name in os.scandir(topDir):
        if name.is_dir():
            if (name not in subdirs and (hasExcludedName(str(name), excludedDirs) == False)):
                subdirs.append(name.path)                
                findAllSubdirs(topDir+name.name+'/', subdirs, excludedDirs)        
            
def returnSubdirs(topDir, excludedDirs):
    subdirs = []
    subdirs.append(topDir) #is this a bit cursed?
    
    findAllSubdirs(topDir, subdirs, excludedDirs)

    #enumeration ensures actual subdir-item is altered
    for idx, item in enumerate(subdirs):
        if subdirs[idx][-1] != '/':
            subdirs[idx] = subdirs[idx]+'/'
    
    return subdirs



#util to find the number of folders between two files
#TODO: rigorize to be less dependent on correct type of \ /
def calculateDistance(file1, file2):
    path1 = os.path.dirname(file1)
    path2 = os.path.dirname(file2)
    common = os.path.commonpath([path1, path2])    
    commondirs = common.split('\\')
    dirs1 = path1.split('/')
    dirs2 = path2.split('/')
    
    distFromCommon1 = abs(len(dirs1)-len(commondirs))
    distFromCommon2 = abs(len(dirs2)-len(commondirs))
    
    distance = distFromCommon1 + distFromCommon2
    
    
    return distance

def isSourceFile(filename):
    pattern = re.compile('^.*\.(c|h|py|hpp)$') #edit to add or remove files to include
    if pattern.search(filename):
        return True
    else:
        return False
    
def findSourceFiles(dirName):
    sourceFiles = []
    for item in os.scandir(dirName):
        if isSourceFile(item.name):
            sourceFiles.append(dirName + item.name)
            
    return sourceFiles
    
    
    

#Make an educated guess as to where the included file originated
def findFullIncludePath(possibleDirs, incFilename, orgFilename):    
    hits = []    
    for directory in possibleDirs:
        for name in os.scandir(directory):            
            if (name.name == incFilename):
                hits.append(name.path)                    
    #is there more than one file of this file name? Trivial if no
    if len(hits) == 1:        
        return hits[0]
    
    #if multiple hits: probably the one closest to the origin file
    #TODO:Implement using orgFilename
    if len(hits) > 1:
        #print(os.path.abspath(hits[1]) + os.path.abspath(orgFilename))
        shortestDist = 1000 #start with a very high weight. TODO: learn graph stuff
        nameofshortest = ''
        for hit in hits:
            currentDist = calculateDistance(hit, orgFilename)
            if currentDist < shortestDist:
                shortestDist = currentDist
                nameofshortest = hit
        return nameofshortest
        
    
    #unable to find it? Return the file name
    if len(hits) == 0:        
        return incFilename

#solution to task 2
def findAllIncludePaths(filename, topDir, exlDirs):
    file =  openFile(filename)
    rawincludes = findIncludes(file)
    subDirs = returnSubdirs(topDir, exlDirs)    
    
    allPaths = []
    for file in rawincludes:
        fullPath = findFullIncludePath(subDirs, file, filename)
        allPaths.append(fullPath)
    
    if len(allPaths) == 0:
        allPaths.append('no_includes')        
        
    cleanPaths = []
    for path in allPaths:        
        clean = path.replace('\\', '/')
        cleanPaths.append(clean)    
    #print(cleanPaths, '\n')
        
    return cleanPaths

#hopefully faster
def findAllIncludePaths_v2(currentFile, fileCatalogue):
    file = openFile(currentFile)
    rawincludes = findIncludes(file)
    fullIncludes = []
    
    missing = []    

    for inc in rawincludes:
        candidates = []
        pattern = os.path.basename(inc)
        for item in fileCatalogue:
            itembase = os.path.basename(item)
            try:
                if re.match(pattern, itembase).group() == pattern:
                    candidates.append(item)
            except:
                string = 'No match'
        if len(candidates) == 0:
            fullIncludes.append(inc)         
            string = 'No candidates for: ' + inc + ' in ' + currentFile +'\n'                 
            missing.append(string)
            
            
        elif len(candidates) == 1:
            fullIncludes.append(candidates[0])
            string = 'Single candidate for ' + inc + ' in ' + currentFile + '\n: ' + str(candidates) + '\n0:' + candidates[0] + '\n\n'
            missing.append(string)
        else:            
            shortestDist = 1000
            bestcandidate = ''
            for item in candidates:
                distance = calculateDistance(currentFile, item)
                if distance < shortestDist:
                    bestcandidate = item
                    shortestDist = distance
            fullIncludes.append(bestcandidate)
            print('Multiple candidates for: ', currentFile, ':', inc, ':\n')
            for item in candidates:
                print(item)
            print('Chose: ', bestcandidate,'\n')
            
    for idx, name in enumerate(fullIncludes):
        fullIncludes[idx] = fullIncludes[idx].replace('\\', '/')
        
    return fullIncludes, missing

# 3. Find, store and count function calls: also args in the call?
# Rules:
#     1. Must be a user-defined string followed immediately by an opening parenthesis
#     2. The opening parenthesis can be followed by anything, incl. 
            # 2.1 whitespace,
            # 2.2 escape chars,
            # 2.3 more parentheses
#     3. The function call ends in a closing parenthesis
            # 3.1 Almost always followed by a semicolon
#     4. Args are comma-separated
#     5. A valid call will not be inside a string


def findCandidateFcCalls(filename):    
    pattern = '(\w+\(([^()]|(?R)*)*\))'
    candidates_raw = regex.findall(pattern, filename)
    #does not return recursively found function calls, will need to deal with that
    #dealt with by findFuncsAndArgs
    
    calls = []
    for el in candidates_raw:
        calls.append(el[0])
        
        
    return calls
    
def findFcName(fcCall):
    fcPtrn = re.compile('(\w)+\(')
    fcName = fcPtrn.match(fcCall)

    if(fcName):
        return fcName.group().strip("(")



#not used in solution
def findAllFuncs(fcCndList):
    funcs = []
    for fcCnd in fcCndList:
        funcs.append(findFcName(fcCnd))
        
    return funcs

def findArgs(fcCall):
    argPtn = '\(([^()]|(?R)*)*\)'
    arguments_raw = regex.search(argPtn, fcCall)
    
    argstr = arguments_raw.group()[1:-1] #strips surrounding parentheses
    args = re.split(', ', argstr)
    for arg in args:
        arg.strip('[\s]')
    
    return args

def isCallCtrlsig(call, ctrlSigs):
    for sig in ctrlSigs:
        if call == sig:            
            return True
    return False

#solution to task 3
#Doesn't differentiate between function calls and declarations
def findFuncsAndArgs(filename, excluded):
    file = openFile(filename)
    functioncalls = findCandidateFcCalls(file)    
    functionList = []
    
    for call in functioncalls:        
        function = findFcName(call)
        if not isCallCtrlsig(function, excluded):
            args = findArgs(call)        
            functionList.append((function, args))
            
            for el in findArgs(call):
                if(len(findCandidateFcCalls(el)) >= 1):                
                    functioncalls.append(findCandidateFcCalls(el)[0])
                    
    if len(functionList) == 0:        
        functionList.append(('No calls', ['No args']))
    
    return functionList        

# 4. Find, store and count variables: types and names?
# 5. FSC function declarations: return types and args?
# 6. FSC class declarations
# 7. Find relations between vars and function calls, i.e. how data is manipulated

#8. Write to file?

#9. Store the information in an object
class File:
    def __init__(self, aAbsPath, aTopDir):
        self.name = os.path.basename(aAbsPath)
        self.path = os.path.dirname(aAbsPath)
        self.absPath = aAbsPath
        self.topDir = aTopDir
        
            
    includes = []    
    shortIncludes = []
    functioncalls = {}        
    
    
    def setIncludes(self, includelist):
        self.includes = includelist
        
    def addInclude(self, includefile):
        if includefile not in self.includes:
            self.includes.append(includefile)
            
    def setFunctioncalls(self, calldict):
        self.functioncalls = calldict
    
    def addFunctioncall(self, calltuple):
        self.functioncalls[calltuple[0]] = calltuple[1]
        
    def setShortPath(self):
        self.homeDir = re.split('/', self.topDir)[-2]+'/'        
        self.shortpath = self.homeDir + re.split(self.topDir, self.absPath)[1]
        self.shortpathBase = os.path.dirname(self.shortpath)
        
    # def shortenIncludes(self):
    #     #pattern = re.compile(self.topDir)
    #     for item in self.includes:       
    #         if len(re.findall(topDir, item)) > 0:
    #             shortInclude = self.homeDir + re.split(self.topDir, item)[1]
    #             self.shortIncludes.append(shortInclude)
                
    #         else:
    #             self.shortIncludes.append(item)
    
    def setShortenedIncludes(self, shortlist):
        self.shortIncludes = shortlist

def shortenIncludes(includeList, topDir, homeDir):
    shortened = []
    for item in includeList:
        if len(re.findall(topDir, item)):
            current = homeDir + re.split(topDir, item)[1]
            shortened.append(current)
        else:
            shortened.append(item)
            
    return shortened

def writeFiletotxt(outfile, file):    
    name = '----------'+file.name + '----------\n'
    outfile.write(name)
    abspath = 'Absolute path: '+ file.absPath + '\n'
    outfile.write(abspath)
    
    outfile.write('\n\nIncludes:\n')
    for include in file.includes:
        inc = include + '\n'
        outfile.write(inc)
        
    outfile.write('\n\nShort form includes:\n')
    for short in file.shortIncludes:
        shortinc = short + '\n'
        outfile.write(shortinc)
        
    outfile.write('\n\nFunction calls:\n')
    for item in file.functioncalls:
        outstr = item[0] + ':' + str(item[1]) + '\n'
        outfile.write(outstr)
        
        
    footer = '--------------------------------\n\n\n'
    outfile.write(footer)
    
#10. Utility functions for exploration
#check if a file contains a certain function call
def findCall(callname, fileObject):
    for call in fileObject.functioncalls:
        if call[0]==callname:
            return True
    return False

#check if a file includes a file from a certain folder
def assertIncludeFolder(checkFolder, fileObject):
    for include in fileObject.shortIncludes:
        folder = os.path.dirname(include)
        if folder == checkFolder:
            return True
    return False
        

#----
#main
# test = openFile('main.c')
# #topDir = sys.argv[0]
# homeDir = re.split('/', topDir)[-2]+'/'
# excludeddirs = ['.vs', 'sam', 'build']
# #excludeddirs = ['.git', '.vscode', 'asio', 'build', 'doc', 'experimental', 'Jackal_head_in_a_jar', 'JackalNode_Test', 'lib', 'msvc']
# excludedsyms = ['if', 'else', 'for', 'while', 'printf']

# part2test = findAllIncludePaths(test, topDir, excludeddirs)


# functest = findCandidateFcCalls(test)
# allFuncs = findAllFuncs(functest)
# argtest = findArgs(functest[40])
# part3test = findFuncsAndArgs(test, excludedsyms)

# fileTest = File(topDir+'main.c', topDir)
# fileTest.setIncludes(part2test)
# fileTest.setFunctioncalls(part3test)
# fileTest.setShortPath()
# fileTest.setShortenedIncludes(shortenIncludes(fileTest.includes, topDir, homeDir))

# #---
# #Test in a full-project setting:
# sourceDirs = returnSubdirs(topDir, excludeddirs)
# allfiles = []
# #inc.findAndFilter(topDir, allfiles, excludeddirs)
# for item in sourceDirs:
#     allfiles.extend(findSourceFiles(item))


# allnodes = {}
# nodeObjectTest0 = []
# nodeObjectTest1 = {}
# missingout = []
# for file in allfiles:
    
#     results = findAllIncludePaths_v2(file, allfiles)
#     includes = results[0]
#     missingout.extend(results[1])
#     functioncalls = findFuncsAndArgs(file, excludedsyms)
#     allnodes[file] = includes, functioncalls
    
#     #populate list of objects
#     nodeObjectTest0.append(File(file, topDir))    
#     nodeObjectTest1[file] = File(file, topDir)
    
# for fileObject in nodeObjectTest0:
#     fileObject.setIncludes(findAllIncludePaths_v2(fileObject.absPath, allfiles)[0])
#     fileObject.setFunctioncalls(findFuncsAndArgs(fileObject.absPath, excludedsyms))
#     fileObject.setShortPath()
#     fileObject.setShortenedIncludes(shortenIncludes(fileObject.includes, topDir, homeDir))
    

# # for fileObject in nodeObjectTest1:
# #     currentFile = nodeObjectTest1[fileObject]
# #     currentFile.setIncludes(findAllIncludePaths(currentFile.absPath, topDir, excludeddirs))
# #     currentFile.setFunctioncalls(findFuncsAndArgs(currentFile.absPath, excludeddirs))    

# with open('fileobjects.txt', 'w') as outfile:
#     for obj in nodeObjectTest0:
#         writeFiletotxt(outfile, obj)

# with open('outputlog.txt', 'w') as log:
#     for line in missingout:
#         log.write(line)

# #Graphviz
# #NOTE: For subgraphs, scan through each dir and group each node
# foldernames = {}
# for fileObject in nodeObjectTest0:
#     try:
#         foldernames[fileObject.shortpathBase].append(fileObject.name)
#     except:
#         foldernames[fileObject.shortpathBase] = [fileObject.name]


# maingraph = graphviz.Digraph(comment = 'Testgraph_v2')
# # maingraph.overlap = -100000
# # maingraph.stagger = 3
# # maingraph.label='graph2'
# subgraphs = []
# nodes = []
# for key in foldernames:    
#     subname = 'cluster_'+key+'/'
#     subgraphs.append(graphviz.Digraph(name=subname, comment=key))
    
    
# for fileObject in nodeObjectTest0:
#     for sub in subgraphs:
#         if fileObject.shortpathBase == sub.comment:
#             if findCall('updateOutcome', fileObject):
#                 sub.node(name=fileObject.shortpath, label=fileObject.name, shape='box', color='green')
#             elif assertIncludeFolder('cppr/include/Hardware', fileObject):
#                 sub.node(name=fileObject.shortpath, label=fileObject.name, shape='box', color='yellow')                
        
#             else:
#                 sub.node(name=fileObject.shortpath, label=fileObject.name, shape='box')                 
            
            
# for sub in subgraphs:
#     maingraph.subgraph(sub)
#     sub.unflatten(stagger=3)    
    
# def isListed(include, fileList):
#     listed = False
#     for item in fileList:
#         if (include == item.absPath or include == item.shortpath):
#             listed = True
#             return listed
#     return listed

# redEdgeHighlights = []
# blueEdgeHighlights = ['cppr/include/Hardware/Tickable.h']
    

# for fileObject in nodeObjectTest0:
#     for include in fileObject.shortIncludes:        
#         try:
#             if(include != 'no_includes' and not isListed(include, nodeObjectTest0)):
#                 # maingraph.node(name=include, label=include, shape='oval', color='magenta', group='libs')                
#                 # maingraph.edge(include, fileObject.shortpath, color='gray')
#                 dummy=0
            
#             elif(include != 'no_includes' and isListed(include,  nodeObjectTest0)):
#                 if (include in redEdgeHighlights):
#                     maingraph.edge(include, fileObject.shortpath, color='red')
#                 # elif (findCall('updateOutcome', fileObject)):
#                 #     maingraph.edge(include, fileObject.shortpath, color='green')
#                 elif (blueEdgeHighlights[0] in fileObject.shortIncludes):
#                     maingraph.edge(include, fileObject.shortpath, color='blue')
#                 else:
#                     maingraph.edge(include, fileObject.shortpath)
#         except:
#             print('Edgecreation failed')

# staggered = maingraph.unflatten(stagger=(5), fanout=(True))
    
# maingraph.render('Testgraph_v2')
# staggered.render('Testgraph_v2.1')
