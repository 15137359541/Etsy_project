#coding=utf-8
import threading
from Etsy import getPage
from Etsy import getAllGoodsUrls
threads = []
# url1='https://www.etsy.com/c/bath-and-beauty/skin-care?explicit=1&page='
url1='https://www.etsy.com/c/art-and-collectibles/glass-art?explicit=1&page='
# url2='https://www.etsy.com/c/accessories/hair-accessories?explicit=1&page='
url2='https://www.etsy.com/c/craft-supplies-and-tools/home-and-hobby/woodworking-and-carpentry?explicit=1&page='
# url3='https://www.etsy.com/c/accessories/hats-and-caps?explicit=1&page='

t1 = threading.Thread(target=getPage,args=(1,20,url1))
threads.append(t1)
t2 = threading.Thread(target=getPage,args=(1,20,url2))
threads.append(t2)
# t3 = threading.Thread(target=getPage,args=(1,20,url3))
# threads.append(t3)

# t2 = threading.Thread(target=startbangong)
# threads.append(t2)

if __name__ == '__main__':
    # 对访问到的商品页面匹配，如果访问过，就不在访问
    all_good_id = getAllGoodsUrls()
    for t in threads:
        if t.isAlive() == False:
            t.start()