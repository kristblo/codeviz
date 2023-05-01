#ifndef FILEWRITER_H
#define FILEWRITER_H

#include <iostream>
#include <fstream>
#include <algorithm>

void write_line_to_file(std::string outputFile, std::string outputString);

void write_to_file(std::string outputFile, std::string outputString);

std::string str_toupper(std::string s);

#endif //FILEWRITER_H