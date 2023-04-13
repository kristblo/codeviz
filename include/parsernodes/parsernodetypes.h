#ifndef PARSER_NODES_H
#define PARSER_NODES_H

#include <iostream>
#include <vector>
#include "string.h"

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

class ParserNode{
private:
    //Sets the type of node
    ParserNodeType type;
    ScopeNode* scope;

public:
    ParserNodeType getParserNodeType();
    ScopeNode* getScope();
    void setScope(ScopeNode* aScope);
    ParserNode(ParserNodeType aType, ScopeNode* aScope);
    ParserNode(ParserNodeType aType);

};

class IncludeNode : public ParserNode{
private:
    std::string value;
    std::string user; //Local file, probably

public:
    
    std::string getValue();
    std::string getUser();
    IncludeNode(std::string aValue, 
                std::string aUser,                
                ScopeNode* aScope);

};

class DefineNode : public ParserNode{
private:
    std::string value;

public:
    std::string getValue();
    DefineNode(std::string aValue,               
               ScopeNode* aScope);

};

class ArgumentNode : public ParserNode {
private:
    std::string name;
    std::string dtype;
    void* actual; //Pointer to the piece of data parsed as an argument

public:
    std::string getName();
    std::string getDtype();
    void* getActual();
    void setActual(void* aActual);    
    ArgumentNode(std::string aName,
                 std::string aDtype,
                 void* aActual,                 
                 ScopeNode* aScope);
};


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

class FunctionDefNode : public FunctionNode{
public:    
    FunctionDefNode(std::string aName,
                    std::string aRettype,
                    ScopeNode* aScope);
};

class FunctionCallNode : public FunctionNode {
public:
    FunctionCallNode(std::string aName,
                     ScopeNode* aScope);
};

class FunctionDeclNode : public FunctionNode {
public:
    FunctionDeclNode(std::string aName,
                     std::string aRettype,
                     ScopeNode* aScope);
};

class AccessNode : public ParserNode{
private:
    std::string accessor; //TODO: Consider void* to actual?
    std::string accessee;

public:
    std::string getAccessor();
    std::string getAccessee();
    AccessNode(std::string aAccessor,
                std::string aAccessee,
                ScopeNode* aScope);
};

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

class VarDeclNode : public VariableNode{
public:
    VarDeclNode(std::string aName,
                std::string aDtype,
                ScopeNode* aScope);
};

class VarInitNode : public VariableNode{
public:
    VarInitNode(std::string aName,
                std::string aValue,
                std::string aDtype,
                ScopeNode* aScope);
};

class VarAssignmentNode : public VariableNode{
public:
    VarAssignmentNode(std::string aName,
                        std::string aValue,
                        ScopeNode* aScope);
};

#endif //PARSER_NODES_H