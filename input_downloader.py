# Philip Arthur
# Oct 14 2013

import urllib2
import os
import sys


# Data
directory = "input"
input = {
	'CLEF_2011_GS':'http://c1elct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2011/Training_Data/Goldstandard/QA4MRE-2011-ES_GS.xml',
	'CLEF_2012_GS': 'http://celct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2012/Main_Task/Training_Data/Goldstandard/Parallel_Aligned/QA4MRE-2012-EN_GS_SYNC.xml',
	'CLEF_2013_GS': 'http://celct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2013/Main_Task/Training_Data/Goldstandard/QA4MRE-2013-EN_GS.xml'
}


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

download_all_files(True)