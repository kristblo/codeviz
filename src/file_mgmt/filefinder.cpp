#include "filefinder.h"

void find_files_recursively(const fs::path& top_dir, 
                const std::unordered_set<std::string>& excl_dirs,
                std::vector<std::string>& output)
{
    for (auto p: fs::directory_iterator(top_dir))
    {
        if(fs::is_regular_file(p))
        {
            //std::cout << p.path() << std::endl;
            output.push_back(p.path());
        }
        else if(fs::is_directory(p))
        {
            if (excl_dirs.find(p.path().filename()) == excl_dirs.end()) 
            {
                find_files_recursively(p.path(), excl_dirs, output);
            }
        }
    }
}

void find_files_recursively(const fs::path &top_dir, std::vector<std::string> &output)
{
    for(auto p: fs::directory_iterator(top_dir))
    {
        if(fs::is_regular_file(p))
        {
            output.push_back(p.path());
        }
        else if (fs::is_directory(p))
        {
            find_files_recursively(p.path(), output);
        }        
    }
}
