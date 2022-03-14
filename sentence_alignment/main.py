import os
import pickle
import argparse
import numpy as np
from weighting_schemes import checkDictionary, sentence_length_weight
from utils_new import cosine_metrix, euclidean_metrix, metriclearning_metrix, combined_metrix, get_MBS_metrix

wordDictionary = {}

def main():

    parser = argparse.ArgumentParser(
        'Align sentences',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-l', '--language_pair', type=str, required=True,
                        choices = ['si-en', 'ta-en', 'si-ta'],
                        help='source and target languages separated by a hyphen')

    parser.add_argument('-w', '--website', type=str, required=True,
                        choices = ['army' ,'hiru', 'itn', 'newsfirst'],
                        help='name of the website')

    parser.add_argument('-s', '--similarity_measure', type=str, required=True,
                        choices = ['cosine' ,'euclidean', 'sdml', 'itml', 'combined_sdml', 'combined_itml'],
                        help='Sentence similarity measurement.')

    parser.add_argument('-r', '--ratio', type=bool, default=False,
                        help='Use ratio score or not.')

    parser.add_argument('-d', '--dictionary', type=bool, default=False,
                        help='Use dictionary weighting or not.')

    parser.add_argument('-e', '--embedding', type=str, required=True,
                        choices = ['laser', 'xlmr', 'labse'],
                        help='Embedding type')


    args = parser.parse_args()
    language_pair = args.language_pair
    website = args.website
    similarity_measure = args.similarity_measure
    ratio = args.ratio
    dictionary = args.dictionary
    embedding=args.embedding

    print('ratio: {} & dictionary : {}'.format(ratio, dictionary))
    get_alignment(language_pair, website, similarity_measure, ratio, dictionary, embedding)
    get_intersection(language_pair, website, similarity_measure, dictionary, embedding)
    recall_precision(language_pair, website, similarity_measure, dictionary, embedding)

def get_alignment(language_pair, website, similarity_measure, ratio, dictionary, embedding):    

    wordDictionary = loadDictionary(language_pair)
    #sdml = load_sdml_model(language_pair)
    #itml = load_itml_model(language_pair)

    # path_forward_alignment = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".forward"
    # path_backward_alignment = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".backward"
    path_forward_alignment = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".forward"
    path_backward_alignment = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".backward"
    forward_alignment = open(path_forward_alignment, "a")
    backward_alignment = open(path_backward_alignment, "a")

    #Evaluation set
    root_dir = "/userdirs/aloka/p2_parallel_corpus_mining/comparable-corpus/Comparable_Sentences_with_Golden_Alignment_v2/"+language_pair+"/"+website
    if language_pair == 'si-en':
        embeddings_A = root_dir + "/embeddings_laser/sinhala/"
        embeddings_B = root_dir + "/embeddings_laser/english/"
        docs_A = root_dir + "/sentences/sinhala/"
        docs_B = root_dir + "/sentences/english/"

    if language_pair == 'ta-en':
        embeddings_A = root_dir + "/embeddings_laser/tamil/"
        embeddings_B = root_dir + "/embeddings_laser/english/"
        docs_A = root_dir + "/sentences/tamil/"
        docs_B = root_dir + "/sentences/english/"

    if language_pair == 'si-ta':
        embeddings_A = root_dir + "/embeddings_laser/sinhala/"
        embeddings_B = root_dir + "/embeddings_laser/tamil/"
        docs_A = root_dir + "/sentences/sinhala/"
        docs_B = root_dir + "/sentences/tamil/"

    for file in os.listdir(embeddings_A):
        path_embA = embeddings_A + file
        path_embB = embeddings_B + file
        path_docA = docs_A + file[:-4]
        path_docB = docs_B + file[:-4]
        embA = read_emb_file(path_embA)
        embB = read_emb_file(path_embB)
        sentences_A = read_sentence_file(path_docA)
        sentences_B = read_sentence_file(path_docB)

        if similarity_measure == 'cosine':
            metrix_AB = cosine_metrix(embA, embB)
        elif similarity_measure == 'euclidean':
            metrix_AB = euclidean_metrix(embA, embB)
        elif similarity_measure == 'sdml':
            metrix_AB = np.array(metriclearning_metrix(embA, embB, sdml))
        elif similarity_measure == 'itml':
            metrix_AB = np.array(metriclearning_metrix(embA, embB, itml))
        elif similarity_measure == 'combined_sdml':
            cosine = cosine_metrix(embA, embB)
            euclidean = euclidean_metrix(embA, embB)
            metriclearning = metriclearning_metrix(embA, embB, sdml)
            metrix_AB = combined_metrix(cosine, euclidean, metriclearning)
        elif similarity_measure == 'combined_itml':
            cosine = cosine_metrix(embA, embB)
            euclidean = euclidean_metrix(embA, embB)
            metriclearning = metriclearning_metrix(embA, embB, itml)
            metrix_AB = combined_metrix(cosine, euclidean, metriclearning)

        if dictionary:
            #ratio true with dictionary
            if ratio:
                #print('dictionary: {} & ratio : {}'.format(dictionary, ratio))
                metrix_A = []
                for index_a in range(len(metrix_AB)):
                    weighted_similarities = []
                    for index_b in range (len(metrix_AB.T)):
                        siLine = sentences_A[index_a][1]
                        enLine = sentences_B[index_b][1]
                        overlap_count = checkDictionary(siLine, enLine, wordDictionary)[1]
                        weight_dict = len(siLine.split()) / (len(siLine.split()) + 1 - overlap_count)
                        weighted_similarities.append(metrix_AB[index_a, index_b] * weight_dict)
                    metrix_A.append(weighted_similarities)
                metrix_A = np.array(metrix_A)

                metrix_B = []
                for index_b in range(len(metrix_AB.T)):
                    weighted_similarities = []
                    for index_a in range(len(metrix_AB)):
                        siLine = sentences_A[index_a][1]
                        enLine = sentences_B[index_b][1]
                        overlap_count = checkDictionary(siLine, enLine, wordDictionary)[0]                        
                        try:
                            weight_dict = len(enLine.split()) / (len(enLine.split()) + 1 - overlap_count)
                            
                        except:
                            weight_dict = len(enLine.split())
                            
                        weighted_similarities.append(metrix_AB[index_a, index_b] * weight_dict)
                    metrix_B.append(weighted_similarities)
                metrix_B = np.array(metrix_B)

                metrix_AB = np.add(metrix_A, metrix_B.T)/2
                metrix_AB = get_MBS_metrix(metrix_AB, embA, embB)

                for i in range(len(metrix_AB)):
                    index_a = i
                    index_b = np.argmax(metrix_AB[i])
                    distance=metrix_AB[i][index_b]
                    # print('Indexes a:{} b:{}'.format(index_a, index_b))
                    # print('Cosine similarity between each target sentence:')
                    # print(metrix_AB[i])
                    # print('max cosine similarity :{}'.format(distance))

                    #print('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))
                    forward_alignment.write('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))

                for i in range(len(metrix_AB.T)):
                    index_b = i
                    index_a = np.argmax(metrix_AB.T[i])
                    distance=metrix_AB.T[i][index_a]

                    #print('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))
                    backward_alignment.write('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))

                    #old code
                    #backward_alignment.write(sentences_A[index_a][0] + "\t" + sentences_B[index_b][0] + "\n") #+ "\t" + distance + "\n")

            #ratio - False not used
            else:
                #print('dictionary: {} & ratio : {}'.format(dictionary, ratio))
                for index_a in range(len(embA)):
                    similarities = metrix_AB[index_a]
                    max_indexes = np.argsort(similarities)[-4:]
                    weighted_similarities = []
                    for i in max_indexes:
                        siLine = sentences_A[index_a][1]
                        enLine = sentences_B[i][1]
                        overlap_count = checkDictionary(siLine, enLine, wordDictionary)[1]
                        weight_dict = len(siLine.split()) / (len(siLine.split()) + 1 - overlap_count)
                        weighted_similarities.append(similarities[i] * weight_dict)
                    max_score = np.amax(weighted_similarities)
                    index_max = np.argmax(weighted_similarities)
                    index_b = max_indexes[index_max]
                    forward_alignment.write(sentences_A[index_a][0] + "\t" + sentences_B[index_b][0] + "\n")

                for index_b in range(len(embB)):
                    similarities = metrix_AB.T[index_b]
                    max_indexes = np.argsort(similarities)[-4:]
                    weighted_similarities = []
                    for i in max_indexes:
                        siLine = sentences_A[i][1]
                        enLine = sentences_B[index_b][1]
                        overlap_count = checkDictionary(siLine, enLine, wordDictionary)[0]
                        try:
                            weight_dict = len(enLine.split()) / (len(enLine.split()) + 1 - overlap_count)
                        except:
                            weight_dict = len(enLine.split())
                        weighted_similarities.append(similarities[i] * weight_dict)
                    max_score = np.amax(weighted_similarities)
                    index_max = np.argmax(weighted_similarities)
                    index_a = max_indexes[index_max]
                    backward_alignment.write(sentences_A[index_a][0] + "\t" + sentences_B[index_b][0] + "\n")

        else:#dic False
            if ratio:
                #print('dictionary: {} & ratio : {}'.format(dictionary, ratio))

                metrix_AB = get_MBS_metrix(metrix_AB, embA, embB)

            for i in range (len(metrix_AB)):
                index_a = i
                index_b = np.argmax(metrix_AB[i])
                distance=metrix_AB[i][index_b]
                forward_alignment.write('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))
            for i in range (len(metrix_AB.T)):
                index_b = i
                index_a = np.argmax(metrix_AB.T[i])
                distance=metrix_AB.T[i][index_a]
                backward_alignment.write('{}\t{}\t{}\n'.format(sentences_A[index_a][0], sentences_B[index_b][0], distance))

    forward_alignment.close()
    backward_alignment.close()


def read_sentence_file(path):
    sentences = open(path, "r").read()
    sentences = sentences.split("\n")
    sentences = sentences[:-1]
    sentences = [i.split("\t") for i in sentences]
    return sentences


def read_file(path):
    sentences = open(path, "r").read()
    #sentences = sentences.split("\n")
    sentences=['\t'.join(sent.split('\t')[0:2]) for sent in sentences.split('\n')]
    sentences = sentences[:-1]
    return sentences


#read file for intersection with distances
def read_file_for_intersection(path):
    sentences = open(path, "r").read()
    #sentences = sentences.split("\n")
    sentences=[sent for sent in sentences.split('\n')]
    sentences = sentences[:-1]
    return sentences


def read_emb_file(path):
    dim = 1024
    X = np.fromfile(path, dtype=np.float32, count=-1)
    X.resize(X.shape[0] // dim, dim)
    return X


def get_intersection(language_pair, website, similarity_measure, dictionary, embedding):
    # path_forward = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".forward"
    # path_backward = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".backward"
    # path_intersection = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".intersection"
    path_forward = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".forward"
    path_backward = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".backward"
    path_intersection = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".intersection"
    forward = read_file(path_forward)
    forward_sents=read_file_for_intersection(path_forward)
    backward = read_file(path_backward)
    backward_sents=read_file_for_intersection(path_backward)

    intersection = open(path_intersection, "a")
    for i in range(len(forward)):
        if forward[i] in backward:
            intersection.write('{}\t{}\n'.format(forward_sents[i], backward_sents[backward.index(forward[i])].split('\t')[-1]))
    intersection.close()


def recall_precision(language_pair, website, similarity_measure, dictionary, embedding):
    # path_forward = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".forward"
    # path_backward = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".backward"
    # path_intersection = "/media/laka/Lakmali/FYP/dilan_paper/"+ language_pair + "/" + website + "/" + similarity_measure + ".intersection"
    path_forward = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".forward"
    path_backward = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".backward"
    path_intersection = "/userdirs/aloka/p2_parallel_corpus_mining/logs_sent_alingment/"+language_pair+"_"+website+"_"+embedding+"_"+similarity_measure+"_dic"+str(dictionary)+".intersection"
    path_golden = "/userdirs/aloka/p2_parallel_corpus_mining/comparable-corpus/Comparable_Sentences_with_Golden_Alignment_v2/"+language_pair+"/"+website+"/"+"sentences/"+website+"."+language_pair
    forward = read_file(path_forward)
    backward = read_file(path_backward)
    intersection = read_file(path_intersection)
    golden = read_file(path_golden)

    print('Golden Sentences: {}'.format(len(golden)))
    print('forward Sentences: {}'.format(len(forward)))
    print('backward Sentences: {}'.format(len(backward)))
    print('intersection Sentences: {}'.format(len(intersection)))

    print('Scores:')
    print ("---------------Forward---------------------")
    cal_recall_precision(golden, forward)
    print ("---------------Backward--------------------")
    cal_recall_precision(golden, backward)
    print ("---------------Intersection----------------")
    cal_recall_precision(golden, intersection)


def cal_recall_precision(golden, alignment):
    alignment_count=len(alignment)
    match_count = 0
    for i in golden:
        if i in alignment:
            match_count += 1

    #recall
    recall = (match_count / len(golden)) * 100
    precision = (match_count/alignment_count)*100
    F1=2*recall*precision/(recall+precision)

    print('{:10}{:10}{:10}{:10}'.format('Sents', 'R', 'P', 'F1'))
    print('{:<10d}{:<10.3f}{:<10.3f}{:<10.3f}'.format(match_count, recall, precision, F1))
    #print ("Recall :", recall)
    #print ("Matches :", match_count)




def loadDictionary(language_pair):

    root_dir = "/userdirs/aloka/p2_parallel_corpus_mining/Dictionaries/"+language_pair
    
    dictionaryA=''
    dictionaryB=''
    personNamesA=''
    personNamesB=''
    designationsA=''
    designationsB=''

    if language_pair == 'si-en':
        dictionaryA = root_dir + "/combineddictionary.en"
        dictionaryB = root_dir + "/combineddictionary.si"
        #dictionaryA = root_dir + "/9.comDic-augDicGlUn-ndDicUn.en"
        #dictionaryB = root_dir + "/9.comDic-augDicGlUn-ndDicUn.si"
        personNamesA = root_dir + "/person-names.en"
        personNamesB = root_dir + "/person-names.si"
        designationsA =  root_dir + "/designations.en"
        designationsB = root_dir + "/designations.si"
        print(dictionaryA)

    if language_pair == 'ta-en':
        dictionaryA = root_dir + "/combinedGlossary.en"
        dictionaryB = root_dir + "/combinedGlossary.ta"
        # dictionaryA = root_dir + "/existingdictionary.en"
        # dictionaryB = root_dir + "/existingdictionary.ta"
        personNamesA = root_dir + "/person-names.en"
        personNamesB = root_dir + "/person-names.ta"
        designationsA = root_dir + "/designations.en"
        designationsB = root_dir + "/designations.ta"

    if language_pair == 'si-ta':
        dictionaryA = root_dir + "/combinedDictionaryNew.ta"
        dictionaryB = root_dir + "/combinedDictionaryNew.si"
        # dictionaryA = root_dir + "/existingdictionary.ta"
        # dictionaryB = root_dir + "/existingdictionary.si"
        personNamesA = root_dir + "/person-names.ta"
        personNamesB = root_dir + "/person-names.si"
        designationsA = root_dir + "/designations.ta"
        designationsB = root_dir + "/designations.si"

    # wordDictionary = []

    with open(dictionaryA) as dictionaryFileA:
        with open(dictionaryB) as dictionaryFileB:
            linesA = dictionaryFileA.readlines()
            linesB = dictionaryFileB.readlines()
            for i in range(len(linesA)):
                word = linesA[i].strip().replace("\n", "").lower()
                if (wordDictionary.get(word, False)):
                    if (linesB[i].strip().replace("\n", "") not in wordDictionary.get(word)):
                        wordDictionary[word].append(linesB[i].strip().replace("\n", ""))
                else:
                    wordDictionary[word]  = [linesB[i].strip().replace("\n", "")]

    with open(designationsA) as designationsFileA:
        with open(designationsB) as designationsFileB:
            linesA = designationsFileA.readlines()
            linesB = designationsFileB.readlines()
            for i in range(len(linesA)):
                word = linesA[i].strip().replace("\n", "").lower()
                if (wordDictionary.get(word, False)):
                    wordDictionary[word].append(linesB[i].strip().replace("\n", ""))
                else:
                    wordDictionary[word]  = [linesB[i].strip().replace("\n", "")]

    with open(personNamesA) as personNamesA:
        with open(personNamesB) as personNamesB:
            namesA = personNamesA.readlines()
            namesB = personNamesB.readlines()
            for  i in range(len(namesA)):
                nameA = namesA[i].strip().replace("\n", "")
                if (wordDictionary.get(nameA, False)):
                    wordDictionary[nameA].append(namesB[i].strip().replace("\n", ""))
                else:
                    wordDictionary[nameA] = [namesB[i].strip().replace("\n", "")]

    return wordDictionary



def load_sdml_model(language_pair):
    filename = '/media/laka/Lakmali/FYP/ml_paper/'+ language_pair + '/SDML.sav'
    sdml = pickle.load(open(filename, 'rb'))
    return sdml


def load_itml_model(language_pair):
    filename = '/media/laka/Lakmali/FYP/ml_paper/'+ language_pair + '/ITML.sav'
    itml = pickle.load(open(filename, 'rb'))
    return itml


if __name__ == "__main__":
    main()
