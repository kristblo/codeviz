import re
import os
from global_utilities import *
from c_tokenizer import *
from analyse_functions import FunctionDef
from analyse_functions import FunctionCall


#Refactor of analyse_functions for use with scopedTokens


language_keywords_file = getFileAsString('c_grammar/c_keywords.txt')
language_keywords = re.split('\n', language_keywords_file)
currentFile = getFileAsString('/home/kristian/byggern-nicer_code/node2/main.c')

language_fc_kw_file = getFileAsString('c_grammar/c_function_kw.txt')
language_fc_kw = re.split('\n', language_fc_kw_file)

def findCandidateFuncs_scoped(scopedTokenList):
    candidates = []
    for index, scopedT in enumerate(scopedTokenList):
        if scopedT.Tok.type == 'ID' \
            and scopedT.Tok.value not in language_keywords\
            and scopedTokenList[index+1].Tok.type == 'PAROPEN':
            candidates.append(index, scopedT)
    return candidates

def sortCandidateFuncs_scoped(candList, scopedTokenList):
    decs = []
    defs = []
    calls = []

    for candidate in candList:
        index = candidate[0]

        parenthesesCt = 1
        isCall = 0
        if scopedTokenList[index-1].Tok.type != 'ID':
            isCall = 1
        
        currentScopedTIdx = index + 2
        while parenthesesCt > 0:
            currentToken = scopedTokenList[currentScopedTIdx]
            if currentScopedTIdx.Tok.type == 'PAROPEN':
                parenthesesCt += 1
            if currentScopedTIdx.Tok.type == 'PARCLOSE':
                parenthesesCt -= 1
            currentScopedTIdx += 1

        if scopedTokenList[currentScopedTIdx].Tok.type == 'BRACEOPEN':
            defs.append(candidate)
        elif scopedTokenList[currentScopedTIdx].Tok.type == 'END' and isCall == 0:
            decs.append(candidate)
        elif isCall == 1:
            calls.append(candidate)
    
    return decs, defs, calls

def parseArguments_scoped(index, scopedTokenList):
    scopedTokenIndex = index + 2
    argStartIndex = scopedTokenIndex
    parenthesisCt = 1
    while parenthesisCt > 0:
        if scopedTokenList[scopedTokenIndex].Tok.type == 'PAROPEN':
            parenthesisCt += 1
        if scopedTokenList[scopedTokenIndex].Tok.type == 'PARCLOSE':
            parenthesisCt -= 1
        scopedTokenIndex += 1
    argEndIndex = scopedTokenIndex - 1

    argScopedTokenList = scopedTokenList[argStartIndex:argEndIndex]
    args = []
    currentArg = []
    internalParCt = 0
    for scopedT in argScopedTokenList:
        if scopedT.Tok.type == 'PAROPEN':
            internalParCt += 1            
        if scopedT.Tok.type == 'PARCLOSE':
            internalParCt -= 1            

        if scopedT.Tok.type == 'LISTSEP' and internalParCt == 0:
            args.append(currentArg)
            currentArg = []
        if scopedT.Tok.type == 'LISTSEP' and internalParCt != 0:
            continue
        if scopedT.Tok.type != 'LISTSEP':
            currentArg.append(scopedT.Tok.value)

    return args

def parseDefinitions(candidateDefList, scopedTokenList):
    definitions = []
    for candidate in candidateDefList:
        index = candidate[0]
        args = parseArguments_scoped(index, scopedTokenList)

        rettype = ''
        if scopedTokenList[index-1].Tok.value == '*':
            rettype = scopedTokenList[index-2].Tok.value + '_p'
        else:
            rettype = scopedTokenList[index-1].Tok.value

        signature = [rettype, candidate[1].Tok.value]
        for i in range(0, len(args)):
            sigPart = ''
            if len(args[i]) > 0:
                for j in range(0, len(args[i])-1):
                    sigPart += args[i][j]
            if sigPart == '':
                if args[i] == ['...']:
                    sigPart = '...'
                else:
                    sigPart = 'void'
            signature.append(sigPart)
            sigPart = ''
        
        callees = findCallees_scoped()
        scope = [scopedTokenList[candidate[0]].ScopeID] \
                + [scopedTokenList[candidate[0]].Filepath]\
                + [scopedTokenList[candidate[0]].Tok.line]
        definitions.append(FunctionDef(candidate[1].Tok.value,
                                       args,
                                       rettype,
                                       signature,
                                       callees,
                                       scope))
        return definitions
    


def findCallees_scoped(candidateDef, scopedTokenList):
    scopedTIdx = candidateDef[0]
    defintionScope = scopedTokenList[scopedTIdx].ScopeID


    return 0


