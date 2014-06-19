# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
import os, codecs, random
from math import sqrt
#Kmeans聚类，sparse matrix 实现
#保存row的模
row_norms={}
def readfile(dirname):
    rows={} 
    for f in os.listdir(dirname):
    	print f
        fr=codecs.open(dirname+f, 'r', encoding='utf-8') 
        #mod=0
        tw_dict={}
        norm=0
        for line in fr:
        	#print line
        	items=line.split('\t')
        	#print items
        	token=items[0].strip()
        	#print token
        	#一个中文字符，舍弃
        	if len(token)<2:
        		continue 
        	w=float(items[1].strip())
        	#print w
        	norm+=w**2
        	#print norm
        	tw_dict[token]=w
        	#print tw_dict
#取出文档编号
        rows[str(f[:-4])]=tw_dict
        row_norms[str(f[:-4])]=sqrt(float(norm))
    print len(rows)
    return rows
        #vector_norm[f]=math.sqrt(norm)
#向量模
def norm(vec):
    return sqrt(sum([pow(v,2) for k, v in vec.items()]))
#v1: row, norm_v1: row的norm; v2:聚类中心点， norm_v2:中心点的norm
def cosine(v1, norm_v1, v2, norm_v2):
    # 交集w乘积
    if norm_v1==0 or norm_v2==0:
        return 1.0
    dividend=0
    #sum1Sq=0
    for k, v in v1.items():
        if k in v2:
            dividend+=v*v2[k]
        #sum1Sq+=pow(v, 2)

    # Sums of the squares
    #sum2Sq=sum([pow(v,2) for k, v in v2.items()])    
    #if sum1Sq==0 or sum2Sq==0:
        #return 1.0
    #else:
    return 1.0-dividend/(norm_v1*norm_v2)

#计算数据各个维度的限制
def rows_range(rows):
    tokens={}
    for k, tw in rows.items():
        for t, w in tw.items():
            if t not in tokens:
                tokens[t]=[]
            tokens[t].append(w)
    res={}
    for t, wl in tokens.items():
        res[t]=(min(wl), max(wl))
    return res

#生成随机初始点
def random_vec(ranges):
    res={}
    for k, v in ranges.items():
        res[k]=random.random()*(v[1]-v[0])+v[0]
    return res

#计算类中心
def center(clust, rows):
    res={}
    s=len(clust)
    for c in clust:
        for k, v in rows[c].items():
            if not k in res:
                res[k]=0.0
            res[k]+=v
    for k, v in res.items():
        res[k]=v/s
    return res

def kcluster(rows,distance=cosine,k=4):
    # Determine the minimum and maximum values for each point
    ranges=rows_range(rows)
    # Create k randomly placed centroids
    clusters=[]
    for i in range(k):
        clusters.append(random_vec(ranges))

    clusteres_norm=[]
    for i in range(k):
        clusteres_norm.append(norm(clusters[i]))
    lastmatches=None
    for t in range(20):
        print 'Iteration %d' % t
        bestmatches=[[] for i in range(k)]

        # Find which centroid is the closest for each row
        for j in rows.keys():
            print 'iter row:', j
            row=rows[j]
            row_norm=row_norms[j]
            bestmatch=0
            min_dis=9999999
            for i in range(k):
                d=distance(row, row_norm, clusters[i],clusteres_norm[i])
                if d<min_dis:
                    bestmatch=i
                    min_dis=d
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches==lastmatches: 
            break
        lastmatches=bestmatches

        # Move the centroids to the average of their members

        for i in range(k):
            clusters[i]=center(bestmatches[i], rows)

    return bestmatches

if __name__ == '__main__':
    corpus_dir='/Users/dehao/github/Lydata/ckip/corpus_res/'
    rows=readfile(corpus_dir)
    print 'create vectorspace'
    n=150
    clust=kcluster(rows,k=n)
    fw=open('/Users/dehao/github/Lydata/ckip/kmean/kmeans_'+str(n)+'.txt', 'w')
    for c in clust:
        fw.write('%s\n' % ','.join([str(v) for v in c]))