import os
filename='491821654.jpg'
for item in os.listdir('E:\Etsy1\static\es_platform\Picture'):
    if filename==item:
        os.remove('E:\Etsy1\static\es_platform\Picture/'+filename)
        print("delect one data")