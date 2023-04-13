#include "parsernodetypes.h"


ParserNodeType ScopeNode::getParserNodeType()
{
    return type;
}

std::vector<int> ScopeNode::getScopeID()
{
    return ScopeID;
}

int ScopeNode::getScopeStart()
{
    return scopeStart;
}

int ScopeNode::getScopeEnd()
{
    return scopeEnd;
}

void ScopeNode::setScopeEnd(int end)
{
    scopeEnd = end;
}

ScopeNode::ScopeNode(std::vector<int> aScopeID, 
                     int start, 
                     int end) : 
                     ScopeID{aScopeID}, 
                     scopeStart{start}, 
                     scopeEnd{end} 
{

}

ParserNodeType ParserNode::getParserNodeType()
{
    return type;   
}

ScopeNode* ParserNode::getScope()
{
    return scope;
}

void ParserNode::setScope(ScopeNode* aScope)
{
    scope = aScope;
}

ParserNode::ParserNode(ParserNodeType aType, 
                       ScopeNode* aScope) : 
                       type{aType}, 
                       scope{aScope}
{

}

ParserNode::ParserNode(ParserNodeType aType) : type{aType}, scope{nullptr}
{

}


std::string IncludeNode::getValue()
{
    return value;
}

std::string IncludeNode::getUser()
{
    return user;
}

IncludeNode::IncludeNode(std::string aValue, 
                         std::string aUser,                         
                         ScopeNode* aScope) : 
                         value{aValue}, 
                         user{aUser}, 
                         ParserNode(INCLUDE, aScope)
{

}

std::string DefineNode::getValue()
{
    return value;
}

DefineNode::DefineNode(std::string aValue,                       
                       ScopeNode* aScope) :
                       value{aValue},
                       ParserNode(DEFINE, aScope)
{

}

std::string ArgumentNode::getName()
{
    return name;
}

std::string ArgumentNode::getDtype()
{
    return dtype;
}

void* ArgumentNode::getActual()
{
    return actual;
}

void ArgumentNode::setActual(void* aActual)
{
    actual = aActual;
}

ArgumentNode::ArgumentNode(std::string aName,
                           std::string aDtype,
                           void* aActual,                           
                           ScopeNode* aScope) :
                           name{aName},
                           dtype{aDtype},
                           ParserNode(ARGUMENT, aScope)
{

}                    

std::string FunctionNode::getName()
{
    return name;
}

std::vector<ArgumentNode*> FunctionNode::getArguments()
{
    return arguments;
}

void FunctionNode::setArguments(std::vector<ArgumentNode*> aArgNodeVector)
{
    arguments = aArgNodeVector;
}

void FunctionNode::appendArgument(ArgumentNode* aArgNode)
{
    arguments.push_back(aArgNode);
}

void FunctionNode::replaceArgument(ArgumentNode* aArgNode, int idx)
{
    arguments[idx] = aArgNode;
}

std::string FunctionNode::getRettype()
{
    return rettype;
}


FunctionNode::FunctionNode(std::string aName,
                           std::string aRettype,
                           ParserNodeType aType,
                           ScopeNode* aScope) :
                           name{aName},
                           rettype{aRettype},
                           ParserNode(aType, aScope)
{

}                           

FunctionDefNode::FunctionDefNode(std::string aName,
                                 std::string aRettype,
                                 ScopeNode* aScope) :
                                 FunctionNode(aName, 
                                              aRettype,
                                              FUNCDEF,
                                              aScope)
{

}

FunctionCallNode::FunctionCallNode(std::string aName,
                                   ScopeNode* aScope) :
                                   FunctionNode(aName,
                                                "",
                                                FUNCCALL,
                                                aScope)
{
    
}

FunctionDeclNode::FunctionDeclNode(std::string aName,
                                   std::string aRettype,
                                   ScopeNode* aScope) :
                                   FunctionNode(aName,
                                                aRettype,
                                                FUNCDECL,
                                                aScope)
{

}                                                                


std::string AccessNode::getAccessor()
{
    return accessor;
}

std::string AccessNode::getAccessee()
{
    return accessee;
}

AccessNode::AccessNode(std::string aAccessor,
                       std::string aAccessee,
                       ScopeNode* aScope) :
                       accessor{aAccessor},
                       accessee{aAccessee},
                       ParserNode(ACCESS, aScope)
{

}

std::string StructNode::getName()
{
    return name;
}

std::vector<void*> StructNode::getMembers()
{
    return members;
}

void StructNode::setMembers(std::vector<void*> memberVec)
{
    members = memberVec;
}

void StructNode::appendMember(void* aMember)
{
    members.push_back(aMember);
}

StructNode::StructNode(std::string aName,
                       ScopeNode* aScope) :
                       name{aName},
                       ParserNode(STRUCT, aScope)
{

}

std::string VariableNode::getValue()
{
    return value;
}

std::string VariableNode::getName()
{
    return name;
}

std::string VariableNode::getDtype()
{
    return dtype;
}

VariableNode::VariableNode(std::string aName,
                           std::string aValue,
                           std::string aDtype,
                           ParserNodeType aType,
                           ScopeNode* aScope) :
                           name{aName},
                           value{aValue},
                           dtype{aDtype},
                           ParserNode(aType, aScope)
{

}

VarDeclNode::VarDeclNode(std::string aName,
                         std::string aDtype,
                         ScopeNode* aScope) :
                         VariableNode(aName,
                                      "NULL",
                                      aDtype,
                                      VARDECL,
                                      aScope)
{

}

VarInitNode::VarInitNode(std::string aName,
                         std::string aValue,
                         std::string aDtype,
                         ScopeNode* aScope) :
                         VariableNode(aName,
                                      aValue,
                                      aDtype,
                                      VARINIT,
                                      aScope)
{

}

VarAssignmentNode::VarAssignmentNode(std::string aName,
                                     std::string aValue,
                                     ScopeNode* aScope) :
                                     VariableNode(aName,
                                                  aValue,
                                                  "",
                                                  VARASSIGN,
                                                  aScope)
{

}