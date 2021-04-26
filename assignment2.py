import nltk
from nltk.collocations import *
import sys


def coll_pmi(text_file):
	with open(text_file, 'r') as infile:
		text = infile.read()
	
	tokens = nltk.wordpunct_tokenize(text)
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.pmi)
	sorted(bigram for bigram, score in scored)
	return scored[0:19]
	

def coll_chi(text_file):
	with open(text_file, 'r') as infile:
		text = infile.read()
	
	tokens = nltk.wordpunct_tokenize(text)
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.chi_sq)
	sorted(bigram for bigram, score in scored)
	return scored[0:19]


def manual_pos():
	print(
		'''
		Penn Treebank POS tagset
		Peter: NN
		really: RB
		liked: VBD
		the: DT
		movies: NN
		and: CC
		warm: JJ
		pop-corn: NN
		He: PRP
		would: VBD
		never: RB
		bring: VBD
		Mira: NN
		with: IN
		him: PRP
		though:
		
		Brown Corpus Tagset
		Peter: NN
		really: RB
		liked: VBD
		the: AT
		movies: NNS
		and: CC
		warm: JJ
		pop-corn: NN
		.: .
		He: PPS
		would: MD
		never: RB
		bring: VB
		Mira: NN
		with: IN
		him: PPO
		,: ,
		though: RB
		.: .
		
		NLTK Universal Tagset
		Peter: NOUN
		really: ADV
		liked: VERB
		the: DET
		movies: NOUN
		and: CONJ
		warm: ADJ
		pop-corn: NOUN
		.: .
		He: NOUN
		would: VERB
		never: ADV
		bring: VERB
		Mira: NOUN
		with: ADP
		him: NOUN
		,: .
		though: ADJ
		.: .
		''')


def main():
	pmiscores = coll_pmi(sys.argv[1])
	print("20 most like collocations using Pointwise Mutual Information:\n")
	print(pmiscores)
	print()
	chiscores = coll_chi(sys.argv[1])
	print("20 most like collocations using Chi-Squared:\n")
	print(chiscores)
	print()
	print("Any differences might be explained by differences in the ways PMI and Chi-Sq. are calculated\n")
	manual_pos()
	print()
	
	
if __name__ == "__main__":
	main()
