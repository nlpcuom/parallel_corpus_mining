wordDictionary = {}

def loadDictionaries():
    enDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-TA/existingdictionary.en", "r")
    taDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-TA/existingdictionary.ta", "r")
    enWords = enDictionary.readlines()
    taWords = taDictionary.readlines()
    for i in range(len(enWords)):
        enword = enWords[i].strip().replace("\n", "")
        if (wordDictionary.get(enword, False)):
            wordDictionary[enword].append(taWords[i].strip().replace("\n", ""))
        else:
            wordDictionary[enword] = [taWords[i].strip().replace("\n", "")]
    print(len(wordDictionary))


def mapWords(enWords, taLine):
    enLine = " ".join(enWords)
    talinewords = taLine.split()
    for i in range(0, len(enWords)):
        tawords = wordDictionary.get(enWords[i], False)
        if (tawords):
            # print(tawords)
            for taword in tawords:
                if (taword in talinewords):
                    taLine = taLine.replace(taword, "")
                    enLine = enLine.replace(enWords[i], "")
                    talinewords.remove(taword)
    taLine = " ".join(taLine.strip().split())
    enLine = " ".join(enLine.strip().split())
    if (len(taLine) > 1):
        # print(taLine)
        if (wordDictionary.get(enLine, False)):
            wordDictionary[enLine].append(taLine)
        else:
            wordDictionary[enLine] = [taLine]

################################
# execution
################################

loadDictionaries()

enGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.en", "r")
taGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.ta", "r")

enGlossWords = enGlossary.readlines()
taGlossWords = taGlossary.readlines()

for i in range(len(enGlossWords)):
    words = enGlossWords[i].strip().replace("\n", "").lower().split()
    mapWords(words, taGlossWords[i].strip().replace("\n", ""))

with open("./Dictionaries/EN-TA/combinedGlossary.en", "w") as enwritefile:
    with open("./Dictionaries/EN-TA/combinedGlossary.ta", "w") as tawritefile:
        for key, values in wordDictionary.items():
            for value in values:
                enwritefile.write(key + "\n")
                tawritefile.write(value + "\n")
            # print(key, values)