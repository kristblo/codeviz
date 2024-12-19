#include "moduleobject.h"

str ModuleObject::getFileName()
{
    return this->mModuleName;
}

void ModuleObject::addIncludeString(str aModuleName)
{
    this->mIncludesAsString.push_back(aModuleName);
}

void ModuleObject::addIncludeModule(ModuleObject* aModuleName)
{
    this->mIncludes.push_back(aModuleName);
}

void ModuleObject::addSourceFile(str aSourceFile)
{
    this->mSourceFiles.push_back(aSourceFile);
}

vec<str> ModuleObject::getSourceFiles()
{
    return this->mSourceFiles;
}

vec<str> ModuleObject::getIncludeStrings()
{
    return this->mIncludesAsString;
}

ModuleObject::ModuleObject(str aModuleName)
{
    this->mModuleName = aModuleName;
}