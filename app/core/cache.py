import json
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cache(key: str, value):
    serialized = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status
        }
        for t in value
    ]
    redis_client.setex(key, 60, json.dumps(serialized))


def delete_cache(key: str):
    redis_client.delete(key)