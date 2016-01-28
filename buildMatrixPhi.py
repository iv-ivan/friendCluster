import urllib2
import json
import codecs
import sklearn

def main():
	with codecs.open("wallsDB.txt","r",encoding='utf-8') as f:
		walls = f.read().split("\t\n\t")
		print len(walls)
		
if __name__ == "__main__":
	main()
