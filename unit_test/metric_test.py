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

# Include upper directory
import sys
import math
import unittest
sys.path.insert(0, '..')

# Other imports
from metric import *

v1 = {
	'philip' : 1,
	'arthur' : 2,
	'is':1,
	'a':3,
	'student':5
}
v2 = {
	'student':2,
	'philip':1,
	'a':2,
	'research':1
}

class FundamentalTest(unittest.TestCase):

	# Dot Product and len
	def testOne(self):
		self.failUnless(dot_product(v1,v2) == (1*1 + 5*2 + 3*2))
		self.failUnless(norm_2(v1) == math.sqrt(1*1 + 2*2 + 1*1 + 3*3 + 5*5))
		self.failUnless(norm_2(v2) == math.sqrt(2*2 + 1*1 + 2*2 + 1*1))

	# Cosine Similarity
	def testTwo(self):
		print sim(v1,v2)
		self.assertEquals(sim(v1,v2),float(dot_product(v1,v2)) / (norm_2(v1) * norm_2(v2)))

	# Merge
	def testThree(self):
		v1_v2 = {
			'philip' : 2,
			'arthur' : 2,
			'is':1,
			'a':5,
			'student':7,
			'research':1
		}
		self.assertEquals(merge(v1,v2), v1_v2)
		

if __name__ == '__main__':
	unittest.main()