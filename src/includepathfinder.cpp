#include "includepathfinder.h"


vec<str> IncludePathFinder::findIncludeStatements(str fileString)
{
    vec<str> includeStatements;
    std::regex re(includePattern);

    vec<str> matches{
        std::sregex_token_iterator(fileString.begin(), fileString.end(), re),{}
    };

    vec<char> erasees = {'<','>','\'','\"'};
    for(auto& match: matches)
    {
        match.erase(match.begin(), match.begin()+9); //size("#include ")=9
        for(char c: erasees)
        {

            match.erase(std::remove(match.begin(), match.end(), c), match.end());
        }
        //std::cout << match << std::endl;
        includeStatements.push_back(match);        
    }

    return includeStatements;

}

void IncludePathFinder::findFullIncludePathsInFile(str currentFilePath, 
                                                   vec<str> fileList,
                                                   vec<str>& fullPathsHere,
                                                   vec<str>& danglersHere)
{
    str fileString = readFileIntoString(currentFilePath);
    vec<str> incStatements = findIncludeStatements(fileString);
    vec<str> fullIncludePaths;
    vec<str> danglingIncludes;

    for(str include: incStatements)
    {
        vec<str> candidates;
        std::string pattern = std::filesystem::path(include).filename().string();
        std::string outputString;

        for(str file: fileList)
        {
            std::string fileBaseName = std::filesystem::path(file).filename().string();
            if(fileBaseName == pattern)
            {
                candidates.push_back(file);
            }
            else
            {
                outputString = "No match";
            }
            
        }

        if(candidates.size() == 0)
        {
            outputString = "No candidates for " + include + " in " 
                         + currentFilePath + '\n';
            write_line_to_file(incLog, outputString);
            danglingIncludes.push_back(include);
        }
        else if (candidates.size() == 1)
        {
            fullIncludePaths.push_back(candidates[0]);
            outputString = "Single candidate for " + include + " in "
                         + currentFilePath + ":\n" + candidates[0] + "\n\n";
            write_line_to_file(incLog, outputString);
        }
        else
        {
            int shortestDist = 1000;
            str bestCandidate;
            for(str candidate: candidates)
            {
                int dist = calculate_distance_between_files(currentFilePath, candidate);
                if(dist < shortestDist)
                {
                    bestCandidate = candidate;
                    shortestDist = dist;
                }                
            }
            fullIncludePaths.push_back(bestCandidate);
            str op = "Multiple candidates for: " + currentFilePath + ": "
                    + include + ":\n";
            write_line_to_file(incLog, op);
            for(str candidate: candidates)
            {
                write_line_to_file(incLog, candidate);
            }
            op = "Selected: " + bestCandidate + '\n';
            write_line_to_file(incLog, op);
        }

    }
    fullPathsHere = fullIncludePaths;
    danglersHere = danglingIncludes;

}

void IncludePathFinder::trimIrrelevantFiles(vec<str>& fileList)
{
    str pattern = "^.*\\.(";

    for(str type: fileTypes)
    {
        pattern.append(type+"|");
    }
    pattern.pop_back();
    pattern.append(")");
    std::regex re(pattern);    
    for(int i = 0; i < fileList.size(); i++)
    {
        if(!std::regex_match(fileList[i], re))
        {
            fileList.erase(fileList.begin()+i);
        }
    }
}

void IncludePathFinder::calculateProjectInclusionData(str topDir, vec<str> exclDirs)
{
    std::unordered_set<std::string> exclDirsSet;
    for(str dir: exclDirs)
    {
        exclDirsSet.emplace(dir);
    }
    vec<str> allKnownFiles;
    find_files_recursively(topDir, exclDirsSet, allKnownFiles);    
    trimIrrelevantFiles(allKnownFiles);

    for(str file: allKnownFiles)
    {   
        vec<str> fullIncludesHere;
        vec<str> danglersHere;
        this->findFullIncludePathsInFile(file, allKnownFiles, 
                                         fullIncludesHere, danglersHere);
        fullIncludePathsPerFile[file] = fullIncludesHere;
        danglingIncludesPerFile[file] = danglersHere;        
        
    }    

    //Catalogue of dangling includes across project
    for(auto file: danglingIncludesPerFile)
    {
        for(str dangler: file.second)
        {
            danglingIncludesInProject.insert(dangler);
        }
    }    

    //Generate inclusion matrix
    int numKnownFiles = fullIncludePathsPerFile.size();
    int numDanglers = danglingIncludesInProject.size();
    for(auto file: fullIncludePathsPerFile)
    {
        vec<str> includesInThis = fullIncludePathsPerFile[file.first];
        vec<str> danglersInThis = danglingIncludesPerFile[file.first];
        vec<bool> matrixRow(numKnownFiles+numDanglers, 0);
        
        auto f_iterator = fullIncludePathsPerFile.begin();
        for(int i = 0; i < numKnownFiles; i++)
        {
            if(std::find(includesInThis.begin(), includesInThis.end(), 
               (*f_iterator).first) != includesInThis.end())
            {
                matrixRow[i] = 1;
            }
            f_iterator++;
        }

        auto d_iterator = danglingIncludesInProject.begin();
        for(int i = 0; i < numDanglers; i++)
        {
            if(std::find(danglersInThis.begin(), danglersInThis.end(),
               *d_iterator) != danglersInThis.end())
            {
                matrixRow[numKnownFiles + i] = 1;
            }
            d_iterator++;
        }

        inclusionMatrix.push_back(matrixRow);
    }    
}

vec<vec<bool>> IncludePathFinder::getInclusionMatrix()
{
    return inclusionMatrix;
}

std::map<str, vec<str>> IncludePathFinder::getIncludesPerFile()
{
    return fullIncludePathsPerFile;
}

std::map<str, vec<str>> IncludePathFinder::getDanglersPerFile()
{
    return danglingIncludesPerFile;
}

std::set<str> IncludePathFinder::getDanglersInProject()
{
    return danglingIncludesInProject;
}

IncludePathFinder::IncludePathFinder()
{

}
