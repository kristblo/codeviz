#include "fileparser.h"


//Functions:
//  Call hierarchy
//  Arguments
//      IDs
//      Literals
//      Calls (=IDs)
//  Return values
//Only the information entering and leaving the function is interesting
//Arithmetics etc in an argument is not relevant; only the participants
//Information enters via argument (pure) or scope (impure/class).
//Information leaves via return value or by writing to arg/scope.

//Assignments: Arithmetics irrelevant, only participants.
//  Participants: IDs, 

void FileParser::parseFile(std::string aFileToParse)
{
    mTokenizer.tokenize(aFileToParse);
    std::vector<Token> tokens = mTokenizer.tokens;

    for(Token token: tokens)
    {
        //Match the longest possible pattern with the
        //available tokens. If no matches can be found,
        //go to the next token.


    }

}

FileParser::FileParser()
{
}
