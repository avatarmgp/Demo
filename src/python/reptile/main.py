# -*- coding: utf-8 -*-
import requests
import json
from urllib.request import urlretrieve

headers = {'authorization':'Bearer Mi4xQXN3S0F3QUFBQUFBUUVJSjdTempDaGNBQUFCaEFsVk5BQzRmV3dDVVJzeU9NOWxNU0pZT1BNdFJ5bTlrSzk3MU1B|1513218048|1e03f7e7f26825482a72e4a629ef80292847548e',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'x-udid':'AEBCCe0s4wqPToZZF6LV3roAjT8uEikZF1k=',
           }   #请求头
urls = ['https://www.zhihu.com/api/v4/members/feifeimao/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_' \
      'followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'.format(i*20) for i in range (0,5)]
img_urls = []   #用来存所有的img_url
for url in urls:
    datas = requests.get(url,headers = headers).json()["data"]   #获取json文件下的data
    for it in datas:
        img_url = it['avatar_url']   #获取头像url
        img_urls.append(img_url)      #把获取的url依次放入img_urls

    i = 0   #计数
    for it in img_urls:
        urlretrieve(it,'D://%s.jpg' % i)   #通过url,依次下载头像，并保存于D盘
        i = i+1   #i依次累加