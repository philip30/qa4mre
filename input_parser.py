# Philip Arthur
# Oct 14 2013

import nltk
import re
import xml.etree.ElementTree as etree
from util import directory as directory
from util import input as inp
from util import build_name_txt as build_name

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def sentence_splitter(d):
	d = re.sub(r"\n",". ",d)
	d = re.sub("\.{2,}",". ",d)
	d = re.sub("^.","", d)
	d = re.sub("--", " ",d)
	d = re.sub(" {2,}"," ",d)
	d = re.sub("/", " ",d)
	return tokenizer.tokenize(d)

def parse(filename):
	tree = etree.parse(filename)
	root = tree.getroot()

	tests = []
	for test in root.iter('reading-test'):
		doc = sentence_splitter(test.find('doc').text.encode('utf8'))
		
		_questions = []
		for q_index in range (1,len(test)):
			question = test[q_index]
			q_str = question.find('q_str').text.encode('utf8')

			choices = []
			for c_index in range (1, len(question)):
				choice = question[c_index]
				_choice = {}
				_choice["value"] = choice.text.encode('utf8')
				if 'correct' in choice.attrib and choice.attrib['correct'].lower() == 'yes':
					_choice["correct"] = True
				choices.append(_choice)
			_questions.append({"q_str" : q_str, "answer" : choices})
		tests.append({'doc':doc, 'q': _questions})
	return tests

def get_example():
	return parse(build_name(directory, "CLEF_2011_GS"))

if __name__ == "__main__":
	print(get_example()[0])

