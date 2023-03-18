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
    # 'INT',
    # 'FLOAT',
    # 'CHAR',
    'STRING',    
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
    'NONDECIMAL'
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

def t_NONDECIMAL(t):
    r'0[xb]\d+'
    t.value = int(t.value[2:])
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
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
             | func_def             
             | func_call
             | statement
             | control_expr'''

    p[0] = p[1]

def p_literal(p):
    '''literal  : FLOAT
                | INT
                | CHAR
                | STRING
                | NONDECIMAL'''
    p[0] = p[1]

def p_assign(p):
    '''assign : SIMPLE_ASSIGN
              | COMPLEX_ASSIGN'''
    p[0] = p[1]

def p_dtype(p):
    '''dtype : CHAR             
             | DOUBLE
             | FLOAT
             | INT
             | VOID
             | UINT8_T
             | UINT16_T
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

#Preprocessor statements
class IncludeNode(NamedTuple):
    type = 'Include'
    value: str
    user: str

def p_include(p):
    '''include : INCLUDE'''
    incnode = IncludeNode(p[1], "filename")
    p[0] = incnode


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
    '''conditional_expr : ID conditional expression
                        | expression conditional ID
                        | expression conditional expression
                        | ID conditional ID'''
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
    '''func_arg : ID
                | expression
                | dtype ID
                | dtype
                '''
    if len(p) == 2:
        p[0] = ArgumentNode(str(p[1]), str(p[1]))
    elif len(p) == 3:
        p[0] = ArgumentNode(str(p[2].value), str(p[1].value))

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
    '''func_call : ID LPAREN func_arglist RPAREN SEMI
                 '''    
    p[0] = FunctionCallNode(str(p[1]), p[3])

#Structs

#Classes

#Statements and expressions
def p_statement_assign(p):
    '''statement : init_var
                 | assign_var
                 | declare_var
                 | increment'''
    p[0] = p[1]
    
def p_expression_literal(p):
    '''expression : literal'''
                  
    p[0] = p[1]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_bitw_neg(p):
    '''expression : NEGATE expression
                  | MINUS expression'''
    p[0] = p[2]

def p_binops(p):
    '''binop : PLUS
             | MINUS
             | ASTERISK
             | DIVIDE
             | LSHIFT
             | RSHIFT
             | PERCENT'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression binop ID
                  | ID binop expression'''
    p[0] = "binop " + str(p[3])

def p_expression_increment(p):
    '''increment : ID INCREMENT SEMI'''
    p[0] = "increment" + str(p[1])

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
                   | dtype ID assign'''
    if len(p) == 5:
        p[0] = [p[2], p[3]]
    elif len(p) == 4:
        p[0] = [p[1], p[2]]

def p_init_var_rs(p):
    '''init_var_rs : literal SEMI
                   | ID SEMI
                   | LPAREN dtype RPAREN literal SEMI
                   | LPAREN dtype RPAREN ID SEMI
                   | func_call
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

def p_assign_var(p):
    '''assign_var : ID assign expression SEMI'''
    p[0] = VarAssignmentNode(str(p[3]), str(p[1]))
           



#Read and write


#Error handling
def p_error(p):
    print("Syntax error at %s" % p)
    #parser.errok()

parser = yacc.yacc()

code = getFileAsString('/home/kristian/byggern-nicer_code/misc.c')[0:1500]

parser.parse(code,debug=False)
# for node in nodes:
#     print(node)