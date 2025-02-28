#include <iostream>
#include <thread>
#include <map>

#include "parsernodetypes.h"
#include "fileopener.h"
#include "filefinder.h"
#include "filewriter.h"
#include "filedeleter.h"
#include "tokenizer.h"              
#include "includepathfinder.h"

//CTAGS includes
#include "tagobject.h"
#include "stringtotags.h"
#include "tagfileparser.h"
#include "moduleobject.h"
#include "classtag.h"
#include "headertag.h"
#include "functionobject.h"
#include "classobject.h"

int main(int argc, char** argv){
    std::cout << "Hello, world!" << std::endl;

#if(0)

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
#endif

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
            [](std::string contentsToTokenize, std::string outputFileName){                
                Tokenizer tokenizer;
                tokenizer.tokenize(contentsToTokenize);

                for(auto& token: tokenizer.tokens)
                {
                    std::string scopestr;
                    for(int el: token.scope)
                    {
                        scopestr.append(std::to_string(el));
                        scopestr.append(".");
                    }
                    scopestr.pop_back();
                    std::string s = token.type + ", " + token.value + ", " + std::to_string(token.line) + ", " + scopestr;
                    write_line_to_file(outputFileName, s);
                }
                
            }, contents, outputFile)
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
#if(0)
    //std::string topDir = "/home/kristian/Project_codeviz_cpp";
    std::string topDir = argv[1];
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

#if(1)
  //CTAGS test: find inclusions from ctags tagfile
  //string inputFileName = "../tagfiles/tags_codeviz"; //debug only
  string inputFileName = argv[1];
  string tagFileDump = readFileIntoString(inputFileName);
  
  TagFileParser parserTest = TagFileParser(tagFileDump);
  parserTest.parseTagFile();
  std::vector<SplitTagString> splitTagStrings = parserTest.getSplitTagStrings();

  std::cout << splitTagStrings.size() << std::endl;
  std::cout << splitTagStrings[splitTagStrings.size() - 1].getTagHeader() << std::endl;
  
  std::vector<TagItemsAsStrings> itemsTest = parserTest.getItemStrings();

  std::vector<TagObject> tagObjects;
  for(auto item : itemsTest)
  {
    TagObject tagObject = TagObject(item.getTagHeaderItems()[0],
                                    item.getTagHeaderItems()[1],
                                    item.getTagHeaderItems()[2],
                                    item.getTagFieldItems());
    tagObjects.push_back(tagObject);
  }

  int headerCount = 0;
  for(auto tag : tagObjects)
  {
    if(tag.getTagFields()["kind"] == "header")
    {
      std::cout << tag << "\n" << std::endl;
      headerCount++;
    }
  }
  std::cout << "Number of headers: " << headerCount << std::endl;

  /////////////////
  //FILES/MODULES//
  /////////////////
  
  //Find all files/modules relevant to the project based on ctags
  //TODO: move to tagfileparser
  std::map<std::string, ModuleObject> projectModulesStringMap;
  for(auto tag : tagObjects)
  {
    //Shorten execution time by only using file tags?
    if(tag.getTagFields()["kind"] == "file")
    {
      std::string tagFile = tag.getTagFile();
      std::string fileBaseName = std::filesystem::path(tagFile).stem().string();
      projectModulesStringMap.try_emplace(fileBaseName, ModuleObject(fileBaseName));

    
      std::string fileFullname = std::filesystem::path(tagFile).string();

      //Using .at() instead of [] to avoid attempting to create an object if the module is 
      //not already listed
      std::vector<std::string> currentSourceFiles = projectModulesStringMap.at(fileBaseName).getSourceFiles();
      auto iterator = std::find(currentSourceFiles.begin(),
                              currentSourceFiles.end(),
                              fileFullname);
      if(iterator == currentSourceFiles.end())
      {
        projectModulesStringMap.at(fileBaseName).addSourceFile(fileFullname);
      }
    }
  }

  for(auto filename : projectModulesStringMap)
  {
    std::cout << filename.second.getModuleName() << std::endl;
    for(std::string sourcefile : filename.second.getSourceFiles())
    {
      std::cout << sourcefile << std::endl;
    }
  }

  ////////////
  //INCLUDES//
  ////////////
  
  //Check all header tags and add to modules map; build includes
  vec<HeaderTag> headerTags;
  for(auto tag : tagObjects)
  {
    if(tag.getTagKind() == "header")
    {
      HeaderTag test = HeaderTag(tag);

      std::string moduleName = std::filesystem::path(tag.getTagFile()).stem().string();
      std::string headerName = test.getHeaderName();
      if(headerName != moduleName)
      {
        projectModulesStringMap.at(moduleName).addIncludeString(headerName);
        try
        {
          projectModulesStringMap.at(moduleName).addIncludeModule(
                        &(projectModulesStringMap.at(headerName)));        
        }
        catch(const std::exception& e)
        {
          std::cerr << "Error: " << e.what() << " | Module \"" << headerName << "\" is probably external. Adding empty module." << '\n';
          projectModulesStringMap.try_emplace(headerName, ModuleObject(headerName, true));
        }
      }
    }
  }

  for(auto module : projectModulesStringMap)
  {
    std::cout << module.first << ":" << std::endl;
    for(auto inc : module.second.getIncludedModules())
    {
      if(!inc->isModuleExternal())
      {
      }
      std::cout << inc->getModuleName() << std::endl;
    }
    std::cout << std::endl; 
  }

  ///////////
  //CLASSES//
  ///////////
  for(auto tag : tagObjects)
  {
    if(tag.getTagKind() == "class")
    {
      ClassTag test = ClassTag(tag);
      std::string cleanaddress = tag.getTagName();
      std::cout << test << std::endl << std::endl;
    }
  }
  


#endif

    return 0;
}