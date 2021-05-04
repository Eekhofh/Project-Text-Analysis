from nltk.corpus import wordnet as wn
from nltk.parse import CoreNLPParser
from nltk import download
import sys
import re

download('wordnet')

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


def ner_wordnet(text_file):
	with open(text_file, 'r') as infile:
		text = infile.read()
		tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
		print(list(tagger.tag(text.split())))
		# In exercise 2.1, not all Tags are correct. King is not an organization!
		# In exercise 2.2, the 4 tag class model is almost the same as the 3 class model.
		# So I have chosen to use the 7 class model, since it correctly classifies the word 'King' as Person.




def main():
	text = sys.argv[1]
	data1 = question1(sys.argv[1])
	print("Question 1")
	print(str(data1[0]) + " word(s) refer to a relative")
	print("These words are: " + ", ".join(data1[1]))
	print(str(data1[2]) + " word(s) refer to an illness")
	print("These words are: " + ", ".join(data1[3]))
	print(str(data1[4]) + " word(s) refer to a science")
	print("These words are: " + ", ".join(data1[5]))
	print('Exercise 2')
	# Do not run without server!
	ner_wordnet(text)
	

if __name__ == '__main__':
	main()
