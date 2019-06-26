# -*- coding: UTF-8 -*-

import redis

MasterIpList = ["192.168.199.132:6386", "192.168.199.132:6385", "192.168.199.131:6379", "192.168.199.131:6386", "192.168.199.131:6383", "192.168.199.132:6384"]
KeyList = []
RedisNodes = []
Count = 0

for MasterIp in MasterIpList:
    RedisHost = MasterIp.split(":")[0]
    RedisPort = MasterIp.split(":")[1]
    RedisNodes.append({"host": RedisHost, "port": RedisPort})

    pool = redis.ConnectionPool(host = RedisHost, port = RedisPort, db = 0)
    Conn = redis.Redis(connection_pool = pool)
    for Key in Conn.scan_iter(match='c:60000000000224*', count=100):
        Conn.delete(Key)