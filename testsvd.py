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

matrix = mat( [[1,1,1,3,2], [3,3,3,4,5], [4,4,4,1,1], [5,5,5,3,2]] );
#matrix = mat(origin);
print "Original matrix:"
print matrix
U, s, V = linalg.svd( matrix, full_matrices=False )
print "U:"
print U
print "sigma:"
print s
print "VT:"
print V
rows,cols = matrix.shape
print U.shape, s.shape, V.shape

print np.delete(U, np.s_[3:], 1)

reconstructedMatrix= dot(dot(U,linalg.diagsvd(s,len(matrix),len(V))),V)