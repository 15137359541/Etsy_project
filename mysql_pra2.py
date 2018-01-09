#coding=utf-8
from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')
import re


def getAllGoodsUrls():
    all_good_id = []


    good_all_url = 'select good_url from platformes_goods'
    res = good_sql.fetchall(good_all_url)
    for item in res:
        good_id = re.search('(\d+)', item[0]).group(1)
        all_good_id.append(good_id)
    return all_good_id

all_good_id = getAllGoodsUrls()

good_id_one="105881829"
if good_id_one in all_good_id:
    # print("已经存在路由url: %s"% all_good_id)
    del_good='DELETE FROM platformes_goods WHERE good_id = "%s" '%(good_id_one,)
    print del_good
    res=good_sql.update(del_good)
    print res
    print good_id_one
else:
    print("no")

if __name__=="__main__":
    getAllGoodsUrls()