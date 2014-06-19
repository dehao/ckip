from scipy import linalg, mat, dot;


matrix = mat( [[2,1,0,0], [4,3,0,0]] );
print "Original matrix:"
print matrix
U, s, V = linalg.svd( matrix )
print "U:"
print U
print "sigma:"
print s
print "VT:"
print V
dimensions = 1
rows,cols = matrix.shape
#Dimension reduction, build SIGMA'
for index in xrange(dimensions, rows):
 s[index]=0
print "reduced sigma:"
print s
#Reconstruct MATRIX'
reconstructedMatrix= dot(dot(U,linalg.diagsvd(s,len(matrix),len(V))),V)
#Print transform
print "reconstructed:"
print reconstructedMatrix