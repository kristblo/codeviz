#include "filewriter.h"

void write_line_to_file(std::string outputFile, std::string outputString)
{
    std::ofstream filestream;
    filestream.open(outputFile, std::ios_base::app);
    filestream << outputString + '\n';
    filestream.close();
}

void write_to_file(std::string outputFile, std::string outputString)
{
    std::ofstream filestream;
    filestream.open(outputFile, std::ios_base::app);
    filestream << outputString;
}

std::string str_toupper(std::string s){
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c){return std::toupper(c);}
                   );
    return s;
}