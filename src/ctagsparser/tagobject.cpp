#include "tagobject.h"

std::string TagObject::getTagString()
{
    return this->mTagString;
}

std::vector<std::string> TagObject::getTagFields()
{
    return this->mTagFields;
}

TagObject::TagObject(std::string aTagName,
            std::string aTagFile,
            std::string aTagAddress,
            std::vector<std::string> aTagFields)
{
    
    this->mTagName = aTagName;
    this->mTagFile = aTagFile;
    this->mTagAddress = aTagAddress;
    this->mTagFields = aTagFields;
    
    // size_t fieldEndPos = 0;
    // std::string field;
    // while((fieldEndPos = aTagString.find('\t')) != std::string::npos)
    // {
    //     field = aTagString.substr(0, fieldEndPos);
    //     mTagFields.push_back(field);
    //     aTagString = aTagString.substr(fieldEndPos + 1);
    // }

}