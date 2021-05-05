import nltk
from nltk.parse import CoreNLPParser
from nltk import download, word_tokenize, pos_tag, ne_chunk
import sys

download('wordnet')
download('maxent_ne_chunker')
download('words')


def ner_wordnet(text_file):
	# Server is required to run this

	with open(text_file, 'r') as infile:
		text = infile.read()
		tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
		print('Exercise 2.1')
		tagged_text = list(tagger.tag(text.split()))
		print(tagged_text)
		# In exercise 2.1, not all Tags are correct. King is not an organization!
		# In exercise 2.2, the 4 tag class model is almost the same as the 3 class model.
		# So I have chosen to use the 7 class model, since it correctly classifies the word 'King' as Person.

		text_tokens = word_tokenize(text)
		pos_tokens = pos_tag(text_tokens)
		nouns = []
		type_nouns = ['NN', 'NNS', 'NNP', 'NNPS']

		for pos_token in pos_tokens:
			if pos_token[1] in type_nouns:
				nouns.append(pos_token[0])

		chunks_tree = ne_chunk(pos_tokens)

		tagged_nouns = []

		# Get tagged chunks
		for chunk in chunks_tree:
			if type(chunk) == nltk.tree.Tree:
				tag = chunk.label()
				tag_string = ''
				if len(chunk.leaves()) > 1:
					for leave in chunk.leaves():
						if tag_string == '':
							tag_string += leave[0]
						else:
							tag_string = tag_string + ' ' + leave[0]
				else:
					tag_string = chunk.leaves()[0][0]

				complete_tag = (tag_string, tag)
				tagged_nouns.append(complete_tag)

		# Get tagged words and merge them with the chunks
		for tagged_word in tagged_text:
			if tagged_word[0] in nouns and not tagged_word[1] == 'O':
				in_text = False
				for tagged_noun in tagged_nouns:
					if tagged_word[0] in tagged_noun[0]:
						in_text = True
						break

				if not in_text:
					tagged_nouns.append(tagged_word)

		print(f'Exercise 2.3\nAll tagged nouns: \n{tagged_nouns}')


def main():
	text = sys.argv[1]
	ner_wordnet(text)


if __name__ == '__main__':
	main()
