# coding=utf-8
"""
比较完善的程序，可以自动删除已存在的数据和图片，添加新的数据
"""

from selenium import webdriver
import requests
# 线程等待着2秒钟，直接操作浏览器的方式，那么我自己在操作浏览器的时候，也会有所停留
import time,re,thread
from feedback1 import getFeedback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')

lock = thread.allocate_lock()

feedBackForeigns=[]

def getAllGoodsUrlsFeedback():
    getfedbackUrl = 'select feedbackUrl from platformes_feedbacks WHERE feedbackId_id = "%s" ' % (109248751,)
    feedbackUrl = good_sql.fetchone(getfedbackUrl)
    print feedbackUrl[0]

if __name__=="__main__":
    getAllGoodsUrlsFeedback()