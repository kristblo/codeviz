
from ply_classes import Scope
from copy import deepcopy

#Compatible with tokenizer
def calculateScope(LexToken, scopeStack, scopes):
    if LexToken.value == "{":
        scopeStack.append(LexToken.lineno)
    elif LexToken.value == "}":
        deepStack = deepcopy(scopeStack)
        scope = Scope(deepStack, scopeStack[-1], LexToken.lineno)
        scopes.append(scope)
        scopeStack.pop()

def addScope(LexToken, scopeStack, currentScopeID):
    scopeStack.append(LexToken.lineno)
    try:
        currentScopeID[len(scopeStack)] += 1
    except IndexError:
        currentScopeID.append(1)

def popScope(scopeStack, currentScopeID):
    for i in range(len(scopeStack+1), len(currentScopeID)):
        currentScopeID[i] = 0
    
    scopeStack.pop()
    


#Compatible with p_scope