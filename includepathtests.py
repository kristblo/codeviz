import re
import os
import json
#import graphviz


def readfile(filename):    
    
    try:
        file = open(filename,  'r')
        out = file.read()
    except:
        out = "The file " + filename + " could not be opened"    
        #print(out)
    return str(out)

def writeFile(filename, string):
    try:
        file = open(filename, 'w')
        file.write(string + '\n')
        file.close()
    except:
        print('Could not write to file')
            


def getIncludeFileNames(sourceAsList):
    IncludedFileNames = []
    
    for el in sourceAsList:
        
        includePattern = re.compile('#include', re.IGNORECASE)
        isInclude = includePattern.match(el) #could also use .search(el) for entire string
       
        if isInclude: #returns None if no match, which Python interprets as 0
        
            includedFilePattern = re.compile('[\'\"<](\w|[./])*[\'\">]')
            try:
                
                includedFileName = includedFilePattern.search(el).group()            
            except:
                includedFileName = "getIncludeFileNames failed"
                
            strippedName = includedFileName.strip("<>\'\"")
            IncludedFileNames.append(strippedName)
        
    if(len(IncludedFileNames) == 0):
        IncludedFileNames.append('No includes found')
            
    return IncludedFileNames
    
# Explanation for includedFilePattern:
#     First character group [...] looks for the first instance
#     of ', " or <. Then the repeated pattern (...)* looks for any
#     alphanumerical character \w, period or forward slash. 
#     Lastly, the final character group [...] looks for any ', " or >. 
#     This ends the pattern. The symbols should cover most non-alphanum
#     characters used in include filepaths.
#     Most of the backslashes in the expression are there to deal with
#     python's string interpretation. The Regex on its own would look like
#     this: ['"<](\w|[\./]])*['">]
#     We see that w and . have special meanings in Regex.
    

def generateFileName(filePath, fileName):
    return filePath + fileName

def generateSourceList(filename):    
    fileString = readfile(filename)
    listifiedFile = re.split('\n', fileString)
    
    return listifiedFile


### Depth first approach

def recursiveIncludes(sourceDir, entryPoint):    
    if(entryPoint != 'No includes found'):
        
        currentName = generateFileName(sourceDir, entryPoint)
        currentFile = generateSourceList(currentName)    
        masterDictionary = {}    
        masterDictionary[entryPoint] = getIncludeFileNames(currentFile)
        
        for el in masterDictionary[entryPoint]:         
            if(el != 'No includes found'):
                masterDictionary[el] = recursiveIncludes(sourceDir, el)
            
        return masterDictionary
    
    
    
def printDict(dictionary):
    for key, val in dictionary.items():
        if (isinstance(val, dict)):
            printDict(val)
        #else:
            print(key, ' has \n', val, '\n')
            

def flattenDict(deepDict, outputDict):
    
    for key, val in deepDict.items():
        if not (isinstance(val, dict)):
            outputDict[key] = val
        else:
            flattenDict(val, outputDict)
            

### Width first approach
#Find all the files in the directories under topDir. These are the files
#we will be looking in.
def findAllNames(topDir, nameList):        
    
    for name in os.scandir(topDir):
        if name.is_dir():
            findAllNames(topDir+name.name+'/', nameList)
        else:            
            nameList.append(name.path)
            
#Try to determine whether or not a file is a source file (.c, .h, .cpp etc)
def isSourceFile(filename):
    pattern = re.compile('^.*\.(c|h|py|make|cpp|hpp)$') #edit to add or remove files to include
    if pattern.search(filename):
        return True
    else:
        return False

def hasExcludedName(filename, excludedNames):
    forbidden = False
    
    for name in excludedNames:
        pattern = re.compile(name)
        if pattern.search(filename):            
            forbidden = True
            
    return forbidden
        
        
        
        

#From the full list of names, filter out the ones we aren't interested in
def filterRelevant(filenames, excludedNames):
    
    relevantNames = []
    for el in filenames:
        if isSourceFile(el) and not hasExcludedName(el, excludedNames):
            relevantNames.append(el)
    return relevantNames

#Strip top level names for readability
def stripTopLevel():
    return 0

def findAndFilter(topDir, nameList, exNames): #try to save memory by filtering immediately
    for name in os.scandir(topDir):
        if name.is_dir():
            findAndFilter(topDir+name.name+'/', nameList, exNames)
        else:
            if(isSourceFile(name.name) and not hasExcludedName(name.path, exNames)):
                nameList.append(name.path)
    

#Do the thing
def buildIncludes(topDir, excludedNames):
    #allNames = []
    #findAllNames(topDir, allNames)
    #relevantNames = filterRelevant(allNames, excludedNames)
    relevantNames = []
    findAndFilter(topDir, relevantNames, excludedNames)
    
    masterDictionary = {}
    for currentName in relevantNames:
        currentFileAsList = generateSourceList(currentName)                
        if(os.path.basename(currentName) not in masterDictionary):
            masterDictionary[os.path.basename(currentName)] = getIncludeFileNames(currentFileAsList)        
            
    return masterDictionary
        
    
    
    
    
        
#####################

#sourceDirectory = 'C:/Users/krist/Dropbox/Stuff/Semester 5/TTK4155 Byggern/Kode/byggern-nicer_code/'
sourceDirectory = 'C:/Users/krist/Dropbox/Jobbrelatert/ESA Internships/JACKAL/onboard_repo/Jackal-Onboard-Software/'
entryPoint = 'main.c'

fileToRead = readfile(sourceDirectory + entryPoint)

fileAsList = re.split('\n', fileToRead)

mainIncludes = getIncludeFileNames(generateSourceList(generateFileName(sourceDirectory, entryPoint)))

masterDictionary = {}

masterDictionary[entryPoint] = mainIncludes
print(masterDictionary)
for el in masterDictionary['main.c']:
    masterDictionary[el] = getIncludeFileNames(generateSourceList(generateFileName(sourceDirectory, el)))
    #print(getIncludeFileNames(generateSourceList(generateFileName(sourceDirectory, el))))
        
for el in masterDictionary:
    print(el + ' includes:\n')
    print(masterDictionary[el], '\n')


allIncludes = recursiveIncludes(sourceDirectory, entryPoint)

# for el in allIncludes:
#     print(el + ' includes:\n')
#     print(allIncludes[el], '\n')

#printDict(allIncludes)

print('Testing flat includes: \n')
flatIncludes = {}
flattenDict(allIncludes, flatIncludes)
printDict(flatIncludes)



print('\nTesting width first approach\n')
#tExcludedNames = ['sam','.vs', 'build']
tExcludedNames = ['msvc', 'ros', 'lib', 'arduino', 'asio', 'build', 'experimental']
widthFirstDictionary = buildIncludes(sourceDirectory, tExcludedNames)

printDict(widthFirstDictionary)

    
    
#### Visualisation
###widthfirst


# dot = graphviz.Digraph(comment = 'Testdiagram')
# nodes = []
# uniquedirs = []
# for key in widthFirstDictionary.keys():
#     nodes.append(os.path.basename(key))
#     dot.node(os.path.basename(key), os.path.basename(key), shape = 'box')
    
#     #add directories to construct subgraphs and clusters later
#     if(os.path.dirname(key) not in uniquedirs):
#         uniquedirs.append(os.path.dirname(key))    
    
    
    
    
# for key in widthFirstDictionary.keys():
#     keybasename = os.path.basename(key)
    
#     for val in widthFirstDictionary[key]:
#         if (val != 'No includes found'):
#             dot.edge(val, keybasename)
    
    
# dot.unflatten(stagger = 3)
    

# dot.render('testgraph', view=True)

# #depthfirst
# depthdot = graphviz.Digraph(comment = 'TestDepth')
# depthnodes = []
# for key in flatIncludes.keys():
#     depthnodes.append(depthdot.node(key, key, shape='box'))
    
    
# for key in flatIncludes.keys():
#     for val in flatIncludes[key]:                
#         if(val != 'No includes found'):
#             #print(key, ':', val)
#             depthdot.edge(val, key)
        
#depthdot.render('depthtest', view = True)