#ifndef MEMBEROBJECT_H
#define MEMBEROBJECT_H

#include <vector>
#include <string>

#define str std::string
#define vec std::vector

//TODO: Make virtual?
/// @brief Generic class for anything that can be a member of something else, or have members
class MemberObject{
private:
    /// @brief Name of the member
    str mName;

    /// @brief Nested members
    vec<MemberObject*> mMembers;

    /// @brief The name of the entity to which the member belong/is a member of
    MemberObject* mOrigin;


public:
    /// @brief Adds a member reference
    /// @param aMember 
    virtual void addMember(MemberObject* aMember) = 0;
    
    /// @brief Returns references to the member's members
    /// @return vec this.mMembers
    virtual vec<MemberObject*> getMembers() = 0;

    /// @brief Set the origin of the object
    /// @param aOrigin Reference to the origin object
    virtual void setOrigin(MemberObject* aOrigin) = 0;

    /// @brief Returns a pointer to the origin object
    /// @return this.mOrigin
    virtual MemberObject* getOrigin() = 0;

    MemberObject(str aName);

};

#endif //MEMBEROBJECT_H