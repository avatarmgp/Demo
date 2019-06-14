# -*- coding: UTF-8 -*-
import time
import redis
import sys
import getopt

#统计购物车数量
UNLOGIN_CUSTOMER_ID_LIMIT = 1 << 50

nlcount = 0
lcount = 0

l0t20 = 0
l21t50 = 0
l51t100 = 0
l101t200 = 0
l201t300 = 0
l301t600 = 0

nl0t20 = 0
nl21t50 = 0
nl51t100 = 0
nl101t200 = 0
nl201t300 = 0
nl301t600 = 0

#hash:UserShoppingCart:object: CustomerId:700019501:Gpid:50000002698615:SkuId:4003465547008:ServiceTypeId:1
#0      1               2       3           4       5       6              7        8           9         10       
#CustomerId:600027681:Gpid:50000002700746:SkuId:0:ServiceTypeId:1
#0          1           2   3               4    5   6          7

#执行管道
def execute_pipline(po):
    global nlcount,lcount,l0t20,l21t50,l51t100,l101t200,l201t300,l301t600,nl0t20,nl21t50,nl51t100,nl101t200,nl201t300,nl301t600
    ds = po.execute()
    for d in ds:
        if not d:
            continue
        try:
            if d[b'CustomerId']:
                customerid = int(d[b'CustomerId'])

            if d[b'DefaultCount']:
                defaultCount = int(d[b'DefaultCount'])

            if customerid > UNLOGIN_CUSTOMER_ID_LIMIT:
                nlcount = nlcount + 1
                if defaultCount >= 0 and defaultCount <= 20:
                    nl0t20 = nl0t20 + 1
                elif defaultCount >= 21 and defaultCount <= 50:
                    nl21t50 = nl21t50 + 1
                elif defaultCount >= 51 and defaultCount <= 100:
                    nl51t100 = nl51t100 + 1
                elif defaultCount >= 101 and defaultCount <= 200:
                    nl101t200 = nl101t200 + 1
                elif defaultCount >= 201 and defaultCount <= 300:
                    nl201t300 = nl201t300 + 1
                else:
                    nl301t600 = nl301t600 + 1
            else:
                lcount = lcount + 1
                if defaultCount >= 0 and defaultCount <= 20:
                    l0t20 = l0t20 + 1
                elif defaultCount >= 21 and defaultCount <= 50:
                    l21t50 = l21t50 + 1
                elif defaultCount >= 51 and defaultCount <= 100:
                    l51t100 = l51t100 + 1
                elif defaultCount >= 101 and defaultCount <= 200:
                    l101t200 = l101t200 + 1
                elif defaultCount >= 201 and defaultCount <= 300:
                    l201t300 = l201t300 + 1
                else:
                    l301t600 = l301t600 + 1
        except Exception as e:
            print(e)
            continue

def run(po, ro):
    count = 0
    for key in ro.scan_iter(match = "hash:UserShoppingCartCountCache:object:CustomerId:*", count = 2000):
        try:
            po.hgetall(key)
            count = count + 1
            if count >= 1000:
                execute_pipline(po)
                count = 0
        except Exception as e:
            print(e)

    if count > 0:
        execute_pipline(po)

    print(nlcount,lcount,l0t20,l21t50,l51t100,l101t200,l201t300,l301t600,nl0t20,nl21t50,nl51t100,nl101t200,nl201t300,nl301t600)

def connectRedis(redishost,redisport):
    pool = redis.ConnectionPool(host=redishost, port=redisport, db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline(transaction=False)
    return pipe,r

def main(argv):
    redishost = ""
    redisport = ""
    index = ""
    nologin = False
    try:
      opts, args = getopt.getopt(argv,"h",["rh=","rp="])
    except getopt.GetoptError:
      sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('redis2mysql.py -rh <redis host> -rp <redis port>')
            return
        elif opt == "--rh":
            redishost = arg
        elif opt == "--rp":
            redisport = int(arg)

    po, ro = connectRedis(redishost, redisport)

    run(po,ro)

if __name__ == "__main__":
    main(sys.argv[1:])