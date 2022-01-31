# Compiler
> Se presenta la implementación de un compilador compuesto por el frontend y backend para el lenguaje de programación Pascal.
> Primera parte se presenta la implementación del analizador léxico.
> Segunda parter se presenta la implementación del parser.

El proyecto hasta el momento presenta los siguientes archivos:
- scanner.cpp : Scanner que revisara caracter por caracter para obtener los tokens, asi como errores y trabajar con saltos y comentarios.
```
Funciones importantes:
- getChar(string,int,bool) : Lee el caracter de la entrada y puede o no mover el puntero
- peek1Char(string,int) : Lee el siguiente caracter sin mover el puntero
- peek2Char(string,int) : Lee el siguiente-siguiente caracter sin mover el puntero
- getToken(map<string,string>::iterator,ofstream) : Crea el token y lo escribe en el archivo
- getToken(string,string,ofstream) : Crea el token y lo escribe en el archivo 
```
- tokens.h : Encabezado donde se presenta la estructura del Token **<token_type,token_value>**  así como estructuras que almacenan símbolos y palabras permitidos para el lenguaje
- tests : Carpeta donde se encuentran los test para el scanner
- scanner.exe : Ejecutable del scanner
- tokens_ans.txt : Archivo donde se escribira el resultado del test, o sea la lista de los tokens con los errores identificados
- requirements.txt : Para instalar las dependencias de python
- parser.py : Parser que hara uso de los tokens y la gramática asignada

## Instalación y Ejecución
```
instalar Graphviz en su ordenador
git clone https://github.com/HectorIdme/Compiler.git
cd Compiler
pip install -r requirements.txt
g++ scanner.cpp -o scanner.exe
./scanner.exe <file with test (tests/test.txt)>
python parser.py
```

