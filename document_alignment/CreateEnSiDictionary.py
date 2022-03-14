
# wordDictionary = {}

# def loadDictionaries():
#     enDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.en", "r")
#     siDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.si", "r")
#     # enDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.en", "r")
#     # siDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.si", "r")
#     enWords = enDictionary.readlines()
#     siWords = siDictionary.readlines()
#     for i in range(len(enWords)):
#         wordDictionary[enWords[i].strip().replace("\n", "")] = siWords[i].strip().replace("\n", "")

# def mapWords(enWords, siLine):
#     enLine = " ".join(enWords)
#     for i in range(0, len(enWords)):
#         siword = wordDictionary.get(enWords[i], False)
#         if (siword):
#             if (siword in siLine):
#                 print(siword)
#                 print(enWords[i])
#                 print()
#                 siLine = siLine.replace(siword, "")
#                 enLine = enLine.replace(enWords[i], "")
#     siLine = " ".join(siLine.strip().split())
#     enLine = " ".join(enLine.strip().split())
#     # print(siLine)
#     # print(enLine)
#     # print()
#     wordDictionary[enLine] = siLine

# ################################
# # execution
# ################################

# loadDictionaries()

# enGlossary = open("./glossary/glossary-06.11.2019.en", "r")
# siGlossary = open("./glossary/glossary-06.11.2019.si", "r")

# enGlossWords = enGlossary.readlines()
# siGlossWords = siGlossary.readlines()

# for i in range(len(enGlossWords)):
#     words = enGlossWords[i].strip().replace("\n", "").lower().split()
#     mapWords(words, siGlossWords[i].strip().replace("\n", ""))

# with open("./glossary/combinedGlossary.en", "w") as enwritefile:
#     with open("./glossary/combinedGlossary.si", "w") as siwritefile:
#         for key, value in wordDictionary.items():
#             enwritefile.write(key + "\n")
#             siwritefile.write(value + "\n")



wordDictionary = {}

def loadDictionaries():
    enDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-SI/existingdictionary.en", "r")
    siDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-SI/existingdictionary.si", "r")
    enWords = enDictionary.readlines()
    siWords = siDictionary.readlines()
    for i in range(len(enWords)):
        enword = enWords[i].strip().replace("\n", "")
        if (wordDictionary.get(enword, False)):
            wordDictionary[enword].append(siWords[i].strip().replace("\n", ""))
        else:
            wordDictionary[enword] = [siWords[i].strip().replace("\n", "")]
    print(len(wordDictionary))


def mapWords(enWords, siLine):
    enLine = " ".join(enWords)
    silinewords = siLine.split()
    for i in range(0, len(enWords)):
        siwords = wordDictionary.get(enWords[i], False)
        if (siwords):
            # print(tawords)
            for siword in siwords:
                if (siword in silinewords):
                    siLine = siLine.replace(siword, "")
                    enLine = enLine.replace(enWords[i], "")
                    silinewords.remove(siword)
    siLine = " ".join(siLine.strip().split())
    enLine = " ".join(enLine.strip().split())
    if (len(siLine) > 1 and len(enLine) > 1):
        print(siLine, enLine)
        if (wordDictionary.get(enLine, False)):
            if (siLine not in wordDictionary.get(enLine)):
                wordDictionary[enLine].append(siLine)
        else:
            wordDictionary[enLine] = [siLine]
    # if (len(enLine) > 1 and len(siLine) > 1 and len(siLine) < 3):
    #     print(enLine, siLine)
 
################################
# execution
################################

loadDictionaries()

enGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.en", "r")
siGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.si", "r")

enGlossWords = enGlossary.readlines()
siGlossWords = siGlossary.readlines()

for i in range(len(enGlossWords)):
    words = enGlossWords[i].strip().replace("\n", "").lower().split()
    mapWords(words, siGlossWords[i].strip().replace("\n", ""))

with open("./Dictionaries/EN-SI/test.en", "w") as enwritefile:
    with open("./Dictionaries/EN-SI/test.si", "w") as siwritefile:
        for key, values in wordDictionary.items():
            for value in values:
                enwritefile.write(key + "\n")
                siwritefile.write(value + "\n")
            print(key, values)