#ifndef FILEOPENER_H
#define FILEOPENER_H

#include <iostream>
#include <fstream>
#include <sstream>

using std::cout;
using std::cerr;
using std::endl;
using std::string;
using std::ifstream;
using std::ostringstream;

string readFileIntoString(const string& path);

#endif //FILEOPENER_H   