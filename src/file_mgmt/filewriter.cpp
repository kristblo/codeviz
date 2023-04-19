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