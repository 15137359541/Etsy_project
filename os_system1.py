#coding=utf8
import os

#从文件夹中选择出文件名
filenames=[]
print len(os.listdir('E:\Etsy1\static\es_platform\Feedback'))
for item in os.listdir('E:\Etsy1\static\es_platform\Feedback'):
    filenames.append(item)
    print item