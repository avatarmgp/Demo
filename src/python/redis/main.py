# -*- coding: UTF-8 -*-
import redis

r = redis.Redis(host='localhost', port=6379)
for num in range(0,100000):
    r.set(num, 'junxi')