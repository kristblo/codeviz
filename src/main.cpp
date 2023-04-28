#include <iostream>
#include "parsernodetypes.h"
#include "fileopener.h"
#include "filefinder.h"
#include "filewriter.h"
#include "tokenizer.h"              

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

    std::string filename = "/home/kristian/byggern-nicer_code/misc.c";
    std::string file_contents = readFileIntoString(filename);

    //std::cout << file_contents << endl;

    fs::path top_dir = "/home/kristian/byggern-nicer_code";
    std::unordered_set<std::string> excl_dirs = {".vs", "sam", "build", "logfiles"};
    std::vector<std::string> found_files;

    find_files("/home/kristian/byggern-nicer_code", excl_dirs, found_files);
    for(std::string s : found_files)
    {
        std::cout << s << std::endl;
        write_line_to_file("filesfound.txt", s);
    }

    Tokenizer tokenizer;
    std::vector<std::string> tokentest = tokenizer.tokenize(file_contents);
    std::cout << tokenizer.tokens_pattern << std::endl;
    for(std::string tok: tokentest)
    {
        write_line_to_file("tokenizertest.txt", tok);
    }

    return 0;
}