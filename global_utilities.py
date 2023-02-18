import re
import os

#Opens an existing file and returns it as a string
def getFileAsString(filename):
    try:
        file = open(filename, 'r')
        out = file.read()
        return out

    except Exception as e:
        print('File: ' + filename + ' could not be read')
        print(e)
        return 'ERROR'


#Appends a string to a file, starting with a newline
def appendStringToFile(filename, string):
    with open(filename, 'a') as outfile:
    # file = open(filename, 'w')
    # file.write(string)
    # file.close()
        outfile.write(string)

#Gets an arbitrary line from the config file
def getKeywordFromConfigFile(configfile, keyword):
    file = getFileAsString(configfile)
    fileAsArray = re.split('\n', file)

    for line in fileAsArray:
        if(re.search(keyword, line)):
            pattern=re.split(':', line)[1]
            return pattern
    raise Exception("keyword ", keyword, " could not be found")

#Scans the config file for the project's top directory
def getTopDirectory(configfile):
    topDirName = getKeywordFromConfigFile(configfile, 'topDirectory')
    return topDirName

#Scans the config file for the project's irrelevant directories
def getExludedDirs(configfile):
    excldirstring = getKeywordFromConfigFile(configfile, 'excludedDirectories')
    strip1 = excldirstring.strip('[]')
    split = strip1.split(',')
    excldirs = []
    for name in split:
        strip2 = name.strip(' ')
        strip3 = strip2.strip('\'')
        excldirs.append(strip3)

    return excldirs

#Scans the config file for the project's desired tokenizer output directory
def getTokenDir(configfile):
    tokendirstring = getKeywordFromConfigFile(configfile, 'tokenDirectory')
    return tokendirstring

#Checks a file ending against permitted source file types
def isSourceFile(filename, configfile):
    pattern = re.compile(getKeywordFromConfigFile(configfile, 'sourcepattern'))    
    if(pattern.search(filename)):
        return True
    else:
        return False

#Finds all sourcefiles under topDir
def findAllSourceFilePaths(topDir, excludedDirs, configfile):
    sourcefiles = []
    directories = getRelevantSubdirs(topDir, excludedDirs)
    for dir in directories:
        for item in os.scandir(dir):
            if(isSourceFile(item.name, configfile)):
                sourcefiles.append(dir+item.name)
    return sourcefiles

#Determines whether a path contains an excluded directory
def hasExcludedPath(path, excludedDirs):
    forbidden = False 
    for dir in excludedDirs:
        pattern = re.compile(dir)
        if(pattern.search(path)):
            forbidden = True
    return forbidden

#Finds all relevant functions recursively
def findAllRelevantSubDirs(topDir, relevantSubDirs, excludedDirs):
    for name in os.scandir(topDir):
        if(name.is_dir()):
            if(name not in relevantSubDirs and (hasExcludedPath(str(name), excludedDirs) == False)):
                relevantSubDirs.append(name.path)
                findAllRelevantSubDirs(topDir+name.name+'/', relevantSubDirs, excludedDirs)

#Wraps recursive finder-function in a non-recursive function
def getRelevantSubdirs(topDir, excludedDirs):
    relevant = [topDir]
    findAllRelevantSubDirs(topDir, relevant, excludedDirs)

    #enumeration ensures actual relevant-object is being altered
    for idx, item in enumerate(relevant):
        if relevant[idx][-1] != '/':
            relevant[idx] = relevant[idx]+'/'
    return relevant

#Calculate the number of folders between two files, aka distance
def calculateDistance(file1, file2):
    path1 = os.path.dirname(file1)
    path2 = os.path.dirname(file2)
    common = os.path.commonpath([path1, path2])    
    commondirs = common.split('/') #\\ for Win10
    dirs1 = path1.split('/')
    dirs2 = path2.split('/')
    
    distFromCommon1 = abs(len(dirs1)-len(commondirs))
    distFromCommon2 = abs(len(dirs2)-len(commondirs))
    
    distance = distFromCommon1 + distFromCommon2
    
    
    return distance