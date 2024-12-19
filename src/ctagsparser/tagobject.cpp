#include "tagobject.h"

str TagObject::getTagName()
{
  return this->mTagName;
}

str TagObject::getTagFile()
{
  return this->mTagFile;
}

str TagObject::getTagAddress()
{
  return this->mTagAddress;
}

str TagObject::getTagKind()
{
  return this->getTagFieldValue("kind");
}

int TagObject::getTagLine()
{
  return stoi(this->getTagFieldValue("line"));
}

str TagObject::getCleanAddress()
{
  return this->mTagAddress;
}

std::map<str, str> TagObject::getTagFields()
{
  return this->mTagFields;
}

str TagObject::getTagFieldValue(str aTagField)
{
  try
  {
    return this->mTagFields.at(aTagField);
  }
  catch(const std::exception& e)
  {
    std::cerr << e.what() << '\n';
    return "FieldNotFound";
  }
  
}

std::vector<str> TagObject::getTagFieldsAsVec()
{
  std::vector<str> fields;
  for(auto item : this->mTagFields)
  {
    str field = item.first + ":" + item.second;
    fields.push_back(field);
  }

  return fields;
}

TagObject::TagObject(str aTagName,
            str aTagFile,
            str aTagAddress,
            std::vector<str> aTagFields)
{
    
  this->mTagName = aTagName;
  this->mTagFile = aTagFile;
  this->mTagAddress = aTagAddress;

  for(str tagField : aTagFields)
  {
    size_t splitPos = tagField.find(":");
    str fieldName = tagField.substr(0, splitPos);
    str fieldContent = tagField.substr(splitPos + 1, str::npos);
    this->mTagFields.try_emplace(fieldName, fieldContent);

  }
  
}

std::ostream& operator<<(std::ostream& os, const TagObject& tag)
{
  os << "Name: " << tag.mTagName << std::endl
      << "File: " << tag.mTagFile << std::endl
      << "Address: " << tag.mTagAddress << std::endl
      << "Fields: ";

  for(auto field : tag.mTagFields)
  {
    os << field.second << " | ";
  }

  return os;
}