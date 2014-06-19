#coding=utf-8
#import re
from nltk import *
from nltk.util import ngrams
from nltk.corpus import PlaintextCorpusReader
from math import log
from os import listdir
import codecs
corpus_dir='/Users/dehao/github/Lydata/ckip/corpus/'
#consider n-grams, 构造一个dict, fileid:<tokens>
#此处语料库的格式是文件夹，里边每个文件为一个分类。
#文件已分好了词，词之间用空格隔开，如：
#马云 催泪 励志 演讲 为什么 你还是 穷人
#谢霆锋 励志 演讲 看完 跟 打了 鸡血 似的
corpus={}
for f in listdir(corpus_dir):
    print f
    fi=codecs.open(corpus_dir+f, 'r', encoding='utf-8')
    grams=[]
    for line in fi:
        sigram=line.strip().split()
        l=len(sigram)
        for cnt in range(l):
            grams.append(sigram[cnt])
            #可加入高阶模型
            #if cnt < l-1:
                #grams.append('%s|%s' % (sigram[cnt], sigram[cnt+1]))
            #if cnt < l-2:
                #grams.append('%s|%s|%s' % (sigram[cnt], sigram[cnt+1], sigram[cnt+2]))
    corpus[f]=grams
    fi.close()
print 'step1 OK'

cfd_dir='/Users/dehao/github/Lydata/ckip/corpus_res/'
cfd=ConditionalFreqDist(
    (topic, word)
    for topic in corpus.keys()
    for word in corpus[topic])

df={}
print 'step2 OK'
#类
topics=cfd.conditions()
sum_topics=len(topics)
#store idf of every word
#df
for topic in topics:
    for k in cfd[topic].keys(): 
        if k not in df:
            df[k]=0
        df[k]+=1
#tf-idf
topic_tf_idf={}
for topic in topics:
    if topic not in topic_tf_idf:
            topic_tf_idf[topic]={}
    sum_tf=len(corpus[topic])
    for k, v in cfd[topic].items():
        topic_tf_idf[topic][k]=float(v)/sum_tf*log(float(sum_topics)/df[k])
#输出到文件夹中，每个文件一个类，里边是依tf-idf倒序排列的主题词，如:
#演讲	0.375399
#励志	0.337192
#马云	0.242213

for topic, tf_idf in topic_tf_idf.items():
    fw=open(cfd_dir+topic, 'w')
    for k, v in sorted(tf_idf.items(), key=lambda x:x[1], reverse = True): 
        if v < 0.05:
            continue
        fw.write('%s\t%f\n' % (k.encode('utf-8'), v))
    fw.close()