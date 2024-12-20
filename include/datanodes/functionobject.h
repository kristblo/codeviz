#ifndef FUNCTIONOBJECT_H
#define FUNCTIONOBJECT_H

#include <map>

#include "memberobject.h"

class FunctionObject : public MemberObject{
private:
    /// @brief Function inputs: members used by the function
    vec<MemberObject*> mInputs;

    /// @brief Function outputs: members modified by the function
    vec<MemberObject*> mOutputs;

    std::map<str, vec<MemberObject*>> mMembers;
public:
    void addMember(str aMemberType, MemberObject* aMember);
    
    vec<MemberObject*> getMembers(str aMemberType);

    FunctionObject(str aName);

};

#endif //FUNCTIONOBJECT_H