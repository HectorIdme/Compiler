# Compiler
> Se presenta la implementación de un compilador compuesto por el frontend y backend para el lenguaje de programación Pascal.
> Para esta primera parte se presenta la implementación del analizador léxico.

El proyecto hasta el momento presenta los siguientes archivos:
- scanner.cpp : Scanner que revisara caracter por caracter para obtener los tokens, asi como errores y trabajar con saltos y comentarios.
- tokens.h : Encabezado donde se presenta la estructura del Token así como estructuras que almacenan símbolos y palabras permitidos para el lenguaje
- tests : Carpeta donde se encuentran los test para el scanner
- scanner.exe : Ejecutable del scanner
- tokens_ans.txt : Archivo donde se escribira el resultado del test, o sea la lista de los tokens con los errores identificados

## Instalación y Ejecución
```
git clone https://github.com/HectorIdme/Compiler.git
cd Compiler
g++ scanner.cpp -o scanner.exe
./scanner.exe <file with test (tests/test.txt)>
```

