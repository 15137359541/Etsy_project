# coding=utf-8
import re,uuid
from GetPost import gets,posts
from PIL import Image
from io import BytesIO
num=0
def get_cloth():
    global num
    url='https://www.etsy.com/listing/463076391/'
    res=gets(url=url)

    if res['issuccess'] !=1:
        return None
    else:
        print res['message']

'''自动生成一个唯一的字符串，固定长度为36'''
def unique_str():
    return str(uuid.uuid1())


if __name__=="__main__":
    get_cloth()
