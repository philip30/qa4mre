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

import os
import sys
import simplejson as json

def open_cache(dir,command):
	if not os.path.exists("cache"):
		os.makedirs("cache")
	return open("cache/"+dir,command)

def stored_weight():
	try:
		return open_json('weight.txt')
	except Exception:
		print >> sys.stderr, 'Could not load weight, executing re-training.'
	return None

def store_weight(data):
	write_json(data,'weight.txt')

def store_preprocessed_data(data):
	write_json(data,'preprocessed_data.txt')

def preprocessed_data():
	try:
		return open_json('preprocessed_data.txt')
	except Exception:
		print >> sys.stderr, 'No preprocessed data is found, executing preprocessing.'
	return None
	
def open_json(name):
	if os.path.exists('cache/' + name):
		with open_cache(name,'r') as f:
			return json.load(f)
	else:
		return None

def write_json(data, name):
	with open_cache(name, 'w') as f:
		f.write(json.dumps(data))
