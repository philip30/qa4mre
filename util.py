# Philip Arthur
# Oct 14 2013
#from __future__ import print_function
import unittest

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

def count_leaves(node):
	i = 0;
	if isinstance(node,list) or isinstance(node,tuple):
		for item in node:
			i += count_leaves(item)
	elif isinstance(node,dict):
		for item in node.itervalues():
			i += count_leaves(item)
	elif isinstance(node,str):
		i = 1
	return i;

def print_leaves(node,f=None):
	if isinstance(node,list) or isinstance(node,tuple):
		for item in node:
			print_leaves(item,f)
	elif isinstance(node,dict):
		for item in node.itervalues():
			print_leaves(item,f)
	else:
		if f != None:
			try:
				write_line(f,node)
			except Exception:
				print nod
		else:
			print node

def write_line(f,string):
	f.write(str(string)+'\n')

def traverse_test_set(action,test,list_method=False):
	for sentence in test['doc']:
		apply_action(action,sentence,list_method)
	for question in test['q']:
		apply_action(action,question['q_str'],list_method)
		for choice in question['answer']:
			apply_action(action,choice['value'],list_method)

def apply_action(action, item, list_method):
	if not list_method and isinstance(item,list):
		for i in range(0,len(item)):
			item[i] = action(item[i])
		return item
	else:
		return action(item)

def traverse_test_set_with_assignment(action,test,list_method = False):
	for i in range (0,len(test['doc'])):
		test['doc'][i] = apply_action(action,test['doc'][i],list_method)
	for question in test['q']:
		question['q_str'] = apply_action(action,question['q_str'],list_method)
		for choice in question['answer']:
			choice['value'] = apply_action(action,choice['value'],list_method)

def traverse_test_set_root(action,test_set,assignment=False,list_method = False):
	for test in test_set:
		if not assignment:
			traverse_test_set(action,test,list_method)
		else:
			traverse_test_set_with_assignment(action,test,list_method)

def traverse_all_test_sets(action,test_sets,assignment=False,list_method = False):
	for test_set in test_sets:
		traverse_test_set_root(action,test_set,assignment,list_method)

# Unit test
class TestCase(unittest.TestCase):
	def test_count_leaves(self):
		self.assertEquals((count_leaves({1:[1,2,3,4,[3,4,5,6]],2:[3,4,5]})),11)

	def test_build_name_txt(self):
		self.assertEquals(build_name_txt('dir','file'),'dir/file.txt')

def _print(x):
	print x

if __name__ == "__main__":
	print print_leaves( {
      'answer': [
        {
          'value': 'the imprisonment of Nelson Mandela at Robben Island'
        },
        {
          'value': "the closing ceremony of Nelson Mandela's Foundation"
        },
        {
          'value': "the meeting with Youssou N'Dour"
        },
        {
          'value': 'the racial segregation in South Africa'
        },
        {
          'correct': True,
          'value': "Nelson Mandela's conference to the world press"
        }
      ],
      'q_str': 'What event caused Annie Lennox to commit herself to the fight against AIDS?'
    })
	unittest.main()

