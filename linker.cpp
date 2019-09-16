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

    ifstream input;                      // Input File
    string inputName;                    // Input File Name
    static int modNum = 0;               // Total number of modules
    static map<string, int> symbolTable; // Final Symbol Table
    static int addressOffset = 0;        // Offset for addresses
    static vector<int> baseAddress;      // Stores base address of modules
    // static vector<(vector<int>)> inputList;                   // 2-D Arraylist of inputs

    cout << "Please enter the name of the input file: ";
    cin >> inputName;
    input.open(inputName.c_str());

    // cout << input;
}
// ----- First Pass: Symbol Table and Base Addresses -----

// static void firstPass(ifstream input) {
//     int lineCount=0 , absAddress, offset, mod;
//     std::vector<std::int> symbols;
//     std::vector<std::int> uses;
//     std::vector<std::int> tokens;
//     char curr;                                  // Current character
//     string delimiter = ("\\s+")

// // While file is open
// if(input.is_open(){
//     while(input >> words){
//         // Storing input into an array and splitting all white spaces (removing empty line)
//         string currentLine = input.next();
//         tokens = currentLine.split(delimiter)

//         for(int i; i< tokens.length; i++) {
//             if(!"".equals(tokens[i])) {
//                 tokens
//             }
//         }
//     }
// }

//     }

// }

// int main()
// {
//     ifstream input;

//     string inputName, words, flag, flagbase;
//     char ch;

//     int countL, countM, countML, i, base;

//     cout << "Symbole Table \n"
//     int definitions;
//     int baseAddress;
//     int moduleSize;
//     string symbols;
//     int

//     i = 1;
//     base = 0;
//     countL = 1;  //line counter
//     countML = 1; //line counter inside module
//     countM = 1;  //module counter

//     if (input.is_open())
//     {
//         while (input >> words)
//         {
//             cout << words << endl;
//             input.get(ch);

//             if (flag == "progtext" && flagbase != "done")
//             {
//                 // i am trying to find a way to convert the result from in.get(ch) to int and store it to base
//                 baseAddress[countM] = base;
//                 cout << "test " << base << endl;
//                 flagbase = "done"; //the computing of the base address of the current module is done
//             }
//             if (ch == '\n')
//             {
//                 countL++;
//                 countML++;
//                 cout << "new line " << countM << "." << countML << endl;

//                 switch (countML)
//                 { //keep track of the current module list
//                 case 1:
//                     flag = "deflist";
//                     break;
//                 case 2:
//                     flag = "uselist";
//                     break;
//                 case 3:
//                     flag = "progtext";
//                     break;
//                 }

//                 if (countL % 3 == 0)
//                 { //each module has 3 lines
//                     countM++;
//                     flagbase = " "; //i reset the flag
//                 }
//                 if (countML == 3) //each module has 3 lines, so i initialize the module line counter every 3 lines
//                     countML = 0;
//             }
//         }
//         input.close();
//         for (i; i <= baseAddress.size(); i++)
//         { //just print the contents
//             cout << "size " << baseAddress.size() << endl;
//             cout << "base " << baseAddress[i] << endl;
//         }
//     }
//     else
//         cout << "Unable to open file" << endl;
//     return 0;
// }