#include <iostream>
#include <thread>
#include "parsernodetypes.h"
#include "fileopener.h"
#include "filefinder.h"
#include "filewriter.h"
#include "filedeleter.h"
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
    std::unordered_set<std::string> excl_dirs = {".vs", "sam", "build", "logfiles", ".vscode"};
    std::vector<std::string> found_files;

    find_files_recursively("/home/kristian/byggern-nicer_code", excl_dirs, found_files);
    for(std::string s : found_files)
    {
        //std::cout << s << std::endl;
        write_line_to_file("filesfound.txt", s);

    }

    //Pre-tokenization cleanup
    delete_files_in_tree("../logfiles");
    //Test tokenizer for the full project
    #if(0)
    for(std::string file: found_files)
    {
        std::cout << "Currently tokenizing: " << file << std::endl;
        std::string alteredName = file;
        std::replace(alteredName.begin(), alteredName.end(), '/', '_');
        std::string outputfolder = "../logfiles/tokenizer_output/";
        std::string outputfile = outputfolder + "tokenized_" + alteredName + ".txt";
        std::string contents = readFileIntoString(file);
        Tokenizer tokenizer;        
        tokenizer.tokenize(contents);
        for(auto& token: tokenizer.tokens)   
        {
            std::string s = token.type + ", " + token.value + ", " + std::to_string(token.line);
            write_line_to_file(outputfile, s);
        }
    }
    #endif

    //Multithreaded execution
    #if(1)
    std::vector<std::pair<std::string, std::thread>> tok_threads;
    for(std::string file: found_files)
    {           
        std::string cleanFileName = file;
        std::replace(cleanFileName.begin(), cleanFileName.end(), '/', '_');
        
        std::string outputDir = "../logfiles/tokenizer_output/";
        std::string outputFile = outputDir + "tokenized_" + cleanFileName + ".txt";
        std::string contents = readFileIntoString(file);

        tok_threads.push_back(
            {file,
            std::thread(
            [](std::string contentsToTokenize){                
                Tokenizer tokenizer;
                tokenizer.tokenize(contentsToTokenize);
            }, contents)
            }
        );
        //std::cout << "Tokenization of " << tok_threads.back().first << " started" << std::endl;


    }
    for(auto& tok_thread: tok_threads)
    {        
        tok_thread.second.join();
        std::cout << "Tokenization of " << tok_thread.first << " complete" << std::endl;
    }
    #endif

    return 0;
}