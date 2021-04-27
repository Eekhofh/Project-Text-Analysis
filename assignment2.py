import nltk
from nltk.collocations import *
from nltk.corpus import brown
from nltk.tag import UnigramTagger
import sys

nltk.download('brown')
nltk.download('averaged_perceptron_tagger')


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


def brownpos():
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')

    # Exercise 2.2a
    print(f'Total words found: {len(br_tw)}')
    print(f'Total sentences found: {len(br_ts)}\n')

    # Exercise 2.2b
    print(f"The 50th word is {br_tw[49][0]} and it's: {br_tw[49][1]} (Adjective)")
    print(f"The 75th word is {br_tw[74][0]} and it's: {br_tw[74][1]} (Preposition)\n")

    # Exercise 2.2c
    counted_items = []
    for word in br_tw:
        if word[1] not in counted_items:
            counted_items.append(word[1])

    print(f'There are {len(counted_items)} different tags represented in the Brown Mystery category\n')
    counted_items.clear()

    # Exercise 2.2d/e
    brown_words = []
    for word in br_tw:
        brown_words.append(word[0])
    freq_words = nltk.FreqDist(brown_words)
    brown_words.clear()

    brown_pos = []
    for word in br_tw:
        brown_pos.append(word[1])

    freq_pos = nltk.FreqDist(brown_pos)
    brown_pos.clear()

    print('15 Most common words and their frequency')
    print(freq_words.most_common()[:15])
    print()
    print('15 Most common POS and their frequency')
    print(freq_pos.most_common()[:15])
    print()

    # Exercise 2.2f
    pos_sent1 = []
    for word in br_ts[19]:
        pos_sent1.append(word[1])

    pos_sent2 = []
    for word in br_ts[39]:
        pos_sent2.append(word[1])

    freq_sent1 = nltk.FreqDist(pos_sent1)
    freq_sent2 = nltk.FreqDist(pos_sent2)
    pos_sent1.clear()
    pos_sent2.clear()

    print(f'Most common POS in sentence 20: {freq_sent1.most_common(1)} (3rd. singular nominative pronoun)')
    print(f'Most common POS in sentence 40: {freq_sent2.most_common(1)} (3rd. singular nominative pronoun)\n')

    # Exercise 2.2g
    adverbs_brown = []
    # Words
    for word in br_tw:
        if word[1] == 'RB' or word[1] == 'RBR' or word[1] == 'RBT':
            adverbs_brown.append(word[0])

    # Sentences
    for sentence in br_ts:
        for word in sentence:
            if word[1] == 'RB' or word[1] == 'RBR' or word[1] == 'RBT':
                adverbs_brown.append(word[0])

    freq_adverbs = nltk.FreqDist(adverbs_brown)
    adverbs_brown.clear()
    print(f'Most common Adverb is: {freq_adverbs.most_common(1)}')

    # Exercise 2.2h
    adjectives_brown = []
    # Words
    for word in br_tw:
        if word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS' or word[1] == 'JJT':
            adjectives_brown.append(word[0])

    # Sentences
    for sentence in br_ts:
        for word in sentence:
            if word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS' or word[1] == 'JJT':
                adjectives_brown.append(word[0])

    freq_adjectives = nltk.FreqDist(adjectives_brown)
    adjectives_brown.clear()
    print(f'Most common Adjective is: {freq_adjectives.most_common(1)}\n')

    # Exercise 2.2i

    so_brown = []
    # Words
    for word in br_tw:
        if word[0].lower() == 'so':
            so_brown.append(word[1])

    # Sentences
    for sentence in br_ts:
        for word in sentence:
            if word[0].lower() == 'so':
                so_brown.append(word[1])

    print(f'The most common POS tags for so are: {set(so_brown)}')
    print(f'(Adjective, Qualifier and Subordinating Conjunction)\n')

    # Exercise 2.2j
    freq_so = nltk.FreqDist(so_brown)
    print(f'Most common POS tag for so is: {freq_so.most_common(1)}\n')

    # Exercise 2.2k
   

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
    brownpos()


if __name__ == "__main__":
    main()
