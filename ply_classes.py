from typing import NamedTuple

class Scope(NamedTuple):
    type = 'Scope'
    scopeID : list
    scopeStart : int
    scopeEnd : int

class IncludeNode(NamedTuple):
    type = 'Include'
    value: str
    user: str

class DefineNode(NamedTuple):
    type = 'Define'
    value : str

class ArgumentNode(NamedTuple):
    type = 'Argument'
    value : str
    dtype : str

class FunctionDefNode(NamedTuple):
    type = 'FunctionDef'
    name:       str
    args:       list #of tuples, for type check
    rettype:    str  #for type check in call
    scope : Scope
    #signature:  list #for overload check, uniqueID
    #callees:    list #of CallNodes

class FunctionCallNode(NamedTuple):
    type = 'FunctionCall'
    name : str
    args: list
    scopeID : list

class FunctionDeclNode(NamedTuple):
    type = 'FunctionDef'
    name:       str
    args:       list #of tuples, for type check
    rettype:    str  #for type check in call
    scopeID : list

class AccessNode(NamedTuple):
    type = 'Access'
    accessor : str
    accessee : str
    scopeID : list

class StructNode(NamedTuple):
    type = 'StructDef'
    name : str
    members : list
    scope : Scope

class VarDeclNode(NamedTuple):
    type = 'VarDecl'
    value = 'DECL'
    name: str
    dtype: str
    scopeID : list

class VarInitNode(NamedTuple):
    type = 'VarInit'
    value: str
    name: str
    dtype: str
    scopeID : list

class VarAssignmentNode(NamedTuple):
    type = 'VarAssignment'
    value: str
    name: str
    scopeID : list
