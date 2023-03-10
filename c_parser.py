from typing import NamedTuple
import re
import os
from global_utilities import *



#This will be the master in the improved parser,
#finding calls, assignments, defs, etc by moving
#through the project token by token. Should be a
#lot faster than my previous method as well
def parseProject(tokensPerFile):

#Keep track of scopes:
#Scopes are uniquely identified by a list of numbers.
#Zeroeth index is the outermost scope; a file.
#The value of the number is the scope's number inside that level
#Ex: [1,2,3] could be the 3rd function of the 
# 2nd class of the 1st file in a project
    currentScopeID = [0]*7
    scopeStack = []

    for file in tokensPerFile:
        currentScopeID[0] += 1
        tokensInThisFile = tokensPerFile[file]
        for token in tokensInThisFile:
            if token.type == "BRACEOPEN":
                scopeStack.append(token.value)
                currentScopeID[len(scopeStack)] += 1                
                print(file, currentScopeID, token.line)
            elif token.type == 'BRACECLOSE':                        
                for i in range(len(scopeStack)+1, len(currentScopeID)):
                    currentScopeID[i] = 0
                scopeStack.pop() 
        for i in range(len(scopeStack)+1, len(currentScopeID)):
            currentScopeID[i] = 0


####For isolated testing####
from main import tokensPerFile

parseProject(tokensPerFile)
