#ifndef FILEOBJECT_H
#define FILEOBJECT_H

#include <string>
#include <vector>

#define str std::string
#define vec std::vector

/// @brief Module level information container; collects all data relevant to a module
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

    /// @brief Indicates whether the module is external to the project
    bool isExternal;

public:
    
    /// @brief Returns the name of the module
    /// @return str this.mModulename
    str getModuleName();

    /// @brief Adds the name of a module included in this module
    /// @param aModuleName String name of module
    void addIncludeString(str aModuleName);

    /// @brief Adds a reference to a module included in this module
    /// @param aModuleName Name of module reference
    void addIncludeModule(ModuleObject* aModuleName);

    /// @brief Adds the relative path to a source file associated with the module
    /// @param aSourceFile String path to source file
    void addSourceFile(str aSourceFile);

    /// @brief Returns vector of paths to source files
    /// @return vec this.mSourcefiles
    vec<str> getSourceFiles();

    /// @brief Returns vector of module names included in the module
    /// @return vec this.mIncludesAsStrings
    vec<str> getIncludeStrings();

    /// @brief Returns vector of modules included in the module
    /// @return vec this.mIncludess
    vec<ModuleObject*> getIncludedModules();

    /// @brief Returns status of the external flag
    /// @return bool this.isExternal
    bool isModuleExternal();

    /// @brief Constructs the object containing only its name and external status
    /// @param aModuleName Name of the module
    /// @param isExternal Whether the module is defined externally of the project
    ModuleObject(str aModuleName, bool isExternal = false);

};

#endif //FILEOBJECT_H