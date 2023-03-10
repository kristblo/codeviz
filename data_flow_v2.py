from typing import NamedTuple
from global_utilities import *
from c_tokenizer import *
from analyse_assignments import *
from analyse_functions import *

#For use with GraphTool
class Scope(NamedTuple):
    filepath:   str
    lineno:     str

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
    inputs = [assignmentNode.input] #TODO: Make unique?
    scope = assignmentNode.scope
    color = 'orange' #TODO: Find out if graph-tool takes color words
    uniqueID = ''.join([field for field in scope])+name
    
    node = DataNode(name, inputs, scope, color, uniqueID)
    return node

def dataNode_from_defNode(definitionNode):
    name = definitionNode.name
    inputs = []
    try:
        for callee in definitionNode.callees:
            inputs.append(callee.name)#TODO: Fix uniqueIDs
    except:
        pass
    for argtokens in definitionNode.args:
        inputs.append(argtokens[-1]) #TODO: Create a symbol list

    scope = definitionNode.scope
    color = 'maroon'
    uniqueID = ''.join([str(field) for field in scope])

    node = DataNode(name, inputs, scope, color, uniqueID)
    return node    

#Effectively becomes a mix of call and its def
def dataNode_from_callNode(callNode):
    name = callNode.name
    
    inputs = [] #Predictably calculable uniqueIDs for args and callees
    try:
        for callee in callNode.definition.callees:
            calleeID = ''.join([str(field) for field in callee.scope])+callee.name
            #inputs.append(calleeID) #TODO: Fix uniqueIDs
            inputs.append(callee.name)

    except:
        pass    
    for arg in callNode.arguments:
        #Assuming a function won't take an argument from outside
        # its own file, and that arg.value is unique
        path = callNode.scope.filepath
        argID = path+str(arg) #TODO:Use tokens/refined argtypes
        #inputs.append(argID) #TODO:Fix uniqueID
        inputs.append(arg)
    scope = callNode.scope
    color = 'maroon'
    uniqueID = ''.join([str(field) for field in callNode.scope])+callNode.name
    
    node = DataNode(name, inputs, scope, color, uniqueID)
    return node


def generateUniqueID(nodeObject):
    uniqueID = ''

    uniqueID += nodeObject.scope.filepath
    uniqueID += nodeObject.name
    uniqueID += nodeObject.scope.lineno

    return uniqueID


def create_AssignmentNodes_from_Consts(constantList, exConstNames):
    assignmentNodes = []

    for const in constantList:
        if const.name in exConstNames:
            continue
        name = const.name
        input = const.value
        scope = Scope(const.scope[0], const.scope[1])

        node = AssignmentNode(name, input, scope)
        assignmentNodes.append(node)

    return assignmentNodes
    
def create_DefNodes_from_FcDefs(fcDefList, exFcnames):
    defNodes = []

    for fc in fcDefList:
        if fc.name in exFcnames:
            continue
        name = fc.name
        args = []
        for argTokenVals in fc.args:
            try:
                args.append(argTokenVals[-1]) #TODO:Make robust enough to return type as well
            except:
                continue
        rettype = fc.rettype
        signature = fc.signature
        callees = fc.callees #TODO:Change from FunctionCall to CallNode?
        scope = Scope(fc.scope[0], fc.scope[1])

        node = DefNode(name, args, rettype, signature, callees, scope)        
        defNodes.append(node)

    return defNodes

def create_CallNodes_from_FunctionCalls_and_DefNodes(defNodes, callList, exCallNames):
    callNodes = []

    for fc in callList:
        fcObj = fc[1]
        if fcObj.name in exCallNames:
            continue
        name = fcObj.name
        arguments = []
        for argTokenVals in fcObj.args:
            try:
                arguments.append(argTokenVals[-1]) #TODO:Use tokens instead
            except:
                continue
        definition = ''
        for defNode in defNodes:
            if defNode.name == name:
                definition = defNode
                break
        scope = Scope(fcObj.scope[0], fcObj.scope[1])

        node = CallNode(name, arguments, definition, scope)
        callNodes.append(node)

    return callNodes

        

def getDataNodeMx(dataNodes):
    flowMx = []

    #TODO: Dangling inputs
    for node in dataNodes:
        row = [0]*len(dataNodes)
        for input in node.inputs:
            for index, checkNode in enumerate(dataNodes):
                if checkNode.name == input:
                    row[index] = 1
        flowMx.append(row)

    return flowMx
