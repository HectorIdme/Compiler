#include <iostream>
#include <map>
#include <set>
#include <utility>
#include <string>

using namespace std;


struct Token{
    string type;
    string val;

    Token(string t,string v){
        type = t;
        val = v;
    }

    string toString(){
        string s;
        s = "<"+type+"|"+val+">\n";
        return s;
    }
};


set <char> alphabet = {'a','b','c','d','e','f','g','h','i','j',
                        'k','l','m','n','o','p','r','s','t','u',
                        'v','w','x','y','z',
                        'A','B','C','D','E','F','G','H','I','J',
                        'K','L','M','N','O','P','R','S','T','U',
                        'V','W','X','Y','Z'
                    };

set <char> digits = {'0','1','2','3','4','5','6','7','8','9'};

set <char> num = {'0','1','2','3','4','5','6','7','8','9','.','+','-','e','E'};

map<string,string> words{
    {"+","OP_SUM"},
    {"-","OP_RES"},
    {"*","OP_MULT"},
    {"/","OP_DIVIS"},
    {":=","OP_ASSG"},
    {"=","OP_EQ"},
    {"<>","OP_NOT_EQ"},
    {"<","OP_LESS"},
    {"<=","OP_LESS_EQ"},
    {">=","OP_GRT_EQ"},
    {">","OP_GRT"},
    {"^","OP_POW"},
    {".","OP_POINT"},
    {"and","OP_AND"},
    {"or","OP_OR"},
    {"not","OP_NOT"},
    {"div","OP_DIV"},
    {"mod","OP_MOD"},
    {"in","OP_IN"},

    {",","DEL_COMMA"},
    {";","DEL_SEMICOLON"},
    {":","DEL_TWOPOINT"},
    {"(","DEL_LT_PARNT"},
    {")","DEL_RT_PARNT"},
    {"[","DEL_LT_CORCH"},
    {"]","DEL_RT_CORCH"},
    {"..","DEL_DBL_POINT"},
    

    {"array","ARRAY"},
    {"begin","BEGIN"},
    {"case","CASE"},
    {"const","CONST"},
    {"do","DO"},
    {"downto","DOWNTO"},
    {"else","ELSE"},
    {"end","END"},
    {"file","FILE"},
    {"for","FOR"},
    {"function","FUNCTION"},
    {"goto","GOTO"},
    {"if","IF"},
    {"label","LABEL"},
    {"nil","NIL"},
    {"of","OF"},
    {"packed","PACKED"},
    {"procedure","PROCEDURE"},
    {"program","PROGRAM"},
    {"record","RECORD"},
    {"repeat","REPEAT"},
    {"set","SET"},
    {"then","THEN"},
    {"to","TO"},
    {"type","TYPE"},
    {"until","UNTIL"},
    {"var","VAR"},
    {"while","WHILE"},
    {"with","WITH"},
    {"write","WRITE"},
    {"writeln","WRITELN"},
    {"until","UNTIL"},
    {"continue","CONTINUE"},
    {"break","BREAK"}
};
 
map<string,string> keyWords{
    {"array","ARRAY"},
    {"begin","BEGIN"},
    {"case","CASE"},
    {"const","CONST"},
    {"do","DO"},
    {"downto","DOWNTO"},
    {"else","ELSE"},
    {"end","END"},
    {"file","FILE"},
    {"for","FOR"},
    {"function","FUNCTION"},
    {"goto","GOTO"},
    {"if","IF"},
    {"label","LABEL"},
    {"nil","NIL"},
    {"of","OF"},
    {"packed","PACKED"},
    {"procedure","PROCEDURE"},
    {"program","PROGRAM"},
    {"record","RECORD"},
    {"repeat","REPEAT"},
    {"set","SET"},
    {"then","THEN"},
    {"to","TO"},
    {"type","TYPE"},
    {"until","UNTIL"},
    {"var","VAR"},
    {"while","WHILE"},
    {"with","WITH"},
    {"write","WRITE"},
    {"writeln","WRITELN"},
    {"until","UNTIL"},
    {"continue","CONTINUE"},
    {"break","BREAK"},

    {"and","OP_AND"},
    {"or","OP_OR"},
    {"not","OP_NOT"},
    {"div","OP_DIV"},
    {"mod","OP_MOD"},
    {"in","OP_IN"}
};

map <string,string> operators{
    {",","DEL_COMMA"},
    {";","DEL_SEMICOLON"},
    {":","DEL_TWOPOINT"},
    {"(","DEL_LT_PARNT"},
    {")","DEL_RT_PARNT"},
    {"[","DEL_LT_CORCH"},
    {"]","DEL_RT_CORCH"},
    {"..","DEL_DBL_POINT"},
    {"+","OP_SUM"},
    {"-","OP_RES"},
    {"*","OP_MULT"},
    {"/","OP_DIVIS"},
    {":=","OP_ASSG"},
    {"=","OP_EQ"},
    {"<>","OP_NOT_EQ"},
    {"<","OP_LESS"},
    {"<=","OP_LESS_EQ"},
    {">=","OP_GRT_EQ"},
    {">","OP_GRT"},
    {"^","OP_POW"},
    {".","OP_POINT"},
};