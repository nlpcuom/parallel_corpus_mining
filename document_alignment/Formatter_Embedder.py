import os
import json
from random import randrange
import csv
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import sys
from stopwords import enstopwords, sistopwords

sys.path.insert(0, "../../sinling/sinling/sinhala/")
LASER = os.environ['LASER']
sys.path.insert(1, LASER + "/source/")

from tokenizer import SinhalaTokenizer
# from embed_from_lasertrain import MultipleEncoder
from embed import MultipleEncoder

outputEmbedList = []
inputEmbedList = []

sinhalasplitter = SinhalaTokenizer()
englishsplitter = SentenceSplitter(language='en')

def convertToEmbedding(readpath, writepath, lang):
    print('bleh')
    os.system("${LASER}/tasks/embed/embed.sh " + readpath + " " + lang + " " + writepath)

def addToEmbeddingList(readpath, writepath):
    inputEmbedList.append(readpath)
    outputEmbedList.append(writepath)

def converBatchToEmbedding(lang):
    # MultipleEncoder(
    #     "/home/dilan/Private/Projects/FYP/Laser/LASER/models/3way/checkpoint_best.pt",
    #     "/home/dilan/Private/Projects/FYP/Laser/LASER/models/3way/dict." + lang + ".txt",
    #     "en-si",
    #     inputEmbedList,
    #     outputEmbedList
    # )
    MultipleEncoder("/home/dilan/Private/Projects/FYP/Laser/LASER/models/bilstm.93langs.2018-12-26.pt",
        lang, 
        "/home/dilan/Private/Projects/FYP/Laser/LASER/models/93langs.fcodes",
        inputEmbedList,
        outputEmbedList
    )

def formatFileForEmbedding(readpath, writepath, lang):
    try:
        content = ""
        with open(readpath) as document:
            doc = json.load(document)
            content = doc["Content"]
            if len(content) == 0:
                return
        sentences = []
        for line in content:
            if (lang == "en"):
                sentences = sentences + englishsplitter.split(text = line)
            elif (lang == "si"):
                sentences = sentences + sinhalasplitter.split_sentences(line)
        # sentences = sentences + content.split(".")
        # print(sentences)
        writefile = open(writepath, "w")
        for sentence in sentences:
            if sentence != "" and sentence != " " and sentence != "\n":
                writesent = sentence.strip().replace("\n", "")
                if writesent != "" and writesent != " ":
                    writefile.write(writesent)
                    writefile.write("\n")
        writefile.close()
    except Exception:
        print(readpath)

def formatArmyFileForEmbedding(readpath, writepath, lang):
    # try:
    content = ""
    with open(readpath) as document:
        doc = json.load(document)
        content = doc["Content"]
        if len(content) == 0:
            return
    sentences = []
    if (lang == "en"):
        sentences = sentences + englishsplitter.split(text = content)
    elif (lang == "si"):
        sentences = sentences + sinhalasplitter.split_sentences(content)
    elif (lang == "ta"):
        sentences = sentences + content.split(".")
    # print(sentences)
    writefile = open(writepath, "w")
    for sentence in sentences:
        if sentence != "" and sentence != " " and sentence != "\n":
            writesent = sentence.strip().replace("\n", "")
            if writesent != "" and writesent != " ":
                # writefile.write(writesent)
                writefile.write(removeStopWords(writesent, lang))
                writefile.write("\n")
    writefile.close()
    # except Exception:
    #     print(readpath)

def removeStopWords(sentence, lang):
    words = sentence.split()
    newwords = []
    for word in words:
        if lang == 'en':
            if word not in enstopwords:
                newwords.append(word)
        elif lang == 'si':
            if word not in sistopwords:
                newwords.append(word)
        else:
            newwords.append(word)
    return " ".join(newwords)

def formatFiles(path, writepath):
    files = os.listdir(path)
    for file in files:
        formatFileForEmbedding((path + file), (writepath + str(randrange(100000000)) + ".txt"))

def createEmbeddings(path, writepath, lang):
    files = os.listdir(path)
    print(files)
    a = 0
    for file in files:
        convertToEmbedding((path + file), (writepath + file.replace("txt", "raw")), lang)
        # a = a + 1
        # if a == 300:
            # break

def getFromHiruFolder():
    sinhalafiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/sinhala/January/27/")
    englishfiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/english/January/27/")
    for sinhalafile in sinhalafiles:
        if sinhalafile in englishfiles:
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/sinhala/January/27/"+sinhalafile, "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/si/" + sinhalafile.replace(".json", ".txt"), "si")
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/english/January/27/"+sinhalafile, "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/en/" + sinhalafile.replace(".json", ".txt"), "en")

def getFromWswsFolder():
    sinhalafiles = os.listdir("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/sinhala/")
    englishfiles = os.listdir("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/english/")
    for englishfile in englishfiles:
        formatFileForEmbedding("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/sinhala/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/si/" + englishfile.replace("json", "txt"), "si")
        formatFileForEmbedding("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/english/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/en/" + englishfile.replace("json", "txt"), "en")

def getFromWikipediaFolder():
    sinhalafiles = os.listdir("/home/dilan/Downloads/New/wikipediasinhala/sinhala/")
    englishfiles = os.listdir("/home/dilan/Downloads/New/wikipediaengilsh/english/")
    for englishfile in englishfiles:
        formatFileForEmbedding("/home/dilan/Downloads/New/wikipediasinhala/sinhala/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/si/" + englishfile.replace("json", "txt"), "si")
        formatFileForEmbedding("/home/dilan/Downloads/New/wikipediaengilsh/english/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/en/" + englishfile.replace("json", "txt"), "si")

def getFromArmyFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/"
    sinhalafiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/"
    englishfiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/"
    sifiles = os.listdir(sinhalafiles)
    enfiles = os.listdir(englishfiles)
    enfilenames = []
    sifilenames = []
    with open(csvpath + "golden_alignment.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            sifilenames.append(row[0].strip())
            enfilenames.append(row[2].strip()) 
    for sinfile in sifiles:
        if sinfile in sifilenames:
            print("yes")
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/" + str(sifilenames.index(sinfile)) + ".txt", "si")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/" + sinfile.replace(".json", ".txt"), "si")
    for enfile in enfiles:
        if enfile in enfilenames:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/" + str(enfilenames.index(enfile)) + ".txt", "en")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/" + enfile.replace(".json", ".txt"), "en")


def getFromITNFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/"
    sinhalafiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/Sinhala/"
    englishfiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/English/"
    sifiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/Sinhala/")
    enfiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/English/")
    enfilenames = []
    sifilenames = []
    with open(csvpath + "golden_alignment.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            # if " "+row[0].strip() in files:
            #     print("present")
            #     print(row[0].strip())
            sifilenames.append(row[0].strip())
            enfilenames.append(row[2].strip())
    for sifile in sifiles:
        a = False
        for i in range(len(sifilenames)):
            if sifile.strip() == sifilenames[i]:
                formatArmyFileForEmbedding(sinhalafiles + sifile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/" + str(i) + ".txt", "si")
                a = True
        if a == False:
            formatArmyFileForEmbedding(sinhalafiles +sifile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/" + str(randrange(10000000)) + ".txt", "si")
    for enfile in enfiles:
        a = False
        for i in range(len(enfilenames)):
            if enfile.strip() == enfilenames[i]:
                formatArmyFileForEmbedding(englishfiles + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/" + str(i) + ".txt", "en")
                a = True
        if a == False:
            formatArmyFileForEmbedding(englishfiles + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/" + str(randrange(10000000)) + ".txt", "en")

def readCsvGossipLanka():
    csvpath = "/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/"
    with open(csvpath + "aligned_GL.csv") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = ",")
        for row in csvReader:
            print(row[0], row[1])
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/English/" + row[1].strip(), "/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/en/" + row[0].replace(".json", ".txt").strip(), "en")
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/Sinhala/" + row[0].strip(), "/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/si/" + row[0].replace(".json", ".txt").strip(), "si")

def getFromNewsfirstFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/golden_alignment_newsfirst_updated.txt"
    alignedEng = []
    alignedSin = []
    with open(csvpath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            alignedEng.append(row[0].strip())
            alignedSin.append(row[2].strip())
    sinfilepath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/"
    enfilepath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/"

    sinfiles = os.listdir(sinfilepath)
    enfiles = os.listdir(enfilepath)
    for sinfile in sinfiles:
        if sinfile in alignedSin:
            print("yes")
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/" + str(alignedSin.index(sinfile)) + ".txt", "si")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/" + sinfile.replace(".json", ".txt"), "si")
    for enfile in enfiles:
        if enfile in alignedEng:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/" + str(alignedEng.index(enfile)) + ".txt", "en")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/" + enfile.replace(".json", ".txt"), "en")

def formatDateWiseWithoutParallelChecking(news):
    sipath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/" + news + "/sinhala/"
    enpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/" + news + "/english/"
    tapath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/" + news + "/tamil/"
    simonths = os.listdir(sipath)
    enmonths = os.listdir(enpath)
    tamonths = os.listdir(tapath)
    # for simonth in simonths:
    #     try:
    #         os.mkdir("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/si/" + simonth)
    #         os.mkdir("/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/si/" + simonth)
    #     except:
    #         print(" ")
    #     sidays = os.listdir(sipath + simonth + "/")
    #     for siday in sidays:
    #         try:
    #             os.mkdir("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/si/" + simonth + "/" + siday)
    #             os.mkdir("/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/si/" + simonth + "/" + siday)
    #         except:
    #             print(" ")
    #         sifiles = os.listdir(sipath + simonth + "/" + siday + "/")
    #         for sifile in sifiles:
    #             formatArmyFileForEmbedding(sipath + simonth + "/" + siday + "/" + sifile, 
    #             "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/si/" 
    #             + simonth + "/" + siday + "/" + sifile.replace("json", "txt"), "si")
    #             # convertToEmbedding("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/si/"
    #             # + simonth + "/" + siday + "/" + sifile.replace("json", "txt"),
    #             # "/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/si/" + simonth + "/" + siday + "/" + sifile.replace("json", "raw"),
    #             # "si")
    #             addToEmbeddingList("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/si/"
    #             + simonth + "/" + siday + "/" + sifile.replace("json", "txt"),
    #             "/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/si/" + simonth + "/" + siday + "/" + sifile.replace("json", "raw"))
    # converBatchToEmbedding("si")
    # for enmonth in enmonths:
    #     try:
    #         os.mkdir("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/en/" + enmonth)
    #         os.mkdir("/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/en/" + enmonth)
    #     except:
    #         print(" ")
    #     endays = os.listdir(enpath + enmonth + "/")
    #     for enday in endays:
    #         try:
    #             os.mkdir("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/en/" + enmonth + "/" + enday)
    #             os.mkdir("/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/en/" + enmonth + "/" + enday)
    #         except:
    #             print(" ")
    #         enfiles = os.listdir(enpath + enmonth + "/" + enday + "/")
    #         for enfile in enfiles:
    #             formatArmyFileForEmbedding(enpath + enmonth + "/" + enday + "/" + enfile, 
    #             "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/en/" 
    #             + enmonth + "/" + enday + "/" + enfile.replace("json", "txt"), "en")
    #             # convertToEmbedding("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/en/"
    #             # + enmonth + "/" + enday + "/" + enfile.replace("json", "txt"),
    #             # "/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/en/" + enmonth + "/" + enday + "/" + enfile.replace("json", "raw"),
    #             # "en")
    #             addToEmbeddingList("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/en/"
    #             + enmonth + "/" + enday + "/" + enfile.replace("json", "txt"),
    #             "/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/en/" + enmonth + "/" + enday + "/" + enfile.replace("json", "raw"))
    # converBatchToEmbedding("en")
    for tamonth in tamonths:
        try:
            os.mkdir("/home/dilan/Private/Projects/FYP1/Data-Formatted/datewise/" + news + "/ta/" + tamonth)
            os.mkdir("/home/dilan/Private/Projects/FYP1/Embeddings/datewise/" + news + "/ta/" + tamonth)
        except:
            print(" ")
        tadays = os.listdir(tapath + tamonth + "/")
        for taday in tadays:
            try:
                os.mkdir("/home/dilan/Private/Projects/FYP1/Data-Formatted/datewise/" + news + "/ta/" + tamonth + "/" + taday)
                os.mkdir("/home/dilan/Private/Projects/FYP1/Embeddings/datewise/" + news + "/ta/" + tamonth + "/" + taday)
            except:
                print(" ")
            tafiles = os.listdir(tapath + tamonth + "/" + taday + "/")
            for tafile in tafiles:
                formatArmyFileForEmbedding(tapath + tamonth + "/" + taday + "/" + tafile, 
                "/home/dilan/Private/Projects/FYP1/Data-Formatted/datewise/" + news + "/ta/" 
                + tamonth + "/" + taday + "/" + tafile.replace("json", "txt"), "ta")
                # convertToEmbedding("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/" + news + "/ta/"
                # + tamonth + "/" + taday + "/" + tafile.replace("json", "txt"),
                # "/home/dilan/Private/Projects/FYP/Embeddings/datewise/" + news + "/ta/" + tamonth + "/" + taday + "/" + tafile.replace("json", "raw"),
                # "ta")
                addToEmbeddingList("/home/dilan/Private/Projects/FYP1/Data-Formatted/datewise/" + news + "/ta/"
                + tamonth + "/" + taday + "/" + tafile.replace("json", "txt"),
                "/home/dilan/Private/Projects/FYP1/Embeddings/datewise/" + news + "/ta/"
                + tamonth + "/" + taday + "/" + tafile.replace("json", "raw"))
    converBatchToEmbedding("ta")

###### Hiru
# getFromHiruFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/en/", "/home/dilan/Private/Projects/FYP/Embeddings/datewise/hiru/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/si/", "/home/dilan/Private/Projects/FYP/Embeddings/datewise/hiru/si/", "si")

# readCsvGossipLanka()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/en/", "/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/si/", "/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/si/", "si")

# Wsws
# getFromWswsFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/en/", "/home/dilan/Private/Projects/FYP/Embeddings/wsws/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/si/", "/home/dilan/Private/Projects/FYP/Embeddings/wsws/si/", "si")

# Wikipedia
# getFromWikipediaFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/en/", "/home/dilan/Private/Projects/FYP/Embeddings/wikipedia/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/si/", "/home/dilan/Private/Projects/FYP/Embeddings/wikipedia/si/", "si")

# Army
# getFromArmyFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/", "/home/dilan/Private/Projects/FYP/Embeddings/army/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/", "/home/dilan/Private/Projects/FYP/Embeddings/army/si/", "si")

# ITN
# getFromITNFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/", "/home/dilan/Private/Projects/FYP/Embeddings/itn/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/", "/home/dilan/Private/Projects/FYP/Embeddings/itn/si/", "si")

# Newsfirst
# getFromNewsfirstFolder()
# formatNewsfirstDateWiseWithoutParallelChecking()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/", "/home/dilan/Private/Projects/FYP/Embeddings/newsfirst/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/", "/home/dilan/Private/Projects/FYP/Embeddings/newsfirst/si/", "si")


# formatDateWiseWithoutParallelChecking("hiru")
# formatDateWiseWithoutParallelChecking("army")
# formatDateWiseWithoutParallelChecking("itn")
formatDateWiseWithoutParallelChecking("newsfirst")