import os
import sys

disagreements = {}

for pdir in os.listdir('data/Hessel/group15'):
	for ddir in os.listdir(f'data/Hessel/group15/{pdir}'):
		annotator1 = f'data/Hessel/group15/{pdir}/{ddir}/en.tok.off.pos'
		annotator2 = f'data/JoeyAnnotations/group15/{pdir}/{ddir}/en.tok.off.pos'
		annotator3 = f'data/LouisAnnotations/group15/{pdir}/{ddir}/en.tok.off.pos'

		annotator1_file = open(annotator1, 'r')
		annotations1 = annotator1_file.readlines()
		annotator1_file.close()

		annotator2_file = open(annotator2, 'r')
		annotations2 = annotator2_file.readlines()
		annotator2_file.close()

		annotator3_file = open(annotator3, 'r')
		annotations3 = annotator3_file.readlines()
		annotator3_file.close()

		disagreements_file = []

		for annotation1 in annotations1:
			if annotation1 not in annotations2:
				disagreements_file.append(annotation1)
			if annotation1 not in annotations3:
				disagreements_file.append(annotation1)

		for annotation2 in annotations2:
			if annotation2 not in annotations1:
				disagreements_file.append(annotation2)
			if annotation2 not in annotations3:
				disagreements_file.append(annotation2)

		for annotation3 in annotations3:
			if annotation3 not in annotations1:
				disagreements_file.append(annotation3)
			if annotation3 not in annotations2:
				disagreements_file.append(annotation3)

		disagreements[f'{pdir}/{ddir}'] = set(disagreements_file)

with open('disagreements.txt', 'w+') as disagree_file:
	for key in disagreements:
		disagree_file.write(str(key) + str(disagreements[key]) + '\n')
