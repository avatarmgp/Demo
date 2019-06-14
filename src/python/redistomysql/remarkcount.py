# -*- coding: UTF-8 -*-
import time
import redis
import sys
import getopt

#匿名用户的购物车数量
UNLOGIN_CUSTOMER_ID_LIMIT = 1 << 50

def execute_pipline(po):
    ds = po.execute()
    for d in ds:
        if not d:
            continue
        try:
            remark = d[b"Remark"]
            if len(remark) > 1000:
                remark = remark[0:1000]

        except Exception as e:
            continue

def run(po, ro):
    count = 0
    for key in ro.scan_iter(match = "hash:UserShoppingCart:object:CustomerId:*", count = 2000):
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
        count = 0

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
            print('remarkcount.py -rh <redis host> -rp <redis port>')
            return
        elif opt == "--rh":
            redishost = arg
        elif opt == "--rp":
            redisport = int(arg)

    po, ro = connectRedis(redishost, redisport)

    run(po,ro)

if __name__ == "__main__":
    main(sys.argv[1:])