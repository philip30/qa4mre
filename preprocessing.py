#!/bin/python
import nltk
import util
import re
from input_parser import parse
from nltk.tag.stanford import NERTagger


st = NERTagger(tagset_path, jar_path) 
st.tag('Rami Eid is studying at Stony Brook University in NY'.split()) 

def preprocess(testdoc):
	pass

# for testingf
if __name__ == "__main__":
	data = parse(util.build_name_txt(util.directory, "CLEF_2011_GS"))
	k = sentence_splitter(data[0]["doc"])

	k = map(nltk.word_tokenize, k)
	#k = map(nltk.pos_tag, k)
	
	for s in k:
		j = st.tag(s)
		print j

	#k = map(st.tag,k)
	#print st.tag('Rami Eid is studying at Stony Brook University in NY'.split()) 



	#k = map(nltk.chunk.named_entity.NEChunkParser.parse,k)
	#for i in k:
	#	print i