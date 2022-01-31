#!/bin/bash
g++ scanner.cpp -o scanner.exe
./scanner.exe $1
python parser.py