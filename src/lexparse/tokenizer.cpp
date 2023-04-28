#include "tokenizer.h"


std::string Tokenizer::compile_pattern()
{
    std::string pattern = "";
    std::string wrap_begin = "(?:";
    std::string wrap_end = ")|";
    for(auto& token: tokens)
    {
        pattern += (wrap_begin + token.second + wrap_end);  
        std::cout << token.first << std::endl;          
        //pattern += token.second + "|";
    }
    pattern.pop_back(); //Remove final |

    return pattern;    

}

std::vector<std::string> Tokenizer::tokenize(std::string input)
{
    std::regex re(tokens_pattern);

    std::vector<std::string> output{
       std::sregex_token_iterator(input.begin(), input.end(), re),{}
    };
    
    return output;
}

Tokenizer::Tokenizer()
{
    tokens_pattern = compile_pattern();
}