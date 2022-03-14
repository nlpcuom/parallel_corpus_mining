import os
import numpy as np
import inputpaths
import math

def getSentenceDict(datapath):
    sentenceDic = {}
    files = os.listdir(datapath)
    x=0
    #create sent dictionary with counts for all documnets in the date - sentenceDic
    for tempfile in files:
        # x=x+1
        # print(x)
        tempfile = open(datapath + tempfile)
        sentences = tempfile.readlines()
        for sentence in sentences:
            if sentence in sentenceDic:
                sentenceDic[sentence] = sentenceDic[sentence] + 1
            else:
                sentenceDic[sentence] = 1
        tempfile.close()
    idfDictionary = {}
    for tempfile in files:
        txtfile = open(datapath + tempfile)
        idfDictionary[tempfile] = []
        sentences = txtfile.readlines()
        for sentence in sentences:
            idfDictionary[tempfile].append(sentenceDic[sentence])
        txtfile.close()
    return idfDictionary #returns idfDic containing counts of sentences

def getIDFDictionaryWithNgrams(datapath, n):
    ngramDic = {}
    files = os.listdir(datapath)
    x=0
    for tempfile in files:
        # x=x+1
        # print(x)
        tempfile = open(datapath + tempfile)
        sentences = tempfile.readlines()
        for sentence in sentences:
            words = sentence.split()
            ngrams = []
            ngram = ""
            if len(words) < n:
                ngram = " ".join(words)
                if ngram in ngramDic:
                    ngramDic[ngram] = ngramDic[ngram] + 1
                else:
                    ngramDic[ngram] = 1
            else:
                for i in range(len(words) - n + 1):
                    ngrams.append(words[i:i + n])
                    ngram = " ".join(words[i:i + n])
                    if ngram in ngramDic:
                        ngramDic[ngram] = ngramDic[ngram] + 1
                    else:
                        ngramDic[ngram] = 1
        tempfile.close()
    idfDictionary = {}
    # print(ngramDic)
    for tempfile in files:
        txtfile = open(datapath + tempfile)
        idfDictionary[tempfile] = []
        sentences = txtfile.readlines()
        for sentence in sentences:
            ngramMax = 0
            words = sentence.split()
            if len(words) < n:
                ngram = " ".join(words)
                ngramMax = max(ngramMax, ngramDic[ngram])
            else:
                for i in range(len(words) - n + 1):
                    ngram = " ".join(words[i:i + n])
                    ngramMax = max(ngramMax, ngramDic[ngram])
            idfDictionary[tempfile].append(ngramMax)
        txtfile.close()
    return idfDictionary

def getTFDictionaryWithNgrams(datapath, n):
    ngramDic = {}
    files = os.listdir(datapath)
    x=0
    for tempfilename in files:
        tempfile = open(datapath + tempfilename)
        sentences = tempfile.readlines()
        ngramDic[tempfilename] = {}
        for sentence in sentences:
            words = sentence.split()
            ngrams = []
            ngram = ""
            if len(words) < n:
                ngram = " ".join(words)
                if ngram in ngramDic[tempfilename]:
                    ngramDic[tempfilename][ngram] = ngramDic[tempfilename][ngram] + 1
                else:
                    ngramDic[tempfilename][ngram] = 1
            else:
                for i in range(len(words) - n + 1):
                    ngrams.append(words[i:i + n])
                    ngram = " ".join(words[i:i + n])
                    if ngram in ngramDic[tempfilename]:
                        ngramDic[tempfilename][ngram] = ngramDic[tempfilename][ngram] + 1
                    else:
                        ngramDic[tempfilename][ngram] = 1
        tempfile.close()
    tfDictionary = {}
    # print(ngramDic)
    for tempfilename in files:
        txtfile = open(datapath + tempfilename)
        tfDictionary[tempfilename] = []
        sentences = txtfile.readlines()
        for sentence in sentences:
            ngramMax = 0
            words = sentence.split()
            if len(words) < n:
                ngram = " ".join(words)
                ngramMax = max(ngramMax, ngramDic[tempfilename][ngram])
            else:
                for i in range(len(words) - n + 1):
                    ngram = " ".join(words[i:i + n])
                    ngramMax = max(ngramMax, ngramDic[tempfilename][ngram])
            tfDictionary[tempfilename].append(ngramMax)
        txtfile.close()
    return tfDictionary

def getTFWeightsForFile(filename, path, tfDictionary, weightings):
    tempfile = open(path + filename.replace("raw", "txt"), "r")
    sentences = tempfile.readlines()
    totalDocs = len(os.listdir(path))
    # totalDocs = 3000
    for i in range(len(tfDictionary[filename.replace("raw", "txt")])):
        weightings[i] = weightings[i] * (math.sqrt(tfDictionary[filename.replace("raw", "txt")][i]))
        # weightings[i] = weightings[i] * (
        #         0.4 + 0.6 * (tfDictionary[filename.replace("raw", "txt")][i])/max(tfDictionary[filename.replace("raw", "txt")])
        #     )
    return weightings

def getIDFWeightingsForFile(filename, path, idfDictionary):
    weightings = []
    tempfile = open(path + filename.replace("raw", "txt"), "r")
    sentences = tempfile.readlines()
    totalDocs = len(os.listdir(path))
    # totalDocs = 3000
    for count in idfDictionary[filename.replace("raw", "txt")]:
        weightings.append(1 + np.log((totalDocs + 1)/(1 + count)))
    return weightings #idf weight

def getIDFWeightingForEquationEight(filename, path, idfDictionary):
    weightings = []
    tgetSentenceDictempfile = open(path + filename.replace("raw", "txt"), "r")
    sentences = tempfile.readlines()
    totalDocs = len(os.listdir(path))
    # totalDocs = 3000
    print(idfDictionary)
    for count in idfDictionary[filename.replace("raw", "txt")]:
        # weight = 1 + np.log((totalDocs + 1)/(1 + count))
        # weightings.append(weight)
        # weight = (totalDocs)/(1 + count)
        # weightings.append(weight)
        # weight = np.log(1 + (totalDocs)/(count))
        # weightings.append(weight)
        weight = max(0, np.log((totalDocs - count)/count))
        weightings.append(weight)
        # print(weight)
    return weightings
