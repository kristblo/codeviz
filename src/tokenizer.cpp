#include "tokenizer.h"


Token::Token(std::string aType, std::string aValue, int aLine, std::vector<int> aScope)
{
    type = aType;
    value = aValue;
    line = aLine;
    scope = aScope;
}

std::string Tokenizer::compile_pattern()
{
    std::string pattern = "";
    std::string wrap_begin = "(?:";
    std::string wrap_end = ")|";
    for(auto& token: token_definitions)
    {
        pattern += (wrap_begin + token.second + wrap_end);  
        //std::cout << token.first << std::endl;          
        //pattern += token.second + "|";
    }
    pattern.pop_back(); //Remove final |

    return pattern;    

}

void Tokenizer::tokenize(std::string input)
{
    std::regex re(tokens_pattern);

    std::vector<std::string> token_matches{
       std::sregex_token_iterator(input.begin(), input.end(), re),{}
    };


    //Token object generation:
    //1. For each object in token_matches,
    //2. check which definition gave a hit by looping through the defs
        //2.2 until the right one is found.
    //3. Use the token_actions map to take necessary actions such as
        //3.2 counting lines
        //3.3 ignoring comments while also counting lines
    //4. Generate the corresponding token object by calling map[hit]    
    for(auto& raw_token: token_matches)
    {   
        currentRaw = raw_token;
        for(auto& definition: token_definitions)
        {            
            if(std::regex_search(raw_token, std::regex(definition.second)))
            {
                //std::cout << definition.first << std::endl;
                currentHit = definition;
                break;
            }
        }



        //token_actions[token_hit.first]; //How do I call this lmao
        std::map<std::string, void(Tokenizer::*)()>::iterator iter = //
            token_actions.find(currentHit.first);
        if(iter != token_actions.end())
        {        
            (this->*(iter->second))();
        }
        else{
            //No particular action is taken for most tokens
            Token currentToken = Token(currentHit.first, 
                                       currentRaw, 
                                       lineno,
                                       currentScope);
            tokens.push_back(currentToken);
        }
        
    }
    std::cout << "Final linecount: " << lineno << std::endl;    
}

void Tokenizer::action_LCOMMENT()
{    
    //Count lines in the comment
    std::string input = currentRaw;
    std::regex pattern("\\n");
    std::sregex_iterator iter(input.begin(), input.end(), pattern);
    std::sregex_iterator end;
    int count = 0;
    while(iter != end)
    {
        ++count;
        ++iter;
    }
    lineno += count;

}

void Tokenizer::action_COMMENT()
{
    //Do nothing
}

void Tokenizer::action_NEWLINE()
{    
    lineno++;
}

void Tokenizer::action_ID()
{
    std::string name = currentRaw;
    std::string upper = str_toupper(name);        
    if(reserved_words.find(upper) != reserved_words.end())
    {                
        tokens.push_back(Token(upper, 
                               currentRaw, 
                               lineno,
                               currentScope));
    }
    else{
        tokens.push_back(Token(currentHit.first, 
                               currentRaw, 
                               lineno,
                               currentScope));
    }
}

void Tokenizer::action_LBRACE()
{
    tokens.push_back(Token(currentHit.first,
                           currentRaw,
                           lineno,
                           currentScope));
    currentScope.push_back(lineno);
}

void Tokenizer::action_RBRACE()
{
    currentScope.pop_back();
    tokens.push_back(Token(currentHit.first,
                           currentRaw,
                           lineno,
                           currentScope));
}

// void Tokenizer::action_DEFDTYPE()
// {
//     std::string name = str_toupper(currentRaw);
//     tokens.push_back(Token(name,
//                            currentRaw,
//                            lineno,
//                            currentScope));
// }

Tokenizer::Tokenizer()
{
    tokens_pattern = compile_pattern();
}
