#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <iostream>
#include <string>
#include <regex>
#include "filewriter.h"


/// @brief Represents a symbol in a C/C++ file
class Token{
public:
    std::string type;
    std::string value;
    int line;
    
    /// @brief Scope identificator for the token. Indeces represent depth, value is lineno
    std::vector<int> scope;

    Token(std::string aType, std::string aValue, int aLine, std::vector<int> aScope);
};


/// @brief Finds and stores tokens from an input string
class Tokenizer{
public:

    /// @brief Tokens found while tokenizing
    std::vector<Token> tokens;
    
    //State variables for use during tokenization
    
    /// @brief String containing composite regexpr of all tokens
    std::string tokens_pattern;
    
    /// @brief Linecount in input strin
    int lineno = 1;

    /// @brief Latest regex hit and match group
    std::pair<std::string, std::string> currentHit;

    /// @brief Latest regex hit
    std::string currentRaw;
    
    std::vector<int> currentScope = {0};

    /// @brief All tokens: type and corresponding regexpr. Ordered by priority
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
        {"DEFDTYPE", "[a-zA-Z_][a-zA-Z0-9_]*_t"},
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

    /// @brief Reserved words in C/C++
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

    /// @brief Register of actions to take when encountering specific tokens, inspired by PLY
    std::map<std::string, void(Tokenizer::*)()> token_actions =    
    {
        {"LCOMMENT", &Tokenizer::action_LCOMMENT},
        {"COMMENT", &Tokenizer::action_COMMENT},
        {"NEWLINE", &Tokenizer::action_NEWLINE},
        {"ID", &Tokenizer::action_ID},
        {"LBRACE", &Tokenizer::action_LBRACE},
        {"RBRACE", &Tokenizer::action_RBRACE},
        //{"DEFDTYPE", &Tokenizer::action_DEFDTYPE},
    };


    void action_LCOMMENT();
    void action_COMMENT();
    void action_NEWLINE();
    void action_ID();
    void action_LBRACE();
    void action_RBRACE();
    //void action_DEFDTYPE();

    /// @brief Compiles the complete regexpr for finding tokens
    /// @return String of composite regexpr
    std::string compile_pattern();

    /// @brief Do the thing
    /// @param input Any string, nominally a .c/.cpp/.h file
    void tokenize(std::string input);

    Tokenizer();

};

#endif //TOKENIZER_H