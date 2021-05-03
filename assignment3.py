from nltk.corpus import wordnet as wn
import sys
import re

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


def main():
	data1 = question1(sys.argv[1])
	print("Question 1")
	print(str(data1[0]) + " word(s) refer to a relative")
	print("These words are: " + ", ".join(data1[1]))
	print(str(data1[2]) + " word(s) refer to an illness")
	print("These words are: " + ", ".join(data1[3]))
	print(str(data1[4]) + " word(s) refer to a science")
	print("These words are: " + ", ".join(data1[5]))
	

if __name__ == '__main__':
	main()
