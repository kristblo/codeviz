from ply import lex, yacc
from global_utilities import *
from typing import NamedTuple

# Define the C lexer
keywordList = re.split('\n', getFileAsString('./c_grammar/c_keywords.txt'))
keywordDict = {}
for word in keywordList:
    keywordDict[word] = word.upper()

tokens = [
    'SIMPLE_ASSIGN',
    'COMPLEX_ASSIGN',
    'COMMENT',
    'LCOMMENT',
    'ID',
    'INT_L', #Int literal; literally an int
    'FLOAT_L',
    'CHAR_L',
    'STRING_L',    
    'PLUS',
    'MINUS',
    'ASTERISK',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'SEMI',
    'EQ',
    'NEQ',
    'LT',
    'LE',
    'GT',
    'GE',
    'NEGATE',
    'PERCENT',
    'AND',
    'OR',    
    'BITAND',
    'BITOR',
    'MEMBER',
    'COMMA',
    'IFNDEF',
    'ENDIF',
    'NUMBER',
    'LSHIFT',
    'RSHIFT',
    'INCREMENT',
    'NONDECIMAL_L'
]+list(keywordDict.values())

reserved = list(keywordDict.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_ASTERISK   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_SEMI    = r';'
t_SIMPLE_ASSIGN = r'='
t_EQ      = r'=='
t_NEQ     = r'!='
t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_NEGATE  = r'~'
t_PERCENT = r'%'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_BITAND  = r'&'
t_BITOR   = r'\|'
t_MEMBER  = r'(->)|(\.)'
t_COMMA   = r','
t_ENDIF   = r'\#endif'
t_ignore = ' \t'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_INCREMENT = r'\+\+'

def t_COMPLEX_ASSIGN(t):
    r'(&=)|(\|=)|(\^=)|(%=)'
    return t

def t_ignore_COMMENT(t):
    r'\/\/[^\n]*'
    #return t
    #t_newline(t)
    pass

def t_ignore_LCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #t.type = keywordDict.get(t.value, 'ID')
    if t.value.upper() in reserved:
        t.type = t.value.upper()        
    return t

def t_NONDECIMAL_L(t):
    r'0[xb]\d+'
    t.value = int(t.value[2:])
    return t

def t_FLOAT_L(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_L(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR_L(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t

def t_STRING_L(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_INCLUDE(t):
    r'\#include\s*("|<).*?(>|")'    
    return t

def t_DEFINE(t):
    r'\#define(\s+\w+)+'    
    return t

def t_IFNDEF(t):
    r'\#ifndef\s+\w+'
    return t

def t_error(t):
    print("Illegal character '%s' line %s" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.columnno = 0

lexer = lex.lex()

################
#####PARSER#####
################
#Top level rule: collect all entities into list of nodes
nodes = []
def p_node_list(p):
    '''node_list :
                 | node_list node'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]
        nodes.append(p[2])
        print("Added ", p[2])

def p_node(p):
    ''' node : include
             | define
             | if
             | func_def                          
             | func_decl
             | statement
             | control_expr
             | struct_def'''

    p[0] = p[1]

#Convenience groups
def p_literal(p):
    '''literal  : FLOAT_L
                | INT_L
                | CHAR_L
                | STRING_L
                | NONDECIMAL_L'''
    p[0] = p[1]

def p_assign(p):
    '''assign : SIMPLE_ASSIGN
              | COMPLEX_ASSIGN'''
    p[0] = p[1]

def p_struct_type(p):
    '''struct_type : STRUCT ID'''
    p[0] = p[2]

def p_type_cast(p):
    '''type_cast : LPAREN dtype RPAREN'''


#TODO: Replace ID with a more robust solution for typedef'd structs! Look at name lookup in calc.py
def p_dtype(p):
    '''dtype : CHAR             
             | DOUBLE
             | FLOAT
             | INT
             | STRUCT
             | VOID
             | UINT8_T
             | UINT16_T
             | struct_type
             | ID
             | dtype ASTERISK'''
    p[0] = p[1]

def p_modifier(p):
    '''modifier : CONST
                | EXTERN
                | INLINE
                | LONG
                | SHORT
                | SIGNED
                | UNSIGNED
                | VOLATILE
                '''
    p[0] = p[1]

def p_names(p):
    '''name : ID
            | literal
            | access'''
    p[0] = p[1]

#Preprocessor statements
class IncludeNode(NamedTuple):
    type = 'Include'
    value: str
    user: str

class DefineNode(NamedTuple):
    type = 'Define'
    value : str


def p_include(p):
    '''include : INCLUDE'''
    incnode = IncludeNode(p[1], "filename")
    p[0] = incnode

def p_define(p):
    '''define : DEFINE '''
    p[0] = DefineNode(p[1])

def p_ifs(p):
    '''if : IFNDEF
          | ENDIF'''
    p[0] = p[1]
    

#Scopes

#Flow control
def p_controls(p):
    '''control : WHILE
              | IF
              | ELSE
                '''
    p[0] = p[1]


def p_conditionals(p):
    '''conditional : EQ
                   | NEQ
                   | LT
                   | GT
                   | LE
                   | GE
                   | AND
                   | OR'''
    p[0] = p[1]

def p_conditional_expr(p):
    '''conditional_expr : name conditional expression
                        | expression conditional name
                        | expression conditional expression
                        | name conditional name
                        | name'''
    p[0] = 'condexpr'

def p_for_loop(p):
    '''for_loop : FOR LPAREN init_var conditional_expr SEMI ID INCREMENT RPAREN'''
    p[0] = 'for_loop'

def p_control_expr(p):
    '''control_expr : control LPAREN conditional_expr RPAREN LBRACE node_list RBRACE
                    | control LBRACE node_list RBRACE
                    | for_loop LBRACE node_list RBRACE'''
    p[0] = str(p[1])+str(p[3])

#Functions
class ArgumentNode(NamedTuple):
    type = 'Argument'
    value : str
    dtype : str

def p_func_arg(p):
    '''func_arg : name                
                | dtype name
                | dtype                
                | type_cast name
                | type_cast expression
                | func_call
                | type_cast func_call'''
    if len(p) == 2:
        p[0] = ArgumentNode(str(p[1]), str(p[1]))
    elif len(p) == 3:
        p[0] = ArgumentNode(str(p[2]), str(p[1]))
    elif len(p) == 5:
        p[0] = ArgumentNode(str(p[4]), str(p[2]))

def p_func_arglist(p):
    '''func_arglist : 
                    | func_arglist func_arg
                    | func_arglist func_arg COMMA'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

class FunctionDefNode(NamedTuple):
    type = 'FunctionDef'
    name:       str
    args:       list #of tuples, for type check
    rettype:    str  #for type check in call
    #signature:  list #for overload check, uniqueID
    #callees:    list #of CallNodes


def p_func_def(p):
    '''func_def : dtype ID LPAREN func_arglist RPAREN LBRACE node_list RBRACE'''    
    fdef = FunctionDefNode(str(p[2]),p[4], str(p[1]))
    p[0] = fdef

class FunctionCallNode(NamedTuple):
    type = 'FunctionCall'
    name : str
    args: list

def p_func_call(p):
    '''func_call : ID LPAREN func_arglist RPAREN
                 '''    
    p[0] = FunctionCallNode(str(p[1]), p[3])

class FunctionDeclNode(NamedTuple):
    type = 'FunctionDef'
    name:       str
    args:       list #of tuples, for type check
    rettype:    str  #for type check in call

def p_func_decl(p):
    '''func_decl : dtype ID LPAREN func_arglist RPAREN SEMI'''
    p[0] = FunctionDeclNode(str(p[2]), p[4], str(p[1]))

#Structs
class AccessNode(NamedTuple):
    type = 'Access'
    accessor : str
    accessee : str

def p_access(p):
    '''access : name LBRACK name RBRACK
              | name LBRACK expression RBRACK
              | name MEMBER name'''
    p[0] = AccessNode(str(p[1]), str(p[3]))

class StructNode(NamedTuple):
    type = 'StructDef'
    name : str
    members : list

def p_struct_def(p):
    '''struct_def : STRUCT ID LBRACE node_list RBRACE SEMI'''
    p[0] = StructNode(str(p[2]), p[4])


#Classes

#Statements and expressions
def p_statement_assign(p):
    '''statement : init_var
                 | assign_var
                 | declare_var
                 '''
    p[0] = p[1]

def p_statement_expression(p):
    '''statement : expression SEMI
                 | func_call SEMI'''
    p[0] = p[1]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN
                  | LPAREN name RPAREN'''
    p[0] = p[2]

def p_expression_neg(p):
    '''expression : NEGATE expression
                  | MINUS expression
                  | NEGATE name
                  | MINUS name'''
    p[0] = 'negate ' + str(p[2])

def p_binops(p):
    '''binop : PLUS
             | MINUS
             | ASTERISK
             | DIVIDE
             | LSHIFT
             | RSHIFT
             | PERCENT
             | BITAND
             | BITOR
             | conditional'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression binop name
                  | name binop expression
                  | name binop name
                  | expression binop expression'''
    p[0] = str(p[1]) + ' binop ' + str(p[3])


def p_expression_increment(p):
    '''expression : ID INCREMENT'''
    p[0] = "increment " + str(p[1])


#Variables
class VarDeclNode(NamedTuple):
    type = 'VarDecl'
    value = 'DECL'
    name: str
    dtype: str

class VarInitNode(NamedTuple):
    type = 'VarInit'
    value: str
    name: str
    dtype: str

class VarAssignmentNode(NamedTuple):
    type = 'VarAssignment'
    value: str
    name: str

def p_decl_var(p):
    '''declare_var : dtype ID SEMI
                   | modifier dtype ID SEMI'''
    
    if len(p) == 4:
        p[0] = VarDeclNode(str(p[2]), str(p[1]))
    elif len(p) == 5:
        p[0] = VarDeclNode(str(p[3]), str(p[1])+' '+str(p[2]))

def p_init_var_ls(p):
    '''init_var_ls : modifier dtype ID assign
                   | dtype ID assign
                   | modifier dtype ID LBRACK RBRACK assign
                   | dtype ID  LBRACK RBRACK assign'''
                   
    if len(p) == 5:
        p[0] = [p[2], p[3]]
    elif len(p) == 4:
        p[0] = [p[1], p[2]]
    elif len(p) == 7:
        p[0] = [str(p[2])+"_arr", p[3]]
    elif len(p) == 6:
        p[0] = [str(p[1])+"_arr", p[2]]

def p_init_var_rs(p):
    '''init_var_rs : name SEMI
                   | type_cast name SEMI                   
                   | func_call SEMI
                   '''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 6:
        p[0] = p[4]
    elif len(p) == 2:
        p[0]  = p[1].name

#'''init_var : dtype ID assign expression SEMI'''
def p_init_var(p):
    '''init_var : init_var_ls init_var_rs'''
    value = p[2]
    name = p[1][1]
    dtype = p[1][0]
    #p[0] = VarInitNode(str(p[4]), str(p[2]), str(p[1]))      
    p[0] = VarInitNode(value, name, dtype)

def p_assign_var_ls(p):
    '''assign_var_ls : name assign'''
    p[0] = p[1]

def p_assign_var_rs(p):
    '''assign_var_rs : expression SEMI
                     | name SEMI
                     | func_call SEMI
                     | type_cast assign_var_rs SEMI'''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    

def p_assign_var(p):
    '''assign_var : assign_var_ls assign_var_rs'''
    p[0] = VarAssignmentNode(str(p[2]), str(p[1]))
           



#Read and write


#Error handling
def p_error(p):
    print("Syntax error at %s" % p)
    #parser.errok()

parser = yacc.yacc()

code = getFileAsString('/home/kristian/byggern-nicer_code/menu.c')

parser.parse(code,debug=False)
# for node in nodes:
#     print(node)