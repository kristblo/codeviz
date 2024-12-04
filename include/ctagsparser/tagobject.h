#ifndef TAGOBJECT_H
#define TAGOBJECT_H

#include <iostream>

#include <string>
#include <vector>

class TagObject{
private:
    /// @brief The string which makes up a single tag
    std::string mTagString;

    //Tag information as defined in https://docs.ctags.io/en/latest/man/tags.5.html#tags-5
    //Chapter: Proposal

    /// @brief The name of the tag
    std::string mTagName;

    /// @brief The file in which the tag was found
    std::string mTagFile;

    /// @brief The tag's vim-searchable name string
    std::string mTagAddress;

    /// @brief Tag fields
    std::vector<std::string> mTagFields;

public:
    std::string getTagString();
    std::vector<std::string> getTagFields();
    
    TagObject(std::string aTagName,
                std::string aTagFile,
                std::string aTagAddress,
                std::vector<std::string> aTagFields);

};

#endif //TAGOBJECT_H