#include "tagobject.h"

std::string TagObject::getTagName()
{
  return this->mTagName;
}

std::string TagObject::getTagFile()
{
  return this->mTagFile;
}

std::string TagObject::getTagAddress()
{
  return this->mTagAddress;
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
  
}

std::ostream& operator<<(std::ostream& os, const TagObject& tag)
{
  os << "Name: " << tag.mTagName << std::endl
      << "File: " << tag.mTagFile << std::endl
      << "Address: " << tag.mTagAddress << std::endl
      << "Fields: ";

  for(auto field : tag.mTagFields)
  {
    os << field << " | ";
  }

  return os;
}