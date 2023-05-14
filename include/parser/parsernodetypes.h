#ifndef PARSER_NODES_H
#define PARSER_NODES_H

#include <iostream>
#include <vector>
#include "string.h"


/// @brief Types of information the parser looks for
enum ParserNodeType{SCOPE, INCLUDE, DEFINE, ARGUMENT, 
                    FUNCDEF, FUNCCALL, FUNCDECL, ACCESS, 
                    STRUCT, VARDECL, VARINIT, VARASSIGN};

class ScopeNode{
private:
    ParserNodeType type = SCOPE;
    std::vector<int> ScopeID;
    int scopeStart;
    int scopeEnd;

public:
    ParserNodeType getParserNodeType();
    std::vector<int> getScopeID();
    int getScopeStart();
    int getScopeEnd();
    void setScopeEnd(int end);
    
    ScopeNode(std::vector<int> aScopeID, int start, int end);
};

/// @brief C/C++ specific pieces of information become ParserNodes
class ParserNode{
private:    
    ParserNodeType type;    
    ScopeNode* scope;

public:
    ParserNodeType getParserNodeType();
    ScopeNode* getScope();
    void setScope(ScopeNode* aScope);
    ParserNode(ParserNodeType aType, ScopeNode* aScope);
    ParserNode(ParserNodeType aType);

};

/// @brief Inclusion statements
class IncludeNode : public ParserNode{
private:
    /// @brief File being included
    std::string value;

    /// @brief File using another file
    std::string user;

public:
    
    std::string getValue();
    std::string getUser();
    IncludeNode(std::string aValue, 
                std::string aUser,                
                ScopeNode* aScope);

};

/// @brief Define statements, no current use
class DefineNode : public ParserNode{
private:
    std::string value;

public:
    std::string getValue();
    DefineNode(std::string aValue,               
               ScopeNode* aScope);

};

/// @brief Function argument
class ArgumentNode : public ParserNode {
private:
    /// @brief The literal name of the argument
    std::string name;
    
    /// @brief Data type of the argument, if discernible
    std::string dtype;
    
    /// @brief Pointer to the piece of data parsed as an argument
    ParserNode* actual;

public:
    std::string getName();
    std::string getDtype();
    ParserNode* getActual();
    void setActual(ParserNode* aActual);    
    ArgumentNode(std::string aName,
                 std::string aDtype,
                 ParserNode* aActual,                 
                 ScopeNode* aScope);
};

/// @brief Base class for all functions
class FunctionNode : public ParserNode{
private:
    std::string name;
    std::vector<ArgumentNode*> arguments;
    std::string rettype;

public:
    std::string getName();
    std::vector<ArgumentNode*> getArguments();
    void setArguments(std::vector<ArgumentNode*> aArgNodeVector);
    void appendArgument(ArgumentNode* aArgnode);
    void replaceArgument(ArgumentNode* aArgNode, int idx);
    std::string getRettype();
    FunctionNode(std::string aName,
                 std::string aRettype,
                 ParserNodeType aType,
                 ScopeNode* aScope);
};

/// @brief Function definition
class FunctionDefNode : public FunctionNode{
public:    
    FunctionDefNode(std::string aName,
                    std::string aRettype,
                    ScopeNode* aScope);
};

/// @brief Function call
class FunctionCallNode : public FunctionNode {
public:
    FunctionCallNode(std::string aName,
                     ScopeNode* aScope);
};

/// @brief Function declaration
class FunctionDeclNode : public FunctionNode {
public:
    FunctionDeclNode(std::string aName,
                     std::string aRettype,
                     ScopeNode* aScope);
};

/// @brief Access generally refers to the . or -> operators
class AccessNode : public ParserNode{
private:
    /// @brief Left hand side of access operator
    std::string accessor; //TODO: Consider void* to actual?
    
    /// @brief Right hand side of access operator
    std::string accessee;

public:
    std::string getAccessor();
    std::string getAccessee();
    AccessNode(std::string aAccessor,
                std::string aAccessee,
                ScopeNode* aScope);
};

/// @brief Represents C struct definitions
class StructNode : public ParserNode{
private:
    std::string name;
    std::vector<void*> members; //Yikes

public:
    std::string getName();
    std::vector<void*> getMembers();
    void setMembers(std::vector<void*> members);
    void appendMember(void* aMember);
    StructNode(std::string aName,
                ScopeNode* aScope);

};

/// @brief Variable base class
class VariableNode : public ParserNode{
private:
    std::string value;
    std::string name;
    std::string dtype;

public:
    std::string getValue();
    std::string getName();
    std::string getDtype();
    VariableNode(std::string aName,
                    std::string aValue,
                    std::string aDtype,
                    ParserNodeType aType,
                    ScopeNode* aScope);
};

/// @brief Variable declaration
class VarDeclNode : public VariableNode{
public:
    VarDeclNode(std::string aName,
                std::string aDtype,
                ScopeNode* aScope);
};

/// @brief Variable initialization
class VarInitNode : public VariableNode{
public:
    VarInitNode(std::string aName,
                std::string aValue,
                std::string aDtype,
                ScopeNode* aScope);
};

/// @brief Variable (re)assignment, core concept in data flow
class VarAssignmentNode : public VariableNode{
public:
    VarAssignmentNode(std::string aName,
                        std::string aValue,
                        ScopeNode* aScope);
};

#endif //PARSER_NODES_H