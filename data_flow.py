from typing import NamedTuple
from  global_utilities import *
from c_tokenizer import tokenizeString
from analyse_functions import *




#Goal: store relations relevant to the flow of data in a project, such that
#they may be visualised in graphtool. 
#Use tokenized data and functions (and incs?)
#1. Arguments in function calls
#2. Assignments (= et var)
#3. Member variable access (., ->)

#Make a node object that generalises the idea of inputs and outputs?
#For functions: args global vars/funcs are inputs, return is output
#For variables: Right side of assignment is input, output defined implicitly by users

class DataNode(NamedTuple):
    name: str #the node's human-readable name as defined in the source code
    inputs: list
    output: list
    uniquename: str #some unique identifier to prevent confusion

#TODO: Make part of config
excludedFcNames = ['printf','printi','prints','printchar', '_delay_ms', 'malloc']
def createNodesFromFcCalls(fcCallList, excludedFcNames):
    dataNodes = []

    for fc in fcCallList:
        fcObject = fc[1]        
        outputs = []
        inputs = []

        if fcObject.name in excludedFcNames:
            continue
        for ArgList in fcObject.args:
            currentarg = ''
            for argStr in ArgList:
                argToken = tokenizeString(str(argStr))
                if argToken[0].value not in language_keywords:
                    currentarg += (str(argToken[0].value))
            inputs.append(currentarg)
            currentarg = ''

        #print(fcObject.name, inputs, outputs, 'idstr')
        dataNodes.append(DataNode(fcObject.name, inputs, outputs, fcObject.scope[0]))

            


    return dataNodes

def createNodesFromFcDefs(fcDefList, excludedFcNames):
    dataNodes = []

    for fc in fcDefList:
        fcObject = fc        
        outputs = [fcObject.rettype]
        inputs = []

        if fcObject.name in excludedFcNames:
            continue
        for callee in fcObject.callees:
            inputs.append(callee.name)
        node = DataNode(fcObject.name, inputs, outputs, fc.scope)
                            
        dataNodes.append(node)

    return dataNodes

#TODO: Make part of config, include reserved names
excludedConstNames = ['i'] 
def createNodesFromConstants(constantList, excludedConstNames):
    dataNodes = []

    for const in constantList:
        if const.name in excludedConstNames:
            continue
        name = const.name
        scope = const.scope
        input = [const.value]
        output = ['CONST']

        dataNodes.append(DataNode(name, input, output, scope))

    return dataNodes

def getDataFlowData(constList,
                      exclConstNames,
                      fcCallList,
                      fcDefList,
                      exclFcNames):
    constNodes = createNodesFromConstants(constList, exclConstNames)
    funcCallNodes = createNodesFromFcCalls(fcCallList, exclFcNames)
    funcDefNodes = createNodesFromFcDefs(fcDefList, exclFcNames)
    allNodes = constNodes + funcCallNodes + funcDefNodes
    flowMx = []#Nodes²
    
    #Index is 1 indicates input
    # => If an input of a Node can be found as a name of another, set 1
    #TODO: Dangling inputs
    for node in allNodes:
        row = [0]*len(allNodes)
        currentNodeInputs = node.inputs
        for input in currentNodeInputs:
            for index, checkNode in enumerate(allNodes):
                currentName = checkNode.name
                if currentName == input:
                    row[index] = 1
        flowMx.append(row)

    return flowMx, allNodes
