#ifndef TAGPARSER_H
#define TAGPARSER_H

#include <string>
#include <vector>
#include <iostream>
#include <exception>

#define str std::string
#define vec std::vector

/// @brief Helper class I'm too lazy to make a separate file for.
class SplitTagString{
private:
	str mTagHeader;
	str mTagFields;


public:
	str getTagHeader();
	str getTagFields();
	SplitTagString(str aTagHeader, str aTagFields);

};

/// @brief Processes a SplitTagString into two string vectors
class TagItemsAsStrings{
private:
	SplitTagString* mSplitTagString;
	vec<str> mTagHeaderItems;
	vec<str> mTagFieldItems;

	void splitTagHeaderItems();
	void splitTagFieldItems();
public:

	SplitTagString* getSplitTagString();
	vec<str> getTagHeaderItems();
	vec<str> getTagFieldItems();
	void processSplitTagString();

	TagItemsAsStrings(SplitTagString* aSplitTagString);
};

class TagFileParser{
private:
	str mTagFile;
	vec<str> mTagStrings;
	vec<SplitTagString> mSplitTagStrings;
	vec<TagItemsAsStrings> mItemStrings;

	void createTagStringsFromTagFile();
	void splitTagStrings();
	void splitStringsToItems();

public:

	void parseTagFile();
	vec<SplitTagString> getSplitTagStrings();
	vec<TagItemsAsStrings> getItemStrings();
	
	TagFileParser(str aTagFile);

};


#endif //TAGPARSER_H