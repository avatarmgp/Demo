import pymysql
import time

sql = "insert into user_shopping_cart(customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,selected,create_date,update_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
sql2 = "select * from user_shopping_cart where customer_id=%s and service_type_id=%s and gpid=%s and sku_id=%s"
#并发插入
conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", database="defaultcart", charset="utf8")
'''
def many_insert(count):
    cursor = conn.cursor()
    for i in range(count):
        if i%1000==0:
            l = []
            for j in range(1000):
                l.append([i+j, 1, 1, 'sss', 'www.baidu.com', 'remark', 1, 1, 1, 111111111, 1111111])
            cursor.executemany(sql, l)
            conn.commit()

start = time.time()
many_insert(10000000)
print(time.time() - start)
'''

#并发查询
def man_query(count):
    cursor = conn.cursor()
    for i in range(count):
        l = [1,1,1,'sss']
        cursor.execute(sql2, l)
    print(conn.commit())

start = time.time()
man_query(10000)
print(time.time() - start)