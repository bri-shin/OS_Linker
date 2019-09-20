import sys

"""
Seung Heon (Brian) Shin
shs522@nyu.edu
N17816629

Two Steps for this Two Pass Linker:
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

# Receiving User Input through redirection
def getUserInput():
    inputArray = []
    for line in sys.stdin:
        inputArray.append(line)
    userInput = " ".join(inputArray)
    return userInput

def twoPassLinker(textInput):

    # Defining Variables
    definitions = {}
    programList = []
    indexCount = 1
    baseIncrement = 0

    inputList = textInput.split()

    # Converting datatype of numbers from str to int
    for i in range(len(inputList)):
        if inputList[i].isdigit():
            inputList[i] = int(inputList[i])

    moduleSize = inputList[0]

    # ----- Pass One -----
    for i in range(moduleSize):
            
        # Defining Variables 
        pairSize = inputList[indexCount]     
        m = inputList[indexCount+1+(2*pairSize)]
        instSize = inputList[indexCount+2+(2*pairSize)+(2*m)]-1

        indexCount += 1              
        for j in range(pairSize):

            # Error
            if inputList[indexCount] in definitions:
                print("Error: Variable {} multiply defined; first value used.".format(
                    inputList[indexCount]))

            elif (inputList[indexCount+1] > instSize) :
                print("Error: The definition of {} is outside module {}; zero (relative) used.".format(
                    inputList[indexCount], i))
                definitions[inputList[indexCount]
                            ] = baseIncrement

            else:
                definitions[inputList[indexCount]
                            ] = inputList[indexCount+1] + baseIncrement
            indexCount += 2           

        pairSize = inputList[indexCount]
        indexCount += (2*pairSize) + 1   

        pairSize = inputList[indexCount]
        indexCount += 1               
        baseIncrement += pairSize                     
        currentProgram = []
        for j in range(pairSize):            
            currentProgram.append(inputList[indexCount])
            indexCount += 1

        programList.append(currentProgram)        

    # ----- Pass Two -----

    # Defining Variables
    symbolList = []
    indexCount = 1
    passTwo = 0
    passTwoCount = 1
    baseIncrement = 0
    
    for i in range(moduleSize):

        pairSize = inputList[indexCount]     
        indexCount += (2*pairSize) + 1
        immediateAddressError=[]
        checker = [0] * (len(programList[i]))
        pairSize = inputList[indexCount]     
        indexCount += 1               
        
        for j in range(pairSize):                  

            if (programList[i][inputList[indexCount+1]] % 10 > 4):
                print("Error: Invalid Instruction code")
                break

            programDigit = programList[i][inputList[indexCount+1]] // 10
            symbol = inputList[indexCount]  
            addressField = programDigit % 1000
            isDefined = True

            # Error: not defined but used
            if symbol not in definitions:
                isDefined = False
                replace = 0

            else:
                symbolList.append(symbol)
                replace = definitions[symbol]           

            replaceIndex = inputList[indexCount+1]
        
            while(addressField != 777):
                if checker[replaceIndex] is not 0:
                    if checker[replaceIndex] == 777:
                        programDigit = programDigit - addressField + 777
                        addressField = 777
                        break
                    print("Error: Multiple Symbols used at Memory Map line {}".format(
                        replaceIndex + baseIncrement))

                checker[replaceIndex] = 1        
                if not isDefined:
                    print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                        symbol, replaceIndex + baseIncrement))  
                programDigit = programDigit - addressField + replace        

                if (programList[i][j] % 10 == 1):
                    print("Error: Immediate address on use list at Memory Map line {}; treated as External.".format(
                        passTwoCount))
                passTwoCount += 1

                programList[i][replaceIndex] = programDigit
                replaceIndex = addressField       
                programDigit = programList[i][addressField] // 10
                addressField = programDigit % 1000
                passTwoCount += 1

            if checker[replaceIndex] is not 0:
                print("Error: Multiple Symbols used in Memory Map line {}".format(
                    replaceIndex + baseIncrement))
            checker[replaceIndex] = 777
            programDigit = programDigit - addressField + replace
            programList[i][replaceIndex] = programDigit

            if not isDefined:
                print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                    symbol, replaceIndex + baseIncrement)) 
            indexCount += 2
            passTwoCount += 1

        pairSize = inputList[indexCount]
        indexCount += 1+pairSize

        for j in range(pairSize):
            instCode = (programList[i][j] % 10)
            address = (programList[i][j]//10)

            if (programList[i][j] > 9999) and (instCode == 3):
                if ((programList[i][j]//10) % 1000 > len(programList[i])-1):
                    print("Error: Relative Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, passTwo))
                    programList[i][j] -= address % 1000
                programList[i][j] = programList[i][j]+(baseIncrement*10)

            elif (programList[i][j] > 9999) and (instCode == 2):
                if (address % 1000) > 199:
                    print("Error: Absolute Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, passTwo))
                    programList[i][j] -= address % 1000
                    programList[i][j] += 199

            if (programList[i][j] > 9999) and (instCode == 4) and not((address) % 10 == replace):
                print("Error: E type address not on use chain at Memory Map line {}; treated as I type.".format(
                    passTwo))

            if programList[i][j] > 99999:
                print("Error: program exceeds 4 decimal digits")
                break

            if programList[i][j] > 9999:
                programList[i][j] = programList[i][j] // 10

            passTwo += 1
        baseIncrement += pairSize

    print("\nSymbol Table")
    symbolTable(definitions)
    print("\nMemory Map")
    memoryMap(programList)
    print("\n")
    for key, value in definitions.items():
        if key not in symbolList:
            print("Warning: {} was defined but never used.".format(key))
    return

# Priting the symbol table
def symbolTable(dictionary):
    for key, value in dictionary.items():
        print("{}={}".format(key, value))

# Printing memory map
def memoryMap(memoryMap):
    numbers = 0
    for moduleSize in memoryMap:
        for pair in moduleSize:
            print("{}: {}".format(numbers, pair))
            numbers += 1

textInput = getUserInput()
twoPassLinker(textInput)
