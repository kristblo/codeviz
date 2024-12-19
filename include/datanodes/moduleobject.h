#ifndef FILEOBJECT_H
#define FILEOBJECT_H

#include <string>
#include <vector>

#define str std::string
#define vec std::vector

class ModuleObject{
private:
    /// @brief Name of the module
    str mModuleName;

    /// @brief Relative paths to associated source files
    vec<str> mSourceFiles;

    /// @brief Vector of module names included in the file
    vec<str> mIncludesAsString;

    /// @brief Vector of files included in the file
    vec<ModuleObject*> mIncludes;

public:
    str getFileName();
    void addIncludeString(str aModuleName);
    void addIncludeModule(ModuleObject* aModuleName);

    void addSourceFile(str aSourceFile);
    vec<str> getSourceFiles();

    vec<str> getIncludeStrings();

    ModuleObject(str aModuleName);

};

#endif //FILEOBJECT_H