from typing import NamedTuple
from global_utilities import *
from c_tokenizer import *
from analyse_assignments import *
from analyse_functions import *

#For use with GraphTool
class Scope(NamedTuple):
    ScopeID:    list
    filepath:   str
    lineno:     int

class DataNode(NamedTuple):
    name:     str   #The name of the node, as presented graphically
    inputs:   list  #Unique identifiers of other DataNode instances
    scope:    Scope #For clustering
    color:    str   #For color scheming
    uniqueID: str   #For use with inputs

class AssignmentNode(NamedTuple):
    name:       str
    input:      list
    scope:      Scope    

#"Virtual" node not to be visualised directly, informs edgecreation
class DefNode(NamedTuple):
    name:       str
    args:       list #of tuples, for type check
    rettype:    str  #for type check in call
    signature:  list #for overload check, uniqueID
    callees:    list #of CallNodes
    scope:      Scope #TODO:Consider removing, not needed for viz


class CallNode(NamedTuple):
    name:       str
    arguments:  list #of tokens
    definition: DefNode
    scope:      Scope

def dataNode_from_assignmentNode(assignmentNode):
    name = assignmentNode.name
    #inputs = [assignmentNode.input] #TODO: Make unique?

    inputstr = ''
    inputstr += ''.join([str(num) for num in assignmentNode.scope.ScopeID])
    inputstr += assignmentNode.input
    inputstr += str(assignmentNode.scope.lineno)
    inputs = [inputstr]

    scope = assignmentNode.scope
    color = 'orange' #TODO: Find out if graph-tool takes color words
    #uniqueID = ''.join([field for field in scope])+name
    uniqueID = generateUniqueID(assignmentNode)
    
    node = DataNode(name, inputs, scope, color, uniqueID)
    return node

def dataNode_from_defNode(definitionNode):
    name = definitionNode.name
    inputs = []
    for callee in definitionNode.callees:
        try:
            calleeID = ''
            calleeID += ''.join([str(num) for num in callee.scope[0]])
            calleeID += callee.name
            calleeID += str(callee.scope[2])
            inputs.append(calleeID)            
        except:
            print("Could not generate calleID for %s at %s, %s" %(name, callee.scope, callee.scope))

    # for argtokens in definitionNode.args:
    #     inputs.append(argtokens[-1]) #TODO: Create a symbol list
    for arg in definitionNode.args:
        inputs.append(arg)

    uniqueID = generateUniqueID(definitionNode)
    scope = definitionNode.scope
    color = 'maroon'

    node = DataNode(name, inputs, scope, color, uniqueID)
    return node    

#Effectively becomes a mix of call and its def
def dataNode_from_callNode(callNode):
    name = callNode.name
    inputs = [] #Predictably calculable uniqueIDs for args and callees
    
    if callNode.definition != '':
        for callee in callNode.definition.callees:
            #print("callee: ", callee.scope)            
            try:
                calleeID = ''
                calleeID += ''.join([str(num) for num in callee.scope[0]])
                calleeID += callee.name
                calleeID += str(callee.scope[2])
                inputs.append(calleeID)                            
            except:
                print("Warning: Could not generate calleeID for %s at %s, %s" %(name, callNode.scope.filepath, callNode.scope.lineno))
                pass
    
    for arg in callNode.arguments:
        #Assuming a function won't take an argument from outside
        # its own file, and that arg.value is unique        
        #inputs.append(argID) #TODO:Fix uniqueID        
        #inputs.append(arg)
        try:
            if arg != []:
                argID = generateUniqueID(arg)
                inputs.append(argID)

        except:
            print("Warning: Could not generate argID for %s at %s, %s" %(name, callNode.scope.filepath, callNode.scope.lineno))
            pass            

    scope = callNode.scope
    color = 'maroon'
    uniqueID = generateUniqueID(callNode)
    
    node = DataNode(name, inputs, scope, color, uniqueID)
    return node


def generateUniqueID(nodeObject):
    uniqueID = ''
    
    uniqueID += ''.join([str(field) for field in nodeObject.scope.ScopeID])
    uniqueID += nodeObject.name
    uniqueID += str(nodeObject.scope.lineno)
    
    return uniqueID


def create_AssignmentNodes_from_Consts(constantList, exConstNames):
    assignmentNodes = []

    for const in constantList:
        if const.name in exConstNames or const.value in language_keywords:
            continue
        name = const.name
        input = const.value
        scope = Scope(const.scope[0], const.scope[1], const.scope[2])

        node = AssignmentNode(name, input, scope)
        assignmentNodes.append(node)

    return assignmentNodes
    
def create_DefNodes_from_FcDefs(fcDefList, exFcnames):
    defNodes = []

    for fc in fcDefList:
        if fc.name in exFcnames:
            continue
        name = fc.name
        args = fc.args
        # for argTokenVals in fc.args:
        #     try:
        #         args.append(argTokenVals[-1]) #TODO:Make robust enough to return type as well
        #     except:
        #         continue
        rettype = fc.rettype
        signature = fc.signature
        callees = fc.callees #TODO:Change from FunctionCall to CallNode?
        scope = Scope(fc.scope[0], fc.scope[1], fc.scope[2])

        node = DefNode(name, args, rettype, signature, callees, scope)        
        defNodes.append(node)

    return defNodes

def create_CallNodes_from_FunctionCalls_and_DefNodes(defNodes, callList, exCallNames):
    callNodes = []

    for fc in callList:
        fcObj = fc
        if fcObj.name in exCallNames:
            continue
        name = fcObj.name                    
        arguments = fcObj.args
        # for argTokenVals in fcObj.args:
        #     try:
        #         arguments.append(argTokenVals[-1]) #TODO:Use tokens instead
        #     except:
        #         continue
        definition = ''
        for defNode in defNodes:
            if defNode.name == name:
                definition = defNode
                break
        scope = Scope(fcObj.scope[0], fcObj.scope[1], fcObj.scope[2])

        node = CallNode(name, arguments, definition, scope)
        callNodes.append(node)

    return callNodes

        

def getDataNodeMx(dataNodes):
    flowMx = []

    # #TODO: Dangling inputs
    # for node in dataNodes:
    #     row = [0]*len(dataNodes)
    #     for input in node.inputs:
    #         for index, checkNode in enumerate(dataNodes):
    #             if checkNode.name == input:
    #                 row[index] = 1
    #     flowMx.append(row)

    #Finding inputs using
    #1. uniqueIDs
        #if the uniqueID of one node matches an input of another,
        #then an edge should certainly be added
    #2. scope understanding
        #the uniqueID of an argument wouldn't match that of the corresponding
        #symbol as they would have different linenos.
        #Equal scope and equal name is should be a hit
        #Higher(?) scope and equal name should be a hit
    #3. Dangler heuristics
        #Some inputs will be lists of ScopedTokens.
        #Compare scope of ST with that of a symbol,
        #and/or the name/value of the ST with that of a symbol.
        #If none are found, create a node using the information in the dangler
        #and add it to the list of inputs/outputs
    for node in dataNodes:
        row = [0]*len(dataNodes)
        for input in node.inputs:
            for index, checkNode in enumerate(dataNodes):
                if checkNode.uniqueID == input:
                    row[index] = 1

        flowMx.append(row)

    

    return flowMx
