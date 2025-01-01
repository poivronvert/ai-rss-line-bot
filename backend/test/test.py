import redis

try:
    redis_client = redis.Redis(host='130.211.241.254', port=6379, password=None)
    print("Trying to ping Redis...")
    response = redis_client.ping()
    print(f"Redis ping response: {response}")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
