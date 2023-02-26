from typing import NamedTuple
import re
import os
from global_utilities import getFileAsString
from global_utilities import getKeywordFromConfigFile
from global_utilities import appendStringToFile

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenizeCode(code):
    tokens = []
    keywords = {'IF', 'ELSE', 'ELSE IF', 'FOR', 'RETRUN'}
    token_specification = [
        ('LCOMS',   r'(\/\*)'),         #Start of long comment /*
        ('LCOME',   r'(\*\/)'),         #End of long comment */
        ('COMMENT', r'(//)+.*'),        #Ignore singe line comments
        ('ID',      r'[A-Za-z_]+[A-Za-z_\d]*'),  #Identifiers
        ('PREFIX',  r'(0x)|(0b)'),      #Number prefixes
        ('NUMBER',  r'\d+(\.\d*)?'),    #Integer or decimal number        
        ('ASSIGN',  r'(&=)|(\|=)|(\^=)|='), #Assignment operator
        ('VARARG',  r'(\.\.\.)'),       #Variable argument list
        ('END',     r';'),              #Statement terminator
        ('MEMBER',  r'(\.)|(->)'),      #Member variable access
        ('LOGOP',   r'(&&)|(\|\|)|(==)|(>=)|(<=)'),          #Logic operators
        ('BITWOP',  r'(<<)|(>>)|[&\|\^~]'), #Bitwise operators
        ('ARITOP',  r'[+\-*/<>:]'),        #Arithmetic operators        
        ('STRING',   r'(\")'),          #Start and end string
        ('CHAR',    r'\''),             #Start and end char
        ('NEWLINE', r'\n'),             #Line endings
        ('SKIP',    r'[ \t]+'),         #Skip spaces and tabs
        ('PREPROC', r'[#]+.*'),         #Prepocessor flags files
        ('BRACEOPEN',   r'{'),          #Start of scope or body
        ('BRACECLOSE',  r'}'),          #End of scope or body
        ('PAROPEN',     r'\('),         #Opening parentheses
        ('PARCLOSE',    r'\)'),         #Closing parentheses
        ('BRACKOPEN',   r'\['),         #Opening bracket
        ('BRACKCLOSE',  r'\]'),         #Closing bracket
        ('LISTSEP', r','),              #List/argument element separator
        ('MISMATCH',    r'.'),          #Any other character
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    inlongcomment = 0 #Are we currently dealing with a multiline comment?
    inshortcomment = 0 #Are we currently dealing with a single line comment?
    instring = 0 #Are we currently dealing with a string?
    currentstring = ''    
    inchar = 0 #Are we currently dealing with a char?
    currentchar = ''
    lastval = '' #Remembers previous char when working with strings/chars


    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if inlongcomment == 1 and kind != 'LCOME':
            if kind == 'NEWLINE':
                line_num += 1
            continue
        elif inlongcomment == 1 and kind == 'LCOME':
            inlongcomment = 0
            continue

        if inshortcomment == 1 and kind != 'NEWLINE':
            continue
        elif inshortcomment == 1 and kind == 'NEWLINE':            
            inshortcomment = 0            

        if instring == 0 and kind == 'STRING':
            instring = 1
            continue
        if instring == 1 and kind != 'STRING':
            currentstring += value
            lastval = value
            continue
        if instring == 1 and kind == 'STRING':
            if lastval != '\\':
                value = currentstring
                instring = 0
                currentstring = ''            
            else:
                currentstring += value
                continue
        
        if inchar == 0 and kind == 'CHAR':
            inchar = 1
            continue
        if inchar == 1 and kind != 'CHAR':
            currentchar = value
            lastval = value
            continue
        if inchar == 1 and kind == 'CHAR':
            if lastval != '\\':
                value = currentchar
                inchar = 0
                currentchar = ''
            else:
                currentchar = value
                continue



        
        if kind == 'LCOMS':
            #print('Started longcom at line ', line_num, ' col ', column)
            inlongcomment = 1
            continue
        elif kind == 'LCOME':
            inlongcomment = 0
            continue
        elif kind == 'COMMENT':
            #print('Found comment at line ', line_num)
            inshortcomment = 1 
            continue
        elif kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value.upper() in keywords:
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1 
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            #raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            continue
        #yield Token(kind, value, line_num, column)
        tokens.append(Token(kind, value, line_num, column))
    return tokens

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

file = getFileAsString('/home/kristian/byggern-nicer_code/adc_driver.c')

# for token in tokenize(file):
#     #print(token)
#     appendStringToFile('tokenizeroutput.txt', str(token) + '\n')

def getTokenDir(configfile):
    tokendirstring = getKeywordFromConfigFile(configfile, 'tokenDirectory')
    return tokendirstring

def tokenizeProject(configfile, projectfiles):
    tokensPerFile = {}
    tokenTextFileDirectory = getTokenDir(configfile)

    for file in projectfiles:
        tokens = []        
        tokenTextFileName = tokenTextFileDirectory + os.path.basename(file) + '.txt'

        for token in tokenizeCode(getFileAsString(file)):
            if tokenTextFileDirectory != '0':
                appendStringToFile(tokenTextFileName, str(token)+'\n')
            tokens.append(token)
        tokensPerFile[file] = tokens

    return tokensPerFile

