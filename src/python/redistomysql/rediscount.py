# -*- coding: UTF-8 -*-
import time
import redis
import sys
import getopt

#匿名用户的购物车数量
UNLOGIN_CUSTOMER_ID_LIMIT = 1 << 50

def run(po,ro,idx,nologin):
    count = 0
    for key in ro.scan_iter(match = idx, count = 2000):
        if nologin:
            try:
                s = key.decode()
                keys = s.split(':')
                cid = int(keys[4])
                if cid > UNLOGIN_CUSTOMER_ID_LIMIT:
                    count = count + 1
                    print(key)
            except Exception as e:
                print(e)
                print(key)
        else:
            count = count + 1

    print(count)

def connectRedis(redishost,redisport):
    pool = redis.ConnectionPool(host=redishost, port=redisport, db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline(transaction=False)
    return pipe,r

def str_to_bool(str):
    return True if str.lower() == 'true' or str == '1' else False

def main(argv):
    redishost = ""
    redisport = ""
    index = ""
    nologin = False
    try:
      opts, args = getopt.getopt(argv,"h",["rh=","rp=","idx=","nl="])
    except getopt.GetoptError:
      sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('redis2mysql.py -rh <redis host> -rp <redis port> -mh <mysql host> -mp <mysql port> -mu <mysql user> -mps <mysql password> -mdb <mysql database>')
            return
        elif opt == "--rh":
            redishost = arg
        elif opt == "--rp":
            redisport = int(arg)
        elif opt == "--idx":
            index = arg
        elif opt == "--nl":
            nologin = str_to_bool(arg)

    po, ro = connectRedis(redishost, redisport)

    run(po,ro,index,nologin)

if __name__ == "__main__":
    main(sys.argv[1:])