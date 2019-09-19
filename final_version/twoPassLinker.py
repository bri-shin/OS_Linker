import sys

"""
Seung Heon (Brian) Shin
shs522@nyu.edu
N17816629

1. The first pass finds the base address of each module and creates the symbol table. 

2. Utilizing the base addresses and the symbol table computed in the first pass, the 
second pass generates the actual output by relocating relative addresses and resolving 
external references.

Error Statements:
• (checked) If a symbol is defined but not used, print a warning message and continue.
• (checked) If a symbol is multiply defined, print an error message and use the value given in the first definition. 
• (needs recheck) If a symbol is used but not defined, print an error message and use the value zero.
• (checked) If multiple symbols are listed as used in the same instruction, print an error message and ignore all but the last usage
given.
• (checked) If an address appearing in a definition exceeds the size of the module, print an error message and treat the address
as 0 (relative).
• (checked) If an immediate address (i.e., type 1) appears on a use list, print an error message and treat the address as external
(i.e., type 4).
• (checked) If an external address is not on a use list, print an error message and treat it as an immediate address. ()
• (checked) If an absolute address exceeds the size of the machine, print an error message and use the largest legal value.
"""


def TwoPassLinker(textInput):

    inputList = textInput.split()

    # Converting datatype of numbers from str to int
    for i in range(len(inputList)):
        if inputList[i].isdigit():
            inputList[i] = int(inputList[i])

    moduleSize = inputList[0]
    currentIndex = 1
    definitions = {}
    programList = []

    offset = 0

    # ----- Pass One -----
    for i in range(moduleSize):
            
        # definition 
        pairSize = inputList[currentIndex]     
        m = inputList[currentIndex+1+(2*pairSize)]
        instSize = inputList[currentIndex+2+(2*pairSize)+(2*m)]-1

        currentIndex += 1              
        for j in range(pairSize):

            # Error
            if inputList[currentIndex] in definitions:
                print("Error: Variable {} multiply defined; first value used.".format(
                    inputList[currentIndex]))

            elif (inputList[currentIndex+1] > instSize) :
                print("Error: The definition of {} is outside module {}; zero (relative) used.".format(
                    inputList[currentIndex], i))
                definitions[inputList[currentIndex]
                            ] = offset

            else:
                definitions[inputList[currentIndex]
                            ] = inputList[currentIndex+1] + offset
            currentIndex += 2           

        # use list
        pairSize = inputList[currentIndex]
        currentIndex += 2*pairSize + 1   

        # program 
        pairSize = inputList[currentIndex]
        offset += pairSize                     
        currentIndex += 1               
        temp = []
        for j in range(pairSize):            
            temp.append(inputList[currentIndex])
            currentIndex += 1

        programList.append(temp)        

    currentIndex = 1
    offset = 0
    usedSymbols = []
    passTwo = 0
    secondPassCounter1 = 1
    
    # ----- Pass Two -----
    for i in range(moduleSize):

        # definition 
        pairSize = inputList[currentIndex]     
        currentIndex += 1 + 2*pairSize         

        # use list
        pairSize = inputList[currentIndex]     
        currentIndex += 1               
        changedElements = [False] * (len(programList[i]))
        immediateAddressError=[]

        for j in range(pairSize):
            num = programList[i][inputList[currentIndex+1]] // 10
            addressField = num % 1000                  

            if (programList[i][inputList[currentIndex+1]] % 10 > 4):
                print("Error: Invalid Instruction code")
                break

            symbol = inputList[currentIndex]  
            defined = True

            # Error: not defined but used
            if symbol not in definitions:
                replace = 0
                defined = False
            else:
                usedSymbols.append(symbol)
                replace = definitions[symbol]           

            replaceIndex = inputList[currentIndex+1]
        
            while(addressField != 777):
                if changedElements[replaceIndex] is not False:
                    if changedElements[replaceIndex] == 777:
                        num = num - addressField + 777
                        addressField = 777
                        break
                    print("Error: Multiple Symbols used at Memory Map line {}".format(
                        replaceIndex + offset))

                changedElements[replaceIndex] = True        
                if not defined:
                    print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                        symbol, replaceIndex + offset))  
                num = num - addressField + replace        

                if (programList[i][j] % 10 == 1):
                    print("Error: Immediate address on use list at Memory Map line {}; treated as External.".format(
                        secondPassCounter1))
                secondPassCounter1 += 1

                programList[i][replaceIndex] = num
                replaceIndex = addressField       
                num = programList[i][addressField] // 10
                addressField = num % 1000
                secondPassCounter1 += 1

            if changedElements[replaceIndex] is not False:
                print("Error: Multiple Symbols used in Memory Map line {}".format(
                    replaceIndex + offset))
            changedElements[replaceIndex] = 777
            num = num - addressField + replace
            programList[i][replaceIndex] = num

            if not defined:
                print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                    symbol, replaceIndex + offset)) 
            currentIndex += 2
            secondPassCounter1 += 1

        # definition 
        pairSize = inputList[currentIndex]
        currentIndex += 1+pairSize

        for j in range(pairSize):
            word = (programList[i][j] % 10)
            address = (programList[i][j]//10)

            if (programList[i][j] > 9999) and (word == 3):
                if ((programList[i][j]//10) % 1000 > len(programList[i])-1):
                    print("Error: Relative Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, passTwo))
                    programList[i][j] -= address % 1000
                programList[i][j] = programList[i][j]+(offset*10)

            elif (programList[i][j] > 9999) and (word == 2):
                if (address % 1000) > 199:
                    print("Error: Absolute Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, passTwo))
                    programList[i][j] -= address % 1000
                    programList[i][j] += 199

            if (programList[i][j] > 9999) and (word == 4) and not((address) % 10 == replace):
                print("Error: E type address not on use chain at Memory Map line {}; treated as I type.".format(
                    passTwo))

            if programList[i][j] > 99999:
                print("Error: program exceeds 4 decimal digits")
                break

            if programList[i][j] > 9999:
                programList[i][j] = programList[i][j] // 10


            passTwo += 1
        offset += pairSize

    print("\nSymbol Table")
    printDictionary(definitions)
    print("\nMemory Map")
    printMemoryMap(programList)
    print("\n")
    for key, value in definitions.items():
        if key not in usedSymbols:
            print("Warning: {} was defined but never used.".format(key))
    return

# User Input
def getUserInput():
    inputArray = []
    for line in sys.stdin:
        inputArray.append(line)
    userInput = " ".join(inputArray)
    return userInput

# Priting the symbol table
def printDictionary(dictionary):
    for key, value in dictionary.items():
        print("{}= {}".format(key, value))

# Printing memory table
def printMemoryMap(memoryMap):
    inc = 0
    for moduleSize in memoryMap:
        for pair in moduleSize:
            print("{}: {}".format(inc, pair))
            inc += 1

textInput = getUserInput()
TwoPassLinker(textInput)
