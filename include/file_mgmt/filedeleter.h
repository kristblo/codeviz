#ifndef FILEDELETER_H
#define FILEDELETER_H

#include <iostream>
#include <dirent.h>
#include <cstring>
#include <filesystem>
#include "filefinder.h"

void delete_files_in_dir(const char* dir);

void empty_dir_filesys(std::string dir);

void delete_files_in_tree(std::string topDir);

void delete_file(std::string filename);

#endif //FILEDELETER_H