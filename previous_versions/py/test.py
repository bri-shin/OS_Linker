inputName = input("Please type the input file name:")
# file1 = str(open(inputName,"r"))
# # print(type(file1))
# print(file1)


with open(inputName) as fileName:
    userInput = fileName.read()
print(userInput)