#ifndef CLASSOBJECT_H
#define CLASSOBJECT_H

#include <map>

#include "memberobject.h"

/// @brief Class: contains references to functions, variables etc. 
class ClassObject : public MemberObject{
private:
    vec<MemberObject*> privateMembers;
    vec<MemberObject*> publicMembers;
    vec<MemberObject*> protectedMembers;

    /// @brief Map of all members, sorted by access status
    std::map<str, vec<MemberObject*>> mMembers = {
        {"private", this->privateMembers},
        {"public", this->publicMembers},
        {"protected", this->protectedMembers}
    };

public:
    /// @brief Adds a member reference to one of the member vectors
    /// @param aMemberType One of private, public, protected
    /// @param aMemberObject Reference to member object
    void addMember(str aMemberType, MemberObject* aMemberObject);
    
    /// @brief Returns one of the three types of member
    /// @param aMemberType one of private, public, protected
    /// @return vec this.TYPEmember
    vec<MemberObject*> getMembers(str aMemberType);
    
    ClassObject(str aName);
};

#endif //CLASSOBJECT_H