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

def open_cache(dir,command):
	if not os.path.exists("cache"):
		os.makedirs("cache")
	return open("cache/"+dir,command)
