from typing import NamedTuple
import re
import os
from global_utilities import *
import copy
# from c_tokenizer import Token


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class ScopedToken(NamedTuple):
    Tok: Token
    ScopeID: list
    Filepath: str

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

    scopedTokens = []

    for file in tokensPerFile:
        currentScopeID[0] += 1
        tokensInThisFile = tokensPerFile[file]
        

        for idx, token in enumerate(tokensInThisFile):
            if token.type == "BRACEOPEN":
                scopeStack.append(token.value)
                currentScopeID[len(scopeStack)] += 1                 
            elif token.type == 'BRACECLOSE':                               
                for i in range(len(scopeStack)+1, len(currentScopeID)):
                    currentScopeID[i] = 0
                scopeStack.pop()                      
            deepID = copy.deepcopy(currentScopeID) #Dunno wtf, but necessary
            Scoped = ScopedToken(token, deepID, file)            
            #yield(Scoped)            
            scopedTokens.append(Scoped)

        for i in range(1, len(currentScopeID)):
            currentScopeID[i] = 0

    return scopedTokens


####For isolated testing####
#from main import tokensPerFile

#parseRes = parseProject(tokensPerFile)
# for i in parseRes:
#     print(i)