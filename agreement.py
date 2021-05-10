from sklearn.metrics import cohen_kappa_score
import os
import sys
import nltk
	
def get_tags(path):
	file = f'{path}/en.tok.off.pos'
	with open(file, 'r') as infile:
		lines = infile.readlines()
		tags_content = []
		for line in lines:
			line = line.rstrip().split()
			if len(line) > 5:
				if line[5] in 'COU CIT NAT PER ORG ANI SPO ENT':
					tags_content.append(line[5])
				else:
					tags_content.append('none')
			else:
				tags_content.append('none')
	return tags_content
			

def main():
	annotator1 = []
	root_path = sys.argv[1] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator1.extend(get_tags(path))
			
	annotator2 = []
	root_path = sys.argv[2] + '/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			annotator2.extend(get_tags(path))
	
	
	cm = nltk.ConfusionMatrix(annotator1, annotator2)
		
	print("Cohen's kappa score: " + str(cohen_kappa_score(annotator1, annotator2)))
	print()
	print(cm)
	
main()
