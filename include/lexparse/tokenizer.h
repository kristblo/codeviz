#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <iostream>
#include <string>
#include <regex>
#include <utility>

class Token{
public:
    std::string type;
    std::string value;
    int line;
    int column;
};

class Tokenizer{
public:
    std::string tokens_pattern;

    std::vector<std::pair<std::string, std::string>> tokens = 
    {
        {"LCOMMENT","\\/\\*(.|\\n)*?\\*\\/"},
        {"COMMENT", "\\/\\/[^\\n]*"},
        {"COMPLEX_ASSIGN", "(&=)|(\\|=)|(\\^=)|(%=)|(\\*=)|(\\/=)|(\\+=)|(-=)"},
        {"ID","[a-zA-Z_][a-zA-Z0-9_]*"},
        {"AND","&&"},
        {"OR", "\\|\\|"},
        {"MEMBER","(->)|(\\.)"},
        {"FLOAT_L","\\d+\\.\\d+"},
        {"INT_L","\\d+"}, //Int literal; literally an int
        {"STRING_L",  "\"[^\"]*\""},
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
        {"SEMI",";"},
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
        {"IFNDEF","\\#ifndef\\s+\\w+"},
        {"ENDIF","\\#endif"},        
        {"LSHIFT","<<"},
        {"RSHIFT",">>"},
        {"INCREMENT","\\+\\+"},
        {"NONDECIMAL_L","0[xXbB][0-9a-fA-F]+"},
        {"DEFINE", "\\#define([\\t\\f ]+\\w+)+"},
        {"INCLUDE", "\\#include\\s*(\"|<).*?(>|\")"},
        //{"newline", "\\n"},
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
    std::string compile_pattern();
    std::vector<std::string> tokenize(std::string input);

    Tokenizer();

};

#endif //TOKENIZER_H