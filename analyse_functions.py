import re
import os
from global_utilities import *
from c_tokenizer import *

#Identify and treat function decs, defs and calls

language_keywords_file = getFileAsString('c_grammar/c_keywords.txt')
language_keywords = re.split('\n', language_keywords_file)
currentFile = getFileAsString('/home/kristian/byggern-nicer_code/node2/main.c')

language_fc_kw_file = getFileAsString('c_grammar/c_function_kw.txt')
language_fc_kw = re.split('\n', language_fc_kw_file)

# tokens = []
# for token in tokenize(currentFile):
#     tokens.append(token)
#     appendStringToFile('tokenizeroutput.txt', str(token) + '\n')

#Find a way to use the tokens to identify functions
#Use valid token sequences based on the functions.txt files
#1. Look for identifiers followed by PAROPEN in the token list
#2. Start counting parentheses to keep track of arglist
#3. Use token after arglist closing parenthesis to determine type
#3.1 token BRACEOPEN means it is a definition
#3.2 token END means it is either a declaration or a call
#3.2.1 A declaration must be followed by END
#3.2.2 A call need not be followed by a call
#   => Neither END nor BRACEOPEN means it's definitely a call
#4. Ignore ARITOP (pointer *) in decs/defs
#5. Identifier immediately preceding the function name is return type


class FunctionDef(NamedTuple):
    name: str
    args: list #of tuples? (argtype, argname)
    rettype: str
    signature: list #rettype + argtypev
    callees: list

class FunctionCall(NamedTuple):
    name: str
    args: list



#Find all possible function uses
def findCandidateFuncs(tokenList):
    candidates = [] #(token index, token)
    for index, token in enumerate(tokenList):
        if token.type == 'ID' and token.value not in language_keywords and tokenList[index+1].type == 'PAROPEN':
            candidates.append((index, token))
    return candidates

#Sort them into probable declarations, definitions and calls
def sortCandidateFuncs(candList, tokenList):
    decs = []
    defs = []
    calls = []

    for candidate in candList:
        index = candidate[0]

        parenthesesCt = 1
        isCall = 0
        if tokenList[index-1].type != 'ID':
            #is most probably a call
            isCall = 1

        currentTokenIdx = index + 2
        while parenthesesCt > 0:
            currentToken = tokenList[currentTokenIdx]
            if currentToken.type == 'PAROPEN':
                parenthesesCt += 1
            if currentToken.type == 'PARCLOSE':
                parenthesesCt -= 1

            currentTokenIdx += 1

        if tokenList[currentTokenIdx].type == 'BRACEOPEN':
            defs.append(candidate)
        elif tokenList[currentTokenIdx].type == 'END' and isCall == 0:
            decs.append(candidate)
        elif isCall == 1:
            calls.append(candidate)


    return decs, defs, calls


#Compile lists of unique functions and calls in the file using Function class

#Extracts the list of arguments for decs/defs/calls
def parseArguments(index, tokenList):
    tokenIndex = index + 2
    argStartIndex = tokenIndex
    parenthesisCt = 1
    while parenthesisCt > 0:
        if tokenList[tokenIndex].type == 'PAROPEN':
            parenthesisCt += 1
        if tokenList[tokenIndex].type == 'PARCLOSE':
            parenthesisCt -= 1
        tokenIndex += 1
    argEndIndex = tokenIndex - 1
    
    unfilteredArgs = [token.value for token in tokenList[argStartIndex:argEndIndex]]
    argTokenList = tokenList[argStartIndex:argEndIndex]
    args = []
    currentArg = []
    internalParCt = 0
    for token in argTokenList:
        if token.type == 'PAROPEN':
            internalParCt += 1            
        if token.type == 'PARCLOSE':
            internalParCt -= 1            
    
        if token.type == 'LISTSEP' and internalParCt == 0:
            args.append(currentArg)
            currentArg = []
        if token.type == 'LISTSEP' and internalParCt != 0:
            continue
        if token.type != 'LISTSEP':
            currentArg.append(token.value)
    args.append(currentArg)


    return args


#Declarations are not really interesting/can be parsed with this
def parseDefinitions(candidateDefList, tokenList):
    definitions = []
    for candidate in candidateDefList:
        index = candidate[0]
        args = parseArguments(index, tokenList)

        #Refine arguments?
        #Nah

        #Determine return type
        rettype = ''
        if tokenList[index-1].value == '*':
            rettype = tokenList[index-2].value+'_p'
        else:
            rettype = tokenList[index-1].value

        #Make signature
        signature = [rettype, candidate[1].value]
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

        #Find possible callees
        callees = findCallees(candidate, tokenList)
        definitions.append(FunctionDef(candidate[1].value, args, rettype, signature, callees))
    return definitions

#Look for calls to functions inside a function def body
#after finding all calls in a project
def findCallees(candidateDef, tokenList):
    #1. For each def in candidates, use the token index to start looking
    #2. Determine scope of function body by counting braces, store token indeces
    #3. Look for calls within that range
    #4. (Do second pass to) decide if the call is among user-declared functions
    tokenIndex = candidateDef[0]
    bodyStart = 0
    bodyEnd = 0
    braceCt  =0
    for i in range(tokenIndex, len(tokenList)):
        if tokenList[i].type == 'BRACEOPEN':
            bodyStart = i
            tokenIndex = i+1
            braceCt = 1
            break
    while braceCt > 0:        
        if tokenList[tokenIndex].type == 'BRACEOPEN':
            braceCt += 1
        if tokenList[tokenIndex].type == 'BRACECLOSE':
            braceCt -= 1
        tokenIndex += 1
        bodyEnd = tokenIndex

    bodyTokens = tokenList[bodyStart:bodyEnd]
    candidates = findCandidateFuncs(bodyTokens)
    calleeCands = sortCandidateFuncs(candidates, bodyTokens)[2]
    callees = []
    callees.append(parseCalls(calleeCands, bodyTokens))

    return callees[0]





def parseCalls(candidateCallList, tokenList):
    rettype = 'call'
    calls = []
    for candidate in candidateCallList:
        index = candidate[0]
        args = parseArguments(index, tokenList)

        #Make signature
        # signature = [rettype, candidate[1].value]
        # for i in range(0, len(args)):
        #     sigPart = ''
        #     if len(args[i]) > 0:
        #         for j in range(0, len(args[i])):
        #             sigPart += str(args[i][j])
        #     else:
        #         sigPart = 'void'
        #     signature.append(sigPart)
        #Not much point, the info is better preserve in the arglist
        calls.append(FunctionCall(candidate[1].value, args))                
    return calls



#Return decs+defs, calls and cross-call matrix
def getProjectFunctionData(configfile, tokenizedFiles):
    #tokenDirectory = getTokenDir(configfile)
    functionDefinitionsPerFile = []
    functionCalls = []
    undefinedCallees = []

    for file in tokenizedFiles:
        tokens = tokenizedFiles[file]
        candidates = findCandidateFuncs(tokens)
        sortedCandidates = sortCandidateFuncs(candidates, tokens)

        defCandidates = sortedCandidates[1]
        definitions = parseDefinitions(defCandidates, tokens)
        functionDefinitionsPerFile.append((file, definitions))

        callCandidates = sortedCandidates[2]
        calls = parseCalls(callCandidates, tokens)
        #functionCalls.append((file, calls))
        for item in calls:
            functionCalls.append((file, item))
    
    globalDefinitions = []
    for i in range(0, len(functionDefinitionsPerFile)):
        defsInCurrent = functionDefinitionsPerFile[i][1]
        globalDefinitions += defsInCurrent        
    globalDefNames = [definition.name for definition in globalDefinitions]

    #Make the list of undefined callees
    for definition in globalDefinitions:
        calleeNames = [callee.name for callee in definition.callees]
        for calleeName in calleeNames:
            if (calleeName not in globalDefNames) and \
                (calleeName not in undefinedCallees):
                undefinedCallees.append(calleeName)    

    fcMx = []
    #Check each definitions among the global ones
    for i, thisDefinition in enumerate(globalDefinitions):
        thisDefsRow = [0]*len(globalDefinitions) + [0]*len(undefinedCallees)
        callees = thisDefinition.callees
        
        #Get the list of callees from the relevant defintion
        calleeNames = [callee.name for callee in callees]
        for thisCalleeName in calleeNames:
            #For each callee, look through the list of global defs
            #If the callee is the same as the global, set the corresponding
            #index in the function matrix to one
            #TODO: Optimize
            for j, globalName in enumerate(globalDefNames):            
                if thisCalleeName == globalName:
                    thisDefsRow[j] = 1
            for j, undefined in enumerate(undefinedCallees):
                rowIdx = len(globalDefNames) + j
                if thisCalleeName == undefined:
                    thisDefsRow[rowIdx] = 1

        fcMx.append(thisDefsRow)

    return functionDefinitionsPerFile, functionCalls, globalDefinitions, undefinedCallees, fcMx





# candidates = findCandidateFuncs(tokens)
# sortedCandidates = sortCandidateFuncs(candidates, tokens)

# decCandidates = sortedCandidates[0]
# defCandidates = sortedCandidates[1]
# callCandidates = sortedCandidates[2]



# print('Decs:')
# for item in decCandidates:
#     print(item)

# print('Defs:')
# for item in defCandidates:
#     print(item)

# print('Calls:')
# for item in callCandidates:
#     print(item)

# defintions = parseDefinitions(defCandidates, tokens)
# for item in defintions:
#     print(item)

# calls = parseCalls(callCandidates, tokens)
# for item in calls:
#     print(item)