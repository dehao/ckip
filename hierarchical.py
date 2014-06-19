import Orange

iris = Orange.data.Table("reconstructedterm.csv")

matrix = Orange.misc.SymMatrix(len(iris))
matrix = Orange.distance.distance_matrix(iris, Orange.distance.Euclidean)

clustering = Orange.clustering.hierarchical.HierarchicalClustering()
clustering.linkage = Orange.clustering.hierarchical.WARD
root = clustering(matrix)

root.mapping.objects = iris

topmost = sorted(Orange.clustering.hierarchical.top_clusters(root, 20), key=len)

print topmost

for n, cluster in enumerate(topmost):
    print "\n\n Cluster %i \n" % n
    #for instance in cluster:
        #print instance