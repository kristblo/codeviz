import re
import os
from sys import exit
from global_utilities import *
from c_tokenizer import *

#Find and map all constants and assignments using token signatures
class Constant(NamedTuple):
  name: str
  dtype: str #keyword?
  value: str #right side of assignment
  scope: str #idk, filename? Something to determine validity area

#TODO:implement editability from txt file?
sequences = [['ID', 'ID', 'ASSIGN', 'PAROPEN', 'ID', 'PARCLOSE', 'NUMBER', 'END'],
             ['ID', 'ID', 'ASSIGN', 'PAROPEN', 'ID', 'PARCLOSE', 'ID', 'END'],
             ['ID', 'ID', 'ASSIGN', 'PREFIX', 'NUMBER', 'END'],
             ['ID', 'ID', 'ASSIGN', 'ID', 'END'],
             ['ID', 'ID', 'ASSIGN', 'NUMBER', 'END'],
             ['ID', 'MEMBER', 'ID', 'ASSIGN', 'ID', 'END'],
             ['ID', 'ID', 'END']]

####REWRITE PLY-STYLE####
def assignmentLeftSide():
  ##patterns which form a valid left half of assignments, including ASSIGN
  lsPts = {
    "common":   ['ID', 'ID', 'ASSIGN'],
    "common_p": ['ID', 'ARITOP', 'ID', 'ASSIGN'],
    "member":   ['ID', 'MEMBER', 'ID', 'ASSIGN'],
    "decl"  :   ['ID', 'ID', 'END']
  }
  return lsPts

def assignmentRightSide():
  ##patterns which form a valid right half of assignents, from ASSIGN trough END
  rsPts = {
    "typecast_id":  ['PAROPEN', 'ID', 'PARCLOSE', 'ID', 'END'] ,
    "typecast_num": ['PAROPEN', 'ID', 'PARCLOSE', 'NUMBER', 'END'],
    "typecast_p":   ['PAROPEN', 'ID', 'ARITOP', 'PARCLOSE', 'ID', 'END'],
    "nondec_const": ['PREFIX', 'NUMBER', 'END'],
    "dec_const":    ['NUMBER', 'END'],
    "reassign":     ['ID', 'END'],
    "fc_call":      ['ID', 'PAROPEN']
  }
  return rsPts

assignmentpatterns = [assignmentLeftSide, assignmentRightSide]

def findAssignments(tokenList, currentFileName):
  assignments = []

  leftSide = []
  rightSide = []
  for index, token in enumerate(tokenList):
    #Find a left side match    
    for patternname in assignmentpatterns[0]():      
      pattern = assignmentpatterns[0]()[patternname]      
      try:
        tokenListSlice = [token for token in tokenList[index:index+len(pattern)]]        
      except:
        continue #Use this to trigger right half finding?
      tokenTypeSlice = [token.type for token in tokenListSlice]      
      if tokenTypeSlice == pattern:        
        if patternname == 'common':
          leftSide = [tokenListSlice[0].value, tokenListSlice[1].value]
        if patternname == 'common_p':
          leftSide = [tokenListSlice[0].value+'*', tokenListSlice[2].value]
        if patternname == 'member':
          leftSide = ['ASSIGNMENT', ''.join(token.value for token in tokenListSlice[0:3])]  
        if patternname == 'decl':
          #We might actually not be interested in declarations.
          #They don't contain any data flow.
          #No, but they might be used for it later
          leftSide = [tokenListSlice[0].value, tokenListSlice[1].value]
          rightSide = ['DECL', str(tokenListSlice[0].line)]
        break        
    
    #Continue onto right side after left side is found
    if leftSide != [] and rightSide == []:      
      for patternname in assignmentpatterns[1]():
        pattern = assignmentpatterns[1]()[patternname]
        try:
          tokenListSlice = [token for token in tokenList[index:index+len(pattern)]]
        except:
          continue
        tokenTypeSlice = [token.type for token in tokenListSlice]        
        if tokenTypeSlice == pattern:         
          rightSide = [str(tokenListSlice[-2].value), str(tokenListSlice[-2].line)]
          break          

    #Make the Constant object    
    if rightSide != []:      
      assignments.append(Constant(leftSide[1], \
                                  leftSide[0], \
                                  rightSide[0],\
                                  currentFileName+' '+rightSide[1]))
      leftSide = []
      rightSide = []


  return assignments

####PLY-STYLE REWRITE END####
def updateConstantScopes(constList, filename):
  for item in constList:
    item._replace(scope = filename)

  return constList

def getProjectConstants(tokenizedFiles):
  constantList = []
  
  for file in tokenizedFiles:
    tokens = tokenizedFiles[file]
    localconsts = findAssignments(tokens, file)
    #scopedconsts = updateConstantScopes(localconsts, file)
    for item in localconsts:
      constantList.append(item)      
  
  return constantList
