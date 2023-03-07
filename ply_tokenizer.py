from ply import lex, yacc
from global_utilities import *

# Define the C lexer
keywordList = re.split('\n', getFileAsString('./c_grammar/c_keywords.txt'))
keywordDict = {}
for word in keywordList:
    keywordDict[word] = word.upper()

tokens = [
    'ASSIGN',
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
]+list(keywordDict.values())

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

def t_ASSIGN(t):
    r'(&=)|(\|=)|(\^=)|(%=)|='
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
    t.type = keywordDict.get(t.value, 'ID')
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

# Define the C parser
declarations = []
def p_declaration(p):
    '''declaration : preprocessor'''    
    print("Found something: %s" % p[1])
    p[0] = p[1]
    declarations.append(p[1])


preprocessor_flags = []
def p_preprocessor(p):
    '''preprocessor : IFNDEF
                    | DEFINE'''
    print("Found preprocessor %s" % p[1])
    preprocessor_flags.append(p[1])
    p[0]=p[1]

    

def p_type_specifier(p):
    '''type_specifier : INT
                      | FLOAT
                      | CHAR
                      | VOID
                      | DOUBLE
                      | UINT8_T
                      | UINT16_T
                      | type_specifier ASTERISK
                      | LPAREN type_specifier RPAREN'''
    p[0] = p[1]

# # Define a rule for function declarations
def p_function_declaration(p):
    '''
    function_declaration : type_specifier ID LPAREN parameter_list RPAREN SEMI
                         | type_specifier ASTERISK ID LPAREN parameter_list RPAREN SEMI
                         | type_specifier ID LPAREN RPAREN
                         | type_specifier ASTERISK ID LPAREN RPAREN
    '''
    return {'type': 'function_declaration', 'return_type': p[1], 'name': p[2], 'parameters': p[4]}

# # Define a rule for function calls
# def p_function_call(p):
#     '''
#     function_call : ID LPAREN argument_list RPAREN
#     '''
#     return {'type': 'function_call', 'name': p[1], 'arguments': p[3]}

# Define a rule for parameter lists
def p_parameter_list(p):
    '''
    parameter_list : parameter_declaration
                   | parameter_declaration COMMA parameter_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Define a rule for parameter declarations
def p_parameter_declaration(p):
    '''
    parameter_declaration : type_specifier ID
                          | type_specifier ASTERISK ID
                          | VOID
    '''
    if len(p) == 3:
        return {'type': 'parameter_declaration', 'data_type': p[1], 'name': p[2]}
    if len(p) == 4:
        return {'type': 'parameter_declaration', 'data_type': p[1], 'name': p[3]}
    if len(p) == 2:
        return {'type': 'parameter_declaration', 'data_type': 'void', 'name': 'void'}
    

# # Define a rule for argument lists
# def p_argument_list(p):
#     '''
#     argument_list : expr
#     '''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = [p[1]] + p[3]


def p_expr(p):
    '''expr : INT
            | FLOAT
            | CHAR
            | ID
            | expr PLUS expr
            | expr MINUS expr
            | expr ASTERISK expr
            | expr DIVIDE expr
            | LPAREN expr RPAREN'''
    p[0] = p[1]



def p_error(p):
    print("Syntax error at '%s' line %s" % (p.value, parser.token().lineno))    
    #Expand to look for the next semicolon and then keep trying
    # if not p:
    #     print("End of file!")
    #     return
    # while True:
    #     token = parser.token()
    #     if not token or token.type == 'SEMI':
    #         break
    #parser.restart()

    #Simpler solution: Discard token and carry on
    if p:
        print("Syntax error")
        parser.errok()
    else:
        print("EOF!")



parser = yacc.yacc()

# Parse a list of tokens and extract variable declarations
def ply_tokenize(file_path):
    with open(file_path) as file:
        code = file.read()
    lexer.input(code)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token)       
        print(token) 
    return tokens

def get_variables(tokens):
    variables = set()

    for i, tok in enumerate(tokens):
        if tok.type == 'ID':            
            parser.parse(' '.join(t.value for t in tokens[i:]))

            if parser.symstack[-1] in variables:
                continue

            variables.add(parser.symstack[-1])
    
    return variables

def parse_file(filename):
    """
    Parses a file of C code and returns the abstract syntax tree.
    """
    # read the file contents
    with open(filename, "r") as f:
        code = f.read()

    result = []
    # while True:
    #     try:
    #         s = input(code)            
    #     except EOFError:
    #         break
    print("Parser result:")
    result = parser.parse(code, debug=True)
    return result

def get_variablesv2(tokens):
    """
    Given a list of tokens, returns a set of all variable names.
    """
    variables = set()
    variable_types = {"INT", "FLOAT", "DOUBLE", "CHAR", "LONG", "SHORT"}
    for i in range(len(tokens)):
        if tokens[i].type in variable_types:
            j = i + 1
            while j < len(tokens) and tokens[j].type != "SEMI":
                if tokens[j].type == "ID":
                    variables.add(tokens[j].value)
                j += 1

    return variables

def get_function_declarations(tokens):
    """
    Given a list of tokens, returns a list of function declarations in the form of dictionaries.
    Each dictionary contains the name, return type, and argument types of a function.
    """
    function_regex = r"(\w+\s+)+(\w+)\s*\(([^)]*)\)\s*;"
    function_declarations = []
    for i in range(len(tokens)):
        if tokens[i].type == "ID" and tokens[i+1].value == "(":
            match = re.match(function_regex, tokens[i-1].value + " " + tokens[i].value + " " + tokens[i+1].value)
            if match:
                return_type, function_name, arguments = match.groups()
                argument_types = [arg.strip().split(" ")[0] for arg in arguments.split(",")]
                function_declaration = {
                    "name": function_name,
                    "return_type": return_type.strip(),
                    "argument_types": argument_types
                }
                function_declarations.append(function_declaration)
    return function_declarations

def get_function_calls(tokens):
    """
    Given a list of tokens, returns a list of function calls in the form of dictionaries.
    Each dictionary contains the name and argument values of a function call.
    """
    function_calls = []
    function_call = {}
    for i in range(len(tokens)):
        if tokens[i].type == "ID" and tokens[i+1].value == "(":
            function_call["name"] = tokens[i].value
            function_call["arguments"] = []
            j = i + 2
            while j < len(tokens) and tokens[j].value != ")":
                if tokens[j].value != ",":
                    function_call["arguments"].append(tokens[j].value)
                j += 1
            function_calls.append(function_call)
            function_call = {}
    return function_calls