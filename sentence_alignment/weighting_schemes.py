def checkDictionary(lineB, lineA, wordDictionary):
    count_A = 0
    count_B = 0
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
                            count_A = count_A + len(x.split())
                            count_B = count_B + len(value.split())
                            try:
                                for val in value.split():
                                    wordsB.remove(val)
                            except:
                                pass
                            lineB = " ".join(wordsB)
    else:
        for i in range(1, len(wordsA) + 1):
            for j in range(0, len(wordsA) - (i - 1)):
                x = " ".join(wordsA[j: j + i])
                y = wordDictionary.get(x, False)
                if (y):
                    for value in y:
                        for value in y:
                            contain = True
                            for val in value.split():
                                if (val.strip() not in wordsB):
                                    contain = False
                                    break
                            if (contain):
                                count_A = count_A + len(x.split())
                                count_B = count_B + len(value.split())
                                try:
                                    for val in value.split():
                                        wordsB.remove(val)
                                except:
                                    pass
                                lineB = " ".join(wordsB)
    return count_A, count_B


def sentence_length_weight(siLine, enLine, word_count_A, word_count_B):
    count_a = len(siLine)
    count_b = len(enLine)
    length_ratio = word_count_B / word_count_A
    diff = abs(count_b - (length_ratio * count_a))
    weight = 1 / diff
    return weight


# def get_dictionary_weight(siLine, enLine, wordDictionary):
#     count = 0
#     enWords = enLine.split()
#     siWords = siLine.split()
#     for i in range(len(enWords)):
#         enWords[i] = enWords[i].strip().replace(".", "").replace(",", "").lower()
#     for i in range(len(siWords)):
#         siWords[i] = siWords[i].strip().replace(".", "").replace(",", "")
#     for enWord in enWords:
#         value = wordDictionary.get(enWord, False)
#         if (value != False):
#             if (value in siWords):
#                 count = count + 1
#                 siWords.remove(value)
#     return count
#
#
# def get_designations_weight(siLine, enLine, DesigDic):
#     count = 0
#     enWords = enLine.strip().replace("\n", "").replace(".", "").lower().split()
#     siLine = siLine.strip().replace("\n", "")
#
#     if (len(enWords) > 3):
#         for i in range(1, 5):
#             for j in range(0, len(enWords) - (i - 1)):
#                 x = " ".join(enWords[j: j + i])
#                 y = DesigDic.get(x, False)
#                 if (y):
#                     if (y in siLine):
#                         count = count + len(x.split())
#     else:
#         for i in range(1, len(enWords) + 1):
#             for j in range(0, len(enWords) - (i - 1)):
#                 x = " ".join(enWords[j: j + i])
#                 y = DesigDic.get(x, False)
#                 if (y):
#                     if (y in siLine):
#                         count = count + len(x.split())
#     return count
