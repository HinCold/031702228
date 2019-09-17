# encoding=utf-8
import re
import time
import requests
import json
#1!张三,福建福州闽13599622362侯县上街镇福州大学10#111.


#print(s0[:1])
#匹配等级
def getlevel(s0):
    level = s0[0]
    #print(level)
    s1 = s0[1:]
    return level, s1
#匹配姓名
def getname(s1):

    #t2 = time.time()
    rout = re.search(r'!(.+?),', s1)
    name = rout.group()
    pos = rout.span()
    name = name[1:-1]
    s2 = s1[pos[1]:]
    return name, s2

#匹配手机号
def gettelnumber(s2):
    rp = re.search(r'\d{11}', s2)
    if rp == None:
        telnumber = ''
        s3 = s2
    else:
        telnumber = rp.group()
        pos = rp.span()
        #print(pos)
        s3 = s2[0:pos[0]] + s2[pos[1]:]
        #print(s3)
    return telnumber, s3

#seg_list = jieba.cut(s3, cut_all=False)
#print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

#地址划分 gd的api
def geocodapi(s3):
    url = "https://restapi.amap.com/v3/geocode/geo?key=891fc6769c45ed042ef6729dde41fb28"

    u = url + "&address=" + s3

    wb = requests.get(u).text
    content = json.loads(wb)
    #soup = BeautifulSoup(wb)
    #print(content)
    #print(content["geocodes"])
    return content
#逆向地理编码
def regecodapi(position):
    #position = content["geocodes"][0]["location"]
    rurl = "https://restapi.amap.com/v3/geocode/regeo?output=JSON&key=891fc6769c45ed042ef6729dde41fb28&radius=100&extensions=base"

    ru = rurl + "&location=" + position

    respond = requests.get(ru).text
    respond = json.loads(respond)
    #print(respond)
    return respond
#信息处理
def togetherrules(s3, level, content, respond, name, telnumber):
    if level == "1":
        #township doornumber
        city = content["geocodes"][0]["city"]
        township = respond["regeocode"]["addressComponent"]["township"]
        rt = re.search(r"." + township, s3)
        district = content["geocodes"][0]["district"]
        province = content["geocodes"][0]["province"]
        if city == '':
            city = content["geocodes"][0]["province"]
        if city == "北京市" or city == "天津市" or city == "重庆市" or city == "上海市":
            province = province[:-1]
        if rt == None:
              township = ''
              rdt = re.search(r"." + district, s3)
              if rdt == None:
                  district = ''
                  rc = re.search(r"." + city, s3)
                  tpos = rc.span()
              else:
                  tpos = rdt.span()
        else:
            tpos = rt.span()
        s4 = s3[tpos[1]:-1]
        imformation = {

            "姓名": name,
            "手机": telnumber,
            "地址": [

                province,
                city,
                district,
                township,
                s4
            ]
        }

    elif level == '2':
        #print(1111111)
        district = content["geocodes"][0]["district"]
        city = content["geocodes"][0]["city"]
        township = respond["regeocode"]["addressComponent"]["township"]
        rd = re.search(r'\d+号', s3)
        road = respond["regeocode"]["addressComponent"]["streetNumber"]["street"]
        rt = re.search(r"." + township, s3)
        rdt = re.search(r"." + district, s3)
        province = content["geocodes"][0]["province"]
        if city == "北京市" or city == "天津市" or city == "重庆市" or city == "上海市":
            province = province[:-1]
        if rdt == None:
            district = ''
        if rt == None:
            township = ''
        if city == '':
            city = content["geocodes"][0]["province"]
        if rd == None:
            doornumber = ''
            road = ''
            if rt == None:
                township = ''

                if district == '':

                    rc = re.search(r"." + city, s3)
                    dpos = rc.span()
                else:
                    dpos = rdt.span()

            else:
                dpos = rt.span()
        else:
            doornumber = rd.group()
            dpos = rd.span()
        s4 = s3[dpos[1]:-1]

        imformation = {

            "姓名": name,
            "手机": telnumber,
            "地址": [

                province,
                city,
                district,
                township,
                road,
                doornumber,
                s4
            ]
        }
    else:
        district = content["geocodes"][0]["district"]
        city = content["geocodes"][0]["city"]
        township = respond["regeocode"]["addressComponent"]["township"]
        road = respond["regeocode"]["addressComponent"]["streetNumber"]["street"]
        rd = re.search(r'\d+号', s3)
        province = content["geocodes"][0]["province"]
        if city == "北京市" or city == "天津市" or city == "重庆市" or city == "上海市":
            province = province[:-1]
        if rd == None:
            doornumber = ''

            rt = re.search(r"." + township, s3)
            if rt == None:

                rdt = re.search(r"." + district, s3)
                if rdt == None:

                    rc = re.search(r"." + city, s3)
                    dpos = rc.span()
                else:
                    dpos = rdt.span()

            else:
                dpos = rt.span()
        else:
            doornumber = rd.group()
            dpos = rd.span()
        s4 = s3[dpos[1]:-1]
        imformation = {

            "姓名": name,
            "手机": telnumber,
            "地址": [

                province,
                city,
                district,
                township,
                road,
                doornumber,
                s4
            ]
        }

    jdata = json.dumps(imformation, ensure_ascii=False)
    print(jdata)

#1!张三,福建福州闽13599622362侯县上街镇福州大学10#111.
s0 = input()
level, s1 = getlevel(s0)
name, s2 = getname(s1)
tel, s3 = gettelnumber(s2)
content = geocodapi(s3)
position = content["geocodes"][0]["location"]
respond = regecodapi(position)
togetherrules(s3, level, content, respond, name, tel)
