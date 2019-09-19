import sys

"""
Error Statements:
• (checked) If a symbol is defined but not used, print a warning message and continue.
• (checked) If a symbol is multiply defined, print an error message and use the value given in the first definition. 
• (needs recheck) If a symbol is used but not defined, print an error message and use the value zero.
• (checked) If multiple symbols are listed as used in the same instruction, print an error message and ignore all but the last usage
given.
• (checked) If an address appearing in a definition exceeds the size of the module, print an error message and treat the address
as 0 (relative).
• If an immediate address (i.e., type 1) appears on a use list, print an error message and treat the address as external
(i.e., type 4).
• (checked) If an external address is not on a use list, print an error message and treat it as an immediate address. ()
• (checked) If an absolute address exceeds the size of the machine, print an error message and use the largest legal value.
"""


def TwoPassLinker(textInput):

    listInput = textInput.split()

    # modifies text input to a workable format
    for i in range(len(listInput)):
        if listInput[i].isdigit():
            listInput[i] = int(listInput[i])

    moduleSize = listInput[0]

    currentIndex = 1
    definitions = {}
    programText = []
    offset = 0

    # ----- Pass One -----
    for i in range(moduleSize):

        # definition line
        n = listInput[currentIndex]     # n = 1,0,0,1
        currentIndex += 1               # currentIndex = 1,13,24,31
        for j in range(n):

            # Error
            if listInput[currentIndex] in definitions:
                print("Error: Symbol {} multiply defined; first value used.".format(
                    listInput[currentIndex]))

            if listInput[currentIndex+1] > listInput[currentIndex+(2*n+1)-1]:
                print("Error: The definition of {} is outside module {}; zero (relative) used.".format(
                    listInput[currentIndex], i))
                definitions[listInput[currentIndex]
                            ] = offset
            else:
                definitions[listInput[currentIndex]
                            ] = listInput[currentIndex+1] + offset
            currentIndex += 2           # currentIndex = 3,n,n,33

        # use line
        # currentIndex = 3,13,24,33 &   n = 1,1,1,1
        n = listInput[currentIndex]
        currentIndex += 2*n + 1            # currentIndex = 6, 16, 27, 36

        # program text
        # currentIndex = 6 ,16, 27, 36 &   n = 5,6,2,3
        n = listInput[currentIndex]
        offset += n                     # offset = 5,11,13,16
        currentIndex += 1               # currentIndex = 7,17,28,37
        temp = []
        for j in range(n):            # n-1 = 4,5,1,2
            # temp.append(listInput[currentIndex:currentIndex+2])
            temp.append(listInput[currentIndex])
            currentIndex += 1

        programText.append(temp)        # current Index = 12, 23, 30

    currentIndex = 1
    offset = 0
    usedSymbols = []
    secondPassCounter = 0
    secondPassCounter1 = 0
    # unusedSymbolMod = []

    # ----- Pass Two -----
    for i in range(moduleSize):

        # definition line
        n = listInput[currentIndex]     # cI = 0    ;   n = 1
        currentIndex += 1 + 2*n         # cI = 3,

        # use line
        n = listInput[currentIndex]     # n = 1
        currentIndex += 1               # cI = 4
        changedElements = [False] * (len(programText[i]))

        for j in range(n):
            # cI= 5 -> 4   ; num = 70024
            num = programText[i][listInput[currentIndex+1]] // 10
            lastThree = num % 1000                  # lastThree= 2

            if (programText[i][listInput[currentIndex+1]] % 10 > 4):
                print("Error: Invalid Instruction code")
                break

            symbol = listInput[currentIndex]  # symbol = z
            defined = True

            # Error: not defined but used
            if symbol not in definitions:
                replace = 0
                defined = False
                # unusedSymbolMod.append(i)

            else:
                usedSymbols.append(symbol)
                replace = definitions[symbol]           # replace = 2

            # cI = 5 &   replaceIndex = 4
            replaceIndex = listInput[currentIndex+1]
            # print("First replace Index is", replaceIndex)

            while(lastThree != 777):
                if changedElements[replaceIndex] is not False:
                    if changedElements[replaceIndex] == 777:
                        num = num - lastThree + 777
                        lastThree = 777
                        break
                    print("Error: Multiple Symbols used at Memory Map line {}".format(
                        replaceIndex + offset))

                changedElements[replaceIndex] = True        # cE[4] = True
                if not defined:
                    print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                        symbol, replaceIndex + offset))  # replaceIndex + offset
                num = num - lastThree + replace             # 7002 - 2 + 2

                if (programText[i][j] % 10 == 1):
                    print("Error: Immediate address on use list at Memory Map line {}; treated as External.".format(
                        secondPassCounter1))

                programText[i][replaceIndex] = num
                replaceIndex = lastThree                    # replaceIndex = 24
                num = programText[i][lastThree] // 10
                lastThree = num % 1000
                secondPassCounter1 += 1

            if changedElements[replaceIndex] is not False:
                print("Error: Multiple Symbols used in Memory Map line {}".format(
                    replaceIndex + offset))
            changedElements[replaceIndex] = 777
            num = num - lastThree + replace
            programText[i][replaceIndex] = num

            if not defined:
                print("Error: {} used at Memory Map line {} but not defined; zero used".format(
                    symbol, replaceIndex + offset))  # problem here
            currentIndex += 2
            secondPassCounter1 += 1

        # definition line
        n = listInput[currentIndex]
        currentIndex += 1+n

        for j in range(n):
            word = (programText[i][j] % 10)
            address = (programText[i][j]//10)

            # if (word

            if (programText[i][j] > 9999) and (word == 3):
                if ((programText[i][j]//10) % 1000 > len(programText[i])-1):
                    print("Error: Relative Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, secondPassCounter))
                    programText[i][j] -= address % 1000
                programText[i][j] = programText[i][j]+(offset*10)

            elif (programText[i][j] > 9999) and (word == 2):
                if (address % 1000) > 199:
                    print("Error: Absolute Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, secondPassCounter))
                    programText[i][j] -= address % 1000
                    programText[i][j] += 199

            if (programText[i][j] > 9999) and (word == 4) and not((address) % 10 == replace):
                print("Error: E type address not on use chain at Memory Map line {}; treated as I type.".format(
                    secondPassCounter))

            if programText[i][j] > 9999:
                programText[i][j] = programText[i][j] // 10

            secondPassCounter += 1
        offset += n

    # Printing everything
    print("\nSymbol Table:")
    printDictionary(definitions)
    print("\nMemory Map:")
    printMemoryMap(programText)
    print("\n")
    for key, value in definitions.items():
        if key not in usedSymbols:
            print("Warning: {} was defined but never used.".format(key))

    return

# Takes User Input


def takeInput():
    inputArray = []
    inputName = input("Please type the input file name:")
    with open(inputName) as fileName:
        userInput = fileName.read()
    return userInput

# Prints a Dictionary


def printDictionary(dictionary):
    for key, value in dictionary.items():
        print("{}= {}".format(key, value))

# Prints the Memory Map


def printMemoryMap(map1):
    counter = 0
    for moduleSize in map1:
        for pair in moduleSize:
            print("{}: {}".format(counter, pair))
            counter += 1


textInput = takeInput()
TwoPassLinker(textInput)
