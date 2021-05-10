import nltk
import os


def get_text(path):
	file = f'{path}/en.tok.off'
	with open(file, 'r') as infile:
		lines = infile.readlines()
		text = []
		for line in lines:
			line = line.rstrip().split()
			text.append(line[3])

		return text


def pos_text(tokens):
	pos_tagged = nltk.pos_tag(tokens)
	return pos_tagged


def add_tags(tagged_words, path):
	file = f'{path}/en.tok.off'
	new_file = f'{path}/en.tok.off.pos'
	new_lines = []
	with open(file, 'r') as infile:
		lines = infile.readlines()
		pos = 0
		for line in lines:
			line = line.rstrip()
			line = f'{line} {tagged_words[pos][1]}\n'
			pos += 1
			new_lines.append(line)

	with open(new_file, 'w') as infile:
		for line in new_lines:
			infile.write(line)


def main():
	root_path = 'data/Louis Annotations/group15'
	for dir in os.listdir(root_path):
		for pdir in os.listdir(f'{root_path}/{dir}'):
			path = f'{root_path}/{dir}/{pdir}'
			text = get_text(path)
			tagged_text = pos_text(text)
			add_tags(tagged_text, path)


if __name__ == '__main__':
	main()
