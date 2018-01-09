# coding=utf-8
"""
比较完善的程序，可以自动删除已存在的数据和图片，添加新的数据
"""

from selenium import webdriver
import requests
# 线程等待着2秒钟，直接操作浏览器的方式，那么我自己在操作浏览器的时候，也会有所停留
import time,re,thread
from feedback2 import getFeedback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')

lock = thread.allocate_lock()

feedBackForeigns=[]

def getAllGoodsUrlsFeedback():
    good_all_url = 'select feedbackId_id from platformes_feedbacks'
    res = good_sql.fetchall(good_all_url)
    for item in res:
        goodId = re.search('(\d+)', item[0]).group(1).strip()
        feedBackForeigns.append(goodId)
    return feedBackForeigns

#从数据库选择url
def getAllGoodsUrls():
    # 获取商品中左右的url
    good_all_url = 'select good_url from platformes_goods'
    res = good_sql.fetchall(good_all_url)
    for item in res[33:]:
        lock.acquire()
        goodId = re.search('(\d+)', item[0]).group(1).strip()
        if goodId in feedBackForeign:
            getfedbackUrl = 'select feedbackUrl from platformes_feedbacks WHERE feedbackId_id = "%s" ' % (goodId,)
            feedbackUrl = good_sql.fetchone(getfedbackUrl)

            del_good = 'DELETE FROM platformes_feedbacks WHERE feedbackId_id = "%s" ' % (goodId,)
            res = good_sql.update(del_good)
            print res
            print('已删除原有的数据')
            print('正在访问：%s' % feedbackUrl[0])
            getFeedback(feedbackUrl[0], goodId)
        else:
            feedBack(item[0])
        lock.release()
    return True
num=34
def feedBack(goodUrl):
    global num
    print("第%s条商品" % num)
    print goodUrl
    num += 1
    # 商品id编号
    goodId = re.search('(\d+)', goodUrl).group(1).strip()
    # 启动谷歌浏览器
    # PhantomJS同谷歌火狐一样，是个没有图形界面的浏览器
    driver = webdriver.PhantomJS()
    try:
        driver.set_page_load_timeout(80)
        driver.get(goodUrl)
        print("得到url...")
        # 隐性等待，最长时间等待20秒，隐性等待对整个driver的周期都起作用，所以只要设置一次即可
        driver.implicitly_wait(10)
        print("开始调用浏览器...")


        # 显示等待,面的代码最多等待 10 秒，超时后就抛出 TimeoutException，假设在第3秒就找到了这个元素，那么也就不会多等剩下的7秒使时间，而是继续执行后续代码。
        # element = WebDriverWait(driver, 10, 0.5).until(ec.presence_of_all_elements_located((By.ID, "reviews")))
        # 找到评论中more按钮，彰显出更多评论
        print("正在找reviews按钮...")
        elem = driver.find_element_by_xpath('//*[@id="reviews"]/div/button')
        print("找到reviews按钮!")
        # 敲回车了
        elem.click()
        time.sleep(1)
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
            f.write("\n")
            f.write(goodUrl)
            f.write(",")

    finally:
        driver.quit()
        # driver.close()    #     driver.close()

if __name__=="__main__":
    #得到评论的所有外键
    feedBackForeign = getAllGoodsUrlsFeedback()
    getAllGoodsUrls()