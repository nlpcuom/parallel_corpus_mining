# lines = open("en-ta.txt").readlines()

# en = []
# ta = []

# with open("existingdictionary.en", "w") as enDicFile:
#     with open("existingdictionary.ta", "w") as taDicFile:
#         for line in lines:
#             entawords = line.strip().replace("\n", "").split()
#             enDicFile.write(entawords[0] + "\n")
#             taDicFile.write(entawords[1] + "\n")

enwords = open("existingdictionary.en").readlines()

lines = open("ta-en.txt", "r").readlines()

for i in range(len(enwords)):
    enwords[i] = enwords[i].replace("\n", "")

x = 1
for line in lines:
    if (line.replace("\n", "").strip().split()[1] not in enwords):
        print(line)
        x = x + 1

# print(enwords)