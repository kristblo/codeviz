
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASTERISK AUTO BITAND BITOR BREAK CASE CHAR COMMA COMMENT COMPLEX_ASSIGN CONST CONTINUE DEFAULT DEFINE DIVIDE DO DOUBLE ELSE ENDIF ENUM EQ EXTERN FLOAT FOR GE GOTO GT ID IF IFNDEF INCLUDE INCREMENT INLINE INT LBRACE LBRACK LCOMMENT LE LONG LPAREN LSHIFT LT MEMBER MINUS NEGATE NEQ NONDECIMAL NUMBER OR PERCENT PLUS RBRACE RBRACK REGISTER RESTRICT RETURN RPAREN RSHIFT SEMI SHORT SIGNED SIMPLE_ASSIGN SIZEOF STATIC STRING STRUCT SWITCH TYPEDEF UINT16_T UINT8_T UNION UNSIGNED VOID VOLATILE WHILE _ALIGNAS _ALIGNOF _ATOMIC _BOOL _COMPLEX _GENERIC _IMAGERY _NORETURN _STATIC_ASSERT _THREAD_LOCALnode_list :\n                 | node_list node node : include\n             | func_def             \n             | func_call\n             | statement\n             | control_exprliteral  : FLOAT\n                | INT\n                | CHAR\n                | STRING\n                | NONDECIMALassign : SIMPLE_ASSIGN\n              | COMPLEX_ASSIGNdtype : CHAR             \n             | DOUBLE\n             | FLOAT\n             | INT\n             | VOID\n             | UINT8_T\n             | UINT16_T\n             | dtype ASTERISKmodifier : CONST\n                | EXTERN\n                | INLINE\n                | LONG\n                | SHORT\n                | SIGNED\n                | UNSIGNED\n                | VOLATILE\n                include : INCLUDEcontrol : WHILE\n              | IF\n              | ELSE\n                conditional : EQ\n                   | NEQ\n                   | LT\n                   | GT\n                   | LE\n                   | GE\n                   | AND\n                   | ORconditional_expr : ID conditional expression\n                        | expression conditional ID\n                        | expression conditional expression\n                        | ID conditional IDfor_loop : FOR LPAREN init_var conditional_expr SEMI ID INCREMENT RPARENcontrol_expr : control LPAREN conditional_expr RPAREN LBRACE node_list RBRACE\n                    | control LBRACE node_list RBRACE\n                    | for_loop LBRACE node_list RBRACEfunc_arg : ID\n                | expression\n                | dtype ID\n                | dtype\n                func_arglist : \n                    | func_arglist func_arg\n                    | func_arglist func_arg COMMAfunc_def : dtype ID LPAREN func_arglist RPAREN LBRACE node_list RBRACEfunc_call : ID LPAREN func_arglist RPAREN SEMI\n                 statement : init_var\n                 | assign_var\n                 | declare_var\n                 | incrementexpression : literalexpression : LPAREN expression RPARENexpression : NEGATE expression\n                  | MINUS expressionbinop : PLUS\n             | MINUS\n             | ASTERISK\n             | DIVIDE\n             | LSHIFT\n             | RSHIFT\n             | PERCENTexpression : expression binop ID\n                  | ID binop expressionincrement : ID INCREMENT SEMIdeclare_var : dtype ID SEMI\n                   | modifier dtype ID SEMIinit_var_ls : modifier dtype ID assign\n                   | dtype ID assigninit_var_rs : literal SEMI\n                   | ID SEMI\n                   | LPAREN dtype RPAREN literal SEMI\n                   | LPAREN dtype RPAREN ID SEMI\n                   | func_call\n                   init_var : init_var_ls init_var_rsassign_var : ID assign expression SEMI'
    
_lr_action_items = {'INCLUDE':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,8,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,8,8,-82,-83,-88,-49,-50,-79,-59,-1,-1,8,-84,-85,8,-48,-58,]),'ID':([0,1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,20,21,22,23,24,39,40,41,43,44,45,46,47,48,52,53,54,55,56,57,58,60,61,62,63,66,67,68,69,70,74,75,76,77,80,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,125,126,127,128,129,130,131,138,140,141,142,143,145,146,148,],[-1,10,-2,-3,-4,-5,-6,-7,-31,38,-60,-61,-62,-63,-15,-16,-17,-18,-19,-20,-21,50,-22,-55,64,-13,-14,72,-1,-1,-87,-86,-8,-9,-10,-11,-12,79,-55,-78,-81,84,-64,64,64,64,-77,10,10,-82,-83,72,123,84,-51,-56,-52,127,-10,-8,-9,64,-68,-69,-70,-71,-72,-73,-74,-88,129,-66,-67,132,-35,-36,-37,-38,-39,-40,-41,-42,135,-49,-50,137,-79,-80,139,-59,-57,-53,-76,-75,-65,-1,144,-1,10,-84,-85,10,-48,-58,]),'CHAR':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,24,25,30,31,32,33,34,35,36,37,39,40,41,43,44,45,46,47,48,51,52,53,54,55,56,57,59,60,61,62,63,66,67,68,69,70,74,75,76,77,80,81,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,17,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,55,17,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,55,-13,-14,55,-1,-1,-87,17,-86,-8,-9,-10,-11,-12,17,-55,-78,-81,89,-64,55,55,55,-77,17,17,-82,-83,55,17,89,-51,-56,-52,-54,-10,-8,-9,55,-68,-69,-70,-71,-72,-73,-74,-88,-66,-67,55,-35,-36,-37,-38,-39,-40,-41,-42,55,-49,-50,55,-79,-80,-59,-57,-53,-76,-75,-65,-1,-1,17,-84,-85,17,-48,-58,]),'DOUBLE':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,25,30,31,32,33,34,35,36,37,39,40,46,47,48,51,52,53,54,55,56,57,59,60,61,63,66,70,74,75,76,77,81,83,84,86,87,88,89,90,91,100,103,104,116,117,119,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,18,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,18,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,-1,-1,-87,18,-86,-8,-9,-10,-11,-12,18,-55,-78,18,-64,-77,18,18,-82,-83,18,18,-51,-56,-52,-54,-10,-8,-9,-88,-66,-67,-49,-50,-79,-59,-57,-53,-76,-75,-65,-1,-1,18,-84,-85,18,-48,-58,]),'FLOAT':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,24,25,30,31,32,33,34,35,36,37,39,40,41,43,44,45,46,47,48,51,52,53,54,55,56,57,59,60,61,62,63,66,67,68,69,70,74,75,76,77,80,81,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,19,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,53,19,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,53,-13,-14,53,-1,-1,-87,19,-86,-8,-9,-10,-11,-12,19,-55,-78,-81,90,-64,53,53,53,-77,19,19,-82,-83,53,19,90,-51,-56,-52,-54,-10,-8,-9,53,-68,-69,-70,-71,-72,-73,-74,-88,-66,-67,53,-35,-36,-37,-38,-39,-40,-41,-42,53,-49,-50,53,-79,-80,-59,-57,-53,-76,-75,-65,-1,-1,19,-84,-85,19,-48,-58,]),'INT':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,24,25,30,31,32,33,34,35,36,37,39,40,41,43,44,45,46,47,48,51,52,53,54,55,56,57,59,60,61,62,63,66,67,68,69,70,74,75,76,77,80,81,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,20,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,54,20,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,54,-13,-14,54,-1,-1,-87,20,-86,-8,-9,-10,-11,-12,20,-55,-78,-81,91,-64,54,54,54,-77,20,20,-82,-83,54,20,91,-51,-56,-52,-54,-10,-8,-9,54,-68,-69,-70,-71,-72,-73,-74,-88,-66,-67,54,-35,-36,-37,-38,-39,-40,-41,-42,54,-49,-50,54,-79,-80,-59,-57,-53,-76,-75,-65,-1,-1,20,-84,-85,20,-48,-58,]),'VOID':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,25,30,31,32,33,34,35,36,37,39,40,46,47,48,51,52,53,54,55,56,57,59,60,61,63,66,70,74,75,76,77,81,83,84,86,87,88,89,90,91,100,103,104,116,117,119,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,21,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,21,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,-1,-1,-87,21,-86,-8,-9,-10,-11,-12,21,-55,-78,21,-64,-77,21,21,-82,-83,21,21,-51,-56,-52,-54,-10,-8,-9,-88,-66,-67,-49,-50,-79,-59,-57,-53,-76,-75,-65,-1,-1,21,-84,-85,21,-48,-58,]),'UINT8_T':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,25,30,31,32,33,34,35,36,37,39,40,46,47,48,51,52,53,54,55,56,57,59,60,61,63,66,70,74,75,76,77,81,83,84,86,87,88,89,90,91,100,103,104,116,117,119,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,22,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,22,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,-1,-1,-87,22,-86,-8,-9,-10,-11,-12,22,-55,-78,22,-64,-77,22,22,-82,-83,22,22,-51,-56,-52,-54,-10,-8,-9,-88,-66,-67,-49,-50,-79,-59,-57,-53,-76,-75,-65,-1,-1,22,-84,-85,22,-48,-58,]),'UINT16_T':([0,1,2,3,4,5,6,7,8,11,12,13,14,18,21,22,23,25,30,31,32,33,34,35,36,37,39,40,46,47,48,51,52,53,54,55,56,57,59,60,61,63,66,70,74,75,76,77,81,83,84,86,87,88,89,90,91,100,103,104,116,117,119,125,126,127,128,129,130,131,140,141,142,143,145,146,148,],[-1,23,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-16,-19,-20,-21,23,-23,-24,-25,-26,-27,-28,-29,-30,-22,-55,-1,-1,-87,23,-86,-8,-9,-10,-11,-12,23,-55,-78,23,-64,-77,23,23,-82,-83,23,23,-51,-56,-52,-54,-10,-8,-9,-88,-66,-67,-49,-50,-79,-59,-57,-53,-76,-75,-65,-1,-1,23,-84,-85,23,-48,-58,]),'WHILE':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,26,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,26,26,-82,-83,-88,-49,-50,-79,-59,-1,-1,26,-84,-85,26,-48,-58,]),'IF':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,27,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,27,27,-82,-83,-88,-49,-50,-79,-59,-1,-1,27,-84,-85,27,-48,-58,]),'ELSE':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,28,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,28,28,-82,-83,-88,-49,-50,-79,-59,-1,-1,28,-84,-85,28,-48,-58,]),'FOR':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,29,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,29,29,-82,-83,-88,-49,-50,-79,-59,-1,-1,29,-84,-85,29,-48,-58,]),'CONST':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,30,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,30,-78,-77,30,30,-82,-83,-88,-49,-50,-79,-59,-1,-1,30,-84,-85,30,-48,-58,]),'EXTERN':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,31,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,31,-78,-77,31,31,-82,-83,-88,-49,-50,-79,-59,-1,-1,31,-84,-85,31,-48,-58,]),'INLINE':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,32,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,32,-78,-77,32,32,-82,-83,-88,-49,-50,-79,-59,-1,-1,32,-84,-85,32,-48,-58,]),'LONG':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,33,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,33,-78,-77,33,33,-82,-83,-88,-49,-50,-79,-59,-1,-1,33,-84,-85,33,-48,-58,]),'SHORT':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,34,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,34,-78,-77,34,34,-82,-83,-88,-49,-50,-79,-59,-1,-1,34,-84,-85,34,-48,-58,]),'SIGNED':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,35,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,35,-78,-77,35,35,-82,-83,-88,-49,-50,-79,-59,-1,-1,35,-84,-85,35,-48,-58,]),'UNSIGNED':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,36,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,36,-78,-77,36,36,-82,-83,-88,-49,-50,-79,-59,-1,-1,36,-84,-85,36,-48,-58,]),'VOLATILE':([0,1,2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,59,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-1,37,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,37,-78,-77,37,37,-82,-83,-88,-49,-50,-79,-59,-1,-1,37,-84,-85,37,-48,-58,]),'$end':([0,1,2,3,4,5,6,7,8,11,12,13,14,48,52,61,70,76,77,100,116,117,119,125,142,143,146,148,],[-1,0,-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-87,-86,-78,-77,-82,-83,-88,-49,-50,-79,-59,-84,-85,-48,-58,]),'RBRACE':([2,3,4,5,6,7,8,11,12,13,14,46,47,48,52,61,70,74,75,76,77,100,116,117,119,125,131,140,141,142,143,145,146,148,],[-2,-3,-4,-5,-6,-7,-31,-60,-61,-62,-63,-1,-1,-87,-86,-78,-77,116,117,-82,-83,-88,-49,-50,-79,-59,-1,-1,146,-84,-85,148,-48,-58,]),'ASTERISK':([9,17,18,19,20,21,22,23,39,53,54,55,56,57,58,64,65,66,72,73,78,82,84,87,88,89,90,91,102,103,104,122,128,129,130,132,133,134,135,],[39,-15,-16,-17,-18,-19,-20,-21,-22,-8,-9,-10,-11,-12,39,95,95,-64,95,95,39,39,95,95,39,-10,-8,-9,95,95,95,39,95,-75,-65,95,95,95,95,]),'LPAREN':([10,15,18,21,22,23,24,26,27,28,29,38,39,40,41,43,44,45,48,50,52,53,54,55,56,57,60,62,63,66,67,68,69,76,77,80,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,103,104,106,107,108,109,110,111,112,113,114,115,120,125,126,127,128,129,130,142,143,],[40,45,-16,-19,-20,-21,51,-32,-33,-34,59,60,-22,-55,67,-13,-14,67,-87,40,-86,-8,-9,-10,-11,-12,-55,-81,67,-64,67,67,67,-82,-83,67,67,-51,-56,-52,-54,-10,-8,-9,67,-68,-69,-70,-71,-72,-73,-74,-66,-67,67,-35,-36,-37,-38,-39,-40,-41,-42,67,-80,-59,-57,-53,-76,-75,-65,-84,-85,]),'INCREMENT':([10,144,],[42,147,]),'SIMPLE_ASSIGN':([10,38,79,123,139,],[43,43,43,43,43,]),'COMPLEX_ASSIGN':([10,38,79,123,139,],[44,44,44,44,44,]),'LBRACE':([15,16,26,27,28,105,124,149,],[46,47,-32,-33,-34,131,140,-47,]),'RPAREN':([17,18,19,20,21,22,23,39,40,53,54,55,56,57,60,63,66,71,78,83,84,86,87,88,89,90,91,102,103,104,126,127,128,129,130,132,133,134,135,147,],[-15,-16,-17,-18,-19,-20,-21,-22,-55,-8,-9,-10,-11,-12,-55,85,-64,105,118,124,-51,-56,-52,-54,-10,-8,-9,130,-66,-67,-57,-53,-76,-75,-65,-46,-43,-45,-44,149,]),'COMMA':([18,21,22,23,39,53,54,55,56,57,66,84,86,87,88,89,90,91,103,104,127,128,129,130,],[-16,-19,-20,-21,-22,-8,-9,-10,-11,-12,-64,-51,126,-52,-54,-10,-8,-9,-66,-67,-53,-76,-75,-65,]),'NEGATE':([18,21,22,23,39,40,41,43,44,45,48,52,53,54,55,56,57,60,63,66,67,68,69,76,77,80,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,103,104,106,107,108,109,110,111,112,113,114,115,125,126,127,128,129,130,142,143,],[-16,-19,-20,-21,-22,-55,68,-13,-14,68,-87,-86,-8,-9,-10,-11,-12,-55,68,-64,68,68,68,-82,-83,68,68,-51,-56,-52,-54,-10,-8,-9,68,-68,-69,-70,-71,-72,-73,-74,-66,-67,68,-35,-36,-37,-38,-39,-40,-41,-42,68,-59,-57,-53,-76,-75,-65,-84,-85,]),'MINUS':([18,21,22,23,39,40,41,43,44,45,48,52,53,54,55,56,57,60,63,64,65,66,67,68,69,72,73,76,77,80,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,102,103,104,106,107,108,109,110,111,112,113,114,115,125,126,127,128,129,130,132,133,134,135,142,143,],[-16,-19,-20,-21,-22,-55,69,-13,-14,69,-87,-86,-8,-9,-10,-11,-12,-55,69,94,94,-64,69,69,69,94,94,-82,-83,69,69,94,-56,94,-54,-10,-8,-9,69,-68,-69,-70,-71,-72,-73,-74,94,94,94,69,-35,-36,-37,-38,-39,-40,-41,-42,69,-59,-57,-53,94,-75,-65,94,94,94,94,-84,-85,]),'STRING':([18,21,22,23,24,39,40,41,43,44,45,48,52,53,54,55,56,57,60,62,63,66,67,68,69,76,77,80,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,103,104,106,107,108,109,110,111,112,113,114,115,118,120,125,126,127,128,129,130,142,143,],[-16,-19,-20,-21,56,-22,-55,56,-13,-14,56,-87,-86,-8,-9,-10,-11,-12,-55,-81,56,-64,56,56,56,-82,-83,56,56,-51,-56,-52,-54,-10,-8,-9,56,-68,-69,-70,-71,-72,-73,-74,-66,-67,56,-35,-36,-37,-38,-39,-40,-41,-42,56,56,-80,-59,-57,-53,-76,-75,-65,-84,-85,]),'NONDECIMAL':([18,21,22,23,24,39,40,41,43,44,45,48,52,53,54,55,56,57,60,62,63,66,67,68,69,76,77,80,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,103,104,106,107,108,109,110,111,112,113,114,115,118,120,125,126,127,128,129,130,142,143,],[-16,-19,-20,-21,57,-22,-55,57,-13,-14,57,-87,-86,-8,-9,-10,-11,-12,-55,-81,57,-64,57,57,57,-82,-83,57,57,-51,-56,-52,-54,-10,-8,-9,57,-68,-69,-70,-71,-72,-73,-74,-66,-67,57,-35,-36,-37,-38,-39,-40,-41,-42,57,57,-80,-59,-57,-53,-76,-75,-65,-84,-85,]),'SEMI':([38,42,49,50,53,54,55,56,57,65,66,79,85,103,104,121,128,129,130,132,133,134,135,136,137,],[61,70,76,77,-8,-9,-10,-11,-12,100,-64,119,125,-66,-67,138,-76,-75,-65,-46,-43,-45,-44,142,143,]),'PLUS':([53,54,55,56,57,64,65,66,72,73,84,87,89,90,91,102,103,104,128,129,130,132,133,134,135,],[-8,-9,-10,-11,-12,93,93,-64,93,93,93,93,-10,-8,-9,93,93,93,93,-75,-65,93,93,93,93,]),'DIVIDE':([53,54,55,56,57,64,65,66,72,73,84,87,89,90,91,102,103,104,128,129,130,132,133,134,135,],[-8,-9,-10,-11,-12,96,96,-64,96,96,96,96,-10,-8,-9,96,96,96,96,-75,-65,96,96,96,96,]),'LSHIFT':([53,54,55,56,57,64,65,66,72,73,84,87,89,90,91,102,103,104,128,129,130,132,133,134,135,],[-8,-9,-10,-11,-12,97,97,-64,97,97,97,97,-10,-8,-9,97,97,97,97,-75,-65,97,97,97,97,]),'RSHIFT':([53,54,55,56,57,64,65,66,72,73,84,87,89,90,91,102,103,104,128,129,130,132,133,134,135,],[-8,-9,-10,-11,-12,98,98,-64,98,98,98,98,-10,-8,-9,98,98,98,98,-75,-65,98,98,98,98,]),'PERCENT':([53,54,55,56,57,64,65,66,72,73,84,87,89,90,91,102,103,104,128,129,130,132,133,134,135,],[-8,-9,-10,-11,-12,99,99,-64,99,99,99,99,-10,-8,-9,99,99,99,99,-75,-65,99,99,99,99,]),'EQ':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,107,107,-66,-67,-76,-75,-65,]),'NEQ':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,108,108,-66,-67,-76,-75,-65,]),'LT':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,109,109,-66,-67,-76,-75,-65,]),'GT':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,110,110,-66,-67,-76,-75,-65,]),'LE':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,111,111,-66,-67,-76,-75,-65,]),'GE':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,112,112,-66,-67,-76,-75,-65,]),'AND':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,113,113,-66,-67,-76,-75,-65,]),'OR':([53,54,55,56,57,66,72,73,103,104,128,129,130,],[-8,-9,-10,-11,-12,-64,114,114,-66,-67,-76,-75,-65,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'node_list':([0,46,47,131,140,],[1,74,75,141,145,]),'node':([1,74,75,141,145,],[2,2,2,2,2,]),'include':([1,74,75,141,145,],[3,3,3,3,3,]),'func_def':([1,74,75,141,145,],[4,4,4,4,4,]),'func_call':([1,24,74,75,141,145,],[5,52,5,5,5,5,]),'statement':([1,74,75,141,145,],[6,6,6,6,6,]),'control_expr':([1,74,75,141,145,],[7,7,7,7,7,]),'dtype':([1,25,51,59,63,74,75,81,83,141,145,],[9,58,78,82,88,9,9,122,88,9,9,]),'init_var':([1,59,74,75,141,145,],[11,80,11,11,11,11,]),'assign_var':([1,74,75,141,145,],[12,12,12,12,12,]),'declare_var':([1,74,75,141,145,],[13,13,13,13,13,]),'increment':([1,74,75,141,145,],[14,14,14,14,14,]),'control':([1,74,75,141,145,],[15,15,15,15,15,]),'for_loop':([1,74,75,141,145,],[16,16,16,16,16,]),'init_var_ls':([1,59,74,75,141,145,],[24,24,24,24,24,24,]),'modifier':([1,59,74,75,141,145,],[25,81,25,25,25,25,]),'assign':([10,38,79,123,139,],[41,62,120,62,120,]),'init_var_rs':([24,],[48,]),'literal':([24,41,45,63,67,68,69,80,83,92,106,115,118,],[49,66,66,66,66,66,66,66,66,66,66,66,136,]),'func_arglist':([40,60,],[63,83,]),'expression':([41,45,63,67,68,69,80,83,92,106,115,],[65,73,87,102,103,104,73,87,128,133,134,]),'conditional_expr':([45,80,],[71,121,]),'func_arg':([63,83,],[86,86,]),'binop':([64,65,72,73,84,87,102,103,104,128,132,133,134,135,],[92,101,92,101,92,101,101,101,101,101,92,101,101,92,]),'conditional':([72,73,],[106,115,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> node_list","S'",1,None,None,None),
  ('node_list -> <empty>','node_list',0,'p_node_list','ply_tokenizer.py',165),
  ('node_list -> node_list node','node_list',2,'p_node_list','ply_tokenizer.py',166),
  ('node -> include','node',1,'p_node','ply_tokenizer.py',175),
  ('node -> func_def','node',1,'p_node','ply_tokenizer.py',176),
  ('node -> func_call','node',1,'p_node','ply_tokenizer.py',177),
  ('node -> statement','node',1,'p_node','ply_tokenizer.py',178),
  ('node -> control_expr','node',1,'p_node','ply_tokenizer.py',179),
  ('literal -> FLOAT','literal',1,'p_literal','ply_tokenizer.py',184),
  ('literal -> INT','literal',1,'p_literal','ply_tokenizer.py',185),
  ('literal -> CHAR','literal',1,'p_literal','ply_tokenizer.py',186),
  ('literal -> STRING','literal',1,'p_literal','ply_tokenizer.py',187),
  ('literal -> NONDECIMAL','literal',1,'p_literal','ply_tokenizer.py',188),
  ('assign -> SIMPLE_ASSIGN','assign',1,'p_assign','ply_tokenizer.py',192),
  ('assign -> COMPLEX_ASSIGN','assign',1,'p_assign','ply_tokenizer.py',193),
  ('dtype -> CHAR','dtype',1,'p_dtype','ply_tokenizer.py',197),
  ('dtype -> DOUBLE','dtype',1,'p_dtype','ply_tokenizer.py',198),
  ('dtype -> FLOAT','dtype',1,'p_dtype','ply_tokenizer.py',199),
  ('dtype -> INT','dtype',1,'p_dtype','ply_tokenizer.py',200),
  ('dtype -> VOID','dtype',1,'p_dtype','ply_tokenizer.py',201),
  ('dtype -> UINT8_T','dtype',1,'p_dtype','ply_tokenizer.py',202),
  ('dtype -> UINT16_T','dtype',1,'p_dtype','ply_tokenizer.py',203),
  ('dtype -> dtype ASTERISK','dtype',2,'p_dtype','ply_tokenizer.py',204),
  ('modifier -> CONST','modifier',1,'p_modifier','ply_tokenizer.py',208),
  ('modifier -> EXTERN','modifier',1,'p_modifier','ply_tokenizer.py',209),
  ('modifier -> INLINE','modifier',1,'p_modifier','ply_tokenizer.py',210),
  ('modifier -> LONG','modifier',1,'p_modifier','ply_tokenizer.py',211),
  ('modifier -> SHORT','modifier',1,'p_modifier','ply_tokenizer.py',212),
  ('modifier -> SIGNED','modifier',1,'p_modifier','ply_tokenizer.py',213),
  ('modifier -> UNSIGNED','modifier',1,'p_modifier','ply_tokenizer.py',214),
  ('modifier -> VOLATILE','modifier',1,'p_modifier','ply_tokenizer.py',215),
  ('include -> INCLUDE','include',1,'p_include','ply_tokenizer.py',225),
  ('control -> WHILE','control',1,'p_controls','ply_tokenizer.py',234),
  ('control -> IF','control',1,'p_controls','ply_tokenizer.py',235),
  ('control -> ELSE','control',1,'p_controls','ply_tokenizer.py',236),
  ('conditional -> EQ','conditional',1,'p_conditionals','ply_tokenizer.py',242),
  ('conditional -> NEQ','conditional',1,'p_conditionals','ply_tokenizer.py',243),
  ('conditional -> LT','conditional',1,'p_conditionals','ply_tokenizer.py',244),
  ('conditional -> GT','conditional',1,'p_conditionals','ply_tokenizer.py',245),
  ('conditional -> LE','conditional',1,'p_conditionals','ply_tokenizer.py',246),
  ('conditional -> GE','conditional',1,'p_conditionals','ply_tokenizer.py',247),
  ('conditional -> AND','conditional',1,'p_conditionals','ply_tokenizer.py',248),
  ('conditional -> OR','conditional',1,'p_conditionals','ply_tokenizer.py',249),
  ('conditional_expr -> ID conditional expression','conditional_expr',3,'p_conditional_expr','ply_tokenizer.py',253),
  ('conditional_expr -> expression conditional ID','conditional_expr',3,'p_conditional_expr','ply_tokenizer.py',254),
  ('conditional_expr -> expression conditional expression','conditional_expr',3,'p_conditional_expr','ply_tokenizer.py',255),
  ('conditional_expr -> ID conditional ID','conditional_expr',3,'p_conditional_expr','ply_tokenizer.py',256),
  ('for_loop -> FOR LPAREN init_var conditional_expr SEMI ID INCREMENT RPAREN','for_loop',8,'p_for_loop','ply_tokenizer.py',260),
  ('control_expr -> control LPAREN conditional_expr RPAREN LBRACE node_list RBRACE','control_expr',7,'p_control_expr','ply_tokenizer.py',264),
  ('control_expr -> control LBRACE node_list RBRACE','control_expr',4,'p_control_expr','ply_tokenizer.py',265),
  ('control_expr -> for_loop LBRACE node_list RBRACE','control_expr',4,'p_control_expr','ply_tokenizer.py',266),
  ('func_arg -> ID','func_arg',1,'p_func_arg','ply_tokenizer.py',276),
  ('func_arg -> expression','func_arg',1,'p_func_arg','ply_tokenizer.py',277),
  ('func_arg -> dtype ID','func_arg',2,'p_func_arg','ply_tokenizer.py',278),
  ('func_arg -> dtype','func_arg',1,'p_func_arg','ply_tokenizer.py',279),
  ('func_arglist -> <empty>','func_arglist',0,'p_func_arglist','ply_tokenizer.py',287),
  ('func_arglist -> func_arglist func_arg','func_arglist',2,'p_func_arglist','ply_tokenizer.py',288),
  ('func_arglist -> func_arglist func_arg COMMA','func_arglist',3,'p_func_arglist','ply_tokenizer.py',289),
  ('func_def -> dtype ID LPAREN func_arglist RPAREN LBRACE node_list RBRACE','func_def',8,'p_func_def','ply_tokenizer.py',305),
  ('func_call -> ID LPAREN func_arglist RPAREN SEMI','func_call',5,'p_func_call','ply_tokenizer.py',315),
  ('statement -> init_var','statement',1,'p_statement_assign','ply_tokenizer.py',325),
  ('statement -> assign_var','statement',1,'p_statement_assign','ply_tokenizer.py',326),
  ('statement -> declare_var','statement',1,'p_statement_assign','ply_tokenizer.py',327),
  ('statement -> increment','statement',1,'p_statement_assign','ply_tokenizer.py',328),
  ('expression -> literal','expression',1,'p_expression_literal','ply_tokenizer.py',332),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','ply_tokenizer.py',337),
  ('expression -> NEGATE expression','expression',2,'p_expression_bitw_neg','ply_tokenizer.py',341),
  ('expression -> MINUS expression','expression',2,'p_expression_bitw_neg','ply_tokenizer.py',342),
  ('binop -> PLUS','binop',1,'p_binops','ply_tokenizer.py',346),
  ('binop -> MINUS','binop',1,'p_binops','ply_tokenizer.py',347),
  ('binop -> ASTERISK','binop',1,'p_binops','ply_tokenizer.py',348),
  ('binop -> DIVIDE','binop',1,'p_binops','ply_tokenizer.py',349),
  ('binop -> LSHIFT','binop',1,'p_binops','ply_tokenizer.py',350),
  ('binop -> RSHIFT','binop',1,'p_binops','ply_tokenizer.py',351),
  ('binop -> PERCENT','binop',1,'p_binops','ply_tokenizer.py',352),
  ('expression -> expression binop ID','expression',3,'p_expression_binop','ply_tokenizer.py',356),
  ('expression -> ID binop expression','expression',3,'p_expression_binop','ply_tokenizer.py',357),
  ('increment -> ID INCREMENT SEMI','increment',3,'p_expression_increment','ply_tokenizer.py',361),
  ('declare_var -> dtype ID SEMI','declare_var',3,'p_decl_var','ply_tokenizer.py',383),
  ('declare_var -> modifier dtype ID SEMI','declare_var',4,'p_decl_var','ply_tokenizer.py',384),
  ('init_var_ls -> modifier dtype ID assign','init_var_ls',4,'p_init_var_ls','ply_tokenizer.py',392),
  ('init_var_ls -> dtype ID assign','init_var_ls',3,'p_init_var_ls','ply_tokenizer.py',393),
  ('init_var_rs -> literal SEMI','init_var_rs',2,'p_init_var_rs','ply_tokenizer.py',400),
  ('init_var_rs -> ID SEMI','init_var_rs',2,'p_init_var_rs','ply_tokenizer.py',401),
  ('init_var_rs -> LPAREN dtype RPAREN literal SEMI','init_var_rs',5,'p_init_var_rs','ply_tokenizer.py',402),
  ('init_var_rs -> LPAREN dtype RPAREN ID SEMI','init_var_rs',5,'p_init_var_rs','ply_tokenizer.py',403),
  ('init_var_rs -> func_call','init_var_rs',1,'p_init_var_rs','ply_tokenizer.py',404),
  ('init_var -> init_var_ls init_var_rs','init_var',2,'p_init_var','ply_tokenizer.py',415),
  ('assign_var -> ID assign expression SEMI','assign_var',4,'p_assign_var','ply_tokenizer.py',423),
]
