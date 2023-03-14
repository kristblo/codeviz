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
            candidates.append((index, scopedT))
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
            if currentToken.Tok.type == 'PAROPEN':
                parenthesesCt += 1
            if currentToken.Tok.type == 'PARCLOSE':
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

def parseDefinitions_scoped(candidateDefList, scopedTokenList):
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
        
        callees = findCallees_scoped(candidateDefList, scopedTokenList)        
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
    scopedTIdx = candidateDef[0][0]
    bodyStart = 0
    bodyEnd = 0
    braceCt = 0
        
    for i in range(scopedTIdx, len(scopedTokenList)):
        if scopedTokenList[i].Tok.type == 'BRACEOPEN':
            bodyStart = i
            scopedTIdx = i + 1
            braceCt = 1
            break

    while braceCt > 0:
        if scopedTokenList[scopedTIdx].Tok.type == 'BRACEOPEN':
            braceCt += 1
        if scopedTokenList[scopedTIdx].Tok.type == 'BRACECLOSE':
            braceCt -= 1
        scopedTIdx += 1
        bodyEnd = scopedTIdx
    
    bodyScopedTokens = scopedTokenList[bodyStart:bodyEnd]
    candidates = findCandidateFuncs_scoped(bodyScopedTokens)
    calleeCands = sortCandidateFuncs_scoped(candidates, bodyScopedTokens)[2]
    callees = parseCalls_scoped(calleeCands, bodyScopedTokens)

    return callees

def parseCalls_scoped(candidateCallList, scopedTokenList):
    calls = []
    for candidate in candidateCallList:
        index = candidate[0]
        args = parseArguments_scoped(index, scopedTokenList)
        
        scope = [candidate[1].ScopeID] \
                + [candidate[1].Filepath] \
                + [candidate[1].Tok.line]
        calls.append(FunctionCall(candidate[1].Tok.value, args, scope))
        
    return calls

def getProjectFunctionData_scoped(scopedTokenList):

    candidates = findCandidateFuncs_scoped(scopedTokenList)
    sortedCandidates = sortCandidateFuncs_scoped(candidates, scopedTokenList)

    defCandidates = sortedCandidates[1]    
    definitions = parseDefinitions_scoped(defCandidates, scopedTokenList)

    callCandidates = sortedCandidates[2]
    calls = parseCalls_scoped(callCandidates, scopedTokenList)
    
    globalDefNames = [definition.name for definition in definitions]

    undefinedCallees = []
    for definition in definitions:        
        calleeNames = [callee.name for callee in definition.callees]
        for calleeName in calleeNames:
            if (calleeName not in globalDefNames) and \
                (calleeName not in undefinedCallees):
                undefinedCallees.append(calleeName)
    
    fcMx = []
    for i, thisDefinition in enumerate(definitions):
        thisDefsRow = [0]*len(definitions) + [0]*len(undefinedCallees)
        callees = thisDefinition.callees

        calleeNames = [callee.name for callee in callees]
        for thisCalleeName in calleeNames:
            for j, defName in enumerate(globalDefNames):
                if thisCalleeName == defName:
                    thisDefsRow[j] == 1
            for j, undefined in enumerate(undefinedCallees):
                rowIdx = len(globalDefNames)
                if thisCalleeName == undefined:
                    thisDefsRow[rowIdx] = 1
        fcMx.append(thisDefsRow)

    return definitions, calls, definitions, undefinedCallees, fcMx
                    

        




