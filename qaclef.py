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

import sys
import argparse
import qacache
import configuration
import input_downloader
import input_parser
import preprocessing
import model_builder
import scoring
import operator
from evaluation import evaluate
from collections import defaultdict
from tmert import execute_mert as mert_training

parser = argparse.ArgumentParser(description="Run QA-CLEF-System")
parser.add_argument('--preprocess',action="store_true")
parser.add_argument('--train',action="store_true")
parser.add_argument('--answeronly',action='store_true')
parser.add_argument('--selftest',action='store_true')
parser.add_argument('--data',nargs = '+',default=[2011],type=int)
parser.add_argument('--test',nargs = '+',default=[2012],type=int)
parser.add_argument('--forcedownload',action='store_true')
parser.add_argument('--ngram', type=int, default=3)
parser.add_argument('--threshold', type=float, default=0.5)
args = parser.parse_args()

def main():	
	process_args(args)

	data = qacache.preprocessed_data(args.data,args.test)
	# parsing and preprocessing
	if args.preprocess or data is None:
		# parsing
		print >> sys.stderr, 'Preprocessing data...'
		input_check(args.data+args.test, args.forcedownload)
		data = input_parse(args.data + args.test)
		data = preprocessing.preprocess(data)
		qacache.store_preprocessed_data(data,args.data,args.test)
	else:
		print >> sys.stderr, 'Preprocessed data is found on cache/preprocessed_data.txt'

	# build-model
	print >> sys.stderr, 'Building model...'
	training_model = model_builder.build_model(data[:len(args.data)])
	test_model = model_builder.build_model(data[-len(args.test):]) if len(args.test) != 0 else []

	# scoring
	print >> sys.stderr, 'Unweighted Scoring...'
	training_model and scoring.score(training_model)
	test_model and scoring.score(test_model)

	# training
	weight = qacache.stored_weight()
	if args.train or weight is None:
		print >> sys.stderr, 'Training...'
		weight = train(training_model)
	else:
		print >> sys.stderr, 'Weight is found on cache/weight.txt'

	# weighted_scoring
	print >> sys.stderr, 'Weighted Scoring...'
	final = scoring.weighted_scoring(args.selftest and training_model or test_model, weight)

	# answer selection
	select_answer(final)

	# evaluation
	result = evaluate(final)

	print "Result: %f" % result

def input_check(data, force):
	for edition in data:
		if not input_downloader.download(configuration.input.keys()[edition-2011],
			configuration.input.values()[edition-2011],force):
			sys.exit(1)

def input_parse(data):
	parsed_data = []
	for edition in data:
		parsed_data.append(input_parser.parse(configuration.input.keys()[edition-2011]))
	return parsed_data

def process_args(args):
	model_builder.n_gram = args.ngram

def train(model):
	questions = defaultdict(lambda: []) # empty list as default value
	features_names = {}

	# build input for tmert
	for _model in model:
		for i in range(0,len(_model)):
			for j in range (0, len(_model[i]['q'])):
				qs = _model[i]['q'][j]['answer']
				for candidate in qs:
					_id = str(i) + str(j)
					feats = candidate['score']
					feature_names = {name: 1 for name in feats.keys()}
					correct = 1 if 'correct' in candidate and candidate['correct'] 1 else 0
					questions[_id].append((int(correct), feats))

	best_weight = mert_training(questions,feature_names)
	qacache.store_weight(best_weight)
	return best_weight

def select_answer(data):
	for model in data:
		for test_set in model:
			for question in test_set['q']:
				
				for i in range(0,len(question['answer'])):
					candidate = question['answer'][i]
					candidate['total_score'] = sum(candidate['weighted_score'].values())
					
				_max = max([y['total_score'] for y in question['answer']])
				for i in range (0, len(question['answer'])):
					if _max == question['answer'][i]['total_score']:
						_index = i
						break
				totals = list(enumerate([candidate['total_score'] for candidate in question['answer']]))
				up_threshold = [abs(_max - score) > args.threshold for (index, score) in totals if index != _index]

				question['output'] = _index if reduce(operator.and_,up_threshold) else None


if __name__ == '__main__':
	main()
	
"""
question = { 
	'answer': [
		{'total_score':1},
		{'total_score':52},
		{'total_score':50},
		{'total_score':48},
		{'total_score':50}
	]
}


for i in range (0, len(question['answer'])):
	if _max == question['answer'][i]['total_score']:
		_index = i
		break

print _max, _index

x = reduce(operator.and_, [(_max - score > 1) for (index, score) in list(enumerate([candidate['total_score'] for candidate in question['answer']])) if index != _index]) and _index or None
print x

"""




