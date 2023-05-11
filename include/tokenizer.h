#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <iostream>
#include <string>
#include <regex>
#include "filewriter.h"


class Token{
public:
    std::string type;
    std::string value;
    int line;    

    Token(std::string aType, std::string aValue, int aLine);
};

class Tokenizer{
public:

    std::vector<Token> tokens;
    
    //State variables for use during tokenization
    std::string tokens_pattern;
    int lineno = 1;
    std::pair<std::string, std::string> currentHit;
    std::string currentRaw;

    std::vector<std::pair<std::string, std::string>> token_definitions = 
    {
        {"DEFINE", "\\#define([\\t\\f ]+\\w+)+"},
        {"INCLUDE", "\\#include\\s*(\"|<).*?(>|\")"},
        {"STRING_L",  "\"[^\"]*\""},
        {"LCOMMENT","\\/\\*(.|\\n)*?\\*\\/"},
        {"COMMENT", "\\/\\/[^\\n]*"},        
        {"NEWLINE", "\\n"}, 
        {"COMPLEX_ASSIGN", "(&=)|(\\|=)|(\\^=)|(%=)|(\\*=)|(\\/=)|(\\+=)|(-=)"},
        {"INCREMENT", "\\+\\+"},
        {"ID","[a-zA-Z_][a-zA-Z0-9_]*"},
        {"AND","&&"},
        {"OR", "\\|\\|"},
        {"MEMBER","(->)|(\\.)"},
        {"FLOAT_L","\\d+\\.\\d+"},
        {"INT_L","\\d+"}, //Int literal; literally an int
        {"CHAR_L","\'[^\']*\'"},
        {"PLUS","\\+"},
        {"MINUS","-"},
        {"ASTERISK","\\*"},
        {"DIVIDE","\\/"},
        {"LPAREN","\\("},
        {"RPAREN","\\)"},
        {"LBRACE","\\{"},
        {"RBRACE","\\}"},
        {"LBRACK","\\["},
        {"RBRACK","\\]"},
        {"LSHIFT","<<"},
        {"RSHIFT",">>"},
        {"EQ","=="},
        {"NEQ","!="},
        {"LT","<"},
        {"LE","<="},
        {"GT",">"},
        {"GE",">="},
        {"SIMPLE_ASSIGN", "="},
        {"NEGATE","~"},
        {"PERCENT","%"},
        {"BITAND","&"},
        {"BITOR","\\|"},
        {"COMMA",","},
        {"SEMI",";"},
        {"IFNDEF","\\#ifndef\\s+\\w+"},
        {"ENDIF","\\#endif"},                
        {"NONDECIMAL_L","0[xXbB][0-9a-fA-F]+"},
    };

    std::map<std::string, std::string> reserved_words =
    {
        {"AUTO","auto"}, //Reserved starts here
        {"BREAK","break"},
        {"CASE","case"},
        {"CHAR","char"},
        {"CONST","const"},
        {"CONTINUE","continue"},
        {"DEFAULT","default"},
        {"DO","do"},
        {"DOUBLE","double"},
        {"ELSE","else"},
        {"ENUM","enum"},
        {"EXTERN","extern"},
        {"FLOAT","float"},
        {"FOR","for"},
        {"GOTO","goto"},
        {"IF","if"},
        {"INLINE","inline"},
        {"INT","int"},
        {"LONG","long"},
        {"PROGMEM","progmem"},
        {"REGISTER","register"},
        {"RESTRICT","restrict"},
        {"RETURN","return"},
        {"SHORT","short"},
        {"SIGNED","signed"},
        {"SIZEOF","sizeof"},
        {"STATIC","static"},
        {"STRUCT","struct"},
        {"SWITCH","switch"},
        {"TYPEDEF","typedef"},
        {"UNION","union"},
        {"UNSIGNED","unsigned"},
        {"VOID","void"},
        {"VOLATILE","volatile"},
        {"WHILE","while"},

    };

    std::map<std::string, void(Tokenizer::*)()> token_actions =    
    {
        {"LCOMMENT", &Tokenizer::action_LCOMMENT},
        {"COMMENT", &Tokenizer::action_COMMENT},
        {"NEWLINE", &Tokenizer::action_NEWLINE},
        {"ID", &Tokenizer::action_ID},
    };

    void action_LCOMMENT();
    void action_COMMENT();
    void action_NEWLINE();
    void action_ID();


    std::string compile_pattern();
    void tokenize(std::string input);

    Tokenizer();

};

#endif //TOKENIZER_H