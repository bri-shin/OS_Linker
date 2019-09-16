/*
Seung Heon (Brian) Shin
shs522@nyu.edu
N17816629
*/

#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <string>
#include <stdio.h>
#include <sstream>
using namespace std;

/*
The two-pass linker consists of two parts:

1. The first pass finds the base address of each module and creates the symbol table. 

2. Utilizing the base addresses and the symbol table computed in the first pass, the 
second pass generates the actual output by relocating relative addresses and resolving 
external references.
*/

int main()
{
    map<int, int> numbers;
    char s[100];
    int numOfLines;
    cin >> numOfLines;
    for (int i; i < numOfLines * 3; i++)
    {
        scanf("", s);
    }
    printf("%s", s);
    return 0;
}