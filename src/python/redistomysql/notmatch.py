import pymysql
import time
import redis
import sys
import getopt

#########节点方式连接######################
#执行管道
def execute_pipline(pipe,conn,cursor):
    ds = pipe.execute()
    l = []
    for d in ds:
        if not d:
            continue
        try:
            if d[b'CustomerId']:
                customerid = int(d[b'CustomerId'])
            if d[b"ServiceTypeId"]:
                servicetypeid = int(d[b"ServiceTypeId"])
            if d[b"Gpid"]:
                gpid = int(d[b"Gpid"])
            skuid = d[b"SkuId"]
            url = d[b"Url"]
            if len(url) > 100:
                url = url[0:100]
            remark = d[b"Remark"]
            if len(remark) > 100:
                remark = remark[0:100]

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
            print(e)
            #print(d)
            continue

        l.append([customerid, servicetypeid, gpid, skuid,url,remark,qty,originPrice,selected,createDate,updateDate])
    try:
        cursor.executemany(sql, l)
        conn.commit()
        l.clear()
    except Exception as e:
        print(e)
        #print(cursor._last_executed)

#开始执行导入
def run(conn, pipe, r):
    count = 0
    cursor = conn.cursor()
    for key in r.scan_iter(match = '[^hash:UserShoppingCart:object:]*', count = 2000):
        pipe.hgetall(key)
        count = count + 1
        if count >= 1000:
            execute_pipline(pipe,conn,cursor)
            count = 0

    if count > 0:
        execute_pipline(pipe,conn,cursor) 

    cursor.close()       
    conn.close()

#连接redis
def connectRedis(redishost,redisport):
    pool = redis.ConnectionPool(host=redishost, port=redisport, db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline(transaction=False)
    return pipe,r

#连接mysql
def connectMysql(host, port, user, password, db):
    print(host,port,user,password,db)
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, charset="utf8")
    return conn

def main(argv):
    mysqlhost = ""
    mysqlport = 0
    mysqluser = ""
    mysqlpass = ""
    mysqldb = ""
    redishost = ""
    redisport = ""
    try:
      opts, args = getopt.getopt(argv,"h",["rh=","rp=","mh=","mp=","mu=","mps=","mdb="])
    except getopt.GetoptError:
      print('redis2mysql.py -rh <redis host> -rp <redis port> -mh <mysql host> -mp <mysql port> -mu <mysql user> -mps <mysql password> -mdb <mysql database>')
      sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('redis2mysql.py -rh <redis host> -rp <redis port> -mh <mysql host> -mp <mysql port> -mu <mysql user> -mps <mysql password> -mdb <mysql database>')
            return
        elif opt == "--rh":
            redishost = arg
        elif opt == "--rp":
            redisport = int(arg)
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
    
    conn = connectMysql(mysqlhost, mysqlport, mysqluser, mysqlpass, mysqldb)
    pipe, r = connectRedis(redishost, redisport)

    start = time.time()
    run(conn, pipe, r)
    print(time.time()-start)

if __name__ == "__main__":
    main(sys.argv[1:])