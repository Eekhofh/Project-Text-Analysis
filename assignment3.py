from nltk.corpus import wordnet as wn
from nltk.parse import CoreNLPParser
from nltk import download, word_tokenize, pos_tag, sent_tokenize, ne_chunk
import sys
import re
from random import randrange

download('wordnet')
download('maxent_ne_chunker')
download('words')



def hypernymOf(synset1, synset2):
	if synset1 == synset2:
		return True
	for hypernym in synset1.hypernyms():
		if synset2 == hypernym:
			return True
		if hypernymOf(hypernym, synset2):
			return True
	return False


def question1(text_file):
	relatives = 0
	relatives_words = []
	illnesses = 0
	illnesses_words = []
	sciences = 0
	sciences_words = []
	with open(text_file, 'r') as infile:
		fl = infile.read()
	relative = wn.synsets('relative')[0]
	illness = wn.synsets('illness')[0]
	science = wn.synsets('science')[0]
	words = fl.split(' ')
	for w in words:
		try:
			word = wn.synsets(re.sub('[.,"\'!?:;()]+', r'', w.lower()))[0]
			if hypernymOf(word, relative) == True:
				relatives += 1
				relatives_words.append(w)
			elif hypernymOf(word, illness) == True:
				illnesses += 1
				illnesses_words.append(w)
			elif hypernymOf(word, science) == True:
				sciences += 1
				sciences_words.append(w)
		except IndexError:
			continue
	return relatives, relatives_words, illnesses, illnesses_words, sciences, sciences_words


def question2(text_file):
	top_hypernyms = ['act', 'animal', 'artifact', 'attribute', 'body', 'cognition', 'communication', 'event', 'feeling', 'food', 'group', 'location', 'motive', 'natural object', 'natural phenomenon', 'person', 'plant', 'possession', 'process', 'quantity', 'relation', 'shape', 'state', 'substance', 'time']
	class_dict = {}
	with open(text_file, 'r') as infile:
		fl = infile.read()	
	words = re.sub('[.,;:!?\'")(]+', r'', fl.lower())
	words = re.sub('[\n]+', r' ', words)
	nouns = [word for word, pos in pos_tag(word_tokenize(words)) if pos == 'NN']
	for hypernym in top_hypernyms:
		for noun in nouns:
			if noun != 'ada':
				try:
					noun_synset = wn.synsets(noun)[0]
					if hypernymOf(noun_synset, wn.synsets(hypernym)[0]):
						if hypernym in class_dict:
							if noun not in class_dict[hypernym]:
								class_dict[hypernym].append(noun)
						else:
							class_dict[hypernym] = [noun]
				except IndexError:
					continue
	
	noun_dict = {}
	for noun_list in class_dict.values():
		for noun in noun_list:
			if noun in noun_dict:
				noun_dict[noun] += 1
			else:
				noun_dict[noun] = 1
	
	return noun_dict, class_dict


def ner_wordnet(text_file):
	with open(text_file, 'r') as infile:
		text = infile.read()
		tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
		print('Exercise 2.1')
		print(list(tagger.tag(text.split())))
		# In exercise 2.1, not all Tags are correct. King is not an organization!
		# In exercise 2.2, the 4 tag class model is almost the same as the 3 class model.
		# So I have chosen to use the 7 class model, since it correctly classifies the word 'King' as Person.
		text_tokens = word_tokenize(text)
		text_sents = sent_tokenize(text)
		pos_text = pos_tag(text_tokens)
		print(ne_chunk(pos_text))


def wordnet_similarity(text_file):
	ranking = {}
	with open(text_file, 'r') as infile:
		text = infile.read()
	car_automobile = ('car', wn.synset('car.n.01'),'automobile', wn.synset('automobile.n.01'))
	coast_shore = ('coast', wn.synset('coast.n.01'), 'shore', wn.synset('shore.n.01'))
	food_fruit = ('food', wn.synset('food.n.01'), 'fruit', wn.synset('fruit.n.01'))
	journey_car = ('journey', wn.synset('journey.n.01'), 'car', wn.synset('car.n.01'))
	monk_slave = ('monk', wn.synset('monk.n.01'), 'slave', wn.synset('slave.n.01'))
	moon_string = ('moon', wn.synset('moon.n.01'), 'string', wn.synset('string.n.01'))
	pairs = [car_automobile, coast_shore, food_fruit, journey_car, monk_slave, moon_string]
	for pair in pairs:
		score = pair[1].wup_similarity(pair[3])
		pair_name = f'{pair[0]}-{pair[2]}'
		ranking[pair_name] = score

	sorted_ranking = dict(sorted(ranking.items(), key=lambda pair: pair[1], reverse=True))
	for pair, score in sorted_ranking.items():
		print(pair, score)
	print('The biggest difference between the two rankings is the switch between the medium-level similarity and the low-level similarity.')
	print('The top level remains the same by a large difference in score.')


def main():
	text = sys.argv[1]
	data1 = question1(sys.argv[1])
	print("Exercise 1.1")
	print()
	print(str(data1[0]) + " word(s) refer to a relative")
	print("These words are: " + ", ".join(data1[1]))
	print(str(data1[2]) + " word(s) refer to an illness")
	print("These words are: " + ", ".join(data1[3]))
	print(str(data1[4]) + " word(s) refer to a science")
	print("These words are: " + ", ".join(data1[5]))
	print()
	print('Exercise 1.2')
	hypernym_count = question2(sys.argv[1])[0]
	hypernyms = question2(sys.argv[1])[1] 
	one_hypernym = 0
	one_hypernym_nouns = []
	more_hypernyms = 0
	more_hypernym_nouns = []
	
	for noun in hypernym_count:
		if hypernym_count[noun] == 1:
			one_hypernym += 1
			one_hypernym_nouns.append(noun)
		else:
			more_hypernyms += 1
			more_hypernym_nouns.append(noun)
	
	one_hypernym_noun = one_hypernym_nouns[randrange(len(one_hypernym_nouns))]
	more_hypernym_noun = more_hypernym_nouns[randrange(len(more_hypernym_nouns))]
	
	one_hypernym_hypernyms = ""
	for h in hypernyms:
		if one_hypernym_noun in hypernyms[h]:
			one_hypernym_hypernyms += h
	
	more_hypernym_hypernyms = []
	for h in hypernyms:
		if more_hypernym_noun in hypernyms[h]:
			more_hypernym_hypernyms.append(h)
	
	print()
	print("NOTE: in the following answers, types (not tokens) were used")
	print("In " + str(one_hypernym) + " case(s), the noun was classified in only 1 hypernym")
	print("One of these nouns is '" + one_hypernym_noun + "', which belongs to the hypernym '" + one_hypernym_hypernyms + "'")
	print("In " + str(more_hypernyms) + " case(s), the noun was classified in more than 1 hypernym")
	print("One of these nouns is '" + more_hypernym_noun + "', which belongs to the hypernyms '" + "', '".join(more_hypernym_hypernyms) + "'")
	total_hypernyms = 0
	for noun in hypernym_count:
		total_hypernyms += hypernym_count[noun]
	hypernym_average = total_hypernyms / len(hypernym_count)
	print("The average amount of hypernyms per noun type is " + str(hypernym_average))
	# Do not run without server!
	#ner_wordnet(text)
	print()
	print('Exercise 1.3')
	print()
	wordnet_similarity(sys.argv[1])


if __name__ == '__main__':
	main()
