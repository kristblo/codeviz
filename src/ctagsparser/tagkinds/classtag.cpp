#include "classtag.h"

str ClassTag::getCleanAddress()
{
  str tagAddress = this->getTagAddress();
  std::regex re("*");

  std::vector<str> matches{
    std::regex_token_iterator(tagAddress.begin(), tagAddress.end(), re), {}
  };

  str cleanAddress;
  if (matches.size() > 0)
  {
    cleanAddress = matches[0];
  }
  else
  {
    cleanAddress = tagAddress;
  }

  return cleanAddress;

}

str ClassTag::getClassName()
{
  return this->getTagName();
}

ClassTag::ClassTag(TagObject aTagObject) : TagObject(aTagObject.getTagName(),
                                          aTagObject.getTagFile(),
                                          aTagObject.getTagAddress(),
                                          aTagObject.getTagFieldsAsVec())
{

}