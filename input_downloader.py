# Philip Arthur
# Oct 14 2013

import urllib2
import os
import sys

from util import directory as directory
from util import input as input


# Functions
def download(name, url, force):
	try:
		file_path = directory + "/" + name + ".txt"
		if force or not os.path.exists(file_path):
			print "Downloading ", name,
			response = urllib2.urlopen(url)
			 
			#open the file for writing
			fh = open(file_path, "w")
			 
			# read from request while writing to file
			fh.write(response.read())
			fh.close()
			print ""
	except Exception:
		print "\nCannot Download file in url:", url, " system is now exiting..."
		return False

	return True


def download_all_files(force = False):
	print "Preparing input..."
	if not os.path.exists(directory):
		os.makedirs(directory)


	for name, url in input.iteritems():
		if not download(name, url, force):
			break;
	else:
		sys.exit(1)

if __name__ == "__main__":
	download_all_files(True)