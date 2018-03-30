import redis

conn = redis.StrictRedis(host='localhost', port=6379)

# ret = conn.lpush('nba', 'weishao')

ret = conn.lpop('nba')

print(ret)
