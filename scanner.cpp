#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include "tokens.h"

using namespace std;



char getChar(string line,int &pos,bool op=1){
    if(op) return line[pos];
    return line[++pos];
}

char peek1Char(string line,int pos){
    if(pos+1 == line.size()) return ' ';
    return line[pos+1];
}

void getToken(map<string,string>::iterator it,ofstream &f){
    Token t(it->second,it->first);
    t.toString();
    f<<t.toString();
}

void getToken(string type, string value,ofstream &f){
    Token t(type,value);
    t.toString();
    f<<t.toString();
}



int main(){

    string line;
    string word = "";
    string type_token = "";
    char letter;
    int pos;
    bool comment = false;
    bool vstring = false;
    bool exp_string = false;
    int num_exp_string = 0;
    bool e_num = false;
    int cont_sim = 0;

    bool error_id = false;
    bool error_num = false;
    bool error_string = false;


    ifstream fileRead("tests/test4.txt");
    ofstream fileWrite;
    fileWrite.open("tokens_ans.txt",ios::out);
    

    //leyendo lineas
    while(getline(fileRead,line)){
        pos = 0;

        //leyendo caracteres
        while(pos!=line.size()){

            letter = getChar(line,pos);
            
            //Espacios en blanco y comentarios
            if(letter == ' ' || letter == '\t'){
                if(!vstring){
                    word.clear();
                    pos++;
                    continue;
                }
            }
            else if(letter == '{'){
                comment = true;
                pos++;
                continue;
            } 
            else if(letter == '}' && comment) {
                comment = false;
                pos++;
                continue;
            }
            else if(letter == '('){
                if(peek1Char(line,pos) == '*') {
                    getChar(line,pos,0);
                    comment = true;
                    pos++;
                    continue;
                }
            }
            else if(letter == '*'){
                if(peek1Char(line,pos) == ')') {
                    getChar(line,pos,0);
                    comment = false;
                    pos++;
                    continue;
                }
            }


            //Obteniendo tokens
            if(!comment){
                word += letter;


                //verificando operadores de dos simbolos
                if(word == ":"){
                    if(peek1Char(line,pos) == '=')
                        word += getChar(line,pos,0);
                }
                else if(word == "<"){
                    if(peek1Char(line,pos) == '>') 
                        word += getChar(line,pos,0);
                }
                else if(word == "<"){
                    if(peek1Char(line,pos) == '=') 
                        word += getChar(line,pos,0);
                }
                else if(word == ">"){
                    if(peek1Char(line,pos) == '=') 
                        word += getChar(line,pos,0);
                    
                }
                else if(word == "."){
                    if(peek1Char(line,pos) == '.') 
                        word += getChar(line,pos,0);
                }
                else if(word == "do"){
                    if(peek1Char(line,pos) == 'w') 
                        word += getChar(line,pos,0);
                }

                auto it = words.find(word);

                //verificando si token en palabras definidas
                if(it != words.end()){
                    getToken(it,fileWrite);
                    word.clear();
                }

                //verificando si token posible ID,String,Number
                else{

                    //identificando tipo de token
                    if(word.size()==1){
                        if( digits.find(letter) != digits.end())
                            type_token = "NUM"; 
                        else if( alphabet.find(letter) != alphabet.end())
                            type_token = "ID";
                        else if( letter == '\''){
                            type_token = "STRING";
                            vstring = true;
                            pos++;
                            continue;
                        }   
                    }
                    

                    //Identificando errores en el token
                    if(type_token == "ID"){
                        if( digits.find(letter) == digits.end() && alphabet.find(letter) == alphabet.end())
                            error_id = true;
                    }
                    else if(type_token == "NUM"){
                        if( num.find(letter) == num.end())
                            error_num = true;

                        else if(letter == '+' || letter == '-'){
                            if( digits.find(peek1Char(line,pos)) == digits.end())
                                error_num = true;
                        }
                    }



                    //Verificar que se obtuve valor completo del token 
                    char tmp_letter = peek1Char(line,pos);

                    if(type_token == "ID"){
                        if(tmp_letter == ' ' || words.find(string(1,tmp_letter)) != words.end()){
                            if(error_id){
                                type_token = "ERROR";
                                error_id = false;
                            }
                            getToken(type_token,word,fileWrite);
                            word.clear();
                        }
                    
                    }
                    else if(type_token == "NUM"){
                        
                        if(letter == 'e' || letter == 'E') e_num = true;

                        else if(letter == '+' || letter == '-'){
                            if(e_num) cont_sim++;
                        }

                        else if(tmp_letter == ' ' || words.find(string(1,tmp_letter)) != words.end()){
                                if(tmp_letter != '.'){
                                    if(error_num){
                                        type_token = "ERROR";
                                        error_num = false;
                                    }
                                    getToken(type_token,word,fileWrite);
                                    word.clear();

                                    cont_sim = 0;
                                    e_num = false;
                                }
                        }
                    }
                    else if(type_token == "STRING"){

                        if(letter == '\''){
                            if(tmp_letter == '\'' || exp_string){
                                num_exp_string++;
                                exp_string = true;

                                if(num_exp_string==2 && tmp_letter != '\''){
                                    exp_string = false;
                                    num_exp_string = 0;
                                }
                                if(num_exp_string>2){
                                    error_string = true;
                                    if(tmp_letter != '\''){
                                        exp_string = false;
                                        num_exp_string = 0;
                                    }
                                }
                            }
                            else{
                                vstring = false;
                                if(error_string){
                                    type_token = "ERROR";
                                    error_string = false;
                                }
                                getToken(type_token,word,fileWrite);
                                word.clear();
                            }
                        } 

                    }
                        
                }
            }
            pos++;
        }


    } 
    
    fileRead.close();
    fileWrite.close();

    return 0;
}