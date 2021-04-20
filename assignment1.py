# Project Text Analysis
# Assignment 1 part 1
# 20-04-2021

# USAGE: in the command line, type 'python3 assignment1.py <text.txt>'


import random
import sys
import re
import nltk
nltk.download(['punkt'])


def read_text(txt):
	with open(txt, 'r') as infile:
		lines = infile.read()

	tokenized_text = nltk.sent_tokenize(lines)
	return lines, tokenized_text


def longest_sentence(sentences):
	
	longest_sent_list = ['']
	for sent in sentences:
		if len(sent) > len(longest_sent_list[0]):
			longest_sent_list = [sent]
		elif len(sent) == len(longest_sent_list[0]):
			longest_sent_list.append(sent)
	
	if len(longest_sent_list) > 1:
		random_sentence = longest_sent_list[random.randrange(len(longest_sent_list))]
		return random_sentence
	else:
		return longest_sent_list[0]
	

def shortest_sentence(sentences):
	
	shortest_sent_list = [sentences[0]]
	for sent in sentences:
		if len(sent) < len(shortest_sent_list[0]):
			shortest_sent_list = [sent]
		elif len(sent) == len(shortest_sent_list[0]):
			shortest_sent_list.append(sent)
	
	if len(shortest_sent_list) > 1:
		random_sentence = shortest_sent_list[random.randrange(len(shortest_sent_list))]
		return random_sentence
	else:
		return shortest_sent_list[0]


def length_distribution(sentences):
	
	dist_dict = {}
	for sent in sentences:
		if len(sent) in dist_dict:
			dist_dict[len(sent)] += 1
		else:
			dist_dict[len(sent)] = 1
	
	return dict(sorted(dist_dict.items()))
	

def average_length(sentences):
	
	total_length = 0
	total_sentences = 0
	
	for sent in sentences:
		total_sentences += 1
		total_length += len(sent)
	
	return round(total_length / total_sentences, 2)


def char_types(txt):
	# Character uni-grams
	token_char = nltk.ngrams(txt, 1)
	type_char = set(token_char)
	sorted_dist = sorted(type_char, key=lambda item: item[0])

	return len(sorted_dist), sorted_dist


def top_char(txt):
	uni_char = list(nltk.ngrams(txt, 1))
	bi_char = list(nltk.ngrams(txt, 2))
	tri_char = list(nltk.ngrams(txt, 3))
	total_char = uni_char + bi_char + tri_char

	fdist = nltk.FreqDist(total_char)

	return fdist.most_common(20)


def main():
	text, sentences = read_text(sys.argv[1])
	longest_sent = longest_sentence(sentences)

	print()
	print('Longest sentence: ' + longest_sent)
	print()
	shortest_sent = shortest_sentence(sentences)
	print('Shortest sentence: ' + shortest_sent)
	print()
	distribution = length_distribution(sentences)
	print('Sentence length distribution (length: quantity)')
	print()
	print(distribution)
	print()
	average = average_length(sentences)
	print('Average sentence length: ' + str(average))
	print()

	amount_chartypes, total_chartypes = char_types(text)
	print(f'Amount of character types found: {amount_chartypes}\n{total_chartypes}\n')

	top20_chartypes = top_char(text)
	print(f'Top 20 most common uni, bi and trigram characters: \n{top20_chartypes}\n')


if __name__ == '__main__':
	main()