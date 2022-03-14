import inputpaths

def getSentenceLengthWeightings(datapath, fileName, lang):
    fnames = fileName.split(".")
    newfname = ".".join(fnames[0: -1])
    docFile = open(datapath + newfname + ".txt")
    sentenceCounts = getSentenceCounts(docFile, lang)
    weightings = []
    total = getTotalTokenCount(sentenceCounts)
    for sentenceCount in sentenceCounts:
        weightings.append(sentenceCount/total)
    return weightings

def getSentenceCounts(docFile, lang):
    lines = docFile.readlines()
    counts = []
    for line in lines:
        count = 0
        for alllines in lines:
            if line == alllines:
                count = count + 1
        counts.append(count * len(line.split()))
    return counts

# def getSentenceCounts(docFile, lang):
#     lines = docFile.readlines()
#     counts = []
#     for line in lines:
#         count = 0
#         for alllines in lines:
#             if line == alllines:
#                 count = count + 1
#         if (lang == 'en'):
#             wordcount = 0
#             words = line.split()
#             for word in words:
#                 if word not in enstopwords:
#                     # print('en')
#                     wordcount = wordcount + 1
#             counts.append(count * wordcount)
#         elif (lang == 'si'):
#             wordcount = 0
#             words = line.split()
#             for word in words:
#                 if word not in sistopwords:
#                     # print('si')
#                     wordcount = wordcount + 1
#             counts.append(count * wordcount)
#         else:
#             counts.append(count * len(line.split()))
#     return counts

def getTotalTokenCount(counts):
    total = 0
    for count in counts:
        total = total + count
    return total