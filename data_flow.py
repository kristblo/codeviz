from typing import NamedTuple
from  global_utilities import *
from c_tokenizer import tokenizeCode
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
    inputs = list
    output = list
    uniquename = str #some unique identifier to prevent confusion

excludedFcNames = ['printf', '_delay_ms']
def createNodesFromFcCalls(fcCallList, excludedFcNames):
    dataNodes = []

    for fc in fcCallList:
        fcObject = fc[1]        
        outputs = []
        inputs = []

        if fcObject.name in excludedFcNames:
            continue
        for ArgList in fcObject.args:
            for argStr in ArgList:
                argToken = tokenizeCode(argStr)
                if argToken[0].type == 'ID' and argToken[0].value not in language_keywords:
                    inputs.append(str(argToken[0].value))        

        print(fcObject.name, inputs, outputs, 'idstr')

            


    return dataNodes


