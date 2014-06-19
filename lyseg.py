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




class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

def CkipReturn(in_text): #in_text is string
	segmenter = CKIPSegmenter('changchengtu', 'asd')
	try:
		segmented_in_text_result = segmenter.process(unicode(in_text))
	except:
		segmented_in_text_result = segmenter.process(unicode('got an error'))
	return segmented_in_text_result

def simple_tokenize(document):
    """
    Clean up a document and split into a list of words.

    Converts document (a string) to lowercase and strips out everything which
    is not a lowercase letter.

    """
    #document = document.lower()
    #document = re.sub('[^\u4e00-\u9fa5]', '', document)
    #return document.strip().split()
    return document


class TermDocumentMatrix(object):

    """
    Class to efficiently create a term-document matrix.

    The only initialization parameter is a tokenizer function, which should
    take in a single string representing a document and return a list of
    strings representing the tokens in the document. If the tokenizer
    parameter is omitted it defaults to using textmining.simple_tokenize

    Use the add_doc method to add a document (document is a string). Use the
    write_csv method to output the current term-document matrix to a csv
    file. You can use the rows method to return the rows of the matrix if
    you wish to access the individual elements without writing directly to a
    file.

    """

    def __init__(self, tokenizer=simple_tokenize):
        """Initialize with tokenizer to split documents into words."""
        # Set tokenizer to use for tokenizing new documents
        self.tokenize = tokenizer
        # The term document matrix is a sparse matrix represented as a
        # list of dictionaries. Each dictionary contains the word
        # counts for a document.
        self.sparse = []
        # Keep track of the number of documents containing the word.
        self.doc_count = {}

    def add_doc(self, document):
        """Add document to the term-document matrix."""
        # Split document up into list of strings
        #words = self.tokenize(document)
        words = document
        # Count word frequencies in this document
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        # Add word counts as new row to sparse matrix
        self.sparse.append(word_counts)
        # Add to total document count for each word
        for word in word_counts:
            self.doc_count[word] = self.doc_count.get(word, 0) + 1

    def rows(self, cutoff=2):
        """Helper function that returns rows of term-document matrix."""
        # Get master list of words that meet or exceed the cutoff frequency
        words = [word for word in self.doc_count \
          if self.doc_count[word] >= cutoff]
        # Return header
        yield words
        # Loop over rows
        for row in self.sparse:
            # Get word counts for all words in master list. If a word does
            # not appear in this document it gets a count of 0.
            data = [row.get(word, 0) for word in words]
            yield data

    def write_csv(self, filename, cutoff=2):
        """
        Write term-document matrix to a CSV file.

        filename is the name of the output file (e.g. 'mymatrix.csv').
        cutoff is an integer that specifies only words which appear in
        'cutoff' or more documents should be written out as columns in
        the matrix.

        """
        f = csv.writer(open(filename, 'wb'))
        for row in self.rows(cutoff=cutoff):
            f.writerow(row)



ckip_dir='/Users/dehao/github/Lydata/ckip/ckip/'

ed_dir='/Users/dehao/github/Lydata/ckip/ckip_ed/'

#file = open('testfile.txt', 'r')


'contentinline = file.readline()'

'print contentinline'
parse = []
i = 0
j = 1
tdm = TermDocumentMatrix()


#segfile = open("segmentfile.txt", "w")

for f in listdir(ckip_dir):
	fi=codecs.open(ckip_dir+f, 'r', encoding='utf-8')
	print f
	d = str(j)
	segfile=open(ed_dir+f, 'w')
	j +=1
	for line in fi:
		i +=1
		#print len(line)
		line = re.sub("[,]"," ", line)
		print line
		ckip_json = CkipReturn(line)

		res = ckip_json['result']
		str1 = [' '.join([str(term) for term in cd]) for cd in res]
		#print res
		tdm.add_doc(str1)

		for sentence in ckip_json['result']:
			segfile.write("\n")
			for term in sentence:
				if term['pos']=='N' or term['pos'] == 'Vi' or term['pos'] == 'Vt':
					if len(term['term']) > 1:
						niceterm = term['term']
						print i,niceterm
						parse.append(niceterm)
						segfile.write("%s " % niceterm)


				#str1 = ''.join(str(parse))
				#print 
				#str1.encode('utf8')
				#print i,parse
				#segfile.write("%s " % parse)
				#tdm.add_doc(parse)
				#parse = []






				#print sentence
				#tdm.add_doc(sentence['term'])
				#for term in sentence:
					#print term['term'], term['pos']
					#print i
					#tdm.add_doc(term['term'])
				#	if term['pos']=='N' or term['pos'] == 'Vi' or term['pos'] == 'Vt':
				#		if len(term['term']) > 1:
				#			entry = term['term']
								#reg = ''.join(str(entry))
								#reg.encode(encoding='UTF-8',errors='strict')
								#print entry
								#print i
								#print reg
								#print i,key
								#print type(key)
								#tdm.add_doc(key)
				#			if entry in countdic:
				#				countdic[entry] += 1
				#			else:
				#				countdic[entry] = 1
				

#tdm.write_csv('matrix.csv', cutoff=2)

#MyPrettyPrinter().pprint(countdic)

'''
for key, value in dict.items(countdic):
	print key
'''
#j = 0
#for row in tdm.rows(cutoff=2):

#	j +=1
	#print j,row