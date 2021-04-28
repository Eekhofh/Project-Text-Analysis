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
        Exercise 2.1
        
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
    print('Exercise 2.2\n')
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
    so_adj = ('so', 'RB')
    so_qual = ('so', 'QL')
    so_sub = ('so', 'CS')

    print('So Adverb Sentence')
    for sentence in br_ts:
        if so_adj in sentence:
            new_sentence = ''
            for word in sentence:
                new_sentence += (' ' + word[0])
            print(new_sentence)
            break

    print('\nSo Qualifier Sentence')
    for sentence in br_ts:
        if so_qual in sentence:
            new_sentence = ''
            for word in sentence:
                new_sentence += (' ' + word[0])
            print(new_sentence)
            break

    print('\nSo Subordinating Conjunction Sentence')
    for sentence in br_ts:
        if so_sub in sentence:
            new_sentence = ''
            for word in sentence:
                new_sentence += (' ' + word[0])
            print(new_sentence)
            break

    print()
    # Exercise 2.2l
    so_adj_prev = []
    so_adj_fol = []

    so_qual_prev = []
    so_qual_fol = []

    so_sub_prev = []
    so_sub_fol = []
    for sentence in br_ts:
        word_position = 0
        for word in sentence:
            if word[0] == 'so' and word[1] == 'RB':
                prev_word = sentence[word_position - 1]
                fol_word = sentence[word_position + 1]
                so_adj_prev.append(prev_word[1])
                so_adj_fol.append(fol_word[1])

            elif word[0] == 'so' and word[1] == 'QL':
                prev_word = sentence[word_position - 1]
                fol_word = sentence[word_position + 1]
                so_qual_prev.append(prev_word[1])
                so_qual_fol.append(fol_word[1])

            elif word[0] == 'so' and word[1] == 'CS':
                prev_word = sentence[word_position - 1]
                fol_word = sentence[word_position + 1]
                so_sub_prev.append(prev_word[1])
                so_sub_fol.append(fol_word[1])

            word_position += 1

    print('\nMost likely POS preceding and following So as Adverb.')
    so_adj_freq_prev = nltk.FreqDist(so_adj_prev)
    print(so_adj_freq_prev.most_common(1)[0][0])

    so_adj_freq_fol = nltk.FreqDist(so_adj_fol)
    print(so_adj_freq_fol.most_common(1)[0][0])

    print('\nMost likely POS preceding and following So as Qualifier.')
    so_qual_freq_prev = nltk.FreqDist(so_qual_prev)
    print(so_qual_freq_prev.most_common(1)[0][0])

    so_qual_freq_fol = nltk.FreqDist(so_qual_fol)
    print(so_qual_freq_fol.most_common(1)[0][0])

    print('\nMost likely POS preceding and following So as Subordinating Conjunction.')
    so_sub_freq_prev = nltk.FreqDist(so_sub_prev)
    print(so_sub_freq_prev.most_common(1)[0][0])

    so_sub_freq_fol = nltk.FreqDist(so_sub_fol)
    print(so_sub_freq_fol.most_common(1)[0][0])

def manual_pos_tag(text_file):
    with open(text_file, 'r') as infile:
        text = infile.read()

    text = nltk.word_tokenize(text)
    tagged_text = nltk.pos_tag(text)
    return tagged_text

def collocations(text_file):
    text = manual_pos_tag(text_file)
    #text = nltk.Text(text)
    #print(text.collocations())
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text)
    return finder.nbest(bigram_measures.chi_sq, 5)


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
    print()
    print('(Next assignment is cut off at 100 POS tags, to not clutter the screen.)')
    print(manual_pos_tag(sys.argv[1])[0:100])
    print()
    print('Top 5 POS collocations, using Chi-Squared: (Using PMI, the list is the same)')
    print(collocations(sys.argv[1]))
    print('All these bigrams all occur a maximum of 1 times next to each other in holmes.txt')
    print('Not one bigram is the same.')
    print('/')


if __name__ == "__main__":
    main()
