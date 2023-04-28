#ifndef TOKENIZER_RIPPED_H
#define TOKENIZER_RIPPED_H

#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <vector>
using namespace std;


void printToken(vector<int> token);

void putVector(vector<int> token);

vector<int> parseNumber(int start);

bool isword(int inch);

vector<int> parseWord(int start);

vector<int> parseComment(int start);

vector<int> parseSentence(int start);

void parse_error(string message, char ch);

void getToken();

void tokenize();

#endif //TOKENIZER_RIPPED_H