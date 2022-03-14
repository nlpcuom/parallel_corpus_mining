import os
from GreedyMoversDistance import greedyMoversDistance
from SentenceLengthWeighting import getSentenceLengthWeightings
from MergeSort import mergeSort
from CompetitiveMatching import competitiveMatching
from IDFWeighting import getIDFWeightingsForFile, getSentenceDict, getIDFWeightingForEquationEight, getIDFDictionaryWithNgrams, getTFDictionaryWithNgrams, getTFWeightsForFile
from DatewiseEvaluater import evaluateDatewise
import numpy as np
import inputpaths
import sys
import pickle

# embeddingPathA = inputpaths.embeddingPathA
# embeddingPathB = inputpaths.embeddingPathB
# datPathA = inputpaths.dataPathA
# datPathB = inputpaths.dataPathB
# paralleltxt = inputpaths.paralleltxt

embeddingPathA = ""
embeddingPathB = ""
datPathA = ""
datPathB = ""
paralleltxt = ""
option = ""
metric = ""


# filename = '/home/dilan/Private/Projects/FYP/kishkyImplementation/model2_itm2.sav'
loaded_model = ""

wordDictionary = {}

def main():
    global embeddingPathA
    global embeddingPathB
    global datPathA
    global datPathB
    global paralleltxt

    global loaded_model
    global option
    global dim
    global metric

    embeddingPathA = sys.argv[1]
    embeddingPathB = sys.argv[2]
    datPathA = sys.argv[3]
    datPathB = sys.argv[4]
    paralleltxt = sys.argv[5]
    mlModelPath = sys.argv[6]
    option = sys.argv[7]
    dim = int(sys.argv[8])
    metric = sys.argv[9]

    loaded_model = pickle.load(open(mlModelPath, 'rb'))
    # print(embeddingPathA)
    # print(embeddingPathB)
    # print(datPathA)
    # print(datPathB)
    # print(paralleltxt)
    # print(mlModelPath)
    # print(option)
    # print(dim)
    # print(metric)


    #loadDictionaries()
    runDatewise()
    # runcombined()

def runcombined():
    # matchedpairs = SLIDFAlignment(embeddingPathA, embeddingPathB, datPathA, datPathB)
    matchedpairs = SentenceLengthAlignment(embeddingPathA, embeddingPathB, datPathA, datPathB)
    print(matchedpairs)
    results = evaluateDatewise(paralleltxt, matchedpairs)
    print("Aligned count - " + str(results[0]))
    print("Total count - " + str(results[1]))

def runDatewise():

    alignedcounts = []
    totcounts = []
    alignment_pairs_found=[]
    enYears = os.listdir(embeddingPathA)
    for enYear in enYears:
        enMonths = os.listdir(embeddingPathA + enYear + "/")
        for enMonth in enMonths:
            enDays = os.listdir(embeddingPathA + enYear + "/" + enMonth + "/")
            for enDay in enDays:
                #sentence length
                matchedpairs = SentenceLengthAlignment(
                    embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                    embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                    datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                    datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                    )
                #idf
                # matchedpairs = IDFAlignment(
                #     embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                #     )
                #slidf
                # matchedpairs = SLIDFAlignment(
                #     embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                #     )
                #print(enYear, enMonth, enDay)
                # print(len(matchedpairs))
                # print(matchedpairs)
                #print('Matched count {} {} {} : {}'.format(enYear, enMonth, enDay, len(matchedpairs)))
                alignment_pairs_found.append(len(matchedpairs))
                result = evaluateDatewise(
                                paralleltxt,
                                matchedpairs
                                )
                alignedcounts.append(result[0])
                totcounts.append(result[1])

    # print(alignedcounts)
    # print(totcounts)
    golden_aligned_doc_pairs=len([line for line in open(paralleltxt)])
    total_alignments_found=sum(alignment_pairs_found)
    total_matches_with_eval_set=sum(alignedcounts)

    print('Total Aligned count : {}'.format(total_alignments_found))
    print('Total golden-alignment entries : {}'.format(golden_aligned_doc_pairs))
    print("Matched Aligned count ", total_matches_with_eval_set)
    print("Total count with source doc", sum(totcounts))

    recall=total_matches_with_eval_set/golden_aligned_doc_pairs*100
    precision=total_matches_with_eval_set/total_alignments_found*100
    f1=2*recall*precision/(recall+precision)

    print('Recall {:0.3f} Precision {:0.3f} F1 {:0.3f}'.format(recall, precision, f1))

def SentenceLengthAlignment(embedPathA, embedPathB, dataPathA, dataPathB): # hiru -  325/500 # gosssip - 296/300 # wsws - 497/500 # army - 523/535 # itn - 41/51

    # print(embedPathA)
    # print(embedPathB)
    # print(dataPathA)
    # print(dataPathB)
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []
    # print(len(files1), len(files2))
    # print(files1)
    # print(files2)

    weightsA = []
    weightsB = []
    for file1 in files1:
        try:
            weightsA.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathA, file1, "si")))
        except:
            print("An exception occurred")
    for file2 in files2:
        try:
            weightsB.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathB, file2, "ta")))
        except:
            print("An exception occurred")
    tempDistances = []
    for i in range(len(files1)):
        for j in range(len(files2)):
            try:
                weightA = weightsA[i].copy()
                weightB = weightsB[j].copy()
                tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary, loaded_model, dataPathA, dataPathB, option, dim, metric)})
            except:
                print("error")

    mergeSort(tempDistances)
    #print(tempDistances)
    #print(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
    return matchedPairs

def IDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB):
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []

    # idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    # idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    # tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    # tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    # for file1 in files1:
    #     weightsA.append(normalizeDocumentMass(
    #         getTFWeightsForFile(
    #             file1,
    #             dataPathA,
    #             tfDictA,
    #             getIDFWeightingsForFile(file1, dataPathA, idfDictA)
    #         )
    #     ))
    # for file2 in files2:
    #     weightsB.append(normalizeDocumentMass(
    #         getTFWeightsForFile(
    #             file2,
    #             dataPathB,
    #             tfDictB,
    #             getIDFWeightingsForFile(file2, dataPathB, idfDictB)
    #         )
    #     ))

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    for file1 in files1:
        weightsA.append(normalizeDocumentMass(
            getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)
        ))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(
            getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)
        ))

    tempDistances = []
    for i in range(len(files1)):
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary, loaded_model, dataPathA, dataPathB, option, dim, metric)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
    return matchedPairs

def SLIDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB):
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    # idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    # idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    # tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    # tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    tempweightA1 = []
    tempweightA2 = []
    tempweightB1 = []
    tempweightB2 = []
    
    for file1 in files1:
        try:
            tempweightA1.append(np.array(getSentenceLengthWeightings(dataPathA, file1, "si")))
            # tempweightA2.append(normalizeDocumentMass(
            #     getTFWeightsForFile(
            #         file1,
            #         dataPathA,
            #         tfDictA,
            #         getIDFWeightingsForFile(file1, dataPathA, idfDictA)
            #     )
            # ))
            tempweightA2.append(
                getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)
            )
        except:
            print("Exception")
        # tempweightA2.append(np.array(getIDFWeightingForEquationEight(file1, dataPathA, sentenceDictA)))
    # print("weights A")
    for file2 in files2:
        try:
            tempweightB1.append(np.array(getSentenceLengthWeightings(dataPathB, file2, "ta")))
            # tempweightB2.append(normalizeDocumentMass(
            #     getTFWeightsForFile(
            #         file2,
            #         dataPathB,
            #         tfDictB,
            #         getIDFWeightingsForFile(file2, dataPathB, idfDictB)
            #     )
            # ))
            tempweightB2.append(
                getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)
            )
        except:
            print("Exception")
        # tempweightB2.append(np.array(getIDFWeightingForEquationEight(file2, dataPathB, sentenceDictB)))
    # print("weigths B")

    for i in range(len(tempweightA1)):
        weightsA.append(normalizeDocumentMass(tempweightA1[i] * tempweightA2[i]))
    for i in range(len(tempweightB1)):
        weightsB.append(normalizeDocumentMass(tempweightB1[i] * tempweightB2[i]))

    tempDistances = []
    for i in range(len(files1)):
        # print("i",i)
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            try:
                tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary, loaded_model, dataPathA, dataPathB, option, dim, metric)})
            except:
                print("New")
    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
    # print(matchedPairs)
    # print("SLIDF count for " + dataPathA.split("/")[10] + " - " + dataPathA.split("/")[11] + " : " + str(count))
    return matchedPairs

def normalizeDocumentMass(fileWeights):
    total = sum(fileWeights)
    for i in range(len(fileWeights)):
        fileWeights[i] = fileWeights[i] / total
    return fileWeights

def loadDictionaries():
    # sitasiNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/uniq_names.tok.si-ta.si", "r")
    # sitatafNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/uniq_names.tok.si-ta.ta", "r")

    #wordsA = open(inputpaths.existingDictionaryA).readlines()
    #wordsB = open(inputpaths.existingDictionaryB).readlines()
    
    namesA = open(inputpaths.personNamesA).readlines()
    namesB = open(inputpaths.personNamesB).readlines()

    # for i in range(len(wordsA)):
    #     wordA = wordsA[i].strip().replace("\n", "")
    #     if (wordDictionary.get(wordA, False)):
    #         wordDictionary[wordA].append(wordsB[i].strip().replace("\n", ""))
    #     else:
    #         wordDictionary[wordA]  = [wordsB[i].strip().replace("\n", "")]
    for  i in range(len(namesA)):
        nameA = namesA[i].strip().replace("\n", "")
        if (wordDictionary.get(nameA, False)):
            wordDictionary[nameA].append(namesB[i].strip().replace("\n", ""))
        else:
            wordDictionary[nameA] = [namesB[i].strip().replace("\n", "")]
    #print(wordDictionary)

if __name__ == "__main__":
    main()