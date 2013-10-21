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
import configuration
import input_downloader
import input_parser
import preprocessing
import model_builder
import scoring

parser = argparse.ArgumentParser(description="Run QA-CLEF-System")
parser.add_argument('--preprocess',action="store_true")
parser.add_argument('--train',action="store_true")
parser.add_argument('--data',nargs = '+',default=[2011,2012],type=int)
parser.add_argument('--test',nargs = '+',default=[2013],type=int)
parser.add_argument('--forcedownload',action='store_true')
parser.add_argument('--selftest',action="store_true")
parser.add_argument('--n_gram', type=int, default=3)
args = parser.parse_args()

def main():
	input_check(args.data+args.test, args.forcedownload)
	process_args(args)

	# parsing
	data = input_parse(args.data + args.test)
	
	# preprocessing
	data = preprocessing.preprocess(data)

	# build-mode
	training_model = model_builder.build_model(data[:len(args.data)])
	test_model = model_builder.build_model(data[-len(args.test):])

	# scoring
	scoring.score(training_model)
	scoring.score(test_model)

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
	model_builder.n_gram = args.n_gram

if __name__ == '__main__':
	main()
