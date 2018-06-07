# -*- coding:utf-8 -*-
import re
import random

a = 1

def getInsertStr(path, city):
    global a
    with open(path, "r") as fp:
        dataStr = fp.read()


    nameArr = re.findall(r' alt=""(.*?)"> </span>', dataStr)
    nameArr = list(nameArr)
    addressArr = re.findall(r'<i>地址：</i><span class="limit-address">(.*?)</span><a class="J_miniMap"', dataStr)
    addressArr = list(addressArr)
    phoneArr = re.findall(r'<i>电话：</i>(.*?)</div>', dataStr)
    phoneArr = list(phoneArr)
    scoreArr = re.findall(r'评分：<strong>(.*?)</strong></div>', dataStr)
    scoreArr = list(scoreArr)

    hallNum = [5,6,7,8,9,10]
    serviceCharge = [1,1.1,1.2,2]
    astrict = [5,10,20]
    flag = [0,1]

    num = 0
    while num <= 9:
        district = addressArr[num].split("区")[0]
        values = '"'+nameArr[num]+'","'+city+'","'+district+'","'+addressArr[num]+'","'+phoneArr[num]+'",'+scoreArr[num]+','+str(random.choice(hallNum))+','+str(random.choice(serviceCharge))+','+str(random.choice(astrict))+','+str(1)
        insertStr = "insert into cinemas(name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag) values("+ values +");"
        print(insertStr)
        num += 1
        # print(a)
        # a += 1


t = 1
while t <= 11:
    path = "cinema"+str(t)
    city = "深圳"
    if t == 11:
        city = "北京"
    getInsertStr(path, city)
    t += 1


