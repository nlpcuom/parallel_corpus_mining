import inputpaths

#enDesigList = []
#siDesigList = []

#desigDic = {}

############# not needed

# def calcDictionaryWeight(fileA, fileB, pathA, pathB, wordDictionary):
#     docA = open(pathA.replace("Embeddings", "Data-Formatted") + fileA.replace("raw", "txt"), "r")
#     docB = open(pathB.replace("Embeddings", "Data-Formatted") + fileB.replace("raw", "txt"), "r")
#     enLines = docA.readlines()
#     siLines = docB.readlines()
#     enWords = []
#     siWords = []
#     for enLine in enLines:
#         enWords = enWords + enLine.split()
#     for siLine in siLines:
#         siWords = siWords + siLine.split()
#     for i in range(len(enWords)):
#         enWords[i] = enWords[i].strip().replace(".", "").replace(",", "").lower()
#     for i in range(len(siWords)):
#         siWords[i] = siWords[i].strip().replace(".", "").replace(",", "")
#     count = 1
#     for enWord in enWords:
#         value = wordDictionary.get(enWord, False)
#         if (value != False):
#             if (value in siWords):
#                 count = count + 1
#                 siWords.remove(value)
#                 # print("en word: ", enWord, "si word: ", value)
#     # return ((len(siWords) + len(enWords)) / (count * 2))
#     # return ((count * 2) / (len(siWords) + len(enWords)))
#     if (count > 10):
#         # print(count)
#         # print(enWords)
#         # print(siWords)
#         # print()
#         return 0.2
#     elif (count > 8):
#         return 0.4
#     elif (count > 6):
#         return 0.6
#     elif (count > 4):
#         return 0.8
#     else:
#         return 1
#     # return 1/count

# def checkDesignations(enLine, siLine):
#     count = 1
#     for i in range(len(enDesigList)):
#         if (enDesigList[i] in enLine):
#             if (siDesigList[i] in siLine):
#                 count = count + len(enDesigList[i])
#                 print(count)
#                 print(enDesigList[i], siDesigList[i])
#     return count

############# not needed end


# # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/designation.en", "r") as tempfile1:
# # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/designation.en", "r") as designationsFileA:
# # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/parallel-designations-term1-tr.cl.si-ta.si", "r") as tempfile1:
# with open(inputpaths.designationsA) as designationsFileA:
#     # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/designation.si", "r") as tempfile2:
#     # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/designation.ta", "r") as designationsFileB:
#     # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/parallel-designations-term1-tr.cl.si-ta.ta", "r") as tempfile2:
#     with open(inputpaths.designationsB) as designationsFileB:
#         linesA = designationsFileA.readlines()
#         linesB = designationsFileB.readlines()
#         # for line in enlines:
#         #     enDesigList.append(line.strip().replace("\n", "").lower())
#         # for line in silines:
#         #     siDesigList.append(line.strip().replace("\n", "").lower())
#         for i in range(len(linesA)):
#             desigDic[linesA[i].strip().replace("\n", "").lower()] = linesB[i].strip().replace("\n", "")

# def checkDesignations(lineA, lineB):
#     count = 1
#     wordsA = lineA.strip().replace("\n", "").replace(".", "").lower().split()
#     lineB = lineB.strip().replace("\n", "")

#     if (len(wordsA) > 3):
#         for i in range(1, 5):
#             for j in range(0, len(wordsA) - (i - 1)):
#                 x = " ".join(wordsA[j: j + i])
#                 y = desigDic.get(x, False)
#                 if (y):
#                     if (y in lineB):
#                         count = count + len(x.split())
#     else:
#         for i in range(1, len(wordsA) + 1):
#             for j in range(0, len(wordsA) - (i - 1)):
#                 x = " ".join(wordsA[j: j + i])
#                 y = desigDic.get(x, False)
#                 if (y):
#                     if (y in lineB):
#                         count = count + len(x.split())
#     return count

# def calcDicWeightForLine(lineA, lineB, wordDictionary):
#     count = checkDesignations(lineA, lineB)
#     # count = 1
#     wordsA = lineA.split()
#     wordsB = lineB.split()
#     for i in range(len(wordsA)):
#         wordsA[i] = wordsA[i].strip().replace(".", "").replace(",", "").lower()
#     for i in range(len(wordsB)):
#         wordsB[i] = wordsB[i].strip().replace(".", "").replace(",", "")
#     for wordA in wordsA:
#         values = wordDictionary.get(wordA, False)
#         if (values != False):
#             for value in values:
#                 if (value in wordsB):
#                     count = count + 1
#                     wordsB.remove(value)
#     return (len(wordsA) - count)/len(wordsA)




wordDictionary = {}
# with open(inputpaths.designationsA) as designationsFileA:
#     with open(inputpaths.designationsB) as designationsFileB:
#         linesA = designationsFileA.readlines()
#         linesB = designationsFileB.readlines()
#         for i in range(len(linesA)):
#             word = linesA[i].strip().replace("\n", "").lower()
#             if (wordDictionary.get(word, False)):
#                 wordDictionary[word].append(linesB[i].strip().replace("\n", ""))
#             else:
#                 wordDictionary[word]  = [linesB[i].strip().replace("\n", "")]

# with open(inputpaths.existingDictionaryA) as dictionaryFileA:
#     with open(inputpaths.existingDictionaryB) as dictionaryFileB:
#         linesA = dictionaryFileA.readlines()
#         linesB = dictionaryFileB.readlines()
#         for i in range(len(linesA)):
#             word = linesA[i].strip().replace("\n", "").lower()
#             if (wordDictionary.get(word, False)):
#                 if (linesB[i].strip().replace("\n", "") not in wordDictionary.get(word)):
#                     wordDictionary[word].append(linesB[i].strip().replace("\n", ""))
#             else:
#                 wordDictionary[word]  = [linesB[i].strip().replace("\n", "")]

def checkDictionary(lineA, lineB):
    count = 1
    wordsA = lineA.strip().replace("\n", "").replace(".", "").lower().split()
    lineB = lineB.strip().replace("\n", "")
    wordsB = lineB.split()

    if (len(wordsA) > 3):
        for i in range(1, 5):
            for j in range(0, len(wordsA) - (i - 1)):
                x = " ".join(wordsA[j: j + i])
                y = wordDictionary.get(x, False)
                if (y):
                    for value in y:
                        contain = True
                        for val in value.split():
                            if (val.strip() not in wordsB):
                                contain = False
                                break
                        if (contain):
                            count = count + len(x.split())
                            try:
                                for val in value.split():
                                    wordsB.remove(val)
                            except:
                                pass
                            # lineB = " ".join(wordsB)
    else:
        for i in range(1, len(wordsA) + 1):
            for j in range(0, len(wordsA) - (i - 1)):
                x = " ".join(wordsA[j: j + i])
                y = wordDictionary.get(x, False)
                if (y):
                    for value in y:
                        contain = True
                        for val in value.split():
                            if (val.strip() not in wordsB):
                                contain = False
                                break
                        if (contain):
                            count = count + len(x.split())
                            try:
                                for val in value.split():
                                    wordsB.remove(val)
                            except:
                                pass
                            # lineB = " ".join(wordsB)
    return count

def calcDicWeightForLine(lineA, lineB, personNamesDictionary):
    #count = checkDictionary(lineA, lineB)
    count = 1
    wordsA = lineA.split()
    wordsB = lineB.split()
    for i in range(len(wordsA)):
        wordsA[i] = wordsA[i].strip().replace(".", "").replace(",", "").lower()
    for i in range(len(wordsB)):
        wordsB[i] = wordsB[i].strip().replace(".", "").replace(",", "")
    for wordA in wordsA:
        values = personNamesDictionary.get(wordA, False)
        if (values != False):
            for value in values:
                if (value in wordsB):
                    count = count + 1
                    wordsB.remove(value)
    return (len(wordsA) - count)/len(wordsA)

# ## future - use character matching for කතුවැකියෙන්, කතුවැකි etc