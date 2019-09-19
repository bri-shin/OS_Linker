# Operating System: Two Pass Linker

<i> Operating System 2019 Fall </i>

<i> Author: Seung Heon Brian Shin </i>



This program has two primary steps of processing the input:

1. The first pass finds the base address of each module and creates the symbol table. 
2. Utilizing the base addresses and the symbol table computed in the first pass, the second pass generates the output by relocating relative addresses and resolving external references.



##### Program Specifications:

<i> Programming Language Used: </i> Python 3



##### Error Specifications:

- If a symbol is multiply defined, the program prints an error message and use the value given in the first definition.
- If a symbol is used but not defined, the program prints an error message and use the value zero.
- If multiple symbols are listed as used in the same instruction, the program prints an error message and ignores all but the last usage given.
- If an address appearing in a definition exceeds the size of the module, the program prints an error message and treat the address as 0 (relative).
- If an immediate address (i.e., type 1) appears on a use list, the program prints an error message and treat the address as external
- If an external address is not on a use list, the program prints an error message and treats it as an immediate address.
- If an absolute address exceeds the size of the machine, the program prints an error message and use the largest legal value (i.e. 199).
- If the address component value exceeds 4, the program prints an error message and calls break.
- If the program text is greater than 5-digits, the program prints an error message and calls break.



##### How to run this program:

```shell
python3 TwoPassLinker.py < input-1
```

This program utilizes stdin to take input (text file) through redirection. The sample above is TwoPassLinker.py program taking 'input-1' text file as input.