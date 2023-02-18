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

tokens = []
for token in tokenize(currentFile):
    tokens.append(token)
    appendStringToFile('tokenizeroutput.txt', str(token) + '\n')

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


class Function(NamedTuple):
    ftype: str #dec/def/call
    name: str
    args: list #of tuples? (argtype, argname)
    rettype: str
    signature: list #rettype + argtypev

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
    parenthesisCt = 1
    args = []
    currentarg = []
    while parenthesisCt > 0:
        if tokenList[tokenIndex].type == 'PAROPEN':
            parenthesisCt += 1
        if tokenList[tokenIndex].type == 'PARCLOSE':
            parenthesisCt -= 1
        if tokenList[tokenIndex].type == 'LISTSEP' or parenthesisCt == 0:
            args.append(currentarg)
            currentarg = []
        if tokenList[tokenIndex].type != 'LISTSEP':
            currentarg.append(tokenList[tokenIndex].value)        
        tokenIndex += 1

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

        
        definitions.append(Function('def', candidate[1].value, args, rettype, signature))

    return definitions

def parseCalls(candidateCallList, tokenList):
    calls = []
    rettype = 'call'
    for candidate in candidateCallList:
        index = candidate[0]
        args = parseArguments(index, tokenList)

        #Make signature
        # signature = [rettype, candidate[1].value]
        # for i in range(0, len(args)):
        #     sigPart = ''
        #     #for j in range(0, len(args[i])):
        #     sigPart += str(args[i])
        #     signature.append(sigPart)
        #     sigPart = ''
        calls.append(Function('call', candidate[1].value, args, rettype, 'call'))
    return calls

        



        

candidates = findCandidateFuncs(tokens)
sortedCandidates = sortCandidateFuncs(candidates, tokens)

decCandidates = sortedCandidates[0]
defCandidates = sortedCandidates[1]
callCandidates = sortedCandidates[2]



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