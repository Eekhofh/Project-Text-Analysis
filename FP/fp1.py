import nltk
from nltk.corpus import wordnet as wn
import re
import sys

def hypernymOf(synset1, synset2):
	if synset1 == synset2:
		return True
	for hypernym in synset1.hypernyms():
		if synset2 == hypernym:
			return True
		if hypernymOf(hypernym, synset2):
			return True
	return False

def read_file(text_file):
	with open(text_file, 'r') as infile:
		text = infile.readlines()
	return " ".join(text)
	
def tokenize_sentences(text_file):
	text = read_file(text_file)
	return nltk.sent_tokenize(text)
	
def tokenize_words(text_file):
	text = tokenize_sentences(text_file)
	tokenized_text = []
	for sent in text:
		tokenized_text.append(nltk.word_tokenize(sent))
	return tokenized_text
	
def chunk(sentences):
	tagged_sents = []
	named_sents = []
	for sent in sentences:
		tagged_sent = nltk.pos_tag(sent)
		tagged_sents.append(tagged_sent)
	for sent in tagged_sents:
		named_sent = nltk.ne_chunk(sent, binary=False)
		named_sents.append(named_sent)
	return named_sents
				
def get_persons_orgs(named_text):
	persons = []
	organizations = []
	for sentence in named_text:
		for word in sentence:
			if 'PERSON' in str(word):
				persons.append(str(word).split('/')[0].split(" ")[1].lower())
			elif 'ORGANIZATION' in str(word):
				organizations.append(str(word).split('/')[0].split(" ")[1].lower())
	return persons, organizations
	
def get_nature_words():
	natural_place = wn.synsets('formation')[3]
	natural_place_hyponyms = []
	nature_words = []
	for hyponym in natural_place.hyponyms():
		natural_place_hyponyms.append(hyponym.definition().lower())
	
	nature_words = [token for token, pos in nltk.pos_tag(nltk.word_tokenize(" ".join(natural_place_hyponyms))) if pos.startswith('N')]
	return nature_words

def get_entertainment():
	# Book/Film titles always start with capital letters.
	# Though not always: Born to run. But: Mission Impossible
	# How to check if title is book or film AND assign the tags to ALL words?
	return None


def name_entities(persons, organizations, nature_words, tokenized_text):
	organization = wn.synsets('organization')[0]
	animal = wn.synsets('animal')[0]
	sport = wn.synsets('sport')[0]


	with open('named_text.txt', 'w') as outfile:
		
		for sentence in tokenized_text:
			i = 0
			while i < len(sentence):
				try:
					word = wn.synsets(re.sub('[.,"\'!?:;()]+', r'', sentence[i].lower()))[0]
					if hypernymOf(word, animal) == True:
						outfile.write(sentence[i] + " (ANI) ")
					elif hypernymOf(word, sport) == True and sentence[i].lower() != 'sport':
						outfile.write(sentence[i] + " (SPO) ")
					elif sentence[i][0].isupper() and 'city' in word.definition().lower() or 'town' in word.definition().lower() or 'capital' in word.definition().lower() or 'village' in word.definition().lower():
						outfile.write(sentence[i] + " (CIT) ")
					elif sentence[i].lower() in persons:
						outfile.write(sentence[i] + " (PER) ")
					elif sentence[i][0].isupper() and 'nation' in word.definition().lower() or 'republic' in word.definition().lower() or 'monarchy' in word.definition().lower():
						outfile.write(sentence[i] + " (COU) ")
					else:
						nature_matches = 0
						for w in nltk.word_tokenize(word.definition().lower()):
							if w in nature_words:
								nature_matches += 1
						if nature_matches > 0 and sentence[i][0].isupper():
							outfile.write(sentence[i] + " (NAT) ")
						elif sentence[i].lower() in organizations:
							outfile.write(sentence[i] + " (ORG) ")
						else:
							outfile.write(sentence[i] + " ")
					i += 1
				except IndexError:
					outfile.write(sentence[i] + " ")
					i += 1

def main():
	text = tokenize_words(sys.argv[1])
	
	chunked_text = chunk(text)
	persons = get_persons_orgs(chunked_text)[0]
	organizations = get_persons_orgs(chunked_text)[1]
	nature_words = get_nature_words()
	
	name_entities(persons, organizations, nature_words, text)

main()
