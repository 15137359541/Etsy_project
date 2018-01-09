# coding=utf-8
"""
可以更新数据页面，重新爬取时，会删除原来的，获取新的内容
"""
import re,threading,os
from GetPost import gets,posts
import uuid
from PIL import Image
from io import BytesIO
from selenium import webdriver
import requests
# 线程等待着2秒钟，直接操作浏览器的方式，那么我自己在操作浏览器的时候，也会有所停留
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')

#从数据库选择url
def getAllGoodsUrls():
    all_good_id = []

    # 获取商品中左右的url
    good_all_url = 'select good_url from platformes_goods'
    res = good_sql.fetchall(good_all_url)
    for item in res:
        good_id = re.search('(\d+)', item[0]).group(1)
        all_good_id.append(good_id)
    return all_good_id

#从文件中选择文件名
def getAllFilenames():
    # 从文件夹中选择出文件名
    filenames = []
    for item in os.listdir('E:\Etsy1\static\es_platform\img'):
        filenames.append(item)
    return filenames



#可以定量爬取页面数
def getPage(start_page,end_page,url):
    for page in range(start_page, end_page+1):
        url=url+str(page)
        get_cloth(url)
num=0
def get_cloth(url):
    global num,all_good_id
    res=gets(url=url)

    if res['issuccess'] !=1:
        return None
    else:
        # print res["message"]

        # 简单处理页面
        html =res['message'].replace('\n', '').replace('\r', '').replace('\t', '')
        list_urls=re.findall('<a        class=" display-inline-block listing-link"(.*?)href="(.*?)"',html)

        if len(list_urls) > 0 :
            for ever_url in list_urls:
                every_url=ever_url[1]
                num +=1
                print("目前访问第%s个网页：%s,"% (num,every_url))
                good_id_one = re.search('(\d+)', every_url).group(1)
                # print("________")
                # print good_id_one
                # print all_good_id
                # print("+++++++++")
                if good_id_one in all_good_id:
                    # print("已经存在路由url: %s"% every_url)
                    del_good = 'DELETE FROM platformes_goods WHERE good_id = "%s" ' % (good_id_one,)
                    res = good_sql.update(del_good)
                    print('已删除原有的数据')
                    #重新获取数据
                    # 对得到的地址做进一步的处理
                    res = goods_list(every_url)
                    all_good_id.append(good_id_one)
                else:
                    #对得到的地址做进一步的处理
                    res=goods_list(every_url)
                    # # 将url添加到所有的商品的列表当中
                    all_good_id.append(good_id_one)


        else:
            print '没有这个网页'
#商品详情页
def goods_list(url):
    detail_res=gets(url=url)
    if detail_res['issuccess'] !=1:
        # print(detail_res['issuccess'])
        print '没有这个网址'
        return None

    else:
        #商品id编号
        goodId = re.search('(\d+)', url).group(1).strip()
        # print detail_res["message"]
        # 简单处理详情页面
        html = detail_res['message'].replace('\n', '').replace('\r', '').replace('\t', '')
        #图片
        img_url = re.search('data-full-image-href="(.*?)"', html)
        # print('图片地址：',img_url.group(1))
        if img_url:
            img_path=get_path(img_url.group(1),goodId)
        else:
            img_path="no picture"

        #标题
        title=re.search('<span itemprop="name">(.*?)</span>',html)
        if title:
            title=title.group(1)
        else:
            title='no title'
        # 价格,第一种情况，拥有现价，原价
        try:
            price=re.search('<span id="listing-price" class="vertical-align-middle ">        <span>(.*?)</span>        <strike class="text-gray-lighter text-smallest normal">(.*?)</strike>',html)

            price_now=price.group(1).strip()
            if "+" in price_now:
                #对于价格去$ +符号转为整数处理
                price_now=float(price_now[price_now.index('$')+1:][:price_now.index("+")-1])
            else:
                price_now = float(price_now[price_now.index('$') + 1:])
            #
            # 对于价格去$ +符号
            price_ago=price.group(2).strip()
            if "+" in price_ago:
                price_ago=float(price_ago[price_ago.index('$')+1:][:price_ago.index("+")-1])
            else:
                price_ago = float(price_ago[price_ago.index('$') + 1:])
        #价格，第二种情况，没有原价，只有现价
        except:
            try:
                price = re.search(
                    '<span id="listing-price" class="vertical-align-middle ">(.*?)<meta itemprop="currency" content="USD"/>',
                    html)
                price_now=price.group(1).strip()
                if "+" in price_now:
                    # 对于价格去$ +符号转为整数处理
                    price_now = float(price_now[price_now.index('$') + 1:][:price_now.index("+") - 1])
                else:
                    price_now = float(price_now[price_now.index('$') + 1:])

                price_ago=price.group(1).strip()
                if "+" in price_ago:
                    price_ago=float(price_ago[price_ago.index('$')+1:][:price_ago.index("+")-1])
                else:
                    price_ago = float(price_ago[price_ago.index('$') + 1:])
            except:
                price_ago,price_now=0,0


        #评论和喜欢的人
        feedback_loved=re.search('<a href="#reviews">(.*?) reviews</a>(.*?)Favorited by: <a href="(.*?)">(.*?) people</a>', html)
        if feedback_loved:
            feedback=float((feedback_loved.group(1)))
            favorited=float(feedback_loved.group(4))
        else:
            feedback,favorited="no feedback",'no favorited'

        #店铺名和店铺url；
        shopNameUrl=re.search('<a itemprop="url" href="(.*?)"><span itemprop="title">(.*?)</span></a>',html)
        #店铺名有两种匹配规则
        if shopNameUrl:
            #商电名
            shop_name=shopNameUrl.group(2)
            #商电url:
            shop_url=shopNameUrl.group(1)
        else:
            shopNameUrl = re.search('<a class="text-gray-darker" itemprop="url" href="(.*?)"><span itemprop="title">(.*?)</span></a>', html)
            if shopNameUrl:
                # 商电名
                shop_name = shopNameUrl.group(2)
                # 商电url:
                shop_url = shopNameUrl.group(1)
            else:
                shop_name,shop_url='no shop',''

        #标签label：
        try:
            label_one,label_two=getLabel(html)
        except:
            label_one,label_two='no label','no label'

        #添加爬取的时间
        source_time=datetime.now()

        #加入数据库
        count=pollMysql(goodId,title, price_ago, price_now, feedback, favorited, img_path,url,label_one,label_two,shop_name,shop_url,source_time)
        #写入文件
        # with open("con_es.txt","a")as f:
        #     f.write('商品id:%s' %goodId)
        #     f.write('商电名：%s '% shop_name)
        #
        #     f.write("图片：%s  "% img_path)
        #     f.write("标题：%s  "%  title)
        #     f.write("现价：%s  "% price_now)
        #     f.write("原价：%s  "%  price_ago)
        #     f.write("评论：%s  "% feedback)
        #     f.write("收藏：%s  "%  favorited)
        #     f.write('label_one:%s' % label_one)
        #     f.write('label_two:%s' % label_two)
        #     f.write('商品url:%s '% url)
        #     f.write('商电url：%s ' % shop_url)
        #     f.write("\n")

        '''
        search得到的是对象如<_sre.SRE_Match object at 0x0300E770>
        加.group(0)显示匹配的所有字段
        .group(1)显示组一，以后一次类推
        '''

    return detail_res["issuccess"]

# def poll_mysql(img,title,price,feedback_loved):

'''自动生成一个唯一的字符串，固定长度为36'''
def unique_str():
    return str(uuid.uuid1())
# 图片保存
def get_path(img_url,goodId):
    res=gets(url=img_url)
    if res['issuccess'] !=1:
        return None
    else:

        # 图片格式如.jpg
        img_format = img_url.split('.')[-1]
        # 图片名
        img_name = goodId + '.' + img_format
        for item in filenames:
            if img_name == item:
                os.remove('E:\Etsy1\static\es_platform\img/'+img_name)
        #将文件添加到文件列表中
        filenames.append(img_name)
        # 路径
        img_path = 'E:\Etsy1\static\es_platform\img/'+img_name
        img_content = Image.open(BytesIO(res['message']))
        img_content.save(img_path)
        return "static/es_platform/img/"+img_name

#加入数据库
def pollMysql(goodId,title,price_ago,price_now,feedback,favorited,img,url,label_one,label_two,shop_name,shop_url,source_time):

    good_one='insert into platformes_goods(good_id,title,price_ago,price_now,feedback,favorited,img,good_url,label_one,label_two,shop_name,shop_url,source_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    good_one_name=(goodId,title,price_ago,price_now,feedback,favorited,img,url,label_one,label_two,shop_name,shop_url,source_time)
    count=good_sql.update(good_one,good_one_name)
    return count

#标签处理；
def getLabel(html):
    #匹配到所有的标签中的网页
    label_html = re.search('<ul id="listing-tag-list">(.*?)</ul>', html)
    #匹配到的是每一个标签的内容
    label_list = re.findall('<a href="(.*?)">(.*?)</a>', label_html.group(0))
    label_content=[]
    for label in label_list:
        label_content.append(label[1])
    label=','.join(label_content)

    #label长度太长，超过255，即数据库的字段长度，一分为二
    label_one = label.split(',')[:int(len(label.split(',')) / 2)]
    label_one = ','.join(label_one)

    label_two = label.split(',')[int(len(label.split(',')) / 2) + 1:]
    label_two = ','.join(label_two)
    return label_one,label_two


if __name__=="__main__":
    # #获得操作系统中的所有图片
    filenames=getAllFilenames()
    # 对访问到的商品页面匹配，如果访问过，就不在访问
    all_good_id = getAllGoodsUrls()

    page_start=int(raw_input("请输入起始页："))
    page_end=int(raw_input("请输入终止页："))
    # url=raw_input("请输入网址：")
    url='https://www.etsy.com/c/art-and-collectibles/glass-art?explicit=1&page='
    getPage(page_start,page_end,url)



    '''
    re.search匹配结果中，只有一个匹配，结果位res,则res.group(0)代表匹配的整个内容，即html网页，res.group(n)得到的是匹配选择的第n个内容
    re.findall,是一个符合条件的列表，没有group之说，如果是想得到res中第二个元组中的第二个内容，为res[2][2]
    '''