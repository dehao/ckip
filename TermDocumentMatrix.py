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
from scipy import linalg, mat, dot;
import Orange
import numpy as np
import numpy

def square(list):
    ret = []
    for i in list:
        ret.append(i ** 2)
    return ret

def accumu(list):
    total = 0
    sa = []
    for x in list:
        total += x
        sa.append(total)
    return sa




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
		segmented_in_text_result = segmenter.process(unicode('error'))
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



term_dir='/Users/dehao/github/Lydata/issckip/parse/C1/'

tdm = TermDocumentMatrix()
docname = []

for f in listdir(term_dir):
    #print f
    docname.append(f)
    parse = []
    fi=codecs.open(term_dir+f, 'r', encoding='utf-8')
    for line in fi:
        sigram=line.strip().split()
        for gram in sigram:
            parse.append(gram)
        
        #sigram=line.str
        #print sigram
    #print parse
    tdm.add_doc(parse)

print "Docname:"

#print docname


#docnamewrite = csv.writer(open('docname.csv', 'wb'))
#docnamewrite.writerow(docname)


with open('docname.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in docname:
        writer.writerow([val])    

#res = ckip_json['result']
#str1 = [' '.join([str(term) for term in cd]) for cd in res]
#print res
#tdm.add_doc(str1)


				

tdm.write_csv('matrix.csv', cutoff=9)

#MyPrettyPrinter().pprint(countdic)

'''
for key, value in dict.items(countdic):
	print key
'''
#j = 0
flag = []
cutdet = iter(tdm.rows(cutoff=1))
next(cutdet)



for row in cutdet:
    flag.append(row)
    #print row

cutdetlist = iter(tdm.rows(cutoff=1))
next(cutdetlist)
cutdetlist = list(cutdetlist)


flagging = mat(flag);
#print flagging
rows,cols = flagging.shape
#print rows
bet =  int(rows)
#print bet


cutdetarray = np.asarray(cutdetlist)
#print cutdetarray.transpose()

mindflist = []
for i in cutdetarray.transpose():
	countofzero = int(list(i).count(0))
	#print countofzero
	#print bet
	#print bet - countofzero
	noofdf = bet - countofzero
	mindflist.append(noofdf)


mindfarray = np.array(mindflist)
percenttileforcutoff =  np.percentile(mindfarray, 90)

print "Cutoff from percentile:"
print percenttileforcutoff


origin = []
saveterm = []

itercars = iter(tdm.rows(cutoff=percenttileforcutoff))
save = iter(tdm.rows(cutoff=percenttileforcutoff))
next(itercars)

for row in save:
    saveterm.append(row)

for row in itercars:
    origin.append(row)

#print origin
#matrix = mat( [[1,1,1,3,2], [3,3,3,4,5], [4,4,4,1,1], [5,5,5,3,2], [0,2,0,4,4]] );
matrix = mat(origin);
print "Original matrix:"
print matrix
U, s, V = linalg.svd( matrix, full_matrices=True  )
print "U:"
print U
print "sigma:"
print s
print "VT:"
print V
print U.shape, s.shape, V.shape
#dimensions = 2
rows,cols = matrix.shape
#original term matrix
conterm = csv.writer(open('originalterm.csv', 'wb'))
conterm.writerow(saveterm[0])
conterm.writerow(s)
beat = square(s)
#print beat
cumubeat = accumu(beat)
#print cumubeat
print "Total Energy:"
sumbeat = sum(beat)
print sumbeat
beathold = sumbeat * 0.9
print "Energy thold:"
print beathold
for index, x in enumerate(cumubeat):
	if x > beathold:
		tholdindex = index
		tholdcontent = cumubeat[index-1]
		break
print "Energy thold index:"
print tholdindex
print "Energy thold content:"
print tholdcontent
print "Energy percentage:"
print tholdcontent / sumbeat
dimensions = tholdindex
print "size of cols:"
print cols
maxofcolandrow = min(cols,rows)
print maxofcolandrow


#sandv = np.dot(linalg.diagsvd(s,len(matrix),len(V)), V)

#Dimension reduction, build SIGMA'
for index in xrange(dimensions, maxofcolandrow):
	s[index]=0
print "reduced sigma:"
print s

#Reconstruct MATRIX'
#print len(matrix)
#print len(V)
#print linalg.diagsvd(s,len(matrix),len(V)).shape
#print linalg.diagsvd(sigma,len(matrix),len(V))
#sandv = dot(linalg.diagsvd(s,len(matrix),len(V)), V)
#print "sigmaandV"

#print sandv
#print sandv.shape


reconstructedMatrix= dot(dot(U,linalg.diagsvd(s,len(matrix),len(V))),V)
#Print transform
print "reconstructed:"
print reconstructedMatrix

countterm = []


for i in range(0, cols):
	countterm.append(i)


#print countterm


#print out reconstructed term
conterm = csv.writer(open('sigmaterm.csv', 'wb'))
conterm.writerow(saveterm[0])
conterm.writerow(s)
conterm.writerow(countterm)
print "reducedofu"
reducedumatrix = np.delete(U, np.s_[tholdindex:], 1)
print reducedumatrix


print reducedumatrix.shape
with open('C1reducedu.csv', 'wb') as f:
	a = numpy.asarray(reducedumatrix)
	numpy.savetxt(f, a, delimiter=",")




with open('reconstructedterm.csv', 'wb') as f:
	a = numpy.asarray(reconstructedMatrix)
	numpy.savetxt(f, a, delimiter=",")


U, s, V = np.linalg.svd(matrix, full_matrices=False)

print U.shape, s.shape, V.shape

sandv = np.dot(np.diag(s), V)
print "sigmaandV"

print sandv

with open('sigmaandV.csv', 'wb') as f:
	a = numpy.asarray(sandv)
	numpy.savetxt(f, a, delimiter=",")

