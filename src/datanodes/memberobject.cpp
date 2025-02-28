#include "memberobject.h"

void MemberObject::addMember(MemberObject* aMember)
{
    this->mMembers.push_back(aMember);
}

vec<MemberObject*> MemberObject::getMembers()
{
    return this->mMembers;
}

void MemberObject::setOrigin(MemberObject* aOrigin)
{
    this->mOrigin = aOrigin;
}

MemberObject* MemberObject::getOrigin()
{
    return this->mOrigin;
}