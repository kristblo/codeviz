#include "tagfileparser.h"

void TagFileParser::splitTagStrings()
{
	for(str tagString : this->mTagStrings)
	{
		size_t splitPos = tagString.find(";\"");
		str tagHeader = tagString.substr(0, splitPos);

		try
		{
			if(tagString[splitPos + 2] == '\t') //Prevent leading tab from becoming part of the string
			{
				str tagFields = tagString.substr(splitPos + 3, str::npos);
				this->mSplitTagStrings.push_back(SplitTagString(tagHeader, tagFields));
			}
			else
			{
				str tagFields = tagString.substr(splitPos + 2, str::npos);
				this->mSplitTagStrings.push_back(SplitTagString(tagHeader, tagFields));				
			}
		}
		catch(const std::exception& e)
		{
			std::cerr << e.what() << '\n';
		}
		

	}
}

void TagFileParser::createTagStringsFromTagFile()
{	
	str tag;
	size_t tagEndPos = 0;
	while((tagEndPos = this->mTagFile.find('\n')) != str::npos)
	{
		tag = this->mTagFile.substr(0, tagEndPos);
		if((tag[0]) != '!')
		{
			this->mTagStrings.push_back(tag);
		}
		this->mTagFile = this->mTagFile.substr(tagEndPos + 1);
	}
}

void TagFileParser::splitStringsToItems()
{
	for(SplitTagString splitTag : this->mSplitTagStrings)
	{
		TagItemsAsStrings currentTag = TagItemsAsStrings(&splitTag);
		currentTag.processSplitTagString();
		this->mItemStrings.push_back(currentTag);
	}
}

void TagFileParser::parseTagFile()
{
	this->createTagStringsFromTagFile();
	this->splitTagStrings();
	this->splitStringsToItems();
}

vec<SplitTagString> TagFileParser::getSplitTagStrings()
{
	return this->mSplitTagStrings;
}

vec<TagItemsAsStrings> TagFileParser::getItemStrings()
{
	return this->mItemStrings;
}

TagFileParser::TagFileParser(str aTagFile)
{
	this->mTagFile = aTagFile;
}

///////////////////////////////////////////////

str SplitTagString::getTagHeader()
{
	return this->mTagHeader;
}

str SplitTagString::getTagFields()
{
	return this->mTagFields;
}

SplitTagString::SplitTagString(str aTagHeader, str aTagFields)
{
	this->mTagHeader = aTagHeader;
	this->mTagFields = aTagFields;
}

/////////////////////////////////////////////////

void TagItemsAsStrings::splitTagHeaderItems()
{
	str tagHeader = this->mSplitTagString->getTagHeader();
	str tagName;
	str tagFile;
	str tagAddress;
	
	//Get the 'tag name', i.e. first field of a tag
	size_t headerPos = tagHeader.find('\t');
	tagName = tagHeader.substr(0, headerPos);
	tagHeader = tagHeader.substr(headerPos + 1);
	
	//Get the 'tag file', second field of a tag
	headerPos = tagHeader.find('\t');
	tagFile = tagHeader.substr(0, headerPos);
	tagHeader = tagHeader.substr(headerPos + 1);
	
	//Get and strip the 'tag address', third field of a tag
	headerPos = tagHeader.find("/^");
	tagHeader = tagHeader.substr(headerPos + 2);
	while(tagHeader[0] == '\t' || tagHeader[0] == ' ')
	{
		headerPos = 1;
		tagHeader = tagHeader.substr(headerPos);
	}
	

	if(tagHeader.back() == '/') //Possibly remove terminal /
	{
		tagHeader.pop_back();
	}
	if(tagHeader.back() == '$') //Possibly remove terminal $
	{
		tagHeader.pop_back();
	}
	while(tagHeader.back() == '\t' || tagHeader.back() == ' ') //Possibly remove trailing whitespace
	{
		tagHeader.pop_back();
	}
	
	try
	{
		tagAddress = tagHeader;
	}
	catch(const std::exception& e)
	{
		tagAddress = "1";
		std::cerr << "Tag name: " << tagName << ", Tag address error: " << e.what() << std::endl;
	}
	

	this->mTagHeaderItems.push_back(tagName);
	this->mTagHeaderItems.push_back(tagFile);
	this->mTagHeaderItems.push_back(tagAddress);

}

void TagItemsAsStrings::splitTagFieldItems()
{
	str tagFields = this->mSplitTagString->getTagFields();

	size_t tagFieldPos = 0;
	str tagFieldItem;
	while((tagFieldPos = tagFields.find('\t')) != str::npos)
	{
		tagFieldItem = tagFields.substr(0, tagFieldPos);
		this->mTagFieldItems.push_back(tagFieldItem);
		tagFields = tagFields.substr(tagFieldPos + 1);
	}
	this->mTagFieldItems.push_back(tagFields);
}

SplitTagString* TagItemsAsStrings::getSplitTagString()
{
	return this->mSplitTagString;
}

void TagItemsAsStrings::processSplitTagString()
{
	this->splitTagHeaderItems();
	this->splitTagFieldItems();
}

vec<str> TagItemsAsStrings::getTagHeaderItems()
{
	return this->mTagHeaderItems;
}

vec<str> TagItemsAsStrings::getTagFieldItems()
{
	return this->mTagFieldItems;
}

TagItemsAsStrings::TagItemsAsStrings(SplitTagString* aSplitTagString)
{
	this->mSplitTagString = aSplitTagString;
}
