# coding=utf-8
from templates_mysql import SqlHelper
from drawing import draw
import re,time,datetime
from templates_mysql import SqlHelper
good_sql = SqlHelper(host='localhost', port=3306, db='etsy', user='root', password='123456')

dictGoodId={}
def pollMysql():
    good_all_url='select feedbackTime,feedbackId_id from platformes_feedbacks'
    res=good_sql.fetchall(good_all_url)
    # print res
    # print len(res)
    item3=[]
    item6=[]
    item9=[]
    item12=[]
    item15 = []
    item18 = []
    item21 = []
    item24 = []
    item27 = []
    item30 = []
    item33 = []
    itemOther=[]
    for item in res:
        goodTime=item[0]
        # goodId=item[1]
        #处理日期,转化为时间戳
        timeStamp=allGoodTime(goodTime)
        # 根据时间戳以三天一个段，总结商品个数
        if time.time()>timeStamp>agoTimeStamp(3):
            item3.append(item)
        elif agoTimeStamp(3)>=timeStamp>agoTimeStamp(6):
            item6.append(item)
        elif agoTimeStamp(6)>=timeStamp>agoTimeStamp(9):
            item9.append(item)
        elif agoTimeStamp(9)>=timeStamp>agoTimeStamp(12):
            item12.append(item)
        elif agoTimeStamp(12)>=timeStamp>agoTimeStamp(15):
            item15.append(item)
        elif agoTimeStamp(15)>=timeStamp>agoTimeStamp(18):
            item18.append(item)
        elif agoTimeStamp(18)>=timeStamp>agoTimeStamp(21):
            item21.append(item)
        elif agoTimeStamp(21)>=timeStamp>agoTimeStamp(24):
            item24.append(item)
        elif agoTimeStamp(24)>=timeStamp>agoTimeStamp(27):
            item27.append(item)
        elif agoTimeStamp(27)>=timeStamp>agoTimeStamp(30):
            item30.append(item)
        elif agoTimeStamp(30)>=timeStamp>agoTimeStamp(33):
            item33.append(item)
        else:
            itemOther.append(item)


    for i3 in item3:
        allGoodId(i3[1], 3)
    for i6 in item6:
        allGoodId(i6[1], 6)
    for i9 in item9:
        allGoodId(i9[1],9)
    for i12 in item12:
        allGoodId(i12[1],12)
    for i15 in item15:
        allGoodId(i15[1],15)
    for i18 in item18:
        allGoodId(i18[1],18)
    for i21 in item21:
        allGoodId(i21[1],21)
    for i24 in item24:
        allGoodId(i24[1],24)
    for i27 in item27:
        allGoodId(i27[1],27)
    for i30 in item30:
        allGoodId(i30[1],30)
    for i33 in item33:
        allGoodId(i33[1],33)
    for oth in itemOther:
        allGoodId(oth[1], 100)
        #处理商品id
        # allGoodId(goodId)
    # print dictGoodId
    savePicture(dictGoodId)

#处理日期
def allGoodTime(goodTime):
    #将字符串‘Dec 29, 2017’转换成12,29,2017
    list1={"Dec":"12,","Nov":"11,","Oct":"10,","Sep":'9,',"Aug":"8,","Jul":"7,","Jun":"6,","May":"5,","Apr":"4,","Mar":"3,","Feb":"2,","Jan":"1,"}
    for key,value in list1.iteritems():
        goodTime=re.sub(key,value,goodTime)
        goodTime=re.sub(' ','',goodTime)
        #将字符创转换成时间数组
    timeArray=time.strptime(goodTime,"%m,%d,%Y")
    # print timeArray
    #转换成时间戳
    timeStamp= time.mktime(timeArray)
    return timeStamp


#以当前时间为基础，获得几天前的时间戳
def agoTimeStamp(dayAgo):
    #先获得时间数组格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=dayAgo))
    #转换为时间戳:
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    return timeStamp
#处理id
def allGoodId(goodId,day):
    if goodId in dictGoodId:
        if day in dictGoodId[goodId]:
            dictGoodId[goodId][day]=[dictGoodId[goodId][day][0] + 1]
        else:
            dictGoodId[goodId][day]=[1]
    else:
        dictGoodId[goodId]={day:[1]}
    return dictGoodId

#将数据保存为图片
def savePicture(dictGoodId):
    for key,value in dictGoodId.iteritems():
        #这两个列表至关重要，不能放在其他循环那里
        goodDayType = []
        goodDayNum = []
        goodDay={}
        #给每一个值赋值0
        days=[3,6,9,12,15,18,21,24,27,30,33,100]
        for i in range(len(days)):
            goodDay[days[i]]=[0]
        for key1,value1 in value.iteritems():
            if key1 in goodDay:
                goodDay[key1]=value1
        #对数据进行一个排序，按照时间来，否则会是乱序，但字典没有顺序asd[0]根据键排序，asd=[1]根据值排序
        goodDay=sorted(goodDay.iteritems(), key=lambda asd: asd[0], reverse=True)
        # print goodDay
        #获取一个月的数据
        for key2, value2 in goodDay[1:]:
            goodDayType.append(key2)
            goodDayNum.append(value2[0])
        #数据整理好之后开始画图：
        pic_path=draw(goodDayType,goodDayNum,key)
        print pic_path
        sqlAdd(pic_path,key)


#将图表插入到商品表里面
#加入数据库
def sqlAdd(picPath,key):

    good_one='update platformes_goods set chart=%s where good_id = %s'
    good_one_name=(picPath,key)
    count=good_sql.update(good_one,good_one_name)
    return count




if __name__=="__main__":
    pollMysql()