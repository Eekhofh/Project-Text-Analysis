import os
from collections import Counter
from nltk.metrics import ConfusionMatrix
import sys

def get_tags(path):
	file = f'{path}/en.tok.off.pos'
	with open(file, 'r') as infile:
		lines = infile.readlines()
		tags_content = []
		tags_found = []
		for line in lines:
			line = line.rstrip().split()
			if len(line) > 5:
				if line[5] in 'COU CIT NAT PER ORG ANI SPO ENT':
					tags_content.append(line[5])
					tags_found.append('y')
				else:
					tags_content.append('none')
					tags_found.append('n')
			else:
				tags_content.append("none")
				tags_found.append('n')
	return tags_found, tags_content
	

def tags_found():
	annotator1 = []
	root_path = sys.argv[1] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator1.extend(get_tags(path)[0])
	
	annotator2 = []
	root_path = sys.argv[2] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator2.extend(get_tags(path)[0])
	
	cm = ConfusionMatrix(annotator1, annotator2)

	print(cm)

	labels = set('y n'.split())
	
	true_positives = Counter()
	false_negatives = Counter()
	false_positives = Counter()
	
	for i in labels:
		for j in labels:
			try:
				if i == j:
					true_positives[i] += cm[i, j]
				else:
					false_negatives[i] += cm[i, j]
					false_positives[j] += cm[i, j]
			except KeyError as e:
				missing_tag = e.args[0]
				true_positives[missing_tag] = 0
		
	print("TP:", sum(true_positives.values()), true_positives)
	print("FN:", sum(false_negatives.values()), false_negatives)
	print("FP:", sum(false_positives.values()), false_positives)
	print()

	for i in sorted(labels):
		if true_positives[i] == 0:
			fscore = 0
			precision = 0
			recall = 0
		else:
			precision = true_positives[i] / float(true_positives[i] +
												false_positives[i])
			recall = true_positives[i] / float(true_positives[i] +
												false_negatives[i])
			fscore = 2 * (precision * recall) / float(precision + recall)
		print(i, "F-score:", fscore, ", Precision:", precision, ", Recall:", recall)		


def tags_content():
	annotator1 = []
	root_path = sys.argv[1] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator1.extend(get_tags(path)[1])
	
	annotator2 = []
	root_path = sys.argv[2] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator2.extend(get_tags(path)[1])
	
	cm = ConfusionMatrix(annotator1, annotator2)

	print(cm)

	labels = set('COU CIT NAT PER ORG ANI SPO ENT none'.split())
	
	true_positives = Counter()
	false_negatives = Counter()
	false_positives = Counter()
	
	for i in labels:
		for j in labels:
			try:
				if i == j:
					true_positives[i] += cm[i, j]
				else:
					false_negatives[i] += cm[i, j]
					false_positives[j] += cm[i, j]
			except KeyError as e:
				missing_tag = e.args[0]
				true_positives[missing_tag] = 0
		
	print("TP:", sum(true_positives.values()), true_positives)
	print("FN:", sum(false_negatives.values()), false_negatives)
	print("FP:", sum(false_positives.values()), false_positives)
	print()

	for i in sorted(labels):
		if true_positives[i] == 0:
			fscore = 0
			precision = 0
			recall = 0
		else:
			precision = true_positives[i] / float(true_positives[i] +
												false_positives[i])
			recall = true_positives[i] / float(true_positives[i] +
												false_negatives[i])
			fscore = 2 * (precision * recall) / float(precision + recall)
		print(i, "F-score:", fscore, ", Precision:", precision, ", Recall:", recall)


def main():
	print("Exercise 3.1")
	print()
	tags_found()
	print()
	print("Exercise 3.2")
	print()
	tags_content()

main()
