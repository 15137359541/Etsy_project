#coding=utf-8
import numpy as np
import matplotlib.mlab as malb
import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
import os
mpl.rcParams['font.sans-serif'] = ['SimHei']
filenames=[]
for item in os.listdir('E:\Etsy1\static\es_platform\Picture'):
    filenames.append(item)

def draw(goodtype,goodnum,goodid):
    filename=goodid+'.jpg'
    #查看一下文件是否已经存在，
    for item in filenames:
        if filename == item:
            os.remove('E:\Etsy1\static\es_platform\Picture/' +filename)
            print("删除一个文件")
    #将文件添加到列表
    filenames.append(filename)
    #X轴，Y轴数据
    x = range(len(goodtype))
    y = goodnum
    plt.plot(x,y,marker="*",label=u"折线图",linewidth=1)
    plt.legend()#让图例生效
    plt.xticks(x,goodtype)
    # plt.figure(figsize=(500,500))

    plt.xlabel('x_zxis')#x轴标签
    plt.ylabel('y_azis')#y轴标签
    plt.title('bar chart')#图标题

    plt.savefig('E:\Etsy1\static\es_platform\Picture/'+goodid+'.jpg')#保存图
    plt.close()
    return "static/es_platform/Picture/"+goodid+'.jpg'
# plt.show()#显示图


