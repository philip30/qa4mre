# Philip Arthur
# Oct 14 2013

# Data
directory = "input"
input = {
	'CLEF_2011_GS':'http://celct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2011/Training_Data/Goldstandard/QA4MRE-2011-EN_GS.xml',
	'CLEF_2012_GS': 'http://celct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2012/Main_Task/Training_Data/Goldstandard/Parallel_Aligned/QA4MRE-2012-EN_GS_SYNC.xml',
	'CLEF_2013_GS': 'http://celct.fbk.eu/QA4MRE/scripts/downloadFile.php?file=/websites/ResPubliQA/resources/past_campaigns/2013/Main_Task/Training_Data/Goldstandard/QA4MRE-2013-EN_GS.xml'
}


#function
def build_name_txt(directory, url):
	return directory + "/" + url + ".txt"
