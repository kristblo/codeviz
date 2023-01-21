import re
import os
from global_utilities import *

#Identifying and treating include statements

#checks the config file for an includepattern statement,
#returns the compiled regex expression
def getIncludePattern(configFileName):    
    
    try:
        incpattern = getKeywordFromConfigFile(configFileName, 'includepattern')
        return incpattern

    except Exception as e:
        print(e)


#returns include statements in the investigated file
def findIncludeStatements(filestring, includepattern):
    includeStatements = []
    pattern = re.compile(includepattern)
    matches = pattern.findall(filestring)

    for entry in matches:
        strippedName = entry[0].strip("<>\'\"")
        includeStatements.append(strippedName)

    return includeStatements

#Attempts to find all full include paths for a file,
#choosing from all available files under the topdir
def findFullIncludePaths(currenFilePath, fileList, includePattern, config):
    inclog = str(getKeywordFromConfigFile(config, 'includelog'))
    filestring = getfFileAsString(currenFilePath)
    incStatements = findIncludeStatements(filestring, includePattern)
    fullIncludePaths = []
    danglingIncludes = []

    for inc in incStatements:
        candidates = []
        pattern = os.path.basename(inc)

        for item in fileList:
            itembasename = os.path.basename(item)
            try:
                if(re.match(pattern, itembasename).group() == pattern):
                    candidates.append(item)
            except:
                string = 'No match'

        if(len(candidates) == 0):            
            string = 'No candidates for: ' + inc + ' in ' + currenFilePath + '\n'
            #print(string)
            appendStringToFile(inclog, string)
            danglingIncludes.append(inc)
        elif(len(candidates) == 1):
            fullIncludePaths.append(candidates[0])
            string = 'Single candidate for ' + inc + ' in ' + currenFilePath + '\n: ' + str(candidates) + '\n0:' + candidates[0] + '\n\n'
            appendStringToFile(inclog, string)
        else:
            shortestDistance = 1000
            bestcandidate = ''
            for item in candidates:            
                distance = calculateDistance(currenFilePath, item)
                if distance < shortestDistance:
                    bestcandidate = item
                    shortestDistance = distance
            fullIncludePaths.append(bestcandidate)
            string = 'Multiple candidates for: ' + currenFilePath + ':' + inc + ':\n'
            appendStringToFile(inclog, string)
            for item in candidates:
                #print(item)
                appendStringToFile(inclog, item)
            string = 'Chose: ' + bestcandidate + '\n'
            appendStringToFile(inclog, string)


    
    for idx, name in enumerate(fullIncludePaths):
        fullIncludePaths[idx] = fullIncludePaths[idx].replace('\\', '/')

    return fullIncludePaths, danglingIncludes        

#Calculate inclusion matrix for entire project
def getProjectInclusionData(topDir, exclDirs, configFileName):
    #TODO: Implement
    #Matrix is size (all known files)*(all known files + dangling incs)
    includepattern = getIncludePattern(configFileName)
    allKnownFiles = findAllSourceFilePaths(topDir, exclDirs, configFileName)
    fullIncludePathsPerFile = {}
    danglingIncludesPerFile = {}
    

    #Find full include paths to all files in project
    #TODO: Improve to only look up files once
    for file in allKnownFiles:
        all = findFullIncludePaths(file, allKnownFiles, includepattern, configFileName)
        full = all[0]
        dangling = all[1]
        fullIncludePathsPerFile[file] = full
        danglingIncludesPerFile[file] = dangling
    
    #Create a catalogue of all dangling files in the project
    danglingIncludesInProject = []
    for fileName in danglingIncludesPerFile:
        for dangler in danglingIncludesPerFile[fileName]:
            if(dangler not in danglingIncludesInProject):
                danglingIncludesInProject.append(dangler)
    
    #Generate the final inclusion matrix
    numKnownFiles = len(allKnownFiles)
    numDanglers = len(danglingIncludesInProject)
    inclusionMatrix = []
    inclusionDict = {}

    for file in fullIncludePathsPerFile:
        includesInThis = fullIncludePathsPerFile[file]
        danglersInThis = danglingIncludesPerFile[file]        
        matrixRow = [0]*numKnownFiles + [0]*numDanglers
        
        for i in range(0, numKnownFiles):
            if(allKnownFiles[i] in includesInThis):
                matrixRow[i] = 1
        for i in range(0, numDanglers):
            if(danglingIncludesInProject[i] in danglersInThis):
                matrixRow[numKnownFiles + i] = 1
        inclusionMatrix.append(matrixRow)       
        inclusionDict[file] = matrixRow

    #Distance matrix must be (numKnown+numDanglers)^2
    distanceMatrix = []
    danglerWeight = 10
    for file in fullIncludePathsPerFile:
        includesInThis = fullIncludePathsPerFile[file]                
        matrixRow = []

        #First, calculate the distance to all known files
        for i in range(0, numKnownFiles):
            matrixRow.append(calculateDistance(file, allKnownFiles[i]))
        
        #Then add all the danglers with a constant, high, weight
        matrixRow = matrixRow + [danglerWeight]*numDanglers
        distanceMatrix.append(matrixRow)

    danglerInternalWeight = 5
    for file in danglingIncludesInProject:
        #Danglers should have low relative weight, but high compared to known
        matrixRow = [danglerWeight]*numKnownFiles + [danglerInternalWeight]*numDanglers
        distanceMatrix.append(matrixRow)
    
    return inclusionMatrix, inclusionDict, allKnownFiles, danglingIncludesInProject, distanceMatrix