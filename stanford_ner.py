#!/usr/bin/python

# (C) Copyright 2013 Philip Arthur, NAIST
# 
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Lesser General Public License
# (LGPL) version 2.1 which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/lgpl-2.1.html
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

from configuration import STANFORD_NER_TAGSET_PATH as tagset_path
from configuration import STANFORD_NER_JAR_PATH as jar_path
from configuration import STANFORD_NER_JVM_MEMORY as memory
from util import count_leaves as count_line
from util import traverse_test_set as traverse
from util import traverse_test_set_with_assignment as traverse_assignment
from util import traverse_test_set_root as traverse_root 

import os
import subprocess
import signal
import qacache
import util
import input_parser

#static initialization
merged_name = "1-merged.txt"
ne_tagged_name = "2-netagged.txt"
command = 'java ' + memory + ' -cp '+ jar_path +' edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ' + tagset_path + ' --textFile cache/' + merged_name + ' > cache/' + ne_tagged_name
	

class StanfordNER():
	def __init__(self, document_list):
		f = self.prepare_to_write()
		for test_set_list in document_list:
			for test_set in test_set_list:
				self.write_test_set(f,test_set)
		f.close()	
		self.run_stanford_tagger()
		document_list = self.read_tagged(qacache.open_cache(ne_tagged_name,'r'),document_list)

	def read_ner(self,f):
		value = []
		tokens = self.read_until_not_period(f).strip().split(' ')
		_tag, _word, i = '','',0
		while i < len(tokens):
			word = tokens[i].split('/')
			if word[1] != 'O':
				if _tag != '' and _tag != word[1]:
						value.append((_word, _tag))
						_word, _tag = '', ''
				_word += word[0]
				_tag = word[1]
			else:
				if _tag != '':
					value.append((_word,_tag))
					_word,_tag = '', ''
				value.append((word[0],word[1]))
			i += 1
		return value



	def read_until_not_period(self,f):
		while True:
			line = f.readline()
			if line.split('/')[0] != '.':
				return line
		return ''

	def read_tagged(self,f,document_list):
		for document in document_list:
			traverse_root(lambda x: self.read_ner(f),document,assignment=True)

	def run_stanford_tagger(self):
		os.system(command)

	def prepare_to_write(self):
		return qacache.open_cache(merged_name,'w')

	def write_test_set(self,f,test_set):
		traverse_assignment(lambda x: not any(c in x.strip() for c in ['.','!','?']) and x + '.' or x,test_set)
		traverse(lambda x: util.write_line(f,str(x)),test_set)


if __name__ == '__main__':
	inp = input_parser.get_example()
	StanfordNER([[inp[0]]])
