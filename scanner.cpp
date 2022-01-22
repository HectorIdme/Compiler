#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <vector>
#include <limits>
#include <sstream>
#include <string>
#include <iomanip>
#include "tokens.h"

using namespace std;

struct LexicalError{
    string word;
    int line;
    bool problem;

    LexicalError(string w,int l,bool p=1){
        word = w;
        line = l;
        problem = p;
    }

    string toString(){
        string s;
        if(problem) s = "Error en la linea "+to_string(line)+ " no se reconoce "+word+"\n";
        else s = "Error en la linea "+to_string(line)+ " se produjo overflow\n";
        return s;
    }

    void getError(ofstream &f){
        f<<toString();
    }

};


char getChar(string line,int &pos,bool op=1){
    if(op) return line[pos];
    return line[++pos];
}

char peek1Char(string line,int pos){
    if(pos+1 == line.size()) return ' ';
    return line[pos+1];
}

char peek2Char(string line,int pos){
    if(pos+2 == line.size()) return ' ';
    return line[pos+2];
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



int main(int argc, char** argv){

    string line;
    string word = "";
    string type_token = "";
    int num_line = 1;
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
    bool doubleType = false;

    vector<LexicalError> errors;
    ifstream fileRead(argv[1]);
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
                    else if(peek1Char(line,pos) == '=')
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
                    }

                    //Verificar que se obtuve valor completo del token 
                    char tmp_letter = peek1Char(line,pos);

                    if(type_token == "ID"){
                        //Se completo si el siguiente caracter es ' ' o algun simbolo o palabra especial del lenguaje Pascal
                        if(tmp_letter == ' ' || words.find(string(1,tmp_letter)) != words.end() || tmp_letter == '\''){
                            if(error_id){
                                errors.push_back(LexicalError(word,num_line));
                                error_id = false;
                            }
                            else{
                                getToken(type_token,word,fileWrite);
                            }
                            word.clear();
                        }
                    
                    }
                    else if(type_token == "NUM"){
                        
                        if(letter == 'e' || letter == 'E') e_num = true;

                        //Se completo si el siguiente caracter es ' ' o algun simbolo o palabra especial del lenguaje Pascal
                        if(tmp_letter == ' ' || words.find(string(1,tmp_letter)) != words.end() || tmp_letter == '\''){
                                
                                if(tmp_letter != '.'){
                                    if(e_num){
                                        if(tmp_letter == '+' || tmp_letter == '-') 
                                            e_num = false;
                                    }
                                    else{
                                        try{
                                            if(doubleType){
                                                double x = stod(word);
                                                doubleType = false;

                                                double y;
                                                stringstream ss1;
                                                ss1 << word;
                                                ss1 >> y;

                                                ostringstream ss2;
                                                ss2 << setprecision(10)<<y;
                                                word = ss2.str(); 
                                                
                                            }else{
                                                unsigned long int x = stoul(word);
                                                stringstream ss2;
                                                ss2<<x;
                                                word = ss2.str();
                                            }

                                            if(error_num){
                                                errors.push_back(LexicalError(word,num_line));
                                                error_num = false;
                                            }
                                            else{
                                                getToken(type_token,word,fileWrite);
                                            }

                                        }catch(out_of_range& e){
                                            errors.push_back(LexicalError(word,num_line,0));
                                            error_num = false;
                                        }
                                        word.clear();
                                        e_num = false;
                                    }
                                    if(tmp_letter == ' ' && e_num ){
                                        try{
                                            if(doubleType){
                                                double x = stod(word);
                                                doubleType = false;

                                                double y;
                                                stringstream ss1;
                                                ss1 << word;
                                                ss1 >> y;

                                                ostringstream ss2;
                                                ss2 << setprecision(10)<<y;
                                                word = ss2.str(); 
                                                
                                            }else{
                                                unsigned long int x = stoul(word);
                                                stringstream ss2;
                                                ss2<<x;
                                                word = ss2.str();
                                            }

                                            if(error_num){
                                                errors.push_back(LexicalError(word,num_line));
                                                error_num = false;
                                            }
                                            else{
                                                getToken(type_token,word,fileWrite);
                                            }

                                        }catch(out_of_range& e){
                                            errors.push_back(LexicalError(word,num_line,0));
                                            error_num = false;
                                        }
                                        word.clear();
                                        e_num = false;
                                    }

                                }
                                if(error_num){
                                    errors.push_back(LexicalError(word,num_line));
                                    error_num = false;
                                    word.clear();
                                }
                        }
                        if(tmp_letter == '.' || tmp_letter == 'e' || tmp_letter == 'E'){
                            char tmp_letter2 = peek2Char(line,pos);
                            if(tmp_letter2 != '.')
                                doubleType = true;
                            else{
                                getToken(type_token,word,fileWrite);
                                word.clear();
                            }
                        }


                    }
                    else if(type_token == "STRING"){

                        if(letter == '\''){
                            //Verificar la cantidad de ' en el string para ver si esta bien o es erroneo
                            if(tmp_letter == '\'' || exp_string){
                                num_exp_string++;
                                exp_string = true;

                                if(num_exp_string==2){
                                    exp_string = false;
                                    num_exp_string = 0;
                                    word.pop_back();
                                }
                            }
                            else{
                                vstring = false;
                                if(error_string){
                                    errors.push_back(LexicalError(word,num_line));
                                    error_string = false;
                                }
                                else{
                                    getToken(type_token,word,fileWrite);
                                }
                                word.clear();
                            }
                        } 

                    }
                        
                }
            }
            pos++;
        }
        num_line++;
    }

    if(vstring){
        vstring = false;
        error_string = false;
        errors.push_back(LexicalError(word,--num_line));
        word.clear();
    }

    for(int i=0;i<errors.size();i++){
        errors[i].getError(fileWrite);
    }
    
    fileRead.close();
    fileWrite.close();

    return 0;
}