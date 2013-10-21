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

import math

# NOTE: All of the metrics are the implementations of the following paper:
#	    http://www.phontron.com/paper/arthur13clef.pdf

threshold = 0.1 # l

###
# -- IDF 
#                                     |D|
# idf(t,D) =  log (---------------------------------------------)
#                  1 + (number of sentence where term t occurs)
# log is in base 10
def idf(self,D,v):
	return log(float(D) / (1 + v), 10)

# cosine similarity
# q and dj is already in tf-idf form
def sim(self,q,dj):
	return dot_product(q,dj) / (norm_2(q) * norm_2(dj))

# v1 and v2 are dictionary of occurences
def dot_product(self,v1,v2):
	return sum ([value * v2[word] for (word,value) in v1.items() if word in v2])

def norm_2(self,v):
	return math.sqrt(sum([x**2 for x in v]))


class FeaturesScoring:

	def __init__(self,D,q):
		self.D1 = set(self.find_match(D,q))
		self.r = self.find_r(D,q)

	def greatest_cosine(self,p,D):
		return max([sim(p,dj) for dj in D])

	def greatest_matching(self,q,ak,D):
		p = set(q.keys() + ak.keys()) # p is set of distinct keywords between question and candidate
		return max([len([x for x in dj.keys() if x in p]) for dj in D])
		
	def cosine_matching(self,ak,D):
		D2 = set(self.find_match(D,ak))
		return len ([d for d in self.D1 if d in D2])

	def closest_sentence(self,q,ak,D):
		D2 = set(self.find_match(D,ak))
		if len(D1) == 0 or len (D2) == 0:
			return None
		else:
			return min([math.abs(x-y) for x in D1 for y in D2])

	def closest_matching(self,q,ak,D):
		if len(self.r) == 0:
			return None
		else:
			D2 = find_match(D, ak)
			if len(D2) != 0
				return min([math.abs(x-y) for x in self.r for y in D2])
			else:
				return None

	def find_match(self,doc, d):
		match = []
		i=0
		for sentence in doc:
			if sim(sentence, d) > threshold:
				match.append(i)
			i+=i
		return match

	def find_r(self,doc,q):
		r = set([])
		sentence_similarity = [sim(d,q) for d in doc if sim(d,q) > threshold]
		max_similarity = max(sentence_similarity)
		i = 0 
		for similarity in sentence_similarity:
			if similarity == max_similarity:
				r.append(i)
			i+=1
		return r
