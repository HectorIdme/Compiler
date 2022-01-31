#!/bin/bash
g++ scanner.cpp -o scanner.exe
./scanner.exe tests/test5.txt
python parser.py