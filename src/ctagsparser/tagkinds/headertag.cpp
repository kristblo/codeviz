#include "headertag.h"

str HeaderTag::getCleanAddress()
{
  str tagAddress = this->getTagAddress();
  std::regex re("[\'\"<](\\w|[\\./])*[\'\">]");
  std::vector<str> matches{
    std::regex_token_iterator(tagAddress.begin(), tagAddress.end(), re), {}
  };

  str cleanAddress;
  if(matches.size() > 0)
  {
    cleanAddress = matches[0];
    cleanAddress.erase(cleanAddress.begin());
    cleanAddress.erase(cleanAddress.end()-1);
    cleanAddress = std::filesystem::path(cleanAddress).stem().string();
  }
  else
  {
    cleanAddress = tagAddress;
  }

  return cleanAddress;
}

str HeaderTag::getHeaderName()
{
  return this->getCleanAddress();
}

HeaderTag::HeaderTag(TagObject aTagObject) : TagObject(aTagObject.getTagName(),
                                            aTagObject.getTagFile(),
                                            aTagObject.getTagAddress(),
                                            aTagObject.getTagFieldsAsVec())
{

}                                            