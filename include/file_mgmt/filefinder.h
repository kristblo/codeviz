#ifndef FILEFINDER_H
#define FILEFINDER_H

#include <iostream>
#include <filesystem>
#include <experimental/filesystem>
#include <unordered_set>
#include <vector>

namespace fs = std::filesystem;

void find_files_recursively(const fs::path& top_dir, 
                const std::unordered_set<std::string>& excl_dirs,
                std::vector<std::string>& output);


void find_files_recursively(const fs::path& top_dir,
                std::vector<std::string>& output);

/// @brief Finds lexicographic distance between two path strings
/// @param filepath1 Comparator
/// @param filepath2 Comparee
/// @return idk ask someone who does discrete maths
int calculate_distance_between_files(std::string filepath1, std::string filepath2);

#endif //FILEFINDER_H