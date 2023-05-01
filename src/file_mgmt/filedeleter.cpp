#include "filedeleter.h"

void delete_files_in_tree(std::string topDir)
{

    char directory_path[2048];
    strncpy(directory_path, topDir.c_str(), sizeof(directory_path));
    directory_path[sizeof(directory_path) -1] = 0;
    DIR* directory = opendir(directory_path);

    if(directory != nullptr)
    {
        dirent* entry;

        while((entry = readdir(directory)) != nullptr)
        {
            if(strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            {
                continue;
            }
            std::string file_path = std::string(directory_path) + "/" + entry->d_name; //TODO: OS check

            if(remove(file_path.c_str()) != 0)
            {
                std::cerr << "Failed to delete file: " << file_path << std::endl;
            }
        }
        closedir(directory);
    }
}