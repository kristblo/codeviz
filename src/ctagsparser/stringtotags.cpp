#include "stringtotags.h"

void StringToTags::splitStrToTags(std::string aTagFile)
{
    std::string tag;
    size_t tagEndPos = 0;

    
    //Step 1: Get individual tags as strings by splitting on newline
    std::vector<std::string> tagStrings;

    while((tagEndPos = aTagFile.find('\n')) != std::string::npos)
    {
        tag = aTagFile.substr(0, tagEndPos);
        tagStrings.push_back(tag);
        aTagFile = aTagFile.substr(tagEndPos + 1);

    }

    std::cout << tagStrings[0] << std::endl;

    //Step 2: Split tag header from tagfields by splitting on ;"
    std::vector<std::tuple<std::string, std::string>> splitTags;
    for(std::string tag : tagStrings)
    {
        size_t splitPos = tag.find(";\"");
        std::string tagHeader = tag.substr(0, splitPos);
        std::string mTagFields = tag.substr(splitPos +2, std::string::npos);
        std::tuple<std::string, std::string> splitTag;
        splitTag = {tagHeader, mTagFields};
        splitTags.push_back(splitTag);

    }

    std::cout << std::get<0>(splitTags[0]) << std::endl;
    std::cout << std::get<1>(splitTags[0]) << std::endl;

    //Step 3: Build the tag objects
    int debugCounter = 0;
    for(auto splitTag : splitTags)
    {
        if((std::get<0>(splitTag)[0]) != '!') //! indicates comment
        {
            debugCounter++;

            std::string header = std::get<0>(splitTag);
            std::string tags = std::get<1>(splitTag);

            size_t headerPos = 0;
            std::string headerItem;
            std::vector<std::string> headerFields;
            while((headerPos = header.find('\t')) != std::string::npos)
            {
                headerItem = header.substr(0, headerPos);
                headerFields.push_back(headerItem);
                header = header.substr(headerPos + 1);
            }
            //Loop discards last item, push back manually
            headerFields.push_back(header);
            
            std::cout << "line: " << debugCounter << " headersize: " << headerFields.size() << std::endl;


            size_t tagFieldpos = 0;
            std::string tagFieldItem;
            std::vector<std::string> tagFields;
            while((tagFieldpos = tags.find('\t')) != std::string::npos)
            {
                tagFieldItem = tags.substr(0, tagFieldpos);
                tagFields.push_back(tagFieldItem);
                tags = tags.substr(tagFieldpos + 1);
            }
            tagFields.push_back(tags);
            
            TagObject currentTagObj = TagObject(headerFields[0],
                                                headerFields[1],
                                                headerFields[2],
                                                tagFields);
            this->mTagObjects.push_back(currentTagObj);

        }
    }
}

std::vector<TagObject> StringToTags::getTagObjects()
{
    return this->mTagObjects;
}

StringToTags::StringToTags(std::string aTagFile)
{
    this->splitStrToTags(aTagFile);
}