#ifndef TAGOBJECT_H
#define TAGOBJECT_H

#include <iostream>

#include <string>
#include <vector>
#include <map>

#define str std::string

class TagObject{
private:

	//Tag information as defined in https://docs.ctags.io/en/latest/man/tags.5.html#tags-5
	//Chapter: Proposal

	/// @brief The name of the tag
	str mTagName;

	/// @brief The file in which the tag was found
	str mTagFile;

	/// @brief The tag's vim-searchable name string
	str mTagAddress;

	/// @brief Tag fields
	std::map<str, str> mTagFields;

public:
  /// @brief Returns the name of the tag, i.e. the first field of a ctag
  /// @return TagName
  str getTagName();

	/// @brief Returns the name of the file in which the tag was found, i.e. second field of a ctag
	/// @return TagFile
	str getTagFile();

	/// @brief Returns the address of the tag, i.e. third field of a ctag
	/// @return TagAddress
	str getTagAddress();

  /// @brief Returns the kind of the tag
  /// @return TagKind
  str getTagKind();

  /// @brief Returns the line on which the tag was found in the source code
  /// @return TagLine
  int getTagLine();

  /// @brief Returns a sanitized version of the tag address depending on kind
  /// @return See child classes
  str getCleanAddress();
	
	std::map<str, str> getTagFields();
	str getTagFieldValue(str aTagField);

  std::vector<str> getTagFieldsAsVec();
	
	TagObject(str aTagName,
							str aTagFile,
							str aTagAddress,
							std::vector<str> aTagFields);

	friend std::ostream& operator<<(std::ostream& os, const TagObject& tag);

};

#endif //TAGOBJECT_H