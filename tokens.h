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
        s = "<"+type+","+val+">\n";
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
    

    {"array","RESERVED_WORD"},
    {"begin","RESERVED_WORD"},
    {"case","RESERVED_WORD"},
    {"const","RESERVED_WORD"},
    {"do","RESERVED_WORD"},
    {"downto","RESERVED_WORD"},
    {"else","RESERVED_WORD"},
    {"end","RESERVED_WORD"},
    {"file","RESERVED_WORD"},
    {"for","RESERVED_WORD"},
    {"function","RESERVED_WORD"},
    {"goto","RESERVED_WORD"},
    {"if","RESERVED_WORD"},
    {"label","RESERVED_WORD"},
    {"nil","RESERVED_WORD"},
    {"of","RESERVED_WORD"},
    {"packed","RESERVED_WORD"},
    {"procedure","RESERVED_WORD"},
    {"program","RESERVED_WORD"},
    {"record","RESERVED_WORD"},
    {"repeat","RESERVED_WORD"},
    {"set","RESERVED_WORD"},
    {"then","RESERVED_WORD"},
    {"to","RESERVED_WORD"},
    {"type","RESERVED_WORD"},
    {"until","RESERVED_WORD"},
    {"var","RESERVED_WORD"},
    {"while","RESERVED_WORD"},
    {"with","RESERVED_WORD"},
    
};
 
