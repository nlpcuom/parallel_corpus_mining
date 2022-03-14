

def competitiveMatching(sortedDistancePairs):
    aligned = []
    alignedDocsA = []
    alignedDocsB = []
    for pair in sortedDistancePairs:
        if pair["a"] not in alignedDocsA and pair["b"] not in alignedDocsB:
            aligned.append(pair)
            alignedDocsA.append(pair["a"])
            alignedDocsB.append(pair["b"])
    return aligned