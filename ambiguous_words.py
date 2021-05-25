from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import word_tokenize
from nltk import sent_tokenize
import wikipedia
import random


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
	word_sense = []

	for word in sent:
		definitions = []
		senses = []
		for ss in wordnet.synsets(word, 'n'):
			definitions.append(ss.definition)
			senses.append(ss.definition())

		if len(definitions) > 1:
			ambiguous_words.append(word)

			total_senses += len(definitions)
		if len(definitions) > 0:
			word_sense.append((word, senses))

	return ambiguous_words, total_senses, word_sense



def main():
	total_senses = 0
	total_ambiguous_words = 0
	pages = ["Mathematics", "Call of Duty", "Soccer"]
	found_words = {}
	random_ambiguous_list = []
	total_ambiguous_def = []
	for page in pages:
		ambiguous_words_definitions = []
		sentences = get_wiki(page)
		for sent in sentences:
			ambiguous_words, senses, found_word_senses = find_ambiguous(sent)
			total_ambiguous_words += len(ambiguous_words)
			total_senses += senses

			for found_word_sense in found_word_senses:
				if found_word_sense[0] not in found_words:

					found_words[found_word_sense[0].lower()] = found_word_sense[1]

				else:
					found_words[found_word_sense[0].lower()].extend(found_word_sense[1])

			for word in ambiguous_words:
				definition = disambiguation(sent, word, 'n')
				ambiguous_words_definitions.append(definition)
				total_ambiguous_def.append((definition, sent))

	for i in range(7):
		index = random.randint(0, len(total_ambiguous_def) - 1)
		random_ambiguous_list.append(total_ambiguous_def[index])

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
	print()
	print('Question 4')
	found_words_numbers = {}
	for key in found_words:
		if len(found_words[key]) not in found_words_numbers:
			found_words_numbers[len(found_words[key])] = 1
		else:
			found_words_numbers[len(found_words[key])] += 1

	for key in (found_words_numbers):
		print(f'{found_words_numbers[key]} words showed {key} senses\n')

	print("Question 5")
	# Only used to get the words
	# for i in range(len(random_ambiguous_list)):
	# 	print(f'Word:\n{random_ambiguous_list[i][0]}\nContext:\n{random_ambiguous_list[i][1]}\n')

	print("Question 6")
	print("It has occured once that a word has been assigned a different sense, which is \'game\'.")
	print("It has probably been assigned the sense for the word \'mobile\', which it has taken from the context.")
	print("With more context, I believe the algorithm would have found the right sense, because it could have recognized the words ")
	print("\'release\', \'update\' and \'online\', which all have to do with gaming and not so much with gaming equipment.")

	print("Question 7")
	print("No, I would have thought the algorithm would be more accurate. In my opinion, the context clues should be enough to correctly show the right sense.")
	print("For words like \'Recon\', it's understandable, since it's part of a title. But for example, the word \'games\' could be correct, given ")
	print("the context, which contains the word \'developed\'. On the other hand, it could have been confused by the word \'outside\', where ")
	print("the outcome could have come from, since hunting is outside.")

	print("Question 8")
	print("Look at more of the context. This will take more time for the program to run, but will yield far more accurate results. We have not tested this, ")
	print("but given the context of some words, plus the additional context which would have been a lot clearer and maybe more helpful to the algorithm, ")
	print("my prediction is that more context is equal to higher accuracy, but also to more time needed.")

main()
