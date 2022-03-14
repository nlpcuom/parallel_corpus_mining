#Document Alignment

#embedding filepaths
newsSource="hiru"
embeddingPathA="/userdirs/aloka/p2_parallel_corpus_mining/embeddings_laser/hiru/en/"
embeddingPathB="/userdirs/aloka/p2_parallel_corpus_mining/embeddings_laser/hiru/si/"

#textfiles in respective languages
readbleDataPathA="/userdirs/aloka/p2_parallel_corpus_mining/textfiles/hiru/en/" 
readbleDataPathB="/userdirs/aloka/p2_parallel_corpus_mining/textfiles/hiru/si/"

#en-si
#goldenAlignmentPath="comparable-corpus/comparable_documnets_with_golden_alignment_v2/hiru/hiru_english_sinhala.txt"



mlModelPath="cerebrex_code_B/model2_itm2.sav"
option="laser" #laser, xlmr
dimension=1024 #laser-1024 | xmlr,labse-768
metric="euclidean" #metric, cosine, euclidean

echo "Document Alignment for $newsSource"

python3 cerebrex_code_A/main.py \
	$embeddingPathA \
	$embeddingPathB \
	$readbleDataPathA \
	$readbleDataPathB \
	$goldenAlignmentPath \
	$mlModelPath \
	$option \
	$dimension \
	$metric