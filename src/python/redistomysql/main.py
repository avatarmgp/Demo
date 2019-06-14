from rediscluster import StrictRedisCluster
import pymysql
import numpy as np
import time

#########集群方式连接######################
#获取到mysql连接，存入到默认cart
conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="defaultcart", charset="utf8")

nodes = [{"host":"192.168.199.131", "port":"6379"}]
#获取到redis连接，读取数据
r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)

print(time.time())
cursor = conn.cursor()
l = []
sql = "insert into user_shopping_cart(customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,selected,create_date,update_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
for key in r.scan_iter(match = 'hash:UserShoppingCart:object:*', count = 2000):
    d = r.hgetall(key)
    r.execute_command
    if not d:
        continue
    try:
        if d["CustomerId"]:
            customerid = int(d["CustomerId"])
        if d["ServiceTypeId"]:
            servicetypeid = int(d["ServiceTypeId"])
        if d["Gpid"]:
            gpid = int(d["Gpid"])
        skuid = d["SkuId"]
        url = d["Url"]
        if len(url) > 100:
            url = url[0:100]
        remark = d["Remark"]
        if len(remark) > 100:
            remark = remark[0:100]
        if d["CreateDate"]:
            createDate = int(d["CreateDate"])
        if d["Qty"]:
            qty = int(d["Qty"])
        if d["OriginalUnitPrice"]:
            originPrice = int(d["OriginalUnitPrice"])
        if d["UpdateDate"]:
            updateDate = int(d["UpdateDate"])
        selected = 0
        if 'Selected' in d:
            if d["Selected"] == "true":
                selected = 1
            elif d["Selected"] == "false":
                selected = 0
            else:
                selected = int(d["Selected"])
    except Exception as e:
        print(e)
        print(d)
        continue

    l.append([customerid, servicetypeid, gpid, skuid,url,remark,qty,originPrice,selected,createDate,updateDate])
    if len(l) >= 10:
        try:
            cursor.executemany(sql, l)
            conn.commit()
            l.clear()
        except Exception as e:
            print(e)
            print(cursor._last_executed)

    '''
    try:
        cursor.execute(sql, [customerid, servicetypeid, gpid, skuid, url, remark, qty, originPrice, selected, createDate, updateDate])
        conn.commit()
    except Exception as e:
        print(e)
    '''

if len(l) > 0:
    try:
        cursor.executemany(sql, l)
        conn.commit()
        l.clear()
    except Exception as e:
        print(e)
        print(cursor._last_executed)   

cursor.close()       
conn.close()
print(time.time())