import re
import os
from global_utilities import *
from c_tokenizer import *
from analyse_functions import FunctionDef
from analyse_functions import FunctionCall
from analyse_assignments import Constant
from data_flow_v2 import Scope


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

def argPatterns():
    agPts = {
    "typecast_p":   ['PAROPEN', 'ID', 'ARITOP', 'PARCLOSE', 'ID'],
    "typecast_id":  ['PAROPEN', 'ID', 'PARCLOSE', 'ID'] ,
    "typecast_num": ['PAROPEN', 'ID', 'PARCLOSE', 'NUMBER'],
    "member":       ['ID', 'MEMBER', 'ID'],
    "nondec_num":   ['PREFIX', 'NUMBER'],
    "nondec_const": ['PREFIX', 'ID'],
    "address":      ['BITWOP', 'ID'],
    "pointer":      ['ARITOP', 'ID'],
    "fc_call":      ['ID', 'PAROPEN'],
    "const":        ['NUMBER'],
    "id":           ['ID'],
    "string":       ['STRING'],
    "char":         ['CHAR'],
    #For function defs:
    #TODO: Add patterns for fdefs
        
    }
    return agPts

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
    argsTokens = []
    currentArg = []



    internalParCt = 0
    for scopedT in argScopedTokenList:
        if scopedT.Tok.type == 'PAROPEN':
            internalParCt += 1            
        if scopedT.Tok.type == 'PARCLOSE':
            internalParCt -= 1            

        if scopedT.Tok.type == 'LISTSEP' and internalParCt == 0:
            argsTokens.append(currentArg)
            currentArg = []
        if scopedT.Tok.type == 'LISTSEP' and internalParCt != 0:
            continue
        if scopedT.Tok.type != 'LISTSEP':
            currentArg.append(scopedT)
    argsTokens.append(currentArg)

    #Turn args into Constant or FcCall objects
    argConstObjects = []
    for argScopedTList in argsTokens:        
        constCreationSuccessful = 0

        #Look for pattern match
        for patternname in argPatterns():     
            pattern = argPatterns()[patternname]
            try:
                scopedTokenListSlice = [scopedT for scopedT in argScopedTList[0:len(pattern)]]
            except:
                #print("Could not create scopedTokenListSlice")
                continue
            tokenTypeSlice = [scopedT.Tok.type for scopedT in scopedTokenListSlice]
            if tokenTypeSlice == pattern:
                if patternname == 'typecast_p':
                    name = scopedTokenListSlice[4].Tok.value
                    dtype = scopedTokenListSlice[1].Tok.value + '_p'
                    value = 'ARG'
                    scope = Scope(scopedTokenListSlice[4].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)
                    constCreationSuccessful = 1
                    break

                if patternname == 'typecast_id':
                    name = scopedTokenListSlice[3].Tok.value
                    dtype = scopedTokenListSlice[1].Tok.value
                    value = 'ARG'
                    scope = Scope(scopedTokenListSlice[3].ScopeID,
                                    scopedTokenListSlice[3].Filepath,
                                    scopedTokenListSlice[3].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)
                    constCreationSuccessful = 1
                    break

                if patternname == 'typecast_num':
                    name = 'NUMERIC_CONST'
                    dtype = scopedTokenListSlice[1].Tok.value
                    value = scopedTokenListSlice[3].Tok.value
                    scope = Scope(scopedTokenListSlice[3].ScopeID,
                                    scopedTokenListSlice[3].Filepath,
                                    scopedTokenListSlice[3].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)
                    constCreationSuccessful = 1
                    break 
                
                if patternname == 'nondec_const' or patternname == 'nondec_num':
                    name = 'NUMERIC_CONST'
                    dtype = scopedTokenListSlice[0].Tok.value
                    value = scopedTokenListSlice[1].Tok.value
                    scope = Scope(scopedTokenListSlice[1].ScopeID,
                                    scopedTokenListSlice[1].Filepath,
                                    scopedTokenListSlice[1].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    constCreationSuccessful = 1
                    break

                if patternname == 'address':
                    name = scopedTokenListSlice[1].Tok.value
                    dtype = 'ADDRESS'
                    value = scopedTokenListSlice[1].Tok.value #TODO: Try to find the actual value?
                    scope = Scope(scopedTokenListSlice[1].ScopeID,
                                    scopedTokenListSlice[1].Filepath,
                                    scopedTokenListSlice[1].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    constCreationSuccessful = 1
                    break

                if patternname == 'pointer':
                    name = scopedTokenListSlice[1].Tok.value
                    dtype = 'POINTER'
                    value = scopedTokenListSlice[1].Tok.value #TODO: Try to find the actual value?
                    scope = Scope(scopedTokenListSlice[1].ScopeID,
                                    scopedTokenListSlice[1].Filepath,
                                    scopedTokenListSlice[1].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)  
                    constCreationSuccessful = 1
                    break

                if patternname == 'const':
                    name = 'NUMERIC_CONST'
                    dtype = 'DEFAULT'
                    value = scopedTokenListSlice[0].Tok.value
                    scope = Scope(scopedTokenListSlice[0].ScopeID,
                                    scopedTokenListSlice[0].Filepath,
                                    scopedTokenListSlice[0].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)        
                    constCreationSuccessful = 1
                    break

                if patternname == 'id':
                    name = scopedTokenListSlice[0].Tok.value
                    dtype = 'DATATYPE' #TODO:Find the actual type from the decl
                    value = scopedTokenListSlice[0].Tok.value
                    scope = Scope(scopedTokenListSlice[0].ScopeID,
                                    scopedTokenListSlice[0].Filepath,
                                    scopedTokenListSlice[0].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)           
                    constCreationSuccessful = 1
                    break

                if patternname == 'fc_call': #TODO: Fix call as arg
                    # candidate = [(0, scopedTokenListSlice[0])]
                    # print("Parsing call as arg with cand.: ", candidate)
                    # argConstObjects.append(parseCalls_scoped(candidate, scopedTokenListSlice))
                    # print("parsed fc call as arg")
                    # constCreationSuccessful = 1
                    break

                if patternname == 'string' or patternname == 'char':                                            
                    name = 'STRING'
                    dtype = 'DATATYPE' #TODO:Find the actual type from the decl
                    value = scopedTokenListSlice[0].Tok.value
                    scope = Scope(scopedTokenListSlice[0].ScopeID,
                                    scopedTokenListSlice[0].Filepath,
                                    scopedTokenListSlice[0].Tok.line)
                    argConst = Constant(name, dtype, value, scope)
                    argConstObjects.append(argConst)       
                    constCreationSuccessful = 1
                    break
        
        
        if constCreationSuccessful == 0:
            #argstr = ''.join([str(argST.Tok.value) for argST in argScopedTList])
            #print("Could not create const from tokens: ", argstr)
            #argConstObjects.append(argstr)    
            argConstObjects.append(argScopedTList)


    #return argsTokens
    return argConstObjects

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
                    try:
                        sigPart += args[i][j].Tok.value
                    except:
                        sigPart += args[i][j] #Probably a string
            if sigPart == '':
                if args[i] == ['...']:
                    sigPart = '...'
                else:
                    sigPart = 'void'
            signature.append(sigPart)
            sigPart = ''
        
        callees = findCallees_scoped(candidate, scopedTokenList)        
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
    bodyStart = 0
    bodyEnd = 0
    braceCt = 0
        
    for i in range(scopedTIdx, len(scopedTokenList)):
        if scopedTokenList[i].Tok.type == 'BRACEOPEN':
            bodyStart = i
            scopedTIdx = i + 1
            braceCt = 1            
            break

    while True:
        if scopedTokenList[scopedTIdx].Tok.type == 'BRACEOPEN':
            braceCt += 1
        if scopedTokenList[scopedTIdx].Tok.type == 'BRACECLOSE':
            braceCt -= 1
        if braceCt == 0:
            bodyEnd = scopedTIdx
            break
        scopedTIdx += 1
    
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
                    

        




