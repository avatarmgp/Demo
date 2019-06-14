# coding=utf-8
'''
本代码为自动抓取豆瓣top100电影代码
@pre_url url地址前缀，在这里为http://movie.douban.com/top250?start=
@top_urls url地址池
@top_tag 为抓取电影名正则表达式
'''
 
import urllib.request
import re
 
pre_url = 'http://movie.douban.com/top250?start='
top_urls = []
top_tag = re.compile(r'<span class="title">(.+?)</span>')
top_content = []
top_num = 1
 
# ----------确定url地址池------------
# 因为top100，每页25部电影，故为4页,从零开始
for num in range(10):
  top_urls.append(pre_url + str(num * 25))
 
 
# ------------抓取top100电影名称，并打印输出----------
top_tag = re.compile(r'<span class="title">(.+?)</span>')
for url in top_urls:
  content = urllib.request.urlopen(url).read()
  content = content.decode('utf-8')
  pre_content = re.findall(top_tag, content)
  # 过滤并打印输出
  for item in pre_content:
    if item.find(' ') == -1:
      print('Top' + str(top_num) + '  ' + item)
      top_num += 1