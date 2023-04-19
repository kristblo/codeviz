#ifndef FILEFINDER_H
#define FILEFINDER_H

#include <iostream>
#include <filesystem>
#include <unordered_set>
#include <vector>

namespace fs = std::filesystem;

void find_files(const fs::path& top_dir, 
                const std::unordered_set<std::string>& excl_dirs,
                std::vector<std::string>& output);


#endif //FILEFINDER_H