from ply import lex, yacc
from global_utilities import *
from typing import NamedTuple
from ply_project import calculateScope

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
# t_LBRACE  = r'\{'
# t_RBRACE  = r'\}'
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


file_scopeStack = []
file_scopes = []
def t_LBRACE(t):
    r'\{'
    calculateScope(t, file_scopeStack, file_scopes)
    return t

def t_RBRACE(t):
    r'\}'
    calculateScope(t, file_scopeStack, file_scopes)
    return t

def t_COMPLEX_ASSIGN(t):
    r'(&=)|(\|=)|(\^=)|(%=)|(\*=)|(\/=)|(\+=)|(-=)'
    return t

def t_ignore_COMMENT(t):
    r'\/\/[^\n]*'
    #return t
    #t_newline(t)
    pass

def t_ignore_LCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_ignore_PROGMEM(t):
    r'PROGMEM'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #t.type = keywordDict.get(t.value, 'ID')
    if t.value.upper() in reserved:
        t.type = t.value.upper()        
    return t

def t_NONDECIMAL_L(t):
    r'0[xXbB][0-9a-fA-F]+'    
    if t.value[1] in 'xX':
        t.value = int(t.value, 16)
    elif t.value[1] in 'bB':
        t.value = int(t.value, 2)

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
    r'\#define([\t\f ]+\w+)+'
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

