#python3
# -*- coding: utf-8 -*-
# File  : baiduAPI.py
# Author: Wang Chao
# Date  : 2018/7/31

import urllib3,base64
from urllib.parse import urlencode
import cv2
import sys
import dlib
size = 64


access_token='24.94e43ed4e1b0b4b178fbbeffafc1e26e.2592000.1535605226.282335-11612325'
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+access_token
#参数image：图像base64编码 以及face_fields参数
def baidu():
    f = open('test.jpg', 'rb')
    img = base64.b64encode(f.read())
    params={'image':''+str(img,'utf-8')+'','image_type':'BASE64','face_field':'age,beauty,faceshape,gender,glasses','max_face_num':10}
    #params={'image':'f7ec8ecd441886371b9749d1fc853f44','image_type':'FACE_TOKEN','face_field':'age,beauty,faceshape,gender,glasses'}
    #params={'image':'https://www.xsshome.cn/face.jpg','image_type':'URL','face_field':'age,beauty,faceshape,gender,glasses'}
    #对base64数据进行urlencode处理
    params=urlencode(params)
    request=http.request('POST',
                          url,
                          body=params,
                          headers={'Content-Type':'application/json'})
    #对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
    result = str(request.data,'utf-8')
    result = eval(result)
    return result
####

detector = dlib.get_frontal_face_detector()
cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    cv2.imwrite('test.jpg',img)
    result = baidu()
    #######
    face_num = len(result['result']['face_list'])
    for i in range(face_num):
        age = result['result']['face_list'][i]['age']
        beauty = result['result']['face_list'][i]['beauty']
        location = result['result']['face_list'][i]['location']
        left_top = (int(location['left']), int(location['top']))
        right_bottom = (left_top[0] + int(location['width']), left_top[1] + int(location['height']))
        cv2.rectangle(img, left_top, right_bottom, (200, 100, 0), 2)
        cv2.putText(img, "age:" + str(age) + " beauty:" + str(beauty), left_top, cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 255), 1)
    cv2.imshow('image', img)
    ########
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        sys.exit(0)
