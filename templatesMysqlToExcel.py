#coding=utf-8
import xlwt
import pymysql

def export(host,port,dbname,user,password,tabel_name,outputpath):
    #链接数据库
    conn=pymysql.connect(host=host,port=port,db=dbname,user=user,password=password,charset="utf8")
    # 游标
    cursor = conn.cursor()

    count = cursor.execute("select * from "+tabel_name)
    # print count
    #重置游标位置
    cursor.scroll(0,mode="absolute")
    #获取所有的查询结果
    results=cursor.fetchall()
    # print "输出结果："
    # print results
    # print '输出结束'
    #获取mysql里面数据字段名称以及字段信息
    fields=cursor.description
    print "数据字段名称："
    print fields

    workbook=xlwt.Workbook()
    print workbook

    sheet = workbook.add_sheet('table_message',cell_overwrite_ok=True)
    print sheet

    #写上字段信息
    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field][0])


    #写上获取的数据段信息
    for row in range(1,len(results)+1):
        for col in range(0,len(fields)):
            sheet.write(row,col,results[row-1][col])

    workbook.save(outputpath)

if __name__=="__main__":
    export(host='localhost',port=3306,dbname="etsy",user="root",password="123456",tabel_name='platformes_goods',outputpath=r'./etsy1.xlsx')