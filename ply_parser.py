from ply_tokenizer import *
from ply_classes import *

#####PARSER#####
################
################
#Top level rule: collect all entities into list of nodes
IncludeNodes = []
DefineNodes = []
FunctionDefNodes = []
FunctionCallNodes = []
FunctionDeclNodes = []
AccessNodes = []
StructNodes = []
VarDeclNodes = []
VarInitNodes = []
VarAssignmentNodes = []

nodes_in_file = []
def p_node_list(p):
    '''node_list :
                 | node_list node'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]
        nodes_in_file.append(p[2])
        #print("Added ", p[2])

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
    '''struct_type : STRUCT name'''
    p[0] = p[2]

def p_type_cast(p):
    '''type_cast : LPAREN dtype RPAREN'''
    p[0] = p[2]

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

def p_modifier_list(p):
    '''modifier_list :
                     | modifier_list modifier
                     '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


#TODO: Replace ID with a more robust solution for typedef'd structs! Look at name lookup in calc.py
def p_dtype(p):
    '''dtype : CHAR             
             | DOUBLE
             | FLOAT
             | INT             
             | VOID
             | INT8_T
             | INT16_T
             | INT32_T
             | INT64_T
             | UINT8_T
             | UINT16_T
             | UINT32_T
             | UINT64_T
             | struct_type             
             | dtype ASTERISK             
             '''
    p[0] = p[1]


def p_names(p):
    '''name : ID
            | literal
            | access'''
    p[0] = p[1]

#Preprocessor statements


def p_include(p):
    '''include : INCLUDE'''
    incnode = IncludeNode(p[1], "filename")
    IncludeNodes.append(incnode)
    p[0] = incnode

def p_define(p):
    '''define : DEFINE '''
    defnode = DefineNode(p[1])
    DefineNodes.append(defnode)
    p[0] = defnode

def p_ifs(p):
    '''if : IFNDEF
          | ENDIF'''
    p[0] = p[1]
    

#Scopes
def p_scope(p):
    '''scope : LBRACE node_list RBRACE'''

    p[0] = p[2]

def p_scope_error(p):
    '''scope : error RBRACE'''
    failstring = '\033[91m'
    formatend = '\033[0m'
    print(f"{failstring}Could not parse scope at %s{formatend}" %p[1])
    p[0] = "Parser error"


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

#TODO: Remove or simplify. No reason to treat condexpr as separate from binop
def p_conditional_expr(p):
    '''conditional_expr : name conditional expression
                        | expression conditional name
                        | expression conditional expression
                        | name conditional name
                        | name
                        | expression'''
    p[0] = 'condexpr'

def p_for_loop(p):
    '''for_loop : FOR LPAREN init_var conditional_expr SEMI ID INCREMENT RPAREN'''
    p[0] = 'for_loop'

def p_control_expr(p):
    '''control_expr : control LPAREN conditional_expr RPAREN scope
                    | control scope
                    | for_loop scope
                    '''
    if len(p) == 3:
        p[0] = str(p[1])
    else:
        p[0] = str(p[1])+str(p[3])

# def p_short_if(p):
#     '''control_expr : IF LPAREN conditional_expr RPAREN node_list'''
#     p[0] = str(p[1]+str(p[2]))

def p_short_else(p):
    '''control_expr : ELSE node_list
                    '''
    p[0] = str(p[1]+str(p[2]))

def p_control_error(p):
    '''control_expr : error LBRACE'''
    failstring = '\033[91m'
    formatend = '\033[0m'
    print(f"{failstring}Could not parse controlexpr at %s{formatend}" %p[1])
    p[0] = "Parser error"

#Functions


#NOTE: Argument syntax is probably one thing that should have a lot of detail
#Also, VOID is a dtype
def p_func_def_arg(p):
    '''func_def_arg : dtype
                    | dtype name
                    | modifier_list dtype name
                    '''
    if len(p) == 2:
        p[0] = ArgumentNode(p[1], p[1])
    if len(p) == 3:
        p[0] = ArgumentNode(p[2], p[1])
    elif len(p) == 4:
        p[0] = ArgumentNode(p[3], p[2])

def p_func_def_arglist(p):
    '''func_def_arglist : 
                        | func_def_arglist func_def_arg
                        | func_def_arglist func_def_arg COMMA'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_func_def(p):
    '''func_def : dtype ID LPAREN func_def_arglist RPAREN scope
                | modifier_list dtype ID LPAREN func_def_arglist RPAREN scope
                | func_call scope
                '''

    if len(p) == 3:
        p[0] = "Implicit def"
    if len(p) == 7:
        fdef = FunctionDefNode(str(p[2]),p[4], str(p[1]), file_scopes[-1])
        FunctionDefNodes.append(fdef)
        p[0] = fdef
    if len(p) == 9:
        fdef = FunctionDefNode(str(p[3]), p[5], str(p[2]), file_scopes[-1])
        FunctionDefNodes.append(fdef)
        p[0] = fdef

def p_func_def_error(p):
    '''func_def : error scope'''
    failstring = '\033[91m'
    formatend = '\033[0m'
    print(f"{failstring}Could not create function def at %s{formatend}" %p[1])
    p[0] = "fdef parser error"


def p_func_decl(p):
    '''func_decl : dtype ID LPAREN func_def_arglist RPAREN SEMI'''
    fdecl = FunctionDeclNode(str(p[2]), p[4], str(p[1]), file_scopeStack)
    FunctionDeclNodes.append(fdecl)
    p[0] = fdecl


def p_func_arg(p):
    '''func_arg : name                
                | dtype             
                | expression   
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

def p_func_call(p):
    '''func_call : ID LPAREN func_arglist RPAREN
                 | SIZEOF LPAREN func_arglist RPAREN
                 '''    
    fcall = FunctionCallNode(str(p[1]), p[3], file_scopeStack)
    FunctionCallNodes.append(fcall)
    p[0] = fcall


#Structs

def p_access(p):
    '''access : name LBRACK name RBRACK
              | name LBRACK expression RBRACK
              | name MEMBER name
              | BITAND name'''
    anode = ''
    if len(p) == 3:
        anode = AccessNode(p[1], p[2], file_scopeStack)
    else:
        anode = AccessNode(str(p[1]), str(p[3]), file_scopeStack)
    AccessNodes.append(anode)
    p[0] = anode


def p_struct_def(p):
    '''struct_def : STRUCT ID scope SEMI'''
    snode = StructNode(str(p[2]), p[4], file_scopes[-1])
    StructNodes.append(snode)
    p[0] = snode

def p_struct_typedef(p):
    '''struct_typedef : TYPEDEF STRUCT scope ID SEMI'''
    snode = StructNode(str(p[6]), p[4], file_scopes[-1])
    StructNodes.append(snode)
    p[0] = snode

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
                 | func_call SEMI
                 | return SEMI'''
    p[0] = p[1]

def p_statement_error(p):
    '''statement : error SEMI'''
    failstring = '\033[91m'
    formatend = '\033[0m'
    print(f"{failstring}Could not create statement at %s{formatend}" %p[1])
    p[0] = "Parser error"

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

def p_operands(p):
    '''operand : name
               | expression
               | type_cast name
               | func_call'''
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : operand binop operand'''
    p[0] = str(p[1]) + ' binop ' + str(p[3])


def p_expression_increment(p):
    '''expression : name INCREMENT'''
    p[0] = "increment " + str(p[1])

def p_expression_return(p):
    '''return : RETURN name
              | RETURN expression'''
    p[0] = p[2]



#Variables

def p_decl_var_ls(p):
    '''declare_var_ls : dtype ID              
                      | modifier_list ID        
                      | modifier_list dtype ID'''

    if len(p) == 3:
        p[0] = [p[1],p[2]]
    if len(p) == 4:
        p[0] = [p[2],p[3]]
    

def p_declare_var(p):
    '''declare_var : declare_var_ls SEMI'''

    vdecl = VarDeclNode(p[1][1], p[1][0], file_scopeStack)
    VarDeclNodes.append(vdecl)
    p[0] = vdecl


def p_vector_init(p):
    '''vector_init : LBRACK RBRACK
                   | LBRACK name RBRACK
                   '''    

def p_vector_init_list(p):
    '''vector_init_list : 
                        | vector_init_list vector_init'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


def p_init_var_ls(p):
    '''init_var_ls : declare_var_ls assign
                   | declare_var_ls vector_init_list assign
                   '''
                       
    # if len(p) == 3:        
    p[0] = [str(p[1][0]), p[1][1]]
    # elif len(p) == 4:
    #     p[0] = [str(p[1]), p[3]]
    
def p_vector_item(p):
    '''vector_item : name
                   | func_call
                   | vector_body'''
    p[0] = p[1]

def p_vector_item_list(p):
    '''vec_item_list : 
                     | vec_item_list vector_item
                     | vec_item_list vector_item COMMA
                     '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 4:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = p[1]
    
def p_vector_body(p):
    '''vector_body : LBRACE vec_item_list RBRACE'''
    p[0] = p[2]

def p_vector_init_rs(p):
    '''vector_init_rs : vector_body SEMI'''
    p[0] = str(p[1]) #TODO: Make the VarInitNode value compatible with type(value)=list

def p_typecast_init_rs(p):
    '''typecast_init : type_cast init_var_rs'''
    p[0] = p[2]


def p_init_var_rs(p):
    '''init_var_rs : name SEMI
                   | func_call SEMI
                   | expression SEMI 
                   | typecast_init
                   | vector_init_rs
                   | LPAREN name RPAREN
                   '''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) ==  2:
        p[0] = p[1]

def p_init_var_rs_error(p):
    '''init_var_rs : error SEMI'''
    print("Couldn't parse right side at %s" %p[1])
    p[0] = "parser_error"

def p_init_var(p):
    '''init_var : init_var_ls init_var_rs'''
    value = p[2]
    name = p[1][1]
    dtype = p[1][0]
    #p[0] = VarInitNode(str(p[4]), str(p[2]), str(p[1]))      
    vinit = VarInitNode(value, name, dtype, file_scopeStack)
    VarInitNodes.append(vinit)
    p[0] = vinit

def p_assign_var_ls(p):
    '''assign_var_ls : name assign'''
    p[0] = p[1]


def p_assign_var_rs(p): #NOTE: Or should initialization be considered a special case of assigment instead?
    '''assign_var_rs : init_var_rs'''
    p[0] = p[1]
    

def p_assign_var(p):
    '''assign_var : assign_var_ls assign_var_rs'''
    vass = VarAssignmentNode(str(p[2]), str(p[1]), file_scopeStack)
    VarAssignmentNodes.append(vass)
    p[0] = vass


#Read and write


#Error handling
def p_error(p):
    #print("Syntax error at %s" % p)
    failstring = '\033[91m'
    formatend = '\033[0m'
    print(f"{failstring}Syntax error at %s{formatend}" %p)
    #parser.errok()

parser = yacc.yacc()

code = getFileAsString('/home/kristian/byggern-nicer_code/misc.c')

parser.parse(code,debug=False)
# for node in nodes:
#     print(node)

for item in FunctionDefNodes:
    for member in item:
        print(member)

    print('\n')

for item in FunctionCallNodes:
    for member in item:
        print(member)

    print('\n')
