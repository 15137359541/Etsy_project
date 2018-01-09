# coding=utf-8
from selenium import webdriver
import requests
# 线程等待着2秒钟，直接操作浏览器的方式，那么我自己在操作浏览器的时候，也会有所停留
import time,re,thread
from feedback import getFeedback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')

lock = thread.allocate_lock()
#从数据库选择url
def getAllGoodsUrls():
    # 获取商品中左右的url
    good_all_url = 'select good_url from platformes_goods'
    res = good_sql.fetchall(good_all_url)
    for item in res:
        lock.acquire()
        feedBack(item[0])
        lock.release()
    return True

def feedBack(goodUrl):
    # 商品id编号
    goodId = re.search('(\d+)', goodUrl).group(1).strip()
    # 启动谷歌浏览器
    # PhantomJS同谷歌火狐一样，是个没有图形界面的浏览器
    driver = webdriver.PhantomJS()
    driver.get(goodUrl)
    # 隐性等待，最长时间等待20秒，隐性等待对整个driver的周期都起作用，所以只要设置一次即可
    driver.implicitly_wait(20)
    try:
        # 显示等待,面的代码最多等待 10 秒，超时后就抛出 TimeoutException，假设在第3秒就找到了这个元素，那么也就不会多等剩下的7秒使时间，而是继续执行后续代码。
        element = WebDriverWait(driver, 10, 0.5).until(ec.presence_of_all_elements_located((By.ID, "reviews")))
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
        # 通过评论地址获取更多评论
        getFeedback(feedbackUrl, goodId)
        return True
    except:
        with open('error.txt','a')as f:
            f.write(goodUrl)
    finally:
        driver.close()    #     driver.close()
if __name__=="__main__":
    getAllGoodsUrls()