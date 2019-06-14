import re
import urllib.request
def getimg(url,page):
    # 设置头文件，模拟成浏览器爬取网页
    headers = {
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Accept':'text/html,application/xhtml+xml,application/xml;\
    q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    headall = []
    for key,value in headers.items():
        items = (key,value)
        headall.append(items)
    #print(headall)  # 测试点1：输出头文件
    
    # 设置 opener 对象
    opener = urllib.request.build_opener()
    opener.addheaders = headall
    # 将opener对象设置成全局模式
    urllib.request.install_opener(opener)
    string = urllib.request.urlopen(url).read()
    # 将爬取的网页转换成字符串形式
    string = string.decode('utf-8')
    #print(string)  # 测试点2：输出网址的字符串形式
    
    # 构建匹配图片的正则表达式
    pattern = re.compile(r'<img src="//([^\s:;]+\.(\w|/)*(.jpg|.JPEG)?\?imageView2/1/w/150/h/107)"')
    result = pattern.findall(string)
    print(result)  # 测试点3：输出正则表达式匹配的结果
    x = 1
    for item in result:
        img = item
        print(img[0])  # 测试点4：输出真正需要的图片网址
        print('检验--','第'+str(page)+'页的第'+str(x)+'图片')  # 测试点5：测试前面局部代码是否正确
        # 这里的D盘的地址是我保存在我的电脑的本地磁盘地址
        filename = urllib.request.urlretrieve('http://'+img[0],'/Users/sh-ezbuy-007-009/Documents/douban/'+str(page)+'-'+str(x)+'.jpg')
        urllib.request.urlcleanup()
        x += 1
    print('\n结束--','第'+str(page)+'页结束--')  # 测试点6：测试前面局部代码是否正确
    
# 设置循环遍历爬取13页的用户的头像 
for i in range(1,100):
    # 爬取的原网页地址
    url = 'https://www.qiushibaike.com/8hr/page/'+str(i)+'/'
    getimg(url,i)