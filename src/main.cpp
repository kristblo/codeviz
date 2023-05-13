#include <iostream>
#include <thread>
#include "parsernodetypes.h"
#include "fileopener.h"
#include "filefinder.h"
#include "filewriter.h"
#include "filedeleter.h"
#include "tokenizer.h"              
#include "includepathfinder.h"

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
    #if(0)
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

    //Incpathfinder test
    #if(0)
    IncludePathFinder includePathFinder;
    for(std::string file: found_files)
    {
        std::string contents = readFileIntoString(file);
        includePathFinder.findIncludeStatements(contents);
        includePathFinder.findFullIncludePaths(file, found_files);

    }

    #endif
    
    //Full project inclusion test
    #if(1)
    std::string topDir = "/home/kristian/byggern-nicer_code";
    std::vector<std::string> exclDirs = {".vs", "sam", "build", "logfiles", ".vscode", ".git", "python"};
    IncludePathFinder includePathFinder;
    includePathFinder.calculateProjectInclusionData(topDir, exclDirs);
    std::map<str, vec<str>> incs = includePathFinder.getIncludesPerFile();
    std::map<str, vec<str>> danglers = includePathFinder.getDanglersPerFile();
    for(auto parent: incs)
    {
        std::cout << parent.first << " includes:\n";
        for(str child: incs[parent.first])
        {
            std::cout << '\t' << child << std::endl;
        }
        for(str child: danglers[parent.first])
        {
            std::cout << '\t' << child << std::endl;
        }
        std::cout << std::endl;
    }
    vec<vec<bool>> incMat = includePathFinder.getInclusionMatrix();
    std::string incMatString;
    for(auto row: incMat)
    {
        std::string rowstr;
        for(bool el: row)
        {
            std::cout << el;
            rowstr.append(el?"1":"0");
        }
        std::cout << std::endl;
        //write_line_to_file("../logfiles/incmat.txt", rowstr);
        incMatString.append(rowstr+'\n');
    }
    incMatString.pop_back();
    write_to_file("../logfiles/incmat.txt", incMatString);
    
    std::string allFilesString;
    for(auto file: incs)
    {
        //write_line_to_file("../logfiles/projectFiles.txt", file.first);
        allFilesString.append(file.first+'\n');
    }
    allFilesString.pop_back();
    write_to_file("../logfiles/projectFiles.txt", allFilesString);
    
    std::set<str> allDanglers = includePathFinder.getDanglersInProject();
    std::string allDanglersString;
    for(auto file: allDanglers)
    {
        //write_line_to_file("../logfiles/projectDanglers.txt", file);
        allDanglersString.append(file+'\n');
    }
    allDanglersString.pop_back();
    write_to_file("../logfiles/projectDanglers.txt", allDanglersString);

    #endif

    return 0;
}