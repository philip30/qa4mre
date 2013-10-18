#!/bin/python
import nltk
import util
import re
import simplejson as json
import qacache as cache
from stanford_ner import StanfordNER
from input_parser import parse
from util import traverse_all_test_sets as traverse_all
from stop_word_list import stop_word_list as stop_word_list

def preprocess(testdoc,tag_ner=True):
	if tag_ner:
		StanfordNER(testdoc)

	# lowercasing
	traverse_all(lambda x : (x[0].lower(),x[1]),testdoc,assignment=True)

	# token-altering
	traverse_all(lambda x : (token_altering(x[0]),x[1]),testdoc,assignment=True)

	# only alpha numeric is allowed
	traverse_all(lambda x : (filter(lambda c: c.isalpha(), x[0]),x[1]), testdoc,assignment=True)

	# stop word deletion
	traverse_all(lambda x: x[0] in stop_word_list and ("",x[1]) or x,testdoc, assignment=True)

	# purging
	traverse_all(lambda x: filter(lambda y: len(y[0])!=0, x) ,testdoc, assignment=True,list_method=True)

	write_result(testdoc, '3-stop-word-and-cleaning')
	# co-Reference Resolution

	# stemming


######### IO #####################################
def write_result(testdoc, name):
	f = cache.open_cache(name,'w')
	f.write(json.dumps(testdoc, sort_keys=True, indent=4 * ' '))
	f.close()

######### TOKEN ALTERING #########################
token_map = {
	"n't" : "not",
	"'s" : "is",
	"'re" : "are",
	"'d" : "would",
	"'ve" : "have"
}

def token_altering(token):
	if token in token_map:
		return token_map[token]
	else:
		return token

##################################################
######## UNIT TEST ###############################
##################################################
if __name__ == "__main__":
	data = [parse(util.build_name_txt(util.directory, "CLEF_2011_GS")), parse(util.build_name_txt(util.directory, "CLEF_2012_GS"))]
	preprocess(data)

	#k = sentence_splitter(data[0]["doc"])

	#k = map(nltk.word_tokenize, k)
	#k = map(nltk.pos_tag, k)
	

	#k = map(st.tag,k)
	#print st.tag('Rami Eid is studying at Stony Brook University in NY'.split()) 



	#k = map(nltk.chunk.named_entity.NEChunkParser.parse,k)
	#for i in k:
	#	print i