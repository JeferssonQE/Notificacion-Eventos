# Redis handler placeholder
import redis
from app.core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL)

# Example function


def cache_set(key, value, ex=3600):
    r.set(key, value, ex=ex)


def cache_get(key):
    return r.get(key)
