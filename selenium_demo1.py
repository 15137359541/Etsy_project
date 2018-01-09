# coding=utf-8
from selenium import webdriver
import requests
# 线程等待着2秒钟，直接操作浏览器的方式，那么我自己在操作浏览器的时候，也会有所停留
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 启动谷歌浏览器
# PhantomJS同谷歌火狐一样，是个没有图形界面的浏览器
driver = webdriver.Chrome()
driver.set_page_load_timeout(60)
# driver.implicitly_wait(20)
driver.get('https://www.etsy.com/listing/266972599/agate-and-stained-glass-window-hanging?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-12-12')
#隐性等待，最长时间等待20秒，隐性等待对整个driver的周期都起作用，所以只要设置一次即可

elem = driver.find_element_by_xpath('//*[@id="reviews"]/div/button')
    # 敲回车了
elem.click()
time.sleep(0.5)

try:
    # 浏览器刷新
    # driver.refresh()
    #获取更过评论链接
    elem = driver.find_element_by_xpath('//*[@id="reviews"]/div/div[3]/a')
    #获取到对象，再用一下两种方法可以获取地址
    #  elem.get_property("href")得到的是评论的url
    feedbackUrl= elem.get_attribute("href")
    print feedbackUrl
except:
    print '没有访问到'
finally:
    driver.close()


# print driver.page_source
'''
其他时候可以用，但这里文本不是Read All Reviews
'''
    # locator=(By.LINK_TEXT,'Read All Reviews')
    # try:
    #     WebDriverWait(driver, 20, 0.5).until(ec.presence_of_element_located(locator))
    #     print driver.find_element_by_link_text('Read All Reviews').get_attribute('href')
    # finally:
    #     driver.close()