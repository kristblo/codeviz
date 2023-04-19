#include "filefinder.h"

void find_files(const fs::path& top_dir, 
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
                find_files(p.path(), excl_dirs, output);
            }
        }
    }
}