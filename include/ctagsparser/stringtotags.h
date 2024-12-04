#ifndef STRINGTOTAGS_H
#define STRINGTOTAGS_H

#include <string>
#include <vector>
#include "tagobject.h"

class StringToTags{
private:

    /// @brief Contains the split tags file
    std::vector<TagObject> mTagObjects;

    /// @brief Parse a ctags tagfile to tag objects
    /// @param aTagString 
    void splitStrToTags(std::string aTagFile);

public:

    std::vector<TagObject> getTagObjects();

    StringToTags(std::string aTagFile);
};

#endif //STRINGTOTAGS_H