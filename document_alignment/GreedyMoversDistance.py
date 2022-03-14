import numpy as np
import os
import inputpaths
import pickle
import time
from DictionaryWeighting import calcDicWeightForLine

# dim = 1024
# filename = '/home/dilan/Private/Projects/FYP/kishkyImplementation/model2_itm2.sav'
# loaded_model = pickle.load(open(mlModelPath, 'rb'))
# Input for the method must be array of tuples

# def greedyMoversDistance(docA, docB, weightsA, weightsB, embedpathA, embedpathB):
#     docVecA = getDocVec(docA, embedpathA)
#     docVecB = getDocVec(docB, embedpathB)
#     maxSortedVecs = getSortedDistances(docVecA, docVecB)
#     minSortedVecs = np.flipud(maxSortedVecs)
#     distance = 0
#     for sortedPair in minSortedVecs:
#         weigVecA = weightsA[sortedPair["i"]]
#         weigVecB = weightsB[sortedPair["j"]]
#         flow = min(weigVecA, weigVecB)
#         weightsA[sortedPair["i"]] = weigVecA - flow
#         weightsB[sortedPair["j"]] = weigVecB - flow
#         vecA = docVecA[sortedPair["i"]]
#         vecB = docVecB[sortedPair["j"]]
#         distance = distance + np.linalg.norm(vecA - vecB) * flow
#     return distance

def greedyMoversDistance(docA, docB, weightsA, weightsB, embedpathA, embedpathB, wordDictionary, loaded_model, datapathA, datapathB, option, dim, metric):
    try:
        docVecA = getDocVec(docA, embedpathA, option, dim)
        docVecB = getDocVec(docB, embedpathB, option, dim)
        docFileA = getDocFile(docA, embedpathA, datapathA)
        docFileB = getDocFile(docB, embedpathB, datapathB)

        maxSortedVecs = getSortedDistances(docVecA, docVecB, loaded_model, metric)
        minSortedVecs = np.flipud(maxSortedVecs)
        # print(minSortedVecs)
        distance = 0
        for sortedPair in minSortedVecs:
            # print(sortedPair)
            weigVecA = weightsA[sortedPair["i"]]
            weigVecB = weightsB[sortedPair["j"]]
            flow = min(weigVecA, weigVecB)
            weightsA[sortedPair["i"]] = weigVecA - flow
            weightsB[sortedPair["j"]] = weigVecB - flow
            vecA = docVecA[sortedPair["i"]]
            vecB = docVecB[sortedPair["j"]]
            # only euclidean
            # distance = distance + (
            #     np.linalg.norm(vecA - vecB) * flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
            #     )

            # print(np.linalg.norm(vecA - vecB))
            # print(flow)

            # only cosine
            # distance = distance + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) * flow
            # cosine + euclidean
            # distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB)) * (
            #     flow * calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
            #     )
            # metric learning distance
            if (metric == "metric"):
                distance = distance + (
                    (
                        loaded_model.score_pairs([(vecA, vecB)])[0]
                        ) * flow * calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                )
            elif (metric == "cosine"):
                distance = distance + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) * flow
            elif (metric == "euclidean"):
                distance = distance + (
                    np.linalg.norm(vecA - vecB) * flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                    )
            else:
                print("Invalid metric")
            # average all
            # distance = distance + (
            #     ((loaded_model.score_pairs([(vecA, vecB)])[0] + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB))/3) * flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
            # )
            # print(distance)
        # dicWeight = calcDictionaryWeight(docA, docB, embedpathA, embedpathB, wordDictionary)
        # return distance * dicWeight
        return distance
    except:
        return 0

def getSortedDistances(docVecA, docVecB, loaded_model, metric):
    eucDistances = np.array([])
    for i in range(len(docVecA)):
        for j in range(len(docVecB)):
            # eucDistances = np.append(eucDistances, [np.linalg.norm(docVecA[i] - docVecB[j])])
            # eucDistances = np.append(eucDistances,
            #     [((1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i])*np.linalg.norm(docVecB[j]))) + np.linalg.norm(docVecA[i] - docVecB[j]))])
            if (metric == "metric"):
                eucDistances = np.append(eucDistances,
                    [loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0]])
            elif (metric == "cosine"):
                eucDistances = np.append(eucDistances,
                    [1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i])*np.linalg.norm(docVecB[j]))])
            elif (metric == "euclidean"):
                eucDistances = np.append(eucDistances, [np.linalg.norm(docVecA[i] - docVecB[j])])
            else:
                print("Invalid metric")
            # average all
            # eucDistances = np.append(eucDistances,
            #     [(loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0] + np.linalg.norm(docVecA[i] - docVecB[j]) + (1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i])*np.linalg.norm(docVecB[j]))))/3])
            # print(eucDistances)
    sortedVecs = []
    for i in range(len(eucDistances)):
        maxi = eucDistances.argmax()
        # print(maxi)
        sortedVecs.append({"dist": eucDistances[maxi], "i": maxi//len(docVecB), "j": maxi % len(docVecB)})
        eucDistances[maxi] = 0
    return sortedVecs

def getDocVec(doc, path, option, dim):
    if (option == "laser"):
        docVec = np.fromfile(path + doc, dtype = np.float32, count = -1)
        docVec.resize(docVec.shape[0] // dim, dim)
        return docVec
    elif (option == "labse"):
        docVec = np.fromfile(path + doc, dtype = np.float32, count = -1)
        docVec.resize(docVec.shape[0] // dim, dim)
        return docVec
    elif (option == "xlmr"):
        docVec = np.fromfile(path + doc, dtype = np.float32, count = -1)
        docVec.resize(docVec.shape[0] // dim, dim)
        return docVec

def getDocFile(doc, path, datapath):
    fnames = doc.split(".")
    newfname = ".".join(fnames[0: -1])
    docFile = open(datapath + newfname + ".txt", "r")
    lines = []
    for line in docFile.readlines():
        lines.append(line.strip().replace("\n", ""))
    return lines
