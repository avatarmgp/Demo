#-*-coding:utf-8-*-
import pymysql
import time
import redis
import sys
import getopt
import logging
from rediscluster import StrictRedisCluster

#########节点方式连接######################
sql = "insert into user_shopping_cart(customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,selected,create_date,update_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE customer_id=values(customer_id),service_type_id=values(service_type_id),gpid=values(gpid),sku_id=values(sku_id),url=values(url),remark=values(remark),qty=values(qty),original_unit_price=values(original_unit_price),selected=values(selected),create_date=values(create_date),update_date=values(update_date);"
UNLOGIN_CUSTOMER_ID_LIMIT = 1 << 50
unloginCustomerCartExpire = 24 * 3600
nologinCount = 0
loginCount = 0

def keyOfObject(customerid,gpid,skuid,servicetypeid):
    return "hash:UserShoppingCart:object:CustomerId:" + str(customerid) + ":Gpid:" + str(gpid) + ":SkuId:" + str(skuid) + ":ServiceTypeId:" + str(servicetypeid)
def keyOfSet(customerid):
    return "set:UserShoppingCart:CustomerIdOfUserShoppingCartIDXRelation:CustomerId:" + str(customerid)
def valOfSet(customerid, gpid, skuid, servicetypeid):
    return "CustomerId:" + str(customerid) + ":Gpid:" + str(gpid) + ":SkuId:" + str(skuid) + ":ServiceTypeId:" + str(servicetypeid)
'''
def keyOfZSet(customerid,gpid,skuid,servicetypeid):
    return "zset:UserShoppingCart:CustomerIdGpidSkuIdServiceTypeIdOfUserShoppingCartRNGRelation:CustomerId:" + str(customerid) + ":Gpid:" + str(gpid) + ":SkuId:" + str(skuid) + ":ServiceTypeId:" + str(servicetypeid)
def valOfZSet(customerid,gpid,skuid,servicetypeid):
    return "CustomerId:" + str(customerid) + ":Gpid:" + str(gpid) + ":SkuId:" + str(skuid) + ":ServiceTypeId:" + str(servicetypeid)
'''

def keyOfCountObject(customerid):
    return "hash:UserShoppingCartCountCache:object:CustomerId:" + str(customerid)
def keyOfCountSet(customerid):
    return "set:UserShoppingCartCountCache:CustomerIdOfUserShoppingCartCountCacheIDXRelation:CustomerId:" + str(customerid)
def valueOfCountSet(customerid):
    return "CustomerId:" + str(customerid)

'''
def keyOfCountZSet(customerid):
    return "zset:UserShoppingCartCountCache:CustomerIdOfUserShoppingCartCountCacheRNGRelation:CustomerId:" + str(customerid)
def valOfCountZSet(customerid):
    return "CustomerId:" + str(customerid)
'''

#保存匿名用户到redis
#[customerid, servicetypeid, gpid, skuid, url, remark, qty, originPrice, selected, createDate, updateDate]
def save_nologin_customer(rl,pnl):
    for r in rl:
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "CustomerId", str(r[0]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "ServiceTypeId", str(r[1]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "Gpid", str(r[2]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "SkuId", str(r[3]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "Url", str(r[4]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "Remark", str(r[5]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "Qty", str(r[6]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "OriginalUnitPrice", str(r[7]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "CreateDate", str(r[9]))
        pnl.hset(keyOfObject(r[0],r[2],r[3],r[1]), "UpdateDate", str(r[10]))
        pnl.hset(keyOfObject(r[0],r[2], r[3], r[1]), "Selected", str(r[8]))
        pnl.sadd(keyOfSet(r[0]), valOfSet(r[0], r[2], r[3], r[1]))
        #pnl.zadd(keyOfZSet(r[0], r[2], r[3], r[1]), float(r[1]), valOfZSet(r[0], r[2], r[3], r[1]))
        pnl.expire(keyOfObject(r[0],r[2], r[3], r[1]), unloginCustomerCartExpire)
    pnl.execute()

#保存到购物车count新的redis
#[customerid,normalcount,primecount,defaultcount,b4mcount]
def save_cart_count(l, pc):
    for r in l:
        pc.hset(keyOfCountObject(r[0]), "CustomerId", str(r[0]))
        pc.hset(keyOfCountObject(r[0]), "NormalCount", str(r[1]))
        pc.hset(keyOfCountObject(r[0]), "PrimeCount", str(r[1]))
        pc.hset(keyOfCountObject(r[0]), "DefaultCount", str(r[1]))
        pc.hset(keyOfCountObject(r[0]), "B4MCount", str(r[1]))
        pc.sadd(keyOfCountSet(r[0]), valueOfCountSet(r[0]))
        #pc.zadd(keyOfCountZSet(r[0]), float(r[0]), valOfCountZSet(r[0]))
        pc.expire(keyOfCountObject(r[0]), unloginCustomerCartExpire)
    pc.execute()

#执行管道
def execute_pipline1(conn,cursor,po,pn):
    ds = po.execute()
    ml = []
    rl = []
    global nologinCount
    global loginCount
    for d in ds:
        if not d:
            continue
        try:
            if d[b'CustomerId']:
                customerid = int(d[b'CustomerId'])
                if customerid <= 0:
                    continue
            if d[b"ServiceTypeId"]:
                servicetypeid = int(d[b"ServiceTypeId"])
            if d[b"Gpid"]:
                gpid = int(d[b"Gpid"])
            skuid = d[b"SkuId"]
            url = d[b"Url"]
            if len(url) > 1000:
                url = url[0:1000]
            remark = d[b"Remark"]
            if len(remark) > 1000:
                remark = remark[0:1000]

            createDate = 0
            if d[b"CreateDate"]:
                createDate = int(d[b"CreateDate"])

            if d[b"Qty"]:
                qty = int(d[b"Qty"])
            if d[b"OriginalUnitPrice"]:
                originPrice = int(d[b"OriginalUnitPrice"])
            if d[b"UpdateDate"]:
                updateDate = int(d[b"UpdateDate"])
            selected = 0
            if b'Selected' in d:
                if d[b"Selected"] == b"true":
                    selected = 1
                elif d[b"Selected"] == b"false":
                    selected = 0
                else:
                    selected = int(d[b"Selected"])
        except Exception as e:
            writeLog(e)
            writeLog(d)
            continue

        if customerid <= 0:
            continue
        elif customerid <= UNLOGIN_CUSTOMER_ID_LIMIT:
            ml.append([customerid, servicetypeid, gpid, skuid, url, remark, qty, originPrice, selected, createDate, updateDate])
            loginCount = loginCount + 1
        else:
            rl.append([customerid, servicetypeid, gpid, skuid, url, remark, qty, originPrice, selected, createDate, updateDate])
            nologinCount = nologinCount + 1
    try:
        if len(ml) > 0:
            '''
            for m in ml:
                try:
                    cursor.execute(sql, m)
                except Exception as e:
                    print(e)
            '''

            cursor.executemany(sql,ml)
            conn.commit()
    except Exception as e:
        writeLog(e)
    try:
        if len(rl) > 0:
            save_nologin_customer(rl,pn)
    except Exception as e:
        writeLog(e)

def execute_pipline2(po,pc):
    ds = po.execute()
    l = []
    for d in ds:
        if not d:
            continue
        try:
            if d[b'CustomerId']:
                customerid = int(d[b'CustomerId'])
            if d[b"NormalCount"]:
                normalCount = int(d[b"NormalCount"])
            if d[b"PrimeCount"]:
                primeCount = int(d[b"PrimeCount"])
            if d[b"DefaultCount"]:
                defaultCount = int(d[b"DefaultCount"])
            if d[b"B4MCount"]:
                b4mCount = int(d[b"B4MCount"])
            l.append([customerid, normalCount, primeCount, defaultCount, b4mCount])
            
        except Exception as e:
            writeLog(e)
            writeLog(d)
            continue
    try:
        if len(l) > 0:
            save_cart_count(l,pc)
    except Exception as e:
        writeLog(e)

#导入购物车
def exportCart(conn, cursor, ro, po, pnl):
    global nologinCount
    global loginCount
    totalcount = 0
    count = 0
    for key in ro.scan_iter(match = 'hash:UserShoppingCart:object:*', count = 2000):
        po.hgetall(key)
        count = count + 1
        if count >= 1000:
            execute_pipline1(conn, cursor, po, pnl)
            totalcount = totalcount + count
            count = 0

    if count > 0:
        execute_pipline1(conn, cursor, po, pnl)
        totalcount = totalcount + count
    
    writeLog("购物车总数:{0}".format(totalcount))
    writeLog("登录用户购物车总数:{0}".format(loginCount))
    writeLog("未登录用户购物车总数:{0}".format(nologinCount))
    
#导入购物车计数
def exportCartCount(ro, po, pc):
    totalcount = 0
    count = 0
    for key in ro.scan_iter(match = 'hash:UserShoppingCartCountCache:object:CustomerId:*', count = 2000):
        po.hgetall(key)
        count = count + 1
        if count >= 1000:
            execute_pipline2(po, pc)
            totalcount = totalcount + count
            count = 0

    if count > 0:
        execute_pipline2(po, pc)
        totalcount = totalcount + count
    
    writeLog("购物车数量总数:{0}".format(totalcount))

#开始执行导入
def run(conn,po,ro,pnl,pc):
    count = 0
    cursor = conn.cursor()
    print("exportCart")
    exportCart(conn, cursor, ro, po, pnl)
    print("exportCartCount")
    exportCartCount(ro, po, pc)
    print("run finish")

    cursor.close()       
    conn.close()

#连接redis
def connectRedis(redishost,redisport):
    pool = redis.ConnectionPool(host=redishost, port=redisport, db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline(transaction=False)
    return pipe, r
    
#连接redis集群
def connectRedisCluster(redishost, redisport):
    try:
        cluster = StrictRedisCluster(startup_nodes=[{'host':redishost, 'port':redisport}])
        return cluster.pipeline(transaction=False)
    except Exception as e:
        print("connectRedisCluster Error:",e)
        sys.exit(1)

#连接mysql
def connectMysql(host, port, user, password, db):
    print(host,port,user,password,db)
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, charset="utf8")
    return conn

#初始化日志
def initLog(host, port):
    logging.basicConfig(filename='./log/{0}_{1}.log'.format(host,port),format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level = logging.INFO,filemode='a',datefmt='%Y-%m-%d%I:%M:%S %p')

#写入日志
def writeLog(log):
    logging.info(log)

#答应日志
def main(argv):
    mysqlhost = ""
    mysqlport = 0
    mysqluser = ""
    mysqlpass = ""
    mysqldb = ""
    redishost = ""
    redisport = ""
    redishost2 = ""
    redisport2 = ""
    redishost3 = ""
    redisport3 = ""
    try:
      opts, args = getopt.getopt(argv,"h",["rh=","rp=","rhnl=","rpnl=","rhc=","rpc=","mh=","mp=","mu=","mps=","mdb="])
    except getopt.GetoptError:
      print('redis2mysql.py -rh <redis host> -rp <redis port> -rhnl <redis nologin host> -rpnl <redis nologin port> -rhc <redis count host> -rpc <redis count port> -mh <mysql host> -mp <mysql port> -mu <mysql user> -mps <mysql password> -mdb <mysql database>')
      sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('redis2mysql.py -rh <redis host> -rp <redis port> -rhnl <redis nologin host> -rpnl <redis nologin port> -rhc <redis count host> -rpc <redis count port> -mh <mysql host> -mp <mysql port> -mu <mysql user> -mps <mysql password> -mdb <mysql database>')
            return
        elif opt == "--rh":
            redishost = arg
        elif opt == "--rp":
            redisport = int(arg)
        elif opt == "--rhnl":
            redishost2 = arg
        elif opt == "--rpnl":
            redisport2 = int(arg)
        elif opt == "--rhc":
            redishost3 = arg
        elif opt == "--rpc":
            redisport3 = int(arg)
        elif opt == "--mh":
            mysqlhost = arg
        elif opt == "--mp":
            mysqlport = int(arg)
        elif opt == "--mu":
            mysqluser = arg
        elif opt == "--mps":
            mysqlpass = arg
        elif opt == "--mdb":
            mysqldb = arg
    
    initLog(redishost, redisport)

    conn = connectMysql(mysqlhost, mysqlport, mysqluser, mysqlpass, mysqldb)
    po, ro = connectRedis(redishost, redisport)     #旧的redis
    pnl = connectRedisCluster(redishost2, redisport2)    #存放匿名用户购物车的redis
    pc = connectRedisCluster(redishost3, redisport3)      #存放购物车数量的redis

    start = time.time()
    run(conn, po, ro, pnl, pc)
    writeLog("迁移耗时:{0}".format(time.time()-start))

if __name__ == "__main__":
    main(sys.argv[1:])