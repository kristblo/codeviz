#include <iostream>
#include "parsernodetypes.h"

int main(int argc, char** argv){
    std::cout << "Hello, world!" << std::endl;
    ScopeNode testNode0 = ScopeNode({3,4,5}, 1, 2);
    std::cout << "ID: " << testNode0.getScopeID()[2] << std::endl;
    testNode0.setScopeEnd(6);
    std::cout << "end: " << testNode0.getScopeEnd() << std::endl;

    ParserNode parserLongInit = ParserNode(INCLUDE, &testNode0);
    std::cout << "Longinit type: " << parserLongInit.getParserNodeType() << std::endl;
    std::cout << "Longinit ID: " << parserLongInit.getScope()->getScopeID()[0] << std::endl;

    ParserNode parserShortInit = ParserNode(DEFINE);
    std::cout << "Shortinit type: " << parserShortInit.getParserNodeType() << std::endl;
    //std::cout << "Shortinit ID: " << parserShortInit.getScope() << std::endl;

    IncludeNode incNodeTest = IncludeNode("filename.h", "username.h", &testNode0);
    
    std::cout << "incnode value: " << incNodeTest.getValue() << std::endl;
    std::cout << "incnode user: " << incNodeTest.getUser() << std::endl;
    std::cout << "incnode type: " << incNodeTest.getParserNodeType() << std::endl;

    return 0;
}