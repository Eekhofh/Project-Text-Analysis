from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
from nltk import sent_tokenize
import wikipedia


def get_wiki(subject):
	page = wikipedia.page(subject)
	return sent_tokenize(page.content)


def disambiguation(sentence, word, pos):
	sent = word_tokenize(sentence)
	synset = lesk(sent, word, pos)
	return word + ": " + synset.definition()
	
def find_ambiguous(sentence):
	sent = word_tokenize(sentence)
	ambiguous_words = []
	total_senses = 0
	for word in sent:
		definitions = []
		for ss in wordnet.synsets(word, 'n'):
			definitions.append(ss.definition)
		if len(definitions) > 1:
			ambiguous_words.append(word)
			total_senses += len(definitions)
	return ambiguous_words, total_senses


def main():
	total_senses = 0
	total_ambiguous_words = 0
	pages = ["Mathematics", "Call of Duty", "Soccer"]
	for page in pages:
		ambiguous_words_definitions = []
		sentences = get_wiki(page)
		for sent in sentences:
			ambiguous_words = find_ambiguous(sent)[0]
			total_ambiguous_words += len(find_ambiguous(sent)[0])
			total_senses += find_ambiguous(sent)[1]
			for word in ambiguous_words:
				definition = disambiguation(sent, word, 'n')
				ambiguous_words_definitions.append(definition)
	
	print("Question 1")
	print("The proportion of polysemous words per Wikipedia page is " + str(round(total_ambiguous_words / len(pages), 2)) + " per page.")
	print()
	print("Question 2")
	for page in pages:
		if len(ambiguous_words_definitions) == 0:
			print("The page about " + page + " has 0 polysemous words.")
		else:
			print("The page about " + page + " has at least 1 polysemous word.")
	print()
	print("Question 3")
	print("The average number of senses for the polysemous words is " + str(round(total_senses / total_ambiguous_words, 2)))
	
	
main()
