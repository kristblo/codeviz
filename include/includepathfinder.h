#ifndef INCLUSIONFINDER_H
#define INCLUSIONFINDER_H

#include <iostream> //TODO: Find and remove unnecessary instances of iostream
#include <regex>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
//#include <filesystem>
//#include <experimental/filesystem>
#include "filewriter.h"
#include "fileopener.h"
#include "filefinder.h"


#define str std::string
#define vec std::vector

//TODO: make everything but calcProjIncData and getters private
class IncludePathFinder{
private:
    vec<vec<bool>> inclusionMatrix;

    std::map<str, vec<str>> fullIncludePathsPerFile;
    std::map<str, vec<str>> danglingIncludesPerFile;

    str incLog = "../logfiles/inclog.txt";
    str includePattern = "#include ([\'\"<](\\w|[\\.\\/])*[\'\">])";//TODO: make config file
    vec<str> fileTypes = {"c", "cpp", "h"};

//public:


    /// @brief Finds all include statements in a file
    /// @param fileString std::string of input file
    /// @return name and suffix of included files
    vec<str> findIncludeStatements(str fileString);
    
    /// @brief Searches a file tree to find paths to all included files
    /// @param currentFilePath The current file being investigated
    /// @param fileList File paths which may contain a relevant file
    /// @param fullPathsHere Return: successfully found files
    /// @param danglersHere Return: unsuccessfully found files
    void findFullIncludePathsInFile(str currentFilePath, 
                                    vec<str> fileList,
                                    vec<str>& fullPathsHere,
                                    vec<str>& danglersHere);
    
    void trimIrrelevantFiles(vec<str>& fileList);

public:
    /// @brief Finds includes in tree and calculates inclusion matrix for project
    /// @param topDir Top dir from which to search
    /// @param exclDirs Dirs which are to be excluded/ignored from the search
    void calculateProjectInclusionData(str topDir, vec<str> exclDirs);
 
    vec<vec<bool>> getInclusionMatrix();    

    std::map<str, vec<str>> getIncludesPerFile();
    std::map<str, vec<str>> getDanglersPerFile();


    IncludePathFinder();
    
};

#endif //INCLUSIONFINDER_H