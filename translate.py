# -*- coding: utf-8 -*-
import hashlib
import json
import sys
import time
import uuid
from imp import reload

import requests
import xlrd

reload(sys)
# 这是基于有道云的自然语言翻译API

YOUDAO_URL = 'https://openapi.youdao.com/api'
# application ID
APP_KEY = ''
# application key
APP_SECRET = ''


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):
    """
    data中需要设置输入的文体的language ：data['from']
    data目标输出的文体的language ：data['to']
    这里只是单纯的句子的翻译
    :param q: 翻译体string
    :return:
    """
    data = {}
    data['from'] = 'en'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"
    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        return json.loads(response.content).get("translation")[0]


if __name__ == '__main__':
    # 输入是xls文件
    workbook = xlrd.open_workbook(r'D:\detect\english.xls')
    sheet1 = workbook.sheet_by_name('Sheet1')
    cols = sheet1.col_values(0)
    # 输出的md文件
    f = open(r'D:\detect\chinese.md', 'a+')
    for i in range(len(cols)):
        print(cols[i], connect(cols[i]))
        f.write(cols[i] + "\t\t\t\t" + connect(cols[i]) + '  \n')
