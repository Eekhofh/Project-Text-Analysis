# Project Text Analysis
# Assignment 1 part 1
# 20-04-2021


import random
import sys
import re
import nltk


def split_sentences(text_file):
	with open(text_file, 'r') as infile:
		lines = infile.read()
	
	sentences = nltk.sent_tokenize(lines)
	return sentences
		

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
		

def main():
	sentences = split_sentences(sys.argv[1])
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
	

if __name__ == '__main__':
	main()
