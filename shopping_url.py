# coding=utf-8
import re
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
num=0

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
        print detail_res["message"]
        # 简单处理详情页面
        html = detail_res['message'].replace('\n', '').replace('\r', '').replace('\t', '')
        #图片
        img_url = re.search('data-full-image-href="(.*?)"', html)
        # print('图片地址：',img_url.group(1))
        if img_url:
            img_path=get_path(img_url.group(1))
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


        #评论和喜欢的人
        feedback_loved=re.search('<a href="#reviews">(.*?) reviews</a>(.*?)Favorited by: <a href="(.*?)">(.*?) people</a>', html)
        if feedback_loved:
            feedback=float((feedback_loved.group(1)))
            favorited=float(feedback_loved.group(4))
        else:
            feedback,favorited="no feedback",'no favorited'

        #店铺名和店铺url；
        shopNameUrl=re.search('<a itemprop="url" href="(.*?)"><span itemprop="title">(.*?)</span></a>',html)
        #店铺名加载的较慢，第一次没有找到的话，在给他0.5时间
        if shopNameUrl:
            #商电名
            shop_name=shopNameUrl.group(2)
            #商电url:
            shop_url=shopNameUrl.group(1)
        else:
            time.sleep(0.5)
            shopNameUrl = re.search('<a itemprop="url" href="(.*?)"><span itemprop="title">(.*?)</span></a>', html)
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
        # count=pollMysql(goodId,title, price_ago, price_now, feedback, favorited, img_path,url,label_one,label_two,shop_name,shop_url,source_time)
        #写入文件
        with open("con_es.txt","a")as f:
            f.write('商品id:%s' %goodId)
            f.write('商电名：%s '% shop_name)

            f.write("图片：%s  "% img_path)
            f.write("标题：%s  "%  title)
            f.write("现价：%s  "% price_now)
            f.write("原价：%s  "%  price_ago)
            f.write("评论：%s  "% feedback)
            f.write("收藏：%s  "%  favorited)
            f.write('label_one:%s' % label_one)
            f.write('label_two:%s' % label_two)
            f.write('商品url:%s '% url)
            f.write('商电url：%s ' % shop_url)
            f.write("\n")

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
def get_path(img_url):
    res=gets(url=img_url)
    if res['issuccess'] !=1:
        return None
    else:
        # 图片格式如.jpg
        img_format = img_url.split('.')[-1]
        # 得到唯一一个字符串
        unique_s = unique_str()
        # 图片名
        img_name = unique_s + '.' + img_format
        # 路径
        img_path = 'E:\Etsy1\static\es_platform\img/' + img_name
        img_content = Image.open(BytesIO(res['message']))
        img_content.save(img_path)
        return "static/es_platform/img/"+img_name

#加入数据库
# def pollMysql(goodId,title,price_ago,price_now,feedback,favorited,img,url,label_one,label_two,shop_name,shop_url,source_time):
#     good_sql=SqlHelper(host='localhost',port=3306,db='etsy',user='root',password='123456')
#     good_one='insert into platformes_goods(good_id,title,price_ago,price_now,feedback,favorited,img,good_url,label_one,label_two,shop_name,shop_url,source_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#     good_one_name=(goodId,title,price_ago,price_now,feedback,favorited,img,url,label_one,label_two,shop_name,shop_url,source_time)
#     count=good_sql.update(good_one,good_one_name)
#     return count

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

#更多评论：
def feedBack(goodUrl):
    # 启动谷歌浏览器
    # PhantomJS同谷歌火狐一样，是个没有图形界面的浏览器
    driver = webdriver.Chrome()
    driver.get(goodUrl)
    try:
        # 显示等待,面的代码最多等待 10 秒，超时后就抛出 TimeoutException，假设在第3秒就找到了这个元素，那么也就不会多等剩下的7秒使时间，而是继续执行后续代码。
        element = WebDriverWait(driver, 10, 0.5).until(ec.presence_of_all_elements_located((By.ID, "reviews")))
    finally:
        # 找到评论中more按钮，彰显出更多评论
        elem = driver.find_element_by_xpath('//*[@id="reviews"]/div/button')
        # 敲回车了
        elem.click()
        time.sleep(0.5)
        # 获取更过评论链接
        elem = driver.find_element_by_xpath('//*[@id="reviews"]/div/div[3]/a')
        # 获取到对象，再用一下两种方法可以获取地址
        #  elem.get_property("href")
        feedbackUrl = elem.get_attribute("href")
        return feedbackUrl

if __name__=="__main__":
    url="https://www.etsy.com/listing/105881829/personalized-birch-vase-wedding-gift?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery_8"
    goods_list(url)

    '''
    re.search匹配结果中，只有一个匹配，结果位res,则res.group(0)代表匹配的整个内容，即html网页，res.group(n)得到的是匹配选择的第n个内容
    re.findall,是一个符合条件的列表，没有group直说，如果是想得到res中第二个元组中的第二个内容，为res[2][2]
    '''