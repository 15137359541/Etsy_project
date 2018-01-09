# coding=utf-8
import re,uuid,os,datetime
from GetPost import gets,posts
from PIL import Image
from io import BytesIO
from templates_mysql import SqlHelper
num=1
#从文件夹中选择出文件名
filenames=[]
for item in os.listdir('E:\Etsy1\static\es_platform\Feedback'):
    filenames.append(item)

def getFeedback(url,goodNum):
    global num
    feedbackUrl=url
    getTime=datetime.datetime.now()
    for page in range(1,3):
        url=url+'&page='+str(page)
        # print('第%s轮评论'% page)
        # print url
        res=gets(url=url)

        if res['issuccess'] !=1:
            return None
        else:
            # print res['message']
            html =res['message'].replace('\n', '').replace('\r', '').replace('\t', '')
            #需要多每一个评论总体做处理
            feedbacks=  re.findall(' <div class="flag-body pb-xs-0">(.*?)show-xs',html)
            for feedback in feedbacks:
                print("第%s条评论"% num)
                num+=1
                #评论时间
                feedbacktime=feedBackTime(feedback)
                #评论图片和题目
                feedbackPicture,feedbackTitle,goodId=feedbackPictureTitle(feedback)
                #加入数据库
                pollMysql(goodId,feedbackTitle,feedbackPicture,feedbacktime,goodNum,feedbackUrl,getTime)
                # 写入文件
                # with open("con_es1.txt", "a")as f:
                #     f.write('外键的编号：%s'% goodNum)
                #     f.write('编号：%s'% goodId)
                #     f.write('时间：%s ' % feedbacktime)
                #     f.write("图片：%s  " % feedbackPicture)
                #     f.write("标题：%s  " % feedbackTitle)
                #     f.write("\n")
    return True

#对评论进行处理
def feedBackTime(html):
    feedbackTime= re.search('<p class="shop2-review-attribution">(.*?)> on(.*?)</p>',html)
    feedbackTime=feedbackTime.group(2).strip()
    return feedbackTime
#对评论的图片和标题做处理
def feedbackPictureTitle(feedback):
    pictureTitle=re.search('<div class="flag-img">                <a href="(.*?)" title="(.*?)" class(.*?)<div class="card-img-wrap">                        <img src="(.*?)"',feedback)
    if pictureTitle:
        #商品id
        goodId=pictureTitle.group(1).strip()
        #获取id号
        goodId=re.search('(\d+)',goodId).group(1).strip()
        feedbackPictureUrl=pictureTitle.group(4).strip()
        #图片保存
        feedbackPicture=get_path(feedbackPictureUrl,goodId)
        feedbackTitle=pictureTitle.group(2).strip()
        return feedbackPicture,feedbackTitle,goodId
    else:
        return 'no picture','no title','no id'
# 图片保存
# def get_path(img_url):
#     res=gets(url=img_url)
#     if res['issuccess'] !=1:
#         return None
#     else:
#         # 图片格式如.jpg
#         img_format = img_url.split('.')[-1]
#         # 得到唯一一个字符串
#         unique_s = unique_str()
#         # 图片名
#         img_name = unique_s + '.' + img_format
#         # 路径
#         img_path = 'E:\Etsy1\static\es_platform\img/' + img_name
#         img_content = Image.open(BytesIO(res['message']))
#         img_content.save(img_path)
#         return "static/es_platform/img/"+img_name
def get_path(img_url,goodId):
    res=gets(url=img_url)
    if res['issuccess'] !=1:
        return None
    else:
        # 图片格式如.jpg
        img_format = img_url.split('.')[-1]
        # 图片名
        img_name = goodId + '.' + img_format
        try:
            for item in filenames:
                if img_name == item:
                    os.remove('E:/Etsy1/static/es_platform/Feedback/'+img_name)
        except Exception as e:
            print "没有这个图片"
            print e
        #将文件添加到文件列表中
        filenames.append(img_name)
        # 路径
        img_path = 'E:\Etsy1\static\es_platform/Feedback/'+img_name
        img_content = Image.open(BytesIO(res['message']))
        img_content.save(img_path)
        return "static/es_platform/Feedback/"+img_name

'''自动生成一个唯一的字符串，固定长度为36'''
def unique_str():
    return str(uuid.uuid1())
#加入数据库
def pollMysql(good_id,feedbackTitle,feedbackPicture,feedbackTime,feedbackId_id,feedbackUrl,getTime):
    good_sql=SqlHelper(host='localhost',port=3306,db='etsy',user='root',password='123456')
    good_one='insert into platformes_feedbacks(good_id,feedbackTitle,feedbackPicture,feedbackTime,feedbackId_id,feedbackUrl,getTime) value(%s,%s,%s,%s,%s,%s,%s)'
    good_one_name=(good_id,feedbackTitle,feedbackPicture,feedbackTime,feedbackId_id,feedbackUrl,getTime)
    count=good_sql.update(good_one,good_one_name)
    return count


if __name__=="__main__":
    url='https://www.etsy.com/shop/HappyPartyDecor/reviews?ref=l2-see-more-feedback'
    good_id='483462689'
    getFeedback(url,good_id)