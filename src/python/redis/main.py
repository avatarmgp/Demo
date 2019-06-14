# -*- coding: UTF-8 -*-
#import redis

# 连接某个redis
#r = redis.Redis(host='localhost', port=7001)
#for num in range(0,100):
#    r.set(num, 'junxi')

# 连接redis集群
#!/usr/bin/env python
#coding:utf-8
'''
from rediscluster import StrictRedisCluster
import sys

def redis_cluster():
    redis_nodes = [{'host':'127.0.0.1', 'port':7001},
                    {'host': '127.0.0.1', 'port': 7002},
                    {'host': '127.0.0.1', 'port': 7003},
                    {'host': '127.0.0.1', 'port': 7004},
                    {'host': '127.0.0.1', 'port': 7005},
                    {'host': '127.0.0.1', 'port': 7006}]
    
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception as e:
        print('Reason:', e)
        sys.exit(1)

    redisconn.set('test','test')

redis_cluster()


import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=7001, db=0)
r = redis.Redis(connection_pool = pool)
for num in range(0, 1):
    r.set(num,"test")

from rediscluster import StrictRedisCluster

nodes = [{"host": "192.168.199.131", "port": "6379"}]
r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)

import redis

pool = redis.ConnectionPool(host='192.168.199.131', port=6379, db=0)
r = redis.Redis(connection_pool = pool)

for key in r.scan_iter(match = 'set:UserShoppingCart:CustomerIdOfUserShoppingCartIDXRelation:CustomerId:*', count = 2000):
    print(key)
    members = r.smembers(key)
    for member in members:
        print(member)
import redis

pool = redis.ConnectionPool(host='192.168.199.131', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

for key in r.scan_iter(match='*', count=10):
    print(key)
'''


######################################################
###redis分布式锁#######################################
#-*-coding:utf-8
import redis
import threading

locks = threading.local()
locks.redis = {}

def key_for(user_id):
    return "account_{}".format(user_id)

def _lock(client, key):
    return bool(client.set(key, True, nx=True, ex=5))

def _unlock(client, key):
    client.delete(key)

def lock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] += 1
        return True
    ok = _lock(client, key)
    if not ok:
        return False
    locks.redis[key] = 1
    return True

def unlock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] -= 1
        if locks.redis[key] <= 0:
            del locks.redis[key]
        return True
    return False

client = redis.StrictRedis()
print("lock", lock(client, "codehole"))
print("lock", lock(client, "codehole"))
print("unlock", unlock(client, "codehole"))
print("unlock", unlock(client, "codehole"))