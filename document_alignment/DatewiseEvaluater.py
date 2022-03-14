import csv

def evaluateDatewise(filePath, results):
    alignedEng = []
    alignedSin = []
    # print(len(results))
    with open(filePath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            alignedEng.append(row[0].strip().replace("json", "raw"))
            alignedSin.append(row[2].strip().replace("json", "raw"))
    totcounter = 0
    alignedcounter = 0
    # print(len(alignedEng))
    # print(len(alignedSin))
    for result in results:
        if result["a"] in alignedEng:
            totcounter = totcounter + 1
            if result["b"] == alignedSin[alignedEng.index(result["a"])]:
                alignedcounter = alignedcounter + 1
        # else:
        #     print(result["a"], result["b"])
    return alignedcounter, totcounter