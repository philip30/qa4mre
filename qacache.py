import os

def open_cache(dir,command):
	if not os.path.exists("cache"):
		os.makedirs("cache")
	return open("cache/"+dir,command)
