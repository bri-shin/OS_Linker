def TwoPassLinker(textInput):

    listInput = textInput.split()

    # modifies text input to a workable format
    for i in range(len(listInput)):
        if listInput[i].isdigit():
            listInput[i] = int(listInput[i])

    currentIndex = 0
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
                print("ERROR: Symbol {} multiply defined.".format(
                    listInput[currentIndex]))
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

    currentIndex = 0
    offset = 0
    usedSymbols = []
    secondPassCounter = 0

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
            symbol = listInput[currentIndex]  # symbol = z
            defined = True

            # Error
            if symbol not in definitions:
                replace = 111
                defined = False
            else:
                usedSymbols.append(symbol)
                replace = definitions[symbol]           # replace = 2

            # cI = 5 &   replaceIndex = 4
            replaceIndex = listInput[currentIndex+1]

            while(lastThree != 777):
                if changedElements[replaceIndex] is not False:
                    if changedElements[replaceIndex] == 777:
                        num = num - lastThree + 777
                        lastThree = 777
                        break
                    print("ERROR: Multiple Symbols used at Memory Map line {}".format(
                        replaceIndex + offset))

                changedElements[replaceIndex] = True        # cE[4] = True
                if not defined:
                    print("ERROR: Symbol {} used at Memory Map line {} but not defined.".format(
                        symbol, replaceIndex + offset))
                num = num - lastThree + replace             # 7002 - 2 + 2

                programText[i][replaceIndex] = num
                replaceIndex = lastThree                    # replaceIndex = 24

                num = programText[i][lastThree] // 10
                lastThree = num % 1000

            if changedElements[replaceIndex] is not False:
                print("ERROR: Multiple Symbols used at Memory Map line {}".format(
                    replaceIndex + offset))
            changedElements[replaceIndex] = 777
            num = num - lastThree + replace
            programText[i][replaceIndex] = num
            if not defined:
                print("ERROR: Symbol {} used at Memory Map line {} but not defined.".format(
                    symbol, replaceIndex + offset))  # problem here
            currentIndex += 2

        # definition line
        n = listInput[currentIndex]
        currentIndex += 1+n

        for j in range(n):
            word = (programText[i][j] % 10)
            address = (programText[i][j]//10)

            if word == 3:
                programText[i][j] = programText[i][j]+(offset*10)
                if ((programText[i][j]//10) % 1000 > len(programText[i])-1):
                    print("ERROR: Relative Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, secondPassCounter))
                    programText[i][j] -= address % 1000

            elif word == 2:
                if address % 1000 > 199:
                    print("ERROR: Absolute Address {} used at Memory Map line {} exceeds size of the machine.".format(
                        address, secondPassCounter))
                    programText[i][j] -= address % 1000
                    programText[i][j] += 199

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
            print("WARNING: {} symbol defined but not used.".format(key))

    return

# Takes User Input


def takeInput():
    inputArray = []
    print("Type input below.\n")
    global moduleSize
    moduleSize = int(input())
    print(moduleSize)
    inputSize = moduleSize*3
    try:
        for i in range(inputSize):
            inputArray.append(input())
    except EOFError:
        pass
    inputArray = " ".join(inputArray)
    return inputArray

# Prints a Dictionary


def printDictionary(dictionary):
    for key, value in dictionary.items():
        print("{}: {}".format(key, value))

# Prints the Memory Map


def printMemoryMap(map1):
    counter = 0
    for moduleSize in map1:
        for pair in moduleSize:
            print("{}: {}".format(counter, pair))
            counter += 1


moduleSize = 0
textInput = takeInput()
TwoPassLinker(textInput)
