#ifndef FILEPARSER_H
#define FILEPARSER_H

#include <string>
#include <vector>

#include "parsernodetypes.h"
#include "tokenizer.h"

class FileParser{
private:
    std::vector<ParserNode> mParserNodes;
    std::vector<int> currentScope;
    std::vector<ScopeNode> mScopeNodes;
    
    Tokenizer mTokenizer;

    //Patterns

    //Actions
    
public:
    void parseFile(std::string aFileToParse);
    FileParser();

};


#endif //FILEPARSER_H