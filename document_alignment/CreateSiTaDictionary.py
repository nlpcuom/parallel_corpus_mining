
# wordDictionary = {}

# def loadDictionaries():
#     siDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.si", "r")
#     taDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.ta", "r")
#     # enDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.en", "r")
#     # siDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.si", "r")
#     siWords = siDictionary.readlines()
#     taWords = taDictionary.readlines()
#     for i in range(len(siWords)):
#         wordDictionary[siWords[i].strip().replace("\n", "")] = taWords[i].strip().replace("\n", "")

# def mapWords(siWords, taLine):
#     siLine = " ".join(siWords)
#     for i in range(0, len(siWords)):
#         taword = wordDictionary.get(siWords[i], False)
#         if (taword):
#             if (taword in taLine):
#                 taLine = taLine.replace(taword, "")
#                 siLine = siLine.replace(siWords[i], "")
#     taLine = " ".join(taLine.strip().split())
#     siLine = " ".join(siLine.strip().split())
#     # print(siLine)
#     # print(enLine)
#     # print()
#     wordDictionary[siLine] = taLine

# ################################
# # execution
# ################################

# loadDictionaries()

# siGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.si", "r")
# taGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.ta", "r")

# siGlossWords = siGlossary.readlines()
# taGlossWords = taGlossary.readlines()

# for i in range(len(siGlossWords)):
#     words = siGlossWords[i].strip().replace("\n", "").lower().split()
#     mapWords(words, taGlossWords[i].strip().replace("\n", ""))

# with open("./glossary/si-ta/combinedGlossary.si", "w") as siwritefile:
#     with open("./glossary/si-ta/combinedGlossary.ta", "w") as tawritefile:
#         for key, value in wordDictionary.items():
#             siwritefile.write(key + "\n")
#             tawritefile.write(value + "\n")


wordDictionary = {}

def loadDictionaries():
    siDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.si", "r")
    taDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.ta", "r")
    siWords = siDictionary.readlines()
    taWords = taDictionary.readlines()
    for i in range(len(siWords)):
        siWord = siWords[i].strip().replace("\n", "")
        if (wordDictionary.get(siWord, False)):
            wordDictionary[siWord].append(taWords[i].strip().replace("\n", ""))
        else:
            wordDictionary[siWord] = [taWords[i].strip().replace("\n", "")]
    print(len(wordDictionary))


def mapWords(siWords, taLine):
    siLine = " ".join(siWords)
    talinewords = taLine.split()
    for i in range(0, len(siWords)):
        tawords = wordDictionary.get(siWords[i], False)
        if (tawords):
            # print(tawords)
            for taword in tawords:
                if (taword in talinewords):
                    taLine = taLine.replace(taword, "")
                    siLine = siLine.replace(siWords[i], "")
                    talinewords.remove(taword)
    taLine = " ".join(taLine.strip().split())
    siLine = " ".join(siLine.strip().split())
    if (len(taLine) > 1):
        # print(taLine)
        if (wordDictionary.get(siLine, False)):
            wordDictionary[siLine].append(taLine)
        else:
            wordDictionary[siLine] = [taLine]

################################
# execution
################################

loadDictionaries()

siGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.si", "r")
taGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.ta", "r")

silossWords = siGlossary.readlines()
taGlossWords = taGlossary.readlines()

for i in range(len(silossWords)):
    words = silossWords[i].strip().replace("\n", "").lower().split()
    mapWords(words, taGlossWords[i].strip().replace("\n", ""))

with open("./Dictionaries/SI-TA/combinedDictionaryNew.si", "w") as siwritefile:
    with open("./Dictionaries/SI-TA/combinedDictionaryNew.ta", "w") as tawritefile:
        for key, values in wordDictionary.items():
            for value in values:
                siwritefile.write(key + "\n")
                tawritefile.write(value + "\n")
            # print(key, values)