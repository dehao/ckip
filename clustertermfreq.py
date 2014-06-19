# -*- coding: utf-8 -*-
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from ckip import CKIPSegmenter
from pprint import pprint
countdic = dict()
import pprint
import textmining
import re
#import stemmer
import csv
import os
import unicodedata
import textwrap
from os import listdir
import codecs
from collections import Counter


ckip_dir='/Users/dehao/github/Lydata/ckip/select/'
allterm = []


for f in listdir(ckip_dir):
	fi=codecs.open(ckip_dir+f, 'r', encoding='utf-8')
	for line in fi:
		line = re.sub("\n","", line)
		dash = line.split(" ")
		#print dash 
		for key in dash:
			print key
			allterm.append(key)

		#str1 = [' '.join([str(term) for term in cd]) for cd in line]
			




		'''
		for sentence in ckip_json['result']:
			segfile.write("\n")
			for term in sentence:
				#print term['term'], term['pos']
				if term['pos']=='Vi':
					if len(term['term']) > 1:
						niceterm = term['term']
						print i,niceterm
						parse.append(niceterm)
						segfile.write("%s " % niceterm)
						'''


#print allterm
with open('set.txt', 'wb') as f:
            for word, count in Counter(allterm).most_common(10000000):
                f.write(u'{} {}\n'.format(word, count).encode('utf8'))

counts = Counter(allterm)

print counts