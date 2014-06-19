# -*- coding: utf-8 -*-
import sys,os

import numpy, math
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance
import nltk.corpus
from nltk import decorators
import nltk.stem
import codecs

#从corpus_res2中读取，先生成set;每个文件进行2阶normalization;结合numpy和nltk.cluster来做
#输入是文件夹：每个文件是一个topic, 文件内容是降序排好的特征词：tf*idf值，如：
#演讲	0.375399
#励志	0.337192
#马云	0.242213
def get_words(corpus_dir):
    words=set() 
    for f in os.listdir(corpus_dir):
        #只保留30个，单机内存不足
        fr=codecs.open(corpus_dir+f, 'r', encoding='utf-8')
        cnt=0
        for line in fr:
            if cnt>=20:
                break 
            word=line.split('\t')[0].strip()
            #如果特征词是一个中文字符，直接舍弃
            if len(word)<2:
                continue 
            #是否去掉停用词？
            words.add(word)
            cnt+=1
    print 'total words:', len(words)
    return list(words)

#求topic的特征词向量
def vectorspaced(title):
    #求出模长
    mod=0
    tw_dict={}
    cnt=0
    for line in title.readlines():
        if cnt>=20:
            break
        items=line.split('\t')
        token=items[0].strip()
        #一个中文字符，舍弃
        if len(token)<2:
            continue
        w=float(items[1].strip())
        tw_dict[token]=w
        mod=mod+w**2
        cnt+=1
    
    mod=math.sqrt(mod)
    w_vec=[]
    for word in words:
        if not word in tw_dict:
            w_vec.append(0)
        else:
            w_vec.append(tw_dict[word]/mod)

    return numpy.array(w_vec, numpy.float)


if __name__ == '__main__':
    corpus_dir='/Users/dehao/github/Lydata/ckip/corpus_res/'
    #corpus_dir='D:/python_workspace/corpus_test/'
    words=get_words(corpus_dir)
    vec_space=[]
    indf_dict={}
    index=0
    #写对应关系
    fw1=open('/Users/dehao/github/Lydata/ckip/index_file.txt', 'w')
    #写结果
    fw2=open('/Users/dehao/github/Lydata/ckip/cluser_res.txt', 'w')
    for f in os.listdir(corpus_dir):
        index+=1
        print 'already handle file:', index
        indf_dict[index]=f
        with codecs.open(corpus_dir+f, 'r', encoding='utf-8') as title:
            vec_space.append(vectorspaced(title))
    
    #如何根据hisgram判断分类数目？
    cluster = GAAClusterer(40)
    clustered=cluster.cluster(vec_space, True)
        #cluster.dendrogram().show()
    for k, v in indf_dict.items():
        fw1.write('%s\t%s\n' % (str(k), str(v)))
    fw1.close()
    
    fw2.write('%s\n' % ','.join([str(v) for v in clustered]))
    fw2.close()