import redis
from app.config import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

def get_session_state(call_id: str):
    state = redis_client.hgetall(f"call_state:{call_id}")
    return state if state else {}

def update_session_state(call_id: str, updates: dict):
    redis_client.hset(f"call_state:{call_id}", mapping=updates)
    redis_client.expire(f"call_state:{call_id}", 3600)  # Call lives max 1 hr
