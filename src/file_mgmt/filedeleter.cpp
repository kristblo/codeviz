#include "filedeleter.h"

void delete_file(std::string filename)
{
    if(!std::filesystem::is_directory(filename))
    {
        std::cout << "Deleting: " << filename << std::endl;
        if(remove(filename.c_str()) != 0)
        {
            std::cerr << "Failed to delete file: " << filename << std::endl;
        }
    }
    else{
        std::cerr << "File was not file, but directory: " << filename << std::endl;
    }
}

void delete_files_in_dir(const char* dir)
{

    DIR* directory = opendir(dir);

    if(directory != nullptr)
    {
        dirent* entry;

        while((entry = readdir(directory)) != nullptr)
        {
            if(strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            {
                continue;
            }
            std::string file_path = std::string(dir) + "/" + entry->d_name; //TODO: OS check

            delete_file(file_path);
        }
        closedir(directory);
    }
}

void delete_files_in_tree(std::string topDir)
{
    std::vector<std::string> files;
    find_files_recursively(topDir, files);
    for(auto file: files)
    {
        delete_file(file);
    }
}